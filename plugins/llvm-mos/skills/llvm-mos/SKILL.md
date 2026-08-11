---
name: llvm-mos
description: Write, debug, and optimize C, C++, and assembly for 6502-family CPUs using the llvm-mos toolchain and llvm-mos-sdk (mos-*-clang, ld.lld linker scripts, imaginary registers). Use this skill whenever the user is working on 6502/65C02/65816/45GS02/HuC6280 code, mentions llvm-mos, mos-clang, or an 8-bit retro target (C64, C128, VIC-20, PET, NES, Atari 2600/8-bit/5200, MEGA65, Commander X16, Lynx, PC Engine, Apple II, Neo6502, CP/M-65), writes or debugs inline assembly for 6502, hits a compiler crash or mysterious miscompile around an asm block, ports or converts cc65/ca65 code, or needs a custom linker script, memory map, bank layout, or zero-page allocation. Trigger it even when the user doesn't name llvm-mos explicitly — if the target is a 6502 and a C compiler is involved, this skill applies.
---

# llvm-mos

llvm-mos is a real optimizing LLVM backend pointed at a CPU with three 8-bit registers. Almost everything that surprises people follows from that one sentence, so start with the mental model rather than the syntax.

## The mental model

LLVM assumes it owns the machine. On a 6502 that means it owns:

- **A, X, Y and the C/V flags.** These are caller-saved scratch. The compiler tracks their contents across your code and will happily assume a value survives something it can't see into.
- **The imaginary registers** — `__rc0`–`__rc31` (8-bit) aliased as `__rs0`–`__rs15` (16-bit pairs), living in zero page at addresses the *linker script* chooses. These are the register file. `__rs0` is the soft stack pointer; `__rs15` is the soft frame pointer.
- **Additional zero page**, allocated whole-program under LTO and sized by `-mlto-zp=<n>`.

The compiler also does whole-program call-graph analysis to prove which functions can't be simultaneously active, and statically allocates those stack frames instead of using the slow soft stack. This is a large part of why llvm-mos beats older 6502 compilers — and it's why lying to the compiler about what your assembly does degrades code quality far away from the assembly itself.

So the recurring theme: **tell the truth about what your code touches, and the compiler rewards you. Stay silent, and it miscompiles or pessimizes.**

## Toolchain basics

Targets are hierarchical (`common` → `commodore` → `c64`). Each complete target gets a driver and a config file:

```sh
mos-c64-clang    -Os -o game.prg game.c    # a complete target: produces a runnable binary
mos-common-clang -Os -o out main.c         # incomplete parent: needs your own link.ld
mos-clang -c my-asm-file.s                 # the assembler, via the same driver
```

`-Os` and `-flto` are on by default via the `.cfg` files. Keep them. LLVM-MOS generates markedly better code optimizing for size than speed, and LTO is what enables zero-page allocation and the static stack analysis.

LTO also **merges identical `static` globals across translation units**, which is worth knowing before you contort a design to avoid duplication: a generated table header `#include`d by two `.c` files yields one copy in the binary, confirmed by link map.

The boundary itself is close to free for code too — splitting a module out measured **−1 byte** once its interface matched what the code was already doing. What costs is the *interface you invent to cross it*: a first attempt at the same split came in **+376** because the extracted function took a pointer out-param and restarted its work on each call, where the single-file loop had kept the state in registers. LTO will inline across the boundary; it cannot undo an interface that is algorithmically worse. So when a split measures expensive, look at the signature before concluding the boundary is to blame.

A related trap when attributing size changes: a semantically-null narrowing can move codegen far from where you wrote it. Declaring a constant `unsigned char` with a value ≥ 0x80 and storing it into a `char` array measured **+17 bytes** against the same value written as a plain literal — identical semantics, since both promote to `int` for the store. The diff was not an extra store but different register allocation inside a large inlined function: a `phy`/`ply` pair appeared and one `inw` split into two `inc`s. So before attributing a small delta to the line you changed, check *where* the bytes went (`llvm-nm --print-size --size-sort` on the ELF, or the `asm-printer` optimization remarks); at this scale ±20 bytes is often the allocator, not your edit.

**Gotcha worth knowing up front:** because LTO is the default, `-S` emits LLVM IR, not assembly. There are three ways to read the generated 6502, and they are not interchangeable:

```sh
mos-c64-clang -Os -fno-lto -S -o - foo.c              # a DIFFERENT build: no LTO
mos-c64-clang -Os -Wl,--lto-emit-asm -o foo.prg foo.c # the real LTO output -> foo.prg.lto.s
llvm-objdump -d --print-imm-hex foo.elf               # only if you actually have an ELF
```

`-fno-lto -S` is the convenient one, but it compiles a different pipeline. It cannot show anything LTO does — zero-page allocation, static stack placement, cross-module inlining — so a bug that only appears in the real build will not be there, and its absence proves nothing. **`-Wl,--lto-emit-asm` is what shows the code that actually ships**; the linker writes `<output>.lto.s` next to the output. Use it whenever you are comparing optimization levels, chasing a miscompile, or checking which instructions the backend chose.

