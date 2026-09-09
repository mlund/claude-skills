# Inline assembly on llvm-mos

Contents:
1. Why this is dangerous
2. Constraints
3. Modifiers and operand substitution
4. Clobbers and the decision procedure
5. Worked patterns
6. Gotchas and crash modes
7. Choosing between inline asm, a real function, and an absolute-symbol declaration

---

## 1. Why this is dangerous

GCC-style inline assembly is designed for *small snippets embedded in a larger C computation*, not for writing routines. The compiler treats the asm string as an opaque blob that consumes declared inputs and produces declared outputs. It does not parse it. Everything it knows about your block, you told it.

Two default assumptions cause nearly all bugs:

- **Anything not declared clobbered is preserved.** GCC chose the faster assumption. A block that trashes A while the compiler holds a live value there produces wrong results with no diagnostic.
- **A block with no used outputs is dead.** Without `volatile`, the compiler may delete it or hoist it out of a loop, since as far as it knows the block "doesn't do anything that involves the loop".

Neither failure produces a warning. Both produce code that looks fine and behaves strangely.

```c
asm volatile("instructions" : outputs : inputs : clobbers);
```

`asm` and `__asm__` are equivalent. `__attribute__((leaf))` may precede the statement to promise the block doesn't call back into the current compilation unit — important for any `jsr` into ROM, because otherwise the compiler must prevent static stack allocation in callers.

---

## 2. Constraints

MOS-specific:

| Constraint | Registers | Notes |
|---|---|---|
| `a` | A | |
| `x` | X | |
| `y` | Y | |
| `d` | X or Y | Compiler picks; use when the opcode must be an index-register form |
| `R` | A, X, or Y | Wider choice, but see the `ina` trap in §6 |
| `c` | Carry flag | Safe as an *input*; broken as an output — see §6 |
| `v` | Overflow flag | |
| `r` | Imaginary register | `__rcN` for 8-bit operands, `__rsN` (ZP pair) for 16-bit |

Generic constraints (check support in the installed compiler):

| Constraint | Meaning |
|---|---|
| `m` | Memory operand |
| `i` | Immediate constant, including link-time symbols |
| `n` | Immediate with a known numeric value at compile time |
| `X` | Any operand whatsoever |
| `p` | A valid memory *address* (yields an address operand, e.g. `__rc2`) |
| `0`–`9` | Tied: must occupy the same location as operand N |

**Not supported:** `o`, `V`, `<`, `>`, `g`, `s`, and `asm goto`. Several of these crash the compiler rather than diagnosing (§6).

> **Naming collision worth internalizing:** `p` as a *constraint* means "an address operand". `"p"` in the *clobber list* means the processor status register. Same letter, unrelated meanings, different positions in the statement.

`"r"` is how you get a value into zero page when A/X/Y are all spoken for, or when you need indirect addressing:

```c
asm volatile("lda (%0),y" :: "r"(ptr) : "a");   // emits lda (__rc2),y
```

---

## 3. Modifiers and operand substitution

**Constraint modifiers**, in the first character (or after `=`/`+` for `&`):

| Modifier | Meaning |
|---|---|
| (none) | Input only |
| `=` | Output only; previous value discarded |
| `+` | Read-write: both input and output |
| `&` | Early-clobber: this output is written *before* all inputs are read |
| `%` | Commutative: the compiler may swap this operand with the next |

**Early-clobber matters more than it looks.** Without `&`, the compiler may assign an input and an output to the same register, assuming all inputs are consumed before any output is produced. If your block stores its result partway through and then reads another input, you need `=&`:

```c
// [hi] is written (sta) before pla reads A, so it must be early-clobber
: [hi] "=&r"(info.addr_hi), "=a"(info.addr_lo)
```

**Positional substitution `%0`, `%1`, …** expands to the register or location name — and because 6502 mnemonics encode the register, it works *inside the mnemonic*:

```c
asm volatile("st%0 $1234" :: "R"(v));    // sta / stx / sty
asm volatile("t%0a" :: "d"(c) : "a");    // txa / tya
```

**Symbolic operands `%[name]`** are the readable alternative and are strongly preferred once a block has more than two operands:

```c
asm volatile("ldy %[idx]" :: [idx] "r"(y_offset));   // ldy __rc2
```

