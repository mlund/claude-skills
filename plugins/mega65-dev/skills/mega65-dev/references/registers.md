# MEGA65 hardware registers

This file curates the registers that come up constantly. **Anything not here is one
grep away** — start with §1 rather than guessing.

---

## 1. Looking a register up

`mega65-core/iomap.txt` is the master list: ~1750 entries generated from `@IO:`
annotations in the VHDL, so it tracks the hardware rather than the documentation.

Line format:

```
<mode> <address> <BLOCK:FIELD> <description>
```

| Field | Values / meaning |
|---|---|
| `<mode>` | `C64` (VIC-II personality), `C65` (VIC-III), `GS` (MEGA65/45GS02) |
| `<address>` | `$D020`, a bit slice `$D030.3`, a range `$D770-3`, or a 28-bit address |
| `<BLOCK:FIELD>` | e.g. `VIC-IV:CHRCOUNT`, `DMA:ADDRMB`, `SD:SECTOR0`. `-` where unnamed |
| `@NAME` | alias marker: `S0X@SNX` defines the pattern, later `@SNX` lines repeat it |

Useful queries:

```sh
grep -E '^\S+ \$D054' iomap.txt          # one register, all its bits
grep -E '^\S+ \$D054\.'  iomap.txt       # only the bit definitions
grep 'VIC-IV:' iomap.txt                 # everything in one block
grep -iE 'sprite.*16.?colour' iomap.txt  # search by description
```

Per-subsystem prose lives in the MEGA65 Book appendices:
`appendix-viciv-registers.tex`, `appendix-45gs02-registers.tex`,
`appendix-dmagic.tex`, `appendix-cia6526-registers.tex`,
`appendix-sid-registers.tex`, `appendix-45io27-registers.tex`,
`appendix-45e100-registers.tex`, `appendix-rtc-registers.tex`.

---

## 2. Before poking anything: personality and hot registers

**I/O personality.** `$D000`–`$DFFF` shows one of four register sets. Most MEGA65
registers, including `$D640`, exist only in the MEGA65 personality; `$D030` does not
exist in the C64 personality at all. Switch with the `$D02F` knock — see
`memory-map.md` §4. All four are always reachable at their 28-bit addresses
(`$FFD0000`/`$FFD1000`/`$FFD2000`/`$FFD3000`).

`$D0xx` is therefore **not a fixed address**: every access is decoded as `$FFD3xxx`
with bits 13–12 replaced by the current I/O mode. A typed register overlay at `$D0xx`
is only correct while the personality is what you assume. Code that must work in a
machine state it did not establish should use the **flat 28-bit form** — writing
`$FFD3021` reaches the VIC-IV screen colour whatever the knock state, where writing
`$D021` may not.

> **`$D02F` is dangerous to write at all.** In `viciv.vhdl` (`register_number=47`)
> *every* write first sets the I/O mode back to `00`; only a matching **second** byte
> of a knock raises it again. Writing `$47` on its own therefore drops you into the
> C64 personality while arming the second half. A bulk restore of a saved VIC register
> block must skip offset `$2F`.

**Which device answers can also change with personality.** `iomapper.vhdl` selects
CIA1 on address prefixes `$D0C`, `$D1C` and `$D3C` — but **not** `$D2C` — and only
while `colourram_at_dc00 = '0'`. So "the CIAs are at `$DC00`" is nearly always true,
with the ethernet personality and the 2 KB colour-RAM mapping as the exceptions.

**Hot registers.** Writing certain VIC-II/VIC-III registers makes the VIC-IV
recompute a whole cluster of its own registers from the legacy values — even if you
write back the value that was already there. This is how unmodified C64 software gets
a sane VIC-IV configuration, and it is why a carefully set up VIC-IV mode collapses
the moment something touches `$D011`.

- Controlled by **HOTREG, bit 7 of `$D05D`**. Clear it and you must configure the
  VIC-IV registers yourself.
- Propagation covers border and display geometry, character/screen pointers, and
  scaling. Character-set base propagation sets only `$D068`–`$D069`; `$D06A` (bits
  23–16) is deliberately left alone so legacy code can use a charset in another bank.
