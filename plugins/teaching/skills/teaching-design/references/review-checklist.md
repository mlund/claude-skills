# Review checklist

Run against the **rendered** deck, never source alone — contrast, overflow and reveal states are
only visible rendered. With Blikfang, check every slide with a picture.

## Procedure

1. **Render every slide**, in both its initial and completed reveal state.
2. **Walk the four high-yield checks** below first; they catch the most.
3. **Run the lint rules**; each is mechanical enough to automate.
4. **Report defects with the rule number and the slide**, not as general advice.

## The four that catch the most

| Check | Why |
|---|---|
| Any text under **4.5:1** (3:1 at ≥18pt or ≥14pt bold) | The usual failure is a greyed placeholder or a decorative colour reused on text. Nobody sets out to do it; nobody measures |
| A **second Tier 3** element on a slide | The salience budget is blown and nothing outranks anything |
| A `callout` or label **not adjacent** to its referent | Forfeits g = 0.63 for free |
| **Feedback distinguished by hue alone** | Fails CVD while passing contrast testing |

## Lint rules

**Salience and roles**

1. More than one Tier 3 element on a slide → **error**.
2. More than ~3 simultaneous Tier 2 elements → warning.
3. `emphasis` carrying colour as well as weight → warning.
4. An `assertion` that is a noun phrase ("Results", "Introduction") → warning: that is a `label`
   wearing the wrong role.
5. `body` below the contrast floor → **error**. Load-bearing text is never styled for difficulty.
6. More than two font families in a deck → warning.

**Contiguity and reveal**

7. `callout` not adjacent to a referent → **error**.
8. A list presented all-at-once in lecture mode → warning (temporal contiguity, g = 0.78).
9. A legend where labels could sit on the graphic → warning.

**Colour**

10. More than two hues outside the ink ramp, deck-wide → warning.
11. `feedback` states distinguished by hue alone → **error**.
12. Red and green used as a contrasting pair → warning.
13. A deck exporting background PDFs with only one ground specified → warning.
14. In an explorable, a hue not bound to a variable or a role → warning (decorational colour).
15. A contrast figure printed beside a colour that has since changed → **error** (a label that lies).

**Interaction**

16. A gate whose items are multiple choice **and** which offers a hint ladder → warning: the
    hint-abuse configuration. Require a fresh item after a hinted pass, or free-form items.
17. `hint` styled more prominently than `feedback` → warning.
18. A failed gate attempt that costs marks → **error**: a gate is a gate, not a grade.
19. An explorable with no prompt, no bounded range, no interpretation scaffold, or no attached
    question → **error** (guidance ships with the primitive).
20. An explorable with no static summary state → warning (animation does not help low-spatial-ability
    learners).
21. A progress tick awarded for viewing rather than passing → **error** (manufactures false
    confidence).
22. Fewer than one retrieval opportunity per ~10 minutes of lecture → warning.
23. A group/pair activity with no individual commitment step first → warning (collaborative
    inhibition).

**Rendering (Blikfang)**

24. Text rendering past its frame → **error**.
25. Less than ~130 units free under a puzzle → **error** (hints and feedback render below the frame).
26. A figure missing axis titles, tick labels or a legend at presentation size → **error**.

## Cross-skill checks

These belong to `teaching-writing` but surface during a visual review — flag and hand over:

- an equation with no terms named, no number and no meaning;
- an explorable caption missing predict, do or notice;
- a wrong-answer option whose hint does not name the misconception;
- notation inconsistent across slides, notes and figures.

## Reporting

State what is wrong, where, and the rule. Do not restate the rule's rationale unless asked — the
references hold it. If a defect recurs across many slides, report the pattern once with a count
rather than slide by slide.
