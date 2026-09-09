# Build artifacts and inspection

Use this reference for driver configuration, LTO diagnostics, maps, and disassembly.

## Confirm the pipeline

Inspect the real command with `mos-<target>-clang -###`. SDK configuration files
include parents using `@mos-<parent>.cfg`: search-path order and last-value option
precedence are different concerns. Inspect resolved `-mcpu`, zero-page budget,
and tool paths rather than inferring them from one configuration file.
See Clang's `ToolChains/MOSToolchain.cpp` and the installed SDK configurations.

With LTO, `-c` can produce bitcode and `-S` can produce IR. A diagnostic build
with `-fno-lto -S` does not reproduce whole-program allocation or inlining.

## Choose the artifact

| Question | Input and tool |
|---|---|
| Final linked instructions | Retained post-LTO ELF with `llvm-objdump -d --print-imm-hex` |
| Allocated region sizes and addresses | Link map from the normal build, `-Wl,-Map,<file>` |
| ELF symbols and sizes | `llvm-nm --print-size --size-sort <elf>` |
| Bitcode symbols | `llvm-nm <bitcode>`; these are not final machine-code sizes |
| LTO assembly | Separate link invocation with `-Wl,--lto-emit-asm` |
| Raw instruction encodings | Textual byte values supplied to `llvm-mc -disassemble -triple mos --mcpu=<cpu>` |

Check format with `file`; naming a PRG `.elf` does not change its contents.
SDK `OUTPUT_FORMAT` can emit a platform image rather than ELF. A build system
may retain a companion ELF; verify it belongs to the same link.

`--lto-emit-asm` replaces normal link output with `<output>.lto.s` in the MOS
linker workflow. Use a separate output name and invocation; do not expect a
runnable image or map from that invocation. Check newly produced files so stale
artifacts cannot masquerade as successful output. Assembly describes codegen;
inspect the linked artifact for final layout and relocation effects.

`llvm-mc -disassemble` consumes textual encodings, not a PRG file directly.
Strip platform headers and distinguish data from code before decoding. Preserve
the intended CPU mode; wrapping raw bytes in an ELF without correct architecture
flags can yield plausible but incorrect decoding. See `llvm/test/MC/MOS/`
for accepted byte input and CPU spellings.

## Attribute a change

Check tool failures before filtering output. Locate loops by symbols and data
accesses, not one common immediate value. If a callee remains out of line, compare
the callee as well as its caller. Normalize shifted addresses when comparing
instruction sequences, but retain actual addresses for layout-sensitive bugs.

Generate symbol maps from each normal build. Map formats can vary: validate
required symbols, reject ambiguous matches, and fail on missing names. Do not
carry hand-copied addresses into emulator scripts.

Measure occupied regions and runtime memory separately from padded image size.
Use linker assertions for expressible layout invariants; add a map-based check
only where the linker cannot express the required condition.