- `$D031` contains the FAST flag, which is unrelated to video but still lives in a hot
  register byte — writing it triggers a full recalculation.
- Re-enabling HOTREG applies any update that became pending while it was off. To
  suppress that, write 0 to HOTREG again immediately before re-enabling.

**Symptom to remember:** "my VIC-IV setup reverted for no reason" is almost always a
hot register write.

---

## 3. CPU speed

| Where | Effect |
|---|---|
| `$0000` ← `$41` (65) | Force 40 MHz; `$40` (64) restores normal speed control |
| `$D054` bit 6 (`VFAST`) | MEGA65 fast mode (~40.5 MHz) |
| `$D031` bit 6 (`FAST`) | C65 fast mode (~3.5 MHz) |
| `$D030` bit 0 (C64 personality) | C128-style 2 MHz |

Slow-bus regions (the cartridge range at `$4000000`) run at 1–10 MHz regardless.
Attic RAM access is roughly 10× slower than Chip RAM.

---

## 4. VIC-IV essentials

Legacy VIC-II registers (`$D000`–`$D02E`) behave as on a C64. The additions below are
the ones that matter for laying out a display.

### Mode control

| Addr | Name | Notes |
|---|---|---|
| `$D02F` | KEY | I/O personality knock (two writes) |
| `$D030` | VIC-III control A | ROM banking + `CRAM2K` (bit 0), `PAL` palette RAM (bit 2) |
| `$D031` | VIC-III control B | `H640` (b7), `FAST` (b6), `ATTR` (b5), `BPM` (b4), `V400` (b3) |
| `$D054` | VIC-IV control C | `CHR16` (b0), `FCLRLO` (b1), `FCLRHI` (b2), `SMTH` (b3), `SPR H640` (b4), `PALEMU` (b5), `VFAST` (b6), `ALPHEN` (b7) |
| `$D05D` bit 7 | HOTREG | Hot-register propagation enable (§2) |
| `$D06F` | — | `RASLINE0` (b0–5), `VGAHDTV` (b6), `PALNTSC` (b7) |

### Memory pointers

| Addr | Name | Width |
|---|---|---|
| `$D060`–`$D062` | `SCRNPTR` | Screen RAM base, 24-bit |
| `$D064`–`$D065` | `COLPTR` | Colour RAM base, 16-bit (offset into the 32 KB colour RAM) |
| `$D068`–`$D06A` | `CHARPTR` | Character set base, 24-bit |
| `$D06C`–`$D06D` | `SPRPTRADR` | Sprite pointer address, 16-bit |

**Reach.** These are flat addresses, not VIC-bank offsets: `SCRNPTR` places screen
memory anywhere in the first 384 KB, `CHARPTR` anywhere in the first 16 MB. Writing
the legacy `$D018` updates only the **low 16 bits** of `CHARPTR`, deliberately leaving
`$D06A` alone, so legacy code can be pointed at a character set in another bank by
presetting `$D06A` once.

**The character-ROM shadow survives.** In VIC bank `$8000` the range `$9000`–`$9FFF`
reads the character ROM, never the RAM beneath it — as does `$1000`–`$1FFF` in bank 0.
Copying a font there accomplishes nothing, and the RAM underneath remains free for
other use.

### Palette

| Addr | Contents |
|---|---|
| `$D100`–`$D1FF` | Red values, 256 entries |
| `$D200`–`$D2FF` | Green values |
| `$D300`–`$D3FF` | Blue values |
| `$D070` bits 6–7 | `MAPEDPAL` — which palette bank is mapped at `$D100`–`$D3FF` |

**Palette bytes are nybble-reversed** (`iomap.txt`: "reversed nybl order"). The bytes
`$BA $13 $62` give the colour `AB3126`. In Super-Extended Attribute Mode a colour-RAM
byte is four attribute bits plus a four-bit index into this 256-entry palette, so
recolouring a display is a palette rewrite, not a mode change. In 16-bit character
mode a cell is two bytes and the colour lives in the **high** byte of the colour cell.

### Geometry

