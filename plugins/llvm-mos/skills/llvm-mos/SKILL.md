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

**Gotcha worth knowing up front:** because LTO is the default, `-S` emits LLVM IR, not assembly. To read the generated 6502, add `-fno-lto`:

```sh
mos-c64-clang -Os -fno-lto -S -o - foo.c    # actual 6502 asm
mos-c64-clang -Os -o foo.elf foo.c && llvm-objdump -d --print-imm-hex foo.elf
```

Select the CPU with `-mcpu=` (`mos6502`, `mos6502x`, `mos65c02`, `mosr65c02`, `mosw65c02`, `mos65ce02`, `mos4510`, `mos45gs02`, `mos65el02`, `mos65dtv02`, `mosw65816`, `moshuc6280`, `mosspc700`, `mossweet16`). Each defines `__mos__` plus a macro per compatible CPU.

## Writing C that compiles well

These rules come from the project's own optimization guide; the reasoning matters more than the list.

- **Don't hand-optimize into globals.** A local can live in A, move to X for indexing, and never touch memory. A global is an address the compiler must often store to, because something else might observe it.
- **Use `-fnonreentrant` (or `__attribute__((nonreentrant))`) when you use function pointers.** Indirect calls defeat the call-graph analysis, so the compiler conservatively falls back to the soft stack for everything reachable. This flag is frequently the single biggest speed/size win in a program with a jump table or callback.
- **Mark assembly-implemented functions `__attribute__((leaf))`.** Same reason: an opaque `jsr` might call anything, including back into C, which forces soft-stack allocation up the call graph. `leaf` promises it doesn't re-enter C. The SDK uses this on essentially every KERNAL/BIOS wrapper.
- **Make function-local constant arrays `static`.** Otherwise the C standard requires a fresh copy per invocation, and the compiler emits the copy.
- **Prefer structs of arrays.** Absolute-indexed addressing needs a constant base plus an 8-bit index; an array of 5-byte structs needs a multiply. `#include <soa.h>` provides `soa::Array<T, N>` in C++ which does the byte-striping for you while looking like a normal array.
- **Keep array indices under 256**, and don't compute in wide types unless you consume the wide result.
- **Infinite loops need a side effect.** `while (1);` is undefined behavior and gets deleted. Write `for (;;) asm volatile("");` or spin on a `volatile` object.

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

**Section granularity decides what `--gc-sections` can drop.** The compiler emits one section per function, so C code is already at the right granularity; hand-written assembly usually is not. A `.s` file with a single `.section .text` at the top is one indivisible unit, and every target that links it takes all of it, however little it calls. Give each entry point its own `.section .text.<name>,"ax",@progbits` — as the SDK's own libraries do — and unreferenced ones drop out. Worth checking `--gc-sections` is actually on the link line; it is not implied by `-Os`/`-Oz`.

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

## Tooling

Everything is ELF, so the standard LLVM tools work: `llvm-objdump -d --print-imm-hex`, `llvm-nm`, `llvm-readelf`, `llvm-size`, `llvm-objcopy`, `llvm-strip`, `llvm-mc`. `llvm-mlb` emits Mesen label files for NES debugging. Compile with `-g` for DWARF and source-level debugging under emulators with a GDB stub.

For editor support, point clangd at the SDK's own binary and pass `--query-driver=/path/to/llvm-mos-sdk/bin/*clang*` (literal asterisks) so it can discover target headers.

## Reference files

- `references/inline-asm.md` — constraints, clobbers, the decision procedure, worked examples, crash modes
- `references/linker-scripts.md` — MEMORY/SECTIONS/OUTPUT_FORMAT, banking, zero page, section flags
- `references/commodore.md` — C64/C128/VIC-20/PET/CX16/MEGA65 hardware support in `mos-platform/`
- `references/45gs02.md` — MEGA65 CPU: Q register, Z=0 invariant, 28-bit addressing, MAP/EOM
- `references/cc65-migration.md` — ca65↔llvm-mos syntax, segments, headers, incremental linking
- `references/abi.md` — full calling convention: argument registers, return values, caller/callee-saved

## Upstream sources

Two repositories, and it matters which one a question belongs to:

- **[llvm-mos](https://github.com/llvm-mos/llvm-mos)** — the compiler, assembler, and linker. Paths below are relative to its root. `llvm/test/MC/MOS/all-<cpu>-opcodes.s` is the authoritative instruction list per CPU, each line annotated with its expected encoding; `llvm/lib/Target/MOS/` holds the backend, including `MOSCallingConv.td` (the ABI) and `MOSInlineAsmLowering.cpp` (constraint handling).
- **[llvm-mos-sdk](https://github.com/llvm-mos/llvm-mos-sdk)** — the platform libraries, headers, and linker scripts under `mos-platform/`, which is what the reference files here cite.

Prefer these over the project wiki when they disagree — the wiki has been observed to be stale (e.g. it documents a `-f[no-]emit-frame-pointer` flag that the driver rejects; see `abi.md`).
