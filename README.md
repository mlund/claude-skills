# claude-skills

Mikael's collection of [Claude Code](https://claude.com/claude-code) skills,
distributed as a plugin marketplace.

## Install

```
/plugin marketplace add mlund/claude-skills
/plugin install scientific-writing
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
