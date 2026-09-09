# Measuring application optimizations

Use this reference for code size and measured CPU hot paths. These are candidate
transformations, not guarantees about llvm-mos output.

## Establish the experiment

Record compiler/SDK revision, CPU, optimization and LTO flags, input, region being
measured, and the command used. Keep a runnable reproducer when recording a byte
or cycle figure. A result without those conditions should not become a skill rule.

Compare correct outputs before comparing cost. Measure the normal linked artifact
and inspect post-LTO code; source-level instruction counting misses allocation,
inlining, library calls, and layout effects.

## Candidates worth pricing

- Narrow values only when their range and arithmetic semantics permit it. Check
  promotions, signedness, overflow, and codegen; narrower source types can still
  change register allocation elsewhere.
- Compare parallel pointer walks with a shared index. A byte index may reduce live
  pointer state, but account for stride, bounds, wraparound, dynamic bases, and
  repeated field loads. Indexing does not require a link-time-constant base.
- Compare offset-pointer helpers with indexed accesses when pointer construction
  survives optimization. Do not assume that it survives inlining.
- Compare nearby store orders only when dependencies and hardware semantics permit
  reordering. Index-register movement and spills determine the benefit.
- Price structure-of-arrays against array-of-structures for the actual access
  pattern. Constant-stride addressing may become shifts, additions, or a helper
  call; inspect rather than assuming a multiply call.
- Give immutable local tables static storage when identity and lifetime permit it,
  then verify materialization and section retention. Automatic storage does not force the
  optimizer to emit a runtime copy, nor does LTO guarantee merging static objects.
- Compare lookup tables with arithmetic, including table bytes and access cost.
  Consider fixed-point only when its precision, range, and rounding meet the task.
- Inspect wrapper call sites before choosing inline assembly, an out-of-line
  function, or forced inlining. Smaller bodies and fewer clobbers can help, but
  duplication and caller spills may dominate.
- Avoid inventing global temporaries as a default optimization. Locals may remain
  in registers; globals can add observable stores. Likewise, a module boundary
  under LTO is not inherently expensive: price the interface and resulting code.

## Correctness limits

`nonreentrant` and `leaf` are promises, not optimization switches to try blindly;
read [abi.md](abi.md) before using them.

For deliberate halt loops, check the selected C/C++ standard and emitted code.
Do not label all constant infinite loops undefined across both languages.
An explicit compiler-supported volatile assembly loop can express a target halt.

After `longjmp`, modified non-volatile automatic locals in the function containing
the matching `setjmp` have indeterminate values. Do not rely on observed rollback
or optimization-level behavior.

Volatile accesses do not make multi-byte operations atomic or describe every bus
side effect. Check the exact CPU's indexed-access and read-modify-write behavior
for read-sensitive I/O.

Simulation measures the chosen CPU model, not DMA contention or raster deadlines.
Use [simulator-testing.md](simulator-testing.md) for compute probes and measure
display smoothness on an appropriate emulator or hardware.
