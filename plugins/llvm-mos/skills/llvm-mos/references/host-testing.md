# Testing on the host

Much of a 6502 program is not hardware access at all: it is arithmetic over formats
something else defines — a disk layout, a register encoding, a text conversion, a
table. That part compiles and runs natively, where it can be exercised far faster and
more thoroughly than under an emulator, and where a failure points at a line rather
than at a hung machine.

This file covers what can move to the host, where the expected values should come
from, and what a passing host test does **not** prove on a 6502 target.

Contents:
1. What can run on the host
2. Where the expected values come from
3. The transcription trap
4. What a host test does not prove
5. Harness shape
6. Splitting a unit for testing
7. What still belongs on the machine

---

## 1. What can run on the host

The test is whether the code touches a register, a DMA controller, or a storage
device. If it does not, it can be split into its own translation unit and run
natively.

Typical candidates, all of them encodings of formats fixed outside your program:

| Kind | Examples |
|---|---|
| On-disk formats | FAT32 directory records, cluster chains, D64/D81/D65 geometry |
| System structures | freeze-slot region walks, process descriptors, save-state headers |
| Register encodings | RTC field packing, video coordinate arithmetic, bank-offset packing |
| Text | PETSCII ↔ ASCII conversion, screen-code folding, case tables |
| Tables | opcode and disassembler tables, name databases |

The split is usually cheap in code size, because LTO already sees through the
boundary — see the SKILL's note that a module split measured **−1 byte** once its
interface matched what the code was doing anyway. What costs is the interface you
invent to cross it, so measure rather than assume.

---

## 2. Where the expected values come from

This is what makes a host test worth writing. These formats are defined outside your
program, so an oracle exists independently of it.

A test whose expectations were copied out of the implementation only detects later
edits to that implementation. A test whose expectations were transcribed from the
format's own definition detects the implementation being wrong **in the first place**.

So: cite the source of every expected value in the test, and prefer, in order —

1. the hardware or firmware source that defines the format,
2. the published specification,
3. a capture from real hardware,
4. the implementation itself (weakest; label it as a regression pin, not a test).

For MEGA65 targets specifically, `mega65-dev/references/xemu-testing.md` lists which
`mega65-core` file answers which format question.

---

## 3. The transcription trap

Re-implementing the function under test *inside* the test — the same walk, the same
rounding, the same special cases — produces something that looks like an independent
oracle and is not. It catches a divergent edit between the two copies; it cannot catch
a shared misreading of the format, because both copies embody the same reading.

Where a second implementation is genuinely wanted, derive it from the *specification*
rather than from the code, and say in the test which of the two it is.

Structural properties are often stronger and cheaper than a reimplementation:

- items that must land in the same 512-byte sector, so they may be batched
- addresses outside every region, which must be reported absent rather than resolving
  to something plausible
- monotonicity and non-overlap across a region table
- round trips: `decode(encode(x)) == x` over a generated range

---

## 4. What a host test does not prove

The host and a 6502 target disagree on two fundamentals. Verified with
`mos-mega65-clang` and the system `cc` on macOS:

| | 6502 target | typical host |
|---|---|---|
| `char` | **unsigned** | **signed** (x86-64 and Apple silicon; unsigned on ARM Linux) |
| `int` | **16 bits** | **32 bits** |
| `long` | 32 bits | 64 bits on LP64 |

Assert rather than assume, in both builds:

```c
_Static_assert((char)-1 > 0, "char is signed here");
_Static_assert(sizeof(int) == 2, "int is not 16-bit here");
```

Consequences worth stating in the test file itself:

- **`char` comparisons diverge.** A `char` against a negative value, or a `>= 0x80`
  test, behaves differently on the two builds. High-bit-set bytes are routine in
  PETSCII and in packed fields, so this is not a corner case.
- **16-bit overflow silently succeeds on the host.** Products of two 16-bit
  quantities, and screen or sector offsets scaled by a row stride, are the usual
  cases. A host test proves nothing about them; use explicitly sized types
  (`uint32_t`) where the intermediate genuinely needs the width, and check the ones
  that must stay narrow on the target.
- **Structure layout and padding can differ.** Pin any structure that hardware or
  firmware defines with `static_assert(offsetof(T, f) == N)` so both builds hold it to
  the same shape.

---

## 5. Harness shape

A small C driver plus a script driving it over a pipe keeps the expectations in a
language suited to holding them:

```c
/* Host driver: include the unit directly, so its statics are reachable. */
#include "../src/<unit>.c"

int main(void) {
    char line[128];
    while (fgets(line, sizeof line, stdin)) {
        /* one command per line in, one result per line out */
    }
    return 0;
}
```

Properties that make this work:

- **Include the `.c`, not the header.** `static` functions and file-scope state are
  then reachable without weakening them in the shipping build.
- **One line in, one line out.** The driver holds no expectations; the script builds
  the command list and compares, so adding a case touches one file.
- **Compile with the host compiler at the same standard and warning level as the
  target build.** A warning that fires on only one of the two is itself a finding —
  and note that `-Wall` is not on by default anywhere in the llvm-mos toolchain.

---

## 6. Splitting a unit for testing

Two things bite when moving code out of a hardware-touching file:

- **The new header must not pull in hardware headers**, or the host build acquires
  them transitively and the split achieves nothing.
- **Section attributes are ELF-shaped.** `__attribute__((section(".rodata")))`
  compiles for a 6502 target and fails on a Mach-O host:

  ```
  error: argument to 'section' attribute is not valid for this target:
  mach-o section specifier requires a segment and section separated by a comma
  ```

  A file built both ways must guard it. **`__mos__` is the reliable discriminator** —
  every 6502 target defines it, alongside one macro per compatible CPU
  (`mos-mega65-clang` defines `__mos__`, `__mos6502__`, `__mos65c02__`,
  `__mos65ce02__`, `__mos4510__`, `__mos45gs02__`).

  ```c
  #ifdef __mos__
  #  define IN_RODATA __attribute__((section(".rodata")))
  #else
  #  define IN_RODATA
  #endif
  ```

---

## 7. What still belongs on the machine

Host tests do not replace emulator tests; they cover a different half.

| Property | Check it |
|---|---|
| Arithmetic over a defined format | host |
| Register writes reaching the right device | emulator |
| DMA and storage transfers, sector round trips | emulator |
| Anything within 16 bits of overflow | emulator |
| Anything depending on `char` signedness | emulator |
| Code size and register allocation | target build, measured |
| Timing, and what persists in a card or cartridge image | emulator, or hardware |

A useful split in practice: the host suite runs on every edit and covers the formats
exhaustively; the emulator suite runs less often and covers the hardware path once per
feature.
