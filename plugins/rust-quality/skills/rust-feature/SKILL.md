---
name: rust-feature
description: Implement a feature or non-trivial change in a Rust codebase with high assurance — explicit invariants, TDD at agreed seams, deep-module design, a cargo verification matrix and an adversarial review. Use whenever the user asks to build, add or implement something in a Rust project (a new module, type, API, pool, parser, state machine, service), even if they don't mention invariants or quality; also when they hand over a Rust ticket or spec to implement.
---

# Rust Feature Workflow

Work through the phases in order. Each produces something the next depends on, and two of them end in a stop where the user confirms before you continue.

This skill builds on two skills from [mattpocock/skills](https://github.com/mattpocock/skills). Load them when the phase says to:

- **`codebase-design`**: the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality). Use its terms exactly.
- **`tdd`**: the red → green loop, tested only at seams agreed with the user.

What this skill adds is **explicit invariants**:

> TDD asks *"Does this behaviour work?"* Invariants ask *"What must stay true no matter which operation runs, or how the system got into its current state?"*

In `codebase-design` terms, invariants are part of a module's **interface**: what a caller must know to use it correctly. This skill makes you write them down before coding, and makes the types, code and tests carry them.

## Assumed repo setup

The skill assumes the repo has the quality configuration from the `rust-quality-setup` skill: workspace lints (no `unwrap`/`expect`/`panic` outside tests, `// SAFETY:` comments required, `#[expect(..., reason = "...")]` instead of `#[allow]`, rustdoc `# Errors`/`# Panics` sections), `clippy.toml`, `deny.toml`, and `cargo xtask verify`.

Check for `[workspace.lints]` (or `[lints]`) in `Cargo.toml` and an `xtask` crate. If they're missing, tell the user once that `rust-quality-setup` would add them, then carry on: in Phase 5, use the repo's own CI commands instead, and treat the lint rules above as rules you follow yourself.

Because the lints enforce those rules mechanically, this skill doesn't repeat them. What lints can't judge is whether a suppression is justified: a `#[expect]` whose reason a sceptical reviewer wouldn't accept is a bug.

## Ground rules

- **Facts vs. assumptions.** Label every assumption about requirements or behaviour. Don't invent requirements.
- **Minimal change surface.** Prefer existing abstractions. No unrelated refactors, speculative generality, or new public API or dependency without a stated reason.
- **No claim without evidence.** Only say something passes or is verified if you ran it in this task and saw the result.

---

## Phase 0: Reconnaissance (delegated)

Reading the codebase is context-heavy and mostly disposable, so give it to a research-only subagent. Brief it with the feature request, and ask for a brief under ~400 words, every claim citing a path:

1. **Analogous implementations**: the existing code most like this feature. These set the conventions.
2. **Conventions**: error types and how errors cross module seams, async runtime, tracing, test layout and helpers.
3. **Dependency direction**: which crates/modules depend on which; layering from code, `deny.toml` bans, or ADRs.
4. **Compatibility surface**: public API of library crates, serialized formats (serde types, wire/disk formats, schemas), feature flags, MSRV.
5. **Verification**: whether `cargo xtask verify` exists; what CI runs; which of nextest, cargo-mutants, cargo-deny, cargo-semver-checks, cargo-hack, Miri are installed or used.
6. **Project docs**: `GLOSSARY.md`, ADRs, `CLAUDE.md`, and the rules in them that apply here.

Read the brief, then open the analogous implementation yourself: you'll follow its conventions, so you need to have seen it.

## Phase 1: Name the invariants (delegated)

**If the feature comes with a spec that already lists invariants** (for example from `to-spec`), use those. Check them against the code, add any that are missing, and skip to the stop at the end of this phase.

Otherwise, invariants come in three categories:

| Category | Question | Example |
|---|---|---|
| **Data** | What must always be true of a valid value? | `idle + checked_out == total`; `total <= capacity` |
| **Transition** | What must hold before and after every operation, including errors, panics, early returns and `async` cancellation? | A failed acquire leaves accounting unchanged |
| **Architectural** | Which dependency directions and ownership rules must never break? | Domain crates never depend on persistence adapters |

Spawn two research-only subagents in parallel. Brief each with the feature request, the Phase 0 brief, this table and the enforcement ladder below.

- **Subagent A, data and transition:** reads the relevant types, constructors, state-changing methods and `GLOSSARY.md`.
- **Subagent B, architectural:** reads the crate/module layout, visibility, workspace `Cargo.toml`, `deny.toml` and ADRs.

Each returns **at most 8 invariants specific to this feature** (nothing that holds for any Rust code), as a table:

| Invariant | Category | Existing / Proposed | Evidence (`file:line`) | Why it matters | Suggested rung |

**Existing** means it holds today, so breaking it is a regression. **Proposed** means it's new with this feature, so it's a design decision for the user. Evidence is the lines that imply it plus one sentence why; for a proposed invariant, cite the requirement or code it protects.

Then, in the main context: spot-check the evidence for every Existing invariant, merge and deduplicate, drop anything you can't justify, and add for each **the test that would catch a violation**. You will enforce this table for the rest of the task, so understand every line of it rather than copying it.

### The enforcement ladder

Pick the highest practical rung, and say why when you settle lower.

1. **Unrepresentable** (types): enums instead of flag combinations, newtypes with validating constructors, typestate, `NonZero*`, ownership so two holders can't exist. The bug can't compile.
2. **Encapsulated**: private fields; state changes only through methods that preserve the invariant or return `Err`.
3. **Runtime-checked**: a private invariant check called via `debug_assert!` at entry and exit of state-changing methods; checked arithmetic where overflow breaks accounting.
4. **Test-only**: last resort; say so explicitly.