**`%c0`** forces the bare constant form of an immediate operand (no `#`). For plain `"i"` operands on this target `%0` already yields a bare number, so `%c` is mainly needed for instructions with unusual immediate encodings — the HuC6280 `st0`/`st1`/`st2` I/O instructions are the SDK's example:

```c
#define PCE_VDC_INDEX_CONST(index) asm volatile("st0 #%c0\n" :: "i"(index))
```

**`#%[name]` with an `r` operand** emits the *zero-page address of the imaginary register*, not its contents. This is how you hand a KERNAL routine a ZP pointer:

```c
// KERNAL SAVE wants A = the ZP address holding the start pointer
uint16_t zp_ptr = (uint16_t)startaddr;
asm volatile("lda #%[zp]\n\t"
             "jsr __SAVE\n\t"
             : "=&a"(err), [zp] "+r"(zp_ptr)
             : "x"(end_lo), "y"(end_hi)
             : "p");
```

---

## 4. Clobbers and the decision procedure

Walk the assembly and ask, for each item:

**A, X, Y** — does any instruction write it? Include implicit writes: `jsr` to code you don't control, `pla`, `tax`, `inx`, `ldy`. A register already declared as an input or output operand is covered; anything else must be listed.

**C and V** — the compiler tracks these two flags across your block. Does anything write them? `clc`/`sec`, arithmetic, shifts, comparisons, `bit`, and any `jsr` you don't control. Declare `"c"`, `"v"`, or `"p"` (all flags). When in doubt on a `jsr`, use `"p"` — it's the most common clobber in the SDK for exactly this reason.

**N and Z** — never declare these. The compiler doesn't track them, precisely because nearly every instruction writes them.

**`"memory"`** — needed when the block touches memory the compiler can't see through your operands, or when you need a barrier so surrounding accesses aren't reordered across it. The common case is MMIO sequencing.

**Soft stack / imaginary registers beyond your operands** — not expressible. That's the signal to write a real function instead (§7).

### Empirical baseline

Across ~416 inline asm sites in llvm-mos-sdk: `y` 197, `a` 190, `c` 166, `v` 166, `x` 134, `p` 86, `memory` 4. Operand constraints: `=x` 78, `=a` 60, `a` 30, `+a` 24, `=y` 15, `x` 11, `+x` 9, `i` 6, `y` 5, `=c` 5.

Note the asymmetry in the carry numbers: `c` appears 166 times as a *clobber* and never once legitimately as an output. The five `=c` sites are all in `pce-cd/libpce/src/cd/bios.c` and are the broken ones described in §6 — don't copy them as precedent.

Typical shapes:

```c
: "p"                        // flags only — a ROM call that preserves registers
: "x", "y", "p"              // ROM call preserving A
: "a", "x", "y", "p"         // ROM call that trashes everything
: "a", "x", "y", "c", "v"    // same, spelling out the flags individually
```

### Volatile

Add `volatile` when the block's purpose isn't fully captured by its outputs — side effects on hardware, memory, or control state. A block with no outputs almost always needs it. A pure computation with outputs usually doesn't, and omitting it lets the compiler CSE and schedule it, which is a real win.

```c
for (;;) asm volatile("");      // keeps an otherwise-UB infinite loop alive
asm volatile("" ::: "memory");  // pure barrier, emits no instructions
```

---

## 5. Worked patterns

**Simple ROM call, value in and out:**

```c
asm volatile("jsr\t__CHROUT" : "+a"(c) : : "p");
```

**Carry-flag result, tested inside the block** — the correct way to return a flag, since `"=c"` doesn't work (§6):

```c
__attribute__((leaf)) __asm__ volatile(
    "    jsr __LOAD   \n"
    "    bcc 1f       \n"   // no error if carry clear
    "    tax          \n"   // else get error code from A
    "    ldy #0       \n"
    "1:               \n"
    : "=x"(result.lo), "=y"(result.hi)
    : "a"(flag), "x"(addr.lo), "y"(addr.hi)
    : "p");
```

Numeric local labels (`1:` / `1f` / `1b`) are required — a named label breaks if the block is emitted more than once through inlining or unrolling.

**Materializing a flag into a value:**

```c
asm volatile("jsr __TestPoint \n"
             "ldx #0 \n"
             "bcc 1f \n"
             "inx \n"
             "1:" : "=x"(is_set) : : "a", "y", "c", "v");
```

