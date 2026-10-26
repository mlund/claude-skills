# Colour

Lightness is the salience channel and costs nothing. Hue is the category channel and is strictly
rationed — it signals category only while it stays scarce.

## The hue budget

- **One ground**, one **ink ramp** of ~4 steps, **one reserved category hue**, at most one more.
- The ink ramp is **lightness, not hue** — it is the salience channel and costs nothing from the
  budget. This is why a five-token palette spends only one hue.
- **At most two hues outside the ink ramp, deck-wide.**
- A third category is a structural problem. Split the slide, or move the distinction to
  **enclosure** — Gestalt common region is strong enough that a border overrides proximity and
  similarity, and it costs no hue.

## The ground inverts, it does not flip

Both grounds work; the room decides. Dark for a darkened theatre; light for a lit room,
screen-share, print or PDF export. Mechanical negation produces muddy mid-tones — invert instead:

| Token | Light ground | Dark ground (`#14161A`) |
|---|---|---|
| `ink` | `#16181D` (17.76:1) | `#F2F3F5` (16.31:1) |
| `body` | `#2E333B` (12.71:1) | `#C9CDD3` (11.35:1) |
| `low` | `#656C76` (5.30:1) | `#8A919B` (5.70:1) |
| `accent` | `#116A86` (6.12:1) | `#5BBBD6` (8.21:1) |

⚠️ Projection washes contrast out. Treat 4.5:1 as the floor for the **worst display in the room**,
not for the authoring monitor. Material that exports background PDFs needs both grounds specified.

⚠️ Ratios are measured for **these exact hexes**. Swap a hue and you must re-measure; an inherited
contrast figure beside a changed colour is a label that lies.

## Feedback colour — the trap

Correct/incorrect feedback invites green/red. Three reasons not to, in increasing order of
importance:

1. **Accessibility.** Red/green is the common colour-vision-deficiency confusion (~8% of men).
   **And contrast testing will not catch it:** `#15803D` measures 5.02:1 and `#B91C1C` measures
   6.47:1 — both pass WCAG 1.4.3 while failing 1.4.1. A scheme can be "accessible" by the metric
   most tools check and still be unreadable to the people it fails. A CVD-safe pair that also
   passes: blue `#175CD3` (5.99:1), orange `#B45309` (5.02:1).
2. **Channel orthogonality.** Correct/incorrect is a **state**, not a category. Two hues on a
   transient state exhausts the budget and makes the `keyword` hue ambiguous — the learner must
   work out whether a coloured word is a term or a verdict.
3. **Pedagogy, which should decide it.** Memory-area activity is *elevated* when learners guess
   **incorrectly**, with durable recall favouring surprising answers. The wrong answer is the
   highest-encoding moment in the material. Styling it as a red failure frames the best teaching
   moment as a penalty — and feeds hint abuse, because if being wrong is visually punished, the
   rational move is to extract the answer rather than think.

**Do this instead.** Carry the verdict in **icon, wording and position** — never hue alone, and
preferably not hue at all. If tinting, tint **both** states with the same neutral wash and let the
*content* differ: one says "yes, and here is why", the other "not quite — here is what is actually
happening". Reserve colour shifts for **resolved vs still open**, a progress state rather than a
verdict.

## Colour inside explorables

- A hue that **encodes a variable** earns its place. A hue that decorates is the **d = −0.05** case:
  it costs budget and returns nothing. The representational/decorational split applies to colour
  exactly as to motion.
- Colour-coding **is signalling**, so it inherits signalling's numbers (g = 0.43, k = 209)
  *including the expertise reversal*: heavy coding mildly hurts high-prior-knowledge learners
  (r = −0.08). Consider dialling it down on a revision pass through the same material.
- In a plot: **hue encodes series, lightness encodes magnitude.** Never assign both to different
  variables at once.
- ⚠️ Brom et al. (2018) found "pleasant colours **or** anthropomorphics" improved retention
  (d = 0.39). The review bundles colour with anthropomorphism, so it cannot be attributed to colour
  alone. Do not cite it as evidence that nicer palettes teach better.

## Accessibility floor

- **4.5:1** normal text; **3:1** for ≥18pt or ≥14pt bold.
- **Never encode meaning in hue alone** (WCAG 1.4.1). A `keyword` marked by colour must also carry
  weight, or it vanishes in greyscale and for colour-blind viewers.
- Prefer blue/orange to red/green wherever two things must be told apart.
- Colours that must be distinguished should differ in **lightness**, not only hue.
