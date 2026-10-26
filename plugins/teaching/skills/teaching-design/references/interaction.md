# Interaction: puzzles, hints, gates, explorables

`teaching-writing` decides what a puzzle *says*. This decides how it *behaves*.

## Cadence: how often to ask

Interpolating a lecture with memory tests halved mind-wandering (19% of probes vs 39–41%), roughly
tripled note-taking (24% of slides vs 7–9%) and raised retention of the final segment to **84% vs
59%**. The segments were ~5 minutes.

So **4–6 class quizzes per 90 minutes is below what the evidence supports** — that is one every
15–22 minutes. Aim closer to one retrieval opportunity per 5–10 minutes.

⚠️ With one caveat that changes the design: that evidence is for **individual** retrieval, not class
discussion. Groups recalling together retrieve *less* than the same individuals pooled
(collaborative inhibition), though post-collaborative individual recall improves. So:

> **Individual commitment first, discussion second.**

This is independently the peer-instruction protocol (vote → discuss → revote) and the Interactive
Lecture Demonstration protocol (write a prediction → small-group discussion → observe). Three
traditions converging is not coincidence.

## Prediction format: free-form beats multiple choice

Interactive Lecture Demonstrations with **written open-ended predictions** produced ~80% conceptual
gain; the same demonstrations with five fixed clicker choices produced **59%** (and 57% vs 76% on a
second question). The author's own reading is that the paper version requires students to "provide
open-ended descriptions of their predictions" while the clicker version makes them choose from five.

- Prefer **free-form or sketch-based prediction** wherever the answer can be checked or
  self-assessed.
- Use multiple choice when the response genuinely cannot be parsed — and accept that it costs.
- ⚠️ This is a single non-randomised comparison in a conference proceeding. Strong hint, not a
  settled finding.

## Gates: this is Keller's PSI

Self-paced modular units with a mastery threshold before the next unlocks is the **Personalized
System of Instruction**, one of the better-evidenced designs in higher education: **~0.4–0.7 SD**
across meta-analyses of 75 and 108 studies, with **reduced variance** in outcomes and the largest
benefit for the **lowest-prior-attainment** students.

Two load-bearing details that are easy to omit:

1. **The gate is a gate, not a grade.** Repeated attempts without penalty. If failing costs marks,
   it is an exam and the PSI evidence no longer applies.
2. **The effect lives at the bottom of the distribution.** Reduced variance is the finding; design
   for the struggling student, not the median.

⚠️ Self-paced mastery's documented failure mode is **procrastination and non-completion** — courses
abandoning full self-pacing, instructor-paced variants cutting dropout. The intervention that moved
those numbers was **deadlines and pacing**, not progress visualisation. A map is a weaker lever than
a due date; offer both.

## Hints: the biggest risk in a gated design

**Gate + hint ladder + multiple choice is the hint-abuse setup.** The answer space is small enough
to brute-force and hints shorten the search. In tutoring-system research, no other off-task
behaviour is associated so strongly with reduced learning, and one analysis found 72% of actions
were unproductive help-seeking. Crucially, **interface design explained more of the variance than
student disposition** — this is a design problem, not a motivation problem.

Mitigations that the literature supports:

- Make hints **cost** something: a delay, a logged attempt, a required follow-up.
- Require a **fresh item** after a hinted success — do not pass on the hinted attempt.
- Prefer **free-form gate items**, which cannot be brute-forced. The spatial equivalent: a
  **continuous** handle judged by a check, not a few drop zones the student can try one by one.
- **Detect** rapid-hint sequences rather than trusting the pass.
- Never let `hint` be more attractive than `feedback`.

Do not remove hints; make gaming cost something. A detect-and-respond intervention reduced gaming
*and* improved learning for the students who gamed.

## Feedback is the teaching moment

Memory-area activity is **elevated when learners guess incorrectly**, and the durable recall
advantage goes to **surprising** answers. The wrong answer is the highest-encoding moment in the
material.

- Spend the real explanation **there**, ideally in the explorable, not in a minimal nudge to retry.
- **Compute the consequence of the answer given** where a script can: "Γ = +0.45: the positive
  area outweighs the negative, move up" teaches; "Not quite" does not. One rule then covers
  every wrong answer, including ones the author never foresaw.
- Draw that consequence for the **checked** answer, not the live control: a figure that updates
  as the student drags gives the answer away before they commit.
- This is also the anti-hint-abuse design: an explanation worth reading is not clicked past.
- Never style it as a red failure state (see `colour.md`).

## Explorables

**Guidance is not optional.** Unsupported exploration fails consistently: pure discovery loses to
guided discovery; simulation reviews find unsupported learners fail at hypothesis generation,
experiment design, data interpretation and self-regulation; minimising guidance clearly degrades
inquiry learning; and PhET's own research finds its simulations work only under an extensive set of
design constraints, with even small amounts of irrelevant information hurting.

So the primitive ships **with** its scaffolding:

- a prompt saying what to vary and what to watch,
- **bounded** parameter ranges,
- an interpretation scaffold (the "what should I have seen" step),
- an attached question.

The caption pattern stays **predict → do → notice** (`teaching-writing` owns the wording).

Two further constraints:

- **Represent, don't decorate.** Motion carrying the mechanism: d = 0.40. Motion decorating:
  d = −0.05, and the difference is significant (z = 3.86). The largest, highest-contrast,
  most-animated element must be the one whose change carries the concept.
- **Animation helps high-spatial-ability learners (d = 0.34) and does not help low (d = −0.16).**
  An explorable may widen the gap between students. Pair each with a **static summary state** that
  carries the same conclusion.

## Progress displays

A module map with completion marks is an **open learner model** supporting self-regulation — frame
it that way, not as gamification (only the cognitive effect of gamification survived rigour
filtering; motivational and behavioural effects were unstable).

- **Never award a tick for viewing. Only for passing.** A tick certifying *exposure* feeds the
  fluency illusion — familiarity mistaken for mastery, with judgments made right after study the
  most inflated of all. A tick backed by retrieval is a valid cue; retrieval is what corrects
  miscalibration.
- Ghost unearned items rather than hiding them. Curiosity requires **awareness of the gap**, so
  concealment suppresses the curiosity it is meant to create. Keep structure legible, obscure
  content.
- Curiosity is worth engineering: high-curiosity states improve memory for the target **and for
  incidental material** encountered during them.
- ⚠️ The progress mechanisms available (goal-gradient, endowed progress) come from **consumer
  loyalty-card field experiments**, not classrooms. Borrow the mechanism as a design hypothesis;
  do not cite as learning evidence.
