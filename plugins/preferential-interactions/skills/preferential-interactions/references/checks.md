# Equations: dimensions and units; verification checks and round trips

Notation: 1 = water, 2 = solute, 3 = cosolute. ρ_i is a number density and m_i = N_i/N1 a
molality, written as a number ratio, so m3/m1 = ρ3/ρ1. φ_i = ρ_iV̄_i. β = 1/k_BT, and RT replaces
k_BT on molar quantities. h_ij = g_ij − 1. G_ij = G_ji, but N_ij = ρ_jG_ij counts j around i, so
N_ij ≠ N_ji. The superscript ° denotes the solute at infinite dilution (m2 → 0).

Sources give the paper's equation number and DOI; equation numbers were checked against
full texts unless marked. "(inference)" marks a step no cited paper states. Section numbers (§N)
are shared across the equation files; SKILL.md maps each § to its file.

## 16. Dimensions and units (sanity check)

Check every equation for dimensional balance before checking anything else. Most errors in this
field are scale or per-molecule/per-mole slips, and they show up as a mismatch here.

| quantity | dimension | typical units | note |
|---|---|---|---|
| ρ_i | number / volume | nm⁻³; molar C_i in mol L⁻¹ | 1 mol L⁻¹ = 0.6022 nm⁻³; water ρ1 ≈ 33.4 nm⁻³ (55.5 mol L⁻¹) |
| m_i | amount / mass solvent | mol kg⁻¹ | m1• ≈ 55.5 mol kg⁻¹ for water |
| G_ij, G_ij(R), G23(D) | volume per molecule | nm³; cm³ mol⁻¹ | 1 nm³ = 602.2 cm³ mol⁻¹; pure water G11 ≈ −17 cm³ mol⁻¹ (BN77) |
| N_ij = ρ_jG_ij | dimensionless | molecules | |
| Γ23, Γ±, γ_i | dimensionless | molecules of 3 per molecule of 2 | Γ23 = (∂m3/∂m2) is mol/mol |
| ρ3G23 (molar scale) | dimensionless | molecules | differs from Γ23 by ≈ ρ3V̄2 (gamma-linkage.md §7) |
| ⟨N3(D)⟩ − ρ3Vol[D] | dimensionless | molecules | ρ3 and Vol in matching length units |
| V̄_i | volume per molecule or per mole | nm³; cm³ mol⁻¹ | |
| φ_i = ρ_iV̄_i | dimensionless | | ρ and V̄ both per molecule, or C_i and V̄ both per mole |
| κ_T | 1 / pressure | Pa⁻¹, GPa⁻¹ | water ≈ 0.45 GPa⁻¹ |
| RTκ_T, k_BTκ_T | volume per mole / per molecule | cm³ mol⁻¹; nm³ | water: RTκ_T ≈ 1.1 cm³ mol⁻¹ at 298 K |
| a33, ∂ln a/∂ln x | dimensionless | | |
| μ_ij (Smith08) = β∂μ_i/∂ln N_j | dimensionless | | Ben-Naim's μ_αβ = ∂μ_α/∂N_β is energy per molecule (BN77) |
| η (BN77 Eq. 2.1) | number / volume | nm⁻³ | ζ is dimensionless |
| ∂ln K/∂ln a3 | dimensionless | | = ΔΓ23 |
| ∂ln K/∂ρ3, m^app (Pierce) | volume | M⁻¹ = L mol⁻¹ | = ΔΓ23a33/ρ3 |
| m (Smith 2004, LEM) | energy / concentration | kJ mol⁻¹ M⁻¹ | = RT × Pierce's m |
| K_p | dimensionless | | ratio of molalities or of ratios |
| b1 | number / area | H₂O Å⁻² | ≈ 0.18 H₂O Å⁻² (PR08) |
| Krüger F^∞ in G^V = G^∞ + F^∞/L | volume × length | nm⁴ | slope of L·G^V vs L is G^∞ |
| surface excess Γ_j at an interface (Ploetz & Smith 2013, §8.5) | number / area | nm⁻² | not the solute Γ23 |

Rules:
- Pair R with molar quantities and k_B with per-molecule ones. Eq. 34 of Smith 2006a,
  ρ3G23 = φ1Γ23 − ρ3(V̄2 − RTκ_T), balances only if ρ3, V̄2 and RTκ_T are all per mole (C3, cm³ mol⁻¹)
  or all per molecule (nm⁻³, nm³, k_BTκ_T).
- A Γ with units is not Γ23: it is a density-weighted integral, a surface excess, or a slip.
- A KBI quoted without units is ambiguous by a factor of 602 (nm³ vs cm³ mol⁻¹).
- Magnitudes: small-solute |Γ23| is of order 0.1–1 per mol L⁻¹ of cosolute; protein Γ23 of order
  1–100. A caffeine-sized |Γ23| ≫ 1 at 1 mol L⁻¹ signals a scale or bulk-ratio error.
  (inference, order-of-magnitude guide)

## 17. Verification checks and round trips

Use these when checking algebra, code or simulation numerics. "(inference)" marks checks that follow
from the cited identities but are not presented as checks by any source.

