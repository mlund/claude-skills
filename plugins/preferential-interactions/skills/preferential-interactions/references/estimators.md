# Equations: counting estimators, bulk ratio, finite-volume KBI (contrast), partitions and site excess

Notation: 1 = water, 2 = solute, 3 = cosolute. ρ_i is a number density and m_i = N_i/N1 a
molality, written as a number ratio, so m3/m1 = ρ3/ρ1. φ_i = ρ_iV̄_i. β = 1/k_BT, and RT replaces
k_BT on molar quantities. h_ij = g_ij − 1. G_ij = G_ji, but N_ij = ρ_jG_ij counts j around i, so
N_ij ≠ N_ji. The superscript ° denotes the solute at infinite dilution (m2 → 0).

Sources give the paper's equation number and DOI; equation numbers were checked against
full texts unless marked. "(inference)" marks a step no cited paper states. Section numbers (§N)
are shared across the equation files; SKILL.md maps each § to its file.

## 8. Counting estimators

Domain-restricted integral (house definition; (inference), the domain generalisation of Pierce Eq. 55 and Ben-Naim Eq. 2.8):

    G_2j(D) ≡ ∫_D h_2j(r) dr,    ⟨N_j(D)⟩ = ρ_jVol[D] + ρ_jG_2j(D)

**8.1 Explicit-solvent (counted-solvent) estimator.** The volume cancels exactly:

    Γ23(D) = ⟨N3(D) − (ρ3/ρ1)N1(D)⟩ = ρ3[G23(D) − G21(D)]  →  Γ23° (molal) as D grows

- Sources:
  - Baynes & Trout 2003, Eq. 4: Γ_XP = ⟨n^II_X − n^II_W(n^I_X/n^I_W)⟩, where II is local and I is bulk, with the ratio inside the average (10.1021/jp0363996).
  - Martínez & Shimizu 2017, Eq. 8: Γ_uc = N_c(R) − (ρ_c/ρ_w)N_w(R) (10.1021/acs.jctc.7b00599).
  - Smith 2004, Eq. 29: ν_sc(R) = n_sc(R) − (ρ_c/ρ_w)n_sw(R) (10.1021/jp0474879).
  - Volume cancellation: Pierce et al. 2008, p. 16, Eq. 55 (10.1007/s12013-007-9005-0).
- A surface origin is allowed for G23 − G21 but not for G23 alone (Pierce p. 16; Smith 2006a, p. 2867).
- RDF route: Γ23 = ρ3(∞)∫(g3 − g1)dV, with g measured from the vdW surface (Shukla et al. 2009, Eq. 7, 10.1021/jp810949t; Baynes & Trout 2003, Eq. 24).
- MDDF route: G_us(R) = [N_us(R) − N*_us(R)]/ρ_s (Martínez & Shimizu 2017, Eq. 2).

**8.2 Implicit-solvent estimator** (water is a continuum):

    Γ_molar(D) = ⟨N3(D)⟩ − ρ3Vol[D] = ρ3G23(D)  →  ρ3G23 (molar, gamma-linkage.md §7)

- The scale identification is cited: Smith 2006a, Eq. 14 (10.1021/jp056100e).
- (inference) The McMillan–Mayer level fixes μ1, which makes the ensemble (T, μ1, μ3).
- D contains the solute, so for a solute core impenetrable to cosolute, Γ_molar(D(0)) = −ρ3Vol[D(0)]: pure excluded volume. Compare Ben-Naim 2012, Eqs. 3.6–3.7 (10.1063/1.4772463).
- Zeindlhofer et al. 2018, Eqs. 5–7 give the same form, Δn_ij = n_ij − N_Ac_jV, with V including the solute (10.1063/1.5009802).
- This estimator does not give the molal Γ23. Convert with gamma-linkage.md §7.

