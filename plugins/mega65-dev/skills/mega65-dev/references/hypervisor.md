# Hyppo, the MEGA65 hypervisor

Hyppo owns the SD cards, the ROM write-protection, the boot process, and the freezer.
Anything those touch goes through a trap.

Sources: MEGA65 Book `appendix-hypervisor-calls.tex`; `mega65-core/src/hyppo/*.asm`;
`mega65-core/docs/secure_mode.md`; `mega65-core/src/vhdl/gs4510.vhdl`.

---

## 1. Calling a trap

Hyppo lives in an address space of its own, so `JSR` cannot reach it. **Writing** to
`$D640`–`$D67F` switches the CPU into hypervisor mode and starts a service:

```asm
        LDA #$74        ; service selector — must be in A
        STA $D640       ; trap number = address - $D640
        CLV             ; see below
```

Rules:

- The selector **must** come from A. Writing the same value from X, Y or Z does not work.
- Which service runs depends on **both** the value in A **and** which trap address you
  write to. Several services share `A` values across `$D640`/`$D641`/`$D642`.
- `$D640`–`$D67F` are present only in the **MEGA65 I/O personality**, and in the
  ethernet one: `gs4510.vhdl` traps on `$FFD367F` or `$FFD267F`, so the C64 and C65
  personalities do not (`memory-map.md` §4). Unlock with the `$D02F` knock before the
  first trap. In C64 mode the `STA $D640` falls into a SID mirror instead, leaving the
  carry alone — which reads as whatever the caller last set, so an unlocked-personality
  bug can look like success.
- **Bit 0 of A is ignored.** `dos_and_process_trap` masks with `#$7E` before indexing
  its jump table, so `$34` and `$35` select the same service.
- On return, registers are preserved except those the service uses for results.
- User memory — including zero page — is untouched unless the service was explicitly
  asked to write somewhere.

**Why `CLV`.** The CPU may or may not execute the byte following the `STA`. A `CLV`
there is harmless either way. `NOP` also works but is risky: on this CPU `NOP` is a
prefix byte for 32-bit addressing modes, so it can change the meaning of the next
instruction. Prefer `CLV`.

**Errors.** Carry set = success. Carry clear = failure, with an error code in A.
`hyppo_geterrorcode` (`$D640`, `A=$38`) re-reads the last code.

| Code | Meaning |
|---|---|
| `$08` | partition error |
| `$10` | invalid address |
| `$80` | no such drive |
| `$81` | name too long |
| `$84` | too many open files |
| `$85` | invalid cluster |
| `$86` | is a directory |
| `$87` | not a directory |
| `$88` | file not found |
| `$89` | invalid file descriptor |
| `$8A` | image wrong length |
| `$8B` | image fragmented |
| `$8D` | file exists |
| `$8F` | double attach |

---

## 2. Traps worth knowing

Full descriptions, inputs and outputs: `appendix-hypervisor-calls.tex`. Services
marked *not implemented* there are omitted below.

### General

| Trap | A | Service |
|---|---|---|
| `$D640` | `$00` | `getversion` — Hyppo and HDOS version |
| `$D640` | `$38` | `geterrorcode` |
| `$D640` | `$3A` | `setup_transfer_area` — Y = page used for data transfer |

### Memory and ROM

| Trap | A | Service |
|---|---|---|
| `$D640` | `$70` | `toggle_rom_writeprotect` — flip write protection on banks 2 and 3 |
| `$D641` | `$02` | `rom_writeenable` |
| `$D641` | `$00` | `rom_writeprotect` |
| `$D640` | `$74` | `get_mapping` — Y = destination page; writes 6 bytes (`map-banking.md` §6) |
| `$D640` | `$76` | `set_mapping` — Y = source page; installs a map from the same 6-byte structure |
| `$D640` | `$72` | `toggle_force_4502` — switch the CPU personality between 45GS02 and 6502 |
| `$D640` | `$7E` | `reset` — warm boot |

The write-protect state is not readable; test it by writing (`memory-map.md` §5).
`set_mapping` gives no protection against mapping out the executing code.

### SD card files (HDOS)

Only Hyppo can reach the SD cards. Typical sequence: select drive → set name →
open/find → read.