**Exact identities (any algebra or code change)**
1. Σ_i ρ_iV̄_i = 1 (Ben-Naim 1977, Eq. 2.9, 10.1063/1.434669).
2. Gibbs–Duhem: ρ_Aμ_AA + ρ_Bμ_AB = 0 (BN77 Eq. 2.7); ternary form in Smith 2008, Eq. 30 (10.1063/1.2982171).
3. G_ij = G_ji, hence ρ_iN_ij = ρ_jN_ji although N_ij ≠ N_ji. Asymmetric measured pairs mean unconverged sampling.
4. Inversion round trip: G_ij → (κ_T, V̄_i, a33 or μ_ij) by the forward relations (kb-integrals.md §3, BN77 Eqs. 2.1–2.6) → G_ij by inversion (kb-integrals.md §14). Inputs must return to machine precision. (inference)
5. Γ23 = φ1(∂m3/∂m2)_{T,P,μ3} + φ3(∂m3/∂m2)_{T,P,μ1}, and (∂m3/∂m2)_{T,P,μ1} = Γ23 − 1/a33 (gamma-linkage.md §6).
6. Σγ_i = Γ and Σv_i = Vol[D] for an exact partition (estimators.md §13).

**Limits with known answers**
7. Ideal gas: all G = 0, k_BTκ_T = 1/ρ, a33 = 1. A closed box biases the raw integral (−0.456 nm³ in the siba-p/kbkit validation); corrections must remove it.
8. Hard spheres: G = (S(0) − 1)/ρ with Carnahan–Starling S(0) (siba-p/kbkit validation).
9. Symmetric ideal mixture: G_ij^SI = k_BTκ_T − V̄_i − V̄_j + Σ_kρ_kV̄_k² (Smith 2008, Eq. 35) gives Δ_AB = 0 (BN77 Eq. 2.14) and ∂ln a/∂ln x = 1.
10. Relabelled water: relabel a random fraction of water molecules as "cosolute". Then G23 = G21 and Γ23 = 0 exactly; any nonzero value is bulk-ratio, closed-box or bookkeeping error. Implicit-solvent analogue: a cosolute interacting with the solute only by excluded volume, whose ρ3G23(δ) must plateau at −ρ3 × excluded volume. (inference)

**Physical constraints**
11. Salts: Γ+ − Γ− = −Z with Z signed (Record & Anderson 1995, Eq. 29, 10.1016/S0006-3495(95)80254-7). Simulated single-ion counts must satisfy it at the plateau; failure means too small a domain or a contaminated bulk region.
12. Stability: η > 0, a33 > 0, μ_ii ≥ 0, μ_ij < 0 for i ≠ j (Smith 2008, Eq. 23); the fluctuation matrix B is positive definite.
13. Closed-box normalisation: ∫ h_ij over the whole periodic box equals −δ_ij/ρ_i (kb-integrals.md §1). Checks RDF normalisation and the integrator.

**Cross-checks between estimators, one trajectory**
14. Molal vs molar with explicit water: Γ23(δ) − ρ3G23(δ) = −ρ3G21(δ), and G21 → k_BTκ_T − V̄2 at infinite dilution without cosolute (Smith 2008, Eq. 34). This yields V̄2 per molecule; compare it with the NpT box-volume difference with and without solute. (inference)
15. Σγ_i plateau versus ρ3(G23 − G21) from solute-centred RDFs with GvdV correction and Krüger extrapolation (simulation.md §2–3).
16. Partition invariance: total Γ must not depend on power, additive or ordinary Voronoi assignment; only site terms may. (inference)
17. r_3 invariance: at large δ the plateau must not depend on the cosolute radius used to build D(δ). (inference)
18. Bulk ratio: n23 − (n3/n1)n21 = Γ23(R)(1 − n21/n1) (estimators.md §9); compare global and moving ratios numerically.
19. Two-domain round trip: Γ = b1·ASA·(m3/m1)(K_p − 1) (Pierce 2008, Eq. 50) must reproduce γ_i where v_i^acc > 0. (inference)
20. Linkage routes: ΔΓ23 (molal) equals [Δ(ρ3G23) + ρ3ΔV̄2]/φ1 (Smith 2006a, Eq. 46, 10.1021/jp056100e).

**Convergence**
21. Converged Γ23 is independent of box size, and agrees between GCMC and NVT with GvdV correction. (inference)
22. Krüger extrapolation: L·G^V linear in L over ≥ 1 nm with R² ≥ 0.99 (KBKit criterion, Peroutka et al. 2026); F^∞ in nm⁴ (§16).
23. Block averages (first versus second half) give sampling error; the spread between estimators gives systematic error (simulation.md §2).

**Pair linkage and slow states** (simulation.md §8; all inference)
24. Finite difference: ΔN23(r) at one composition must match Δln g22(r)/Δln a3 from two nearby compositions, and −½∫g22ΔN23 dr must match ΔB22/Δln a3. Use ΔΓ23 at (T, P). This is the main test on real data.
25. Asakura–Oosawa: run hard spheres with an ideal cosolute through the same counting code. ΔN23(r) must equal ρ3V_overlap(r). It tests the pipeline cheaply.
26. Salt, 1:1: Δ(Γ+ − Γ−)(r) = −Δ⟨Z⟩(r), with Z the solute charge including titrated protons. It is zero only at fixed solute charge; with charge regulation, pairing can shift ⟨Z⟩. Any other charged species in the count must be included in the sum. For dilute fixed point charges, Δ(N2+ + N2−)(r) → ½κZ²ℓ_B e^(−κr).
27. States: where exchange is fast enough to sample, Σ pσ(s3σ + N23^σ) must match the unrestrained N23, using the same bound label throughout.
