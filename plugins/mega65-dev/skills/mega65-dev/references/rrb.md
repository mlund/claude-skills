# The Raster Rewrite Buffer

Composite layers without moving pixels: a screen row is a list of *instructions*
rather than a list of characters. Glyphs paint at the write position, which
advances 8 pixels a cell (16 in NCM), and a **GOTOX token** moves that position
somewhere else. A parallax layer therefore costs one number per row, and an
object costs a token plus its own cells — no background save and restore exists
to get wrong.

Everything below is `src/vhdl/viciv.vhdl` unless said otherwise. Where a claim
was measured rather than read, it says so and how.

---

## 1. The token

A token occupies a screen/colour cell pair like a glyph and paints nothing.

| field | where | note |
|---|---|---|
| it is a token | colour byte 0 bit 4 | `glyph_goto <= colourramdata(4)` (`:4404`) |
| X | screen byte 0, plus byte 1 bits 0–1 | ten bits, `glyph_number(9 downto 0)` (`:4828`) |
| Y offset | screen byte 1 bits 5–7 | `glyph_y_offset <= glyph_width_deduct(2 downto 0)` (`:4844`) |
| Y offset is negative | screen byte 1 bit 4 | `glyph_nve_y_offset <= glyph_number(12)` (`:4848`) |
| what follows composites | colour byte 0 bit 7 | `glyph_paint_background <= not glyph_flip_vertical` (`:4852`) |

**The X is the column itself.** `:4828` reads
`raster_buffer_write_address <= glyph_number - 1`, which looks like a bias to
pay for. It is not: each line starts with that address at all ones "so that it
wraps to zero at the start" (`:3421`), and the subtraction pays for *that*.

> **Measuring it, because reading either line alone gives the wrong answer.**
> Anchor on a cell **no token placed** — the first cell of a row is at column
> zero by construction. Put a second cell behind a token holding N: if it lands
> N columns on, the value is used as written.
>
> Two anchors that do *not* work. Comparing two tokened cells cancels the offset
> under test, since both move together — so a routine that blanks the row with a
> token first has measured nothing. And the border's edge is two pixels out of
> step with the character pixels, so where the display begins is not a reference
> either. Both were tried on hardware before the third worked.

**Why it hides.** Every layer goes through the same call, so a bias shifts the
whole picture together and looks correct. It shows only where a layer sits left
of the screen and relies on the wrap (§4), as a speckled column at the left edge.

**The Y offset is added to `glyph_number & chargen_y`**, so it runs into the
*next glyph number* rather than the tile below. It is smooth vertical scrolling
only where the tile below is the next number up. For genuine per-layer vertical
scroll, see ROWMASK (§5).

---

## 2. Colour byte 0 means different things on a glyph and on a token

This is the trap in the whole mechanism: the same bits are read twice with
different meanings, and nothing distinguishes them but bit 4.

| bit | on a glyph | on a **token** |
|---|---|---|
| 7 | flip vertically | what follows composites rather than painting background |
| 6 | flip horizontally | with bit 5: select the alternate palette |
| 5 | alpha | with bit 6: select the alternate palette |
| 4 | — | **this cell is a token** |
| 3 | NCM: 16 pixels wide, 4 bits each (`:4408`) | **ROWMASK enable** (`:4830`) |

**Bits 5+6 on a token select the alternate palette for every character that
follows on that line** (`:4841`). The core reads them for this specifically:

```vhdl
-- Get bold + reverse combination, even if not in VIC-III extended attribute
-- mode, so that we can check for it in GOTOX tokens.
glyph_bold_and_reverse <= colourramdata(5) and colourramdata(6);   -- :4591
```

That "even if not in extended attribute mode" matters. In full-colour mode with
attributes off, the *glyph* path forces bold and reverse to zero (`:4574-4576`)
so the colour byte can carry eight bits of colour — which reads as though the
alternate palette were unavailable. It is not; the token path has its own source.

**ROWMASK and the alternate palette are mutually exclusive on a token**, and the
core says why in a comment at `:4838-4841`: *"Moved here to fix a bug where
ROWMASK would still be able to select the alternate palette."*

Which palette the alternate is comes from `$D070` bits 1–0 (`:2901`, used at
`:3820`). There are four banks of 256; two are live at a time.

---

## 3. Ending a row

**A row displays only as far as the last pixel painted, not as far as the
highest.** `raster_buffer_max_write_address` is assigned unconditionally on every
painted pixel (`:5312`), so despite the name it holds the *last* position; the
character generator stops once the read address passes it (`:3370`). A layer
drawn further left therefore cuts the row short.

So every row must end with **a token near the right edge followed by a
character**. The token alone does not work — it moves the position and paints
nothing. Both idioms are in use and both work:

| | token X | trailing glyph |
|---|---|---|
| inside the screen | `width - 8` | one glyph, covering the last cell |
| off the right edge | `width` | one glyph, drawn entirely off-screen |

A transparent glyph still advances the write address (`:5310`, `:5316`) while
leaving what is under it alone, so the trailing cell need not paint anything.

---

## 4. Left of the screen

The write address is ten bits and **wraps**, so a layer scrolled part-way into a
tile is placed at a *negative* pixel — `0 - (scroll & 7)` masked to ten bits —
and the tile's right-hand pixels come out at the left edge. Horizontal scrolling
is therefore per pixel and needs no partial-tile art.

Give such a layer **one cell more than the screen is wide**: the shift that opens
a gap at the left opens the same gap at the right.

