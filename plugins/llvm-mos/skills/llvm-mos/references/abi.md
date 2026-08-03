# The llvm-mos C calling convention

You need this when writing assembly that C calls (or that calls C), writing interrupt prologues by hand, or reasoning about why the compiler placed something where it did.

The design borrows from RISC-V: a hybrid of caller- and callee-saved registers, tuned by LLVM's shrink-wrapping and caller-save placement passes.

---

## Register classes

**Real registers:** A, X, Y, the flags C/N/V/Z, PC, S (hardware stack pointer), D (direct page), I (interrupt disable).

**Imaginary registers:** zero-page bytes named `__rc0`–`__rc31`, paired little-endian into 16-bit `__rs0`–`__rs15` (`__rs0` = `__rc0`/`__rc1`, and so on). Their addresses are assigned by the linker script, not fixed by the ABI — assembly must reference the symbols, never literal addresses.

### Caller-saved (a function may freely destroy these)

- A, X, Y
- C, N, V, Z
- `__rs1`–`__rs9`, i.e. `__rc2`–`__rc19`

### Callee-saved (must be restored before returning)

- PC, S, D, I
- `__rs0` (`__rc0`/`__rc1`) — the soft stack pointer
- `__rs10`–`__rs15` (`__rc20`–`__rc31`) — `__rs15` doubles as the soft frame pointer

### Target-specific: Z must be zero (45GS02 / MEGA65)

On `-mcpu=mos45gs02`, **Z is required to be 0 on every transfer of control to compiled code** — returning from inline asm, from external `.s` functions, and from interrupt handlers, and also *calling* into a C function from your own assembly. This isn't a convention you can opt out of: the plain base-page indirect addressing mode is encoded as `(zp),Z`, so `sta ($12)` and `sta ($12),z` are the same opcode, and every compiler-generated pointer dereference is silently Z-indexed. A non-zero Z offsets them all, with no diagnostic and no crash at the site of the bug. Treat Z as callee-saved with a fixed value of 0. Details and worked examples in `45gs02.md`.

---

## Argument passing

Arguments are assigned left to right. The return value is assigned exactly as if it were the first argument.

**Numeric values** go one byte at a time: first A, then X, then `__rc2` through `__rc15`. A 32-bit int occupies four consecutive slots in that sequence.

**Pointers** go in the 16-bit pairs `__rs1`–`__rs7` — up to seven pointers in registers.

**Overflow** goes on the soft stack (managed through `__rs0`).

### Aggregates

- **≤ 4 bytes**: split into constituent values and passed in registers by the rules above. Returned the same way.
- **> 4 bytes**: passed *by pointer*. The caller allocates the storage and passes its address. The callee may write through it freely, so the caller must assume the contents are clobbered.
- **Returning > 4 bytes**: the caller passes a pointer as an implicit first argument, and the function returns `void`.

### Variadic arguments

Everything inside the ellipsis is passed on the soft stack; named parameters before it follow the normal rules. **This makes prototypes load-bearing** — calling a variadic function without a visible prototype produces the wrong convention and fails at runtime.

### Worked examples

| Signature | A | X | rc2 | rc3 | rc4 | rc5 | rc6 | rc7 | Returns in |
|---|---|---|---|---|---|---|---|---|---|
| `char f(int a)` | a.lo | a.hi | | | | | | | A |
| `long f(long a, int b)` | a0 | a1 | a2 | a3 | b0 | b1 | | | A, X, rc2-3 |
| `void f(int64_t a)` | a0 | a1 | a2 | a3 | a4 | a5 | a6 | a7 | — |
| `int *f(void *a)` | | | a.lo | a.hi | | | | | rc2-3 |
| `int f(int a, int b, void *c)` | a.lo | a.hi | b.lo | b.hi | c.lo | c.hi | | | A, X |
| `int f(void *a, char b, int c)` | b | c.lo | a.lo | a.hi | c.hi | | | | A, X |
| `void f(struct div_t a)` | a0 | a1 | a2 | a3 | | | | | — |
| `void f(struct ldiv_t a)` | | | ptr.lo | ptr.hi | | | | | — |
| `div_t f(void *a)` | | | a.lo | a.hi | | | | | A, X, rc2-3 |
| `ldiv_t f(void *a)` | | | ret.lo | ret.hi | a.lo | a.hi | | | via implicit 1st arg |

