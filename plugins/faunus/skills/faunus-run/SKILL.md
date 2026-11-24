---
name: faunus-run
description: Build, run, profile, and manage Faunus simulations. Use when compiling, running simulations, working with state files, equilibrating systems, or debugging simulation output.
---

Help the user build, run, and manage Faunus molecular simulations. Faunus is an
open-source Rust code for Monte Carlo and molecular dynamics
(https://github.com/mlund/faunus-rs).

## Locating the Faunus source

Building, testing, and the example inputs below all live in a local Faunus
checkout — the `faunus/` subdirectory of https://github.com/mlund/faunus-rs.
Before building or running an example, establish that directory once:

1. If the working directory is already inside a Faunus checkout — a `Cargo.toml`
   whose package is `name = "faunus"` — use it.
2. Otherwise, reuse a path the user gave earlier this session or one saved in memory.
3. Otherwise, try the usual checkout locations and use the first that holds a
   `faunus` `Cargo.toml`: `~/github/faunus-rs/faunus`, then `~/faunus-rs/faunus`.
4. Otherwise, **ask the user for the path to their Faunus source directory.** Offer
   to remember it for next time.

Run `cargo` commands from that directory. A user with `faunus` already on their
`PATH` (e.g. via `cargo install`) only needs the source for examples and tests.

## Building

```bash
# Build (binary lands in target/release/faunus)
cargo build --release

# Build with native SIMD (recommended for production)
RUSTFLAGS="-C target-cpu=native" cargo build --release

# GPU Langevin dynamics
cargo run --release --features gpu -- run -i input.yaml
```

## Running simulations

```bash
# Basic run
faunus run -i input.yaml

# With state file for checkpoint/restart
faunus run -i input.yaml -s state.yaml

# Validate the input without running (works with every subcommand)
faunus run -i input.yaml --check

# Custom output path: -o is a top-level option and goes BEFORE the subcommand
faunus -o results.yaml run -i input.yaml

# Verbose / debug logging
faunus -v run -i input.yaml
RUST_LOG=Debug faunus run -i input.yaml
```

Replace `faunus` with `./target/release/faunus` if it is not on your `PATH`. Check
`faunus --version` first: an older 3.0 beta (e.g. from conda) may be earlier on the `PATH`
and lacks options such as `--check`.

## Rerunning trajectories

Replay a trajectory through a different Hamiltonian (e.g. compare explicit vs 6D tabulated energies):

```bash
# Rerun with a different energy configuration
faunus rerun -i input_6dtable.yaml --traj traj.xtc

# Explicit aux file path (default: traj.aux derived from --traj); -o before the subcommand
faunus -o rerun_output.yaml rerun -i input.yaml --traj traj.xtc --aux traj.aux
```

The original simulation must write a `.aux` frame state file alongside the XTC:

```yaml
analysis:
  - !Trajectory
    file: traj.xtc
    frequency: !Every 100
    save_frame_state: true   # writes traj.aux with quaternions, group sizes, atom_ids
```

The rerun input YAML provides the Hamiltonian and analysis config; `propagate:` is ignored. All analysis frequencies are overridden to sample every frame.

## Equilibration workflow

1. **Two-phase approach**: Run a short equilibration with `analysis: []`, saving state with `-s state.yaml`. Then run production loading the same state file.
2. **Energy minimization**: Use `criterion: Minimize` to accept only downhill moves, then switch to `Metropolis`.
3. **Gradual displacement**: Start with small `dp` values to resolve overlaps, increase for production.

Always check `output.yaml` for move acceptance ratios (target ~30-50% for translations).

## State files

State files (`-s` flag) store the configuration for checkpoint/restart:

```yaml
particles:            # per particle: atom kind (index into `atoms`) and position
  - atom_id: 2
    pos: [2.29, 44.5, -27.9]
cell: !Slit [500.0, 500.0, 500.0]
groups:               # per group: molecule kind, capacity, active size, orientation
  - {molecule: 0, capacity: 142, size: Full, quaternion: [0.44, 0.17, -0.35, 0.81]}
step: 2416            # step counter (see gotchas)
```

- Loaded on startup if the file exists; written after the simulation completes
- Stores atom kinds (so titration/speciation states carry over), the cell, group sizes and
  orientations; molecule definitions and energy terms still come from the input YAML
- Gibbs ensemble generates per-box files: `box0_state.yaml`, `box1_state.yaml`

## Gotchas

- `!FromFile` reads coordinates with the origin at the box corner and shifts them by
  −½·box; for a box-centred file use `!FromFile {file: x.xyz, origin: center}`. Positions
  beyond a wall are an error (faunus-rs#177); older builds accept them silently, giving
  `initial: .inf` and zero acceptance. Trajectories (xtc) use the same corner origin.
- Analysis `frequency: !Every N`, the state-file `step` and `step` output columns count
  `propagate` steps (faunus-rs#178). Older builds count move draws instead (`cycles` per
  step); check which one you have before scaling frequencies.
- `mass_center_position` with a single-axis `projection` keeps the sign, like `atom_position`
  and `dipole_moment` (faunus-rs#176); older builds return |z|.
- Langevin blocks take `timesteps:` (integration timesteps per step); older builds call it `steps:`.
- `!CustomExternal` selections by `atomtype` are re-resolved after every accepted
  titration swap; prefer `index …` selections in titrating systems.

## Profiling (macOS)

Use the built-in `sample` command to profile a running simulation:

```bash
# Sample a running process for 10 seconds at 1ms intervals
sample faunus 10 -f profile.txt

# Or by PID
sample <pid> 10 -f profile.txt
```

The output shows a call tree with hit counts, useful for identifying hot functions.

## Remote execution via SSH

With password-free SSH login, sync and run on remote servers:

```bash
# Sync source to remote
rsync -az --exclude target/ ./ user@host:faunus/

# Build and run remotely (Rust installed in user space)
ssh user@host 'source ~/.cargo/env && cd faunus && RUSTFLAGS="-C target-cpu=native" cargo build --release && ./target/release/faunus run -i input.yaml'

# Fetch results back
rsync -az user@host:faunus/output.yaml .
```

## Testing

```bash
# Unit and integration tests
cargo test

# Regression tests (always use --release for performance)
cargo test --test regression --release -- --include-ignored --test-threads=1
```

## Key tips

- Energy drift in `output.yaml` should be ~0; large drift indicates a bug
- Use `!Fixed <seed>` for reproducible runs during development