The third line has a trap: **for a complete target the link output is usually a flat binary** (PRG, XEX, iNES — whatever `OUTPUT_FORMAT` produces), not an ELF, whatever you name it. `llvm-objdump -d` then fails with *"file was not recognized as a valid object file"*. Piping that into `grep -c` silently reports zero matches, which reads exactly like "the instruction isn't there" — an easy way to talk yourself out of a real finding. Check the tool's exit status, or use `--lto-emit-asm` and read the assembly directly.

Select the CPU with `-mcpu=` (`mos6502`, `mos6502x`, `mos65c02`, `mosr65c02`, `mosw65c02`, `mos65ce02`, `mos4510`, `mos45gs02`, `mos65el02`, `mos65dtv02`, `mosw65816`, `moshuc6280`, `mosspc700`, `mossweet16`). Each defines `__mos__` plus a macro per compatible CPU.

## Writing C that compiles well

These rules come from the project's own optimization guide; the reasoning matters more than the list.

- **Don't hand-optimize into globals.** A local can live in A, move to X for indexing, and never touch memory. A global is an address the compiler must often store to, because something else might observe it.
- **Use `-fnonreentrant` (or `__attribute__((nonreentrant))`) when you use function pointers.** Indirect calls defeat the call-graph analysis, so the compiler conservatively falls back to the soft stack for everything reachable. This flag is frequently the single biggest speed/size win in a program with a jump table or callback.
- **Mark assembly-implemented functions `__attribute__((leaf))`.** Same reason: an opaque `jsr` might call anything, including back into C, which forces soft-stack allocation up the call graph. `leaf` promises it doesn't re-enter C. The SDK uses this on essentially every KERNAL/BIOS wrapper.
- **Make function-local constant arrays `static`.** Otherwise the C standard requires a fresh copy per invocation, and the compiler emits the copy.
- **Prefer structs of arrays.** Absolute-indexed addressing needs a constant base plus an 8-bit index; an array of structs needs a multiply by the stride. That is worse than "a multiply" sounds — a non-power-of-two stride emits a *call*, and drags the routine into the link:

  ```asm
  pick:                  ; TABLE[i].field, where sizeof(struct) == 11
      ldx #11
      stx __rc2
      ldx #0
      jsr __mulhi3       ; on every index, plus ~50 bytes of __mulhi3 linked in
  ```

  Padding the struct to 8 or 16 bytes turns that into `asl`/`rol` pairs, which is the escape hatch if you must keep the struct — at the price of the padding. `#include <soa.h>` provides `soa::Array<T, N>` in C++ which does the byte-striping for you while looking like a normal array; LTO mixes C and C++ freely, so reaching for it does not mean rewriting the project.

  All of that is about indexing *per access*. When the index is used **once** — take `&TABLE[i]` into a pointer, then walk the members sequentially — the multiply happens once and the advice inverts. Measured on a 16-entry, 3-byte-per-entry table read at startup: padding each entry to 4 (stride 48 → 64, so the index became a shift) cost **+28 to +32 bytes on every one of seven targets** and saved nothing, because the padding is pure data and the single multiply was already cheap. Check which case you are in before padding.
- **Keep array indices under 256**, and don't compute in wide types unless you consume the wide result.
- **`const` does not keep a table out of zero page, and zero page is not free.** The LTO allocator may put a `static const`/`constexpr` table in `.zp.data`, which costs twice: the data needs a startup copy (`__copy_zp_data`), and every byte it occupies is a byte the allocator cannot give to imaginary registers. That second cost is the large one and it lands in `.text`, far from the table. Measured on a 96-byte startup-only table:

  | | `.zp.data` | `.zp` (imaginary regs) | `.rodata` | `.text` | binary |
  |---|---|---|---|---|---|
  | as written | 117 | 37 | 767 | 17762 | 20363 |
  | `__attribute__((section(".rodata")))` | 21 | 133 | 863 | 17473 | **20074** |

  The table's own 96 bytes merely moved section; the **−289** is code that got smaller once the allocator had 96 more zero-page bytes. Pin startup-only tables to `.rodata` and measure. Spot it with `llvm-nm`: symbol type `d` is writable data (including `.zp.data`), `r` is read-only; `llvm-readelf --section-headers` gives the section sizes. Note `.zp` saturates whatever `-mlto-zp` and the linker script's `__basic_zp_end` allow, so its *size* alone tells you nothing — only the byte count does.

  **Guard the attribute if the file also builds for the host.** Bare section names are an ELF assumption: Mach-O requires `"segment,section"`, so a shared `.c` with unit tests on macOS stops compiling the moment you pin a table (`error: argument to 'section' attribute is not valid for this target: mach-o section specifier requires a segment and section separated by a comma`). Keep the pin target-only:

  ```c
  #if defined(__mos__)
  #define RODATA __attribute__((section(".rodata")))
  #else
  #define RODATA
  #endif
  ```

  `__mos__` is defined by every llvm-mos `-mcpu`, so this is the reliable discriminator. The host build is exactly where you notice — a target-only build passes and the breakage surfaces in the test suite.