`$D07C` bit 3 `NORRBWRAP` disables the wrap (`:2963`); it is enabled at reset
(`:2138`).

---

## 5. ROWMASK: a per-raster-line mask

With bit 3 set on a **token**, colour byte 1 stops being a colour and becomes an
eight-bit mask, one bit per raster line of the character row:

```vhdl
screenline_draw_mask_drive <= colourramdata;                              -- :4584
draw_mask_blank <= not screenline_draw_mask(to_integer(chargen_y_hold));  -- :4458
```

**A set bit means the row is drawn**, so `$FF` shows all eight and `$00` none.

> **Book erratum.** `appendix-viciv-registers.tex` says "For each bit set in the
> row mask, the corresponding row of characters in the line will *not* be
> displayed" — the opposite polarity. The core is above; published examples agree
> with the core, starting their mask tables at `%11111111` for zero offset.

**What it is for: per-layer sub-tile vertical scrolling**, which the token's own
Y offset cannot give (§1). Emit the layer **twice at the same X** with
complementary masks, the second sourcing its tiles one map row further down. The
top part of each character row then shows one tile row and the bottom part the
next. It costs twice the cells for that layer.

The same trick places an object at an arbitrary Y: emit it into three character
rows, the first masked to the rows it covers, the middle unmasked, the last
masked to the complement — skipping the third when the offset is zero.

---

## 6. NCM, the four-bit cell

Bit 3 of colour byte 0 on a *glyph* makes the cell **16 pixels wide at 4 bits
each** — the same 64 bytes covering twice the width, which roughly halves both
the glyph count and the bytes a picture costs.

| nybble | paints |
|---|---|
| `$0` | the background — transparent under a compositing token |
| `$1`–`$E` | `(colour byte & $F0) or nybble` |
| `$F` | the *whole* colour byte |

- **The low nybble of a byte is the left pixel.**
- The bank is the colour byte's high nybble, chosen **per cell**, so 16 banks of
  the 256-entry palette — and the core comments the design intent at `:5284-5289`
  as *"This makes it much more useful for paralax layers etc"*.
- **It is 15 colours a cell, not 16, and only if the colour byte ends in `$F`.**
  Nybble `$F` takes the whole byte, and the bank is that byte's own high nybble,
  so `$F` lands back in the same bank at whatever the low nybble says. Colour a
  cell `bank << 4 | $F` and nybbles 1–F give `$x1`–`$xF`. Any other low nybble
  wastes `$F` on a duplicate and strands `$xF`.

The Book puts the same thing as "16 colours per character"
(`appendix-viciv-registers.tex:678`), counting the background as one of them.

**With alpha blending** (colour byte 0 bit 5 on a glyph) the nybble becomes an
alpha value instead, giving 15 levels between the background and the cell's
foreground colour — which is how anti-aliased proportional text is done, with the
token's X doing negative kerning between glyph pairs (`:709-710`).

---

## 7. Palettes: horizontal comes free, vertical costs a raster

There are four hardware banks of 256 colours; `$D070` chooses which the character
generator reads and which is the alternate (`:2901`). Two are live at a time.

**Across a line, use the cell.** An NCM cell's own colour byte picks its 16-entry
bank (§6), and a token picks between the two live palettes for what follows (§2).
Both are data the row already carries, so a layer or an object gets its own
palette at no cost in time, and it *travels with the object* as it scrolls.

**Down the screen, change `$D070` at a raster.** The palette lookup happens at
pixel output (`:3810-3825`), downstream of the raster buffer, so a write lands on
pixels after it. Reloading the bank — or DMA-ing fresh entries into the bank that
is not being displayed — gives each horizontal band of the screen its own 256
colours, which is how a picture exceeds 256 in total.

**Do not reach for raster timing to colour a moving object.** A mid-line change
applies to *every pixel after it on that line*, not to one object, so following a
sprite would mean recomputing the write's timing per line per frame — and
recolouring everything to its right. Horizontal variation is what the per-cell
bank is for.

Timing note: wait on the physical raster (`$D052`/`$D053`), not `$D011.7`, which
is the VIC-II raster's bit 8 and saturates inside the picture under V400
(`registers.md` §4).

---

## 8. Geometry and the fetch budget

The usual setup is V400 with `CHRYSCL = 0`, `NORRDEL` clear and `DBLRR` set
(`$D051` bits 7 and 6): each displayed row spans two physical rasters, which is
where the doubled character budget comes from. `CHRCOUNT` (`$D05E` plus two bits
of `$D063`) counts *cells*, and `LINESTEP` (`$D058`) counts bytes and applies to
colour RAM as well.

**A raster line has time to fetch a bounded number of cells, and past it the line
is cut short.** Tokens count as well as glyphs. Measured on one machine at V400
with DBLRR: 128 cells a row is clean, 170 loses the right-hand edge of the
busiest rows. **Cells are charged for `CHRCOUNT`, not for cells that carry
anything** — the VIC fetches every reserved cell of every row whether or not the
program wrote to it, so a layer that appears on one row is paid for on all of
them, and reserving generously costs the same as using it.

It is the VIC's own budget, not memory contention: leaving the CPU completely
idle for a frame gives the same cut.

---

## 9. What an emulator will not tell you

`xemu` models neither `raster_buffer_max_write_address` nor the per-line fetch
budget, so an unterminated row renders full width there and short on hardware,
and four full-width layers render perfectly there and are cut on a machine. It
takes a token's X raw. See `xemu-testing.md` §6.

A fault that *reproduces* under the emulator therefore cannot be caused by any of
those — which is the cheapest way to clear them as suspects.
