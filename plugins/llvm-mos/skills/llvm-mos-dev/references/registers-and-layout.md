# Register and layout contracts

Use this reference for register classes, linker assumptions, and pass placement.
Verify implementation details against the checked-out revision.

## Check layout requirements at link time

Register allocation and addressing modes can depend on relationships between
linker-defined symbols that ELF does not describe. Audit every definition of
those symbols, not only linker scripts: platforms may define them in assembly,
generated files, archives, or independently discardable sections.

When code generation relies on such a relationship, emit an undefined marker
reference only when the feature is used and let compatible linker scripts
provide it lazily:

```ld
PROVIDE(__contract_marker = ASSERT(layout_condition,
  "layout does not satisfy the compiler contract"));
```

This keeps programs that do not use the feature compatible while making old,
custom, and incompatible layouts fail at link time. A separate
`ASSERT(!DEFINED(marker) || condition, ...)` is not an equivalent reference
test for a lazy `PROVIDE`.

Under `--gc-sections`, keep the marker relocation in an allocatable, retained
section. Do not rely on `SHF_GNU_RETAIN` alone for non-allocatable metadata;
test that the undefined relocation survives collection. Check where sections not
named in the linker script are placed and how much image space they occupy.

## Adding a composite register class

A nonallocatable super-register class still changes alias and super-register
topology, so it can affect reservation logic, pressure heuristics, and code
that assumes the first super-register has a particular class. Match by class
and subregister index rather than relying on iterator order.

Check hard-coded register uses as well as the `Reserved` bitvector:
`MOSRegisterInfo`'s constructor reserves one pointer as the scavenger temporary,
and `MOSCallLowering` then synthesizes an absolute `JMP` by writing its opcode
into that pointer's high byte, relying on adjacency to the next pointer register;
`MOSFrameLowering` names the same two bytes when saving an interrupt handler.
Search for a register's name before assuming it is relocatable or that its aliases are
free for a wider class.

Before exposing a wider class, check register banks, inline-asm register counts
and constraints, reserved aliases, copy costs, spills and reloads, post-RA
expansion, CSR/zero-page allocation, asm lowering, and debug/DWARF numbering.
Propagate child reservations to super-registers with LLVM's register-info
helpers, then assert in debug builds that no allocatable member aliases a
reserved register.

Test the capacity boundary, one value beyond it, values live across a call, and
the resulting spill path. Checks that pin a preferred allocation order do not
prove that the class is safe under pressure.

## Record assignments before expansion

Post-RA pseudo expansion can dissolve a composite physical register into byte
operations. If module output or diagnostics depend on the composite assignment,
record it after register allocation but before the first expansion that erases
it. Use a dedicated pass at that boundary instead of attaching a whole-function
scan to a nearby pass that may intentionally run more than once.

Inspect the real pipeline with `-debug-pass=Arguments`. A test using
`-start-before` skips every earlier pass, so it cannot prove that an earlier
marker or analysis pass ran. Add a full-pipeline MIR case whose composite
operation is gone by assembly emission but whose recorded side effect remains.
