# Commodore targets in llvm-mos-sdk

Covers what `mos-platform/` actually provides for the Commodore family, with emphasis on MEGA65 and Commander X16.

Contents:
1. The target tree
2. Shared `commodore` layer: KERNAL, CBM DOS, startup objects
3. Hardware register headers
4. Per-target notes (C64, C128, VIC-20, PET, CX16, MEGA65)
5. PETSCII string literals
6. Startup/shutdown hooks and the `.init.NNN` convention

---

## 1. The target tree

```
common → commodore → c64
                   → c128
                   → vic20
                   → pet
                   → cx16
                   → mega65
```

`commodore` is an *incomplete* target: it supplies the KERNAL, CBM DOS file I/O, the BASIC header stub, and `commodore.ld`, but no memory map. Each complete target adds `link.ld`, `kernal.S` (jump-table addresses), hardware headers, and a `clang.cfg`.

**There is no `c65` target.** The MEGA65 target is the one to use for C65-family work — it runs on real C65 hardware paths through the MEGA65's C65 compatibility, and its `clang.cfg` sets `-mcpu=mos45gs02`. Note that MEGA65's config deliberately pulls in the **C64 include and asminc directories** as well, so `<c64.h>`, `<_vic2.h>`, `<_sid.h>`, and `<_6526.h>` are all available when targeting MEGA65 — the VIC-IV is a superset and the CIAs are the same parts.

Config summary:

| Target | `-mcpu` | `-mlto-zp` | Define |
|---|---|---|---|
| c64 | (6502 default) | 110 | `__C64__` |
| c128 | | | `__C128__` |
| vic20 | | | `__VIC20__` |
| pet | | | `__PET__` |
| cx16 | `mosw65c02` | 90 | `__CX16__` |
| mega65 | `mos45gs02` | 110 | `__MEGA65__` |

---

## 2. Shared `commodore` layer

### KERNAL wrappers — `<cbm.h>`

Thin, correctly-clobbered wrappers over the KERNAL jump table, named `cbm_k_*`: `acptr`, `basin`, `bsout`, `chkin`, `chkout`, `chrin`, `chrout`, `cint`, `ciout`, `ckout`, `clall`, `close`, `clrch`, `getin`, `iobase`, `listen`, `load`, `open`, `readst`, `save`, `scnkey`, `second`, `setlfs`, `setnam`, `talk`, `tksa`, `udtim`, `unlsn`, `untlk`.

Most are declared `__attribute__((leaf))`, which is what keeps the static stack analysis intact across a ROM call. **Study these before writing your own ROM call** — they are the reference implementation of the technique-selection rule in `inline-asm.md` §7. Note what they actually are, because it is easy to assume they're all inline asm: **20 of the 21 `cbm_k_*.c` files contain no assembly at all.** The whole of `cbm_k_chrout.c` is:

```c
extern void __CHROUT(unsigned char C) __attribute__((leaf));
void cbm_k_chrout(unsigned char C) { __CHROUT(C); }
```

The compiler emits the `jsr` itself and places arguments by the normal ABI. The split across the 29 wrappers:

| Form | Count | Used when |
|---|---|---|
| `extern` prototype, no asm | 20 `.c` | Arguments and return map onto the C ABI |
| Inline asm | 1 `.c` | A value lands where the ABI has no name for it — `cbm_k_load.c` needs the carry |
| `.s` file | 8 | KERNAL convention needs translation — `cbm_k_setlfs.s` moves a third arg from `__rc2` into Y |

The one-line inline-asm form often quoted as "the simplest wrapper" is *not* a `cbm_k_*` function — it's the internal `__chrout` in `commodore/chrout.c`, which backs `putchar`:

```c
void __chrout(char c) {
  __attribute__((leaf)) asm volatile("jsr\t__CHROUT" : "+a"(c) : : "p");
}
```

It's a good model, and measurably tighter than the prototype form when inlined into a loop (see `inline-asm.md` §7) — just don't mistake it for how the `cbm_k_*` API is built.

The underscore-prefixed `__CHROUT` symbols come from each platform's `kernal.S`, via a `weakdef` macro that declares the entry point `.weak` and aliases it to a `__`-prefixed global (58 of them in `c64/kernal.S`). This does double duty: it lets a program override an individual KERNAL routine at link time, *and* it is what makes the `extern`-prototype technique possible at all, since `__CHROUT` resolves to an absolute address at $FFD2.

```asm
.macro weakdef name:req
  .weak \name
  __\name = \name
  .global __\name
.endm
```

