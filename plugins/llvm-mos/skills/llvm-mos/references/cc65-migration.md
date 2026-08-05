# Converting cc65 / ca65 code to llvm-mos

Contents:
1. Strategy — what to port and what to rewrite
2. C-level differences
3. ca65 → llvm-mos assembly syntax
4. Segments → sections
5. Compatibility headers
6. Incremental migration: linking ca65 objects directly

---

## 1. Strategy — what to port and what to rewrite

The mechanical translation is easy. The trap is porting cc65 *style*.

cc65 is a non-optimizing compiler with a fixed lowering per C construct. A generation of good advice grew around that: avoid locals, hoist everything into globals or static temporaries, reuse scratch variables, avoid passing/returning structs, hand-unroll, precompute tables of things the compiler could fold. **Most of that advice is counterproductive on llvm-mos**, and some of it actively blocks optimization:

- Reusing one global temporary everywhere forces the register allocator to keep a specific memory location live, where it would otherwise have kept the value in A/X/Y or an imaginary register and never stored it at all.
- Globals are observable to other functions, so stores to them are hard to eliminate. Locals can vanish entirely.
- `__fastcall__`, `#pragma` register/static-locals directives, and manual zero-page juggling have no llvm-mos equivalent because the compiler does this work with a whole-program view.

The productive sequence: **port the algorithm as plain, clean C; build with the defaults (`-Os -flto`); measure; then optimize only what's actually hot**, using the guidance in the main skill. Expect the naive port to be smaller and faster than the tuned cc65 original in most cases, and expect a few places where it isn't — those are worth hand-tuning.

Do keep the genuinely architectural cc65 advice, which is about data layout rather than the compiler: struct-of-arrays over array-of-structs, keep indices under 256, prefer 8-bit types where the range allows.

---

## 2. C-level differences

| cc65 | llvm-mos |
|---|---|
| `__fastcall__`, `__cdecl__` | Delete. There's one calling convention (see `abi.md`). |
| `#pragma static-locals`, `#pragma register-vars` | Delete. The compiler decides, better. |
| `#pragma bss-name`, `#pragma code-name` | `__attribute__((section(".name")))` |
| `__A__`, `__X__`, `__AX__` pseudo-vars | Inline asm with `"a"`/`"x"` constraints |
| `__asm__ ("...")` with cc65 syntax | GCC-style inline asm — see `inline-asm.md` |
| Zero page via `#pragma zpsym` / linker cfg | `char __zp x;` (LTO-visible) or `-mreserve-zp=` |
| `.cfg` linker config | `.ld` linker script — see `linker-scripts.md` |
| `--start-addr` | `ORIGIN` in the script's `MEMORY` block |
| `waitvsync()`, `peek`/`poke` | Provided: `<cbm.h>`, `<peekpoke.h>` |

Interrupt handlers need real attributes now (`interrupt`, `interrupt_norecurse`, `no_isr`) — cc65's convention of "just write a function and point the vector at it" is undefined behavior on llvm-mos because of the static stack analysis.

C99/C11/C++ actually work, including much of the C++ standard library's freestanding portion. Templates, `constexpr`, and user-defined literals are all usable and often produce *smaller* code than the C equivalent because computation moves to compile time. `<soa.h>` and `<charset.h>` both exploit this — note `soa.h` is common to every target, while `charset.h` is per-platform (c64, vic20, pet, cx16, atari8; MEGA65 gets the c64 one via its include path) and simply doesn't exist on targets without a native character set.

---

## 3. ca65 → llvm-mos assembly syntax

The assembler is GNU-syntax with 6502 accommodations. `$` works as a hex prefix (so most operand expressions port unchanged), and full GNU macro/conditional/include machinery is available.

| ca65 | llvm-mos |
|---|---|
| `.segment "PRG_ROM_1"` | `.section .prg_rom_1` |
| `.global _score` / `_score: .res 5` | `.global score` / `score: .fill 5` |
| `bne :+` … `:` | `bne 1f` … `1:` |
| `bne :-` … (backward) | `bne 1b` |
| `.res N` | `.fill N` or `.ds.b N` |
| `.byte`, `.word` | `.byte`, `.word` (same) |
| `#<label`, `#>label` | `#<label`, `#>label` (same), or `#mos16lo(label)` / `#mos16hi(label)` |
| `.proc` / `.endproc` | plain labels (use `.Lname` for local scope) |
| `.zeropage` segment | `.section .zp,"az",@nobits` or `.zeropage <symbol>` |
| `.import` / `.export` | `.global` (and just reference it) |

**No leading underscore.** cc65 prefixes C symbols with `_`; llvm-mos does not. A C function `score` is `score` in assembly. This is the single most common porting error.

**Numeric local labels are required inside inline asm.** A named label breaks if the block is instantiated more than once (inlining, loop unrolling). `1:`/`1f`/`1b` are safe; any digit works, giving you several independent local label streams.

**Zero-page addressing is a hint problem.** ca65 could see your whole program; llvm-mos assembles before linking, so the assembler must pick the 1- or 2-byte encoding without knowing the final address. Force zero page one of four ways:

1. Define the symbol as a constant expression: `low = 55 + 2*4` then `lda low,x`
2. Put it in a section named `.zp`, `.zeropage`, or `.directpage`
3. Mark the section with the `z` flag: `.section .lowmem,"az",@nobits`
4. Declare `.zeropage <symbol>` — affects references only, doesn't place anything (use for externs)

Without one of these, everything defaults to 16-bit: correct, just bigger.

