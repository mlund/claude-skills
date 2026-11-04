# Reaction ensemble

## Acceptance

For reaction Σν_i S_i = 0, extent ξ = ±1, ν̄ = Σν_i (Smith & Triska 1994, Eq. 18):

P = min[1, V^(ν̄ξ) Γ^ξ Π_i N_i!/(N_i + ν_iξ)! · e^(−βΔU)]

- Γ = Π(q_i/Λ_i³)^ν_i (Eq. 19) = e^(−ΔG°/RT) (P°/RT)^ν̄ for ideal-gas data (Eq. 21).
- No chemical potential is needed; both the reaction ensemble and RCMC say so.
- **Reaction ensemble and RCMC (Johnson et al. 1994)** were developed independently, with the same
  structure: Johnson's Eq. 11 has Πq_i^ν_i in place of Γ, plus the count factors. House: RxMC.
- Several reactions: "any linearly independent set" (Eq. 25). Pick reaction, then direction, at random.
- Add volume moves for constant P, and box-to-box steps for phases (Γ = 1, ν̄ = 0 gives Gibbs).

## Constants in solution

Implicit solvent makes K an effective solution constant, not the ideal-gas Γ of Eq. 21.

- Faunus: K dimensionless at c° = 1 M; bias uses c°V. `!pK`, `!K`, `!lnK`, `!dG`.
- ESPResSo: Γ = K_c (N_A(σ/dm)³)^ν̄, in simulation units.
- State c°, and whether K is thermodynamic or apparent. A K fitted with one model doesn't carry over.

## Moves

- **Fix the correspondence** between reactants and products for the whole run, or reversibility fails.
  A + B = C + D: if A→C forward, then C→A backward (Smith & Triska).
- **Replace like with like:** similar sizes, and insert only the smallest species at random. Johnson
  inserts dimers into the monomer's cavity to avoid dense-fluid insertion.
- **Forward and reverse with equal probability.** With several reactions, also keep selection fixed.
- **Rate:** Smith & Triska suggest enough attempts that accepted reaction steps reach several percent of
  the molecules per volume step. A starting point, not a rule.
- **Write 2A → B, not A + A → B** in ESPResSo; Faunus counts repeated species sequentially.
- **Corresponding groups:** RxMC exchanges ions with a reservoir only in groups such as a salt, so it can
  exchange dissociated ions only if they also belong to an added salt, and it "does not lead to the correct
  grand-canonical distribution of individual ions"; finite-size effects are worst at low ion
  concentrations, e.g. pH ≈ 7 (Curk et al. 2022).

## Solubility and finite reservoirs

Faunus `reservoir: true` models a finite amount of substance in another phase, such as a solid. It is
never placed in the cell, has activity 1 (no count or volume factor), and its count changes with the
reaction. It differs from `activity`, an infinite bath. Docs: `topology.md` (Implicit Reservoirs).

- Ca(OH)₂ = Ca²⁺ + 2 OH⁻, pK 5.19: ideal s = (K_sp/4)^(1/3) = 0.0117 M, as the docs' 0.012 M.
- **Depletion is physics:** an emptied reservoir stops the forward reaction, so the solution is
  undersaturated. It can also grow from zero, as precipitation (`tests/files/reservoir_caoh2_coupled`).
- Size it deliberately: too little solid dissolves entirely, and K_sp is then not reached. Report the final count.
- Activity 1 ignores particle size and surface terms (our reading).

## pH from a closed run

pH is an output. Options and traps:

- **Concentration estimate:** pH ≈ −lg(c_H,bulk/c°), "should never be used with the constant-pH
  ensemble" (Review §3.4.1); it neglects H⁺ non-ideality, and depends on what counts as bulk.
- **Widom:** needs free H⁺, and "might not have any" at moderate to high pH (B&L 2023).
- **Surface Widom:** B&L use condensed protons, in equilibrium with bulk H⁺, because free H⁺ is scarce.
  With tinfoil Ewald: pH = −lg[(N+1)/Z] + pK_a + lg⟨exp[−β(ΔU + qϕ_B)]⟩₀, N protonated sites (2024 Eq. 6).
  Φ_B enters explicitly (`theory.md`). Their method.
- **K sweeping:** vary pK_a and read pH (Review). It moves differently along the curve from pH sweeping:
  increasing pK_a reduces α while pH rises. Valid only with "all other conditions" the same.
- **Volume and pH:** box size changes pH in RxMC, because H⁺ concentration does (Landsgesell 2017).

For acid–base specifics, see `theory.md`. RxMC in closed systems has no pH_in.
