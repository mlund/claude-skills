# llvm-mos linker scripts

The format is GNU `ld` linker script → extended by LLD → extended by llvm-mos. When something isn't documented here, the `ld` manual is the base reference and LLD's implementation notes cover its deviations.

Contents:
1. Anatomy of a target script
2. MEMORY and region aliases
3. The `c.ld` section machinery
4. Imaginary registers and zero page
5. OUTPUT_FORMAT — building the binary
6. Optional runtime libraries
7. Banking
8. Sections that don't show up
9. Custom scripts on top of a platform target

---

## 1. Anatomy of a target script

A complete, working script for a hypothetical flat-64K machine:

```ld
MEMORY {
  ram           : ORIGIN = 0x0000, LENGTH = 0x10000   /* image written to file */
  user_ram (rw) : ORIGIN = 0x0200, LENGTH = 0xfe00    /* usable by code/data */
}

REGION_ALIAS("c_readonly", user_ram)
REGION_ALIAS("c_writeable", user_ram)

SECTIONS { INCLUDE c.ld }

__rc0 = 0x00;
INCLUDE imag-regs.ld
ASSERT(__rc0 == 0x00, "Inconsistent zero page map.")
ASSERT(__rc31 == 0x1f, "Inconsistent zero page map.")

__stack = 0;   /* top of soft stack; 0x10000 wraps to 0 */

OUTPUT_FORMAT { FULL(ram) SHORT(_start) }
```

Note the two overlapping regions. `user_ram` bounds where the linker may *place* things; `ram` describes the byte range to *emit*. Separating them is what lets `OUTPUT_FORMAT` dump a full 64K image while code is confined to a smaller window.

A real platform script layers: `c64/link.ld` sets `ram` and BASIC zero-page bounds, includes `commodore.ld` (which handles the BASIC header, imaginary registers, and `c.ld`), then supplies its own `OUTPUT_FORMAT`.

---

## 2. MEMORY and region aliases

`c.ld` places C sections into two names you must define:

- `c_readonly` — `.text`, `.rodata`, and the load images (LMA) of initialized data
- `c_writeable` — `.data`, `.bss`, `.noinit`

Point both at the same region on a RAM machine; split them on a ROM machine so initializers live in ROM and get copied at startup.

Region attributes (`(rw)`, `(rx)`, …) participate in automatic placement. `ORIGIN` and `LENGTH` accept expressions, including references to symbols you define — the SDK uses this heavily to size banks from user-set variables:

```ld
/* nes-mmc1/common.ld */
prg_ram_1 : ORIGIN = 0x016000, LENGTH = __prg_ram_size + __prg_nvram_size >= 16 ? 0x2000 : 0
```

`ASSERT(cond, "message")` is the way to reject impossible configurations at link time. Use it liberally — a clear link error beats a mystery at runtime.

---

## 3. The `c.ld` section machinery

`INCLUDE c.ld` pulls in, in order: `zp.ld`, `text.ld`, `rodata.ld`, `data.ld`, `bss.ld`, `noinit.ld`. Each is a thin wrapper — `text.ld` is literally:

```ld
.text : { INCLUDE text-sections.ld } >c_readonly
```

The `*-sections.ld` fragments hold the actual input-section patterns, so you can build a custom output section with the standard contents by including just the fragment. This is the supported extension point: define your own output section, `INCLUDE text-sections.ld` inside it, and assign it wherever you like.

`text-sections.ld` also builds the startup machinery. `_init`/`_start` sit at the top, followed by `KEEP(*(SORT_BY_INIT_PRIORITY(.init.* .init)))` — which is why a module-level `asm(".section .init.250,...")` block runs at a defined point during startup, ordered by the numeric suffix. `_fini` works the same way for teardown, and `__init_array_start`/`__end` bracket C++ constructors and `__attribute__((constructor))` pointers.

Useful symbols it defines for you: `__data_start`, `__data_end`, `__data_load_start`, `__data_size`, `__bss_start`, `__bss_end`, `__bss_size`, `__heap_start`.

---

## 4. Imaginary registers and zero page

```ld
__rc0 = 0x02;          /* wherever the first free ZP byte is */
INCLUDE imag-regs.ld
```