`cbm.h` also carries the cc65-compatible constants — `COLOR_*`, `JOY_*_MASK`, `CH_*` screen/control codes, `CBM_READ`/`CBM_WRITE`/`CBM_SEQ`, `TV_NTSC`/`TV_PAL`, `CBM_A_RO`/`WO`/`RW` — plus `get_tv()`, `kbrepeat()`, and `waitvsync()`.

### CBM DOS file I/O

On top of the KERNAL layer the platform implements POSIX-shaped file access — `open`, `close`, `read`, `write`, plus `remove`/`rename` (`sysremove.s`, `sysrename.s`) and disk commands (`diskcmd.s`, `scratch.s`). This means `<stdio.h>` and `<fcntl.h>` work against a real drive, and `printf`/`putchar` route through CHROUT. Filename translation (`translate-filename.cc`) handles the ASCII↔PETSCII mapping.

### Startup and shutdown objects

Linked in per target via `INPUT()` in the linker script or `-l:`:

| Object | Purpose |
|---|---|
| `basic-header.o` | The `1 SYS ...` BASIC stub that launches the program. Always linked by `commodore.ld`. Uses the `.mos_addr_asciz` directive to emit the SYS address as decimal ASCII computed at link time. |
| `unmap-basic.o` | Banks out the BASIC ROM to free RAM. C64: opens $0801–$CFFF contiguous. Also used by MEGA65. |
| `save-basic.o` | Saves/restores the BASIC zero page and hardware stack pointer so the program can `return` cleanly to the BASIC interpreter instead of looping forever. Link with `-l:save-basic.o`. Uses `__basic_zp_start`/`__basic_zp_size` from the linker script, so it adapts per platform automatically. |
| `init-mmu.o` | C128 only — programs the MMU before CRT init. |
| `init-stack-memtop.o` | VIC-20 only — derives the soft stack top from KERNAL MEMTOP, since RAM size varies with cartridges. |

`commodore.ld` places imaginary registers in the BASIC zero page (`__rc0 = __basic_zp_start`), defines the `zp` region from `__rc31 + 1` up to `__basic_zp_end`, force-links `basic-header.o`, aliases `c_readonly`/`c_writeable` to `ram`, and includes `c.ld`. A complete target therefore only needs to define `ram`, the BASIC ZP bounds, `__stack`, and `OUTPUT_FORMAT`.

---

## 3. Hardware register headers

The SDK models chips as `volatile` structs overlaid at their base address, with `static_assert` on `sizeof` to catch layout mistakes at compile time. Access is ordinary field access, which reads much better than POKE arithmetic and lets the compiler pick good addressing modes.

| Header | Chip |
|---|---|
| `_vic2.h` | VIC-II (C64) — `VIC` / `VICII` |
| `_vic.h` | VIC-I (VIC-20) |
| `_vic3.h`, `_vic4.h` | VIC-III / VIC-IV (MEGA65) — `VICIII` / `VICIV` |
| `_vdc.h` | 8563 VDC (C128 80-column) |
| `_sid.h` | SID — `SID1`…`SID4` on MEGA65 |
| `_6526.h` | CIA — `CIA1`, `CIA2` |
| `_6522.h` | VIA — `VIA1`, `VIA2` (VIC-20, CX16, PET) |
| `_6545.h`, `_6551.h`, `_pia.h` | PET CRTC, ACIA, PIA |
| `_dmagic.h` | MEGA65 DMAgic controller — `DMA` |
| `_45E100.h` | MEGA65 Ethernet — `ETHERNET` |

Fields carry Doxygen comments with register offsets, and bitfields are used where the hardware has them. Sprite registers are exposed both individually (`spr0_x`) and as an array of `{x, y}` via anonymous structs.

**These headers are `volatile`, which matters.** Two 6502 subtleties from the main skill apply directly here: the compiler avoids RMW instructions on volatile objects (so `VIC.border++` becomes load/inc/store), and indexed addressing can emit a spurious read one page below the target — so avoid pointer arithmetic that lands one page above a read-sensitive register.

---

## 4. Per-target notes

### C64

`ram` is $0801–$CFFF with BASIC unmapped, `__stack = 0xD000` (just below I/O). `c64.h` gives `VIC`, colour and joystick constants, and function-key codes. Output is a PRG: `OUTPUT_FORMAT { SHORT(ORIGIN(ram)) TRIM(ram) }`.

### C128

`init-mmu.o` runs at `.init.010` — before CRT init — mapping $4000–$BFFF to RAM and keeping KERNAL/chargen at $C000–$FFFF, then saves the previous MMU config for restoration. `_vdc.h` covers the 80-column VDC, which is accessed through its address/data register pair rather than a memory window.

