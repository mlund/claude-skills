# Toolchain verification

Use this reference for build identity, regression tests, runtime probes, and
bisection. Adapt coverage to the changed behavior.

## Build the tools actually used

After changing source or switching branches, rebuild the affected tools before
interpreting results. MC tests commonly need `llvm-mc` and `llvm-objdump`;
CodeGen tests need `llc`; linker tests also need `lld` and the utilities named in
their RUN lines. Inspect lit substitutions to establish the executable paths.
A missing utility is a setup failure, not a compiler regression.

LTO may execute the backend inside the linker or a plugin. Rebuilding standalone
`llc` does not update that component. Confirm source revision, executable paths,
and fresh output artifacts rather than trusting a version string alone.

An installation also includes Clang's resource directory, SDK libraries, and
builtins. Check `clang -print-resource-dir`; a major-version mismatch can appear
as a missing standard header. Include `<stdint.h>` or `<stdarg.h>` in installation
smoke tests. Use the project's install procedure in a separate prefix rather
than mixing compiler binaries and resource trees by hand.

## Check discovery and coverage

Use lit's test-listing facilities and final counts to confirm the requested tests
were discovered. Separate LLVM and lld invocations can simplify configuration
diagnosis; do not assume a mixed invocation either includes or drops a suite.

| Changed behavior | Useful coverage |
|---|---|
| Encoding or parsing | MC accepted/rejected forms and raw bytes |
| PC-relative convention | Same-section fixup, cross-section linker relocation, printed and annotated target |
| Code generation | Focused MIR/IR regression and a full-pipeline case |
| Register or layout contract | Pressure boundaries, calls, spills, compatible and incompatible layouts |
| Executed semantics | Self-checking probe on a matching simulator or machine |

For linker-resolved branches, place the target in another section and inspect
the relocation. Existing `lld/test/ELF/mos-relocs.s` also demonstrates
`-mos-force-pcrel-reloc` where supported.

A `-run-pass` or `-start-before` test bypasses earlier work. New register classes
or operand kinds need a full-pipeline case to catch legalization, cost-model,
allocation, and expansion interactions. Generated checks still need review
against the intended semantics.

## Runtime probes

Prefer failures that return a wrong result rather than crash: an off-by-one
branch probe can put an observable one-byte instruction just before the intended
target. Keep a bounded timeout because compiler regressions can still hang.

Follow the checked-out llvm-test-suite MOS conventions for directory gating,
`llvm_singlesource`, and reference output. Avoid unnecessary printing when it
would perturb the layout under test.

Before trusting `mos-sim`, inspect its usage, selected CPU mode, opcode coverage,
and timing implementation in SDK `utils/sim/`. Some Fake6502 versions map
unimplemented opcodes to NOP handlers instead of trapping. Neither successful
exit nor absence of an illegal-opcode error establishes instruction support.
Classify failures using a trace and known-supported probes; do not assume every
hang is a compiler bug or every unexpected result is a simulator gap.

## Differential runs and bisection

Compare known-good and candidate toolchains in separate build/install prefixes.
Point each test configuration explicitly at its compiler, linker, libraries,
and simulator. Keep the source, inputs, and flags fixed; record revisions and
artifact hashes. Do not swap binaries into the user's shared installation.

A cross-CPU sweep is useful only if both compiler and simulator support each
selected CPU. Check whether the local llvm-test-suite cache actually provides a
`MOS_CPU` option and how it configures both tools. Put required `-D` definitions
before a `-C` cache script that consumes them.

When tool binaries change, force regeneration of affected test artifacts through
the build system or use a fresh test-build directory. External tool changes may
not appear in the build dependency graph.

For layout-sensitive failures, vary `-mlto-zp` within the platform's valid budget,
keeping other inputs fixed. A threshold is evidence to investigate, not proof
that only one allocation changed. Compare maps and address-normalized code while
retaining actual addresses for the failing accesses.
