# Choosing the chart type

The chart type follows from **the task** — what relationship in the data you
want the reader to decode — not from habit or software defaults. First decide
whether a chart is even the right container.

## Text vs. table vs. figure

- **Text** — one or two numbers. Just write them in the sentence.
- **Table** — exact values matter, the dataset is small/sparse, or readers need
  to make many specific look-ups. Right-align numbers; align the quantities to
  be compared into columns (readers compare down a column more accurately than
  across a row).
- **Figure** — patterns, trends, relationships, or composition matter more than
  exact values, or the data density is too high for a table. (If precise values
  also matter, print them on the figure or give them elsewhere — readers cannot
  read a value off a bar.)

Keep the total figure count low. Main-text figures should carry the key results
that anchor the discussion; push characterization/supporting panels to SI.
(Some journals cap main-text figures — e.g. ACS *JPCL* at 5.)

## Task → chart

Ask: **"What do I want the reader to see?"** (Abela's decision tree.)

### Comparison of discrete quantities
- **Bar chart** — magnitudes across categories. Bars **must** start at zero (the
  bar length *is* the encoding; a truncated baseline lies). Order bars by value
  unless the categories have a natural order — don't default to alphabetical.
- **Dot/lollipop plot** — a better default than bars for many point estimates:
  same position-on-common-scale accuracy, far less ink, and no false zero-anchor
  implication. Ideal when the baseline isn't a meaningful zero.
- Use a **bar diagram, not an X–Y line plot**, when the x-axis is categorical
  (sample names, solvents): a line implies a continuous relationship that isn't
  there. An X–Y plot needs genuine causality/continuity between the axes.

### Relationship between continuous variables
- **Scatter plot** — two continuous variables. For overplotting, use
  transparency/alpha, small open symbols, jitter (for discrete pile-ups), 2-D
  density/hexbin, or contours. Add a **loess/smoother** to reveal the trend with
  minimal assumptions; add a confidence band only if it's relevant.
- **Line chart** — a continuous variable over an ordered dimension (usually
  time), or paired/repeated measures. The line asserts order/continuity — omit
  it for unordered data.
- **Scatterplot matrix (SPLOM) / correlogram** — many pairwise relationships in
  a larger dataset.
- **Bubble chart** — a third quantitative variable via size, small n only
  (< ~100). Encode by **area, not radius** (see below).

### Distribution (shape, spread, outliers)
- **Histogram** — one variable's distribution. Bin count changes the story;
  reasonable start: **≈ √N bins** (bin width ≈ range ÷ √N). Try several.
- **Boxplot** — median, quartiles, whiskers (default 1.5×IQR), outliers. Compact
  for comparing many groups. Caveat: readers often don't know the whisker rule —
  state it.
- **Violin / bean / strip / dot plot** — distribution shape *plus* the raw
  points. Prefer these over a bare boxplot when n is small enough to show points,
  so real structure (bimodality, gaps, n) isn't hidden.
- **Density plot** — smooth alternative to a histogram.

### Composition (parts of a whole)
- **Stacked bar** — total + composition. Only the bottom (baseline) segment sits
  on a common scale; the rest "float" and can't be compared accurately across
  bars. Use a **100%-normalized** stacked bar when only proportions matter.
- **Avoid pie charts** — they encode by angle/area (low on the accuracy
  hierarchy) and have low data density. A labelled bar/dot plot or a small table
  almost always beats a pie. Polar-area is a marginally better relative.

### Complex / many-condition data
- **Heatmap** — many conditions × features. Workflow: normalize → (optionally)
  cluster → color. Filter to the rows/columns that actually vary so the signal
  isn't buried. Use a **diverging** colormap when there's a meaningful midpoint
  (e.g. log fold-change around 0).

### Geographic
- **Maps** — powerful but distortion-prone; a choropleth conflates area with
  magnitude. Decide whether you're really showing geographic distribution or
  just proportions (which a bar chart shows more honestly).

## The perceptual-accuracy hierarchy (why the choices above)

Cleveland & McGill ranked how accurately people decode quantity from each visual
channel, most → least accurate:

1. **Position on a common scale** (aligned) ← best
2. Position on non-aligned scales
3. **Length**
4. Angle / slope
5. **Area**
6. Volume / density
7. **Color hue / saturation** ← worst for *quantity*

Steven's power law says the same thing: perceived magnitude scales as
intensityⁿ, and n < 1 for area (~0.7) and brightness (~0.5) — we systematically
*under*-perceive them — while length is ~linear. Consequences:

- Encode the quantity you most want compared with **position or length**.
- **Angle** (pie), **area** (bubbles, if radius-scaled) and **color** are poor
  for precise quantity — fine for identity/category, weak for magnitude.
- When you must use size, scale by **area, not radius/diameter** — radius-scaling
  a value of 30 vs 10 makes the disc look ~9× bigger, not 3×.
- Reserve **color hue** for categorical identity; use **luminance/saturation**
  (sequential) for ordered magnitude.

## Hard "don'ts"

- **No 3-D** for 2-D data — perspective distorts lengths/areas and occludes
  points. Use panels or color instead.
- **No dual/second y-axes** — the reader can't tell where the implied crossings
  are, and any relationship shown is an artifact of independent scaling. Use two
  aligned panels.
- **No radius-scaled** circles/areas (see above).
- **Don't connect points** with a line unless x is ordered and the line means
  something; a "guide to the eye" must be labelled as such. Show a trend line
  only with enough points (≳5) to justify it.
