# Showing statistics, uncertainty, and raw data honestly

This is where scientific figures most often mislead — usually unintentionally,
via defaults. A survey of 97 graphs from top journals (Gordon & Finch 2015) rated
~40% *poor* and only ~30% good; **statistics journals were no better** than
applied-science ones. The failures below are the common ones.

## Show the raw data

- **Show individual data points whenever feasible** — overlaid on any summary.
  Summary statistics (mean ± bar) hide sample size, spread, outliers, bimodality,
  and clumping. A "dynamite plunger" bar with an error whisker is the worst
  offender: it hides everything and implies the bar length is the datum.
- For small/medium n: dot plot, strip plot, jittered points, or a violin/box with
  points overlaid. For large n where points overplot: transparency, hexbin,
  density, or contours.
- Use **jitter and/or transparency** for overlapping/discrete values so
  detection isn't defeated by pile-ups.

## Points, not bars, for estimates

- **Use points (dots) to plot estimates** — means, proportions, model
  predictions — not bars. A bar's length implies a count/magnitude anchored at
  zero; for a mean that anchor is arbitrary and the bar's fill is non-data-ink.
  (Statisticians use points ~100% of the time; applied scientists still use bars
  ~60% of the time — be a statistician here.)
- Attach uncertainty as an interval **around the point**.

## Uncertainty: say exactly what the interval is

- An error bar is meaningless unless the reader knows what it represents.
  **State in the caption** whether it is: SD, SE, a 95% CI (and that it's 95%), or
  range — and whether it's across replicate measurements of one sample or across
  independent samples.
- Prefer **confidence intervals over bare standard errors**; CIs map directly to
  the inference. Roughly, 95% CI ≈ 2 × SE for a mean.
- **Plot the inference of interest, not just group means.** If the finding is a
  difference, plot the *difference with its CI*, not two means the reader must
  subtract by eye.
- **CIs beat p-value stars.** A CI shows magnitude *and* precision; `*/**/***`
  shows neither. Avoid decorating plots with significance stars in place of
  effect sizes with intervals.
- Don't confuse a **confidence interval** (precision of an estimate) with a
  **prediction interval / SD** (spread of individuals). Show whichever answers
  the reader's question, and label it.
- If error bars are smaller than the plot symbols, **say so in the caption**
  rather than omitting them silently.

## When error bars can be omitted

Primary traces where the per-point error is inherently tiny — spectra, transient
absorption, cyclic voltammograms, chromatograms, TPD — conventionally omit error
bars. **Derived** quantities (rate constants, fitted parameters, averages) must
carry them. Get fit errors from the fitting routine; sanity-check them (vary
parameters and watch the fit); propagate errors for multi-measurement quantities.

## Don't mislead the reader (axis and encoding honesty)

- **Bar charts must start at zero** — the bar length is the encoding, so a
  truncated baseline exaggerates differences. For point/line plots of data that
  don't live near zero, a non-zero range is fine and often better (don't waste
  the plot on empty space) — but be aware truncated axes exaggerate small
  differences, so choose the range to represent the data faithfully, not to
  inflate an effect.
- **Auto-rescaling can lie** even when labelled — the most salient thing is the
  bar/line shape, not the tick numbers. Check that the *visual* impression
  matches the data.
- **Scale by area, not radius** for sized markers; **no dual y-axes**; **no 3-D**
  for 2-D data; **no pie charts** for comparison (all detailed in
  `chart-selection.md`).
- Use the **same scale for the same measurement** across panels so cross-panel
  comparison isn't distorted. Different scales are acceptable only when ranges
  differ drastically — flag it.

## Significant figures and units

- Don't carry meaningless precision: **match significant digits to measurement
  accuracy** (no `400.000 nm` wavelength ticks; no 4-digit sub-nanosecond
  lifetimes from a few-nanosecond pulse). Absolute zero is `0`, not `0.00`.
- Every axis needs a **quantity and units** (e.g. `Time (s)`, `Wavelength (nm)`);
  both `Wavelength (nm)` and `Wavelength / nm` are fine — be consistent across
  all figures. Ratios, fractions, log quantities (absorbance, pH) are
  **dimensionless — no units, and never "a.u." for absorbance.**
- Distinguish *arbitrary / relative / normalized* — they aren't interchangeable;
  define which in the caption. Include a y-scale (or scale bar) so the reader can
  judge magnitude.

## Standard, well-understood forms

Prefer histograms, dot plots, boxplots, line plots, scatterplots — readers decode
them without instruction. A novel chart form is fine only if it decodes *more*
accurately than the standard, and it must still obey the accuracy hierarchy and
be fully defined in the caption. **Define every graphical element** — 20–45% of
surveyed graphs left bars, symbols, or lines undefined.