### VIC-20

Soft stack top comes from KERNAL MEMTOP at runtime (`init-stack-memtop.o`) rather than a link-time constant, because usable RAM depends on which expansion is fitted. Keep this in mind if you write a custom script for a specific memory configuration.

### PET

Headers for the 6545 CRTC, 6551 ACIA, and PIA. No BASIC ROM unmapping — the PET memory map doesn't need it.

### Commander X16 (CX16)

`-mcpu=mosw65c02`, so 65C02 instructions (`bra`, `stz`, `phx`, indirect-no-index) are available; code written for it will not run on a stock 6502.

- **VERA** (`VERA` at $9F20, 32-byte struct, `static_assert`-checked) is the video chip. It's accessed through address/data ports, not a memory window — `vpeek.s`/`vpoke.s` wrap this, and there are helpers `vera_layer_enable`, `vera_sprites_enable`, `videomode.s`, `waitvsync.s`.
- **Extended KERNAL**: a large set of `cx16_k_*` wrappers covering the graph/framebuffer API (`graph_draw_line`, `graph_draw_rect`, `fb_set_pixels`, …), console, mouse, joystick, I2C, RTC, memory copy/fill/CRC/decompress, entropy, keymap, and sprites. Nearly all are `__attribute__((leaf))`. These live mostly as hand-written `.s` files — 68 of the 70 wrappers in `mos-platform/cx16/`. The reason is **convention translation, not a general preference for real functions over inline asm**: the X16 KERNAL's calling conventions frequently don't match the C ABI, and the `.s` files exist to bridge them. `cx16_k_console_put_char.s` turns an X-register flag into the carry with `cpx #1` and brackets the call with `X16_kernal_push_r6_r10`; `cx16_k_bsave.s` loads the end address out of `__rc4`/`__rc4+1` into X/Y and hands the KERNAL `#__rc2` as a zero-page pointer. Where the ABI *can't* express a result at all, cx16 uses inline asm instead — `cx16_k_joystick_get.c` returns three values simultaneously:

```c
__attribute__((leaf)) asm volatile("jsr __JOYSTICK_GET\n"
    : "=a"(s.data0), "=x"(s.data1), "=y"(s.detached)
    : "a"(joystick_num) : "p");
```

