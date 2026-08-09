# MEGA65 KERNAL

Calling the ROM, budgeting zero page, and the Z-register hazard.

Sources: MEGA65 Book `appendix-kernal-jumptable.tex`; `mega65-rom` (`system.src`,
`kernel64.src`, `b65.src`, and the `MEGA65_ROM_ZEROPAGE.md` / `KERNEL-Z-USAGE.md`
notes shipped with it).

---

## 1. Preconditions for every jump-table call

All KERNAL jump-table routines require:

1. `$E000`–`$FFFF` mapped to the KERNAL ROM at `3.E000`–`3.FFFF`.
2. `$0000`–`$1FFF` mapped to KERNAL variable memory at `0.0000`–`0.1FFF`
   (in practice: **unmapped**).
3. The CPU base page register **`B` = `$00`**.

The default BASIC and `SYS` maps satisfy all three. A program that never touches
MAP or `B` can call the KERNAL without setup. A banking scheme must preserve
conditions 1 and 2 at every point where a KERNAL call can happen — including from
inside interrupt handlers (`map-banking.md` §7).

Unless a routine documents otherwise, assume a call **destroys A, X, Y, Z and the
value flags**. Effects on the stack and on the interrupt flag are documented per
routine.

---

## 2. The Z-register hazard

On the 45GS02, `STZ` means **store the Z register**, not "store zero":

> `inst.STZ`: *Store Z Register.* `M ← Z`

It is source-compatible with the 65C02's store-zero only because Z is conventionally
0. Likewise, base-page indirect `($nn)` assembles to the same opcode as `($nn),Z` —
so a non-zero Z silently offsets every such access.

Any code that assumes Z = 0 must therefore treat Z as **caller-preserved across
KERNAL calls that it has verified**, and reload `LDZ #0` after the rest.

### Calls that leave Z non-zero

| Call | Addr | Z on return |
|---|---|---|
| `SCRORG` | `$FFED` | **return value** — window address high byte |
| `RDTIM` | `$FFDE` | **return value** — tenths of a second (0–9) |
| `VERSIONQ` | `$FF2F` | **return value** — ROM version byte 3 (result is in Q) |
| `LOAD` | `$FFD5` | 0 on the slow/burst path, 3 on the FastLoad path — not predictable |
| `SAVE` | `$FFD8` | 0 (implementation detail, not a guarantee) |
| `CURSOR` (disable, C=1) | `$FF35` | cursor column |
| `SWAPPER` | `$FF65` | indeterminate |
| `CINT` | `$FF81` | indeterminate |
| `IOINIT` | `$FF84` | indeterminate |
| `C64MODE` / `MonitorCall` / `BOOT_SYS` | `$FF53` / `$FF56` / `$FF59` | do not return |

### Calls that take Z as an input

| Call | Addr | Meaning of Z |
|---|---|---|
| `SETBNK` | `$FF6B` | Filename bank byte (when X ≥ `$80`) |
| `SETTIM` | `$FFDB` | Tenths of a second, BCD 0–9 |
| `SAVEFL` | `$FF3B` | Flags (bit 6 = raw mode) |

### Calls that preserve Z

The common I/O and file calls preserve Z, either by `PHZ`/`PLZ` or by never touching
it: `BSOUT` `$FFD2`, `BASIN` `$FFCF`, `GETIN` `$FFE4`, `OPEN` `$FFC0`, `CLOSE` `$FFC3`,
`CHKIN` `$FFC6`, `CKOUT` `$FFC9`, `CLRCH` `$FFCC`, `CLALL` `$FFE7`, `CLOSE_ALL` `$FF50`,
`SETLFS` `$FFBA`, `SETNAM` `$FFBD`, `READSS` `$FFB7`, `SETMSG` `$FF90`, `MEMTOP` `$FF99`,
`MEMBOT` `$FF9C`, `IOBASE` `$FFF3`, `PLOT` `$FFF0`, `STOP` `$FFE1`, `ScanStopKey` `$FFEA`,
`RESTOR` `$FF8A`, `VECTOR` `$FF8D`, `RAMTAS` `$FF87`, `KEY` `$FF9F`, `PRIMM` `$FF7D`,
`LKUPLA` `$FF5F`, `LKUPSA` `$FF62`, `ADDKEY` `$FF4A`, `SYSFLAGS` `$FF47`, `GETLFS` `$FF44`,
`GETIO` `$FF41`, the IEC serial group (`TALK` `$FFB4`, `LISTN` `$FFB1`, `SECND` `$FF93`,
`TKSA` `$FF96`, `ACPTR` `$FFA5`, `CIOUT` `$FFA8`, `UNTLK` `$FFAB`, `UNLSN` `$FFAE`), and
the FAR group (`LDA_FAR` `$FF74`, `STA_FAR` `$FF77`, `CMP_FAR` `$FF7A`).

