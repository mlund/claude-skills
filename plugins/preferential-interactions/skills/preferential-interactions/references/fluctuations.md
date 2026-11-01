# Equations: fluctuation theory: second derivatives, solute volume, interfaces

Notation: 1 = water, 2 = solute, 3 = cosolute. ρ_i is a number density and m_i = N_i/N1 a
molality, written as a number ratio, so m3/m1 = ρ3/ρ1. φ_i = ρ_iV̄_i. β = 1/k_BT, and RT replaces
k_BT on molar quantities. h_ij = g_ij − 1. G_ij = G_ji, but N_ij = ρ_jG_ij counts j around i, so
N_ij ≠ N_ji. The superscript ° denotes the solute at infinite dilution (m2 → 0).

Sources give the paper's equation number and DOI; equation numbers were checked against
full texts unless marked. "(inference)" marks a step no cited paper states. Section numbers (§N)
are shared across the equation files; SKILL.md maps each § to its file.

## 15. Fluctuation theory: second derivatives, solute volume, interfaces

Source: Ploetz & Smith 2013, Adv. Chem. Phys. 153, 311 (10.1002/9781118571767.ch4). The PMC text
lacks the equations, so the statements below are from prose; check equation forms in the original.

- **Second cosolute derivative of K (Ploetz & Smith 2013, §11.4)**: ∂²lnK/∂(ln a3)² is set by fluctuations of an
  instantaneous preferential interaction coefficient Γ(t) in the local region (form presumably
  N3(t) − (ρ3/ρ1)N1(t); the equation is stripped)
  around each solute form. A near-zero second derivative (constant m-value) means similar Γ
  fluctuations for both forms. Compare the nonlinear ΔΓ″23 of Heyda & Dzubiella 2014 (gamma-linkage.md §11).
- (inference) With an exact site partition, Γ(t) = Σγ_i(t), so the variance splits into site
  covariances ⟨δγ_iδγ_j⟩. This would attribute the curvature to sites the way Σγ_i attributes Γ.
- **Solute volume and reaction compressibility (Ploetz & Smith 2013, §11.4)**: an instantaneous infinite-dilution pseudo
  volume follows from the local solvent count, N1(t) versus the same volume of bulk. The pressure
  second derivative of K involves fluctuations of that volume. (inference) The explicit-solvent counts
  in D(δ) give the same quantity per site.
- **Do not** apply bulk-system fluctuation formulas to each solute form: "a solute, even the size of
  a protein, cannot be formally treated as a system", and the two forms are not independent species
  (Ploetz & Smith 2013, §11.4). This applies to any per-site compressibility or heat capacity.
- **Convergence in practice (Ploetz & Smith 2013, §13)**: they average running KBIs over about one solvation shell where
  they flatten, and call the choice subjective. κ_T from plain integration is "questionable at best";
  PMVs and chemical-potential derivatives converge better because they involve only *differences*
  of KBIs. Γ23 = ρ3(G23 − G21) is such a difference.
- **Planar analogue of a surface-anchored domain (Ploetz & Smith 2013, §8.5)**: Gibbs adsorption at a liquid–vapour
  interface uses Γ_j relative to the primary solvent, from ∫[g_j(z) − g_1(z)] dz along the normal,
  integrated until the value stops changing ("many solvation shells"). Sign of Γ_j sets the sign of the
  surface-tension change, since the activity derivative is positive. Likely underlying paper (not
  checked against the review's reference list): Chen & Smith 2008 (10.1021/jp711062a).
- Terminology: Ploetz & Smith's "local region" is an open sub-volume of bulk solution with random
  origin (finite-volume KBI sense; see estimators.md §12). Do not use it for the solute-anchored D(δ).
