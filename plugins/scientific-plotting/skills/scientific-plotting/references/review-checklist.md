# Figure review checklist

Use when critiquing an existing figure (yours or someone else's). Work top-down:
message first, then honesty, then perception, then production polish. For each
issue, name the problem, why it misleads or hinders, and the concrete fix.
Test it the acid-test way: **show it to someone unfamiliar with the data — can
they state the take-home message, and is it the one you intended?**

## 1. Message & purpose
- [ ] One clear take-home message; the figure delivers it at a glance.
- [ ] The chart type matches the task (comparison / relationship / distribution
      / composition) — see `chart-selection.md`.
- [ ] A figure is actually warranted (not better as text or a table).
- [ ] The most important comparison is the most visually salient thing.
- [ ] Appropriate to the medium (print vs. slide vs. poster) — not a paper figure
      dumped into a talk.

## 2. Honesty (does it mislead?)
- [ ] Bar charts start at zero; other axes' ranges represent the data faithfully
      (not chosen to inflate/hide an effect).
- [ ] Sized markers scaled by **area, not radius**.
- [ ] No dual y-axes, no 3-D for 2-D data, no pie chart used for comparison.
- [ ] Same measurement plotted on the same scale across panels.
- [ ] Uncertainty shown where it belongs; error bars **defined** (SD/SE/CI, level,
      replicates vs. samples). CIs preferred over SE and over p-value stars.
- [ ] Estimates shown as points (not bars); the inference of interest is plotted
      directly (e.g. the difference + CI).
- [ ] Raw data shown where feasible; distributions not hidden behind a mean±bar.
- [ ] Significant figures match measurement precision.

## 3. Perception & clarity
- [ ] Key quantity encoded by position/length, not angle/area/color.
- [ ] Data detectable: no defeating overplot; jitter/alpha/panels used as needed.
- [ ] Decluttered: no chartjunk, heavy gridlines, boxes, gratuitous color/3-D;
      high data-ink ratio.
- [ ] Light gray gridlines present if they'd aid value read-off.
- [ ] Direct labels where possible; legend only if necessary and not overlapping
      data.
- [ ] Every graphical element (symbol, line, color, band) defined.
- [ ] One encoding per variable (not color *and* shape redundantly, unless for
      grayscale robustness).

## 4. Color & accessibility
- [ ] Colormap type fits the data (sequential / diverging / qualitative); no
      rainbow/`jet`.
- [ ] Works in grayscale; color is redundant, not the sole encoding.
- [ ] Red/green not the only distinction; passes a colorblind simulation.
- [ ] Traces identified by label, not by color name in the caption.
- [ ] Text/background contrast adequate.

## 5. Text & typography
- [ ] Axis titles give **quantity + units**; dimensionless quantities carry no
      units (no "a.u." for absorbance).
- [ ] Notation correct: variables italic, unit symbols upright, space between
      number and unit; math (e.g. *f*(*x*)) set in math mode, not ASCII; real
      `−`/`×`/superscript glyphs; no `1e-3`-style tick litter.
- [ ] Sans-serif; ≤ 3 sizes; legible at final print size (≥ ~5–7 pt); tick labels
      1–2 pt smaller than titles.
- [ ] Labels horizontal (no rotated tick labels, no diagonal text).
- [ ] Consistent fonts/sizes/colors across **all** figures in the manuscript.

## 6. Caption (stands alone)
- [ ] Reads independently of the main text.
- [ ] Defines all symbols/traces/abbreviations and the error type.
- [ ] Gives conditions needed to understand the data (n, units, concentrations,
      temperature, etc.).
- [ ] Reused material credited with permission.

## 7. Production (pre-submission)
- [ ] Built at the journal's column width; caption fits the type area.
- [ ] Vector where possible; images ≥ 300 dpi at final size (check line-art dpi
      per journal); nothing upsampled.
- [ ] Correct file format; RGB; scale bars on micrographs; panel labels in the
      journal's style. (Full list in `journal-specs.md`.)