`imag-regs.ld` fills in `__rc1`–`__rc31`. Odd registers are hard assignments (`__rc1 = __rc0 + 1`) because each `__rsN` pair must be contiguous; even registers use `PROVIDE`, so you may override them to split the bank across non-contiguous zero-page holes:

```ld
__rc0 = 0x02;
__rc16 = 0x80;     /* jump the block over a ROM-reserved area */
INCLUDE imag-regs.ld
```

Only even registers may be relocated this way, and the split must land on even boundaries.

Separately, declare general zero page for the compiler's own allocation with a `zp` memory region:

```ld
MEMORY { zp : ORIGIN = __rc31 + 1, LENGTH = 0x90 - (__rc31 + 1) }
```

and tell the compiler how much is available via `-mlto-zp=<bytes>` in the target's `.cfg`. This only takes effect under LTO, because safe zero-page allocation needs a whole-program view.

`__stack` is the initial soft stack pointer, consumed by the `init-stack` library. The soft stack grows down, so set it to the top of the available window.

---

## 5. OUTPUT_FORMAT — building the binary

This is llvm-mos's most distinctive extension. It replaces `OUTPUT_FORMAT(binary)` with a small emitter script, letting you produce platform file formats with no post-processing tool.

```ld
OUTPUT_FORMAT {
  output-format-command
  ...
}
```

Commands run top to bottom, appending bytes:

- **`BYTE(expr)`, `SHORT(expr)`, `LONG(expr)`, `QUAD(expr)`** — emit little-endian values. Expressions can reference link-time symbols, so headers can carry real addresses and sizes.
- **`FULL(region [, start [, length]])`** — emit the region's loaded contents, padded with zeros to its full length.
- **`TRIM(region [, start [, length]])`** — same, but drop trailing unreferenced bytes.

A region's "contents" are the bytes of every output section whose **LMA** falls in it, positioned by LMA. A section doesn't need `>region` or `AT>region` to be included — overlapping LMAs suffice. `start` is relative to the region start, not an absolute address.

When `OUTPUT_FORMAT { }` is present, the primary output is these bytes and an additional `.elf` file is written alongside.

Real examples:

```ld
/* C64 PRG: 2-byte load address, then trimmed image */
OUTPUT_FORMAT { SHORT(ORIGIN(ram)) TRIM(ram) }

/* Atari XEX */
OUTPUT_FORMAT {
  SHORT(0xffff) SHORT(0x02e0) SHORT(0x02e1) SHORT(_start)
  SHORT(0x2000) SHORT(__data_end - 1) TRIM(main)
}

/* 6502 reset vectors at the end of a ROM image */
OUTPUT_FORMAT { FULL(rom) SHORT(nmi) SHORT(_start) SHORT(_irqbrk) }

/* Cartridge: a fixed stub repeated into every bank */
OUTPUT_FORMAT {
  FULL(fixed, 0, __bank0_fixed_size)  FULL(bank0, __bank0_fixed_size)
  FULL(fixed, 0, __bank1_fixed_size)  FULL(bank1, __bank1_fixed_size)
}
```

The last pattern is the idiom for "give each bank its own copy of the trampoline code": lay the shared code in one region, then emit slices of it interleaved with each bank.

---

## 6. Optional runtime libraries

The `common` target ships only what C strictly requires. The rest are opt-in:

| Library | Effect |
|---|---|
| `exit-loop` | `exit` runs `_fini`, then spins forever |
| `exit-return` | `exit` returns from `_start` to the caller/OS |
| `exit-custom` | you supply the exit routine (e.g. a `brk` into a monitor) |
| `init-stack` | initializes the soft stack pointer from `__stack` |

**How you opt in depends on which kind of target you're building, and neither route is `INPUT(...)` or a `-l` in the platform `.cfg`:**

- **A complete target** merges them into its own `crt0` archive at SDK *build* time, in CMake — not at link time:

  ```cmake
  add_platform_library(mega65-crt0)
  merge_libraries(mega65-crt0
    common-init-stack
    common-exit-loop
  )
  ```

  The result is that `mega65/lib/libcrt0.a` already contains them; there is no separate `libexit-loop.a` in a complete target's `lib/` directory, and no `-lexit-loop` anywhere in its `.cfg` or `link.ld`. Grepping the platform scripts for these names finds nothing — that's expected, not a sign you've missed something.

