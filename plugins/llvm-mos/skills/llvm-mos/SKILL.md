---
name: llvm-mos
description: Build, debug, and optimize 6502-family C, C++, and assembly with llvm-mos and llvm-mos-sdk. Use for application code, inline assembly, linker layouts, and migration to llvm-mos; not for unrelated retro-computing work or compiler-backend development.
---

# llvm-mos

Use this skill for programs built with llvm-mos. Load only the references needed
for the task; do not read the entire reference directory.

## Establish the build

Find the target driver, CPU, SDK/compiler revisions, linker script, and actual
build command in project instructions and configuration. Ask only for missing
information needed for the current task. Preserve the project's language standard,
optimization policy, and toolchain choice.

Complete SDK targets supply platform configuration and image layout; parent
targets may require a custom linker script. Inspect the installed driver with
`-###` rather than assuming inherited flags or tool paths. LTO commonly supplies
whole-program zero-page and static-stack allocation; disabling it changes the
pipeline and is not equivalent evidence for an LTO bug.

## Correctness constraints

- Imaginary registers live in linker-assigned zero page. Reference their symbols,
  not copied addresses. Assembly must preserve the ABI and declare its effects,
  including calls made by the routine, flags, and memory.
- Static-stack allocation depends on which invocations may overlap. Function
  pointers alone do not justify `nonreentrant`. Verify recursion, callbacks, and
  interrupt re-entry before promising non-reentrancy.
- Use `leaf` only after verifying its no-callback promise for the called code.
  Assembly implementation alone does not establish that promise.
- Interrupt entry needs the toolchain's interrupt annotations even when assembly
  supplies the prologue. Use `interrupt_norecurse` only when overlapping
  invocations are impossible; preserve all state the interrupted code may need.
- For the MEGA65 ABI, keep Z=0 and B=0 whenever compiled code executes, including
  calls into C from the middle of assembly routines. Read the 45GS02 reference
  before using Z, Q, MAP, or extended addressing.
- Host tests do not reproduce the target's integer widths or hardware. Check
  width-sensitive arithmetic under the target model and hardware interactions
  on an appropriate emulator or machine.

## Inspect and measure

Establish a baseline before optimizing. Compare the same inputs, target, flags,
and build pipeline; measure the user's relevant code/data region rather than
assuming image-file length measures occupied memory.

Inspect a retained post-LTO ELF when available. LTO assembly emission is a
separate diagnostic build, not a runnable artifact. Verify tool exit status and
output format before interpreting an empty search or zero count. Read the tooling
reference for the commands and artifact checks.

Treat narrower integers, indexing, table lookup, layout changes, and inlining as
experiments. Inspect the changed loop and its callers: register pressure and LTO
can move costs away from the edited source. Do not transfer byte or cycle figures
between programs without measuring.

## Select references

| Task | Read |
|---|---|
| LTO output, disassembly, maps, driver configuration | [tooling.md](references/tooling.md) |
| Code size or measured CPU hot path | [optimization.md](references/optimization.md) |
| C/assembly calls, argument layout, interrupt prologue | [abi.md](references/abi.md) |
| Nontrivial inline assembly or constraint failures | [inline-asm.md](references/inline-asm.md) |
| Memory layout, zero page, banking, keeping sections | [linker-scripts.md](references/linker-scripts.md) |
| SDK platform creation or inheritance | [sdk-platforms.md](references/sdk-platforms.md) |
| Commodore platform libraries and ROM wrappers | [commodore.md](references/commodore.md) |
| MEGA65 compiler/assembly boundary | [45gs02.md](references/45gs02.md) |
| Porting cc65/ca65 code | [cc65-migration.md](references/cc65-migration.md) |
| Native tests for portable logic | [host-testing.md](references/host-testing.md) |
| Target-model computation or simulated cycle measurements | [simulator-testing.md](references/simulator-testing.md) |

## Verify version-sensitive claims

Prefer the checked-out implementation and tests: `MOSCallingConv.td` for ABI,
`MOSInlineAsmLowering.cpp` for constraints, `llvm/test/MC/MOS/` for assembler
encodings, and SDK `mos-platform/` for libraries and layouts. Encoding tests
describe tool behavior, not independent proof of silicon behavior.

When updating this skill, keep each rule in one reference, cite its implementation
or reproducible test, and distinguish requirements from measured examples.
Keep compiler changes in the separate llvm-mos-dev skill.
