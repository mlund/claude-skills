---
name: teaching-design
description: >-
  Design and review how teaching material looks and behaves — text roles and
  salience, colour, progressive reveal, puzzles, hint ladders, mastery gates and
  explorables — grounded in multimedia-learning evidence. Use when laying out,
  styling or reviewing slides, explorables or quizzes (Blikfang decks, Quarto
  lectures, self-study tutorials), or when deciding how a puzzle, gate, hint or
  feedback should behave. Pairs with teaching-writing, which owns the prose.
---

# Designing material that teaches

`teaching-writing` decides **what the words say**. This skill decides **how they look and how the
interaction behaves**. Same deck, different question; use both.

Two findings govern almost everything here, and both are counterintuitive:

- **Attention is not comprehension.** Eye-tracking shows learners attend to on-screen text *at the
  expense of* the graphic, and more fixations often mean more strain, not more learning. Salience
  buys selection, not understanding.
- **The gain is in segmenting, not in handing over control.** Learner control meta-analyses at
  g ≈ 0.05. Breaking material into steps works; a scrubber and an "explore freely" canvas do not.

## Reference files

Read the one you need; do not load them all.

| File | Read it when |
|---|---|
| `references/text-roles.md` | assigning or styling text: the 18 roles, 4 tiers, the scale |
| `references/colour.md` | choosing a palette, a ground, or feedback colours |
| `references/interaction.md` | designing puzzles, hints, gates, feedback or explorables |
| `references/evidence.md` | you need the number, its *k*, its CI or its caveat |
| `references/review-checklist.md` | reviewing a deck, or wiring lint rules into a tool |

## Phase 1 — Decide (before anything is laid out)

### 1. The mode, because it changes the design

`teaching-writing` already splits presented lecture from self-study tutorial. That split is
**system-paced vs self-paced**, and the evidence makes it sharper than a stylistic preference:

- Replacing on-screen text with speech helps **only when system-paced** (d = 0.93) and is
  **eliminated when learners self-pace** — self-paced reading absorbs the overload.
- Design discipline matters **more in the lecture** than in the tutorial, which is the opposite of
  the usual intuition.

So the *same* content renders differently: `body` suppressed in a lecture because you are saying it,
full in a tutorial because nobody is. See the mode table in `references/text-roles.md`.

### 2. The salience budget

Contrast is zero-sum. Per slide: **exactly one** Tier 3 element (the claim, or the question — never
both), **at most ~3** Tier 2 marked elements, unlimited Tier 0–1.

### 3. The hue budget

Hue signals category only while hue is scarce. **One ground, one ink ramp (lightness, free), one
reserved category hue, at most one more.** A third category is a structural problem — split the
slide, or use enclosure, which costs no hue.

### 4. The ground

Dark for a darkened theatre; light for a lit room, screen-share, print or PDF export. The ramp
**inverts rather than flips**. If the material exports background PDFs, specify both grounds.

## Phase 2 — Build

### Assign roles, never fonts

Author text as a **role**; derive size, weight, colour and family from it. Roles let the tool
harvest keywords, suppress `body` by mode, and lint the budget — direct formatting cannot.

Keep the four channels orthogonal: **size+weight = salience · hue = category · italic = voice ·
family = register**. This is what prevents the collapse into bold-red-bigger-underlined.

⚠️ **The title trap.** `teaching-writing` says headings state the claim, not the topic — correct,
and the recalled-better evidence backs it. That makes the heading **load-bearing**, so it must be
Tier 3. A navigational label ("Module 3", "Results") is Tier 0 and should be small and faint. These
are two different roles; most slides carry only one.

### Reveal one step at a time

**Temporal contiguity is g = 0.78** — among the largest effects in this literature — and the
canonical example is one bullet at a time as the presenter talks to each. On-screen text also
suppresses *listening*; progressive reveal restores alternation between speaker and screen.

Default `item` to progressive reveal in lecture mode. Check both the initial view and the completed
slide.

### Put labels on the thing

**Spatial contiguity is g = 0.63.** Labels, value readouts and controls go **on or touching** their
referent — never in a legend or a side panel. Cheapest large win available.

### Explorables earn their place by representing

Animation that carries the mechanism: **d = 0.40**. Animation that decorates: **d = −0.05**, and the
difference is significant (z = 3.86). Make the largest, highest-contrast element the one whose
*change* carries the concept.

Two caveats the skill must always apply:
- **Guidance is not optional.** Unsupported exploration fails consistently (pure discovery,
  simulation reviews, PhET's own findings). Ship prompts, bounded ranges and an attached question
  *with* the explorable — not as something the author remembers to add.
- **Animation helps high-spatial-ability learners (d = 0.34) and does not help low (d = −0.16).**
  Pair every explorable with a static summary state.

### Puzzles, hints and gates

Full treatment in `references/interaction.md`. The three rules that matter most:

1. **Prefer free-form prediction to multiple choice.** Written open-ended predictions beat five
   fixed choices **80% vs 59%** on conceptual gain.
2. **A gate plus a hint ladder plus multiple choice is the hint-abuse setup** — the answer space is
   small enough to brute-force and hints shorten the search. Make hints cost something, require a
   *fresh* item after a hinted pass, and never let `hint` outshine `feedback`.
3. **The wrong answer is the highest-encoding moment.** Memory-area activity is elevated when
   learners guess wrong, with durable recall for surprising answers. Spend the explanation there —
   which is also the anti-hint-abuse design, since an explanation worth reading is not clicked past.

## Phase 3 — Review

Run `references/review-checklist.md` against the rendered deck. Never review from source alone:
contrast, overflow and reveal states are only visible rendered.

The four that catch the most:

- Any text under **4.5:1** (3:1 for ≥18pt or ≥14pt bold). Check Tier 0 and any greyed placeholder.
- A second Tier 3 element on a slide.
- A `callout` or label not adjacent to its referent.
- Feedback distinguished by hue alone.

## The core principles (one-screen summary)

1. Salience is a budget; spend it on load-bearing content only.
2. One job per channel.
3. Segment the content; do not hand over the pacing control.
4. Reveal in step with speech.
5. Labels on the thing, never in a legend.
6. Motion and colour must represent, or they cost and return nothing.
7. The mode changes the render; author once, render twice.
8. De-emphasise by size and weight before contrast, and stop at the floor.
9. The wrong answer is a teaching moment, not a failure state.
10. Guidance ships *with* the explorable, not after it.

## What the evidence will not support

Be honest about these; they are commonly assumed and do not hold.

- **Hard-to-read text aids learning** (disfluency). Failed to replicate across 13 experiments and
  >1,000 participants. Never style load-bearing text for difficulty.
- **Learner control helps.** g ≈ 0.05. Self-pacing is an access benefit, not a learning one.
- **Gamification motivates.** Only the *cognitive* effect survived methodological-rigour filtering;
  motivational and behavioural effects were unstable. Frame progress displays as an open learner
  model supporting self-regulation instead.
- **Interactive documents beat static ones.** Never tested head-to-head. ICAP is a theoretical
  ladder, not evidence for this claim.
- **Polling tools improve learning.** Their evidence is engagement and perception; the one
  exam-score study found no effect.

## Tools

With **Blikfang**, read its MCP guides (`lecture`, `design`, `scenes`, `deck`) first and prefer Rhai
scenes to JS explorables. Map roles onto its primitives rather than styling text directly, and check
every slide with a picture — markdown renders past its frame and puzzle hints render below the
puzzle's frame.