| Trap | A | Service |
|---|---|---|
| `$D640` | `$02` / `$04` | `getdefaultdrive` / `getcurrentdrive` |
| `$D640` | `$06` | `selectdrive` |
| `$D640` | `$3C` | `cdrootdir` — select drive (X) and go to its root |
| `$D640` | `$0C` | `chdir` |
| `$D640` | `$2E` | `setname` — set the working filename |
| `$D640` | `$34` / `$30` / `$32` | `findfile` / `findfirst` / `findnext` |
| `$D640` | `$12` / `$14` / `$16` | `opendir` / `readdir` / `closedir` |
| `$D640` | `$18` / `$1A` / `$1C` / `$20` | `openfile` / `readfile` / `writefile` / `closefile` |
| `$D640` | `$1E` | `mkfile` — create a contiguous file, size in X/Y/Z, 8.3 names only |
| `$D640` | `$22` | `closeall` |
| `$D640` | `$26` | `rmfile` |
| `$D640` | `$36` | `loadfile` — load at a 24-bit address (X/Y/Z), top byte forced to zero |
| `$D640` | `$3E` | `loadfile_attic` — same, with the top byte `$08` |
| `$D640` | `$48` | `get_proc_desc` — copy the process descriptor to page (A) |

`seekfile` (`$24`), `rename` (`$2A`) and `filedate` (`$2C`) dispatch to
"not implemented" (`dos.asm`); `fstat` (`$28`) is incomplete.

`loadfile` is usually the shortest path from "I have a filename" to "the bytes are in
memory", and it does not disturb the KERNAL's file state. It reaches only the **low
16 MB**: `dos.asm` forces address byte 3 to zero and increments only the middle two
bytes, so the address arithmetic wraps inside 16 MB rather than carrying out of it.

Five things about this group that the trap numbers do not tell you:

- **`setname` takes a page number in Y, not a pointer**, and the page must be
  `$00`–`$7E` (`hypervisor_setup_copy_region`, `main.asm`). A buffer anywhere else
  fails with `$10`, invalid address. The same applies to `readdir`'s destination.
- **Matching upper-cases the *request* only.** `dos_dirent_compare_name_to_requested`
  (`dos.asm`) runs `toupper` over the requested name and compares it byte-for-byte
  against the stored long name. A file whose name on the card contains lower case can
  therefore never be found — write names in upper case when you create them. There is
  no wildcard support.
- **`readfile` reports EOF as failure**: C=0 with A=0 and X=Y=0, which is
  indistinguishable from an error unless you check the returned count.
- **A failed `findfile` leaves the previous dirent intact**, so an `openfile` after one
  silently reopens the file found before it.
- **Any file or directory call clears `$D030` bit 0** and never restores it —
  `sd_map_sectorbuffer` does `lda #$01 / trb $D030` (`sdfat.asm`) because colour RAM at
  `$DC00` would block the sector buffer at `$DE00`. If you had colour RAM there, it has
  moved.

**The sector buffer is unmapped again on every trap return** (`return_from_trap_with_*`
in `main.asm` both `jsr sd_unmap_sectorbuffer`), so `$DE00` is not readable when you get
control back — even after `readfile`, which had just mapped it. Read the data at
`$FFD6E00` instead, and set `$D689` bit 7 first: outside hypervisor mode only the low
nine address bits reach the buffer and that bit chooses between the SD and F011 buffers
(`sdcardio.vhdl`), so with it clear you read the floppy controller's buffer instead.

### Disk images (virtualised F011)

| Trap | A | Service |
|---|---|---|
| `$D640` | `$4A` | `attach` — attach or detach an image to a virtual drive (X) |
| `$D640` | `$44` | `d81write_en` — enable writing to attached images |

`d81attach0` (`$40`), `d81attach1` (`$46`) and `d81detach` (`$42`) are deprecated in
favour of `attach`.

### Configuration and freezer

| Trap | A | Service |
|---|---|---|
| `$D642` | `$00` / `$02` / `$04` | `configsector_read` / `_write` / `_apply` |
| `$D642` | `$06` | `configsector_set` |
| `$D642` | `$08` | `dmagic_autoset` — set the DMAgic revision from the loaded ROM |
| `$D642` | `$10` / `$12` / `$14` / `$16` | `locate_freeze_slot` / `unfreeze_from_slot` / `read_freeze_region_list` / `get_slot_count` |
| `$D67F` | any | `freeze_self` — launch the freezer |

**A freeze slot is a run of SD sectors, not memory.** A 28-bit "frozen address" is a
key into a region table, not a location. Reading one byte transfers a whole 512-byte
sector; writing one byte reads a sector, changes a byte and writes it back. Batching
is therefore not an optimisation — it is the difference between 2 and 2N transfers.