**Populating a struct — returning more than one value.** Output operands bind to *lvalues*, not just plain variables, so a struct field or union member works anywhere a variable does. This is the standard way to get several results out of one ROM call, since a C function can only return one thing:

```c
// cx16/cx16_k_joystick_get.c — three results, one call
JoyState cx16_k_joystick_get(const unsigned char joystick_num) {
  JoyState s;
  __attribute__((leaf)) asm volatile(
      "jsr __JOYSTICK_GET\n"
      : "=a"(s.data0), "=x"(s.data1), "=y"(s.detached)
      : "a"(joystick_num)
      : "p");
  return s;
}
```

This composes with the ABI rather than fighting it. `JoyState` is 3 bytes, and aggregates ≤ 4 bytes are returned in registers (`abi.md`), so the whole function compiles to almost nothing — A and X are already the first two return slots:

```asm
joy_get:
    jsr __JOYSTICK_GET
    sty __rc2            ; third return byte
    rts
```

**A union splits a wide value into byte-sized operands.** Registers are 8-bit, so a 16-bit value needs two operands; a union gives you both views without shifting. `cbm_k_load.c` uses it on the input *and* output side:

```c
typedef union {
  uint16_t value;
  struct { uint8_t lo, hi; };
} Word;

Word result;
const Word addr = {.value = (uint16_t)load_addr};
asm volatile("..." : "=x"(result.lo), "=y"(result.hi)
                   : "a"(flag), "x"(addr.lo), "y"(addr.hi) : "p");
return (void *)result.value;      // reassembled for free
```

Operand limits:

- **A whole aggregate larger than a register is not a valid operand.** `"=a"(s)` on a 6-byte struct gives `error: invalid output size for constraint '=a'`. Bind the individual fields.
- **Bitfields do work** as output operands — clang materializes through a temporary and masks (`and #15` for a 4-bit field). Correct, but you pay for the insert; prefer whole-byte fields in a hot path.
- **More results than registers** — fall back to `"=m"` per field, below.

**Capturing more results than there are registers** — write straight to memory with `"=m"`:

```c
asm volatile("sta %[a]\n" "stx %[x]\n" "sty %[y]\n"
             "tza\n" "sta %[z]\n" "ldz #0\n"
             : [a] "=m"(a_val), [x] "=m"(x_val),
               [y] "=m"(y_val), [z] "=m"(z_val)
             : : "a", "x", "y", "p");
```

**MMIO barrier:**

```c
MATH.multina32 = a;
MATH.multinb32 = b;
asm volatile("" ::: "memory");   // both writes land before the result is read
return MATH.result;
```

**Immediate data embedded after a call** (Neo6502-style API):

```c
#define KSendMessage(group, function) \
  asm volatile("jsr 0xFFF7\n.byte %0, %1\n" :: "i"(group), "i"(function) : "p")
```

**Delay loop letting the allocator pick the index register:**

```c
uint8_t counter = 0;
asm volatile("1: in%0\n"
             "   bne 1b" : "+d"(counter));   // inx/bne or iny/bne
```

**Module-level asm defining a real function** — no operands, so no clobber problem; it obeys the normal ABI:

```c
asm(".text\n"
    ".global foo\n"
    "foo:\n"
    "  sta $5678\n"
    "  rts\n");
void foo(char c);   // now callable as ordinary C
```

Placing code in a startup phase uses the same trick:

```c
asm(".section .init.250,\"ax\",@progbits\n"
    "  jsr __late_init\n");
```

---

## 6. Gotchas and crash modes

These failure modes depend on compiler revision. Check the installed compiler
with a small complete build; LTO may defer a constraint failure until linking.

**Carry output constraints can fail during code generation.** If `"=c"` or `"+c"` fails with `unable to translate instruction`, branch on carry inside the block and return the result through a supported register. With LTO, the failure may appear at link time.

Scope this claim carefully — it is routinely overstated:

| Form | Status |
|---|---|
| `"c"` as an input | Fine |
| `"c"` / `"p"` in the clobber list | Fine — and required whenever the block writes C |
| `"=c"` / `"+c"` as an output | Crashes the backend |