- **C23 `constexpr` on aggregates works, and costs exactly what `static const` costs.** clang 23 accepts `constexpr struct T ARR[N] = {…}` with designated initialisers, and taking `&ARR[i]` at runtime is fine. Measured byte-for-byte identical to `static const` across seven targets, so choose on what it says, not on what it emits — and note it does *not* imply `.rodata` placement (see above).
- **Don't force `noinline` on small C helpers.** At `-Os`/`-Oz` the inliner already picks correctly for them, and overriding it measured worse in nine cases out of nine — from +1 byte on a 256-iteration search to +236 on a parser, and +293 for four helpers at once. Getting a pointer argument into imaginary registers and returning through them costs more than a body of a handful of instructions. Note this is the *opposite* of the inline-asm case below, where `noinline` wins: an asm wrapper's body is opaque and its clobbers are already stated, so duplicating it buys nothing.
- **Avoid variable-count loops over small fixed sizes.** A `read(bytes, count)` that shifts and ors `count` times costs far more than straight-line code for the widths you actually use. Replacing one with a fixed 16-bit read plus a single branch for the rare wider case measured **−272 bytes** in one function.
- **Fixed-width string tables need character lists.** clang 23 makes a NUL-less string initialiser an error, so the obvious way to drop the terminators no longer compiles:

  ```c
  static const char NAMES[3][3] = { "ADC", "AND" };            // error:
                                     // -Wunterminated-string-initialization
  static const char NAMES[3][3] = { {'A','D','C'}, ... };      // fine
  static const char NAMES[] = "ADC" "AND" "ASL";               // fine, index by stride
  ```
- **Don't carry a type wider than the value needs — it costs bytes, not just style.** `int` is 16 bits here and `long` is 32, so an over-wide variable turns every use into wider arithmetic. Measured on one program: a screen-position global that only ever held 16 bits, declared `long`, cost **78 bytes**; a loop counter borrowed for a byte-wide hardware index cost **13**; four addresses cast to `long` for a function taking `unsigned int` cost **22**. Each was found by `-Wconversion` and each got *smaller* when the type was corrected rather than cast. On a 16-bit-`int` target `-Wconversion` is partly a size tool, which is not how it reads on a 32-bit host.
- **When the value genuinely needs more than 16 bits, the natural 32-bit type still beats an exact-width one.** A wider-than-a-bank address (a 28-bit MEGA65 address bus, say) has no 16-bit home, so the question shifts from "how narrow" to "which wide representation." C23's `unsigned _BitInt(28)` looks like the honest answer, stating the real width in the type — and it compiles, as of clang 23 (clang 22 accepts it but fails at LTO link time, "unable to legalize G_MERGE_VALUES"). Measured against a plain `typedef long Addr28`, though, the exact-width type cost **582 bytes**: every call boundary needs a conversion, because nothing else in the program or its libraries is 28 bits wide. Matching a library's own signed/unsigned choice isn't automatically cheaper either — `uint32_t`, to match mega65-libc's own `lcopy`/`lpeek` signatures, cost **694 bytes** for a sign bit these addresses never reach. The plain signed `long` alias won because it is what integer promotion and the library's call sites were already producing, so nothing at the boundary needs converting; the typedef name is what documents the intended width once the type itself no longer can.

  Enable its narrowing half and leave the rest: `-Wconversion -Wno-sign-conversion`. `-Wsign-conversion` fires on ordinary hardware-register code, because C promotes every `uint8_t` operand to signed `int` before any operator — measured at 226 findings against 148 for the narrowing half in the same program.
- **Narrow the parameters, not just the variables.** A and X carry the first two argument bytes free; every byte after that costs 4 bytes of code at *every* call site, because zero page has no move and no store-immediate. A pointer parameter is 8 bytes per call, a `long` is 8. So a wrapper taking a narrow offset, over a base the wrapper itself supplies, can pay for itself many times: measured **−406 bytes** across 52 call sites of a 28-bit-address accessor, against 26 bytes of wrapper. **It only works while the wrapper stays out of line**, and that is not automatic — when the call sites pass constants, the constant folds through the wrapper and inlining reconstructs the original code exactly, giving a byte-identical binary with no sign anything happened. `noinline` is required in that case, and a measured no-op when the argument is a runtime value. Confirm with `llvm-nm` that the symbol survived. Cost table in `references/abi.md`.
- **Don't let a constant base become part of runtime arithmetic.** `*(volatile uint8_t *)(BASE + i) = v`, with `BASE` a `constexpr` integer, is one runtime expression: the constant disappears into it, so every store builds a pointer in an imaginary register pair and dereferences indirectly. Keep the base a *pointer* and the selector folds it into an absolute address instead:

  ```c
  #define SCR ((volatile uint8_t *)0xB800)
  SCR[row * 80 + col] = v;      /* sta $xxxx,x — 3 bytes, no pointer pair */
  POKE(0xB800 + row * 80 + col, v);   /* builds __rc2/3, then sta ($02),z */
  ```

  Same semantics; measured **−106 bytes** over 25 stores in one function, plus the register pairs freed. Worth knowing that the SDK's `POKE`/`PEEK` macros are the integer form, so they lose this whenever the base is constant and the index is not.
