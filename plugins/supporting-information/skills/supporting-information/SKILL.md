---
name: supporting-information
description: >-
  Set up, restructure, or review a repository of supporting information (SI) for a scientific
  paper so it is FAIR, reproducible and ready for Zenodo deposition: uv + uv.lock, ruff, pytest,
  CI, .zenodo.json, CITATION.cff, licenses, ORCIDs, DOIs, data layout, large files such as
  trajectories, and tested analysis code. Use whenever someone wants to prepare SI, archive code or
  data for a paper, get a DOI, "make this repo publishable", turn a messy project or analysis
  directory into a clean deposit, or check an existing SI or data repository before release,
  even if Zenodo or FAIR isn't named.
---

# Supporting information

The goal is a deposit a stranger can find, cite, and rerun to get the published numbers. The
scaffold lives in a template repository, so the skill carries the workflow, not the files:

    https://github.com/mlund/template-for-supporting-information

It provides uv + `uv.lock`, ruff (pathlib, explicit encodings, docstrings, notebooks), pytest, CI
that also validates `.zenodo.json`, `CITATION.cff`, an ordered layout and an `AGENTS.md`. Read the
template's README checklist and `AGENTS.md` once cloned; they are the definition of done.

## Pick the mode

- **New**: no project yet, or an empty directory.
- **Adapt**: an existing project, analysis or paper directory to be turned into SI.
- **Review**: an existing SI or data repository to be checked; change nothing unless asked.

If the request is ambiguous, ask which.

## Gather, then ask

Users find it tedious to be asked what the files already say. Read first: README, `.zenodo.json`,
`CITATION.cff`, `pyproject.toml`, `environment.yml`, `LICENSE*`, `git log` authors, notebook
headers, the manuscript if present, and file sizes (`du`, `find -size +50M`). Then ask only for
what is missing or contradictory, one topic at a time, using the AskUserQuestion tool where
available. `references/interview.md` lists the topics and where each answer goes. When you cannot
ask (non-interactive runs), write the open questions to a `QUESTIONS.md` and continue with clearly
marked placeholders rather than invented values; never invent ORCIDs, DOIs, affiliations or grants.

## New

1. `git clone https://github.com/mlund/template-for-supporting-information <dir>`, remove its `.git`,
   `git init`.
2. Interview, then fill `pyproject.toml` (name, description), `.zenodo.json`, `CITATION.cff`,
   `README.md` and `LICENSE*`. Keep `.zenodo.json` and `CITATION.cff` consistent: same title,
   authors (in order), ORCIDs, affiliations, license, related DOI.
3. Add dependencies with `uv add`, never by hand.
4. Run `uv sync`, `uv run ruff check`, `uv run ruff format --check`, `uv run pytest`, and validate
   `.zenodo.json` (command in `references/review-checklist.md`).
5. Tick off the README checklist; leave unticked items the user must do (Zenodo account, release).

## Adapt

The original directory is the reference for what the published numbers came from, so never
rearrange it in place.

1. Clone the template into a **new, separate directory** (as in *New*), and **copy** files in.
2. Inventory the original: code, notebooks, inputs, outputs, figures, large files. Propose a mapping
   onto the template layout as a table (source → destination, or "leave out" with reason) and get it
   confirmed before copying.
3. Decide on large files with `references/large-files.md`: commit inputs and small extracted
   features, keep raw trajectories and similar out of git, and choose GitHub-triggered or
   archive-based Zenodo deposition.
4. Review the analysis code (see *Code review*) and agree on what to refactor.
5. Refactor test-first. Before changing any analysis code, pin its current outputs with
   characterization tests on real or reduced inputs, so the refactor can't silently shift
   published numbers. Then move logic out of notebooks into `src/`, and leave notebooks as thin
   drivers that import, call and plot.
6. Fix paths so everything runs from the new repository root: relative, `pathlib`, no home
   directories or absolute paths.
7. Fill metadata and run the checks, as in *New*. Confirm each notebook runs, in order, from a clean
   checkout. Report anything whose output changed.

## Review

Read-only unless the user asks for fixes. Work through `references/review-checklist.md`
and run what can be run: the `.zenodo.json` schema check, `uv lock --check`, ruff, pytest, and
the notebooks if cheap. Include the code review below.

Report findings ranked by impact on reuse: blockers (can't reproduce, can't cite, wrong or missing
license, invalid metadata) before polish. For each: what, where (`file:line`), why it matters, and
the concrete fix. Group under Findable, Accessible, Interoperable, Reusable, Zenodo, and Code. End by
offering to apply the fixes, which then follows *Adapt*.

## Code review

Load these skills and apply them to the analysis scripts and notebooks; fetch each `SKILL.md` if it
isn't installed:

- Deep module design: https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design
- TDD: https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd

Look for: logic duplicated across notebooks or scripts; shallow modules whose interface is as
complex as the implementation; numerics with no test; magic constants without units or source;
hidden global state; hardcoded paths; `os.path` and text I/O without an encoding. Propose module
boundaries by what the reader needs to reproduce (e.g. "load trajectory → observable per frame →
average with error"), not by file of origin. Prefer the standard library and few dependencies.
Comments say why, not what.

## Gotchas

- Zenodo's GitHub integration uses the legacy deposit schema. It rejects fields such as `language`;
  validate rather than guess.
- When `.zenodo.json` exists, Zenodo ignores `CITATION.cff`; GitHub's "Cite this repository" uses
  only `CITATION.cff`. Both must agree.
- The GitHub integration adds the repository link to the record itself; don't repeat it in
  `related_identifiers`.
- Code and data often need different licenses: e.g. MIT in `LICENSE`, CC-BY-4.0 in `LICENSE-DATA`.
  CC licenses are not meant for software.
- Commit `uv.lock` and `.python-version`; they are what makes the environment reproducible.
- Zenodo needs the repository to be public, and a GitHub release triggers each new version and DOI.
  Point readers at the concept DOI (all versions).
- Never mention the user's other local projects or paths in files that get published.
