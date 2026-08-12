# MAP and banking

How a 16-bit address becomes a 28-bit one, and how to design a banked layout.

Sources: MEGA65 Book `memory.tex` §"Using Memory from Machine Code" and
§"Advanced Memory Topics"; `mega65-core/src/vhdl/gs4510.vhdl` (the `MAP` opcode
handler, ~lines 3805–3835).

---

## 1. What the MAP register is

Eight 8 KB blocks of the 16-bit space. Each block is either **unmapped** (falls
through to cartridge / `$D030` / `$0001` / plain bank-0 RAM) or **mapped**, in which
case an offset is added to the 16-bit address.

There are only **two offsets**, one per half:

| Half | Covers | Blocks |
|---|---|---|
| MAPLO | `$0000`–`$7FFF` | `$0000` `$2000` `$4000` `$6000` |
| MAPHI | `$8000`–`$FFFF` | `$8000` `$A000` `$C000` `$E000` |

All mapped blocks in a half share that half's offset. The offset is a multiple of
`$100` and, in the base (4510-compatible) form, is 20 bits — enough for the first 1 MB.

```
16-bit address  +  offset  =  20-bit address
     $335F      +  $45200  =     $4855F
```

---

## 2. Encoding

Four bytes in four registers. **The register order is not the obvious one:**

| | High byte | Low byte |
|---|---|---|
| MAPLO | **X** = `$s o₁` | **A** = `$o₂ o₃` |
| MAPHI | **Z** = `$s o₁` | **Y** = `$o₂ o₃` |

- `s` — selection nibble, one bit per block, **high bit = highest block**.
  MAPLO `$2` = `%0010` selects only `$2000`–`$3FFF`.
  MAPHI `$B` = `%1011` selects `$E000`, `$A000`, `$8000`.
- `o₁o₂o₃` — the top three hex digits of the offset (offset = `$o₁o₂o₃00`).

```asm
        LDA #$52        ; MAPLO: select $2, offset $45200
        LDX #$24
        LDY #$00        ; MAPHI: select $B, offset $30000
        LDZ #$B3
        MAP
        EOM
```

Confirmed in `gs4510.vhdl`:

```vhdl
reg_offset_low <= reg_x(3 downto 0) & reg_a;
reg_map_low    <= std_logic_vector(reg_x(7 downto 4));
```

**Negative offsets.** Offset addition truncates at 20 bits, so a two's-complement
offset maps downwards. To bring `$8000` to `2.0000`, use offset `$FA000` (−`$06000`).

**`MAP` is `AUG` and `EOM` is `NOP`** in assemblers that do not know the mnemonics —
same opcodes (`$5C` and `$EA`).

---

## 3. Extended 28-bit MAP

The 45GS02 adds a **megabyte byte** per half, supplying address bits 20–27. It is
applied *after* the 20-bit offset addition, so a rollover in the low 20 bits does
**not** carry into it.

Set it with a *first* `MAP` that uses an escape value, then the ordinary `MAP`, then
`EOM`:

| To set | Put the megabyte byte in | Put the escape `$0F` in |
|---|---|---|
| MAPLO megabyte | **A** | **X** |
| MAPHI megabyte | **Y** | **Z** |

```asm
        ; map $A000-$BFFF to $8000000 (Attic RAM):
        ; megabyte byte $80, offset $F6000  ($A000 + $F6000 = $00000, 20-bit)
        LDA #$00
        LDX #$00
        LDY #$80        ; MAPHI megabyte = $80
        LDZ #$0F        ; escape: "this MAP sets the megabyte byte"
        MAP

        LDA #$00
        LDX #$00
        LDY #$60        ; MAPHI offset $F60xx
        LDZ #$2F        ; select $2 = $A000-$BFFF, offset high nibble $F
        MAP
        EOM
```

From `gs4510.vhdl`:

```vhdl
if reg_x = x"0f" then reg_mb_low  <= reg_a; else ... end if;
if reg_z = x"0f" then reg_mb_high <= reg_y; else ... end if;
```

Consequences of the escape being a value rather than a mode bit:

- **`X = $0F` (or `Z = $0F`) can never be an ordinary MAP setting.** That combination
  means "selection nibble `$0`, offset high nibble `$F`" — i.e. *no blocks selected*
  with a high offset nibble — which is a no-op anyway, so nothing useful is lost.
- **Megabyte bytes persist.** An ordinary single-`MAP` sequence does not clear them.
  They reset to zero on CPU reset and the KERNAL leaves them alone, so a freshly
  started program can normally assume zero — but a program that sets them must
  clear them before handing control back.

Zeroing everything:

```asm
        LDA #$00
        LDX #$0F        ; both megabyte bytes = $00
        LDY #$00
        LDZ #$0F
        MAP
        LDA #$00
        LDX #$00        ; both offsets and selection nibbles = 0
        LDY #$00
        LDZ #$00
        MAP
        EOM
```

