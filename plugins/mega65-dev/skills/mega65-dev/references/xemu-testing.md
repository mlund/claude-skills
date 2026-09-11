# Testing and debugging under xemu

`xemu`'s MEGA65 target (`xmega65`) is the practical way to run, inspect and
regression-test MEGA65 code without hardware. It is scriptable, headless-capable,
and can be driven the way a person drives the machine.

Source: <https://github.com/lgblgblgb/xemu> — `targets/mega65/`. Ask the user for a
local checkout if a claim needs checking; **xemu's own source is the authority on
what an option really does**, since the help text is terse and sometimes stale.

---

## 0. First, decide what actually needs the machine

Much of a MEGA65 program is not hardware access: it is arithmetic over formats the
machine defines — FAT32 records, D81/D65 geometry, freeze-slot region walks, register
field packing, PETSCII conversion. Code compiled from C or C++ can be split into its
own translation unit and run natively, which is far faster to exercise than any
emulator and points at a line rather than a hung machine. For the mechanics — the
split, the harness, and the `char`/`int` width gaps that make a host pass meaningless
— see `host-testing.md` in the `llvm-mos` skill. Everything below covers the half that
genuinely needs the machine.

The part of that which is MEGA65 knowledge is **where the expected values come from**.
These formats are defined by the core, not by your program, so an oracle exists
independently of it — and a test whose expectations were transcribed from the core
catches the implementation being wrong in the first place, where one copied out of the
implementation only catches later edits to it.

| Question | Source |
|---|---|
| D81/D65 image sizes a mount will accept | `mega65-core/src/hyppo/dos.asm`, `dos_checkimage` |
| What a freeze slot contains, and in what order | `mega65-core/src/hyppo/freeze.asm`, `freeze_mem_list` |
| Register field positions and widths | `mega65-core/iomap.txt` |
| Hardware behaviour behind an encoding | `mega65-core/src/vhdl/*.vhdl` |
| Keyboard matrix positions | `matrix_to_ascii.vhdl` (`matrix_normal`, `matrix_shift`) |

---

## 1. Options that matter for automation

| Option | Effect |
|---|---|
| `-headless` | No window. Required for CI |
| `-sleepless` | Run at maximum speed rather than real time |
| `-besure` | Skip "are you sure?" prompts on reset and exit |
| `-testing` | Enable privileged test features, including the exit register (§2) |
| `-uartmon <path>` | Expose the serial monitor on a Unix socket (§4) |
| `-prg <file>` | Load a PRG/M65 directly, autodetecting the load address |
| `-prgmode 64\|65` | Override that autodetection |
| `-prgtest <spec>` | Override the startup command, and side-load files (§1a) |
| `-prgexit` | Exit when the `READY.` prompt is reached |
| `-hdosvirt -hdosdir <dir>` | Serve a host directory as the SD card, through the HDOS traps |
| `-sdimg <file>` | Use a specific SD-card image |
| `-8 <file>` | Mount an external D81 on drive 8 via the floppy controller |
| `-dumpmem <file>` | Write all 384 KB of Chip RAM on exit |
| `-dumpscreen <file>` | Write the screen as ASCII on exit (§3) |
| `-allowfreezer` | Allow the freezer trap to fire |
| `-model <n>` | Emulated model ID, as read back at `$D629` |

`-allowfreezer` is described in `configdb.c` as "[NOT YET WORKING]"; the freezer trap
nonetheless reports "FREEZER is not enabled" without it. Check the behaviour against
the build in use.

```sh
xmega65 -headless -sleepless -testing -besure \
        -uartmon /tmp/x.sock -prgmode 64 -prg PROGRAM.M65
```

### 1a. `-prg` starts the program only if the load address is a BASIC one

`-prg` waits for `READY.`, `memcpy`s straight into Chip RAM — so it reaches RAM under
a ROM, and no `CLR` runs — and then decides what to type:

- load address `$0801` (C64) or `$2001` (C65): types `RUN:` and presses RETURN.
- anything else: types `SYS<load_addr>` and **does not press RETURN**. Nothing runs.

So a program whose entry is not at a BASIC load address needs `-prgtest` to start:

```sh
xmega65 -headless -sleepless -testing -prgmode 65 \
        -prg GAME.PRG -prgtest 'SYS8192'
```

`-prgtest` takes `;`-separated items. An item containing `@` is `FILE@ADDR` and is
written to the 28-bit address (`$` prefix for hex) before the program starts — useful
for planting data the program expects without building an image for it. Any other item
is appended to the startup command, and supplying one is what makes xemu press RETURN.