Architectural invariants are best enforced by crate boundaries (a crate can't use what isn't in its `Cargo.toml`) and `deny.toml` `wrappers` bans; then by visibility (`pub(crate)`); then by tests.

**Stop: present the invariant table to the user and wait for them to confirm or amend it.**

## Phase 2: Design the interface (`codebase-design`)

Load `codebase-design` and design the module:

- Aim for **depth**: much behaviour behind a small interface. The machinery that maintains invariants stays inside.
- Place the **seam** deliberately. For external dependencies (database, clock, network), make the seam a trait and plan an in-memory adapter for tests.
- Public constructors return a value that already satisfies every data invariant, or an error. No half-initialized values; no `pub` fields that bypass them.
- Error types are part of the interface: a caller should see from the `Result` what can go wrong.
- **Reuse before adding.** Build on what Phase 0 found; justify any new public item, trait or dependency in one line.
- **Compatibility.** For each item on the compatibility surface, say whether the design changes it. Change public API, serialized formats or feature flags only when the feature requires it.
- **Cost.** State time and space complexity of the main operations, and allocation, cloning or locking on hot paths.

Propose the smallest coherent design plus one alternative you rejected and why. Write out the public interface (signatures, error types, trait seams) with a one-line note on which invariant each choice protects.

## Phase 3: Agree the seams (`tdd`)

Following `tdd`, list the seams to test at, each with a one-line note on what it catches and misses. Map every invariant to at least one seam. An invariant no seam can observe is a design problem: go back to Phase 2.

**Stop: confirm the seams with the user before writing any test.**

## Phase 4: Red → green (`tdd`)

Run the `tdd` loop at the agreed seams. Alongside normal behaviour tests, cover:

- **Invariant-falsifying tests**: tests that try to break an invariant and would fail if the implementation were wrong. Name each after its invariant:

  ```rust
  // Invariant: a failed acquire leaves accounting unchanged.
  #[test]
  fn failed_acquire_leaves_accounting_unchanged() { /* ... */ }
  ```

- **Failure paths**, where they apply: malformed input, boundaries, partial failure midway, retries, timeouts, resource exhaustion, a future dropped mid-operation, a panic inside a callback. Assert the error *and* that the invariants still hold afterwards.
- **Regression tests** for nearby existing behaviour that isn't covered yet.
- **Property tests** (`proptest`) for data and transition invariants, parsers, state machines and round-trips (`decode(encode(x)) == x`). For state machines, apply random operation sequences through the public interface and check invariants after each step. Commit the `proptest-regressions/` files.
- **Concurrency**: check lock ordering, `Send`/`Sync` assumptions, and cancellation safety at every `.await` that holds state. Use `loom` for hand-rolled synchronization; otherwise stress-test with many tasks and assert invariants after.

Restore invariants with RAII guards (`Drop`) rather than relying on every exit path, so early returns, panics and cancellation are covered. Document invariants callers must know in the rustdoc of the public items.

## Phase 5: Verify (delegated to a cheaper model)

Running checks and fixing mechanical findings doesn't need the main model's judgement, and its output is long. Spawn a subagent on a cheaper, faster model (e.g. `model: "haiku"` or `"sonnet"`) with this brief:

> Run `cargo xtask verify` (add `--semver` if a library's public API changed). Fix only **mechanical** findings: formatting, missing rustdoc sections, unused imports, simple clippy suggestions that don't change behaviour. Re-run until clean or until only non-mechanical findings remain.
>
> Do **not**: add `#[expect]`/`#[allow]`; replace `unwrap`/`expect` with a different panic; change a public signature, an error type or an error path; touch tests' assertions. Report those findings back unfixed, with `file:line` and the lint.
>
> Report: the final summary block from `xtask verify`, the fixes you made (one line each), and the unfixed findings.

Handle the unfixed findings yourself; they are usually design questions about how something should fail. Then, as applicable:

- `cargo xtask mutants` when the change has critical logic. Each surviving mutant is a missing test (add it) or an equivalent mutant (say why).
- `cargo +nightly miri test` when the change touches `unsafe`; say if Miri can't run it.

If the repo has no `xtask`, give the subagent the CI commands from Phase 0 instead.

## Phase 6: Review ritual

On the final diff, in order:

1. **`/code-review medium`** (Claude Code's built-in review). Fix confirmed findings; say why for any you decline. Re-verify.
2. **`/simplify`** (Claude Code's built-in). Accept a simplification only if every invariant stays on the same or a higher rung. Re-verify.
3. **Adversarial invariant review (delegated).** Spawn a fresh subagent with the diff, the feature request and the invariant table, **but not your design rationale**, so it doesn't anchor on your reasoning. Ask it for the **three most plausible ways the change is wrong** (a counterexample to an invariant, a broken failure path, a compatibility break, a layering violation) and to write a failing test for each. A test that fails is a real bug: keep it, fix the code, re-verify. Undemonstrated but plausible hypotheses go into the report as risks.

This runs after `/simplify` because simplification is where invariants most often weaken unnoticed. `mattpocock/skills` also has a `code-review` skill; step 1 means the built-in one unless the user says otherwise.

## Phase 7: Report

Passing checks isn't the finish line: first check that the change does what was asked and respects the repo's architecture. Then report:

1. **Invariant table**, final: invariant, category, enforcement rung, tests that target it.
2. **Design**: public interface and seams, the rejected alternative, any compatibility change.
3. **Verification**: the `xtask verify` summary and any other commands run, with results; what couldn't be run and why.
4. **Review**: what `/code-review` found and what was fixed or declined; what `/simplify` changed; what the adversarial review tried and found.
5. **Risks and debt**: invariants left test-only, unverified assumptions, possible regressions, intentional debt.
