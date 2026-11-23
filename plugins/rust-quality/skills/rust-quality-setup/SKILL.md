---
name: rust-quality-setup
description: Set up a Rust repo's mechanical quality gates — workspace lints (no unwrap/expect/panic, SAFETY comments, #[expect] with reasons, rustdoc Errors/Panics), clippy.toml, cargo-deny with architectural dependency bans, and a `cargo xtask verify` / `cargo xtask mutants` command. Use when the user wants to harden a Rust repo, add lint or CI quality config, enforce layering between crates, set up xtask, or prepare a repo for the rust-feature skill.
---

# Rust Quality Setup

Move every rule that a machine can check out of prompts and into cargo config. Lints, bans and one verify command are deterministic, cost no model tokens, and apply to humans and agents alike, so the `rust-feature` skill can simply say "make `cargo xtask verify` pass".

This is a one-off setup per repo. It changes shared config, so **show the user the plan (step 2) and get a yes before writing files.**

## 1. Survey the repo

Find out, without changing anything:

- Single crate or workspace? Existing `[lints]` / `[workspace.lints]`, `clippy.toml`, `deny.toml`, `.cargo/config.toml`, `xtask`, `justfile`, `Makefile`.
- What CI runs (`.github/workflows/`, etc.). The xtask should run the same checks, so local and CI agree.
- `rust-version` (MSRV) in `Cargo.toml`. **The `#[allow]` lints (`allow_attributes`, `allow_attributes_without_reason`) silently do nothing when MSRV is below 1.81**, because `#[expect]` only stabilized then. If MSRV is lower, tell the user and either raise it (if they agree) or drop those two lints.
- Mutually exclusive cargo features (they break `--all-features`).
- Layering: which crates are domain/core vs. adapters (persistence, HTTP, CLI). Ask the user which dependency directions must never break; these become `deny.toml` bans and, ideally, crate boundaries.

## 2. Plan the rollout and confirm

Measure the impact before turning anything on: add the lints at `warn` temporarily and run `cargo clippy --workspace --all-targets 2>&1 | grep -c '^warning'` (and per crate if large). Then propose:

- **Few violations** (roughly under 50): enable everything at the levels below and fix them in this task.
- **Many**: enable at the levels below in the cleanest crates, and at `warn` elsewhere with a note to tighten later; or enable per crate (`[lints]` in each crate instead of `workspace = true`). Don't mass-fix hundreds of violations or sprinkle `#[expect]` without the user agreeing; that's a large diff of judgement calls.

Present: files to add or change, the lint levels, the bans, the violation count and the rollout choice. Wait for confirmation.

## 3. Write the config

### Lints: workspace `Cargo.toml`

```toml
[workspace.package]
rust-version = "1.81"   # at least 1.81, or the allow_attributes lints do nothing

[workspace.lints.rust]
unsafe_code = "deny"        # crates that need unsafe override this in their own [lints]
missing_docs = "warn"
unreachable_pub = "warn"

[workspace.lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
todo = "deny"
unimplemented = "deny"
dbg_macro = "deny"
undocumented_unsafe_blocks = "deny"       # requires `// SAFETY:` comments
missing_errors_doc = "warn"               # rustdoc `# Errors`
missing_panics_doc = "warn"               # rustdoc `# Panics`
allow_attributes = "deny"                 # use #[expect], which errors once the lint stops firing
allow_attributes_without_reason = "deny"  # every suppression needs reason = "..."
```

In every member crate's `Cargo.toml` (including `xtask`):

```toml
[lints]
workspace = true
```

For a single-crate repo, use `[lints.rust]` / `[lints.clippy]` directly in its `Cargo.toml`. `-D warnings` in verify turns the `warn` lints into failures too.

### `clippy.toml`

```toml
allow-unwrap-in-tests = true
allow-expect-in-tests = true
allow-panic-in-tests = true
# Ban APIs that bypass a seam, e.g. time must come through a Clock trait:
# disallowed-methods = [{ path = "std::time::Instant::now", reason = "use the Clock seam" }]
```

### `deny.toml`

Adjust the licence list to the user's policy. Bans with `wrappers` enforce architectural invariants: a crate listed only as allowed for `persistence` fails the check if `domain` depends on it.

```toml
[graph]
all-features = true

[advisories]
yanked = "deny"

