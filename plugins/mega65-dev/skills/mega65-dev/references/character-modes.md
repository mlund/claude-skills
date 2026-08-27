# Full-colour and four-bit character modes

What a *cell* is. How cells composite into layers is `rrb.md`; the two are
independent — these modes work with no RRB token in sight.

Both replace the C64 idea of "a bitmap of an 8×8 glyph plus a colour" with "a
glyph that carries its own pixels". A cell is 64 bytes either way; the modes
differ in how those bytes are cut up.

| | FCM | NCM |
|---|---|---|
| cell | 8×8, one byte a pixel | 16×8, one nybble a pixel |
| enabled by | `$D054` bits 1 and 2 | colour byte 0 bit 3, per cell |
| a pixel is | a palette index, 0–255 | an index into a 16-entry bank |
| costs | 64 bytes for 64 pixels | 64 bytes for 128 pixels |

---

## 1. Turning full-colour mode on

| register | bit | |
|---|---|---|
| `$D054` | 0 `CHR16` | 16-bit character numbers — two screen bytes a cell |
| `$D054` | 1 `FCLRLO` | full colour for character numbers ≤ `$FF` |
| `$D054` | 2 `FCLRHI` | full colour for character numbers > `$FF` |

**Set both `FCLR` bits.** They are independent, and with only `FCLRHI` any glyph
numbered under 256 stays one-bit-per-pixel — which is exactly the range the first
glyphs of a converted image land in, so the picture comes out with its first few
cells drawn as monochrome text.

Two neighbours in the same register that are easy to clear by accident. `VFAST`
(bit 6) is the 40.5 MHz mode and is set at entry; clearing it drops the machine
to 3.5 MHz, which is then the speed every later measurement is taken at.
`PALEMU` (bit 5) is scan-line emulation, which dims every other line — pleasant
on a CRT and half a picture's brightness otherwise. Write the register with every
bit stated rather than OR-ing into it.

**A glyph's number is its address.** Full-colour glyph data is read from 64 ×
the character number and never through the character pointer
(`viciv.vhdl:4464`), so numbering glyphs *is* laying them out in memory. Thirteen
bits of number puts the ceiling at the first 512 KB of chip RAM. Glyph 0 is
therefore the zero page — a cell that should draw nothing must point at 64 bytes
you own, not at 0.

---

## 2. The colour byte, and the bit that is documented three ways

In FCM the colour byte is a palette index, and `$00` and `$FF` are special:

- **`$00` is transparent** — it paints the background, which under a compositing
  RRB token means it leaves what is underneath alone.
- **`$FF` paints the cell's own foreground colour** from colour RAM, so one glyph
  of `$FF` pixels serves as ink in any colour. A font costs no palette entries
  and recolours per speaker for nothing.

**Eight bits of colour, two ways.** Either clear `$D031.5 ATTR`, or set VIC-II
multi-colour mode (`$D016` bit 4) and leave `ATTR` however you like. Only `ATTR`
set with multi-colour clear loses the top nybble to attributes — blink, reverse,
bold and underline — leaving four bits of index.

Measured on hardware, painting a cell whose colour byte is `$80` and asking the
pixel probe what came out:

| `ATTR` | multi-colour | index |
|---|---|---|
| clear | clear | **eight bits** |
| set | clear | **four** — top nybble is attributes |
| clear | set | eight bits |
| set | set | eight bits |

Both branches are in the core. Multi-colour is tested first and short-circuits
the attribute decode entirely (`viciv.vhdl:4594-4597`):

```vhdl
if multicolour_mode='1' then
  -- Multicolour + full colour mode + 16-bit char mode = simple 256 colour
  -- foreground colour selection from 2nd byte of colour RAM data
  glyph_colour_drive(7 downto 4) <= colourramdata(7 downto 4);
else
  if viciii_extended_attributes='1' then ...                     -- :4599
```

and the `ATTR`-clear route is `:4568`.

