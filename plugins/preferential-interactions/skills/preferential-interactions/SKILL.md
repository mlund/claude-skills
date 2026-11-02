---
name: preferential-interactions
description: >-
  Review, write, and explain preferential interaction coefficients, Kirkwood–Buff
  theory, Wyman linkage, and simulation solvation excesses. Use for scientific
  terminology, notation, ensembles, concentration scales, salts, and site
  decompositions in these topics, including wording-only reviews.
---

# Preferential interactions

Resolve differences between the Smith, Shimizu, Record, Trout, Ben-Naim and
finite-volume KB conventions using the sourced references below. Translate
cited work faithfully; distinguish scientific errors from house preferences.

## Modes and scope

- **Review:** report substantive issues first, with location, problem, fix and
  supporting DOI. Label optional house-style suggestions separately. Do not
  expand a wording-only request into a full scientific audit unless the wording
  hides a substantive error.
- **Write:** preserve the existing document's notation and requested format.
  For standalone text, use the house conventions below. Define symbols, scales
  and held-constant variables once per relevant context, rather than repeating
  them at every occurrence. When inserting text, keep the document's notation
  throughout, flag any symbol you had to add, and never silently mix two
  notations.
- **Explain:** map the question's notation to the relevant convention and cite
  the sources supporting nontrivial relations.

A prose skill such as scientific-writing is optional when sentence-level editing
is requested and that skill is available; it is not a dependency.

## Load only what is needed

All paths below are relative to this SKILL.md's directory, **not the user's
working directory**. Resolve that directory from the loaded skill path before
searching references or executing scripts. Do not change the user's project
files merely to use the skill.

Start with the relevant section or search result; expand only to resolve missing
context. Do not read every reference or load scripts just to run them. For term
or citation lookups, use `rg -n -i '<term or author>' <resolved-file-path>`;
each glossary row and BibTeX entry is one line.

| Need | Resource |
|---|---|
| Terminology, symbols, school-specific usage | Search `references/glossary.md` |
| DOI or bibliographic entry | Search `references/references.bib` |
| KBIs, excess numbers, solution relations (§1–3), KB inversion (§14) | `references/kb-integrals.md` |
| Γ23 (§4), Wyman linkage (§5), ensemble offsets (§6), molal/molar conversion (§7), m-values (§11) | `references/gamma-linkage.md` |
| Counting (§8), bulk ratio (§9), finite-volume KBI (§12), partitions and site excess (§13) | `references/estimators.md` |
| Salts and electroneutrality (§10) | `references/salts.md` |
| Second derivatives, solute volume, interfaces (§15) | `references/fluctuations.md` |
| Prose review checklist | `references/review.md` |
| Units (§16) and verification checks (§17) | `references/checks.md` |
| Simulation extraction, finite-size corrections, tools, Methods; pair linkage and slow states (local §8) | `references/simulation.md` |

For a review, use the checklist and load the sections supporting the equations
under review; consult only the applicable checks. A term lookup need not load equation files.
`simulation.md` has its own section numbering; the other equation files share
sections 1–17. Qualify cross-file section references with the filename.

## Essential conventions

Existing document notation and explicit user choices take precedence over house
preferences. Preserve source notation in quotations and describe its mapping.

- House numbering: 1 = water, 2 = solute, 3 = cosolute. Prefer number densities
  ρ_i, molarities C_i and Γ23 with the solute index first. Other schools may put
  the cosolute first. Use δ for domain thickness and δ_ij for a Kronecker delta.
- Γ23 is the molal equilibrium-dialysis coefficient
  (∂m3/∂m2)_{T,μ1,μ3}; at solute infinite dilution,
  Γ23° = ρ3(G23 − G21). State concentration scale and ensemble when reporting
  or comparing values.
- The implicit-solvent count ⟨N3(D)⟩ − ρ3Vol[D] gives the **molar excess**
  Γ_molar(D) = ρ3G23(D), not molal Γ23. It includes excluded volume.
  Explicit-solvent counting uses ⟨N3(D) − (ρ3/ρ1)N1(D)⟩.
  Conversion needs additional thermodynamic information: gamma-linkage.md §7.
- Γ23 > 0 means accumulated; Γ23 < 0 means excluded. Never call Γ23 > 0 "bound"
  in the text's own voice: thermodynamic excess need not be site binding. Reserve
  "bound" for an occupancy count with a stated criterion. Local contact enrichment
  can coexist with net exclusion.
- Call the integral over D(δ) a solute-anchored running KBI. It is not a
  finite-volume fluctuation KBI; their convergence corrections differ
  (estimators.md §12).
- Site counts must partition the domain without overlap. Their sum is
  Γ_molar(D) for implicit-solvent excesses and Γ23(D) for counted-solvent
  excesses. Domain geometry, power/additive/ordinary Voronoi distinctions and
  attribution are in estimators.md §13.
- Dialysis Γ23 can appear in a constant-(T, P) Wyman linkage. Do not flag this
  pairing as an ensemble error. Check stoichiometry and offsets for association
  using gamma-linkage.md §5–7; do not assume the 1:1 cancellation applies.
- For salts, consult salts.md §10 before translating single-ion coefficients,
  salt-component coefficients or indistinguishable-ion notation. State valence,
  charge and activity conventions; only neutral combinations are independent
  thermodynamic derivatives.

## Sources and maintenance checks

Never invent a citation or DOI. Distinguish source statements from inferences.
If a needed relation is absent, identify the source gap and verify an appropriate
primary source when available; do not treat the reference collection as exhaustive.

After editing reference files, run `python3 <skill-dir>/scripts/check_refs.py`.
This checks cross-references and DOI coverage, not scientific validity.

After editing simulation.md §8 or its lattice script, or when specifically
validating those relations, run
`python3 <skill-dir>/scripts/check_pair_linkage.py`. It requires numpy; report a
skip if unavailable. Routine explanations need not rerun this unchanged check.
It tests an implicit-solvent lattice, not the user's data, explicit-solvent
(T, P) forms or ions. For applicable data checks, use checks.md §17, items 24–27.