**Pass `-prgmode` explicitly.** With autodetection and a non-BASIC load address, xemu
opens a modal "C64 or C65?" dialog, which hangs a headless run.

---

### Loading a test PRG from SD in BASIC 65

For a loose PRG on the SD card, use unit 12:

```basic
DIR U12,P
CHDIR "DEMOS",U12
DLOAD "DEMO.PRG",U12
RUN
```

`DIR U12,P` lists the current SD directory by page; press Q to stop or another
key to continue. Omit `,P` for an unpaged listing. `CHDIR` is optional;
`CHDIR "..",U12` goes to the parent directory. Include the `.PRG` suffix.

`RUN` requires a BASIC-startable PRG. For other machine-code programs, use their
documented load address and entry procedure. Files inside a D81 or D64 image need
the image mounted first, then loading from its drive rather than unit 12.

Source: MEGA65 book, `mega65-user-guide/using-disks.tex`, “Accessing the SD Card
from BASIC” and “DLOAD and RUN”.

---

## 2. Exiting with a status code

With `-testing`, `$D6CF` becomes an exit channel. Every write stores the byte as the
pending exit status; writing `$42` exits the emulator with it
(`targets/mega65/io_mapper.c`, case `0xCF`).

```asm
        LDA #<code>     ; becomes the process exit status
        STA $D6CF
        LDA #$42
        STA $D6CF       ; xemu exits here
```

Two properties make this the backbone of a test harness:

- **The status carries information.** Number your checks and exit with the number of
  the one that failed, so a non-zero status says *which* invariant broke, not merely
  that something did.
- **The same binary runs on hardware.** `$D6CF` is the FPGA reconfiguration trigger on
  real hardware, and only reacts to `$42`; a status write lands harmlessly, and on
  hardware the `$42` write prompts rather than silently exiting.

The natural shape is therefore: the test program runs *on* the machine and checks its
own invariants, rather than an external harness inspecting from outside.

---

## 3. Reading the screen back

`-dumpscreen` walks **one byte per cell**. That is correct for 8-bit text mode and
wrong for 16-bit character mode, where it emits `width × height` bytes and so covers
only half the rows — and the missing rows look exactly like blank ones. It also strips
trailing spaces per line and drops trailing blank lines.

For anything but plain 8-bit text, use `-dumpmem` and read the screen out of the dump
at its real address and stride (`SCRNPTR` at `$D060`–`$D062` plus `$D063` bits 0–3, row stride `LINESTEP` at
`$D058`–`$D059`). Colours come out of the same dump: the first 2 KB of colour memory is
mirrored at `$1F800`.

Remember the character encoding: the default charset is the C64 ROM set, so the screen
holds **PETSCII screen codes**, not ASCII — `A`–`Z` are `$01`–`$1A`, `$20`–`$3F`
coincide with ASCII, and `$41`–`$5A` are graphics characters.

---

## 4. Driving a TUI: keypresses over the serial monitor

`-uartmon <path>` exposes the same serial monitor that real hardware offers over its
serial port, on a Unix socket. The monitor's memory-write command can therefore poke
the machine while it runs — and the core provides three **synthetic key slots** for
exactly this:

| Register | Field | Meaning |
|---|---|---|
| `$D615` bits 0–6 | `VIRTKEY1` | Virtual key down, or `$7F` for none |
| `$D616` bits 0–6 | `VIRTKEY2` | Second simultaneous key |
| `$D617` bits 0–6 | `VIRTKEY3` | Third simultaneous key |

Writing a code there is indistinguishable from a physical key press, so a menu-driven
program can be exercised through its real input path rather than through a test-only
back door. Hold a modifier by putting it in a second slot; release by writing `$7F`.

All three slots are real and symmetric: `$D615`–`$D617` reach `virtual_key1..3` in
`iomapper.vhdl`, which feed `virtual_to_matrix.vhdl`, where each is compared against
the scan phase and pulls its matrix line low independently. Two further slots carry
touch input, so five positions can be held at once. xemu implements the same three
(`virtkey_state[3]` in `targets/mega65/input_devices.c`, decoded at
`io_mapper.c:592`), masking to 7 bits and ignoring codes ≥ 72.

**The codes are keyboard-matrix positions, not ASCII or PETSCII.** `m` is `$24`
because of where the key sits in the matrix. The injection mechanism is
`mega65-core/src/vhdl/virtual_to_matrix.vhdl`; the position-to-character mapping is
the `matrix_normal` and `matrix_shift` tables in `matrix_to_ascii.vhdl`.

