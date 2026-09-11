# DMAgic

The fastest way to move bytes. Reaches the whole 28-bit space, including Attic RAM
and the full colour RAM.

| Addr | Name | Effect |
|---|---|---|
| `$D700` | `ADDRLSBTRIG` | List address bits 0–7 — **writing triggers the job** |
| `$D701` | `ADDRMSB` | List address bits 8–15 |
| `$D702` | `ADDRBANK` | List address bits 16–22 (bit 7 = `WITHIO`, unused). Writing clears `$D704` |
| `$D703` | — | bit 0 `EN018B` (F018B list format), bit 1 `NOMBWRAP` (no wrap at MB boundaries) |
| `$D704` | `ADDRMB` | List address bits 20–27 (overlaps `ADDRBANK`) |
| `$D705` | `ETRIG` | Trigger *enhanced* job, list at a 28-bit flat address |
| `$D706` | `ETRIGMAPD` | Trigger enhanced job, list read through the current CPU map |
| `$D707` | `ETRIGINLINE` | Trigger enhanced job whose list starts at the PC; PC resumes after it |
| `$D70E` | `ADDRLSB` | Set list address LSB **without** triggering |

Enhanced job-list option bytes (a `$00`-terminated prefix before the job). **An option
ID with bit 7 set consumes the byte after it; IDs below `$80` stand alone, and
unrecognised IDs are silently ignored** (`gs4510.vhdl:5873-5879`, `:5871`, `:5906`).
One wrong ID therefore desynchronises the rest of the list rather than failing.

**What a job costs.** Measured on hardware at 40 MHz by timing repeated jobs at
six sizes against the physical raster, so that a fixed cost can be separated
from a per-byte one:

| | fixed a job | a byte | throughput |
|---|---:|---:|---|
| copy | ~283 cycles | ~2.0 | ~19.6 MB/s |
| fill | ~102 cycles | ~1.1 | ~37.6 MB/s |

A fill has no source read. In this benchmark, near-memory-to-chip and
chip-to-chip copies measured the same. The fixed cost includes list construction
and triggering: setup accounts for about 82% of a 32-byte copy and 3% of a
4 KiB copy, using the table above.
The board/core revision and exact setup implementation were not recorded here;
these are workload-specific measurements, not hardware guarantees.

Measure several lengths and subtract a matched no-transfer control to separate
harness overhead, setup, and per-byte cost. Do not trigger a raw zero-length job
without checking its length encoding.

| Option | Arg | Meaning |
|---|---|---|
| `$00` | — | End of options |
| `$01` | — | Allow source and destination to cross megabyte boundaries |
| `$06` / `$07` | — | **Disable / enable** transparency — note the order, see below |
| `$0A` / `$0B` | — | Use F018A / F018B list format |
| `$0D` / `$0E` / `$0F` | — | Floppy raw flux write / read ignoring long gaps / read |
| `$10` | — | Sets a "SID mode" flag; behaviour unverified |
| `$53` | — | Sets a "draw spiral" flag, with a 40-column phase; behaviour unverified |
| `$80` / `$81` | `$xx` | Megabyte of source / destination address |
| `$82` / `$83` | `$xx` | Source skip rate: 256ths of a byte / whole bytes |
| `$84` / `$85` | `$xx` | Destination skip rate: 256ths / whole bytes |
| `$86` | `$xx` | The transparent value: bytes equal to `$xx` are not written |
| `$87`–`$8A` | `$xx` | Destination X and Y 8-pixel-boundary offsets (line mode) |
| `$8B`–`$8E` | `$xx` | Slope, and initial slope-accumulator fraction (line mode) |
| `$8F` | `$xx` | Line mode: b7 enable, b6 X-or-Y major, b5 negative slope, b4 scaling |
| `$90` | `$xx` | **Length bits 16–23** — transfers larger than 64 KB |
| `$91` / `$92` | `$xx` | Fractional part of the source / destination *address* |
| `$97`–`$9F` | `$xx` | The `$87`–`$8F` set again, for the **source** side |

`$87` upward come from `gs4510.vhdl:5832-5871`. Only `$00`–`$86` and `$90` reach
`iomap.txt`, so the usual grep does not find the rest — and `$91`/`$92` are annotated
in the VHDL yet still absent from the generated list, so a missing entry is not evidence that an option is absent. Verify option
semantics in the decode, including options listed in iomap.txt.

> **`$06` and `$07` are the other way round from their own documentation.** The core sets
> `use_transparent_value` to `'0'` for `$06` and `'1'` for `$07`, and the copy path
> skips a byte only when that flag is `'1'` (`:5888-5889`, `:9730-9736`). So `$07`
> enables transparency and `$06` disables it. The `@IO:` comment directly above that
> code says the opposite, and `iomap.txt` inherits the error.

**Strides are independent and fractional.** Source and destination each have their own
16-bit 8.8 fixed-point skip rate, defaulting to `$0100` (exactly 1.0) — `$82`/`$83` set
the source fraction and whole part, `$84`/`$85` the destination. `gs4510.vhdl` keeps two
separate address-update paths that read them independently. A strided fill is how you
recolour every other byte of a 16-bit-mode row in a single job.

**F018A vs F018B.** The two list formats differ by a sub-command byte, and which one
the hardware expects depends on the core/ROM combination. `$D703` bit 0 selects it;
the hypervisor trap `dmagic_autoset` (`$D642`, `A=$08`) sets it from the loaded ROM.
Enhanced jobs can pin the format per job with option `$0A`/`$0B`, which is the robust
choice. Getting this wrong produces jobs that transfer the wrong length or nothing.

**Options survive a chained job.** `dmagic_reset_options` runs only when the last job
in a chain finishes — both call sites sit inside the `dmagic_cmd(2)='0'` branch
(`:3844-3883`, `:6305-6312`, `:6774-6781`) — so megabytes, skip rates, transparency
and line mode leak into the next job unless it sets them again. Whether options are
parsed at all is fixed by which trigger register the CPU wrote (`:8935`, `:8954`),
and chaining re-enters the trigger state without changing it, so **every job in an
enhanced chain needs its own `$00`-terminated option prefix**, even an empty one. The
line-scaling accumulators are the exception: they reset per chained job (`:5778-5785`).

### Hardware line drawing

Options `$87`–`$8F` turn a fill into a line: `$87`/`$88` and `$89`/`$8A` give the
bytes to add to the address when crossing an 8-pixel boundary in X and Y, `$8B`–`$8E`
the slope and its starting fraction, `$8F` the mode bits. `$97`–`$9F` do the same for
the source address, which is how a texture is read along an arbitrary angle.

The core's comment block describing the intent (`:5820-5831`) states that this works
only in one-byte-per-pixel modes and assumes the VIC-IV 256-colour card layout — eight
consecutive bytes per row within each 8x8 cell. That is a source comment rather than
synthesised logic, and the address arithmetic has not been checked against it.

`$D710`–`$D71F` are **audio** DMA channels, unrelated to block copies.

Full job-list layout: `appendix-dmagic.tex`.
