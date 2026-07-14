# claude-skills

MLund's collection of scientific and Faunus agent skills, distributed as both
a [Claude Code](https://claude.com/claude-code) plugin marketplace and a Codex
plugin marketplace.

## Install

### Claude Code

```
/plugin marketplace add mlund/claude-skills
/plugin install scientific-writing
/plugin install scientific-plotting
/plugin install faunus
```

Update later by re-running `/plugin marketplace add mlund/claude-skills` (or pulling this repo).

### Codex

From a local checkout, add the repo marketplace:

```
codex plugin marketplace add ./
```

Or add the GitHub marketplace directly:

```
codex plugin marketplace add mlund/claude-skills
```

The Codex marketplace is defined in `.agents/plugins/marketplace.json`. Each
plugin also has a `.codex-plugin/plugin.json` manifest that points at the same
`skills/` directory used by Claude; the `SKILL.md` files are not duplicated.

## Plugins

### scientific-writing

A skill for writing and revising clear, concise, reader-focused scientific prose
(papers, abstracts, grants, reviews, theses). It combines three style sources
and one theoretical-writing exemplar:

- **Nature Masterclasses, "Writing for Greater Impact"** — six readability levers
  (active voice, strong verbs, simple words, conciseness, specificity, signposting).
- **Strunk & White, *The Elements of Style*** — the sentence and the word.
- **The Economist Style Guide** — tone and the shape of the whole piece.
- **Kirkwood & Shumaker (1952)** — staging dense theoretical arguments:
  assumptions, decompositions, limiting cases, and caveats.

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
├── .agents/
│   └── plugins/
│       └── marketplace.json        # Codex marketplace
├── .claude-plugin/
│   └── marketplace.json            # Claude Code marketplace
└── plugins/
    ├── scientific-writing/         # one plugin = one skill
    │   ├── .codex-plugin/
    │   │   └── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── scientific-writing/
    │           └── SKILL.md
    ├── scientific-plotting/        # one plugin = one skill (+ references)
    │   ├── .codex-plugin/
    │   │   └── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── scientific-plotting/
    │           ├── SKILL.md
    │           └── references/
    └── faunus/                     # one plugin = two skills
        ├── .codex-plugin/
        │   └── plugin.json
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
both marketplace files. Keep the actual skill content in `skills/`; add only
platform-specific manifests under `.claude-plugin/` and `.codex-plugin/`.

## License

MIT