- **`char` is unsigned on llvm-mos.** Verify rather than assume — `_Static_assert((char)-1 < 0, "signed")` fails here — because it decides whether `-Wchar-subscripts` is a real hazard or noise. A `char` subscript is 0–255 and cannot go negative, so those warnings are inapplicable rather than latent bugs.
- **Don't assume `-Wall` is on.** Nothing in the llvm-mos toolchain or the usual CMake setup enables it. Switching it on for the first time in a mature codebase is cheap and finds real things: in one case a function that unconditionally called itself (8 call sites, shipped, and invisible to clang-tidy because `misc-no-recursion` had been excluded), plus dead code and a conditionally-uninitialised read.
- **`printf` is the most expensive thing most programs link, and its float conversions silently do nothing.** A `printf("%u\n", v)` measured **4535 bytes** against **509** for a `putchar` loop that formats the same integer — 4026 bytes for one call. Worse, the default `printf` is built without float support, so `printf("%f\n", d)` prints the literal text `%f`: no compile error, no link error, no warning, just a format string where a number should be. Link `-lprintf_flt` to get `3.140000` instead, at **+5400 bytes** (4606 → 10006 measured on the same program). That cost is why it is opt-in, and it is the reason to reach for scaled integers and a hand-rolled formatter — a precomputed integer constant in place of a `log2()` call keeps both the float library and the formatter out of the image.
- **The heap has a limit you probably have to set, and it only ever grows.** `malloc` starts bounded by `__heap_default_limit`, which is per-platform and can be far smaller than the RAM you were counting on. `<stdlib.h>` exposes `__heap_limit()`, `__set_heap_limit()`, `__heap_bytes_used()` and `__heap_bytes_free()` to manage it, with three rules from the header worth internalising: setting the limit **implicitly allocates the heap**, so don't call it in a program that has no other reason to have one; after the first allocation the limit may only increase, and requests to shrink are *ignored* rather than reported; and **nothing validates the heap against the stack**. Raising the limit is a promise you made about your own stack depth, and the collision when you get it wrong is silent corruption, not an allocation failure.
- **Infinite loops need a side effect.** `while (1);` is undefined behavior and gets deleted. Write `for (;;) asm volatile("");` or spin on a `volatile` object. A *condition* is not a side effect: `while (1 || msg) {}`, a common way to silence an unused-parameter warning while halting, is the same undefined loop dressed up — a deliberate halt written that way may not halt.

For hardware registers, `volatile` is the contract that an access happens exactly where you wrote it. Note two 6502-specific subtleties: indexed addressing can emit a spurious read one page *below* the target, so avoid pointer arithmetic that lands one page above read-sensitive I/O; and the compiler deliberately avoids RMW instructions (`INC`) on volatile objects because those double-access.

## Inline assembly — the danger zone

This is where most llvm-mos bugs live. **Read `references/inline-asm.md` before writing anything non-trivial**; it has the full constraint list, the clobber decision procedure, and worked examples. The essentials:

The compiler assumes an `asm` block preserves everything you didn't declare. If your block touches A and you don't say so, the compiler may keep a live value in A across it and silently get the wrong answer.

```c
// Broken: clobbers A, doesn't say so. Compiler may cache a value in A across it.
char foo(char v) { asm volatile("jsr $ffd2"); return v; }

// Correct.
char foo(char v) { asm volatile("jsr $ffd2" ::: "a", "p"); return v; }
```

**Declare every register and flag your code touches**, with one exception: N and Z are never tracked, so never list them. C and V *are* tracked — declare them as `"c"`, `"v"`, or `"p"` (whole status register). Any `jsr` to code you don't control clobbers the flags, so `"p"` belongs on essentially every KERNAL call.

**Use `volatile` whenever the block matters for a reason other than its declared outputs.** Without outputs, a non-volatile `asm` is dead code the compiler may delete or hoist out of a loop.

Constraints: `"a"`, `"x"`, `"y"` (specific register), `"R"` (any of A/X/Y), `"d"` (X or Y), `"c"`, `"v"` (flags), `"r"` (an imaginary register), `"i"` (immediate). Prefix `=` for output, `+` for read-write. Because 6502 mnemonics encode the register, you can substitute the operand into the mnemonic itself — `"st%0 $1234"` becomes `sta`/`stx`/`sty` depending on what the allocator picked.

**Several things crash the compiler outright rather than producing a diagnostic** (verified against clang 22): `asm goto`, the `"g"` constraint, a mistyped or miscased constraint, and — most importantly — **`"=c"` as an output**. Under the default LTO these crashes surface at *link* time as `LLVM ERROR: unable to translate instruction`, which makes them look like linker problems. Suspect the constraint list first.

The carry case is worth stating precisely, because it is usually mis-stated. **You can read the carry back out of an asm block; you just cannot do it with an output constraint.** `"c"` as an *input* is fine, and `"c"`/`"p"` in the clobber list is fine — only `"=c"` (and `"+c"`) is broken, and it is broken identically in C and in C++, so this is not a C++ limitation. Branch on the flag inside the block with `bcc`/`bcs` and materialize the answer into a register you can declare, as the SDK's own `cbm_k_load.c` and `geos_crt.c` do.

**Don't reach for a real function just because there's a lot of assembly — the deciding factor is body size and expressibility, not "how much asm".** A C prototype can only promise the ABI's clobber set (A, X, Y, `__rc2`–`__rc19`); inline asm states exactly what the block touches, so for a short body the allocator gets strictly better information. Measured on a CHROUT loop, inline asm beat an `extern` prototype 83 B to 87 B, and the gap *widened* to 188 B vs 236 B across 12 call sites — the prototype's call boundary forces loop variables into callee-saved registers that then spill to the hardware stack. Duplicating a 3-byte `jsr` is cheap by comparison. The crossover is body size: at ~20 instructions × 12 sites, a real function won 347 B to 592 B. So keep inline asm for short bodies with statable clobbers; switch to a `.s` file or module-level `asm()` when the body is large, or when you're describing more state than you're computing (the soft stack and imaginary registers beyond your operands have no constraint).