This gives a complete loop for testing an interactive program:

1. Start xemu headless with `-uartmon` and the program loaded.
2. Inject keys through `$D615`–`$D617` over the socket.
3. Observe the result three ways — **screen** (dump or read `SCRNPTR` memory),
   **memory** (`-dumpmem`, or monitor reads of specific addresses), and the
   **SD-card image** on disk, for anything that persists.
4. Exit with a status code (§2).

Practical notes:

- **Socket paths must be short.** `AF_UNIX` caps near 104 characters, so the socket
  cannot live under a long temporary directory.
- **RESTORE is a special case, and the emulator does not implement it** (§6). In the
  xemu GUI it is **PageDown** — explicitly not Tab, since C65-style keyboards have
  their own Tab — and it must be *held*: the trap fires only after roughly 20 frames.
- State that persists in the SD-card image — an attached disk image, a freeze slot —
  can be created once by hand and reused as a fixture.

---

## 5. Getting code onto real hardware

The same serial-monitor harness can drive hardware and xemu: `m65harness.py`
(<https://gist.github.com/mlund/48c045f127f600dbe3f238a52d50099e>) offers `attach()` and
`launch()` behind one `Machine` API. It supports 28-bit `read`/`write` while a program
runs and `press`/`type_text` through the synthetic key slots. Standard library only.

Tools are `m65` and `mega65_ftp` from mega65-tools, bundled with M65Connect. Use
`-s 2000000` on both; the default is far slower.

What follows is observed behaviour of those two host tools, not of the core, and it has
moved between builds: figures and quirks below are from 20251015.20 unless noted. Check
against the build in use. Each rule names the symptom it produces, because most of them
fail as something else entirely.

### 5a. Copying files to the SD card

```sh
mega65_ftp -l /dev/cu.usbserial-XXXX -s 2000000 -c "put PROGRAM.M65" -c "exit"
```

`-e` selects ethernet with auto-discovery instead, and is about **six times quicker**:
one 223 KB file went at 218 KB/s over ethernet against 36 KB/s over serial at
`-s 2000000`. It needs remote-control mode armed by hand — DIP switch 2 on, then
SHIFT+POUND — and **that does not survive a reset from `m65 -F`**: the next transfer
refuses outright, naming the two steps. The reset `mega65_ftp`'s own `exit` performs is
not one of those, and consecutive invocations work; re-arm only after resetting the
machine by other means.

**A transfer rate under a few hundred KB is not a measurement.** `mega65_ftp` reports
whole seconds, so a 14 KB file reads as 13.9 KB/s over either link. Time a large one.

- **The machine must be idle.** In the tested build, `mega65_ftp` installs a helper into
  RAM, so it hangs against a looping program. Reset first. It also leaves the helper
  resident, which garbles the screen and takes the BASIC prompt away until the next
  reset.
- **Build `put` commands from a shell glob, not coloured `ls` output.** ANSI escapes
  in filenames caused `stat()` failures while the tested command still exited 0.
  Count the `put` lines and read the transfer output rather than filtering for a
  success word.
- **Compare file contents, not size or timestamp.** In the tested build, replacing a
  same-size file often left the FAT date unchanged, while rebuilt binaries differed
  at the same size. Hash the local file and compare that.

### 5b. Starting a program

```sh
m65 -l /dev/cu.usbserial-XXXX -s 2000000 -F -1 PROGRAM.PRG
```

`-F` (reset) and `-1` (load) belong in **one call**: a later reset throws the injected
program away, and without `-F` a program already looping leaves no prompt to type into.
The `.prg` goes straight into RAM and need not be on the card, but any asset it reads
must already be there.

- **The loader may spin at 100% after transferring, holding the serial port** so that
  nothing else can talk to the machine (seen with `-F -1` on 20251015.20). In that
  case, wait about 45 s, then kill it. Compare memory against the `.prg` before
  concluding that the load failed; an early kill can leave the entry bytes unwritten.
- **Send `t0` down the monitor before typing.** On the tested setup, the CPU could be
  left halted even when the loader exited 0, making synthetic keys appear ineffective.
- **Type `SYS<entry>` rather than using `g`.** The tested `t1`, `g2000`, `t0` sequence
  returned to BASIC, while `-r` could not start a `$2000` machine-code image.
- **Type in lower case.** BASIC boots in upper-case/graphics mode, so shifted
  upper-case letters can arrive as graphics.
- **Read the echoed line back before retrying.** Slow character delivery can make a
  retry append to the existing input and contaminate subsequent measurements. Search
  for the typed text and require an exact match before continuing.
- **Do not inject a key by writing `$D610`.** That register dequeues ASCII input; use
  the `$D615`–`$D617` synthetic-key slots of §4.

### 5c. Reading a running program back

`m65harness`'s `read` works on any 28-bit address while the program runs, which is
sufficient for readback. Two cautions:

- **`settled()` and `snapshot()` freeze the machine** and show a screen that is not the
  one being drawn. To watch a running program use raw `read`, including for the screen.
- **In 8-bit text mode the screen is contiguous screen codes, one byte per cell.**
  Do not de-interleave it as character-and-colour pairs; colour lives in colour RAM.
  Decode per §3 before diagnosing a typing failure.
- **A program meant for hardware should park rather than exit, and leave its diagnostic
  where the monitor can read it.** Take that address from the link map every time: a
  hand-written one reported plausible values belonging to something else after a buffer
  moved underneath it. Clear it at start-up too, or a value from an earlier run is
  indistinguishable from a failure.

`m65 -S` renders a reconstruction from screen and glyph memory, not the VIC's output.
Treat the result as diagnostic evidence only; it may not match a display that is being
updated concurrently.

### 5d. Attic RAM can stop answering

**Observed on hardware, mechanism not established.** HyperRAM sometimes stops retaining
writes, and **a reset does not bring it back — only a power cycle does**. Every symptom
blames software: a Hyppo file load into Attic RAM reports success and stores nothing, so
a format check on the loaded image fails and points at the parser.

Test it directly before believing any software explanation — write two complementary
patterns to an Attic address over the monitor and read them back:

```
$8000000 <- A5 5A, reads back 00 00   # dead: a reset will not fix this
```

Two patterns, not one: memory answering a single fixed value passes a one-pattern
check, and complements fail a bus held high or low. A program loading into Attic RAM is
worth giving the same probe at start-up.

## 6. Where the emulator and the hardware part company

Emulator agreement is not hardware agreement. Known divergences, worth treating as
emulator-passes-hardware-fails candidates:

- **RESTORE can be injected through the synthetic keyboard on hardware, but not in
  xemu.** `virtual_to_matrix.vhdl` special-cases two values in *any* of the three
  slots: `$52` holds RESTORE down, and `$72` taps it with a ~100-cycle timeout. xemu's
  `virtkey()` has no such case — it treats every value as a plain matrix scancode. So
  a test that drives RESTORE this way passes on hardware and does nothing under the
  emulator, which is the inverse of the usual failure direction.
- **The `$DE00` sector-buffer mapping uses a fixed buffer pointer in xemu**, so
  `BUFSEL` (`$D689` bit 7) mistakes go unnoticed there and fail on hardware
  (`registers.md` §7).
- **A frozen program's thumbnail region is not populated** the way hardware populates it.
- **Attic RAM has no wait states in the emulator**, which reads it out of a plain
  array. So the cost of putting code or data in HyperRAM is exactly what xemu cannot
  show, and any such figure has to come from hardware. Nor can xemu reproduce §5d.

When something behaves differently on hardware, read the corresponding VHDL in
`mega65-core` and the corresponding emulation in `xemu/targets/mega65/` and compare —
the difference is usually explicit in one of them.

If an equivalent failure reproduces under an emulator that omits the suspected
mechanism, investigate shared software causes first. Compare state and outputs
before equating the failures: the same symptom can arise by different paths.

---

## 7. Method

- **Never report a timing without a correctness check in the same run.** A wrong
  answer arrives sooner than a right one, so an optimisation that breaks the algorithm
  reads as a large speedup. Hash or checksum the output against a known vector, and
  report both numbers together.
- **Observing the target can change it.** Reading memory over the serial monitor halts
  the CPU at an instruction boundary, which is not the same as an interrupt and is not
  subject to the same guarantees — 45GS02 Q instructions are known to compute wrong
  answers when polled mid-run (`llvm-mos` skill, `references/45gs02.md` §4). Sample
  before and after a timed region, not during it, and if a result only misbehaves under
  observation suspect the observation first.
- **Measure before theorising.** A/B against a reference binary and a memory dump beats
  reasoning from source about a suspected hardware bug.
- **A checker that has only ever reported success is worthless.** Break the code
  deliberately, confirm the check fires, then restore it.
- **Prefer flat 28-bit addressing in test code.** It bypasses MAP and the I/O
  personality, so a check does not depend on machine state it did not establish
  (`map-banking.md` §8).
