# claude-skills

Mikael's collection of [Claude Code](https://claude.com/claude-code) skills,
distributed as a plugin marketplace.

## Install

```
/plugin marketplace add mlund/claude-skills
/plugin install scientific-writing
/plugin install scientific-plotting
/plugin install faunus
```

Update later by re-running `/plugin marketplace add mlund/claude-skills` (or pulling this repo).

## Plugins

### scientific-writing

A skill for writing and revising clear, concise, reader-focused scientific prose
(papers, abstracts, grants, reviews, theses). It combines three sources:

- **Nature Masterclasses, "Writing for Greater Impact"** — six readability levers
  (active voice, strong verbs, simple words, conciseness, specificity, signposting).
- **Strunk & White, *The Elements of Style*** — the sentence and the word.
- **The Economist Style Guide** — tone and the shape of the whole piece.

The skill triggers automatically when drafting or editing scholarly text, or on
request to make writing clearer, tighter, or higher-impact.

### scientific-plotting

A skill for designing, creating, and reviewing plots and data visualizations for
scientific journals. It walks a three-phase workflow — **design** (message,
audience, chart choice), **create** (faithful encoding, color, uncertainty,
typography), and **review** (a structured critique checklist) — and draws its
guidance together from:

- **Perceptual foundations** — the Cleveland–McGill accuracy hierarchy and
  Tufte's data-ink principle (position/length over angle/area/color; maximize
  data-ink; avoid chartjunk).
- **Better-figures guidance** — Rougier et al.'s "Ten Simple Rules for Better
  Figures," a designing-effective-figures workshop, and the Royal Statistical
  Society guide.
- **Statistical honesty** — Gordon & Finch's "Statistician, Heal Thyself" (show
  raw data, points not bars, define your error bars, CIs over p-stars).
- **Journal production specs** — artwork guidelines for Nature, Science, Cell,
  and ACS (size, DPI, fonts, line weights, file formats, color mode).

Reference files cover chart selection, color/accessibility, design principles,
statistics & uncertainty, journal specs, and a review checklist. The skill
triggers when making or critiquing a figure for a paper, poster, or talk.

### faunus

Two skills for [Faunus](https://github.com/mlund/faunus-rs), a Monte Carlo and
molecular dynamics simulation code:

- **faunus-input** — create, validate, and explain Faunus YAML input files
  (atoms, molecules, energy terms, MC moves, analysis).
- **faunus-run** — build, run, profile, and debug simulations; manage state
  files and equilibration.

Both read documentation and example inputs from a local Faunus checkout, so on
first use they ask for the path to your Faunus source directory.

## Layout

```
claude-skills/                      # this repo = a marketplace
├── .claude-plugin/
│   └── marketplace.json            # lists the plugins
└── plugins/
    ├── scientific-writing/         # one plugin = one skill
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── scientific-writing/
    │           └── SKILL.md
    ├── scientific-plotting/        # one plugin = one skill (+ references)
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── scientific-plotting/
    │           ├── SKILL.md
    │           └── references/
    └── faunus/                     # one plugin = two skills
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── faunus-input/
            │   ├── SKILL.md
            │   └── reference.md
            └── faunus-run/
                └── SKILL.md
```

More skills can be added under `plugins/` (each its own plugin) and listed in
`marketplace.json`.

## License

MIT