`freeze_mem_list` in `mega65-core/src/hyppo/freeze.asm` gives the layout: per region
**4 bytes base, 3 bytes length, 1 byte preparatory action**, terminated by `$FF` in
the action byte. Regions lie back to back starting at the slot's *second* sector — the
first holds the SD sector buffer as it was before freezing — each rounded up to a whole
sector. The length field carries flags above bit 23: **mask with `$7FFFFF`**, or a
region declared `$801000` long looks 8 MB rather than 4 KB.

The process descriptor read by `get_proc_desc` groups its fields **by kind, not by
drive**: flags for both drives adjacent, then both name lengths, then both names.
Indexing by drive works, and is safer than hand-written offsets.

### Serial debugger

| Trap | A | Service |
|---|---|---|
| `$D640` | `$7C`, Y = byte | `serial_monitor_write` — write without waiting |
| `$D643` | byte | `serial_monitor_wait_and_write` |

---

## 3. Hypervisor mode as CPU state

Facts from `gs4510.vhdl` that matter to systems code:

- **`$D640`–`$D67F` are dual-purpose.** From normal mode a write triggers a trap. From
  *inside* hypervisor mode the same addresses are the saved user register file:
  `REGA` `$D640`, `REGX` `$D641`, `REGY` `$D642`, `REGZ` `$D643`, and so on through the
  saved MAP state. Writing `$D67F` returns to user mode.
- **MAPHI is locked in hypervisor mode.** The `MAP` handler skips the MAPHI
  offset/selection update while `hypervisor_mode = '1'`, so the upper 32 KB cannot be
  de-mapped from under Hyppo. MAPLO and both megabyte bytes are still settable.
- **Entry and exit save and restore the full map** — offsets, selection nibbles and
  both megabyte bytes — so a trap never disturbs the caller's memory configuration.
- The Hyppo ROM occupies `$FFD8000`–`$FFDBFFF` (16 KB) and is only visible in
  hypervisor mode. Its scratch space is `$FFD6000`–`$FFD6BFF`.

---

## 4. Operating modes, and what Hyppo actually virtualises

Hyppo is closer to a process supervisor than to a virtual-machine hypervisor. It runs
programs in one of three modes:

| Mode | Used for |
|---|---|
| C64-like | C64 programs; entered by holding the MEGA key at boot or via `GO64` |
| C65-like | **The normal mode.** Ordinary MEGA65 programs and BASIC 65 |
| MEGA65 | System programs only: freezer, configuration utility, Matrix Mode debugger |

A running program can effectively change mode by enabling or disabling hardware
features; there is no C128-style hard partition.

Virtualisation is deliberately thin. The floppy controller is virtualised, so disk
images can stand in for physical disks. The serial bus is not (yet).

**Three different DOSes**, easily confused:

| Name | Lives in | Understands |
|---|---|---|
| HDOS | Hyppo | FAT32 on the SD cards. Knows nothing about Commodore filesystems |
| CBDOS | The KERNAL | 1581-like filesystems, via the 45IO27 controller. Knows nothing about SD cards |
| Drive DOS | Each IEC device | That device's own disks |

"Drive" means a different thing in each: an SD-card partition for HDOS, a physical
(or virtualised) unit for CBDOS, a device number on the bus for the third.

`HICKUP.M65` on the SD card updates Hyppo without reflashing the core — which is why
Hyppo is sometimes called "Hickup".

---

## 5. Secure mode

A compartment for code that must run without I/O access. Bit 7 of the protected
hardware register `$D672` disables all I/O except the touch pad (`$D6Bx`), audio
(`$D6F0`–`$D6FE`), the SIDs and the VIC-IV. The gate is `hyper_protected_hardware(7)`
in `gs4510.vhdl`. Note that `$D672` is inside the trap range, so a write from user
mode is trap `$32`, not a register write — the bit is set from hypervisor mode.

The transition is arbitrated by the embedded monitor CPU, not by software: entering
or leaving a secure compartment — and any hypervisor trap taken from inside one —
stops the main CPU and asks the user to ACCEPT or REJECT at the monitor. On REJECT
the monitor erases memory before letting the CPU continue.

Implementation and current status: `mega65-core/docs/secure_mode.md` and
`src/hyppo/securemode.asm`. Treat the details as in flux.

The system partition on the SD card holds freeze slots, the configuration sector, and
service data; see `mega65-core/docs/MEGA65_System_Partition.md`.
