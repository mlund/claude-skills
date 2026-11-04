---
name: speciation
description: >-
  Write, review, explain and develop algorithms for acid-base and speciation
  equilibria in molecular simulation: pH, pKa, titration, charge regulation,
  constant pH, reaction ensemble, grand-reaction, solubility, reservoirs,
  activities, Donnan effects, electroneutrality. Use for scientific writing and
  review on these topics, Faunus SpeciationMove or ESPResSo reaction-method work,
  debugging titration curves, translating between papers, or designing tests.
---

# Speciation

Uses the Lund/Labbez/Košovan vocabulary; other schools' usage is not an error.

## Invariants

- Say which phase, input and concentration scale any pH refers to.
- Keep model quantities apart from measured ones: ΔΦ is not the measured emf E_D.
- Preserve a source's terms, and translate through its equations, units, phase and method.
- Label our own derivations, and don't present disputed positions as settled.
- Check units and signs: pH_sys = pH_res + βeΔΦ/ln 10, so a negatively charged system has pH_sys < pH_res.

House terms, defined in `references/glossary.md`: pH_sys, pH_res, pH_in, uncorrected cpH, GCT, ACP, DAP,
closed RxMC, G-RxMC, ΔΦ, E_D, pc_H(r).

## Where to look

Start with the listed section, searching for the passage before reading a whole file. Open more only
when needed.

| Task | Start with |
|---|---|
| Translate or define a term | `glossary.md`: search the term, read that row |
| Write text | `pitfalls.md`, Documents |
| Review a manuscript | `pitfalls.md`, Manuscript review |
| Review code or an algorithm | `pitfalls.md`, Implementation review |
| Methods section or simulation report | `pitfalls.md`, Reporting checklist |
| pH, activity, potentials (incl. Bethe), IUPAC | `theory.md`, What the sources support |
| pH_in, paired moves | `theory.md`, pH_in |
| Whether to mention "Donnan" | `donnan.md` |
| Comment/Reply, history | `dispute.md` |
| Design a titration move | `theory.md`, pH_in; then `pitfalls.md`, Algorithms |
| General reactions, solubility, pH from closed runs | `rxmc.md`: the matching section |
| Faunus or ESPResSo input, or a wrong result | `software.md`: that code's section and its traps |
| Design or assess validation | `tests.md`: Exact checks or Numerical checks |
| Exact ideal numbers | `scripts/ideal_reference.py --help` |
| A citation or IUPAC term | `sources.md`: search by author, year or DOI, read that row. Consult external sources when evidence is absent or needs verification |

Paths are under `references/`, except the script.

## Modes

- **Write:** house terms for new text; in an existing document, keep its notation.
- **Review:** findings by severity, with location, evidence and fix; correctness apart from house terminology.
- **Develop:** state the acceptance rule, its inputs and their meaning before coding.
- **Debug:** check setup traps first.

Match the request's scope: for a wording edit, change the wording and flag serious errors briefly; for a
narrow question, give only what's needed to interpret the answer.

Don't state what a paper says beyond these notes unless you've read it; ask the user by DOI if text is missing.