Pick by what needs bridging, not by how much assembly is involved — `inline-asm.md` §7 has the size measurements.
- **Banking**: `RAM_BANK` at $00 and `ROM_BANK` at $01 (zero page — note this differs from the C64's CPU port), with the banked window at `BANK_RAM` ($A000). `get_numbanks.s` reports available banks.
- CX16 uses a **non-contiguous imaginary register block**, which is why it ships its own `imag-regs.ld` and why `commodore.ld` skips the usual `__rc31 == 0x1f` assertion. If you write a custom CX16 script, preserve that.
- `NOTES.md` in the directory records open questions from the original author (e.g. whether `fb_*` should call through RAM vectors).

### MEGA65

`-mcpu=mos45gs02` unlocks the 45GS02: 32-bit `Q` register operations (`ldq`/`stq`/`adcq`/`aslq`/…), the `Z` register (`ldz`/`taz`/`tza`/`inz`/`dez`/`cpz`/`phz`/`plz`), flat 28-bit addressing via `[$nn],Z`, and the `MAP`/`EOM` instructions. Base memory map is $2001–$CFFF with BASIC unmapped via `unmap-basic.o` and `__stack = 0xD000`.

> **Before writing any MEGA65 assembly, read `45gs02.md` §2.** Z must be 0 whenever control is in compiled code, because the plain base-page indirect mode `(zp)` is literally the `(zp),Z` opcode — so every compiler-generated pointer dereference is Z-indexed. You may use Z freely in between, but `ldz #0` before handing control back is manual and unassisted: there is no `z` constraint, no `z` clobber, no automatic save/restore, and no diagnostic. Violating it corrupts memory program-wide with no crash at the site of the bug.

Key facilities:

- **`mega65.h`** overlays the whole I/O space: `VICII`/`VICIV` at $D000, `PALETTE` at $D100, four SIDs, `HYPERVISOR` at $D640, `DMA` at $D700, `MATH` at $D768, `ETHERNET` at $D6E0, `CIA1`/`CIA2`, plus `CPU_PORT`/`CPU_PORTDDR`.
- **`MATH`** ($D768, an 88-byte struct) is the hardware math unit — 32×32→64 multiply and divide. Because the inputs and result are separate MMIO registers, you need a compiler barrier between writing the operands and reading the result: `asm volatile("" ::: "memory")`. This is exactly the barrier case from `inline-asm.md`, and the SDK examples use it.
- **`dma.hpp`** (`namespace mega65::dma`, C++) builds DMAgic job structures for fill and copy and triggers them with `trigger_dma()`. DMA is dramatically faster than a CPU loop for screen and buffer work, and the header handles the F018A/F018B list format differences.
- **`_vic4.h`** covers VIC-IV: FCM (full-colour mode), RRB, palette selection, and the extended sprite/raster registers.

MEGA65 is also where the C64 headers come along for free (see §1), so `_vic2.h` bitfields work when you're driving the VIC-IV in a VIC-II-compatible mode.

---

## 5. PETSCII string literals

Rather than hand-encoding character codes, use the C++20 user-defined literals in `<charset.h>` (requires `-std=c++20`):

```cpp
#include <charset.h>
const char msg[] = U"HELLO WORLD"_u;   // unshifted PETSCII
const char low[] = U"hello world"_s;   // shifted PETSCII
const char scr[] = U"HELLO"_uv;        // unshifted *video* (screen RAM) codes
const char inv[] = U"HELLO"_urv;       // reverse video
```

The `U` prefix is required — translation happens at compile time from UTF-32 source literals. Variants: `_u`/`_s` (PETSCII), `_uv`/`_sv` (video/screen-code layout as in character ROM), `_urv`/`_srv` (reverse video). C0 control codes pass through uninterpreted, so `CH_*` constants still work inside these strings. If a character can't be mapped you get a compile error (`no matching literal operator`) rather than silent corruption.

The mappings follow the Unicode "Symbols For Legacy Computing" block, so box-drawing and graphics characters map correctly. CX16 additionally supports `_i` for ISO-8859-15 mode.

### The literal operators lose the length

Each is `template <charset_impl::…String S> constexpr auto operator""_uv() { return S.Str; }` — returning an array by `auto`, which **decays**. So the result is a pointer, not an array:

```cpp
static_assert(std::is_same_v<decltype("AB"_uv), const char *>);  // passes
static_assert(sizeof("AB"_uv) == 2);                             // passes: a pointer
```

That is fine for `cputs()`, and fatal if you need the length at compile time — to build a fixed-size table, emit a run-length, or size a `struct`. Note also that `strlen` is not a fallback for `_uv`/`_sv` output: `@` is screen code `0x00`, so a legitimate string can contain an embedded NUL.

**Use the underlying string type directly.** It is what the literal operator is built from, it keeps `N`, and taking the literal as `const char (&)[N]` deduces it:

```cpp
template <size_t N>
consteval auto encode(const char (&text)[N]) {
  charset_impl::UnshiftedVideoString<N> codes{text};   // N-1 chars plus NUL
  …                                                     // codes.Str[i] is the screen code
}
```

The constructors are `constexpr` and overloaded for `char`, `char16_t` and `char32_t`, so the `U` prefix is needed only when the source literal actually contains non-ASCII. Types: `UnshiftedString`, `ShiftedString`, `UnshiftedVideoString`, `ShiftedVideoString`, and the `…ReverseVideoString` pair.

**It also reports errors far better.** An unmappable character through the literal operator gives only:

```
error: no matching literal operator for call to 'operator""_uv'
```

because the header's `throw` makes the constructor non-constant, so template argument deduction fails and the real reason is never printed. Through the constructor, clang reports the throw itself with the `charset.h` line: *"use U prefix for unicode string literals"*, or *"Unsupported"* for a character with no mapping. Same rejection, and the difference between a fixable error and a puzzle.

Both routes work under **`-fno-exceptions`** — the `throw` is only ever constant-evaluated, and bad characters are still rejected at compile time.

---

## 6. Startup/shutdown hooks and `.init.NNN`

Commodore targets make heavy use of the priority-ordered init mechanism from `text-sections.ld`. A module-level `asm()` block placed in `.init.NNN` runs at startup in numeric order, before `main`:

```c
asm(".section .init.250,\"ax\",@progbits\n"
    "  jsr __late_init\n");
```

Observed slots in the SDK: `.init.005` (save BASIC ZP — must precede ROM unmapping), `.init.010` (bank switching / MMU setup), `.init.100` (stack init), `.init.250` (late init such as selecting the character set). `.fini.NNN` mirrors this for teardown.

If you add your own startup code, pick a number relative to these. Anything that must observe the pre-program machine state belongs below `.init.010`; anything that depends on RAM being banked in belongs above it.

To return cleanly to BASIC rather than hanging, link `save-basic.o` — it overrides the default looping `_Exit` and restores the zero page and stack pointer captured at `.init.005`.