**Address modifiers**, in function or `@` form (function form doesn't work in directives — use the short form there):

| Modifier | Short | Meaning |
|---|---|---|
| `mos8()` | `<` | force 8-bit (zero page) address |
| `mos16()` | `!` | force 16-bit (absolute) address |
| `mos16lo()` | `#<` | low byte of a 16-bit address |
| `mos16hi()` | `#>` | high byte of a 16-bit address |
| `mos24()` | `>` | force 24-bit (long) address |
| `mos24bank()` | `#^` | bank byte of a 24-bit address |
| `mos24segment()`, `mos24segmentlo()`, `mos24segmenthi()` | | segment portion |

`lda #mos16lo(QSORT)`, `lda #QSORT@mos16lo`, and `lda #<QSORT` are all equivalent. In directives (`.byte` etc.) the `#` isn't available, so `<` means what `#<` means in instructions.

llvm-mos-specific directive: `.mos_addr_asciz <expr>, <digits>` emits a relocatable expression as fixed-length decimal ASCII — this is how the Commodore BASIC `SYS` header gets the real start address.

Assemble with the clang driver: `mos-clang -c file.s` (or `mos-c64-clang -c file.s` to get target include paths).

---

## 4. Segments → sections

The SDK's section scripts already accept the standard cc65 segment names as input patterns, so ported assembly mostly lands in the right place:

| cc65 segment | Collected into | Input pattern in |
|---|---|---|
| `CODE`, `LOWCODE`, `ONCE`, `STARTUP` | `.text` | `text-sections.ld` |
| `RODATA` | `.rodata` | `rodata-sections.ld` |
| `DATA` | `.data` | `data-sections.ld` |
| `BSS`, `COMMON` | `.bss` | `bss-sections.ld` |
| `NULL`, `INIT`, `ZPSAVE` | `.noinit` | `noinit-sections.ld` |

Custom segments need a `SECTIONS` entry in your linker script. Remember the two output-visibility rules from `linker-scripts.md`: mark it allocatable (`"a"`) and keep it alive (`"R"` flag or `KEEP()`), or it silently won't appear.

Two habits carry over from ca65 and are worth breaking during the port:

- **Rename `.s` to `.S`.** ca65 has no preprocessor, so cc65 projects put shared constants in an `.inc` full of `.equ` and `.include` it. Keeping the lowercase extension keeps that limitation: only `.S` is preprocessed, and only then can one header of `#define`s serve both the C and the assembly side — which is what lets you delete the hand-maintained C mirror of the constants. The failure mode if you convert the header but not the extension is `undefined symbol` at link time, because the assembler reads `#define` lines as comments.
- **Split the `.text`.** ca65 encourages one segment per file; ld.lld collects at section granularity. A single `.section .text` covering a whole file of routines is linked in full by every target that touches any of it. One `.section .text.<name>,"ax",@progbits` per entry point lets `--gc-sections` drop the rest.

---

## 5. Compatibility headers

Several cc65 headers ship, adapted:

- `<peekpoke.h>` — `PEEK`/`POKE`/`PEEKW`/`POKEW` macros
- `<6502.h>` — `BRK()`, `CLI()`, `SEI()` (implemented as `leaf` inline asm)
- `<cbm.h>` — the Commodore KERNAL layer plus cc65's `COLOR_*`, `JOY_*`, `CH_*`, `CBM_*`, `TV_*` constants
- Per-platform: `<c64.h>`, `<c128.h>`, `<vic20.h>`, `<pet.h>`, `<cx16.h>`, `<mega65.h>`

Hardware access differs in style: instead of cc65's `#define VIC (*(struct __vic2*)0xD000)` plus manual poking, the SDK provides fully-typed `volatile` structs with bitfields and `static_assert`ed sizes. Prefer field access; it's clearer and generates equal or better code.

`__fastcall__` appears in a few header declarations for source compatibility and is ignored.

---

## 6. Incremental migration: linking ca65 objects directly

You don't have to convert everything at once. LLD can link `xo65` object files (ca65's native format) by shelling out to `od65` and `ld65`. It searches `PATH` for them, or you can point at them explicitly:

These are **linker** options, so they need `-Wl,` when going through the clang driver:

```sh
mos-c64-clang -o game.prg main.c -Wl,--od65-path=/usr/bin/od65 -Wl,--ld65-path=/usr/bin/ld65 legacy.o
```

Passing them bare to the driver fails — `mos-c64-clang: error: unknown argument: '--od65-path=...'` — because clang doesn't recognise them as its own. `ld.lld --help` lists both.

Symbol values pass freely between xo65 and ELF objects, and xo65 segments are placed as if they were ELF sections. The SDK already maps the default cc65 segments to the corresponding modern output sections.

Limitations worth knowing before relying on this:

- Doesn't work with a relocatable link (`-r`) — ca65's relocations are richer than llvm-mos ELF represents.
- ld65 can't place segments from different xo65 files differently, so all xo65-derived sections are treated as coming from one fictitious input file named `xo65-enclave` in linker scripts.
- Bank handling: the second-highest byte of LLD's 32-bit virtual address becomes ca65's `.BANK` specifier; the highest byte is zeroed. Symbols get both high bytes zeroed. Only applies when no segment contains far/long addresses.
- ELF section names encode type and flags that xo65 segment names can't hold, so an underscore escaping scheme is used (`__`→`_`, `_d`→`$`, `_h`→`-`, `_p`→`.`, `_xXX`→byte, `_tn`/`_tp`→section type, `_fw`/`_fx`→write/exec flags).

This is a good way to move a large project function-by-function while keeping it building at every step.