**These are not exclusive: put the inline asm in a C function and decide the inlining yourself.** That keeps the precise clobbers and lets constraints place operands where the routine wants them, while `noinline` keeps a single out-of-line copy so a short body is not duplicated per call site. Gate it on the optimisation mode — clang defines `__OPTIMIZE_SIZE__` for `-Os` and `-Oz`, not for `-O2`:

```c
#if defined(__OPTIMIZE_SIZE__)
#define ASM_FN  static inline __attribute__((noinline))
#else
#define ASM_FN  static inline __attribute__((always_inline))
#endif
```

Do not assume LTO gets this right on its own: measured on a short ROM-call wrapper with three call sites, explicit `noinline` beat both forced inlining and leaving the decision to the LTO inliner. The win from constraints is in the body — when the routine wants its arguments somewhere other than where the ABI delivered them, constraints let the compiler put them there, collapsing the `phx/tay/pla/tax` shuffle a hand-written version needs. Where the ABI and the routine genuinely disagree, the shuffle survives, correctly.

There is also a **third technique the SDK actually prefers**: declare the ROM routine as an ordinary C prototype at its absolute address and let the compiler emit the `jsr` — no inline asm at all. Each platform's `kernal.S` exports `__CHROUT` etc. as weak absolute symbols via a `weakdef` macro, and 20 of the 21 `commodore/cbm_k_*.c` wrappers are just `extern void __CHROUT(unsigned char) __attribute__((leaf));` plus a one-line call. Reach for inline asm when a value lands where the ABI has no name for it — `cbm_k_load.c` needs the carry, `cx16_k_joystick_get.c` returns three values at once in A/X/Y — and for a `.s` file when the ROM's convention needs real translation. `references/inline-asm.md` §7 has the full comparison.

## Assembly files

The assembler is GNU-syntax with 6502 conveniences: `$` works as a hex prefix alongside `0x`, and full GNU macro/`.if`/include machinery is available. Key differences from ca65 are in `references/cc65-migration.md`. The two that bite immediately:

- Sections, not segments: `.section .prg_rom_1` rather than `.segment "PRG_ROM_1"`.
- No leading underscore on C symbols. C's `score` is `score` in asm.
- **`.S`, not `.s`, if you want the C preprocessor.** The driver runs it only for the uppercase extension. A `.s` file gets assembler directives alone — `.include`, `.equ`, `.macro`; a `.S` file gets `#include`, `#define` and `#ifdef` as well, so one header of `#define`s can serve both C and assembly. cc65 projects use `.s` universally, so a literal port inherits the lowercase name and quietly forfeits that.

  Getting this wrong fails late and misleadingly. `.include`ing a `#define`-based header from a `.s` file is not an error: the assembler treats `#` lines as comments, so every constant becomes an *undefined external symbol* and the first complaint is `undefined symbol` from the linker. Suspect the extension before the header. Note also that macros shared with assembly must not be parenthesised — `(expr)` is indirect addressing, so `#define BUF (0x0400 + 0x40)` assembles `sta BUF` to something other than what you meant.

**Zero page addressing is a hint problem, not an addressing problem.** The assembler must choose the 1-byte or 2-byte encoding before the linker knows the address. Force zero page by defining the symbol as a constant expression, putting it in a `.zp`/`.zeropage`/`.directpage` section, marking the section with the `z` flag (`.section .lowmem,"az",@nobits`), or declaring `.zeropage <symbol>`. Otherwise everything defaults to 16-bit — safe, bigger.

Use `mos16lo()`/`mos16hi()` or the WDC shorthands `#<`/`#>`/`#^` to take bytes of a link-time address.

To reserve zero page for assembly, prefer declaring it in C where LTO can see it — `char __zp foo;` — rather than `-mreserve-zp=<n>`. The compiler then deducts it automatically and can optimize away unused reservations. Note `char *__zp p` is a 2-byte pointer stored in zero page, while `char __zp *p` is a 1-byte pointer *to* zero page.

## Interrupts

Handlers must be annotated or the static stack analysis will place a frame that an interrupt can corrupt.

- `__attribute__((interrupt))` — saves all registers, emits `cld` on entry, returns with `rti`, and is treated as possibly recursive (forcing callees onto the soft stack).
- `__attribute__((interrupt_norecurse))` — same, but not self-recursive. Use this when the source is masked while handling. It keeps static stack allocation, so prefer it when true.
- `no_isr` added to either — returns with `rts` and emits no save/restore, for when you write the prologue yourself in assembly. The ABI effects still apply.

Writing that prologue by hand means saving the imaginary registers a called C function may clobber, not a guessed few: `abi.md` has the worked sequence and its cost. Pick the subset by eye and it survives until codegen next changes which register the callee reaches for.

It is undefined behavior for anything asynchronous to call a C function lacking one of these attributes.

## Linker scripts

Read `references/linker-scripts.md` when writing or modifying one. The shape of a minimal complete target:

```ld
MEMORY {
  ram      : ORIGIN = 0x0000, LENGTH = 0x10000    /* what gets written to the file */
  user_ram (rw) : ORIGIN = 0x0200, LENGTH = 0xfe00 /* what code/data may use */
}
REGION_ALIAS("c_readonly", user_ram)
REGION_ALIAS("c_writeable", user_ram)
SECTIONS { INCLUDE c.ld }

__rc0 = 0x00;
INCLUDE imag-regs.ld
__stack = 0;                 /* top of soft stack; grows down */

OUTPUT_FORMAT { FULL(ram) SHORT(_start) }
```

Four things are doing the work. `REGION_ALIAS` for `c_readonly`/`c_writeable` is how `c.ld` knows where to put C sections. `__rc0` plus `INCLUDE imag-regs.ld` places the imaginary registers (set only even registers; odd ones must follow their pair). `__stack` feeds the `init-stack` library. And `OUTPUT_FORMAT { }` — an llvm-mos extension — is a small script that emits the actual binary: `BYTE`/`SHORT`/`LONG`/`QUAD` for header fields computed from link-time symbols, and `FULL(region)`/`TRIM(region)` to dump a memory region padded or trailing-trimmed. This is how PRG, XEX, iNES, and cartridge formats are produced without any post-processing tool.

Optional libraries are selected per target by linking them: `-lexit-loop`, `-lexit-return`, `-lexit-custom`, `-linit-stack`. Without an exit library, returning from `main` runs off the end.

**Section granularity decides what `--gc-sections` can drop.** The compiler emits one section per function already — `-ffunction-sections` is the default, so C needs nothing. Hand-written assembly is where it goes wrong: you write the `.section` directive, and a single `.section .text` at the top of a file is one indivisible unit that every target linking any part of it takes whole. Give each entry point its own `.section .text.<name>,"ax",@progbits`, as the SDK's own libraries do. Split data the same way — `.bss.<name>`, `.zp.bss.<name>`, `.data.<name>` — since the collection patterns are `*(.bss .bss.*)` and friends; zero-page bytes retained only for sharing a section name are the expensive case. Check `--gc-sections` is actually on the link line, too: it is not implied by `-Os`/`-Oz`.

The suffix buys linker-side granularity only — garbage collection, `--icf` folding, and per-function placement. It has no effect on inlining: that is decided during codegen, long before section names mean anything, and assembly in a `.s`/`.S` file cannot be inlined at any granularity because the compiler never sees its body. The final link merges everything back through `*(.text .text.*)`, so the names do not survive into the output.

**If a section doesn't appear in the output**, it's one of two causes: it wasn't marked allocatable (add `"a"` to the `.section` flags — this is not the default for non-standard names in hand-written asm), or it was garbage-collected because nothing referenced it (add the `R` retain flag, or `KEEP()` it in the linker script).

Beware supplementary `-T script.ld` on top of a platform target: it can suppress the platform's `OUTPUT_FORMAT`, leaving you with an ELF where you expected a flat binary.

## Converting from cc65

See `references/cc65-migration.md` for the full mapping. The strategic advice: don't translate cc65 idioms literally. Much cc65-era style — manual global temporaries, hand-rolled fixed-point, avoiding locals, avoiding struct returns — actively fights LLVM's register allocator. Port the algorithm, write it as clean C, measure, and only then hand-optimize.

Mechanically: the SDK ships cc65-compatible headers (`peekpoke.h`, `6502.h`, and per-platform ones), the linker already maps cc65 segment names (`CODE`, `RODATA`, `LOWCODE`, `ONCE`, `STARTUP`, `INIT`, `ZPSAVE`) into the modern sections, and LLD can even link `ca65`-produced `.o` files directly via `od65`/`ld65` if you want to migrate incrementally.

## Commodore targets

For C64, C128, VIC-20, PET, Commander X16, and MEGA65 work, read `references/commodore.md` — it covers the shared `commodore` layer (KERNAL wrappers, CBM DOS file I/O, BASIC header, `unmap-basic`/`save-basic`), the `volatile`-struct hardware headers per chip, and the target-specific facilities: VERA and the extended `cx16_k_*` KERNAL on CX16; the 45GS02, DMAgic (`dma.hpp`), hardware math unit, and VIC-IV on MEGA65.

Two things to know immediately. There is **no `c65` target** — MEGA65 is the one to use for C65-family work, and its config also pulls in the C64 headers. And the `cbm_k_*` wrappers are the best available worked examples of correct clobber discipline, so read a few before writing your own ROM calls.

## MEGA65 / 45GS02

`references/45gs02.md` covers the CPU: the Q pseudo-register, the Z register, 28-bit flat addressing via `[$nn],Z`, `MAP`/`EOM`, and how to move values in and out of Z and Q given that no `z` or `q` inline-asm constraint exists. The assembler supports the full 45GS02 instruction set, so hand-written assembly is unrestricted.

**The one rule to internalize before writing any MEGA65 assembly:** Z must be 0 *whenever control is in compiled code*. Your assembly may use Z freely and hand it back — the catch is that "hand it back" comes due earlier than you'd think. The compiler never sets Z, never checks it, and cannot represent it, so every boundary where control reaches compiled code counts: returns from inline asm, from `.s` routines, from interrupt handlers, and — the one people miss, because it's mid-routine rather than at the end — calls from your assembly into C. The plain base-page indirect mode is encoded as `(zp),Z` (`sta ($12)` and `sta ($12),z` are literally the same opcode), so every compiler-generated pointer dereference is Z-indexed; the asm listing shows a bare `lda (__rc2)` and only the disassembler reveals the `,z`. A stray non-zero Z silently offsets memory accesses program-wide, with no crash at the site of the bug.

