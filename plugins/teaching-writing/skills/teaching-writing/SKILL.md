---
name: teaching-writing
description: Write lecture slides, self-study tutorials, notes pages, puzzles, hints and explorable captions that teach, in the style of Dill & Bromberg adapted for slides; distinguishes presented lectures from self-study material. Use when writing or revising teaching material (KEMM30, Blikfang decks, Quarto lecture notebooks) rather than papers; overrides the terse scientific-writing style for that material.
---

# Writing to teach

A paper is read by an expert who can reread; a lecture is met by a student seeing the idea
for the first time, often alone. Write for that student. The model is Dill & Bromberg's
*Molecular Driving Forces*: a simple model said plainly, every step shown, a number after
every formula, and what the number means.

Clarity rules from scientific writing still hold (lead with the point, active voice,
simple words, be quantitative, one term per concept, define symbols with units). What
changes is density: teaching material keeps the connecting steps and says key ideas more
than once.

## Before designing: ask about the target

Ask the author before planning slides, unless the request or earlier material already
answers it. Ask in one round, with a recommended answer for each:

1. **Format:** presented lecture, self-study tutorial, or both (see below).
2. **Students:** programme and year, and what they already know (which earlier courses or
   lectures this builds on).
3. **Maths:** what they can be assumed to handle: algebra only, derivatives and integrals,
   differential equations, vector calculus. This decides whether a derivation goes on the
   slide, in the notes, or is replaced by a physical argument.
4. **Level:** introductory, intermediate or advanced.
5. **Duration:** minutes per session and number of sessions (lecture), or expected study
   time (tutorial). This sets the size: roughly one slide per 2–3 minutes presented, and
   4–6 class quizzes per 90 minutes.
6. **Learning outcomes:** three to five, as checkable verbs ("estimate…", "explain why…",
   "rank…"). If the author has none, propose them from the topic and the course material
   and ask for approval. In a self-study tutorial the quizzes must cover exactly these
   outcomes; in a lecture the outcomes decide what each slide is for and which few
   points get a class quiz.

7. **Exercises:** which problems go with the material (textbook numbers, problem sets,
   exams), if any. Read them before planning. A student must be able to solve them after
   the lecture or tutorial, so every concept, formula, approximation and number they need
   must appear somewhere: on a slide, in the notes, or in a worked example of the same
   kind. Do not solve the exercises themselves on the slides; teach what they need.
8. **Other material:** what students already have: textbook chapters and pages, lecture
   notes, solutions, websites, videos. Read what you can. Follow the textbook's notation
   and sign conventions, cite chapters, equations and figures by number so students can
   look them up, and do not repeat at length what the book already does well; point to it
   and spend the slides on what the book lacks (the picture, the number, the interaction).
9. **Interactive figures:** should the material include explorables, figures the student
   drags and adjusts? If so, in which tool. Recommend Blikfang when it is available: its
   Rhai scenes give plots, draggable handles, sliders, heat maps and checkable state, and
   its MCP server lets Claude build and check slides directly (`run` with a picture). The
   alternatives are D3 explorables in Quarto/Jupyter, or static figures only. Ask which
   ideas deserve one: an explorable earns its place where the student varies one thing and
   watches another (a dependence, a geometry, a limit), not for a picture that never
   changes.