[licenses]
allow = [
  "MIT", "Apache-2.0", "Apache-2.0 WITH LLVM-exception",
  "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unicode-3.0", "Zlib",
]
confidence-threshold = 0.9
unused-allowed-license = "allow"

[bans]
multiple-versions = "warn"
wildcards = "deny"
allow-wildcard-paths = true
deny = [
  # Architectural invariants: only the listed crates may depend directly on these.
  # { crate = "sqlx", wrappers = ["persistence"] },
  # { crate = "reqwest", wrappers = ["http-client"] },
]

[sources]
unknown-registry = "deny"
unknown-git = "deny"
```

### `.cargo/config.toml`

```toml
[alias]
xtask = "run --quiet --package xtask --"
```

### `xtask/Cargo.toml`

Add `"xtask"` to the workspace `members`, then:

```toml
[package]
name = "xtask"
version = "0.0.0"
edition = "2021"
publish = false

[lints]
workspace = true
```

### `xtask/src/main.rs`

Std-only, so it adds no dependencies. Edit `FEATURE_SETS` if the repo has mutually exclusive features, and `DEFAULT_BASE` if the main branch isn't `main`. Optional tools (nextest, deny, hack, semver-checks) are used when installed and listed as skipped otherwise.

```rust
//! Repo automation. Run `cargo xtask help`.
//!
//! `verify` runs every check and prints a summary, rather than stopping at the
//! first failure, so one run shows everything that needs fixing.

use std::env;
use std::fs;
use std::path::PathBuf;
use std::process::{Command, ExitCode};

/// Feature sets to build and test. Edit this if the workspace has mutually
/// exclusive features: replace `--all-features` with the sets CI uses.
const FEATURE_SETS: &[&[&str]] = &[&["--all-features"], &["--no-default-features"]];

/// Branch that `mutants` diffs against when none is given.
const DEFAULT_BASE: &str = "main";

fn main() -> ExitCode {
    let args: Vec<String> = env::args().skip(1).collect();
    let result = match args.first().map(String::as_str) {
        Some("verify") => verify(args.iter().any(|a| a == "--semver")),
        Some("mutants") => mutants(args.get(1).map_or(DEFAULT_BASE, String::as_str)),
        _ => {
            eprintln!(
                "usage:\n  \
                 cargo xtask verify [--semver]   fmt, clippy, tests, docs, deny (+ semver-checks)\n  \
                 cargo xtask mutants [BASE]      mutation-test code changed since BASE (default: {DEFAULT_BASE})"
            );
            return ExitCode::from(2);
        }
    };
    if result {
        ExitCode::SUCCESS
    } else {
        ExitCode::FAILURE
    }
}

/// A check to run: a label and the cargo arguments, plus optional env vars.
struct Check {
    label: String,
    args: Vec<String>,
    env: Vec<(&'static str, &'static str)>,
}

impl Check {
    fn new(label: impl Into<String>, args: &[&str]) -> Self {
        Self {
            label: label.into(),
            args: args.iter().map(|s| (*s).to_owned()).collect(),
            env: Vec::new(),
        }
    }

    fn with_env(mut self, key: &'static str, value: &'static str) -> Self {
        self.env.push((key, value));
        self
    }
}