---

## 4. Interrupts

`MAP` inhibits **all** interrupts, including NMI, until `EOM` executes.

The mechanism is a dedicated inhibit signal, **not** the I flag. In `gs4510.vhdl` the
`MAP` handler sets `map_interrupt_inhibit <= '1'` and `EOM` (`$EA`) clears it;
neither touches `flag_i`. The interrupt check reads:

```vhdl
if map_interrupt_inhibit='0' then
  -- NMI: edge triggered, gated only by the inhibit
  -- IRQ: additionally requires flag_i='0'
```

> **Book erratum.** `memory.tex` describes `MAP` as "similar to SEI" and `EOM` as
> "similar to CLI", and states that `EOM` re-enables interrupts *even if they were
> already disabled when `MAP` was called*. That is wrong for IRQ: `EOM` does not clear
> the I flag, so an `SEI` before the `MAP` still holds afterwards. It is right for
> **NMI**, which the I flag never masks — `EOM` does make NMI deliverable again.

Practical reading: `SEI` around a MAP sequence keeps IRQs off as you would expect, but
nothing you do with the I flag keeps NMI off across `EOM`.

Both the interrupt vectors at `$FFFA`–`$FFFF` and the handler addresses they point to
are subject to the map. If KERNAL interrupt handlers are to remain live, `$E000`–`$FFFF`
must be mapped to `3.E000`–`3.FFFF` (MAPHI offset `$30000`) whenever interrupts are enabled.

Any number of instructions may sit between `MAP` and `EOM`; they run with interrupts
inhibited.

---

## 5. Precedence and interaction

MAP overrides everything else. The other three mechanisms act **only on unmapped blocks**:

| Mechanism | Applies to | Notes |
|---|---|---|
| MAP | selected blocks | highest priority; the only case that returns early |
| `$D030` | unmapped blocks | ROM8/ROMA/ROMC/ROME → bank 2; overrides the cartridge |
| Cartridge ROM | unmapped blocks | C64 EXROM/GAME rules, including Ultimax |
| `$0001` | unmapped blocks | I/O at `$D000`; C64 ROM images |

`resolve_address_to_long` in `gs4510.vhdl` decides all four, and only the MAP case
returns a value; the rest overwrite one `temp_address` variable as the function runs, so
the mechanism appearing **latest in the source** wins. The Ultimax and cartridge
substitutions are at ~line 9225, the `$D030` ones at ~line 9253.

> **Wiki erratum.** The wiki's *Memory Mapping* page ranks `$D030` above `MAP` and
> `$0001` below it. `MAP` in fact overrides everything, `$D030` binds only where `MAP`
> did not, and `$0001` is lowest.

Two edges worth remembering:

- **`$0000`/`$0001` are the CPU port registers only while block 0 is unmapped.** Map
  block 0 with offset 0 and those two addresses become ordinary RAM — and the banking
  registers become unreachable. They are also **write-only**, so `TRB`/`TSB` do not work
  on them.
- **I/O disappears if you map over it.** Selecting `$C000`–`$DFFF` with offset 0 gives
  RAM at `$D000`, not registers, whatever `$0001` holds.

`$D030` bits (VIC-III banking, bank 2 sources):

| Bit | Name | 16-bit range | Reads from |
|---|---|---|---|
| 3 | ROM8 | `$8000`–`$9FFF` | `$28000`–`$29FFF` |
| 4 | ROMA | `$A000`–`$BFFF` | `$2A000`–`$2BFFF` |
| 5 | ROMC | `$C000`–`$CFFF` | `$2C000`–`$2CFFF` |
| 7 | ROME | `$E000`–`$FFFF` | `$2E000`–`$2FFFF` |

`$D030` boots as `$64` (ROMC enabled). It never banks in bank 3 — the KERNAL uses MAP
for its own code and `$D030` only for the interface routines at `2.C000`.

**It affects reads only, and nothing at all in hypervisor mode.** The substitution is
guarded by `writeP=false and hypervisor_mode='0'` (`gs4510.vhdl`, ~line 9253), so writes
to a banked-in region fall through to bank-0 RAM — the C64 shadowing behaviour — and
hypervisor code reads whatever the cartridge and `$0001` give it however `$D030` is set.

---

## 6. Reading the map back

**The MAP register cannot be read by any CPU instruction.** Two options:

- Keep a shadow copy in RAM, updated wherever the map changes. Cheap, but only as
  correct as your discipline.