**8.3 Two-domain (local–bulk) form**:

    Γ°3,2 = B3,2 − B1,2 m3/m1                        [Record & Anderson 1995, Eq. 18; 10.1016/S0006-3495(95)80254-7]
    K_p = (B3/B1)/(ρ3/ρ1),   Γ23 = (ρ3/ρ1)(K_p − 1)B1   [Pierce 2008, Eq. 50; Shukla & Trout 2011, Eq. 8; 10.1007/s12013-007-9005-0; 10.1021/jp108586b]

- (inference) With B_i = ⟨N_i(D_loc)⟩, the first line equals §8.1 on D_loc exactly. K_p is defined only relative to the chosen B1.

Salt ions, solute-partitioning model (uncharged solute; Pegram & Record 2008, 10.1021/jp800816a):

    K_p,i ≡ m_i^local / m_i^bulk,   m_i^bulk ≈ ν_i m3                    [Eq. 1 text]
    ν+K_p,+ + ν−K_p,− ≡ ν K_p,3,    ν = ν+ + ν−                          [Eq. 2]
    SFEI ≡ −RT d ln S2/dC3 = −RT ν b1 ASA (1 + ε±) [(ν+K_p,+ + ν−K_p,−)/ν − 1] / m1•   [Eq. 1]

- m1• ≈ 55.5 mol kg⁻¹ (water molality); ε± is the salt nonideality correction; b1 ≈ 0.18 H2O Å⁻² for hydrocarbon and air–water surfaces.
- Single-ion K_p,i are a molal concentration ratio, equivalent to Record's ratio-of-ratios form. Only their ν-weighted sum (K_p,3) enters the thermodynamics, as for Γ+ + Γ−.
- Pegram & Record call b1·ASA "bound water molecules". Keep the phrase in quotation; in house text say "hydration water in the local domain".

## 9. Bulk-ratio choice (closed simulation box)

Moving bulk, taken from what remains outside R:

    Γ23(R) = n23(R) − [(n3 − n23(R))/(n1 − n21(R))]·n21(R)

- Source: Pierce et al. 2008, Eq. 56 (10.1007/s12013-007-9005-0); Shukla et al. 2009, Eq. 3 (10.1021/jp810949t). Vagenende et al. 2009, Eq. 7 (10.1021/jp903413v) uses the same form. Hervø-Hansen et al. 2023, SI Eq. S3 (10.1021/acs.jpcb.3c01085), uses it for caffeine in aqueous salt, preferred over RDF integration for non-spherical solutes because it needs only coordination numbers.
- Notation: n1 and n3 are the box totals. n2j(R) is the raw count within R. Shukla writes n_i(r,t).
- Pierce: "The correction can be significant for protein systems … as the value of n21 can be large."
- Ploetz & Smith 2013, §13 (10.1002/9781118571767.ch4) give the same adjustment: the bulk ratio is the box totals minus what sits in the local region, "especially … for small systems and/or large values of Γ".
- A fixed far bulk instead takes the ratio from a region beyond r* (Baynes & Trout 2003, Eq. 18, 10.1021/jp0363996).

Global-box ratio bias (inference: exact algebra on Pierce Eq. 56):

    n23 − (n3/n1)·n21 = Γ23(R)·(1 − n21/n1)

- The relative underestimate is n21/n1 ≈ V_local/V_box.

RDF analogue, for contrast (Ganguly & van der Vegt 2013, Eq. 5, 10.1021/ct301017q; Simon et al. 2022, Eq. 6):

    g^corr_ij(r) = g_ij(r) · N_j(1 − V_r/V) / [N_j(1 − V_r/V) − ΔN_ij(r) − δ_ij],   V_r = 4πr³/3

## 12. Finite-volume KBI (for contrast only; not for solute-anchored domains)

This is the open subvolume V of a homogeneous fluid:

    G^V_ij = V(⟨N_iN_j⟩ − ⟨N_i⟩⟨N_j⟩)/(⟨N_i⟩⟨N_j⟩) − δ_ij/ρ_i = (1/V)∫_V∫_V h_ij(r12) dr1 dr2
           = ∫₀^L h_ij(r) w(r) dr,   sphere of diameter L: w = 4πr²(1 − 3x/2 + x³/2), x = r/L
    G^V_ij ≈ G^∞_ij + F^∞_ij/L + O(L⁻²),   F^∞_ij = −(3/2)∫₀^∞ r h_ij(r) 4πr² dr,   L = 6V/A

