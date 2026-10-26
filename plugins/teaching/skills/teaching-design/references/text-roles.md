# Text roles

Author text as a **semantic role**; derive size, weight, colour and family from it. A role lets the
tool harvest every keyword into a vocabulary page, suppress `body` in lecture mode, enforce the
salience budget and re-theme a deck without touching content. Direct formatting does none of that.

## Channel orthogonality

| Channel | Encodes | Never encodes |
|---|---|---|
| Size + weight | **Salience** — how much attention this earns | category, voice |
| Colour (hue) | **Semantic category** — what kind of thing this is | salience alone |
| Colour (lightness) | Salience, reinforcing size | category |
| Italic | **Voice** — aside, quotation, variable | stress in running text |
| Family | **Register shift** — code, maths, quotation | hierarchy |

More attention → move up a tier. A different *kind* of thing → change hue at the same tier. The two
moves stay independent, which is what prevents bold-red-bigger-underlined.

## The salience budget

- **Exactly one** Tier 3 element per slide (`assertion` *or* `question`, never both).
- **At most ~3** Tier 2 elements visible at once.
- Tier 0–1 unlimited — at or below baseline, they do not compete.
- Tier 4 exempt: it borrows salience and gives it back.

## The roles

Sizes are **ratios to body**, never points: published advice on absolute slide sizes ranges from
14pt to 30pt with everyone confident. Pick body for the room; the scale follows.

### Tier 3 — load-bearing

| Role | What it is | Size | Weight | Colour |
|---|---|---|---|---|
| `assertion` | the slide's claim, as a sentence | 1.6–2.0× | bold | max contrast |
| `question` | a gate prompt or posed question | 1.5–1.8× | semibold | max contrast |

⚠️ A claim-stating heading **is** the load-bearing content and must not be styled as chrome.
Principles are recalled better from a sentence headline than from a bulleted list.

### Tier 2 — marked

| Role | What it is | Size | Weight | Colour |
|---|---|---|---|---|
| `keyword` | a term being introduced | 1.0× | medium | **reserved hue** |
| `definition` | the gloss bound to a keyword | 1.0× | regular | body |
| `callout` | a label placed **on** a graphic | 0.9–1.0× | medium | contrast vs *local* background |
| `readout` | a live value from an explorable | 1.0–1.2× | medium, **tabular figures** | body or accent |
| `emphasis` | inline stress in running text | 1.0× | **weight only** | inherit |

- `callout` carries the cheapest large win: spatial contiguity, g = 0.63. Not adjacent → defect.
- `readout` must use tabular figures. Digits that change width create motion carrying no
  information — the decorational case, d = −0.05.
- `emphasis` changes weight only. Hue is spent on category.
- `keyword` is also a **data** role: marking it populates the vocabulary page. Showing key words
  while speaking is the one redundancy that works (g = 0.29); narrating text already on screen
  does nothing (g = −0.04).

### Tier 1 — baseline

| Role | What it is | Size | Weight | Colour |
|---|---|---|---|---|
| `body` | supporting prose | **1.0× (defines the scale)** | regular | normal |
| `item` | one list element, revealed in sequence | 1.0× | regular | normal |
| `caption` | text bound to a figure | 0.85× | regular | reduced |

`item` defaults to progressive reveal synced to speech — temporal contiguity, g = 0.78.

### Tier 0 — suppressed (chrome)

| Role | What it is | Size | Weight | Colour |
|---|---|---|---|---|
| `label` | section/module name, running head | 0.7–0.8× | regular | low, **≥ floor** |
| `aside` | caveat, parenthetical, footnote | 0.8× | italic allowed | low |
| `source` | citation, credit | 0.65–0.75× | regular | lowest used |

Withholding contrast from chrome is **signalling by omission**, not absence of design.

### Tier 4 — transient

| Role | Treatment |
|---|---|
| `signal` | momentary highlight tied to the current step; **then removed**. Dynamic cues beat static (d = 0.43 vs 0.38) |
| `feedback` | **promote to Tier 3 while present** — the wrong-answer moment is the highest-encoding moment |
| `hint` | Tier 2, and deliberately **less** attractive than `feedback` |

### Register shifts (family only, salience-neutral)

`code` (mono, ~0.95× to match optically) · `formula` (maths face, never faked with italic body) ·
`quote` (secondary family or italic, offset — where enclosure earns its place).

## Mode-aware rendering

| Role | Presented lecture | Self-study tutorial |
|---|---|---|
| `assertion` | full | full |
| `body` | **suppressed** — you are saying it | **full** — nobody is |
| `item` | progressive, synced to speech | all visible |
| `label` | minimal | **stronger** — the only navigation |
| `signal` | active | inactive (no utterance to bind to) |
| `hint` / `feedback` | usually inactive | active |
| `caption` | reduced | full |

This is also how an explorable gets *more* scaffolding in self-study: in a lecture the teacher is
the scaffold; alone, the learner has only what the page provides.

## Reference palette

Measured against `#FFFFFF` (WCAG 2.1 relative luminance). One valid resolution, not the spec.

| Token | Hex | Contrast | Used by |
|---|---|---|---|
| `ink` | `#16181D` | 17.76:1 | assertion, question, callout, code |
| `body` | `#2E333B` | 12.71:1 | body, item, definition, emphasis |
| `muted` | `#525964` | 7.07:1 | caption |
| `low` | `#656C76` | **5.30:1** | label, aside, source — the Tier 0 floor |
| `accent` | `#116A86` | 6.12:1 | keyword only |
| `rule` | `#E3E5E8` | 1.26:1 | **non-text only** — dividers |

`low` at 5.30:1 still clears 4.5:1. De-emphasise by going **smaller and lighter in weight**, not
darker-on-white. See `colour.md` for the dark-ground equivalents.

## What this system refuses

- **No `title` role** — it covers two opposite jobs. Choose `assertion` or `label`.
- **No colour-only emphasis.** Hue is category.
- **No underline** except links.
- **No all-caps** beyond a short `label`.
- **No author-set point sizes.** Roles and a scale, or none of the mode-switching works.
