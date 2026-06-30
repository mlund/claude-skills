---
name: faunus-input
description: Create, validate, and explain Faunus YAML input files for molecular simulation. Use when setting up systems, configuring energy terms, MC moves, or analysis.
---

Help the user create or modify Faunus YAML input files for molecular simulation.
Faunus is an open-source code for Monte Carlo and molecular dynamics simulations
(https://github.com/mlund/faunus-rs). Ground every config you write in the
project's own documentation and working examples — never invent options.

## Locating the Faunus source

This skill reads documentation (`docs/`) and example inputs (`examples/`,
`tests/files/`) from a local Faunus checkout — the `faunus/` subdirectory of
https://github.com/mlund/faunus-rs. Before writing or validating a config,
establish that directory once:

1. If the working directory is already inside a Faunus checkout — a `Cargo.toml`
   whose package is `name = "faunus"`, alongside `docs/` and `examples/` — use it.
2. Otherwise, reuse a path the user gave earlier this session or one saved in memory.
3. Otherwise, try the usual checkout locations and use the first that holds a
   `faunus` `Cargo.toml`: `~/github/faunus-rs/faunus`, then `~/faunus-rs/faunus`.
4. Otherwise, **ask the user for the path to their Faunus source directory.** Offer
   to remember it for next time.

All file paths below are relative to that directory. Always read the relevant
example before generating a new config, so options and syntax match the installed
version.

## Example inputs (read these for reference)

Every example and regression test uses `input.yaml` as the main file. List them with:

```bash
ls examples/*/input.yaml tests/files/*/input.yaml
```

Regression-tested inputs (`tests/files/*/input.yaml`) are the most reliable
references — they are validated against known output on every release.

Curated unit-test topologies (partial configs for specific features):

- `tests/files/speciation_test.yaml` — speciation move setup
- `tests/files/topology_pass.yaml` — valid topology with includes
- `tests/files/translate_molecules_simulation.yaml` — molecule translation
- `tests/files/bonded_interactions.yaml` — bonded energy terms
- `tests/files/nonbonded_interactions.yaml` — nonbonded energy terms
- `tests/files/nonbonded_kimhummer.yaml` — Kim-Hummer potential
- `tests/files/nonbonded_custom.yaml` — custom pair potential
- `tests/files/sasa_interactions.yaml` — SASA energy terms
- `tests/files/cell_sphere.yaml` — spherical cell geometry

Include-file fragments (not standalone):

- `examples/calvados3/calvados3.yaml` — CALVADOS3 forcefield
- `examples/sticks/duello-topology.yaml` — stick molecule topology
- `tests/files/top2.yaml`, `tests/files/top3.yaml` — partial topologies

## YAML input structure

A Faunus input file has this top-level structure:

```yaml
include: [forcefield.yaml]      # optional: merge external YAML files
version: 0.2.0                  # optional: semantic version of include files

atoms: [...]                    # required: define atom/bead types
molecules: [...]                # required: define molecular topologies

system:
  medium: {...}                 # required: temperature, dielectric, salt
  cell: ...                     # required: simulation box geometry
  blocks: [...]                 # required: place molecules in box
  energy: {...}                 # required: interaction potentials
  intermolecular: {...}         # optional: cross-molecule bonded terms

propagate: {...}                # required: MC moves or Langevin dynamics
analysis: [...]                 # optional: trajectory, RDF, energy output
```

See `reference.md` in this skill directory for cell types, units, mixing rules,
and a map from each topic to its documentation page and example files.

## Key tips

- Use `spline` tabulation for performance; add `bounding_spheres: true` for rigid molecules
- Use `replace:` for pairs that fully override `default`; `append:` for pairs that extend it
- `!Stochastic` collections for mixed molecule types; `!Deterministic` with `repeat` for sweeps
