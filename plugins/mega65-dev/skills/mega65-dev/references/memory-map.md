# MEGA65 memory map

What lives where in the 28-bit address space. For *how* a 16-bit address reaches
these locations, see `map-banking.md`.

Notation: `B.NNNN` means bank `B`, offset `NNNN` — e.g. `3.E000` = `$3E000`.
Addresses above 1 MB are written in full (`$FF80000`).

Sources: MEGA65 Book `memory.tex` and `appendix-memorymap.tex`; `mega65-core/iomap.txt`.

---

## 1. The 28-bit space at a glance

| Range | Size | Contents |
|---|---|---|
| `$0000000` | 1 | CPU I/O port data direction register |
| `$0000001` | 1 | CPU I/O port data |
| `$0000002`–`$005FFFF` | 384 KB | **Chip RAM** (full CPU speed, VIC-visible) |
| `$0060000`–`$0FFFFFF` | 15.6 MB | Reserved for Chip RAM expansion |
| `$1000000`–`$3FFFFFF` | 48 MB | Reserved |
| `$4000000`–`$7FFFFFF` | 64 MB | Cartridge port / slow bus (1–10 MHz). C64 cartridge appears at `$4000000`–`$400FFFF` |
| `$8000000`–`$87FFFFF` | 8 MB | **Attic RAM** (not on Nexys boards) |
| `$8800000`–`$8FFFFFF` | 8 MB | Cellar RAM (planned trapdoor PMOD) |
| `$9000000`–`$EFFFFFF` | 96 MB | Reserved |
| `$FF7E000`–`$FF7EFFF` | 4 KB | VIC-IV character ROM (**write only**) |
| `$FF80000`–`$FF87FFF` | 32 KB | **VIC-IV colour RAM** (full 32 KB) |
| `$FFCB000`–`$FFCBFFF` | 4 KB | Emulated C1541 RAM |
| `$FFCC000`–`$FFCFFFF` | 16 KB | Emulated C1541 ROM |
| `$FFD0000`–`$FFD3FFF` | 4×4 KB | **I/O personalities** (§4) |
| `$FFD6000`–`$FFD6BFF` | 3 KB | Hypervisor scratch space |
| `$FFD6C00`–`$FFD6DFF` | 512 | F011 floppy controller sector buffer |
| `$FFD6E00`–`$FFD6FFF` | 512 | SD card controller sector buffer |
| `$FFD7000`–`$FFD72FF` | 3×256 | I2C peripherals (MEGAphone r1, MEGA65 r2, HDMI) |
| `$FFD8000`–`$FFDBFFF` | 16 KB | **Hyppo ROM** — only visible in hypervisor mode |
| `$FFDE800`–`$FFDEFFF` | 2 KB | Ethernet frame read buffer (r) / write buffer (w) |
| `$FFDF000`–`$FFDFFFF` | 4 KB | Virtual FPGA registers (selected models) |

Attic RAM caveats: invisible to VIC and to audio DMA; code runs from it but roughly
**10× slower** than Chip RAM; the freezer does **not** save or restore it.

---

## 2. Chip RAM allocation

How the shipped ROM uses the 384 KB. A machine-code program that never returns to
BASIC may reuse everything except what the KERNAL needs.

| Range | Contents | Free for an ML program? |
|---|---|---|
| `0.0000`–`0.0001` | CPU I/O port | no |
| `0.0002`–`0.15FF` | KERNAL variables and data | only if the KERNAL is not used |
| `0.1600`–`0.1EFF` | **Guaranteed unused by KERNAL and BASIC** | yes, always |
| `0.1F00`–`0.1FFF` | BASIC bitmap-graphics base page | yes, if BASIC graphics unused |
| `0.2000`–`0.F6FF` | BASIC program text | yes |
| `0.F700`–`0.FEFF` | BASIC scalar variables | yes |
| `0.FF00`–`0.FFFF` | Reserved | avoid |
| `1.0000`–`1.1FFF` | DOS buffers and variables | only if CBDOS is not used |
| `1.2000`–`1.F6FF` | BASIC arrays and strings | yes |
| `1.F700`–`1.F7FF` | Reserved | avoid |
| `1.F800`–`1.FFFF` | Colour RAM window (first 2 KB of colour RAM) | see §3 |
| `2.0000`–`3.FFFF` | ROM (write-protected at boot) | after unlocking — §5 |
| `4.0000`–`5.FFFF` | BASIC bitmap graphics, utilities | yes |

`0.1600`–`0.1EFF` is the one region the project *guarantees* stays free across ROM
versions. It is visible as RAM in the default configuration, which makes it the
natural home for a small machine-code payload launched from BASIC.

**Memory-map contract.** The MEGA65 ROM is under active development, unlike the C64's.
Only the table above and the KERNAL jump table are guaranteed stable across ROM
releases. Do not read or write KERNAL variables directly, and do not treat
"reserved" regions as free.

### ROM bank contents

