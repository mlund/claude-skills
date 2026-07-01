# Design principles: decluttering, perception, layout, typography

## Data-ink: maximize signal, erase the rest

Tufte's **data-ink ratio** = ink showing non-redundant data ÷ total ink. Push it
toward 1 by iterating:

1. **Above all else, show the data.**
2. Maximize the data-ink ratio, *within reason*.
3. **Erase non-data-ink** — heavy gridlines, background fills, boxes/frames,
   redundant axes, 3-D shading, drop shadows.
4. **Erase redundant data-ink** — don't encode the same variable twice (e.g.
   both color *and* shape for the same grouping) without a reason.
5. **Revise and edit** — decluttering is iterative.

**Chartjunk** is any element that doesn't tell the reader something new: gratuitous
color, ornamental backgrounds, useless gridlines, moiré patterns, cutesy icons,
3-D effects. Remove it. (Exception: an element that's junk in one figure can be
justified in another — e.g. a light gray band to mark a reference range. If it
earns its ink, keep it and explain it in the caption.)

**Nuance on gridlines:** light *gray* gridlines aid accurate value read-off and
are often *missing* where they'd help; heavy/dark gridlines are chartjunk. Thin
and pale, or none.

## Perception: what the eye decodes well

- **Accuracy hierarchy** (Cleveland–McGill): position (common scale) > length >
  angle > area > color. Encode the key comparison with the most accurate channel
  available. (Full list and the pie/bubble/3-D consequences in
  `chart-selection.md`.)
- **Preattentive attributes** are read in < ~250 ms, before conscious attention:
  position, length, orientation, size, hue. Use exactly one to make the key
  element pop from its surroundings — a single red point among gray ones is found
  instantly; the same point among a rainbow is not.
- **Gestalt grouping** — the reader auto-groups elements that are *close*
  (proximity), *alike* (similarity: same color/shape = same category),
  *continuous*, *enclosed*, or *connected*. Use these deliberately to show which
  things belong together, and avoid accidental grouping (e.g. a legend swatch
  whose color also appears as an unrelated data color).

## Visual hierarchy and flow

A figure has a hierarchy whether you plan it or not: composition and emphasis
decide what the eye sees first, how it travels, where it lands. **Visual weight**
(driven by size, color, contrast, position, isolation) should match
**information relevance** — make the finding heavy, make scaffolding light.
Upper-left and center get seen first (in L-to-R reading cultures).

## Decluttering toolkit (when one chart is too busy)

- **Small multiples** — split an overloaded multi-series plot into a grid of
  simple panels, one series each, others ghosted faintly behind for context.
  Same footprint, far more readable; keep axes/scales identical across panels.
- **Filtering** — show only the series that carry the message; drop the rest.
- **Ordering** — order categories by value/meaning to make the pattern visible.
- **Highlighting / embedding** — color/bold the key series, gray the context.
- **Direct labeling** — put each series' label next to the series; a legend box
  forces a back-and-forth look-up and often overlaps the data. Use a legend only
  for 5+ repeated categories that can't be labeled in place.
- **Grouping / containment** — proximity or a light enclosure to bind related
  panels; align everything to an (invisible) grid.

## Layout and composition

- **Sketch the layout first** (by hand). Know the message, and which panel
  carries which part of it, before you place anything.
- **Align to a grid** using the software's align/distribute tools — never by eye.
  Every alignment reads as order; misalignment reads as clutter.
- Balance **white space** against ink; don't cram, but don't waste the data area
  with wide margins either. Maximize the space given to the data.
- **Panel alignment for comparison:** to compare along y, put panels **side by
  side with a shared y-axis**; to compare along x, **stack** them with a shared
  x-axis. Avoid arbitrary matrix layouts unless panels are unrelated.
- **Aspect ratio:** use **1:1** when the two axes are the same quantity
  (predicted vs. observed, before vs. after) so the y = x line is a true
  diagonal. Otherwise choose an aspect ratio that makes the relevant slopes
  readable (banking to ~45°). The "golden rectangle" (~1:1.6) is a pleasant
  default for a standalone plot. Never stretch/squash to fill a hole — it
  distorts slopes and text.

## Typography

- **Sans-serif** (Arial / Helvetica) for labels and anything small — it stays
  legible at reduction. Serif is only for long caption/text blocks.
- **Size at final print size.** Practical floor ~5–7 pt at printed size (≥ half
  the body-text size); design large and know your reduction factor, or design at
  the final width directly. Tick labels 1–2 pt smaller than axis titles.
- **≤ 3 font sizes** in a figure, used to signal hierarchy (panel letter > axis
  title > tick). Random size variation looks careless.
- **Keep text horizontal** (both axis titles readable without tilting the head
  where possible); never diagonal. Rotated y-tick labels (a common software
  default) hurt readability — fix them.
- Ensure the typeface distinguishes `1 l I` and `0 O`. Avoid ALL-CAPS blocks,
  excess italics, and color in text. Spell out contractions.

## Don't trust the defaults

Every library ships defaults tuned to be *acceptable for any plot and best for
none*: `jet` colormaps, gray backgrounds, absent or heavy gridlines, rotated
tick labels, 3-significant-digit ticks, overlapping legends, thin lines. **Every
publication figure needs manual tuning** away from defaults. `ggplot2`'s theme is
a better starting point than base R / Excel / SPSS defaults, but still tune it.