| Addr | Name | Meaning |
|---|---|---|
| `$D058`–`$D059` | `LINESTEP` | Bytes to advance between text rows |
| `$D05A` | `CHRXSCL` | Horizontal scale, 120ths of a pixel per pixel |
| `$D05B` | `CHRYSCL` | Physical rasters per character row |
| `$D05C` + `$D05D` b0–5 | `SDBDRWD` | Single side-border width (LSB + MSB) |
| `$D05E` | `CHRCOUNT` | Characters displayed per row |
| `$D07B` | `DISPROWS` | Text rows to display |
| `$D04C` / `$D04E` | `TEXTXPOS` / `TEXTYPOS` | Character generator origin |

### Sprites (MEGA65 extensions)

| Addr | Name |
|---|---|
| `$D055` / `$D056` | Extended height enable / height in pixels |
| `$D057` | Extended width enable (64 px wide) |
| `$D05F` | H640 X super-MSBs |
| `$D06B` | 16-colour sprite mode enables |
| `$D076`–`$D078` | V400 enables and Y MSBs |

### Raster

| Addr | Name |
|---|---|
| `$D050` + `$D051` b0–5 | Horizontal raster position (read) |
| `$D052` + `$D053` b0–2 | Physical raster position (read) |
| `$D079` + `$D07A` b0–2 | Raster compare value |
| `$D07A` b7 | `FNRSTCMP` — compare in VIC-II rasters if set, physical if clear |
| `$D07A` b6 | `EXTIRQS` — enable extra IRQ sources such as raster X |
| `$D05D` b6 | `RSTDELEN` — delay raster counter and IRQs by one line to match pipeline latency |

The upper bits of `$D051`, `$D053`, and `$D07A` are unrelated control flags, not
address bits — read the bit slices in `iomap.txt` before doing a whole-byte write.

Colour RAM is 32 KB at `$FF80000`; only the first 2 KB is visible at `1.F800`
(`memory-map.md` §3).

---

## 5. DMAgic

The fastest way to move bytes. Reaches the whole 28-bit space, including Attic RAM
and the full colour RAM.

| Addr | Name | Effect |
|---|---|---|
| `$D700` | `ADDRLSBTRIG` | List address bits 0–7 — **writing triggers the job** |
| `$D701` | `ADDRMSB` | List address bits 8–15 |
| `$D702` | `ADDRBANK` | List address bits 16–22 (bit 7 = `WITHIO`, unused). Writing clears `$D704` |
| `$D703` | — | bit 0 `EN018B` (F018B list format), bit 1 `NOMBWRAP` (no wrap at MB boundaries) |
| `$D704` | `ADDRMB` | List address bits 20–27 (overlaps `ADDRBANK`) |
| `$D705` | `ETRIG` | Trigger *enhanced* job, list at a 28-bit flat address |
| `$D706` | `ETRIGMAPD` | Trigger enhanced job, list read through the current CPU map |
| `$D707` | `ETRIGINLINE` | Trigger enhanced job whose list starts at the PC; PC resumes after it |
| `$D70E` | `ADDRLSB` | Set list address LSB **without** triggering |

Enhanced job-list option bytes (a `$00`-terminated prefix before the job):

| Option | Meaning |
|---|---|
| `$00` | End of options |
| `$06` | Enable transparency using the `$86` value |
| `$0A` / `$0B` | Use F018A / F018B list format |
| `$80 $xx` / `$81 $xx` | Megabyte of source / destination address |
| `$82 $xx` / `$83 $xx` | Source skip rate: 256ths of a byte / whole bytes |
| `$84 $xx` / `$85 $xx` | Destination skip rate: 256ths / whole bytes |
| `$86 $xx` | Skip writing bytes equal to `$xx` (with option `$06`) |
| `$0D` / `$0E` / `$0F` | Floppy raw flux write / read ignoring long gaps / read |

**Strides are independent and fractional.** Source and destination each have their own
16-bit 8.8 fixed-point skip rate, defaulting to `$0100` (exactly 1.0) — `$82`/`$83` set
the source fraction and whole part, `$84`/`$85` the destination. `gs4510.vhdl` keeps two
separate address-update paths that read them independently. A strided fill is how you
recolour every other byte of a 16-bit-mode row in a single job.