| Range | Contents |
|---|---|
| `2.0000`–`2.3FFF` | DOS (mapped at `$8000`–`$BFFF` by the ROM) |
| `2.4000`–`2.8FFF` | Reserved |
| `2.9000`–`2.9FFF` | Character set A |
| `2.A000`–`2.BFFF` | C64 BASIC |
| `2.C000`–`2.C7FF` | Reserved |
| `2.C800`–`2.CFFF` | Interface routines (mode switching) |
| `2.D000`–`2.DFFF` | C64 character set (charset C) |
| `2.E000`–`2.FFFF` | C64 KERNAL |
| `3.0000`–`3.1FFF` | Monitor (mapped at `$6000`–`$7FFF`) |
| `3.2000`–`3.7FFF` | C65 BASIC |
| `3.8000`–`3.BFFF` | C65 BASIC graphics routines |
| `3.C000`–`3.CFFF` | Reserved |
| `3.D000`–`3.DFFF` | Character set B |
| `3.E000`–`3.FFFF` | **C65/MEGA65 KERNAL** — must stay at `$E000`–`$FFFF` while KERNAL interrupts are live |

Portability note: only banks 0 and 1 (128 KB) exist on a real C65. Banks 4 and 5
require a 384 KB machine.

---

## 3. Colour RAM

The VIC-IV has 32 KB of separate colour RAM at `$FF80000`–`$FF87FFF`. For C65
compatibility, the **first 2 KB** is also visible at `1.F800`–`1.FFFF` — the
"colour RAM window".

- Reaching the full 32 KB needs 28-bit addressing or DMA; it is outside the first
  megabyte, so `BANK`-style access and 1 MB DMA jobs cannot see it.
- A program using ≤ 30 KB of colour data can move the colour-RAM base forward by
  `$0800` and reclaim the 2 KB window at `1.F800` as ordinary Chip RAM.
- Colour RAM base is set by `$D064`/`$D065` (see `registers.md`).

---

## 4. I/O personalities

`$D000`–`$DFFF` is a *window* onto one of four 4 KB register sets. All four are
permanently visible at their own 28-bit addresses, so 28-bit access reaches any
personality regardless of the current setting.

| Personality | 28-bit base | Selected by writing to `$D02F` |
|---|---|---|
| C64 / VIC-II | `$FFD0000` | `$00` then `$00` |
| C65 / VIC-III | `$FFD1000` | `$A5` then `$96` |
| MEGA65 Ethernet | `$FFD2000` | `$45` then `$54` |
| **MEGA65 / VIC-IV (default)** | `$FFD3000` | `$47` then `$53` |

Verified in `mega65-core/src/vhdl/gs4510.vhdl` (~line 9127): the decoder forms
`FFD3xxx` and then overwrites address bits 13–12 with the two-bit I/O mode, giving
`FFD0`/`FFD1`/`FFD2`/`FFD3` for modes 00/01/10/11.

> **Book erratum.** `memory.tex` states that the default MEGA65 personality maps to
> `FFD.2000`. That is wrong: `FFD2000` is the Ethernet personality.
> `appendix-memorymap.tex` and the VHDL agree on `FFD3000`.

Practical consequences:

- `$D030` does **not** exist in the C64 personality. A program that starts in C64
  mode must knock to C65 or MEGA65 before touching it.
- `$D640` (hypervisor traps) exists only in the MEGA65 personality.
- The `$D02F` "knock" is two writes of specific values; a single write does nothing.
- Defensive startup: set the personality you need rather than assuming it.

Canonical defensive opening sequence (Book, `appendix-memorymap.tex`):

```asm
        LDA #$00        ; clear the C65 memory map
        TAX
        TAY
        TAZ
        MAP
        LDA #$35        ; bank I/O in via the C64 mechanism
        STA $01
        LDA #$47        ; MEGA65 / VIC-IV I/O knock
        STA $D02F
        LDA #$53
        STA $D02F
        EOM             ; end MAP sequence, interrupts allowed again
```

---

## 5. ROM as RAM

Banks 2 and 3 are write-protected at boot. The protection is enforced by the
hypervisor, not by a banking mechanism — unlocking makes the bytes writable in place;
it does not swap anything out.

```asm
        LDA #$70        ; hyppo_toggle_rom_writeprotect
        STA $D640
        CLV
```

There are also explicit traps: `$D641` with `A=$02` enables writing, `A=$00`
restores protection (`hypervisor.md`).

Notes:

- The protection state is **not readable**. Test by writing and reading back.
- Writes must go through MAP, 28-bit addressing, or DMA. With `$0001`/`$D030`
  banking active on an unmapped block, **reads** hit bank 2 ROM but **writes** fall
  through to bank 0 RAM — the same shadowing behaviour as a C64.
- A program that starts in C64 mode can safely reclaim all of bank 3, giving 192 KB
  on every model.
- ROM is loaded from disk by the hypervisor at boot. To restore it after overwriting,
  DMA a copy to Attic RAM first.

---

## 6. Reclaiming the whole machine

To make all Chip RAM reachable at `0.0000`–`5.FFFF`:

1. Disable interrupts.
2. Clear all bits of `$D030`.
3. Set the MAP register to all zeroes (both offsets *and* both megabyte bytes —
   see `map-banking.md`).
4. Clear bits 0–2 of `$0001` to remove I/O from `$D000`–`$DFFF`.
5. Move colour RAM base forward by ≥ `$0800` if the `1.F800` window is wanted as RAM.
6. Disable ROM write-protect on banks 2 and 3.
7. Install your own interrupt handlers and vectors, then re-enable interrupts.

After step 4, `$D000`–`$DFFF` is RAM; reach I/O registers via their 28-bit addresses
(`$FFD3xxx`) instead. After step 3, `$0000`/`$0001` are RAM too — the banking
registers are only reachable while block 0 is *unmapped*.
