# Composition

How a slide is arranged, judged apart from what its words say. The rest of this skill asks *what
deserves attention*; this file asks whether the layout **delivers** it: whether the eye goes
where the salience budget says it should.

**Status of the evidence.** The Gestalt grouping principles (proximity, similarity, common
region, figure–ground) are robust perception findings (Palmer 1992, doi:10.1016/0010-0285(92)90014-s, on common region; Ware,
*Information Visualization: Perception for Design*). Their effect on *learning from slides* has not
been meta-analysed. The scores, ratios and spacing vocabularies below are design craft: useful
for a reviewer, not evidence. Do not quote them as findings.

## Two passes

Review in this order, and keep the passes apart.

1. **Don't read the slide.** Judge structure only: weight, alignment, grouping, whitespace, flow.
   The **thumbnail test** forces this: view the slide at about 1/8 size. If the hierarchy
   disappears when the words can no longer be read, the composition is weak.
2. **Now understand it.** List what the student should notice first, second and third (the
   semantic hierarchy), then compare it with what pass 1 said draws the eye (the visual hierarchy).

**The gap between the two passes is the main finding.** A polished slide whose most prominent
element is not its most important one is still badly designed. In this skill's terms, the
Tier 3 element must also be the strongest thing in pass 1.

## What to judge

| Dimension | Question | Typical failure |
|---|---|---|
| Hierarchy | First, second, third: obvious? | Several elements of equal weight |
| Alignment | Do edges, centres and baselines coincide on purpose? | Almost aligned |
| Grouping | Are related things close, and unrelated ones apart? | A caption nearer the wrong figure |
| Balance | Is the visual mass placed on purpose? (Balanced ≠ symmetrical) | A heavy cluster on one side |
| Whitespace | Is the empty space deliberate, and does it group things? | Every area filled |
| Grid | Does placement follow a small set of columns and rows? | Arbitrary x and y |
| Consistency | Do margins, gaps and treatments repeat, across slides too? | Gaps of 17, 19, 22 |
| Reading flow | Does the eye travel the argument's order? | The student hunts |
| Figure–ground | Does content stand clear of decoration? | Borders, boxes and icons compete |

A working heuristic for weight (not a law): **attention ≈ size × contrast × isolation × position ×
meaning**. Where the title, a big number, a picture and an accent all score high, the slide has
four focal points and a salience budget of one.

## Rules a reviewer can apply

- **Edge discipline.** Count the distinct left edges and tops. A slide with 12 elements on 4–6
  alignment lines reads as intended; one on 12 different lines reads as accidental. Treat a
  near miss (under ~1 % of the canvas) as a defect: snap it or move it clearly apart.
- **Spacing rhythm.** Use a few gaps, e.g. 8 / 16 / 32 / 64 (scaled to the canvas). Equal
  relationships get equal gaps, and different relationships visibly different ones.
- **Grouping by space before boxes.** Separate groups with whitespace first; a card (common
  region) only when space alone fails. Every border and box costs attention.
- **A series shares one layout.** Exercises in a series keep their figure, question and controls
  in the same places, so only the content changes and the student learns where to look once.
- **Titles anchor in one place** across the deck. A Tier 3 line that sits higher or lower from
  slide to slide reads as noise.
- **No stranded islands.** A lone small element far from everything else draws the eye for no
  reason; attach it to its referent or remove it.
- **Don't centre by default.** Left-aligned text with a figure beside it gives one strong edge;
  centring everything gives none.

## Layouts that change: render every state

A slide with a handle, a slider, a movie or a puzzle has **many layouts**, not one. Labels that
fit at the start collide at another state.

- Render the **extremes** of each control and the **last frame** of each motion. A movie's
  final frame can grow over a caption that cleared the first one.
- A readout that follows a moving element will collide somewhere. Give it a **fixed anchor**
  (a corner of the figure) or a fallback position, and check both.
- Feedback and hints grow **downward**, longest at the reveal. Budget for that space, and keep
  the correct-answer note to one sentence; put the detail in the figure or a callout.
- Draw the consequence of the **checked** answer, not of where the control sits now. Shading
  that follows a live handle answers the question before the student commits.

## Lines that wrap

- **Keep the Tier 3 line to one line** (about 40 characters at assertion size on a wide
  slide). Move qualifiers such as "this one takes some thought" into the body. A two-line question
  pushes into the figure below it and doubles the slide's heaviest element.
- **Leave about 10 % of the width spare.** Renderers wrap differently (an editor and a browser
  differ in font metrics). Text that just fits in one will wrap in the other.
- **Maths wraps at relation symbols.** A value with units mid-sentence
  ($\gamma = 0.025\ \mathrm{N\,m^{-1}}$) can break at the `=`. Put such expressions at the end of a
  sentence, or give them their own line.

## Reporting

Report **diagnosis + evidence + one prioritised fix**, not a single aesthetic score. Scores per
dimension (hierarchy, alignment, grouping, balance, whitespace, flow, consistency) may help
compare versions, but the actionable line is the primary issue and its fix:

> **Primary issue:** the plot and the takeaway compete for dominance.
> **Fix:** shrink the plot by ~15 % and open the space around the takeaway, rather than styling
> the takeaway more.

Prefer removing or moving over restyling. Most composition fixes are a smaller element, a shared
edge or more space, not a new colour or border.

## With element coordinates

When the tool gives frames as well as a picture (Blikfang's `read_slide` with `run`), measure
rather than eyeball: count distinct edges, list the gaps between neighbours, and check that the
Tier 3 element is the largest text. Use the picture for weight, balance and the thumbnail test,
which coordinates cannot show.