This is **entirely manual — the toolchain offers no support at all**: no `z`/`q` constraint, no clobber-list entry (`::: "z"` is `unknown register name`), no automatic save/restore even under `__attribute__((interrupt))`, no startup initialization, and no diagnostic. A hand-written `ldz #0` at the end of anything that touches Z is the only mechanism that exists.

**There is no far-pointer type, so don't design around one.** The backend knows two address spaces — `enum AddressSpace { AS_Memory, AS_ZeroPage }` in `MOSInstrInfo.h` — so no `address_space` attribute gives you `FAR[i] = v`, and nothing selects the 32-bit `[$nn],Z` modes the assembler encodes. Every 28-bit access is a call (`lpeek`/`lpoke`, or DMA in bulk) or your own inline asm, and pays the per-argument cost in `references/abi.md`.

## Tooling

The standard LLVM tools — `llvm-objdump -d --print-imm-hex`, `llvm-nm`, `llvm-readelf`, `llvm-size`, `llvm-objcopy`, `llvm-strip`, `llvm-mc` — need an ELF, and **`-c` does not produce one under the default LTO**: it writes LLVM IR bitcode, which every one of them rejects as "not recognized as a valid object file". `-fno-lto -c` gives a real ELF relocatable, at the cost of no longer being the pipeline that ships. `llvm-mlb` emits Mesen label files for NES debugging. Compile with `-g` for DWARF and source-level debugging under emulators with a GDB stub.

**`-finstrument-functions` gives call tracing on a target with no debugger**, through the usual `__cyg_profile_func_enter`/`__cyg_profile_func_exit` hooks — enough to record a call stack and print a backtrace from an assertion handler. Two conditions. Mark the hooks `__attribute__((no_instrument_function))`, or they instrument themselves and recurse. And have them **ignore the `call_site` argument**: clang supplies it with `llvm.returnaddress`, which this backend cannot legalize, so that call has to be optimized away as dead. The consequence is that instrumentation links at `-O1` and above but fails at `-O0`, with `LLVM ERROR: unable to legalize instruction: … llvm.returnaddress` reported at *link* time against no source line. The same limitation means `__builtin_return_address()` does not work here at all. To recover the call site anyway, read it off the hardware stack — `tsx`, then the return address at `$0100+S` — which works because `jsr` still pushes there even though frames live on the soft stack.

The *final link output* of a complete target is generally not ELF — `OUTPUT_FORMAT` emits a flat binary, so `llvm-nm`/`llvm-objdump` reject it no matter what you called the file. Build systems often keep the ELF alongside (CMake leaves `foo.prg.elf` next to `foo.prg`); disassemble that, or use `-Wl,--lto-emit-asm` and read `<output>.lto.s`.

**`--lto-emit-asm` replaces the link output rather than accompanying it.** The link exits 0 and writes `<output>.lto.s`, and no binary and no map file appear — including when you asked for one with `-Wl,-Map` in the same command. Reuse a build command with that flag left in and the build reports success while producing nothing to run; a stale binary from the previous build is still sitting there to be tested. Emit assembly in a separate invocation from the one that produces the artifact. See also the gotcha under **Toolchain basics** — the failure mode is a silently empty search, not an error you notice.

**`-Wl,-Map,<file>` sidesteps the whole problem by writing a link map.** Because the output is not ELF and `llvm-nm` cannot read it, the map is the straightforward route to an address→symbol table — for a build-time size audit, for an emulator test script or debugger symbol file, or compiled back into the program so on-target diagnostics can name a function instead of printing a bare address. Symbol lines carry the VMA in the first column and the name in the last, so extracting one is a filter:

```sh
mos-sim-clang -Os -o prog prog.c -Wl,-Map,prog.map
awk 'NF==5 && $NF ~ /^[A-Za-z_][A-Za-z0-9_]*$/ {print $NF, $1}' prog.map
```

Section names appear in the same shape as symbol names, so filter to the symbols you asked for rather than trusting the whole list. Regenerate on every build and have the consumer fail loudly when a name it needs is missing: an external script holding a hand-copied address is not wrong until the day the layout shifts, and then it reads a plausible value from whatever moved into that byte. The same argument applies to the scripts themselves — a check that rejects literal addresses in them keeps the map the single source of truth.

A map also makes **placement assertions** cheap enough to run on every build: that a symbol landed in the section you meant, that a region stayed inside its budget, that the free-RAM headroom above `__heap_start` is still there. Those are the invariants a linker script cannot express and a successful link will not check for you.

**To disassemble a raw binary, use `llvm-mc`, not `llvm-objdump`.** Wrapping the file in an ELF with `llvm-objcopy -I binary` and disassembling that looks right and is not: the synthesised ELF's `e_flags` say plain 6502, `--mcpu=` does not override them, and every newer instruction comes out as `<unknown>` while the rest decodes plausibly. Feed the bytes to `llvm-mc -disassemble -triple mos --mcpu=…` instead.

