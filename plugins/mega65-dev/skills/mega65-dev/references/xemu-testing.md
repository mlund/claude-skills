# Testing and debugging under xemu

`xemu`'s MEGA65 target (`xmega65`) is the practical way to run, inspect and
regression-test MEGA65 code without hardware. It is scriptable, headless-capable,
and can be driven the way a person drives the machine.

Source: <https://github.com/lgblgblgb/xemu> — `targets/mega65/`. Ask the user for a
local checkout if a claim needs checking; **xemu's own source is the authority on
what an option really does**, since the help text is terse and sometimes stale.

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
| `-prgexit` | Exit when the `READY.` prompt is reached |
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
at its real address and stride (`SCRNPTR` at `$D060`–`$D063`, row stride `LINESTEP` at
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

**The codes are keyboard-matrix positions, not ASCII or PETSCII.** `m` is `$24`
because of where the key sits in the matrix. The matrix is defined in
`mega65-core/src/vhdl/matrix_to_ascii.vhdl`.

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
- **RESTORE cannot be injected this way** — it is an NMI, not a matrix key. In the GUI
  it is **PageDown** (explicitly not Tab, since C65-style keyboards have their own
  Tab), and it must be *held*: the trap fires only after roughly 20 frames.
- State that persists in the SD-card image — an attached disk image, a freeze slot —
  can be created once by hand and reused as a fixture.

---

## 5. Getting code onto real hardware

`mega65_ftp` (from `mega65-tools`) copies files over ethernet with auto-discovery, so
no serial cable is needed:

```sh
mega65_ftp -e -y -c "put PROGRAM.M65 PROGRAM.M65" -c "exit"
```

`-e` selects ethernet with auto-discovery and `-y` skips confirmation, which is needed
for scripted `-c` commands. `-c "dir" -c "exit"` lists the card. Stamping a version
string into the binary lets a script compare before uploading and skip identical builds.

---

## 6. Where the emulator and the hardware part company

Emulator agreement is not hardware agreement. Known divergences, worth treating as
emulator-passes-hardware-fails candidates:

- **The `$DE00` sector-buffer mapping uses a fixed buffer pointer in xemu**, so
  `BUFSEL` (`$D689` bit 7) mistakes go unnoticed there and fail on hardware
  (`registers.md` §7).
- **A frozen program's thumbnail region is not populated** the way hardware populates it.

When something behaves differently on hardware, read the corresponding VHDL in
`mega65-core` and the corresponding emulation in `xemu/targets/mega65/` and compare —
the difference is usually explicit in one of them.

---

## 7. Method

- **Measure before theorising.** A/B against a reference binary and a memory dump beats
  reasoning from source about a suspected hardware bug.
- **A checker that has only ever reported success is worthless.** Break the code
  deliberately, confirm the check fires, then restore it.
- **Prefer flat 28-bit addressing in test code.** It bypasses MAP and the I/O
  personality, so a check does not depend on machine state it did not establish
  (`map-banking.md` §8).