- Ask the hypervisor: `hyppo_get_mapping`, trap `$74` at `$D640`, writes six bytes to
  a page you nominate in Y:

  ```asm
          LDY #$62        ; destination page $6200 (must be $00xx..$7Exx)
          LDA #$74
          STA $D640
          CLV
  ```

  | Offset | Type | Contents |
  |---|---|---|
  | 0 | word | MAPLO (**big-endian**) |
  | 2 | word | MAPHI (**big-endian**) |
  | 4 | byte | MAPLO megabyte byte |
  | 5 | byte | MAPHI megabyte byte |

  The mirror trap `hyppo_set_mapping` (`$76`) installs a map from the same structure.
  It offers no protection against mapping out the executing code.

For interactive debugging, the Matrix Mode debugger's `R` command prints `MAPL`/`MAPH`,
and `m777xxxx` displays memory **through** the current map (bank `777` is the CPU's
own 16-bit view). Plain `mxxxxxxx` always reads raw 28-bit addresses.

---

## 7. Constraints that shape a banking design

1. **Never remap the block containing the code that is executing.** The new map takes
   effect on the `MAP` instruction itself, before `EOM`. The bank-switch routine must
   live in a region that stays fixed. With the extended MAP this applies to the
   *32 KB half* whose megabyte byte you are changing.
2. **One offset per half.** All mapped blocks in `$0000`–`$7FFF` share an offset, and
   likewise for `$8000`–`$FFFF`. A layout needing two independent low-half windows is
   not expressible.
3. **KERNAL preconditions** (`kernal.md`): `$E000`–`$FFFF` → `3.E000`; `$0000`–`$1FFF`
   unmapped; base page register `B` = `$00`.
4. **Offsets are `$100`-granular**, not 8 KB-granular — a block can start anywhere on a
   256-byte boundary.
5. **The map is global state.** Interrupt handlers, KERNAL calls, and any library code
   see whatever map is current. Either keep a KERNAL-compatible map at all times, or
   own the interrupt vectors.

---

## 8. Choosing a mechanism

| Need | Use | Why |
|---|---|---|
| Execute code from another bank | **MAP** | The PC is 16-bit; only MAP can place far code in its reach |
| Read or write a handful of far bytes | **`LDA [$nn],Z`** | No map disturbance, no interrupt window, works from any context |
| Chase pointers into far memory | **`LDA [$nn],Z`** | 4-byte pointers address the whole 28-bit space directly |
| Move a block of data | **DMA** | Far faster than any CPU loop; reaches Attic RAM and colour RAM |
| Reach colour RAM above 2 KB | **28-bit or DMA** | It lives at `$FF80000`, outside the 1 MB MAP range without a megabyte byte |

28-bit addressing costs extra cycles per access but bypasses all four translation
layers, which makes routines using it composable — they behave the same whatever map
their caller installed. Prefer it unless you are executing code or doing enough
16-bit accesses to amortise the MAP setup.

---

## 9. A code-banking pattern

The shape that works on this hardware, independent of language or toolchain:

```
$0000-$1FFF   unmapped   ZP, stack, KERNAL variables
$2000-$7FFF   BANKED     24 KB window, MAPLO offset selects the bank
$8000-$CFFF   FIXED      resident code: bank-switch trampoline, IRQ handlers, hot code
$D000-$DFFF   unmapped   I/O
$E000-$FFFF   MAPHI      KERNAL ROM at offset $30000 (omit if you own the vectors)
```

Why this shape:

- The trampoline lives in the fixed half, so switching MAPLO never pulls the ground
  out from under it (constraint 1).
- `$0000`–`$1FFF` stays unmapped and `$E000`–`$FFFF` stays on the KERNAL, so KERNAL
  calls remain legal from either bank (constraint 3).
- Only MAPLO changes, so MAPHI's single-offset limitation never bites (constraint 2).

A far call becomes: save the current bank, set the new MAPLO, `JSR` into the window,
restore. The save/restore is a shadow variable — the map cannot be read back (§6).
Only the trampoline knows the map; banked code is written as if it always lives at
`$2000`–`$7FFF`.

Data-only banks are simpler: skip the trampoline entirely and use `[$nn],Z` or DMA.

---

## 10. Failure modes and what they look like

| Symptom | Likely cause |
|---|---|
| Machine hangs or runs garbage right at the `MAP` | Remapped the block holding the MAP code (§7.1) |
| Works until an interrupt fires | `$E000`–`$FFFF` not on the KERNAL, or vectors not installed |
| An NMI arrives during a "protected" section | `EOM` lifts the NMI inhibit; the I flag never masked NMI (§4) |
| Writes to `$D020` change RAM instead of the border | `$C000`–`$DFFF` mapped, so I/O is hidden (§5) |
| `$D030` writes do nothing | C64 I/O personality active (`memory-map.md` §4) |
| `$D030` banking ignored, or a knock has no effect | Running in hypervisor mode (§5, `memory-map.md` §4) |
| Address lands 1 MB away from expected | Stale megabyte byte from an earlier extended MAP (§3) |
| Restored map is wrong after a call | Shadow variable out of sync, or a callee changed the map (§6) |