The IRQ and NMI handlers both `PHZ`/`PLZ`, so Z survives interrupts.

**Preserved is not the same as zero.** These calls return Z as *you* left it. The
practical rule: never infer Z from a KERNAL call — set it explicitly with `LDZ #0`
when you need it.

---

## 3. Zero page

`B` = `$00`, so "zero page" is `$0000`–`$00FF` in bank 0.

| Range | Owner | Notes |
|---|---|---|
| `$00`–`$01` | CPU I/O port | Hardware; write-only; unreachable if block 0 is mapped |
| `$02`–`$09` | FAR registers | `bank`, `pc_hi`, `pc_lo`, `s_reg`, `a_reg`, `x_reg`, `y_reg`, `z_reg` — used **only** by `JSRFAR`, `JMPFAR` and BASIC's `SYS` |
| `$0A` | `stkptr` | Allocated but never referenced |
| `$0B`–`$8F` | **BASIC 65 workspace** | The KERNAL never touches it |
| `$56` | `far_mapl_offset_lo` | Exception inside the BASIC range: used by `JSR`/`JMP_FAR` with OFFSET and by `SYS TO ... O(...)` |
| `$90`–`$FA` | KERNAL and screen editor | See below |
| `$FB`–`$FF` | Unallocated | Traditional free KERNAL ZP |

Notable KERNAL locations inside `$90`–`$FA`:

| Addr | Label | Meaning |
|---|---|---|
| `$90` | `status` | IEC I/O status byte (as read by `READSS`) |
| `$99` / `$9A` | `dfltn` / `dflto` | Current default input / output device |
| `$A5`–`$A8` | `farptr` | 32-bit pointer used by `LDA_FAR`/`STA_FAR`/`CMP_FAR` |
| `$A9`–`$AC` / `$AD`–`$B0` | `sal` / `eal` | 32-bit LOAD/SAVE start and end addresses |
| `$B5` | `bp_reg` | Saved base page register |
| `$B7`–`$BE` | `fnlen`…`fnbankhi` | Filename length, address, bank, megabyte |
| `$C4`–`$C7` | `chrptr` | 32-bit pointer to the current screen line |
| `$C8`–`$CB` | `cbdos` | 32-bit pointer to the CBDOS parameter area |
| `$EB` / `$EC` | `tblx` / `pntr` | Cursor row / column |
| `$ED` / `$EE` | `lines` / `columns` | Screen size (24/49 and 39/79) |
| `$F1` | `color` | Current foreground colour |

Bytes explicitly marked free in the ROM source, in addition to `$FB`–`$FF`: `$B6`
and `$D3`–`$D4`.

**Budgeting for a machine-code program.** With BASIC displaced, `$0B`–`$8F` (minus
`$56` if FAR-with-offset is used) is free, as is `$02`–`$0A` for a program that never
calls `JSRFAR`/`JMPFAR`. That is roughly 140 bytes. `$90`–`$FF` must be left alone if
any KERNAL call, interrupt handler, or screen output is used.

Two things that are **not** conflicts, despite appearances:

- **CBDOS zero page.** `dos.src` declares its own variables at `$00`–`$76`, but the
  internal CBDOS runs under a different MAP context (bank 1); `Get_DOS`/`Leave_DOS`
  swap the map around every access. Bank 0 zero page is untouched.
- **Hypervisor traps.** Hyppo runs in its own address space. A trap returns results
  in A/X/Y/Z and the carry flag only; user memory is untouched unless the trap was
  explicitly asked to write somewhere (`loadfile`, `get_mapping`).

---

## 4. FAR access

Two distinct families — do not confuse their costs.

| Call | Addr | Mechanism |
|---|---|---|
| `JSRFAR` / `JMPFAR` | `$FF6E` / `$FF71` | Full context switch. Parameters in `$02`–`$09`; changes the MAP |
| `LDA_FAR` / `STA_FAR` / `CMP_FAR` | `$FF74` / `$FF77` / `$FF7A` | Single byte. Parameters in CPU registers (X = pointer, Y = index, Z = bank); workspace in `farptr` (`$A5`–`$A8`); **does not touch `$02`–`$09`** |
| `SETBNK` | `$FF6B` | Sets the bank used for I/O and filename memory |

For raw far access from your own code, `LDA [$nn],Z` is cheaper than any of these and
has no ZP or MAP side effects (`map-banking.md` §8). The FAR calls are worth using
when you want the KERNAL's bank conventions, or to call code in another bank without
writing your own trampoline.

---

## 5. Jump table

Fixed addresses, guaranteed stable across ROM releases. Derived from the C65 table,
which came from the C128 — **similar names do not imply C64 API compatibility.**
GO64 mode uses the C64 KERNAL instead.