Note rows 5 and 6: pointers claim `__rs`-aligned pairs while scalars fill A/X first, so the *order* of assignment is left-to-right but the *slots* used depend on the type. Don't assume a positional mapping.

---

## Stacks

There are two, and they serve different purposes.

**The soft stack** is the primary one for locals and spilled values: zero-page-managed, pointer in `__rs0`, growing down from the linker symbol `__stack`. It's only used when necessary.

**The hardware stack** (page 1, 256 bytes) holds return addresses and is used for a few leaf-call cases. The compiler may use up to 4 bytes of it for saving temporaries. It's far too small to be the general-purpose stack, which is the whole reason the soft stack exists.

**Static stack allocation** is the important optimization: whole-program call-graph analysis proves which functions can never have two invocations active at once, and allocates their frames at fixed absolute addresses instead of on the soft stack. This is a large part of llvm-mos's performance advantage.

Two things defeat it, and both have fixes:
- **Function pointers** — the analysis can't see through them. Use `-fnonreentrant` or `__attribute__((nonreentrant))`.
- **Opaque calls into assembly** — the compiler must assume they might re-enter C. Use `__attribute__((leaf))` on assembly-implemented declarations.

**The frame pointer** (`__rs15`) is not emitted by default. It's needed for stack unwinding, source-level debugging of frames, and C99 variable-length arrays.

Force it on with **`-fno-omit-frame-pointer`** — note the flag is *omit*, the standard clang spelling. The upstream llvm-mos wiki documents this as `-f[no-]emit-frame-pointer`, which is stale: that spelling is rejected outright (`unknown argument '-fno-emit-frame-pointer'; did you mean '-fno-omit-frame-pointer'?`). The stale name is also inverted in sense, so copying it from the wiki fails loudly rather than silently — but do not propagate it.

---

## Writing a manual interrupt prologue

With `__attribute__((interrupt))` the compiler generates the save/restore for you. If you use `no_isr` to write it yourself, you must preserve everything the compiler might have live. Callee-saved registers are excluded below — the `jsr body` is expected to preserve those itself, as any C-callable function does.

This is the maximal sequence; elide entries only if you can prove the entire transitively-called handler never touches them (realistically, only when the handler is pure assembly).

```asm
  cld                    ; decimal flag is undefined on entry
  pha
  txa
  pha
  tya
  pha
  lda mos8(__rc2)        ; save caller-saved imaginary registers rc2..rc19
  pha
  ; ... repeat for __rc3 through __rc18 ...
  lda mos8(__rc19)
  pha

  jsr body

  pla
  sta mos8(__rc19)       ; restore in reverse order
  ; ... repeat down through __rc3 ...
  pla
  sta mos8(__rc2)
  pla
  tay
  pla
  tax
  pla
  rti
```

That's 18 imaginary-register bytes (`__rc2`–`__rc19`, i.e. the nine caller-saved pairs `__rs1`–`__rs9`) plus A/X/Y — 21 pushes. It's expensive, which is the argument for `interrupt_norecurse` and for keeping handlers small and self-contained.

`mos8(...)` forces the 1-byte zero-page encoding. It's needed because the assembler can't know an extern symbol's address at assembly time and would otherwise emit the 16-bit form (see `cc65-migration.md` on zero-page addressing).

For comparison, what the compiler actually generates under `__attribute__((interrupt))` is far cheaper than this worst case — it saves only the registers the handler provably touches, so a small handler may push just A/X/Y and one or two imaginary registers.

---

## Rules that are undefined behavior to break

- Anything asynchronous calling a C function that lacks `interrupt` or `interrupt_norecurse`.
- A second invocation of an `interrupt_norecurse` function while the first is still active.

Both corrupt statically-allocated frames, and the symptom is usually distant from the cause.