Record the answers (in the deck's notes or in memory) so later sessions use the same
target.

## Presented lecture or self-study tutorial

The same material needs different text depending on who does the explaining.

| | Presented lecture | Self-study tutorial |
|---|---|---|
| Who explains | the presenter, out loud | the text, alone |
| Slide text | cues: claim heading, key equation, one or two full sentences, a box | the whole explanation pattern below, on the page |
| Transitions | spoken | written: "So far…", "Next we ask…", "This matters because…" |
| Derivations | key steps on the slide, the rest in notes | every step on the page, split over slides if needed |
| Figures and explorables | presenter points and asks | caption says what to look at, what to do, and what it shows |
| Puzzles | discussed in the room | hints and feedback must carry the whole correction |
| Pace | one click per thing said | one slide per idea; a short recap after every few slides |

**Presented lecture.** Keep slides light and let the speaker talk; put the spoken
explanation in speaker notes or a notes page so the deck can be reused. Builds pace the
argument.

**Self-study tutorial.** Write what the presenter would have said. Every slide must stand
alone for a student with no one to ask:

- open each slide with one sentence that links it to the previous one;
- after each equation, write the sentences a lecturer would say: what each term is, why
  the step is taken, what the number means;
- anticipate the usual confusion and answer it on the page ("You might expect… but…");
- tell the student what to do with a figure before showing it, and what they should have
  seen afterwards;
- end each section with a recap and a check puzzle.

Expect a tutorial to have about twice as many slides as the lecture on the same topic, not
more text per slide. When one deck must serve both, write the lecture slides and add the
presenter's explanation as notes pages after each section.

## The explanation pattern (Dill & Bromberg)

For every idea, in this order:

1. **Picture first.** One or two sentences of what happens physically, before any symbol:
   "The water dipoles turn towards the ion and partly cancel its field."
2. **The model and its assumptions.** Name the simplification: "Treat the ion as a charged
   sphere in a uniform dielectric; ignore everything but electrostatics."
3. **The steps.** Show every step a student must take; do not jump. Say *why* a step is
   taken ("charge it in small bits, so each bit sees only the charge already there").
4. **Name the terms.** After an equation, say what each term is, with units.
5. **A number.** Put in real values: "560/4 ≈ 140 k_BT ≈ 350 kJ/mol".
6. **What it means.** One sentence turning the number into a physical conclusion: "so ions
   stay out of lipid bilayers". A number is never the end point.
7. **A limit or a check.** "With ε = 1 the energy vanishes: vacuum into vacuum costs
   nothing." Or compare with experiment.

## Slides vs notes

- **On the slide:** short, but full sentences that carry meaning; no telegraphic
  fragments that only make sense to the lecturer. At most about five lines of prose or
  five bullets, plus one display equation.
- **Notes pages** (Blikfang notes slide; Quarto `.notes` or an appendix): the full
  derivation in prose, paragraphs that open with their topic, every step written out,
  sources for numbers. A student who missed the lecture should learn it from the notes.
- Put a notes page after each section whose derivation does not fit on slides.

## Boxes: key concepts and take-home messages

- **Key concept box** on the slide where an idea is defined: one or two sentences, or the
  central equation with one line of meaning. At most one per slide.
- **Take-home box** at the end of each section: the one sentence a student should keep.
- In Blikfang: a `shape` rect card (`fill: surface`, `radius: 16`, a 3-unit border in a
  theme role; `accent` for take-home, `line` for key concepts) placed *before* the text,
  with the text inset 30 units. Start the text with a bold label: **Key concept** or
  **Take-home**.
- Boxes repeat what the slide says; that redundancy is the point.

## Headings

State the claim, not the topic: "Charging a sphere costs q²/8πε₀εa", not "Charging".

## Puzzles and hints

- Ask before telling: a prediction puzzle before the explanation or explorable.
- Each wrong choice option is a real misconception, and its hint names it ("That is a
  transfer energy; solvation starts in vacuum").
- Numeric and condition puzzles get a hint ladder: first where to look or which idea,
  then the step, then the numbers.
- `correct` feedback says *why* it is right in one sentence; `reveal` gives the answer
  and the reason.
- Speak to the student ("you"); keep each hint to one or two sentences.

### Quizzes differ by mode

- **Presented lecture: quizzes are for the class.** Short, quick prompts that start a
  discussion or a vote (think–pair–share), a few per lecture, placed where a misconception
  is likely. They never gate progress: no gating quiz, and no slide waits on a solved
  puzzle except to reveal its own answer. They need not cover every outcome; exercises do
  that.
- **Self-study tutorial: quizzes are the assessment.** Write the learning outcomes first,
  as checkable verbs ("estimate…", "rank…", "explain why…"). Every outcome gets at least one
  puzzle in its section and one in a closing quiz, on a new case rather than a repeat.
  Puzzles are more substantial (multi-step numbers, transfer to a new system), may gate the
  next section, and carry full hint ladders and reveals, since no one else will correct the
  student.

## Explorable captions (predict–observe–explain)

1. **Predict:** a question to answer before touching the figure.
2. **Do:** a concrete task ("drag the shell until the ion has 90 %").
3. **Notice:** what to look for and why it matters, revealed after the task is solved.

## Examples

Food first, then everyday life, then research or industry with a real number and a
source in the notes. Never invent a product, company or number.

## Layout cautions (Blikfang)

With Blikfang, read its MCP guides first (`lecture`, `design`, `scenes`, `deck`), prefer Rhai
scenes over JS explorables, and generate the deck from a script so it can be rebuilt.

Markdown renders past its frame, and puzzle hints and feedback render below the puzzle's
frame. Size frames for the rendered text, leave about 130 units free under every puzzle,
and check every slide with a picture.

## Verify before handing over

- Every slide checked with a picture: no text past its frame, room under every puzzle.
- Every equation followed by its terms, a number and what it means (on the slide or in the
  notes).
- Every explorable has predict, do and notice.
- Every wrong choice has a hint naming the misconception; every numeric puzzle a ladder.
- **Lecture:** quizzes are short class prompts and nothing gates progress.
- **Material:** notation matches the textbook, or the difference is stated once; chapters,
  equations and figures are cited by number.
- **Consistency across slides, notes and figures:** dump all text (slides, notes, hints,
  scene labels) and read it as one document. Each symbol means one thing and is written one
  way (also matching earlier lectures); each named quantity keeps one name; each material
  constant has one value, shown with the same rounding everywhere and matching the code that
  computes the figures; numbers recalled from earlier lectures match those lectures; every
  symbol is defined on or before its first use. Exercises may use slightly different
  notation; say once how it maps.
- **Exercises:** for each associated exercise, list the concepts, formulas and data it
  needs and where the material covers them; report any gap.
- **Tutorial:** list the outcomes and map each to its puzzles (section and closing quiz);
  report any outcome without a puzzle, and any puzzle that tests no outcome.
