# F011 floppy: reading sectors without the ROM

Two ways to get a file off disk without the KERNAL or the C65 DOS ROM:

| Route | Reach | Cost |
|---|---|---|
| Hyppo `loadfile` / `loadfile_attic` traps | Files on the **SD card's** FAT filesystem | One trap; see `hypervisor.md` §2 |
| Drive the **F011** yourself | Sectors of a **D81 image or real disk**, wherever it is mounted | ~40 lines of state machine, this file |

The F011 route needs no zero page, no MAP preconditions and no ROM, and its natural
destination is a DMA job to a 28-bit address — so data lands in any bank without the
loader ever mapping it (§5). That makes it usable from a banked layout where the
KERNAL is not resident.

---

## 1. Registers

From `iomap.txt` (`$D080`–`$D08A`); only the bits a loader needs.

| Addr | Bits | Meaning |
|---|---|---|
| `$D080` | 0–2 `DS` | Drive select. Internal drive is 0 |
| | 3 `SIDE` | Drives the drive's SIDE line — **inverted** (`f_side1 <= not wdata(3)`, `sdcardio.vhdl:2396`) |
| | 4 `SWAP` | Flips bit 8 of the CPU's sector-buffer pointer, i.e. swaps the two 256-byte halves seen through `$D087` (`:2397-2402`). Leave clear |
| | 5 `MOTOR` | Motor and LED on. This alone is enough to spin up |
| | 6 `LED` | Makes the LED *blink*; `$60` is a blinking motor-on, `$20` a steady one |
| `$D081` | 4/3 `STEP`/`DIR` | `$10` steps **out** (head track − 1, toward 0), `$18` steps **in** (+ 1) (`:2690`, `:2736`) |
| | 6 `RDCMD` | `$40` = read sector. Add 1 (`NOBUF`) to reset the buffer pointer first |
| | 7 `WRCMD` | `$80` = write sector |
| `$D082` | 7 `BUSY` | Command executing. Poll this |
| | 4 `RNF` | Sector not found — also "drive not mounted" |
| | 3 `CRC`, 2 `LOST` | Read errors |
| | 0 `TK0` | Head over track 0 |
| `$D084/5/6` | | Requested `TRACK` / `SECTOR` / `SIDE` |
| `$D087` | | Sequential read/write port into the 512-byte buffer |
| `$D089` | | Step rate in 62.5 µs units; default `$80` = 8 ms |

Sector buffer: `$FFD6C00`, 512 bytes. **`$D689` bit 7 (`BUFFSEL`) must be clear** or
both that address and `$DE00` show the SD buffer instead (`registers.md` §7).

## 2. Reading one sector

```asm
        LDA #$20
        STA $D080       ; motor + drive 0, steady LED
        LDA track
        STA $D084       ; 0-based: D81 track 1 is $00
        LDA sector
        STA $D085       ; 1-based, 1..10 per side
        LDA side
        STA $D086
        LDA #$41
        STA $D081       ; read sector, reset buffer pointer
wait:   LDA $D082
        BMI wait        ; BUSY
        AND #$18        ; RNF | CRC
        BNE error
```

Then move the 512 bytes with a DMA job from `$FFD6C00` (§5), or read `$D087` 512 times.
The buffer survives until the next command, so a second read of the same physical
sector can be skipped — worth doing, since the two 256-byte halves of one physical
sector are two consecutive logical sectors of a file (§4).

## 3. Mounted image versus real drive

The same registers serve both, but almost nothing behind them is shared.

| | Mounted D81 image | Real drive |
|---|---|---|
| Sector address | Computed from `$D084`/`$D085`/`$D086` | Matched against the MFM sector header on the media |
| Side | `$D086` **only** | `$D080` bit 3 drives the physical line |
| Stepping | Not needed — the head position is ignored | Needed, or auto-stepping if enabled (`:2531`) |
| `TK0` (`$D082` bit 0) | Just `head_track == 0` (`:2152`) | The drive's real sensor (`:2141`) |
| Format command (`$A0`) | Silently ignored (`:2513`) | Performed |

**Image offset = `track × 20 + physical_sector`**, where `physical_sector` is
`$D085 − 1` for side 0 and `$D085 + 9` otherwise (`sdcardio.vhdl:2168-2181`). Two
consequences:

- **Out-of-range geometry reads the wrong data, not an error.** `track >= 80` or a
  physical sector above 20 clamps the offset to 0, so you get the image's first
  sector with no flag set (`:2181-2183`). `RNF` means *not mounted*, not *bad
  address*.
- **On an image, side 1 is just sectors 11–20 on side 0** — both give the same
  offset. Convenient, and wrong the moment the code meets a real drive.

A drive attached by the hypervisor as a *virtualised* F011 traps each read into the
hypervisor (`HyperTrapRead`, `:2577`) instead of touching the SD card. The register
sequence above is unchanged; only the per-sector cost is.

## 4. From D81 file to F011 sectors

CBM DOS addresses a 1581 disk in **256-byte logical sectors**, 40 per track, tracks
numbered from 1. The F011 moves **512-byte physical sectors** with tracks numbered
from 0. The conversion, for logical track `T` and sector `S` (0–39):

| F011 | Value |
|---|---|
| `$D084` | `T − 1` |
| `$D085` | `(S >> 1) + 1`, minus 10 if that exceeds 10 |
| `$D086` | 0 if it did not exceed 10, else 1 |
| Half of the buffer | `$000` if `S` is even, `$100` if odd |

Each logical sector begins with a two-byte link: next track, next sector. A link
track of 0 marks the last sector, and its sector byte is then the count of valid
bytes. So 254 bytes of payload follow the link in a full sector.

The directory starts at logical track 40, sector 3 — `$D084 = 39`, `$D085 = 2`,
side 0 — and continues along that track. Entries are 32 bytes: file type, start
track, start sector, then a 16-character `$A0`-padded name.

This section is the CBM DOS on-disk layout, not a core-verifiable fact; only the
physical geometry above it comes from `sdcardio.vhdl`.

## 5. Landing the bytes in a bank

The payoff for banked layouts: the destination is a flat 28-bit address, so the
loader never maps the target and never cares what the caller's map looks like.

```asm
        LDA #$80
        TRB $D689       ; BUFFSEL = 0, select the F011 buffer
        LDA #$00
        STA $D704
        LDA #>dmalist
        STA $D701
        LDA #<dmalist
        STA $D705       ; enhanced job

dmalist:
        !byte $0B       ; F018B list format, pinned per job
        !byte $80, $FF  ; source megabyte $FFxxxxx
        !byte $81, $02  ; destination megabyte — e.g. $2xxxxx
        !byte $00       ; end of options
        !byte $00       ; copy
        !word 254       ; payload, link bytes skipped
        !word $6C02     ; $FFD6C00 + 2
        !byte $0D
        !word dest      ; destination, low 16 bits
        !byte $00
        !byte $00
        !word $0000
```

Pinning the list format with option `$0B` matters here: `$D703` bit 0 is whatever the
ROM last left it as, and a loader that runs before any ROM cannot assume
(`registers.md` §5).

## 6. Testing

`xemu`'s `-8 <file>` mounts a D81 on the internal drive, which exercises exactly the
image path in §3 — including its silent-clamp behaviour, so a geometry bug looks like
corrupt data rather than a failure. Cross-check anything side- or step-related against
a real drive before believing it (`xemu-testing.md`).

A public community implementation of this loader is `floppyio.s` in
<https://github.com/smnjameson/Mega65Toolkit>. Useful as a worked example; not
authority — verify its register choices against the core, as above.
