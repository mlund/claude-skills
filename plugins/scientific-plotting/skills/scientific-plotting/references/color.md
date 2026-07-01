# Color and encoding

Color is the channel most often misused. Default rule of thumb: **"Is there a
reason this is blue and not black? If you don't know, keep it black."** Every
use of color should encode data or drive hierarchy — never decorate.

## Match the colormap to the data

| Data kind | Colormap | Example use |
|-----------|----------|-------------|
| Ordered, low→high, one natural extreme | **Sequential** (one hue, varying luminance) | concentration, density, p-value |
| Deviation around a meaningful midpoint | **Diverging** (two hues meeting at neutral) | log fold-change around 0, anomaly vs. mean |
| Discrete, unordered groups | **Qualitative** (distinct hues, similar luminance) | genotype, treatment arm |

- **Never use `jet`/rainbow** as a default. It has no perceptual ordering,
  introduces false luminance "bands" that invent features that aren't in the
  data, and hides detail (e.g. in high-frequency regions). Use a perceptually
  uniform sequential map (viridis, cividis, magma, or a single-hue ramp) instead.
- For sequential data, vary **luminance** (works in grayscale, survives
  colorblindness); don't rely on hue changes alone to encode magnitude.

## Encode magnitude with the right channel

Color hue/saturation is near the *bottom* of the perceptual-accuracy hierarchy
(see `chart-selection.md`). Use color for **identity/category**; use
**position/length** for quantities you want compared precisely. Only a limited
number of hues can be told apart in one figure — keep categorical palettes small
(≲ 6–8), and if you have more categories, reconsider the chart (small multiples,
direct labels).

## Accessibility (non-negotiable)

- **~8% of men (and ~0.5% of women) have red–green color vision deficiency.**
  Avoid red/green as the *only* distinction. If red/green is unavoidable, use
  strongly different luminance/tints **and** add a second channel (shape,
  texture, dash pattern, direct label).
- **Design so the figure survives grayscale.** Color should be a *redundant*
  encoding, not the sole one. Distinguish traces by line style / marker shape /
  direct labels as well as color, so a B&W printout or a colorblind reader loses
  nothing. (Except genuinely color-dependent figures like heatmaps, which should
  then use a luminance-varying map.)
- **Don't name traces only by color** in the caption ("the red curve") — a
  colorblind reader or a B&W reprint can't map it. Give each trace a
  letter/label on the figure.
- Keep **text–background contrast high** (aim ≥ 4.5:1); don't put colored text on
  colored backgrounds. Avoid stereotype-loaded palettes (pink/blue = gender).
- **Test** with a simulator (Coblis, Color Oracle) and by desaturating to gray
  before you finalize.

## Highlighting with color

The strongest use of color is **contrast for emphasis**: color the one series
that carries the message and leave the rest gray/black. Tufte's observation —
varying shades of gray often order quantities *better* than varying color, and
gray "recedes" so the highlighted data pops.

## Print reality

- Author art is **RGB**; print is **CMYK** and cannot reproduce the most
  saturated RGB blues/greens, and renders darker. Soft-proof CMYK before
  submitting to catch shifts (see `journal-specs.md`).
- ACS/Science/Nature no longer charge for online color, but the figure still must
  read correctly in grayscale for print/photocopy.