**F018A vs F018B.** The two list formats differ by a sub-command byte, and which one
the hardware expects depends on the core/ROM combination. `$D703` bit 0 selects it;
the hypervisor trap `dmagic_autoset` (`$D642`, `A=$06`) sets it from the loaded ROM.
Enhanced jobs can pin the format per job with option `$0A`/`$0B`, which is the robust
choice. Getting this wrong produces jobs that transfer the wrong length or nothing.

`$D710`–`$D71F` are **audio** DMA channels, unrelated to block copies.

Full job-list layout: `appendix-dmagic.tex`.

---

## 6. MATH unit

A 32-bit hardware multiplier and divider — far faster than software arithmetic.

| Addr | Name |
|---|---|
| `$D770`–`$D773` | `MULTINA` — multiplier input A / divider numerator |
| `$D774`–`$D777` | `MULTINB` — multiplier input B / divider denominator |
| `$D778`–`$D77F` | `MULTOUT` — 64-bit `A × B` |
| `$D768`–`$D76F` | `DIVOUT` — 64-bit `A ÷ B` |

Results appear after a fixed latency; the division result is a fixed-point quotient.
See `mega65-core/docs/math-unit.md` for the timing and the fractional layout.

---

## 7. SD card and floppy (45IO27)

| Addr | Name | Notes |
|---|---|---|
| `$D680` | `CMDANDSTAT` | SD controller command (write) and status (read) |
| `$D680` bit 3 | — | Reads back "sector buffer mapped" |
| `$D681`–`$D684` | `SECTOR0..3` | 32-bit SD sector address |
| `$D686` | `FILLVAL` | Fill byte for fill mode (write only) |
| `$D689` bit 7 | `BUFFSEL` | Which buffer is visible: 1 = SD card, 0 = F011/FDC |
| `$D689` bit 1 | `BUFFFULL` | Sector read but not yet consumed by the CPU |
| `$D68B` | — | Disk image control flags |
| `$D6A1` | `USEREAL0/1` | Use the real floppy drive rather than an image (read-only outside the hypervisor) |

Sector buffers are at fixed 28-bit addresses: F011 floppy at `$FFD6C00`, SD at
`$FFD6E00` (512 bytes each).

**Mapping the buffer into the I/O area.** Writing `$81` to `$D680` maps the sector
buffer at `$DE00`–`$DFFF`; `$82` removes it (`sdcardio.vhdl`). While mapped it hides
whatever else lives there — cartridge I/O, REU emulation. The state reads back in
`$D680` bit 3.

**`BUFFSEL` applies to both views.** `$D689` bit 7 selects FDC or SD buffer at
`$DE00` *and* at `$FFD6xxx`. Getting it wrong reads the wrong buffer with no error.
Outside hypervisor mode `$FFD6000`–`$FFD6FFF` shows the selected 512-byte buffer
repeated eight times; only the hypervisor sees the full 4 KB.

Sector-buffer access is DMA-capable, and a read can proceed in the background.

Only the hypervisor can talk to the SD cards' file systems. For file access, use the
Hyppo traps (`hypervisor.md`) rather than driving `$D680` directly.

---

## 8. Miscellaneous

| Addr | Name | Notes |
|---|---|---|
| `$D610` | `ASCIIKEY` | Top of the typing queue as ASCII; write anything to pop |
| `$D619` | `PETSCIIKEY` | Same queue as PETSCII |
| `$D61E` | `KEYLED` | Keyboard LED value (write only) |
| `$D629` | `M65MODEL` | Model ID — use this to detect hardware variants |
| `$D62A`–`$D62E` | — | Keyboard firmware date and git hash |
| `$D640`–`$D67F` | `HTRAPxx` | Hypervisor traps when written from normal mode |
| `$D67F` | `ENTEREXIT` | Return from hypervisor |

`$D640`–`$D67F` are **dual-purpose**: from normal mode a write triggers trap number
`(addr − $D640)`; from *inside* hypervisor mode the same addresses are the saved
register file (`REGA` at `$D640`, `REGX` at `$D641`, `REGY` at `$D642`, `REGZ` at
`$D643`, and so on).