The breakage is in the backend, so it is **identical in C and in C++** — same source, same `LLVM ERROR`, via both `mos-*-clang` and `mos-*-clang++`. Statements of the form "C++ can't read the carry out of an asm block" are wrong twice over: it isn't language-specific, and the carry *is* readable — just not through an output constraint. **Return flags by branching inside the asm block** (`bcc`/`bcs` into a numeric local label) and materializing the result into a register you can declare, as `cbm_k_load.c:20` and `geos_crt.c:39` do. The same idiom is used pervasively in the SDK's `.s` files (`cx16/cx16_k_i2c_write_byte.s`, `cx16/videomode.s`, `cpm65/cpm.S`), typically `ldx #0 / bcc 1f / dex` to yield `0` or `-1`.

**`asm goto` crashes the backend** — `unable to translate instruction: callbr`.

**The `"g"` constraint crashes the backend** — `unable to translate instruction: call`. `"s"` is rejected cleanly (`invalid input constraint`).

**Constraints are case-sensitive and must be exact.** `R` and `r` are different. A miscased or nonexistent constraint can crash rather than diagnose (upstream issue #463). If you see `unable to translate instruction`, review the constraint list before anything else.

**`"d"` rejects literals.** `"d"(0)` gives `invalid input size for constraint 'd'`. Bind a `uint8_t` variable instead.

**`"R"` includes A, and not every opcode has an A form.** `in%0` under `"R"` may select A and emit `ina`, which is 45GS02/65C02-family only — it fails to assemble on a stock 6502 with `instruction requires a CPU feature not currently enabled`. Whether it breaks depends on what the allocator happened to pick, so it can pass for months and then fail. Use `"d"` whenever the mnemonic must be an X/Y form.

**The 45GS02 `Z` register has no constraint and no clobber.** All four constraint spellings `z`/`Z`/`q`/`Q` give `invalid input constraint`, and `Z` can't be named in the clobber list either — `::: "z"` gives `unknown register name 'z' in asm`. So there is *no way to tell the compiler you touched Z*; a hand-written `ldz #0` is the only mechanism. Move values through A with `taz`/`tza` inside the block. **You must restore `ldz #0` before returning**, and this is an ABI obligation for external `.s` functions and ISRs too, not just inline asm: the plain base-page indirect mode is encoded as `(zp),Z`, so every compiler-generated pointer dereference is silently Z-indexed and a stray Z corrupts memory access program-wide with no diagnostic. See `45gs02.md`.

**I/O access hazards**: indexed addressing can emit a spurious read one page *below* the target, so avoid pointer arithmetic landing one page above read-sensitive I/O; and the compiler avoids RMW instructions on volatile objects because they double-access.

---

## 6b. Controlling inlining of an asm wrapper

A static C wrapper retains the assembly constraints while allowing control over
inlining. Compare ordinary, forced-inline, and out-of-line builds before choosing
attributes. If measurements justify different choices by optimization mode:

```c
#if defined(__OPTIMIZE_SIZE__)     /* -Os and -Oz; not -O2 */
#define ASM_FN  static inline __attribute__((noinline))
#else
#define ASM_FN  static inline __attribute__((always_inline))
#endif
```

`noinline` keeps the wrapper out of line. Check the linked callers as well as the
wrapper: saved registers and duplicated instructions affect the total cost.

Constraints let the compiler place arguments in the registers the assembly needs.
An external assembly routine must translate from the C calling convention itself.

## 7. Choosing a call form

Choose a form that expresses the calling convention, then measure its cost.

- **C prototype for an absolute symbol:** suitable when the ROM routine follows
  the C ABI. See `commodore/cbm_k_chrout.c` and the platform's `kernal.S`.
- **Inline assembly:** useful for short sequences with precise constraints and
  clobbers, or results outside the C calling convention. See `cbm_k_load.c` for
  carry and `cx16/cx16_k_joystick_get.c` for register results.
- **External assembly function:** useful when the body would be expensive to
  duplicate or needs state that inline constraints cannot describe. See
  `cbm_k_setlfs.s` and `cx16_k_console_put_char.s` for ABI translation.

A prototype makes the caller allow for the ABI's full caller-saved register set.
Inline assembly can describe a smaller set, but may duplicate instructions.
Compare final call sites, register saves, and total size; there is no fixed
instruction-count threshold.

Use `leaf` only after checking that the routine and its callees cannot call back
into the compilation unit. See [abi.md](abi.md).
