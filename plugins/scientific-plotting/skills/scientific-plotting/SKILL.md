---
name: scientific-plotting
description: >-
  Design, create, and review plots and data visualizations for scientific
  journals. Use when making or critiquing a figure, chart, or graph for a paper,
  poster, or talk — choosing the chart type, encoding data faithfully, handling
  color/uncertainty/typography, or meeting journal artwork specs (size, DPI,
  fonts, formats for Nature/Science/Cell/ACS and similar).
---

# Scientific plotting

A figure is **a graphical interface between people and data** — not decoration
and not a data dump. It succeeds when a reader grasps the intended message
quickly and cannot be misled about what the data say. This skill covers the
whole arc: **design → create → review** for publication-quality scientific
figures.

## How to use this skill

1. Work through the phase(s) below that the task needs.
2. Pull the matching **reference file** for specifics (numbers, tables, edge
   cases) rather than guessing. The references are the authority; this file is
   the map.
3. When reviewing an existing figure, jump to `references/review-checklist.md`.
4. When preparing final files for submission, use `references/journal-specs.md`.

**Golden rule that dominates all others:** *message and honesty trump beauty.*
In science, a figure that is plain but truthful and clear beats a beautiful one
that misleads or obscures.

## Reference files

| File | Use it for |
|------|-----------|
| `references/chart-selection.md` | Choosing chart type by task; text/table/figure; the perceptual-accuracy hierarchy; what to avoid (pie, 3-D, dual-axis, radius-scaling). |
| `references/color.md` | Colormaps (sequential/diverging/qualitative), colorblindness, grayscale-safety, highlighting. |
| `references/design-principles.md` | Data-ink & chartjunk, gestalt, preattentive attributes, visual hierarchy, small multiples, layout, typography, defaults. |
| `references/statistics-and-uncertainty.md` | Showing raw data, points-not-bars, error bars/CIs, significant figures, axis honesty, units. |
| `references/journal-specs.md` | Size/width, DPI, fonts, line weights, file formats, color mode, panel labels, production checklist. |
| `references/review-checklist.md` | Structured critique of an existing figure. |

---

## Phase 1 — Design (decide before drawing)

Do this thinking *before* opening a plotting library. It prevents almost every
serious figure problem.

1. **Know the audience and medium.** Collaborators, a journal's broad
   readership, students, or the general public each need a different level of
   detail. A print figure (read at leisure, zoomable) differs from a slide
   (seen briefly, from afar — fewer elements, thicker lines, bigger text). Don't
   lift a paper figure straight into a talk.
2. **Identify the one message.** State, in a sentence, what the figure must make
   the reader see. **One main point per figure.** The message is the design
   brief for every later choice.
3. **Decide text vs. table vs. figure.** One or two numbers → text. Exact values
   / small sparse data / many look-ups → table. Patterns, trends, relationships,
   composition, or high density → figure. (`chart-selection.md`)
4. **Pick the chart type from the task**, not habit: comparison, relationship,
   distribution, or composition. Match the key quantity to the most accurate
   encoding available — **position/length beat angle/area/color**.
   (`chart-selection.md`)
5. **Sketch the layout** by hand — panels, what each carries, reading order —
   before producing anything.

## Phase 2 — Create (build it right)

**Don't trust the defaults.** Every library's defaults are "good enough for any
plot, best for none." Publication figures always need manual tuning.
(`references/design-principles.md`)

Encode honestly (`statistics-and-uncertainty.md`):
- **Show the raw data** where feasible; don't hide distributions behind a
  mean±bar. **Plot estimates as points, not bars.** Bars must start at zero.
- **Show uncertainty and say what it is** — SD, SE, or 95% CI (state which, and
  replicates vs. samples), in the caption. Prefer CIs over SE and over `*` stars.
  Plot the inference of interest (e.g. a difference + CI), not raw group means.
- No 3-D for 2-D data, no dual y-axes, no pie charts for comparison, no
  radius-scaled markers (scale by **area**). Same scale for the same measurement
  across panels. Significant figures match measurement precision.

Declutter and guide the eye (`design-principles.md`):
- Maximize data-ink; erase chartjunk (heavy gridlines, boxes, backgrounds, 3-D,
  gratuitous color). Light gray gridlines are fine and often help read-off.
- Make the key element **preattentively** pop (one channel — e.g. one colored
  series among gray). Use **small multiples** to split an overloaded plot.
- **Direct-label** series where possible; use a legend only for many repeated
  categories, and never let it overlap the data.

Color (`color.md`):
- Every use of color encodes something. If you can't say why it's colored, make
  it black/gray. Match colormap to data; **no rainbow/`jet`**.
- **Design grayscale-safe** and colorblind-safe: color is a *redundant* encoding
  (also vary line style / marker / label). Red/green must never be the only
  distinction. Test with a simulator.

Typography (`design-principles.md`, `journal-specs.md`):
- Sans-serif; size at **final print size** (≥ ~5–7 pt); ≤ 3 sizes; tick labels
  smaller than axis titles; text horizontal. Axis titles = **quantity + units**;
  dimensionless quantities carry no units (never "a.u." for absorbance).
- **Notation:** variables italic, unit symbols upright, a space between number
  and unit; set math (e.g. *f*(*x*)) in **math mode**, not literal ASCII, and use
  real `−`/`×`/superscript glyphs. Full SI/IUPAC rules in
  `statistics-and-uncertainty.md`.
- Keep every text/size/color choice **consistent across all figures** in the
  manuscript.

Write a **stand-alone caption**: it must be understandable without the main
text. Define every symbol, trace, color, and abbreviation; state the error type;
give conditions (n, units, concentrations, temperature) needed to read the data;
credit any reused material.

## Phase 3 — Review & finalize

- Run `references/review-checklist.md` top-down: message → honesty → perception
  → color/accessibility → text → caption → production.
- **The acid test:** show it to someone unfamiliar with the data. Can they state
  the message, and is it the one you intended? Which element do they look at
  first — is that the important one? You've seen the data too often to judge this
  yourself.
- Prepare submission files to the target journal's artwork spec — width, DPI,
  fonts, formats, color mode, panel-label style. (`references/journal-specs.md`)

---

## The core principles (one-screen summary)

1. **Know your audience and the medium.**
2. **Identify one clear message** — it drives every design choice.
3. **Captions are not optional** — the figure + caption must stand alone.
4. **Don't trust the defaults** — always tune.
5. **Use color effectively and accessibly** — purposeful, grayscale- and
   colorblind-safe, right colormap, no rainbow.
6. **Don't mislead** — zero-baseline bars, honest axes, area-not-radius, no
   3-D/pie/dual-axis, defined error bars, raw data shown.
7. **Encode for perception** — position/length over angle/area/color.
8. **Avoid chartjunk** — maximize data-ink; declutter.
9. **Message trumps beauty.**
10. **Use the right tool** and meet the journal's production spec.

## Tools

- **Generate** plots: Python/matplotlib, R (ggplot2 — better defaults than base
  R/Excel/SPSS), GraphPad Prism, D3.js (web/interactive).
- **Refine/assemble** final figures: Inkscape or Adobe Illustrator (vector);
  GIMP/Photoshop for raster/photographic layers. Assemble multi-panel figures at
  the exact final column width.
- **Specialized**: ChemDraw (structures), PyMOL (molecules), ImageJ/FIJI
  (microscopy), Cytoscape (networks), Circos (genomic/relational).
- Analysis tool and figure tool need not be the same — export data and plot in
  the tool that fits the figure.
