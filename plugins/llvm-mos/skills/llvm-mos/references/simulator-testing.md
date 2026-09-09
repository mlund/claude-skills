# Testing under mos-sim

Use this tier to test target-width computation and generated instructions.
Before running, confirm that the installed simulator implements the emitted CPU
instructions and the timing model needed by the experiment. Inspect its usage
and SDK `utils/sim/`; unsupported opcodes in some versions execute as NOPs.

A `sim` build is not the production platform: VIC, DMA contention, raster timing,
banking hardware, and KERNAL behavior are not represented. Simulated cycle counts
do not establish display frame rate or scrolling smoothness.

---

## 1. Build and run

```sh
mos-sim-clang -Os -o prog prog.c     # a complete target like any other
mos-sim --cycles prog                # cycle count to stderr, program output to stdout
```

`mos-sim` takes a flat memory image, not an ELF — `file` reports the link output
as `data`, and `llvm-nm` will not read it. When you need addresses out of a
simulator build, take them from a link map (§4 of this file, and [tooling.md](tooling.md)).

## 2. Find the interface, don't trust a copy of it

Run `mos-sim` with no arguments. It prints its full usage — every option and
every memory-mapped address, generated from the binary you actually have. The
implementation is `utils/sim/mos-sim.c` in llvm-mos-sdk if you need the
semantics behind an entry.

That usage text is the authority for what follows; the point of this section is
what the facility is *for*, not to restate the table:

- A **cycle counter** that is readable and resettable from inside the program.
- **stdin, stdout, exit and abort** as single-byte ports.

The consequence worth planning around is that a simulator run is an ordinary
command-line process: it reads stdin, writes stdout, and its exit status is
whatever `main` returned. A self-checking test can report failure through its exit status. Run it with a
bounded test-runner timeout: a code-generation regression may prevent return.

## 3. Measure a region, not the program

`--cycles` reports the whole run, which includes CRT startup and every library
call the program makes. That number is dominated by whatever formatting you
used to print the result. The `sim` platform's `<stdlib.h>` adds `clock()` and
`reset_clock()` for this reason: bracket the code under test and the count
excludes everything else.

```c
#include <stdlib.h>              /* sim platform: adds clock() / reset_clock() */

reset_clock();
for (uint8_t i = 0; i < 8; i++) sink = shift_var(i);
unsigned long cycles = clock();  /* cycles since the reset */
```

Keep the result observable so the optimizer cannot remove the work. Account for
timing instrumentation, and move reporting outside the measured region.
Use `noinline` only when an isolated call is the experiment; otherwise preserve
production inlining. Record CPU mode, tool revisions, flags, inputs, and repeated
measurements alongside any claimed cycle difference.

`clock()` and `reset_clock()` exist only on this platform, so a benchmark using
them is a `sim`-only translation unit. Keep it beside the unit under test, not
inside it.

## 4. Attributing cycles to functions

`--profile` writes one `<pc-hex> <cycles>` line per executed address to stderr.
Sorting that on the second column gives the hot addresses directly:

```sh
mos-sim --profile prog 2>profile.txt >/dev/null
sort -k2 -rn profile.txt | head
```

Addresses become names by joining against a link map produced by the same
build. Filter the stream to `^[0-9a-f]+ [0-9]+$` before parsing: at least one
line of a different shape appears in the output, and a parser that assumes
uniformity will either crash or silently absorb it as a bogus address.

`--trace` prints each instruction address as it executes, for when the question
is control flow rather than cost. `--cmos` switches the simulated core to
65C02; the default is NMOS 6502.

## 5. What this tier proves

A pass supports correctness for the tested inputs under the selected simulator
model. Cycle counts describe that model, not hardware bus stalls or peripherals.
A matching target data model exposes width-dependent bugs that host tests may
miss; it does not guarantee that every overflow bug is detected.

Use machine or platform-emulator tests for integration, interrupt timing, banking,
and hardware registers. Verify production code separately when its target flags,
libraries, or layout differ from the simulator build.
