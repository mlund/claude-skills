# Encoding and relocation changes

Use this reference for changes shared by the assembler, linker, and disassembler. Verify paths
and implementation details against the checked-out revision.

## Check every implementation

When changing operand encoding or resolution, check each consumer of the
convention:

1. **Encoder / fixups** — `MOSAsmBackend::applyFixup`,
   `getRelativeMOSPCCorrection`, `fixupNeedsRelaxationAdvanced`
2. **Relaxation** — `MOSAsmBackend::relaxInstructionTo` (returns 0 when a CPU
   has no wider form, which is how non-65CE02 targets keep 8-bit branches)
3. **Linker** — `lld/ELF/Arch/MOS.cpp` `relocate()`, one `case` per `R_MOS_*`
4. **Disassembly** — *both* `MOSMCInstrAnalysis::evaluateBranch` (the symbolic
   annotation) and `MOSInstPrinter::printBranchOperand` (the printed address)

Assembler- and linker-resolved operands must agree. Matching disassembly is not
independent proof: decoding errors can hide encoding errors. Check a specification
or execution on a matching CPU model.

## lld sees merged flags, not per-object ones

`MOS::calcEFlags()` ORs the `EF_MOS_ARCH_*` bits of every input, and
`checkEFlagsCompatibility` (`MOSFlags.cpp`) rejects only SWEET16/SPC700 mixes.
So any per-CPU decision inside `lld/ELF/Arch/MOS.cpp` is approximate: in a mixed
link both CPUs' bits are set. The assembler side has no such problem — it reads
the per-fragment `MCSubtargetInfo`.

Also note the arch bits are additive by design: a `mos4510` or `mos45gs02`
object also carries `EF_MOS_ARCH_65CE02` (asserted in `lld/test/ELF/basic-mos.s`),
so one bit test covers the family.

## TableGen operand metadata

- **Keep PC-relative operand metadata.** The AsmWriter emitter passes `Address` to a
  `PrintMethod` only when the operand's type is `MCOI::OPERAND_PCREL`. Retyping
  a PC-relative operand to a target-specific type silently changes the generated
  call to the 3-argument form and the build fails in `MOSGenAsmWriter.inc`.
- **Carry target-specific facts in TSFlags instead.** The pattern already exists:
  `bit MLow = 0; … let TSFlags{0} = MLow;` in `MOSInstrFormats.td`, with matching
  constants in the `MOS::TSFlag` enum in `MCTargetDesc/MOSMCTargetDesc.h`, read
  as `Desc.TSFlags & MOS::TSFlagX`. A
  `let Flag = 1 in { … }` block marks an instruction family without duplicating
  opcode lists.
- `MCInstPrinter` already holds `MII`, so a print method can consult
  `MII.get(MI->getOpcode())` for `TSFlags` and `getSize()`.
