---
name: mega65-dev
description: Systems-level MEGA65 development — the machine, not the toolchain. Use this skill when work involves the 45GS02 memory model, the MAP register, banking, 28-bit addressing, or DMAgic; MEGA65/C65 hardware registers (VIC-II/III/IV, $D030, $D02F I/O personalities, SD/floppy, MATH unit, CIA); the MEGA65 KERNAL (jump table, zero-page usage, Z-register clobbering, MAP preconditions); the Hyppo hypervisor ($D640–$D67F traps, ROM write-protect, freeze, boot); or running and testing MEGA65 code under the xemu emulator. Trigger it for questions like "how do I map Attic RAM into $A000", "what does $D640 trap $70 do", "which KERNAL calls clobber Z", "why did my write to $D031 reset the border", "how do I script a MEGA65 test under xemu", or any MEGA65 bank-switching, memory-layout, or register-poking task. Not for BASIC 65 programming or end-user operation.
---

# MEGA65 systems development

This skill is about the **machine**: how addresses are translated, where memory
and registers live, and what the ROM and hypervisor expect of you. It is
toolchain-neutral — examples are plain 45GS02 assembly.

## Authoritative sources

Upstream repositories, in precedence order. **Ask the user for local paths if they are
not already known**; do not guess, and do not record paths anywhere. If a repository
is not checked out, offer the URL.

| Repo | URL | Authority |
|---|---|---|
| `mega65-core` | <https://github.com/MEGA65/mega65-core> | **Ground truth.** `src/vhdl/*.vhdl` is the hardware; `iomap.txt` is the register master list |
| `mega65-user-guide` | <https://github.com/MEGA65/mega65-user-guide> | The MEGA65 Book. Best prose; occasionally stale |
| `mega65-rom` | <https://github.com/MEGA65/mega65-rom> | KERNAL/BASIC source. Needed for ROM-behaviour claims |
| `xemu` (optional) | <https://github.com/lgblgblgb/xemu> | The emulator, and the authority on what an emulator option really does |

Which file answers which question:

| Question | Source |
|---|---|
| CPU, memory map, MAP, DMA | `mega65-core/src/vhdl/gs4510.vhdl` |
| VIC-IV register behaviour | `mega65-core/src/vhdl/viciv.vhdl` |
| Which device answers at an address | `mega65-core/src/vhdl/iomapper.vhdl` |
| SD controller and sector buffers | `mega65-core/src/vhdl/sdcardio.vhdl` |
| Keyboard matrix positions | `mega65-core/src/vhdl/matrix_to_ascii.vhdl` |
| What freezing saves and restores | `mega65-core/src/hyppo/freeze.asm` |
| Register *names* and prose | the Book's LaTeX register appendices |
| KERNAL and BASIC behaviour | `mega65-rom` sources |
| What an emulator option really does | `xemu/targets/mega65/` |

Rules:

- **VHDL wins.** Where the Book and the core disagree, the core is right and the
  discrepancy is worth flagging. Two are recorded as errata: the default I/O
  personality's 28-bit base (`references/memory-map.md` §4) and what `EOM` does to
  interrupts (`references/map-banking.md` §4).
- **`iomap.txt` is the fast path for registers** — roughly 1750 entries generated from
  `@IO:` annotations in the VHDL, so it never drifts from the hardware. Format and
  grep recipe in `references/registers.md`.
- Never cite the MEGA65 wiki for a hardware fact you can check in the core.
- **`xemu` is optional but valuable.** If a task involves running, testing or debugging
  code, ask whether `xemu` (binary `xmega65`) is available and, optionally, where its
  source is checked out. Emulator agreement is not hardware agreement —
  `references/xemu-testing.md` §6 lists known divergences.

## The one thing to understand first

A 16-bit address goes through **four** translation mechanisms before it reaches the
28-bit address space, in this priority order:

```
MAP register          highest — per-8KB-block offset, set by the MAP instruction
  ↓ (unmapped blocks only)
cartridge ROM         C64 expansion-port EXROM/GAME configurations
  ↓
$D030                 VIC-III ROM banking: ROM8/ROMA/ROMC/ROME → bank 2
  ↓
$0001                 C64-style banking: I/O and C64 ROM at $A000/$D000/$E000
```

Two consequences that explain most confusion:

- **`$0001` and `$D030` only act on blocks the MAP register did not select.** Map
  `$C000–$DFFF` with offset 0 and you get RAM, not I/O, whatever `$0001` says.
- **28-bit addressing modes (`LDA [$nn],Z`) and DMA bypass all four.** They see the
  raw 28-bit space. This is why they are usually the right tool, and why a routine
  that uses them keeps working regardless of the caller's map.

Reach for MAP only when code must **execute** from the region, or when a large
run of 16-bit accesses justifies the setup cost.

## Working rules

- **Cite evidence.** Every hardware claim should carry a register address, a
  `file:line`, or a Book section. Unsourced recollection about MEGA65 hardware is
  frequently wrong.
- **Check `iomap.txt` before asserting a register exists.** Register names and bit
  assignments change between core releases.
- **State the I/O personality.** `$D640`, `$D030`, and most `$D0xx`–`$D7xx` registers
  are only visible in the right personality (`references/registers.md`).
- **Say when something is unverified.** "Reported but not confirmed against the core"
  is a useful thing to write down; a confident guess is not.

## Reference files

| File | Open it when |
|---|---|
| `references/memory-map.md` | You need to know what lives at an address — Chip/Attic RAM, ROM banks, colour RAM, upper I/O, personalities |
| `references/map-banking.md` | Anything involving `MAP`/`EOM`, bank switching, or designing a banked memory layout |
| `references/registers.md` | Looking up or poking a hardware register; hot-register surprises |
| `references/kernal.md` | Calling the KERNAL, zero-page budgeting, or the Z-register hazard |
| `references/hypervisor.md` | `$D640`–`$D67F` traps, ROM write-enable, SD-card file access, freeze |
| `references/xemu-testing.md` | Running, driving or regression-testing code under the emulator; getting builds onto hardware |

## Scope, and sibling skills

In scope: memory model, MAP and banking, hardware registers, KERNAL, hypervisor, and
emulator-based testing.

Out of scope: BASIC 65 programming, end-user operation, core building and flashing.

The 45GS02 **instruction set** — Q pseudo-register, `[$nn],Z`, the Z=0 invariant that
compiled code depends on, per-mnemonic assembler support — is covered by the
`llvm-mos` skill in `references/45gs02.md`. Use that for CPU and compiler questions;
use this skill for the machine around the CPU. `llvm-mos-dev` covers the compiler
backend itself.

## Maintaining this skill

When adding to or correcting these files:

- **Evidence or nothing.** A new claim needs a citation: `iomap.txt` line, a
  `src/vhdl/<file>.vhdl:<line>`, a Book chapter, or a `mega65-rom` source file.
  If you verified it on hardware or in an emulator, say which and what you observed.
- **Prefer the core.** If the only source is the Book and the core is checkable,
  check it. Record contradictions rather than silently picking a side.
- **Generic, not autobiographical.** No dates, no project names, no local paths, no
  "we discovered". Write facts and patterns a stranger can reuse.
- **Brief.** Tables over prose. One idea per row. Delete anything the reader can get
  from `iomap.txt` in one grep, unless it is a gotcha.
- **Assembly stays toolchain-neutral.** No compiler-specific syntax or constraints;
  those belong in `llvm-mos`.
- **Prune.** When the core changes a register or a claim turns out wrong, fix or
  remove it. A stale table is worse than no table.
