# Large files

Git and GitHub are poor at large binaries (GitHub rejects files over 100 MB and slows down well
before), and most readers want the numbers behind the figures, not the raw output.

## What goes where

| Kind | Example | Git | Zenodo |
|---|---|---|---|
| Inputs | topology, force field, simulation input, small experimental data | yes | via git |
| Code and notebooks | | yes | via git |
| Extracted features | per-frame observables, histograms, averages behind each figure | yes, if small (≲ 10s of MB) | via git, else an archive |
| Raw output | trajectories (`.xtc`, `.dcd`, `.trr`), checkpoints, binary dumps | no, `.gitignore` | archive, if needed at all |
| Figures | | generated, optionally committed | via git |

Ask the user whether raw output is needed. Often the inputs (to regenerate it) plus extracted
features (to redo the analysis) suffice, and the deposit shrinks by orders of magnitude. If raw
output is kept, consider stripping it first (e.g. drop solvent, reduce frame rate) and say so in the
README.

## Deposition route

- **Small repository** (everything fits in git): use the GitHub–Zenodo integration. Each GitHub
  release creates a new Zenodo version with its own DOI under one concept DOI.
- **Large data**: upload archives to Zenodo by hand. A record holds several files, and a new version
  can import unchanged files from the previous one. So split archives by how often they change:
  - raw output (never changes),
  - extracted features (change only with the extraction code),
  - code + results from one commit (changes often, small).

  Name each data archive after a hash of its contents, so an unchanged part keeps its name and the
  user knows to import it rather than re-upload. Include `SHA256SUMS` and build only from a clean
  working tree so the archive matches a commit.

## Archive script

`scripts/make_zenodo_zip.py` (in this skill) implements the above with the standard library. Copy it
into the project's `scripts/`, then:

    uv run python scripts/make_zenodo_zip.py --name <deposit-name> \
        --part trajectories='systems/**/*.xtc' --part features='results/counts/*.npz'

It writes to `dist/` (add to `.gitignore`):

- `<name>-<part>-<hash>.zip` per `--part`, of the untracked files matching its globs;
- `<name>-<version>-<commit>.zip` of everything committed (`git ls-files`).

All archives unpack into one `<name>/` folder, each with its own `SHA256SUMS*` manifest. Document in the README which
archive holds what, and the steps for a new Zenodo version: import unchanged archives, remove those
whose name changed, upload their replacements.