- Sources: Simon et al. 2022, Eqs. 1–2, 9–13 (10.1063/5.0106162); Krüger et al. 2013, Eqs. 2, 5–6 (10.1021/jz301992u), written as x = r/2R.
- Shape enters only through L = 6V/A: Krüger & Vlugt 2018 (10.1103/PhysRevE.97.051301). Simon prints "L = V/(6A)", which is a typo.
- Convex shapes give results linear in A/V: Dawass et al. 2018 (10.1080/00268976.2018.1434908).
- The 1/L term comes from pairs that straddle the boundary: ∫_V dr1 ∫_{outside V} dr2 h = V(G^∞ − G^V) ∼ surface (Krüger 2013, p. 236).
- (inference) Γ23(δ) is a one-point integral anchored on the solute, so this surface law does not apply to it. Judge convergence by the δ plateau instead.

## 13. Partitions and site excess

Ownership rules for a point r. R_i is the radius of solute atom i, and p = r_lig + δ:

    radical (power):       owner = argmin_i [ |r − r_i|² − (R_i + p)² ]
    additively weighted:   owner = argmin_i [ |r − r_i| − R_i ]
    ordinary Voronoi:      owner = argmin_i |r − r_i|

- Power: this is the house definition (SKILL.md). No input paper uses it for Γ.
- Additively weighted: Baynes & Trout 2003, p. 14062, which measures "center of mass of each solvent molecule to the van der Waals surface of every atom" (10.1021/jp0363996). Also Shukla & Trout 2011 (10.1021/jp108586b) and Vagenende & Trout 2012 (10.1016/j.bpj.2012.08.011).
- Ordinary: Martínez & Shimizu 2017, Eq. 6 (10.1021/acs.jctc.7b00599); Martínez 2022 (10.1016/j.molliq.2021.117945). Each count goes to the atom of the minimum-distance pair.
- Voronoi solvation shells (Zeindlhofer et al. 2018, Eqs. 14–17, 10.1063/1.5009802) are whole-molecule cells. Their excess is Δñ_ij(S) = ñ_ij(S) − N_Ac_jṼ(S), resolved by shell rather than by solute site.
- (inference) Properties of the three rules:
  - All three reduce to ordinary Voronoi at equal R_i.
  - Additive ownership is unchanged when the same p is added to every radius, so it does not depend on δ, and the volumes v_i ≥ 0.
  - Power ownership depends on p, so it moves with δ. Its faces are planar, so cell volumes v_i are exact polyhedra.
  - Additive faces are hyperboloids, so additive volumes can only be computed numerically.

Site excess on cells C_i(δ), which partition D(δ):

    implicit solvent:  γ_i = ⟨N_3,i⟩ − ρ3 v_i,                Σ_i γ_i = Γ_molar(D)
    explicit solvent:  γ_i = ⟨N_3,i − (ρ3/ρ1) N_1,i⟩,          Σ_i γ_i = Γ23(D)

- Explicit form: Baynes & Trout 2003, Eqs. 14–15, Γ_XP,i = ⟨n^II_X,i − (n^I_X/n^I_W)n^II_W,i⟩ (10.1021/jp0363996). The sum is exact only if every local molecule is assigned to exactly one group.
- Residue form: Vagenende & Trout 2012, Eqs. 2–3 (10.1016/j.bpj.2012.08.011).
- Overlapping cutoffs break the sum: Vagenende et al. 2009, p. 11748 (10.1021/jp903413v).
- The implicit-solvent form is the house definition (SKILL.md). No input paper defines it.
- (inference) KB reading: γ_i = ρ3[∫_{C_i} h23 dr − ∫_{C_i} h21 dr] is a cell-restricted piece of §8.1. Atom-centred integrals G_i3 − G_i1 each converge to the *whole* G23 − G21 for a rigid solute, so they cannot partition Γ.
