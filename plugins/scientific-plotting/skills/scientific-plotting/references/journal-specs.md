# Journal figure specifications (production requirements)

> These are the mechanical requirements a figure must satisfy to survive
> production. They change over time and vary by journal — **always confirm
> against the target journal's current "Guide to Authors" / "Artwork
> guidelines" before final submission.** The numbers below are representative
> of Nature, Science, Cell and major chemistry (ACS) journals as of the source
> material and are good defaults when the specific journal is unknown.

## Width (the number that matters most)

Figures are almost always reduced to fit a fixed column grid. Design at the
final printed width so text and lines end up at the right size — never design
big and let production shrink your 12 pt labels to 4 pt.

| Layout        | Nature        | Science           | Cell            |
|---------------|---------------|-------------------|-----------------|
| Single column | 89 mm         | 85 mm (8.5 cm)    | 85 mm (8.5 cm)  |
| 1.5 column    | 120–136 mm    | —                 | 114 mm (11.4 cm)|
| Double / full | 183 mm        | 175 mm (17.5 cm)  | 174 mm (17.4 cm)|
| Max height    | 247 mm        | 240 mm (24 cm)    | (page-limited)  |

- **1 column ≈ 3.5 in (~9 cm); 2 columns ≈ 7.25 in (~18.3 cm)** is the general
  rule across most journals.
- Figure **and its legend/caption** must fit within the type area.
- Maximize the space given to data; avoid wasted white space and wide internal
  margins.

## Resolution

| Content type            | Typical requirement                        |
|-------------------------|--------------------------------------------|
| Line art (graphs, diagrams) | ≥ 300 dpi (Cell asks **1000 dpi**)     |
| Combination (line+photo)| ≥ 500 dpi (Cell: B&W 500 dpi)              |
| Halftone / photo / micrograph | 300–500 dpi at final print size       |

- dpi/ppi is meaningful **only at final print size**. 300 dpi at 2× size is
  150 dpi when placed.
- **Never upsample.** Artificially increasing resolution adds no detail and
  causes production problems. Re-export from the source at the right size.
- Vector art has no "dpi" — it stays sharp at any size. Prefer it (see below).

## File formats

Preference order, best first:

1. **Vector** — `.ai`, `.eps`, `.pdf`, `.svg` — for graphs, charts, diagrams,
   line art, illustrations. Scales losslessly; production can restyle it.
   - Making graphs in R → export **SVG** (or PDF).
   - ChemDraw / CorelDraw / Inkscape / Canvas → convert to PDF/EPS/PS.
2. **Layered raster** — `.psd`, `.tif` (or `.png`) — for photographs and
   imaging outputs (MRI, ultrasound, micrographs) that have no vector form.
3. **Avoid** JPEG for anything with text or line art — its compression
   smears edges. (Some journals reject JPEG/TIFF for *main* figures entirely.)

Submit **each figure as a separate file**, not embedded in the manuscript.

## Color mode

- **Author submits RGB.** Screens and the online "figure of record" are RGB.
- Print is **CMYK**; the journal converts. CMYK cannot reproduce the most
  vivid RGB colors (especially saturated blues/greens) and is darker — preview
  a CMYK soft-proof yourself to catch nasty shifts before submitting.
- Many journals no longer charge for color online; use it, but see
  `color-and-encoding.md` — color must still survive grayscale and colorblindness.

## Typography

- **Sans-serif only**: Arial or Helvetica are the safe defaults (Cell also
  lists Avenir; some journals set body text in their own face at production).
- **Minimum label size ≈ half the main text size**, and never below the
  journal floor. Practical floors: **5–7 pt** at final size; ACS advises
  designing at **≥ 18 pt originals** knowing figures get reduced. When in
  doubt, **aim for ~7 pt final and no smaller than 5 pt.**
- **At most 3 font sizes** in one figure, used to signal hierarchy
  (panel letter > axis title > tick label). Random size variation reads as
  sloppiness.
- **Panel labels**: Nature uses **lowercase bold a, b, c** (~8 pt); Science
  and Cell use **uppercase A, B, C**, upper-left of each panel. Follow the
  target journal.
- Keep text **live/editable** as long as possible; only outline fonts if the
  journal requires it. Do not rasterize text.

## Line weights

- **Minimum ~0.28 pt (~0.1 mm)** at final print size. Thinner lines drop out
  or break up in print.
- Use **even line weights**; avoid mixing hairline and heavy strokes
  arbitrarily.

## Building the file (production-friendly layers)

- Structure as layers: **base** = raster photo/scan (300 ppi); **mid** =
  vector graphics/arrows/illustration; **top** = vector text labels.
- Keep lines, arrows, and text over images on a **separate editable layer** so
  the journal can restyle without touching the image.
- **Do not flatten** layers or transparencies — production does that last.
- **Embed** linked images (don't leave them as external links) and **delete**
  hidden/off-canvas data; masked or hidden content can resurface in production.

## Micrographs and imaging

- Every micrograph needs a **readable scale bar**; state its length in the
  caption. Place scale bars consistently (e.g. bottom-right) across comparable
  panels.
- Don't paste instrument **screen dumps** — export the data and rebuild.

## Pre-submission checklist

- [ ] Built at exact final column width; caption fits the type area
- [ ] Files editable/vector where possible; images embedded, not linked
- [ ] Resolution meets spec **at print size** (300 dpi photos / 1000 dpi Cell line art)
- [ ] Fonts sans-serif, consistent, ≤ 3 sizes, ≥ 5–7 pt at final size
- [ ] Line weights ≥ 0.28 pt
- [ ] Color submitted RGB; checked to still work in grayscale and for colorblindness
- [ ] No red/green as the only distinction
- [ ] Scale bars on all micrographs; units on all axes
- [ ] Panel labels in the journal's style (a,b,c vs A,B,C)
- [ ] Each figure a separate file; nothing hidden/flattened
- [ ] For reused images: permissions obtained and credited
