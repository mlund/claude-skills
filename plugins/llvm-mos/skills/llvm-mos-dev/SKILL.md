---
name: llvm-mos-dev
description: Develop, debug, test, and review the llvm-mos toolchain itself — the MOS backend in llvm/lib/Target/MOS, the MC layer (encoder, relaxation, disassembler, InstPrinter, MCInstrAnalysis), lld/ELF/Arch/MOS.cpp relocations, MOS tablegen, the mos-sim simulator in llvm-mos-sdk, and MOS runs of llvm-test-suite. Use this skill when the work is on the compiler rather than with it: adding or fixing an instruction, opcode, relocation, fixup, or PC-relative convention; running or interpreting llvm/test/MC/MOS, llvm/test/CodeGen/MOS or lld/test/ELF/*mos* lit tests; bisecting a miscompile between compiler builds; preparing or reviewing an llvm-mos PR. The sibling skill `llvm-mos` covers *using* the toolchain to build 6502 programs; this one covers changing it.
---

# llvm-mos-dev

Working on llvm-mos means working inside an LLVM monorepo where all but a few
dozen files are irrelevant. Two things follow, and they cause most of the wasted
effort: **never search the monorepo at large**, and **never trust a build
directory you did not just rebuild**.

## Where MOS actually lives

Everything else in `llvm/` and `lld/` is noise for this work. Scope every grep
to these paths.

| Area | Path |
|---|---|
| Backend | `llvm/lib/Target/MOS/` |
| MC layer | `llvm/lib/Target/MOS/MCTargetDesc/` — `MOSAsmBackend`, `MOSInstPrinter`, `MOSMCInstrAnalysis`, `MOSMCInstLower`, `MOSMCELFStreamer`, `MOSMCTargetDesc.h` |
| Tablegen | `MOSInstrFormats.td` (operand and instruction classes, TSFlags), `MOSInstrInfo.td` (real ISA), `MOSInstrGISel.td` / `MOSInstrLogical.td` (generic/pseudo), `MOSCombine.td` |
| Disassembler / parser | `llvm/lib/Target/MOS/{Disassembler,AsmParser}/` |
| Linker | `lld/ELF/Arch/MOS.cpp` |
| ELF flags | `EF_MOS_ARCH_*` in `llvm/include/llvm/BinaryFormat/ELF.h`; merge and compatibility logic in `llvm/lib/BinaryFormat/MOSFlags.cpp` |
| Tests | `llvm/test/MC/MOS/`, `llvm/test/CodeGen/MOS/`, `lld/test/ELF/*mos*.s` |

Two sibling repos complete the picture: **llvm-mos-sdk** (`utils/sim/mos-sim.c`
and `fake6502.c` — the simulator the test suite runs under) and
**llvm-test-suite** (MOS subset gated by `ARCH STREQUAL "MOS"`).

## Establish the local setup before building anything

The paths below are per-machine and this skill deliberately does not guess them.
Look first in project memory, `CLAUDE.md`/`AGENTS.md`, and the obvious siblings
of the current repo; if they are still unknown, **ask the user once, up front**,
rather than discovering each one through a failed command:

- the **build directory** and its generator, and whether builds must be capped
  (`ninja -j<N>`) to keep the machine usable
- the **installed toolchain prefix** that the test suite and any `mos-*-clang`
  invocation actually use — it is usually *not* the build tree, so a rebuild has
  no effect until the binaries are copied there
- whether the checked-out **llvm-mos-sdk** simulator supports the CPU mode you
  need (`mos-sim --help`), and which branch it lives on
- for a differential sweep, whether **llvm-test-suite** has a CPU knob, or only
  the default 6502 configuration

Record the answers in memory rather than re-asking each session, and note which
of these are local branches not present in a fresh clone.

## The stale-build trap

A single `build/` shared across branches will hand you failures that belong to
neither the tree nor the branch — a test file from branch A checked against a
binary built from branch B. They look exactly like real regressions and they
will send you on a long hunt.

Before believing any lit result after a branch switch or a `git stash`, rebuild
the tool that test actually drives:

| Test directory | Tool to rebuild |
|---|---|
| `llvm/test/MC/MOS` | `llvm-mc`, `llvm-objdump` |
| `llvm/test/CodeGen/MOS` | `llc` |
| `lld/test/ELF/*mos*` | `lld`, plus `llvm-mc`, `llvm-objdump`, `llvm-objcopy`, `llvm-readelf` |

A tool that is simply *absent* from `build/bin` also fails tests for reasons
unrelated to the code (`'llvm-objcopy': command not found`, `'split-file':
command not found`). Build it and re-run before diagnosing anything.

**Run each suite in its own lit invocation.** Passing LLVM and lld paths to one
`llvm-lit` command silently drops the lld arguments — the run reports a plausible
total and a clean result while never executing the lld tests at all. Check that
the discovered count matches the sum of the suites you meant to run.

### LTO and plugin provenance

The executable that drives a test is not always the component whose source was
changed. Full-LTO links can run the target backend from code linked into the
linker or its plugin, so rebuilding a standalone backend tool may not affect an
end-to-end result. Rebuild the component that actually performs code generation
and confirm its timestamp or version before interpreting the result. When
switching branches, also verify that the compiler, linker, SDK libraries, and
simulator belong to the intended build rather than relying on a shared install.

## One convention, four implementations

The defect pattern that recurs in this backend: a rule about encoding is fixed
in one place and left stale in the others. When you change how an instruction's
operand is encoded or resolved, sweep **all four**:

1. **Encoder / fixups** — `MOSAsmBackend::applyFixup`,
   `getRelativeMOSPCCorrection`, `fixupNeedsRelaxationAdvanced`
2. **Relaxation** — `MOSAsmBackend::relaxInstructionTo` (returns 0 when a CPU
   has no wider form, which is how non-65CE02 targets keep 8-bit branches)
3. **Linker** — `lld/ELF/Arch/MOS.cpp` `relocate()`, one `case` per `R_MOS_*`
4. **Disassembly** — *both* `MOSMCInstrAnalysis::evaluateBranch` (the symbolic
   annotation) and `MOSInstPrinter::printBranchOperand` (the printed address)

Fixing 1 without 3 ships a toolchain that contradicts itself: assembler-resolved
and linker-resolved fixups of the same instruction disagree, and no real CPU can
execute both.

**Corollary — disassembly is not an oracle.** Two of these being wrong in
opposite directions produces output that looks self-consistent: a wrong address
labelled with the right symbol. Only execution distinguishes them.

## lld sees merged flags, not per-object ones

`MOS::calcEFlags()` ORs the `EF_MOS_ARCH_*` bits of every input, and
`checkEFlagsCompatibility` (`MOSFlags.cpp`) rejects only SWEET16/SPC700 mixes.
So any per-CPU decision inside `lld/ELF/Arch/MOS.cpp` is approximate: in a mixed
link both CPUs' bits are set. The assembler side has no such problem — it reads
the per-fragment `MCSubtargetInfo`.

Also note the arch bits are additive by design: a `mos4510` or `mos45gs02`
object also carries `EF_MOS_ARCH_65CE02` (asserted in `lld/test/ELF/basic-mos.s`),
so one bit test covers the family.

## Tablegen facts that are not discoverable by reading

- **`OperandType` is load-bearing.** The AsmWriter emitter passes `Address` to a
  `PrintMethod` only when the operand's type is `MCOI::OPERAND_PCREL`. Retyping
  a PC-relative operand to a target-specific type silently changes the generated
  call to the 3-argument form and the build fails in `MOSGenAsmWriter.inc`.
- **Carry target-specific facts in TSFlags instead.** The pattern already exists:
  `bit MLow = 0; … let TSFlags{0} = MLow;` in `MOSInstrFormats.td`, with matching
  constants in the `MOS::TSFlag` enum in `MCTargetDesc/MOSMCTargetDesc.h`, read
  as `Desc.TSFlags & MOS::TSFlagX`. Adding a bit is three small edits and lets a
  `let Flag = 1 in { … }` block mark a whole instruction family declaratively,
  instead of an opcode list that has to be maintained in two consumers.
- `MCInstPrinter` already holds `MII`, so a print method can consult
  `MII.get(MI->getOpcode())` for `TSFlags` and `getSize()`.

## Verifying a claim about the ISA

Datasheets disagree with silicon often enough that the convention in this
project is to cite more than one source. For 6502-family behaviour: the CPU
datasheet, the MEGA65 FPGA core (`gs4510.vhdl`), the `xemu` emulator
(`cpu65.c`), and pagetable.com's references. A commit message that names two
independent sources survives review; one that says "per the datasheet" does not.

## The verification ladder

Work up it — each rung catches what the one below cannot.

1. **MC** — `llvm-mc … --filetype=obj` then `llvm-objdump -d`. Assert the raw
   encoding *and* the resolved target; asserting only the encoding leaves the
   two disassembly consumers untested.
2. **lld** — a `lld/test/ELF/` case. To force a *linker*-resolved relocation
   rather than an assembler-resolved fixup, put the branch and its target in
   **different sections**; the assembler then cannot resolve it and emits a
   reloc. (`-mos-force-pcrel-reloc`, used in `lld/test/ELF/mos-relocs.s`, is the
   other lever.)
3. **CodeGen** — `llc -mtriple=mos -run-pass=… ` against a `.mir`, or a `.ll`
   with `-mcpu=`. Regenerate expectations with `update_mir_test_checks.py`.
4. **Runtime** — the only rung that proves the bytes execute correctly. Build a
   test under llvm-test-suite and run it under `mos-sim`.

### Designing a runtime probe

Make a wrong result a *wrong answer*, never a crash or a hang — CI cannot
distinguish a hang from a slow test. Arrange for the failure path to execute
valid code: e.g. for an off-by-one branch, place a one-byte, observable
instruction (`inx`) immediately before the intended target, so landing early
increments X and the program still returns cleanly with a different exit code.

llvm-test-suite conventions for a MOS-only test: a directory added from its
parent `CMakeLists.txt` under `if(ARCH STREQUAL "MOS")`, containing
`llvm_singlesource(PREFIX "…")` and a `<name>.reference_output`. `exit 0` alone
is a valid reference output, which keeps the image small — worth doing, since
pulling in `printf` changes code layout.

## Differential sweeps

The strongest signal available: run the whole MOS `SingleSource` corpus at two
CPUs and diff. Anything passing at 6502 and failing at the other is a codegen
bug candidate; anything aborting on an unimplemented opcode is a simulator gap.

`cmake` argument order matters — **`-D` before `-C`**, or the cache file's
`FATAL_ERROR` on a missing `LLVM_MOS` fires before your `-D` is seen:

```sh
cmake -G Ninja -B <dir> -S <llvm-test-suite> \
      -DLLVM_MOS=<sdk-install> -DTEST_SUITE_SUBDIRS=SingleSource \
      -DMOS_CPU=mos65ce02 \
      -C <llvm-test-suite>/cmake/caches/target-mos.cmake
```

`MOS_CPU` drives the compiler's `-mcpu` *and* the `mos-sim` mode together, so
the simulated CPU cannot disagree with the compiled one. Note that ninja does
not know the linker changed: after installing a new `lld`, delete the test
executables or the sweep silently re-reports stale results.

## Simulator caveat

`fake6502.c` fills all 256 opcode slots and points unimplemented ones at `nop()`,
with no undefined-opcode detection. A program using instructions the simulator
does not know therefore executes silently and wrongly instead of failing. Treat
any "hang" or bizarre behaviour under `mos-sim` as a suspected simulator gap
before blaming the compiler.

## Bisecting a miscompile cheaply

Rebuilding clang takes minutes; swapping binaries takes seconds. Keep `.bak`
copies of `clang-23` and `lld` from the known-good build and swap them into the
installed toolchain to isolate which component changed behaviour. When comparing
two binaries, diff **address-normalised** disassembly — a one-instruction size
change shifts every subsequent address and buries the real delta. Instruction
counts from a simulator trace (`--trace`) are a fast way to tell "lost output"
from "diverged control flow".

## Contributing upstream

Before finalizing a fix, inspect related open changes touching the same
convention or source hunk. A neighboring change may add diagnostics, tests, or
an intentionally temporary XFAIL and may be designed to rebase on this fix.
Keep complementary changes separate, but make their tests compose cleanly.

Commit subject is a short imperative with a bracketed component tag — `[MOS] …`,
`[65CE02] …`, `[sim] …`. Match the file's own formatting rather than the repo
`.clang-format` where the two differ: `utils/sim/fake6502.c` carries
`// clang-format off` and its own vendored Fake6502 layout, while `mos-sim.c`
is LLVM-formatted.

Build parallelism is worth capping explicitly on a laptop; a full-width LLVM
build will saturate the machine.
