---
name: llvm-mos-dev
description: Develop and test the llvm-mos compiler backend, assembler, linker, and SDK simulator. Use for toolchain-source changes, MOS regression tests, and compiler-build bisection, rather than application development.
---

# llvm-mos-dev

Use this skill when changing or diagnosing the toolchain itself. Read the
reference matching the affected subsystem, not every workflow.

## Locate the implementation

Start searches in these paths, then widen into shared LLVM infrastructure,
Clang, or SDK code when dependencies require it.

| Area | Starting path |
|---|---|
| Backend and TableGen | `llvm/lib/Target/MOS/` |
| Encoding, fixups, instruction analysis | `llvm/lib/Target/MOS/MCTargetDesc/` |
| Assembly parsing and disassembly | `llvm/lib/Target/MOS/{AsmParser,Disassembler}/` |
| Linker relocations | `lld/ELF/Arch/MOS.cpp` |
| Architecture flags | `llvm/include/llvm/BinaryFormat/ELF.h`, `llvm/lib/BinaryFormat/MOSFlags.cpp` |
| Regression tests | `llvm/test/{MC,CodeGen}/MOS/`, `lld/test/ELF/*mos*` |
| SDK simulator | `utils/sim/` in llvm-mos-sdk |
| Runtime corpus | MOS configuration in llvm-test-suite |

## Identify the tools

Discover relevant source/build directories, generator, installed prefix, and
resource limits from project instructions and local configuration. Ask only for
missing information needed now; a source review does not need a simulator setup.
Keep discovered paths in the working context, without requiring persistent-memory
or configuration writes.

Identify the actual compiler, linker, resource directory, libraries, and simulator
used by the failing command. Rebuild affected tools after source or branch changes;
rebuilding `llc` alone does not refresh an LTO backend running inside the linker.
Use separate build/install prefixes for comparisons. Do not replace binaries in a
shared installation merely to run a bisection.

## Check shared assumptions

For encoding or PC-relative changes, check assembler fixups, relaxation, linker
relocation, and both printed and symbolically annotated disassembly targets.
A successful assembler/disassembler round trip is not independent proof.

For register or layout changes, audit aliases, reservations, spills, call lowering,
interrupt handling, and every producer of linker-defined symbols. An isolated pass
test cannot establish that earlier or later passes preserve the contract.

Select tests by the changed behavior. Narrow MC or parser changes need focused
tests; changes spanning code generation and layout also need full-pipeline and
runtime coverage. Avoid imposing every test suite on unrelated edits.

## Select references

| Task | Read |
|---|---|
| Build identity, lit discovery, runtime probes, simulator limits, bisection | [testing.md](references/testing.md) |
| Encoding, relocation, architecture flags, TableGen operands | [mc-and-relocations.md](references/mc-and-relocations.md) |
| Composite registers, layout contracts, pass placement | [registers-and-layout.md](references/registers-and-layout.md) |

For application ABI or inline-assembly usage, use the separate llvm-mos skill
when available; do not load it merely because both skills share a compiler.

## Verify the result

Confirm that the intended tests were discovered and that changed tools produced
fresh artifacts. Use a bounded timeout for runtime tests. A simulator result is
evidence only for supported instructions, selected CPU semantics, and tested
inputs; confirm hardware-dependent behavior on the relevant machine or emulator.

For ISA claims, consult documentation for the exact CPU variant and, where
available, an independent implementation or hardware test. MEGA65 core behavior
is not authority for unrelated 6502 derivatives. Record disagreements rather
than treating matching toolchain outputs as proof.

Keep tests with the tool whose dependencies they require: linking tests generally
belong under lld rather than LLVM-only CodeGen suites. Follow repository formatting
and contribution instructions. Reviewing or diagnosing does not authorize
installation changes, commits, pushes, or upstream messages.

When maintaining this skill, retain actionable invariants and source/test pointers.
Scope observations to the relevant revision or configuration; replace stale rules
instead of accumulating anecdotes.
