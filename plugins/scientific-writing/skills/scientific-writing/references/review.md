# Review mode: parallel reviewers

A careful review runs every pass in §6 of SKILL.md, one concern per read. That
is slow done serially, and one reader tends to drift: the first pass anchors
the rest. Separate agents with narrow briefs each read the text fresh for one
kind of problem. The main agent then merges, dedupes, and resolves conflicts.

## Contents

1. When to fan out
2. Ask where to focus
3. Lanes
4. Sizing the load
5. Reviewer brief
6. Merging

## 1. When to fan out

Use review mode when the user asks for a review, critique, edit pass, or
pre-submission check of an existing text. Skip it when:

- **The text is short** (an abstract, a paragraph, under ~800 words). Run the
  §6 passes inline. Agents cost more than they find here.
- **The user wants a rewrite or a draft**, not a review. Write it; don't audit
  it.
- **The user named one concern** ("just check the passive voice"). One lane,
  inline or one agent.

## 2. Ask where to focus

Before launching, ask the user (with AskUserQuestion when available) unless the
request already answers it. One round, at most three questions, each with a
sensible default:

1. **Focus** (multi-select): which lanes to run (§3). Default: all lanes that
   fit the stage.
2. **Stage**: early draft, revision, or pre-submission. An early draft gets
   lanes A and D only. Polishing sentences that may be cut wastes the
   reader's time and the author's.
3. **Audience or venue**: specialist journal, broad journal (Nature, Science,
   PNAS), grant panel, thesis committee. This sets how hard lane A pushes on
   the opening and how much jargon lane C tolerates.

Also offer an optional free-text "anything else?" (a section the author
distrusts, a reviewer comment to address). If the user declines to answer,
use the defaults and say so in one line.

## 3. Lanes

Each lane maps to items in the §6 checklist. Lanes are chosen so that no two
reviewers report the same edit.

| Lane | §6 items | Reads | Why it is separate |
|---|---|---|---|
| **A. Structure & argument** | 1 message, 2 curiosity, 3 paragraphs, 4 flow | Whole text | Needs the global view; its findings can delete passages the other lanes would polish. |
| **B. Sentence mechanics** | 5 voice, 6 verbs, 7 simplicity, 8 conciseness | Whole text or a chunk | Local and mechanical; parallelises across sections. |
| **C. Precision & usage** | 9 specificity, 11 usage & consistency | Whole text | Term, acronym, and tense consistency only show up across the whole text. |
| **D. Claims & science** | 12 claims & tone, 10 theory exposition | Whole text + figures/tables if given | Judges whether the science supports the prose. Hardest lane; never chunk it. |

Item 10 belongs to lane D only when equations carry the argument; otherwise D
covers item 12 alone.

## 4. Sizing the load

Scale agents with length, but chunk only lane B. Lanes A, C, and D lose their
point if they see only part of the text.

| Text | Agents | Layout |
|---|---|---|
| < ~800 words | 0 | Inline (§1). |
| ~800–4000 words (letter, short paper, grant section) | 3–4 | One per lane. Merge B and C into one agent if the text is near the low end. |
| ~4000–10 000 words (full paper) | 4–5 | A, C, D whole; B split in two at a section boundary (e.g. Intro + Methods, Results + Discussion). |
| > 10 000 words (thesis, review article) | 5–6 | A, C, D whole; B split by chapter or major section, ~3000–4000 words each. Ask whether to review chapter by chapter instead. |

Keep the total near six. More agents produce more overlapping findings and a
longer merge, not a better review.

Reasoning effort: lane B and C briefs are mechanical and self-checking; run
them one step lower (`effort: "lower"`). Run A and D at the default; they
need judgement.

Launch all reviewers in one message so they run concurrently.

## 5. Reviewer brief

Each agent knows only its brief. Give it:

- The path to SKILL.md and the sections it must apply (e.g. "§1.1–§1.4, §2,
  and checklist items 5–8").
- The path to the text, and for a chunk, the exact section range.
- The stage and audience from §2, plus any user notes.
- Its boundary: report only issues in its lane; others cover the rest.
- The rule from SKILL.md: never invent claims, data, or citations; if the
  science is unclear, flag it rather than rewording around it.
- Read-only: do not edit the file.

Ask for findings in this shape, most important first, at most ~25:

```
- loc: <section/paragraph, plus a short exact quote>
  principle: <short name, e.g. "zombie noun", "ambiguous this", "overclaim">
  severity: high | medium | low
  before: <original>
  after: <suggested revision, or "—" if the fix is the author's to make>
  why: <one line>
```

High means a reader would misunderstand or stop reading; low is polish.

## 6. Merging

The main agent owns the final report.

1. **Structure first.** If lane A proposes cutting or moving a passage, drop
   B/C findings inside it, or note them as "if kept".
2. **Science over style.** If lane D flags a claim as unsupported, don't
   offer a smoother wording of the same claim from B or C.
3. **Dedupe** findings that hit the same span; keep the one with the clearer
   fix and both principle names.
4. **Group by severity, then by location.** Lead with a 3–5 line summary of
   the main problems; then the findings in SKILL.md's before/after style.
5. **Check, don't relay.** Spot-check high-severity findings against the
   text. Reviewers misquote and overreach like any reader; drop what does
   not hold up.
6. Say which lanes ran and which were skipped, so the author knows what the
   review did not cover.