fn verify(semver: bool) -> bool {
    let nextest = has_subcommand("nextest");
    let mut checks = vec![Check::new("fmt", &["fmt", "--all", "--", "--check"])];

    for set in FEATURE_SETS {
        let label = set.join(" ");
        let mut clippy = vec!["clippy", "--workspace", "--all-targets"];
        clippy.extend_from_slice(set);
        clippy.extend_from_slice(&["--", "-D", "warnings"]);
        checks.push(Check::new(format!("clippy {label}"), &clippy));

        if nextest {
            let mut run = vec!["nextest", "run", "--workspace", "--no-tests=pass"];
            run.extend_from_slice(set);
            checks.push(Check::new(format!("nextest {label}"), &run));
            // nextest does not run doctests.
            let mut doc = vec!["test", "--workspace", "--doc"];
            doc.extend_from_slice(set);
            checks.push(Check::new(format!("doctests {label}"), &doc));
        } else {
            let mut test = vec!["test", "--workspace"];
            test.extend_from_slice(set);
            checks.push(Check::new(format!("test {label}"), &test));
        }
    }

    checks.push(
        Check::new(
            "doc",
            &["doc", "--workspace", "--all-features", "--no-deps"],
        )
        .with_env("RUSTDOCFLAGS", "-D warnings"),
    );

    let mut skipped = Vec::new();
    if has_subcommand("deny") {
        checks.push(Check::new("deny", &["deny", "check"]));
    } else {
        skipped.push("deny (cargo-deny not installed)");
    }
    if has_subcommand("hack") {
        checks.push(Check::new(
            "hack each-feature",
            &[
                "hack",
                "check",
                "--workspace",
                "--each-feature",
                "--no-dev-deps",
            ],
        ));
    } else {
        skipped.push("hack (cargo-hack not installed)");
    }
    if semver {
        if has_subcommand("semver-checks") {
            checks.push(Check::new(
                "semver-checks",
                &["semver-checks", "--workspace"],
            ));
        } else {
            skipped.push("semver-checks (cargo-semver-checks not installed)");
        }
    }

    let results: Vec<(String, bool)> = checks
        .into_iter()
        .map(|check| {
            let ok = run(&check);
            (check.label, ok)
        })
        .collect();

    eprintln!("\n=== xtask verify summary ===");
    for (label, ok) in &results {
        eprintln!("{} {label}", if *ok { "PASS" } else { "FAIL" });
    }
    for s in &skipped {
        eprintln!("SKIP {s}");
    }
    results.iter().all(|(_, ok)| *ok)
}

fn mutants(base: &str) -> bool {
    if !has_subcommand("mutants") {
        eprintln!("cargo-mutants is not installed: cargo install --locked cargo-mutants");
        return false;
    }
    // Diff against the merge-base, including uncommitted changes.
    let Some(merge_base) = output("git", &["merge-base", base, "HEAD"]) else {
        eprintln!("could not find merge-base with {base}");
        return false;
    };
    let Some(diff) = output("git", &["diff", merge_base.trim()]) else {
        eprintln!("git diff failed");
        return false;
    };
    if diff.trim().is_empty() {
        eprintln!("no changes since {base}; nothing to mutate");
        return true;
    }
    let dir = PathBuf::from("target/xtask");
    let path = dir.join("mutants.diff");
    if let Err(e) = fs::create_dir_all(&dir).and_then(|()| fs::write(&path, diff)) {
        eprintln!("could not write {}: {e}", path.display());
        return false;
    }
    let path = path.to_string_lossy().into_owned();
    run(&Check::new("mutants", &["mutants", "--in-diff", &path]))
}

fn run(check: &Check) -> bool {
    eprintln!("\n--- {}: cargo {}", check.label, check.args.join(" "));
    let mut cmd = Command::new(cargo());
    cmd.args(&check.args);
    for (k, v) in &check.env {
        cmd.env(k, v);
    }
    match cmd.status() {
        Ok(status) => status.success(),
        Err(e) => {
            eprintln!("failed to start cargo: {e}");
            false
        }
    }
}

fn has_subcommand(name: &str) -> bool {
    Command::new(cargo())
        .args([name, "--version"])
        .output()
        .is_ok_and(|o| o.status.success())
}

fn output(program: &str, args: &[&str]) -> Option<String> {
    let out = Command::new(program).args(args).output().ok()?;
    out.status
        .success()
        .then(|| String::from_utf8_lossy(&out.stdout).into_owned())
}

fn cargo() -> String {
    env::var("CARGO").unwrap_or_else(|_| "cargo".to_owned())
}
```

## 4. Verify the setup

1. `cargo xtask verify` and check its summary. Fix or (per the agreed rollout) relax until it passes.
2. Prove the gates bite: temporarily add an `unwrap()` and a bare `#[allow(dead_code)]` to a library crate, confirm clippy fails on both, then revert. If the `#[allow]` isn't caught, check MSRV (step 1).
3. For each `deny.toml` ban, confirm `cargo deny check bans` passes now. Optionally prove it bites by adding the banned dependency to a non-wrapper crate, then revert.
4. If CI exists, suggest replacing its separate check steps with `cargo xtask verify`, so CI and local runs can't drift.

## 5. Report

List the files changed, lint levels and rollout choice, the bans and the invariant each encodes, the `xtask verify` summary, and which optional tools aren't installed (`cargo install --locked cargo-nextest cargo-deny cargo-hack cargo-semver-checks cargo-mutants`).
