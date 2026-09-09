# SDK platform integration

Use this reference when adding a target or debugging platform inheritance.

A platform normally supplies `CMakeLists.txt`, `clang.cfg`, and a linker script
for a complete target. Inspect a comparable platform and the checked-out SDK's
`platform()` implementation before copying its options.

## Check inheritance

- Parent configuration inclusion affects argument order. Inspect the driver's
  resolved command with `-###`; earlier search paths and later scalar options
  can win independently.
- Inspect `_merge_parent_library` and callers when adding platform libraries.
  Suffix-based ancestor merging can pull in objects unexpectedly. Check archive
  membership with `llvm-ar t` and link diagnostics rather than relying on a
  target's short name.
- Partial links and archives expose duplicate definitions differently. Test the
  complete target, not just successful archive creation.

## Verify the target

Check entry point, startup initialization, exit behavior, memory regions,
imaginary registers, soft stack, and emitted image format. Read
[linker-scripts.md](linker-scripts.md) for layout rules.

Compile and link a smoke test using a standard header as well as a platform
facility. Confirm the selected resource directory, builtins, and SDK libraries
belong to the intended installation. Do not update a shared installation as an
implicit part of diagnosing its configuration.