- **Building against an incomplete parent** directly is where the `-l` form applies, because `common/lib/` does ship `libexit-loop.a`, `libexit-return.a`, `libexit-custom.a` and `libinit-stack.a` as standalone archives:

  ```sh
  mos-common-clang -Os -o main main.c -lexit-loop -linit-stack
  ```

Without an exit library, returning from `main` falls off the end of `_start` into whatever follows. The canonical list of what's available is `common/crt0/exit/CMakeLists.txt` and `common/crt0/CMakeLists.txt`.

`INPUT(foo.o)` in a script force-links an object — how the Commodore scripts inject `basic-header.o` and `unmap-basic.o`.

---

## 7. Banking

There's no built-in bank switching; the pattern is to model each bank as its own memory region at a distinct linker address, then map those addresses to reality in `OUTPUT_FORMAT` and at runtime.

Give banks non-overlapping *linker* addresses even when they share a CPU window. The SDK uses the high bytes of the 32-bit VMA as a bank index (e.g. `0x01000000` for CHR-ROM bank 0), keeping every byte in a unique namespace so the linker can place and diagnose without knowing about the mapper. `OUTPUT_FORMAT` then emits regions in file order, and your runtime code is responsible for actually switching.

Place code into a bank with `__attribute__((section(".bank3")))` or a `.section` directive in asm, and assign that section to the region in `SECTIONS`.

---

## 8. Sections that don't show up

Two causes, and they can both apply:

1. **Not allocatable.** For non-standard section names in hand-written assembly, allocatable is not the default. Write `.section name,"a"` (add `x` for code: `"ax"`, `z` for zero page: `"az"`). Note that clang's `__attribute__((section(...)))` does emit `"a"` automatically — this bites in `.s` files, not in C.
2. **Garbage collected.** If nothing reachable references a symbol in the section, the linker drops it. Fix with the retain flag — `.section name,"aR"` — or `KEEP(*(name))` in the linker script.

The same mechanism is useful deliberately. Collection works per section, so a library of hand-written assembly routines sharing one `.section .text` is all-or-nothing: every target that calls one routine links them all. Give each entry point `.section .text.<name>,"ax",@progbits` and the unused ones drop. Check `--gc-sections` is on the link line first — the optimisation level does not imply it.

Data needs the same treatment, and the collection patterns already allow for it:

| section | pattern in the SDK's scripts |
|---|---|
| `.text.<name>` | `*(.text .text.*)` |
| `.bss.<name>` | `*(.bss .bss.* BSS COMMON)` |
| `.data.<name>` | `*(.data .data.* DATA)` |
| `.zp.bss.<name>` | `*(.zp.bss .zp.bss.*)` |
| `.zp.data.<name>` | `*(.zp.data .zp.data.* .zp.rodata .zp.rodata.*)` |

A scratch variable in a shared `.zp.bss` is retained by any reference to anything else in that section, and zero page is the one budget where a wasted byte is felt. Put a string or buffer used by exactly one routine inside that routine's section rather than a section of its own — a relocation from live code keeps it, and there is no separate name to maintain.

Section names are a linker-side concept only. They control collection, `--icf` folding and placement; they have nothing to do with inlining, which is settled during codegen. `-ffunction-sections` is already the default for C, so this is a concern for hand-written assembly alone.

---

## 9. Custom scripts on top of a platform target

Passing `-T custom.ld` to a complete target replaces the platform script rather than augmenting it, and a script without `OUTPUT_FORMAT { }` yields a plain ELF where the toolchain expected a flat binary. If a build suddenly produces ELF instead of a PRG/ROM, this is why.

Options, in order of preference:

1. **Don't.** Place data at fixed addresses using `__attribute__((section(...)))` plus a section assignment, or via pointer constants (`static uint8_t *const buf = (uint8_t *)0x2100;`) when you just need a known address.
2. **Copy the platform script** and edit it, keeping its `OUTPUT_FORMAT` block intact.
3. **Build a new complete target** parented to the platform's incomplete parent — the supported path when you're doing something structurally different, and the one to take if you plan to upstream it.