| Addr | Name | Purpose |
|---|---|---|
| `$FF2F` | `VERSIONQ` | ROM version number, into Q |
| `$FF32` | `RESET_RUN` | Reset the computer in various ways |
| `$FF35` | `CURSOR` | Enable or disable the cursor |
| `$FF3B` | `SAVEFL` | Save to file, with flags |
| `$FF41` | `GETIO` | Read current input and output devices |
| `$FF44` | `GETLFS` | Read file, device, secondary address |
| `$FF47` | `SYSFLAGS` | Read/set keyboard locks |
| `$FF4A` | `ADDKEY` | Push a character into the keyboard buffer |
| `$FF50` | `CLOSE_ALL` | Close all files on a device |
| `$FF53` | `C64MODE` | Reset into GO64 mode |
| `$FF56` | `MonitorCall` | Enter the monitor |
| `$FF59` | `BOOT_SYS` | Boot an alternate system from disk |
| `$FF5C` | `PHOENIX` | Cartridge cold start / disk boot loader |
| `$FF5F` / `$FF62` | `LKUPLA` / `LKUPSA` | Look up logical file / secondary address in use |
| `$FF65` | `SWAPPER` | Toggle 40×25 ↔ 80×25 |
| `$FF68` | `PFKEY` | Program an editor function key |
| `$FF6B` | `SETBNK` | Set bank for I/O and filename memory |
| `$FF6E` / `$FF71` | `JSRFAR` / `JMPFAR` | Call / jump to any bank |
| `$FF74` / `$FF77` / `$FF7A` | `LDA_FAR` / `STA_FAR` / `CMP_FAR` | Byte access in any bank |
| `$FF7D` | `PRIMM` | Print inline null-terminated string |
| `$FF81` | `CINT` | Initialise screen editor |
| `$FF84` | `IOINIT` | Initialise I/O devices |
| `$FF87` | `RAMTAS` | Initialise RAM and buffers |
| `$FF8A` / `$FF8D` | `RESTOR` / `VECTOR` | Initialise / read-set the KERNAL vector table |
| `$FF90` | `SETMSG` | Enable/disable KERNAL messages |
| `$FF93` / `$FF96` | `SECND` / `TKSA` | Secondary address to listener / talker |
| `$FF99` / `$FF9C` | `MEMTOP` / `MEMBOT` | Read/set memory limits |
| `$FF9F` | `KEY` | Scan the keyboard |
| `$FFA2` | `MONEXIT` | Monitor's exit to BASIC |
| `$FFA5` / `$FFA8` | `ACPTR` / `CIOUT` | Byte from talker / to listener |
| `$FFAB` / `$FFAE` | `UNTLK` / `UNLSN` | Untalk / unlisten |
| `$FFB1` / `$FFB4` | `LISTN` / `TALK` | Listen / talk |
| `$FFB7` | `READSS` | Status of the last I/O operation |
| `$FFBA` / `$FFBD` | `SETLFS` / `SETNAM` | Set file/device/SA; set filename |
| `$FFC0` / `$FFC3` | `OPEN` / `CLOSE` | Open / close a logical file |
| `$FFC6` / `$FFC9` / `$FFCC` | `CHKIN` / `CKOUT` / `CLRCH` | Set input / output channel; restore defaults |
| `$FFCF` / `$FFD2` | `BASIN` / `BSOUT` | Read / write a character |
| `$FFD5` / `$FFD8` | `LOAD` / `SAVE` | Load or verify / save |
| `$FFDB` / `$FFDE` | `SETTIM` / `RDTIM` | Set / read the CIA1 24-hour clock |
| `$FFE1` / `$FFEA` | `STOP` / `ScanStopKey` | Report / scan the Stop key |
| `$FFE4` | `GETIN` | Read a character without waiting |
| `$FFE7` | `CLALL` | Close all files and channels |
| `$FFED` | `SCRORG` | Current screen window size |
| `$FFF0` | `PLOT` | Read/set cursor position |
| `$FFF3` | `IOBASE` | I/O base address |

Addresses not listed (`$FF38`, `$FF3E`, and others) are marked RESERVED — do not call
them.

---

## 6. Symptom → cause

| Symptom | Check |
|---|---|
| KERNAL call crashes or returns garbage | Preconditions §1 — MAP over `$E000` or `$0000`, or `B ≠ 0` |
| Pointer dereferences read from the wrong address after a call | Z left non-zero (§2); `LDZ #0` |
| `STZ` writes a non-zero byte | Same cause — `STZ` stores Z |
| Screen output stops working after a disk call | The call changed MAP, `$D030`, or the I/O personality. Re-establish the map and personality, then `CLRCH` (`$FFCC`) to reset the channels. Reported in the field but not fully characterised — verify against `system.src` before relying on any specific remedy |
| Filename not found although the bytes look right | Filenames are PETSCII: uppercase letters are `$C1`–`$DA`, not `$41`–`$5A` |
| Program corrupts itself after using ZP | Wrote into `$90`–`$FF` while the KERNAL or an IRQ handler was live (§3) |
