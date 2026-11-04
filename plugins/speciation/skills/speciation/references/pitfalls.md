# Pitfalls

## Manuscript review

Check definitions, phase and activity conventions, equations, claims and citations, then the Documents list.
Report by severity with location, evidence and fix. List house-terminology suggestions separately.

## Implementation review

Check the target ensemble, proposal and acceptance probabilities, units, neutrality, activity inputs,
reversibility and whether validation tests can fail. Use `theory.md` (pH_in) or `rxmc.md` (Acceptance) for the
expected rule, the Algorithms list below, `software.md` for that code, and `tests.md` for validation.
Report as above: code location, evidence such as a derivation or failing test, and a fix.

## Documents

- **"pH" with no phase** in an open or two-phase system.
- **Translating by name.** Map through definitions, units, phase and method (`glossary.md`). A closed and an
  open run at the same pH number need not be the same state.
- **Mixing molar and per-particle forms:** RT with z_iFΦ, or k_BT with z_ieΦ.
- **Calling a_H a_Cl a mean activity.** It's a product; a_± = √(a_+a_-) for 1:1.
- **"Universal" pH − pK_a without its condition,** "provided that all other conditions are the same".
  Ionic strength changes with pH outside about 3–11.
- **Equating a suspension meter reading with pH_sys,** or calling the suspension effect a Donnan potential
  (`theory.md`, Oman et al.). Use the separated equilibrium solution.
- **Equating pH_sys with interstitial pH** (`theory.md`).
- **Attributing to IUPAC or an author more than the passage says.** History and attributions: `dispute.md`.

## Reporting checklist

For simulation reports and methods descriptions: method (with ACP/DAP), pH_in and its meaning, source and
phase of counterion activity, neutrality type, salt state, concentration scale, and I where it matters.

## Algorithms

- **Using reservoir pH with uncorrected cpH and calling it pH_res.** It's neither.
- **Comparing methods at the same number but different phases.** Match pH_sys or pH_res first.
- **Single-ion activities in periodic cells.** They depend on the potential reference, so state it (`theory.md`, Φ_B).
  Report allowed combinations. Paired moves aren't affected.
- **Mixing activity sources:** DAP needs a_H a_Cl, ACP a_H/a_cation, salt a_+a_-.
  Otherwise the thermodynamic cycle doesn't close.
- **Adding salt moves to uncorrected cpH expecting Donnan physics** (G-cpH fails).
- **Treating free H⁺ as negligible by habit.** It's small near neutral pH at high salt,
  but not at low pH or low salt, where it also sets ionic strength.
- **Setting a_Na = a_Cl at extreme pH.** The reservoir must stay neutral, and H⁺ and
  OH⁻ then contribute.
- **Validating with closed RxMC seeded from the open run:** weak (tests.md, N4).
- **Ideal-limit tests can't catch missing site–site Coulomb.** Add the two-site test (tests.md, E6).
- **A fixed "reservoir" activity from ideal c.** Use Widom or CS+MSA, and verify by a
  salt-only run.
- **Apparent pK_a shifts against reservoir pH** include a Donnan contribution at finite
  concentration, so a referee can have a real point. Show the concentration dependence.
