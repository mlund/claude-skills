# Testing under mos-sim

`references/host-testing.md` covers running logic natively, and closes by
listing what a host pass cannot prove: anything that depends on this target's
code generation. `mos-sim` is the tier that closes that gap. It executes the
6502 the compiler actually emitted, counts cycles, and needs no hardware and no
emulator — so it answers "is this correct *and* fast enough on a 6502" in the
same run, from a plain `main()`.

It does not replace on-machine testing. The simulator has no VIC, no raster, no
banking hardware and no KERNAL; a program built for it is built for the `sim`
platform, not for yours. Use it for the compute, not the machine.

---

## 1. Build and run

```sh
mos-sim-clang -Os -o prog prog.c     # a complete target like any other
mos-sim --cycles prog                # cycle count to stderr, program output to stdout
```

`mos-sim` takes a flat memory image, not an ELF — `file` reports the link output
as `data`, and `llvm-nm` will not read it. When you need addresses out of a
simulator build, take them from a link map (§4 of this file, and **Tooling** in
`SKILL.md`).

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
whatever `main` returned. A test that returns non-zero on failure needs no
harness, no log scraping and no timeout — `mos-sim prog` **is** the test.
Verified: a program whose `main` returns 3 exits 3; `echo -n A | mos-sim prog`
reaches `getchar()` as 65.

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

Measured on one such pair — a variable shift `1u << row` against an eight-entry
lookup table, same loop, same iteration count — **820 cycles versus 309**. The
same run's `--cycles` total was 24358, essentially all of it `printf`. Quoting
the whole-program figure as the cost of the routine is the easy mistake here,
and it is wrong by two orders of magnitude.

Both functions are `noinline` in that measurement. Without it the loop bodies
fold into the caller and you are timing something you did not write.

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

It proves the compiled code computes the right answer, and what it costs in
cycles. It does not prove the program works on your machine: platform
libraries, interrupt timing, banking, and every hardware register are absent or
different. Treat a `mos-sim` pass the way you would treat a passing unit test
of a driver's arithmetic — necessary, not sufficient.

The `char`/`int` caveats from `host-testing.md` do *not* apply here. This is the
real target's type model, so an overflow that a host test hid will reproduce.
That makes the simulator the cheapest place to re-run anything a host test
flagged as needing on-machine confirmation for type reasons.
