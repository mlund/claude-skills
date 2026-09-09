---
name: mega65-dev
description: "Develop and debug MEGA65 machine-level code: memory mapping, banking, DMAgic, hardware registers, KERNAL, Hyppo, VIC-IV graphics, and xemu testing. Use for hardware access and emulator workflows, not BASIC programming, end-user operation, or compiler-backend development."
---

# MEGA65 systems development

Use this skill for machine behaviour and hardware access. Keep assembly examples toolchain-neutral. For compiler ABI, constraints, or instruction support, consult the available llvm-mos skill only when needed.

## Workflow

1. Establish the relevant board, core/ROM or xemu revision, and current memory map when the answer depends on them. Use paths already supplied or established by project configuration; ask only for a missing checkout needed for this task.
2. Select the reference below that addresses the question. Read only relevant references; do not load the collection by default. Follow cross-references only when the current task needs them.
3. Check the relevant implementation before asserting disputed behaviour. Cite the source symbol and revision when available; line numbers are navigation aids, not version identifiers.
4. Distinguish implementation evidence, hardware measurements, emulator observations, and unverified reports. Do not convert a benchmark from one configuration into a universal timing rule.

## Sources

Choose authority by subject, rather than applying one ranking to every question:

| Subject | Source |
|---|---|
| Hardware behaviour | [mega65-core](https://github.com/MEGA65/mega65-core): relevant VHDL decode/state machine |
| Register lookup | Core's iomap.txt; generated annotations can be incomplete or disagree with logic |
| Explanations and formats | [mega65-user-guide](https://github.com/MEGA65/mega65-user-guide); resolve hardware discrepancies against the relevant core revision |
| KERNAL/BASIC behaviour | [mega65-rom](https://github.com/MEGA65/mega65-rom) |
| Hyppo services | Core's src/hyppo/ |
| Emulator behaviour/options | [xemu](https://github.com/lgblgblgb/xemu), targets/mega65/ |

Community examples can suggest mechanisms to investigate; verify hardware claims against the implementation. Read the complete relevant branch before declaring documentation wrong.

## Essential constraints

- Establish the I/O personality and MAP state before using 16-bit hardware addresses. Mapping over I/O can turn a register access into a RAM access.
- MAP changes must leave executing code, required data, and interrupt paths reachable. Read the banking reference before changing a map.
- Before changing VIC-IV geometry or pointers, check HOTREG handling in the register reference.
- Emulator success does not establish hardware correctness or timing. Similar symptoms on both platforms do not prove a shared cause.
- For performance claims, identify the workload, board/core, CPU mode, transfer endpoints, and timing method. Check correctness and measure without serial polling inside the timed interval.

## References

| Read | When needed |
|---|---|
| [memory-map.md](references/memory-map.md) | Physical regions, Chip/Attic RAM, colour RAM, I/O personalities, ROM protection |
| [map-banking.md](references/map-banking.md) | MAP/EOM encoding, precedence, interrupts, mapping readback, banked layouts |
| [registers.md](references/registers.md) | Register lookup, HOTREG, CPU speed, VIC-IV, MATH, storage and keyboard registers |
| [dma.md](references/dma.md) | DMA triggers, job formats, options, chaining, strides and transfer measurements |
| [kernal.md](references/kernal.md) | KERNAL call preconditions, base page, Z handling and zero-page usage |
| [hypervisor.md](references/hypervisor.md) | Hyppo traps, file loading, freezing and ROM write protection |
| [floppy.md](references/floppy.md) | Direct F011 D81 sector access without KERNAL/DOS |
| [character-modes.md](references/character-modes.md) | FCM/NCM cells, glyph addressing and palettes |
| [rrb.md](references/rrb.md) | GOTOX, compositing, row termination, ROWMASK and fetch budgets |
| [xemu-testing.md](references/xemu-testing.md) | Launching, driving and observing tests; emulator limitations and hardware transfer |