`llvm-mc -disassemble` **decodes each input line independently**, which makes it a batch oracle rather than a one-shot tool: put one encoding per line and thousands come back in a single invocation. That is enough to enumerate an entire opcode space — generate a table from the assembler itself, then diff a decoder against it over a whole ROM — and it is much faster than one process per instruction. Two caveats when comparing: it prints operands in decimal unless you pass `--print-imm-hex`, and it prints branch operands as raw offsets rather than resolved targets.

For editor support, point clangd at the SDK's own binary and pass `--query-driver=/path/to/llvm-mos-sdk/bin/*clang*` (literal asterisks) so it can discover target headers.

**Test the format arithmetic on the host, not in the emulator.** Most of a 6502 program is encoding and decoding formats something else defines — disk layouts, register packings, text conversions, tables — and none of that needs the target. Split it into its own translation unit and run it natively, where it is orders of magnitude faster to exercise and a failure names a line instead of hanging a machine. Two things make a host pass meaningless if ignored: `char` is **unsigned** and `int` is **16 bits** on this target, against signed/32-bit on a typical host, so `char` comparisons and anything near 16-bit overflow must still be checked on the machine. `references/host-testing.md` has the split, the oracle discipline, the harness shape, and the `__mos__` guard for ELF-only section attributes.

**When the question is what the *generated code* does, run it under `mos-sim`.** It executes the 6502 the compiler emitted and counts cycles, with no hardware and no emulator, so correctness and cost come out of the same run — and the type model is the target's, which is what a host pass could not establish. `mos-sim --cycles` covers the whole program including startup and `printf`, so bracket the code under test with the `sim` platform's `reset_clock()`/`clock()` instead; one measured pair came out 820 cycles against 309 inside a run whose total was 24358. `references/simulator-testing.md` covers region timing, `--profile` for per-address cycle attribution, and the boundary of what this proves.

## Reference files

- `references/inline-asm.md` — constraints, clobbers, the decision procedure, worked examples, crash modes
- `references/linker-scripts.md` — MEMORY/SECTIONS/OUTPUT_FORMAT, banking, zero page, section flags
- `references/commodore.md` — C64/C128/VIC-20/PET/CX16/MEGA65 hardware support in `mos-platform/`
- `references/45gs02.md` — MEGA65 CPU: Q register, Z=0 invariant, 28-bit addressing, MAP/EOM
- `references/cc65-migration.md` — ca65↔llvm-mos syntax, segments, headers, incremental linking
- `references/abi.md` — full calling convention: argument registers, return values, caller/callee-saved
- `references/host-testing.md` — running format/logic code natively, and the `char`/`int` gaps that make a host pass meaningless
- `references/simulator-testing.md` — `mos-sim`: cycle counts on real codegen, region timing, `--profile`, and what a simulator pass does not prove

## Upstream sources

Two repositories, and it matters which one a question belongs to:

- **[llvm-mos](https://github.com/llvm-mos/llvm-mos)** — the compiler, assembler, and linker. Paths below are relative to its root. `llvm/test/MC/MOS/all-<cpu>-opcodes.s` is the authoritative instruction list per CPU, each line annotated with its expected encoding; `llvm/lib/Target/MOS/` holds the backend, including `MOSCallingConv.td` (the ABI) and `MOSInlineAsmLowering.cpp` (constraint handling).
- **[llvm-mos-sdk](https://github.com/llvm-mos/llvm-mos-sdk)** — the platform libraries, headers, and linker scripts under `mos-platform/`, which is what the reference files here cite.

Prefer these over the project wiki when they disagree — the wiki has been observed to be stale (e.g. it documents a `-f[no-]emit-frame-pointer` flag that the driver rejects; see `abi.md`).

## Maintaining this skill

When adding to or correcting this file or its reference files:

- **Evidence or nothing.** A new claim needs a citation: an `mos-platform/<path>`
  in llvm-mos-sdk, a path into the backend, a datasheet plus a second
  implementation, or a measurement you took. Say what you ran and what it
  reported. Sizes and cycle counts are this skill's currency — quote the number,
  not "smaller".
- **Two sources for ISA behaviour.** Datasheets disagree with silicon. Cite the
  core (`gs4510.vhdl`), an emulator (`xemu/xemu/cpu65.c`), or a second
  simulator alongside the datasheet, and record contradictions rather than
  picking a side silently.
- **Generic, not autobiographical.** No dates, no branch or PR numbers, no local
  paths, no "we found". A rule a stranger can apply, not an account of how it
  was found. A project that prompted a finding is not a citation for it —
  re-derive the claim against the toolchain and cite that.
- **Brief.** One idea per entry. Delete anything a reader gets from one grep of
  the tree, unless it is a trap.
- **Teach the interrogation, don't transcribe the snapshot.** Where a fact can
  be read out of the tree, a build or a tool, give the command that extracts it
  and say how to read the result. A copied table is stale the day the thing it
  copied changes, and worse, it is stale silently. Record the shape of the
  answer and the trap in reading it; leave the values where they live.
- **Traps earn their space.** Prefer the failure mode that looks like success —
  a link that emits no binary, a search that comes back empty because the tool
  rejected the file, a host pass that the target contradicts. Those are what
  these files are for.
- **Changing the toolchain belongs in `llvm-mos-dev`.** These files cover using it.
- **Prune.** When the toolchain changes or a claim proves wrong, fix or remove
  it. A stale rule is worse than no rule.
