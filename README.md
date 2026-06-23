# claude-skills

Mikael's collection of [Claude Code](https://claude.com/claude-code) skills,
distributed as a plugin marketplace.

## Install

```
/plugin marketplace add mlund/claude-skills
/plugin install scientific-writing
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

## Layout

```
claude-skills/                      # this repo = a marketplace
├── .claude-plugin/
│   └── marketplace.json            # lists the plugins
└── plugins/
    └── scientific-writing/         # one plugin
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── scientific-writing/
                └── SKILL.md
```

More skills can be added under `plugins/` (each its own plugin) and listed in
`marketplace.json`.

## License

MIT