> **`iomap.txt` is the one to distrust here.** It calls the bit "Enable extended
> attributes and 8 bit colour entries", which reads as though *setting* it were
> how eight bits are had. In full-colour mode setting it alone does the opposite.
> The Book's account — that multi-colour mode activates the wide index — is
> correct and describes the other route.

The `ATTR`-off case is also what lets an RRB token select the alternate palette,
which needs bits 5 and 6 of colour byte 0 — see `rrb.md` §2.

---

## 3. NCM, the four-bit cell

Colour byte 0 bit 3 makes a cell **16 pixels wide at 4 bits each** — the same 64
bytes covering twice the width, which roughly halves both the glyph count and the
bytes a picture costs. On an RRB *token* the same bit means something else
entirely (`rrb.md` §5).

**The width is not paid for out of the height.** An NCM cell is **16×8** against
full colour's 8×8: 8 pixel rows either way, 64 bytes either way. Measured on core
v920413 by probing down a glyph whose row `r` is filled with `r+1` — eight
distinct rows, each two physical rasters under V400 with DBLRR, which is a
display setting that applies to FCM equally. The only thing NCM spends is colour
depth.

| nybble | paints |
|---|---|
| `$0` | the background — transparent under a compositing token |
| `$1`–`$E` | `(colour byte & $F0) or nybble` |
| `$F` | the *whole* colour byte |

- **The low nybble of a byte is the left pixel.** The core paints bits 3–0 then
  shifts right by four.
- The bank is the colour byte's high nybble, **chosen per cell** — 16 banks of
  the 256-entry palette. The core comments the intent at `:5284-5289`: *"This
  makes it much more useful for paralax layers etc"*.
- **It is 15 colours a cell, not 16, and only if the colour byte ends in `$F`.**
  `$F` takes the whole byte, and the bank is that byte's own high nybble, so `$F`
  lands back in the same bank at whatever the low nybble says. Colour a cell
  `bank << 4 | $F` and nybbles 1–F give `$x1`–`$xF`. Any other low nybble wastes
  `$F` on a duplicate and strands `$xF`. The Book counts the background and calls
  it 16.

**With alpha blending** (colour byte 0 bit 5 on a glyph) the nybble becomes an
alpha value instead, giving 15 levels between the background and the cell's
foreground — which is how anti-aliased proportional text is done, with an RRB
token's X supplying negative kerning between glyph pairs.

---

## 4. Palettes: across the screen it is free, down it costs a raster

There are four hardware banks of 256 colours; `$D070` chooses which the character
generator reads and which is the alternate (`viciv.vhdl:2901`). Two are live at
once.

**Across a line, use the cell.** An NCM cell's colour byte picks its own bank
(§3), and an RRB token picks between the two live palettes for everything after
it (`rrb.md` §2). Both are data the row already carries, so a layer or an object
gets its own palette at no cost in time — and it **travels with the object** as
that object scrolls, which no timed technique can do.

**Down the screen, change `$D070` at a raster.** The palette lookup happens at
pixel output (`viciv.vhdl:3810-3825`), downstream of the raster buffer, so a
write lands on pixels after it. Reloading the bank — or DMA-ing fresh entries
into the bank not being displayed — gives each horizontal band its own 256
colours, which is how a picture exceeds 256 in total.

**Do not reach for raster timing to colour a moving object.** A mid-line change
applies to *every pixel after it on that line*, not to one object: following a
sprite would mean recomputing the write's timing per line per frame, and
recolouring everything to its right. Horizontal variation is what the per-cell
bank is for; raster timing is for bands.

Wait on the physical raster (`$D052`/`$D053`), not `$D011.7` — that is the
VIC-II raster's bit 8 and saturates inside the picture under V400
(`registers.md` §4).

Writing the palette has two preconditions of its own: `$D030` bit 2 must be set
or colours 0–15 come from the palette ROM and never reach the bank being written,
and `$D070`'s two halves choose which bank the writes reach and which the display
reads — a machine that leaves them disagreeing shows the right picture in the
wrong colours. Hardware boots with `$FF` in `$D070` where an emulator has `$00`.
