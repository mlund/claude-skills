# Glossary: preferential interactions and Kirkwood–Buff terms

House terms are in **bold** and follow SKILL.md. Rows give the house term, the symbol, a short
definition, each school's usage with its own DOI, and pitfalls. "avoid" marks a term the house
style does not use in its own voice. Keep such terms only inside quotations or when you describe
the cited paper's model. Page and equation numbers are the cited paper's own. For equations, see the
equation files listed in SKILL.md.

House notation: 1 = water, 2 = solute, 3 = cosolute. ρ_i is a number density. Γ23 is the
preferential interaction coefficient with the solute index first. N_ij = ρ_jG_ij counts j around i.

## Contents

1. [Components and roles](#1-components-and-roles)
2. [KB integrals and distribution functions](#2-kb-integrals-and-distribution-functions)
3. [Preferential quantities and ensembles](#3-preferential-quantities-and-ensembles)
4. [Concentration scales and activities](#4-concentration-scales-and-activities)
5. [Linkage and experiment](#5-linkage-and-experiment)
6. [Domains, estimators and partitions](#6-domains-estimators-and-partitions)
7. [Salts](#7-salts)
8. [Sign and interpretation words](#8-sign-and-interpretation-words)
9. [Symbol collisions](#9-symbol-collisions)

Short source keys used below. Each row also gives the DOI.
P08 Pierce et al. 2008 · S04 Smith 2004 · S06a Smith 2006 JPCB · S06b Smith 2006 BJ ·
Sh04 Shimizu 2004 · K12 Karunaweera et al. 2012 · RA95 Record & Anderson 1995 · ACR02 Anderson,
Courtenay & Record 2002 · PR08 Pegram & Record 2008 · BT03 Baynes & Trout 2003 · SST09 Shukla, Shinde & Trout 2009 ·
ST11 Shukla & Trout 2011 · VYT09 Vagenende, Yap & Trout 2009 · VT12 Vagenende & Trout 2012 ·
Z17/Z18 Zeindlhofer et al. 2017/2018 · MS17 Martínez & Shimizu 2017 · M22 Martínez 2022 ·
BN88/BN12 Ben-Naim 1988/2012 · M84 Matteoli & Lepori 1984 · Simon22 Simon et al. 2022 · HD14 Heyda & Dzubiella 2014 · HHL23 Hervø-Hansen et al. 2023 ·
K13 Krüger et al. 2013 · D18 Dawass et al. 2018 · G13 Ganguly & van der Vegt 2013 ·
KV18 Krüger & Vlugt 2018 · BN77 Ben-Naim 1977 · Smith08 Smith 2008.

---

## 1. Components and roles

| Term | Symbol | Definition | Variants by school (DOI) | Pitfalls / conflicts |
|---|---|---|---|---|
| **water** (solvent) | 1 | The primary solvent. | "primary solvent (water)" P08 p. 2 (10.1007/s12013-007-9005-0); "w" S04 (10.1021/jp0474879), MS17 (10.1021/acs.jctc.7b00599); "W" BT03 (10.1021/jp0363996); "solvent (1)" RA95 (10.1016/S0006-3495(95)80254-7); A, B = solvent components BN88 (10.1007/BF02918361) | Scatchard numbering (ST11, 10.1021/jp108586b). Implicit-solvent (McMillan–Mayer) work has no component-1 particles; say so. |
| **solute** | 2 | The molecule whose environment is studied: a protein, nucleic acid or small molecule such as caffeine. | "biomolecule solute" P08 (10.1007/s12013-007-9005-0); "s" S04 (10.1021/jp0474879); "u" MS17 (10.1021/acs.jctc.7b00599); "P" BT03 (10.1021/jp0363996); "polymer or polyelectrolyte (2J)" RA95 (10.1016/S0006-3495(95)80254-7); "S" BN88 (10.1007/BF02918361); "solute i" Z18 (10.1063/1.5009802) | Letters collide: in MS17, s = *solvent*. In BN12 (10.1063/1.4772463), s = an added "solute" that the house style calls a cosolute. In M84 (10.1063/1.447034) the organic cosolvent is "solute" 2. |
| **cosolute** | 3 | The added species: osmolyte, denaturant or salt ions. | "cosolvent" P08, S04 (10.1007/s12013-007-9005-0; 10.1021/jp0474879), BT03 "X" (10.1021/jp0363996), MS17 "c" (10.1021/acs.jctc.7b00599); "cosolute" ST11 (10.1021/jp108586b); "solute (3)" / "perturbing solute" RA95, ACR02 (10.1016/S0006-3495(95)80254-7; 10.1021/jp012627p); "osmolyte (i = 3)" Sh04 (10.1073/pnas.0305836101); "co-solvent" Z17 (10.1039/c6ra24736a) | "Cosolute" appears in none of the KB-foundation papers (Simon22, K13, G13, BN, M84, MS17). Translate when you cite them. |
| cosolvent — **avoid** | — | Used for any non-water small component. | P08 p. 1 "anything other than the primary solvent" (10.1007/s12013-007-9005-0); BT03 (10.1021/jp0363996); MS17 (10.1021/acs.jctc.7b00599) | Avoid it for salts, which are not solvents. Keep it only in quotations. |
| biomolecule — **avoid** for small solutes | — | The Smith/Shimizu word for component 2. | P08 (10.1007/s12013-007-9005-0); Sh04 (10.1073/pnas.0305836101) | Wrong for caffeine-sized solutes. Use "solute". |
| osmolyte | — | A cosolute that stabilises the native state, classed by its effect. | P08 p. 1, set against denaturant (10.1007/s12013-007-9005-0); Sh04 uses it for any component 3 in osmotic-stress analysis (10.1073/pnas.0305836101) | This is a role word, not a component number. |
| denaturant | — | A cosolute with Γ_D3 > Γ_N3, which shifts N ⇌ D toward D. | P08 p. 3 (10.1007/s12013-007-9005-0); ACR02 "perturbing solute" classes (10.1021/jp012627p) | The classification is thermodynamic, not mechanistic. |
| component (electroneutral) | 2J, 3 | An electroneutral species or combination of species. | ACR02 p. 419 (10.1021/jp012627p); RA95 Appendix (10.1016/S0006-3495(95)80254-7) | Narrower than "species". A salt is one component but two species. |
| ligand — **avoid** | — | Older manuscript word for the cosolute. | foundations notes (main.tex); RA95 "bound 'as ligand'" water (10.1016/S0006-3495(95)80254-7) | Implies site binding. Use "cosolute". |
| McMillan–Mayer (implicit-solvent) level | — | Water is a continuum and μ1 is implicitly fixed. | scale relation S06a Eq. 14 (10.1021/jp056100e); ensemble identification is an inference | The water term in Γ is absent, not absorbed. Γ then converges to the molar ρ3G23 (§3). |
| Hofmeister salt | — | A salt cosolute classed by its Hofmeister-series effect. | ACR02 p. 418 (10.1021/jp012627p); Pegram & Record 2008 (10.1021/jp800816a) | A salt is two species, so report Γ± (§7). |

Conflicts in brief:
- Numbering versus letters: 1/2/3 (P08, 10.1007/s12013-007-9005-0; RA95; ST11) versus s/c/w
  (S04, 10.1021/jp0474879, which uses both systems), X/W/P (BT03, VYT09, VT12) and u/s/w/c (MS17).
  Give a one-line mapping when you cite a letter-labelled paper.
- The Trout group switches from "cosolvent" (2003–2012) to "cosolute" (ST11, 10.1021/jp108586b).
- In Schröder's papers the small molecule is the *solute* and the ionic liquid the "co-solvent"
  (Z18, 10.1063/1.5009802).

---

## 2. KB integrals and distribution functions

| Term | Symbol | Definition | Variants by school (DOI) | Pitfalls / conflicts |
|---|---|---|---|---|
| **Kirkwood–Buff integral (KBI)** | G_ij | G_ij = 4π∫₀^∞[g_ij^{μVT}(r) − 1]r²dr in the open system at infinite range. | P08 Eq. 11 (10.1007/s12013-007-9005-0); G13 Eq. 1 (10.1021/ct301017q); G^∞_ab Simon22 Eq. 3 (10.1063/5.0106162); G^∞_αβ K13 Eq. 3 (10.1021/jz301992u); G_AB BN88 Eq. 2.4 (10.1007/BF02918361); "KB parameter" Sh04 (10.1073/pnas.0305836101); ΔG_ij Z17 (10.1039/c6ra24736a) | Do not write it as ΔG_ij (Z17), because Δ means a stoichiometric difference. Units vary: cm³ mol⁻¹ (M84, 10.1063/1.447034), nm³ (G13), L mol⁻¹ (MS17), σ³ (Simon22). State yours. |
| KBI, fluctuation form | G_ij | G_ij = V[(⟨N_iN_j⟩ − ⟨N_i⟩⟨N_j⟩)/(⟨N_i⟩⟨N_j⟩) − δ_ij/⟨N_i⟩] for an open region. | P08 Eq. 12 (10.1007/s12013-007-9005-0); Simon22 Eqs. 1–2 (10.1063/5.0106162) | In a closed system ρ_jG_ij = −δ_ij (P08 p. 5; BN88 Eq. 2.6), which is not the KBI. |
| **excess coordination number** | N_ij = ρ_jG_ij | The excess of j around i over a bulk reference at the same μ. N_ij ≠ N_ji. | P08 p. 5, S04, S06a (10.1007/s12013-007-9005-0; 10.1021/jp0474879; 10.1021/jp056100e); N_2i = n_iN_AG_2i "excess solvation number" Sh04 Eq. 4 (10.1073/pnas.0305836101); ΔN_ab(L) Simon22 Eq. 7 (10.1063/5.0106162); "excess (or deficiency) number" ρ_jG_ij M84 (10.1063/1.447034) | The term is not used in the foundation papers. Cite P08. For proteins, N21 and N23 are negative because excluded volume dominates them (S06a p. 2867). |
| cumulative coordination number | n_ij(R) | A raw count within R: n_ij(R) = 4πρ_j∫₀^R g_ij r²dr. N_ij(R) = n_ij(R) − (4/3)πR³ρ_j. | P08 Eq. 55 (10.1007/s12013-007-9005-0); S04 Eq. 30 (10.1021/jp0474879) | Lower-case n is a count and upper-case N an excess. Keep the two visibly distinct. |
| **running KBI** | G̃_ij(R) | The KBI truncated at a finite radius R. | "running KBI" G̃^L_ab Simon22 Eq. 4 (10.1063/5.0106162); "standard, truncated KB-integral" G̃^R K13 Eq. 4 (10.1021/jz301992u); RKBI G_ij(r) G13 Eq. 2 (10.1021/ct301017q); truncated G_ij S04 Eq. 28 (10.1021/jp0474879) | It does *not* measure fluctuations in a volume of size R (K13 p. 236; Simon22 p. -5). Judge convergence by a plateau. |
| **solute-anchored running KBI** | G23(D), Γ23(δ)/ρ3 | A running integral over a solute-shaped domain D(δ). | distance-dependent KBI G_us(R) MS17 Eq. 2 (10.1021/acs.jctc.7b00599); ν_sc(R) S04 Eq. 29 (10.1021/jp0474879); Γ23(R) P08 Eq. 56 (10.1007/s12013-007-9005-0) | **Not** a finite-volume KBI. The 1/L surface law does not apply to it (KV18, 10.1103/PhysRevE.97.051301; D18 convex only, 10.1080/00268976.2018.1434908). |
| local region (fluctuation theory) — **avoid** for D(δ) | — | An open sub-volume of bulk solution, with random origin, whose particle and energy fluctuations give bulk properties. | Ploetz & Smith 2013 §§5, 13 (10.1002/9781118571767.ch4) | Not solute-anchored. For the domain around a solute, say integration domain D(δ). |
| finite-volume KBI — **avoid** for solute-anchored quantities | G^V_ij | The fluctuation integral of a fixed open subvolume: (1/V)∫_V∫_V h(r12) = ∫h(r)w(r)dr. | Simon22 Eqs. 1–2, 9–11 (10.1063/5.0106162); K13 Eq. 2 (10.1021/jz301992u); Schnell 2011 (10.1021/jp204347p); "SKBI" G_ij(L_s) G13 Eq. 3 (10.1021/ct301017q) | Reserve it for the Schnell/Krüger/Simon quantity. Calling Γ(δ) a "finite-volume KBI" is a category error. |
| surface term | F^∞_ij, L | G^V = G^∞ + F^∞/L + O(L⁻²), with F^∞ = −(3/2)∫r h 4πr²dr and L = 6V/A. | Simon22 Eqs. 12–13 (10.1063/5.0106162); K13 p. 236 (10.1021/jz301992u); KV18 (10.1103/PhysRevE.97.051301) | Simon22 prints "L = V/(6A)", a typo. L means a radius in Simon22 Eq. 4, a diameter in Eq. 11, and 2R in K13 (10.1021/jz301992u). Define L. |
| small-system method | — | Fluctuations in subvolumes, extrapolated in 1/L. | D18 (10.1080/00268976.2018.1434908); "sub-box method" G13 (10.1021/ct301017q) | Belongs to the finite-volume family only. |
| radial distribution function | g_ij(r) | The pair correlation of centres in an isotropic system. h = g − 1. | all papers, e.g. P08 p. 4, centre of mass (10.1007/s12013-007-9005-0); PCF K13 (10.1021/jz301992u); "orientationally averaged" BN88 (10.1007/BF02918361) | Avoid the acronym "PDF" (Simon22, 10.1063/5.0106162). |
| closed-system RDF and corrections | g̃_ij, g^{NpT}_ij | In a closed box g → 1 − c/V₀. Corrections are the Ganguly–van der Vegt renormalisation and Ben-Naim's constant shift. | G13 Eq. 5 (10.1021/ct301017q); Simon22 Eqs. 6, 8 (10.1063/5.0106162); K13 Eq. 9 (10.1021/jz301992u) | Simon22's tilde means "running" in Eq. 4 and "canonical" in Eqs. 6–8. Do not reuse the tilde. |
| minimum-distance distribution function (MDDF) | g^md_us(r) | n_us(r)/n*_us(r): the count at minimum distance to any solute atom, divided by the same count around a non-interacting "phantom" solute. | MS17 Eq. 1 (10.1021/acs.jctc.7b00599); M22 (10.1016/j.molliq.2021.117945) | Each count goes to the closest solute atom, which is ordinary Voronoi ownership (§6). |
| proximal / surface-distance RDF | g_i(r) | Density at distance r from the solute's vdW surface, divided by the bulk density. | BT03 Eq. 20 (10.1021/jp0363996); SST09 Eq. 7 (10.1021/jp810949t) | Normalising by spherical-shell volume misleads where the solute excludes volume (Z17 p. 3496, 10.1039/c6ra24736a). |
| correlation region / volume | R, R_c, V_cor | The region beyond which g = 1. | BN88 Eq. 2.7 (10.1007/BF02918361); S04 Eq. 28 (10.1021/jp0474879); "correlation length ξ" K13 (10.1021/jz301992u) | BN88's N_A,S(R_c) = ρ_AG_AS + ρ_AV_cor is the house ⟨N⟩ = Γ + ρ3Vol identity. |
| excluded volume | V_E, V^EX | The volume that is inaccessible to solvent centres. It enters G with a minus sign. | V_E = V_I + V_T Sh04 p. 1196 (10.1073/pnas.0305836101); V^EX_Fw BN12 Eqs. 3.6–3.7 (10.1063/1.4772463); "excluded volume of the solute" M22 (10.1016/j.molliq.2021.117945); salt-depleted shell ΔV, ΔΓ23 ≃ −cΔV, HD14 p. 10984 (10.1021/jp5041635) | It depends on the partner (water versus cosolute). Sh04's N′_2i = N_2i + n_iV_E removes it, and Smith keeps it. |
| Kirkwood interaction volume | I_ij | G_ij = −V_i + I_ij, where V_i is the solute volume where g = 0. | Z18 Eqs. 8–9 (10.1063/1.5009802) | A negative G is not repulsion. |
| fluctuation matrix, stability determinant | B_ab, η | B_ab = ρ_aρ_bG_ab + ρ_aδ_ab. Binary η = ρ1 + ρ2 + ρ1ρ2(G11 + G22 − 2G12) > 0. | Simon22 Eqs. 16, 25 (10.1063/5.0106162); BN12 Eqs. 3.3, 4.4 (10.1063/1.4772463) | Simon22 Eq. 27 prints −δ_abρ_a, a typo. Use +. |
| thermodynamic factor — **avoid** the symbol Γ | Γ^GC | The matrix A^GC = (B^GC)⁻¹. | Simon22 Eq. 21 (10.1063/5.0106162); "thermodynamic correction factor" G13 (10.1021/ct301017q) | It clashes with Γ23. Rename it or spell it out. Do not call a33 a thermodynamic factor (§4). |
| ideal-solution KBI | G^SI_ij | KBIs of a symmetric ideal solution are nonzero. Only differences signal nonideality. | Ploetz 2010 (10.1063/1.3398466); M84 G12 = (G11 + G22)/2 (10.1063/1.447034) | It is a different "ideal" from the bulk reference (§8). |
| thermodynamic limit | G∞, V → ∞ | The value of the KBI at infinite volume. | Simon22 (10.1063/5.0106162); "limiting KBIs" G13 (10.1021/ct301017q) | The plain G_ij in house style already means this limit. |
| KB inversion | — | Recovers G_ij from κ_T, the PMVs V̄_i and the chemical-potential derivatives μ_ij (a33 in a binary solvent); see kb-integrals.md §14. | BN77 (10.1063/1.434669); Smith08, n components (10.1063/1.2982171); applied to caffeine–salt with activity derivatives from fitted ln γ and VPO, HHL23 (10.1021/acs.jpcb.3c01085) | BN77 is the original inversion (binary, water–ethanol); its Eqs. 2.1–2.13 were checked against the full text (kb-integrals.md §14). |
| open-system derivative | — | k_BT(∂ρ_i/∂μ_j)_{T,V,μ′} = ρ_iρ_jG_ij + ρ_iδ_ij. | P08 Eq. 13 (10.1007/s12013-007-9005-0); S06a Eq. 4 (10.1021/jp056100e) | It is exact only in the open ensemble. Closed-system derivatives need matrix inversion (Simon22). |
| excess solvation number, shell-corrected | N′_2i | N′_2i = N_2i + n_iV_E, with the excluded-volume part removed. | Sh04 Eq. 5 (10.1073/pnas.0305836101) | Shimizu only. Smith keeps excluded volume inside N_2j. |
| solvation shell | 1st, 2nd | Defined by g(r) minima or by Voronoi neighbour order. | BT03 (10.1021/jp0363996); Z17 (10.1039/c6ra24736a); "two hydration layers" VYT09 (10.1021/jp903413v) | The distance-based and topological definitions differ. |
| proximity criterion | — | Assigns each solvent molecule to its nearest solute atom. | Mezei & Beveridge 1986 (10.1016/0076-6879(86)27005-6); Mezei 1988 (10.1080/08927028808080954) | Historical origin of nearest-atom domains. |

Conflicts in brief:
- Limit marker: G∞ (Simon22, 10.1063/5.0106162) versus a plain G_ij (G13, 10.1021/ct301017q; P08).
  The house style uses a plain G_ij for the limit and G̃ or an argument (R, D) for truncated forms.
- Ensemble label: "open", "grand-canonical", "μVT" and "T, V, μ" are interchangeable
  (BN88, 10.1007/BF02918361; G13; S04, 10.1021/jp0474879).
- "Running", "truncated" and "RKBI" name the same object (Simon22; K13, 10.1021/jz301992u; G13).
  The finite-volume G^V is a different object. MS17's G_us(R) is a running integral over a
  solute-shaped domain (10.1021/acs.jctc.7b00599).

---

## 3. Preferential quantities and ensembles

| Term | Symbol | Definition | Variants by school (DOI) | Pitfalls / conflicts |
|---|---|---|---|---|
| **preferential interaction coefficient** | Γ23 | Γ23 = (∂m3/∂m2)_{T,μ1,μ3}, the equilibrium-dialysis coefficient. Γ23 = ρ3(G23 − G21) at m2 → 0. | Γ3,2 RA95 Eq. 4 (10.1016/S0006-3495(95)80254-7); Γ_μ1,μ3 ACR02 Eq. 4 (10.1021/jp012627p); Γ23 P08 Eqs. 1, 21 (10.1007/s12013-007-9005-0); Γ^m_{XP,μW,μX,T} VYT09 Eq. 2 (10.1021/jp903413v); ν_sc S04 Eq. 6 (10.1021/jp0474879); Γ_uc MS17 Eq. 7 (10.1021/acs.jctc.7b00599) | Index order differs: RA95 and BT03 put the cosolute first, and Smith and ST11 put the solute first. ST11 (10.1021/jp108586b) defines Γ23 at (T, P, μ3) and calls dialysis an approximation. State the ensemble and the scale. |
| preferential binding parameter / coefficient — **avoid** | Γ23, Γ_XP | Smith's and Trout's name for Γ. | P08 (10.1007/s12013-007-9005-0); BT03 Eq. 3 Γ_XP ≡ (∂m_X/∂m_P)_{μX} (10.1021/jp0363996); "preferential binding" = (∂m3/∂m2)_{T,P,μ3} for Timasheff (via S06a p. 2868, 10.1021/jp056100e) | It implies site binding. RA95 and ACR02 note the cosolute "interacts with, but does not actually bind to" the solute (10.1021/jp012627p). |
| preferential interaction parameter — **avoid** | (∂μ2/∂m3) | Timasheff's chemical-potential cross derivative (∂μ3/∂m2)_{T,P,m3} = (∂μ2/∂m3)_{T,P,m2}. | reported in S06a p. 2868 (10.1021/jp056100e); MS17 uses "parameter" for Γ (10.1021/acs.jctc.7b00599); SST09 too (10.1021/jp810949t); HD14 p. 10980 names (∂m3/∂m2)_{T,μ1,μ3} so (10.1021/jp5041635) | This derivative differs from Γ23. Never use the name as a synonym for Γ23. |
| preferential solvation parameter — **avoid** | Γ | MS17's third name for Γ. | MS17 abstract (10.1021/acs.jctc.7b00599) | It collides with Ben-Naim's δ_A,S (below). |
| Ben-Naim preferential solvation index | δ_A,S, δ⁰_A,S | δ_A,S = x_A,S(local) − x_A = x_Ax_B(G_AS − G_BS)/(x_AG_AS + x_BG_BS + V_cor). | BN88 Eqs. 2.10–2.14 (10.1007/BF02918361); BN12 Eqs. 4.5–4.7 (10.1063/1.4772463) | It is based on mole fractions and has a different normalisation from Γ, with the same sign as G_AS − G_BS. The δ collides with δ_ij and with domain thickness (§9). |
| semi-open (T, P, μ3) coefficient | (∂m3/∂m2)_{T,P,μ3} | Equals Γ23 + φ3/(a33φ1) at m2 → 0, and −(∂μ2/∂μ3)_{T,P,m2}. | Γ′23 S04 Eq. 16 (10.1021/jp0474879); P08 Eqs. 3–4, 23 (10.1007/s12013-007-9005-0); Γ_μ3 ACR02 Eq. 3a (10.1021/jp012627p); Γ23 ST11 Eq. 1 (10.1021/jp108586b) | The offset depends only on the solvent and is the same for every solute (S06a Eqs. 25–27, 10.1021/jp056100e). It is not negligible for small solutes. |
| osmotic (T, P, μ1) coefficient | (∂m3/∂m2)_{T,P,μ1} | Equals Γ23 − 1/a33, measured by VPO or isopiestic methods. It is nonzero even without interactions. | Γ″23 S04 Eq. 17 (10.1021/jp0474879); P08 Eq. 24 (10.1007/s12013-007-9005-0); Γ_μ1 ACR02 Eq. 1a (10.1021/jp012627p) | ACR02's Γ_μ1 is *not* the dialysis coefficient. Its sign can differ from Γ_μ3 (ACR02 p. 428). |
| ensemble | — | The variables held fixed. Dialysis is (T, μ1, μ3) with V implicitly fixed, and "T, P, μ" for all components is meaningless. | S06a p. 2865 (10.1021/jp056100e); P08 Eq. 1 (10.1007/s12013-007-9005-0); Sh04 writes ν21 at (T, P, μ1) (10.1073/pnas.0305836101) | Always write the subscripts. BT03 writes only μ_X (10.1021/jp0363996). |
| open / semi-open / closed | — | Open: T, V, μ_all. Semi-open: T, P, μ3 or T, P, μ1. Closed: T, P, N. | S06b pp. 851–853 (10.1529/biophysj.105.078790); P08 Table 1 (10.1007/s12013-007-9005-0) | Spelling varies (semiopen, semi-open, semi open). The house style uses "semi-open". |
| simulation ensemble | NPT, NVT | The ensemble used to estimate the μVT quantity. | VYT09 p. 11745 "approximation" (10.1021/jp903413v); SST09 "calculated in the NTP ensemble" (10.1021/jp810949t) | Simulating in NPT does not make Γ the (T, P) coefficient. State which coefficient the estimator targets. |
| **molar-scale coefficient** | ρ3G23 | (∂ρ3/∂ρ2)_{T,μ1,μ3} = ρ3G23 = N23. | S06a Eq. 14 (10.1021/jp056100e); molar two-domain form RA95 Eq. A6 (10.1016/S0006-3495(95)80254-7) | It contains the solute's excluded volume and is large and negative for proteins. Never call it plain "Γ". |
| mole-fraction coefficient | (∂x3/∂x2)_{T,μ1,μ3} | Equals −x3 + x1ρ3(G23 − G21). | S06a Eq. 16 (10.1021/jp056100e) | — |
| weight-based coefficient | ξ23 | (∂w3/∂w2), with Γ23 = (M2/M3)ξ23. | S06a Eq. 1 (10.1021/jp056100e) | Eisenberg's density-increment quantity. |
| preferential hydration coefficient | Γ21, ν21 | The water analogue. P08 Eq. 39 gives ΔΓ21 = −(ρ1/ρ3)ΔΓ23. Sh04 gives ν21 = N21 − (n1/n3)N23. | P08 Eqs. 39–41 (10.1007/s12013-007-9005-0); Sh04 Eqs. 1, 3, molarity n_i (10.1073/pnas.0305836101) | The 1 ↔ 3 swap is invalid unless molality is redefined (P08 p. 11). |
| infinite dilution | superscript ° or ∞ | The m2 → 0 limit. | "o" P08, "zero superscript" S06a (10.1021/jp056100e); Γ°3,2 RA95 (10.1016/S0006-3495(95)80254-7); °(2) ACR02 Eq. 13a (10.1021/jp012627p) | In Sh04, superscript 0 means n3 → 0, the cosolute-free limit (10.1073/pnas.0305836101). Say which limit you mean. |

Conflicts in brief:
- Names for Γ23: "preferential binding parameter" (P08), "preferential interaction" (S04),
  "preferential interaction parameter(s)" (S06a/b titles), "preferential interaction coefficient"
  (RA95, ACR02, ST11) and "preferential binding coefficient" (BT03). Translate all of them to
  Γ23 and say which ensemble each paper meant (10.1021/jp056100e; 10.1021/jp0363996).
- Constants written for the dialysis coefficient: (T, μ1, μ3) in P08, S04, RA95 and VYT09;
  (T, V, μ1, μ3) in S06a; (T, P, μ3) in ST11 and BT03; (T, P, μ1) for Sh04's ν21
  (10.1073/pnas.0305836101).

---

## 4. Concentration scales and activities

| Term | Symbol | Definition | Variants by school (DOI) | Pitfalls / conflicts |
|---|---|---|---|---|
| **number density** | ρ_i | ρ_i = ⟨N_i⟩/V. | Simon22, G13, BN12, MS17 (10.1063/5.0106162; 10.1021/ct301017q; 10.1063/1.4772463; 10.1021/acs.jctc.7b00599); "number density (molar concentration)" S04 (10.1021/jp0474879); c_α K13 (10.1021/jz301992u); n_i "density (molarity)" Sh04 (10.1073/pnas.0305836101) | Do not use c or n for it. MS17 converts to molarity by "multiplying" by N_A, which is wrong: divide. |
| **molality** | m_i | m_i = N_i/N1, a number ratio, or mol per kg of water. | P08 p. 3, S06a (10.1007/s12013-007-9005-0; 10.1021/jp056100e); ACR02 Table 1 fn. a counts all water, bound or not (10.1021/jp012627p); m₃^bulk RA95 (10.1016/S0006-3495(95)80254-7) | The ratio forms (m3/m1 = ρ3/ρ1) are scale-free. |
| **molarity** | C_i | mol L⁻¹. | C_c salt molarity S04 (10.1021/jp0474879); C₃^bulk RA95 Eq. A6 (10.1016/S0006-3495(95)80254-7); c3 axes P08 (10.1007/s12013-007-9005-0) | — |
| mole fraction | x_i | — | BN88 (10.1007/BF02918361); M84 (10.1063/1.447034); S06a (10.1021/jp056100e) | Ben-Naim's preferential solvation is based on mole fractions. |
| volume fraction | φ_i | φ_i = ρ_iV̄_i. | S04 p. 18718 (10.1021/jp0474879); P08 p. 6 (10.1007/s12013-007-9005-0) | — |
| partial molar volume | V̄_i | V̄2° = RTκ_T − N21V̄1 − N23V̄3. | P08 Eq. 28 (10.1007/s12013-007-9005-0); Sh04 Eq. 12 (10.1073/pnas.0305836101); BN12 Eq. 3.5, ΔV → G_Uw − G_Fw (10.1063/1.4772463); "partial molal" M84 (10.1063/1.447034) | MS17 equates −G_uw with the apparent molar volume at infinite dilution (10.1021/acs.jctc.7b00599). |
| isothermal compressibility | κ_T | For a pure fluid, k_BTκ_Tρ = 1 + ρG. | Simon22 Eq. 23 (10.1063/5.0106162); K_T M84 Eq. 2 (10.1063/1.447034) | — |
| activity | a_i, a± | a3 on any scale in ∂ln K/∂ln a3. For salts, a_c = a±. | P08 Eq. 5 (10.1007/s12013-007-9005-0); S04 (10.1021/jp0474879); RA95 Eq. 2 (10.1016/S0006-3495(95)80254-7) | ACR02 differentiates against ln a3 with a factor ν. RA95 uses ln a± (§7). |
| **activity derivative** | a33 | a33 = (∂ln a3/∂ln ρ3)_{T,P} = 1/[1 + ρ3(G33 − G13)] ≈ φ1/(1 + N33). | P08 Eqs. 15, 19 (10.1007/s12013-007-9005-0); a_cc S04 Eq. 2 (10.1021/jp0474879) | Do not call it "thermodynamic factor" or "stability". a33 > 0 in real solutions. Urea has a33 ≈ 1 on the molar scale, and TFE has a33 ≈ 0.2. |
| chemical-potential derivatives — **avoid** bare | μ23, μ33 | S04: μ23 = β(∂μ2/∂ln m3), reduced and logarithmic. | S04 App. 2 (10.1021/jp0474879); μ33 ACR02 Eq. 13a (10.1021/jp012627p) | Timasheff's μ23 = (∂μ2/∂m3) is neither reduced nor logarithmic. Define the symbol inline. |
| pseudo-chemical potential | μ_i* | Ben-Naim's chemical potential without the liberation term. | P08 p. 5 (10.1007/s12013-007-9005-0); S04 Eq. 3 (10.1021/jp0474879); BN88 p. 263 (10.1007/BF02918361) | Spelling varies: "pseudochemical" in S06b (10.1529/biophysj.105.078790). |
| activity coefficients | γ, y, f | Molal, molar and mole-fraction activity coefficients. | P08 Eq. 14 (10.1007/s12013-007-9005-0) | γ collides with the house site excess γ_i. Write γ_i only for sites. |

---

## 5. Linkage and experiment

| Term | Symbol | Definition | Variants by school (DOI) | Pitfalls / conflicts |
|---|---|---|---|---|
| **Wyman linkage** | — | (∂ln K/∂ln a3)_{T,P} = ΔΓ23 at m2 → 0. | P08 Eq. 5 (10.1007/s12013-007-9005-0); RA95 Eq. 1 with the dialysis Γ (10.1016/S0006-3495(95)80254-7); S04 Eq. 9 Δν_sc (10.1021/jp0474879); S06a Eq. 45 "any ensemble" (10.1021/jp056100e) | Pairing the dialysis Γ with a (T, P) linkage is exact *for 1:1 processes* (P08 p. 9). Do not "correct" it. |
| concentration-scale linkage | — | (∂ln K/∂ln ρ3)_{T,P} = ΔΓ23·a33. | P08 Eq. 32 (10.1007/s12013-007-9005-0) | The note gamma_in_kb.md wrote ÷a33. That is wrong (verification). |
| salt derivative | S_aK_obs | S_aK_obs ≡ ∂ln K_obs/∂ln a± = Δ(Γ+ + Γ−). | RA95 Eqs. 2, 42 (10.1016/S0006-3495(95)80254-7); S_aK_obs = Δ\|Z\| + νΔΓ_μ3 ACR02 Eqs. 6–7 (10.1021/jp012627p) | K_obs is in molar concentrations (RA95). |
| m-value | m | βΔΔG = −mρ3, and m^app = ΔΓ23a33/ρ3. | P08 Eqs. 42–43 (10.1007/s12013-007-9005-0); ΔΔG = −mC_c, "LEM" S04 Eq. 21 (10.1021/jp0474879); S06a p. 2868, m > 0 for accumulation (10.1021/jp056100e) | Units clash: M⁻¹ (P08) versus kJ mol⁻¹ M⁻¹ (S04). Spelling varies: "m value" or "m-value". State the units. |
| equilibrium dialysis | Γ^exp3,2 | (m3^total(α) − m3(β))/m2 across a membrane permeable to 1 and 3. | RA95 Eqs. 7, 10 (10.1016/S0006-3495(95)80254-7); S06a p. 2865 (10.1021/jp056100e) | It measures the (T, μ1, μ3) coefficient. |
| vapour-pressure osmometry, isopiestic distillation | — | These measure the (T, P, μ1) coefficient. | S04 p. 18719 (10.1021/jp0474879); ACR02 (10.1021/jp012627p); Courtenay 2000 (10.1021/bi992887l) | Convert to Γ23 with −1/a33 (§3). |
| Wyman/Tanford binding numbers | B3, B1 | Γ23 = B3 − (ρ3/ρ1)B1. In KB terms, B_i are excess numbers over the whole solution. | P08 Eqs. 2, 6 (10.1007/s12013-007-9005-0); S04 p. 18718 (10.1021/jp0474879) | In RA95 (10.1016/S0006-3495(95)80254-7), B_i,2 instead means *local-domain* contents. They are not virial coefficients. |
| site-binding model — **avoid** for Γ | Δn, K_b | βΔΔG = −Δn ln(1 + K_bρ3). | P08 Eq. 47, "clearly incorrect for weak binding cosolvents" (10.1007/s12013-007-9005-0) | It implies 2:3 complexes. |
| exchange model | K_e | βΔΔG = −Δn ln(a1 + K_ea3) (Schellman). It allows Γ < 0. | P08 Eq. 48 (10.1007/s12013-007-9005-0); S1,3 link RA95 Eq. 54 (10.1016/S0006-3495(95)80254-7) | — |
| transfer free energy | Δμ^tr_P | ≈ −RTΓ_XP when Γ is proportional to m_X. | BT03 Eqs. 1–7 (10.1021/jp0363996) | — |
| cosolute effect on μ2* | — | −β(∂μ2*/∂ln ρ3)_{T,P} = Γ23a33. A positive Γ means salting in. | P08 Eq. 26 (10.1007/s12013-007-9005-0); S04 Eq. 5 (10.1021/jp0474879) | — |
| osmotic stress analysis | OSA | It assumes ΔN′21 = Δν21⁰, "merely an assumption". | Sh04 Eq. 15 (10.1073/pnas.0305836101) | — |
| solute denaturation (Ben-Naim) | — | Governed by (G_Us − G_Fs) + (G_Fw − G_Uw). | BN12 Eq. 4.3 (10.1063/1.4772463) | Here "s" is Ben-Naim's added "solute", the house cosolute. |
| Gibbs–Duhem two-part picture | Π | An open solution of 1 + 3 holding solute 2, in equilibrium with a closed 1 + 3 reference. | P08 Eqs. 7–10, after Hall (10.1007/s12013-007-9005-0; 10.1039/tf9716702516); Sh04 Eqs. 7–10 (10.1073/pnas.0305836101) | This is the derivation route of Γ23 = ρ3(G23 − G21). |
| LCPE model | V^l, Δμ3 | Smith's local chemical potential equalisation: the solute sits behind a virtual dialysis membrane. | P08 Eqs. 52–53 (10.1007/s12013-007-9005-0) | Like the local–bulk model, it has two fitted parameters. |

---

## 6. Domains, estimators and partitions

| Term | Symbol | Definition | Variants by school (DOI) | Pitfalls / conflicts |
|---|---|---|---|---|
| **integration domain** | D(δ) | The union of spheres of radius R_i + r_lig + δ around the solute atoms. It is a region of integration whose estimate converges. | union of spheres R_i + R, "within R of the vdW surface" BT03, VT12 (10.1021/jp0363996; 10.1016/j.bpj.2012.08.011); equal-radius minimum-distance domain MS17 (10.1021/acs.jctc.7b00599); V_cor sphere BN88 (10.1007/BF02918361) | Do not present it as a bound layer. Sh04 rejects postulated local domains (p. 1198, 10.1073/pnas.0305836101). |
| **thickness** | δ | The thickness of D beyond the cosolute-accessible surface. | r* BT03 (10.1021/jp0363996); R VYT09 (10.1021/jp903413v); R MS17 (10.1021/acs.jctc.7b00599) | Write δ alone only for the thickness (§9). |
| local domain / bulk domain — **avoid** outside Record's model | B_i,2, II/I, L/B | Record: a "local" domain holding only 1 and 3, plus a bulk domain at dialysis composition. | RA95 p. 788 (10.1016/S0006-3495(95)80254-7); "local-bulk domain model" ACR02 (10.1021/jp012627p), P08 Eq. 50 (10.1007/s12013-007-9005-0); II/I BT03 (10.1021/jp0363996); L/B VYT09 (10.1021/jp903413v) | "Two-domain" is Record's word. The model adds a boundary choice and a step profile. |
| **K_p** (local–bulk partition coefficient) | K_p | (local cosolute/water ratio)/(bulk ratio), so Γ = B1(m3/m1)(K_p − 1). | P08 Eq. 50 (10.1007/s12013-007-9005-0); BT03 Eq. 12 (10.1021/jp0363996); ST11 Eq. 8 (10.1021/jp108586b); Courtenay 2000 (10.1021/bi992887l); single-ion K_p,i ≡ m_i^local/m_i^bulk and νK_p,3 = ν+K_p,+ + ν−K_p,−: PR08 Eqs. 1–2 (10.1021/jp800816a) | It is defined only relative to a chosen B1, so it inherits the domain thickness. Do not reuse the symbol. For salts, only K_p,3 enters the thermodynamics. |
| hydration amount | B1,2, b1 | Water per solute in the local domain. b1 is water per Å² of ASA. | RA95 (10.1016/S0006-3495(95)80254-7); b1 Courtenay 2000 (10.1021/bi992887l); b1 ≈ 0.18 H2O Å⁻² PR08 (10.1021/jp800816a); "monolayer" BT03 p. 14060 (10.1021/jp0363996) | b1 is absent from RA95, ACR02, BT03, ST11 and VT12. Cite Courtenay. |
| **counted-solvent estimator** (explicit solvent) | Γ23(δ) | ⟨N3(D) − (ρ3/ρ1)N1(D)⟩ = ρ3[G23(D) − G21(D)]. Vol[D] cancels exactly. | Γ_XP BT03 Eq. 4 (10.1021/jp0363996); MS17 Eq. 8 (10.1021/acs.jctc.7b00599); ν_sc(R) S04 Eq. 29 (10.1021/jp0474879); P08 Eq. 55 cancellation (10.1007/s12013-007-9005-0) | It converges to the *molal* Γ23. A surface origin is fine for G23 − G21 but not for G23 alone (P08 p. 16). |
| **implicit-solvent estimator** | ⟨N3(D)⟩ − ρ3Vol[D] | → ρ3G23, the molar scale. | Smith scale relation S06a Eqs. 14, 34 (10.1021/jp056100e); Z18 Δn_ij = n_ij − N_Ac_jV (10.1063/1.5009802) | It is not molal Γ. The gap is ≈ ρ3V̄2. Γ(0) = −ρ3Vol[D(0)] is pure excluded volume. |
| **bulk ratio** | ρ3/ρ1 (bulk) | The reference ratio. Take it from outside the widest domain, or from the moving remainder (n3 − n23)/(n1 − n21). | moving bulk P08 Eq. 56 (10.1007/s12013-007-9005-0), SST09 Eq. 3 (10.1021/jp810949t), VYT09 Eq. 7 (10.1021/jp903413v); fixed far bulk BT03 Eq. 18 (10.1021/jp0363996) | The global box ratio biases Γ by the factor (1 − n21/n1) (inference, algebra on P08 Eq. 56). |
| cutoff | r*, R | The boundary beyond which Γ(r) is constant. | 6 Å BT03 (10.1021/jp0363996); ~6 Å SST09 (10.1021/jp810949t); 5 Å VT12 (10.1016/j.bpj.2012.08.011) | A single shell (3.5–4 Å) biases Γ by ≈ 0.5–1 (BT03 p. 14063). |
| **plateau** | — | Γ(δ) constant in δ, the convergence criterion. | VT12 "plateau from 5 Å" (10.1016/j.bpj.2012.08.011); G13 RKBI plateau (10.1021/ct301017q) | VYT09, VT12 and SST09 also use "plateau" for block-averaging inefficiency (10.1021/jp903413v). Keep it for Γ(δ). |
| instantaneous / apparent coefficient | Γ_XP(t), Γ*_XP(r*) | A per-frame estimate, and the RDF-route estimate up to r*. | BT03 Eqs. 18, 24–26 (10.1021/jp0363996); SST09 Γ23(r,t) (10.1021/jp810949t) | "Apparent" here means truncated, not "apparent molar". |
| virtual dialysis membrane | — | A boundary at R that is permeable to 1 and 3. | S06a Fig. 1 (10.1021/jp056100e); P08 p. 15, LCPE (10.1007/s12013-007-9005-0) | It is a picture, not a model assumption. |
| **site excess** | γ_i | Implicit solvent: γ_i = ⟨N_i⟩ − ρ3v_i with Σγ_i = Γ. Explicit solvent: ⟨N3,i − (ρ3/ρ1)N1,i⟩. | group coefficient Γ_XP,i BT03 Eq. 14 (10.1021/jp0363996); "partial preferential binding coefficients" of caffeine functional groups by proximal distance to group heavy atoms, ΣΓ_i = Γ, HHL23 Fig. 3B (10.1021/acs.jpcb.3c01085); residue Γ^i_XP VT12 Eq. 2 (10.1016/j.bpj.2012.08.011); shell Δñ_ij(S) Z18 Eq. 17 (10.1063/1.5009802) | Sites are additive only with exclusive ownership. Overlapping cutoffs break the sum (VYT09 p. 11748, 10.1021/jp903413v). |
| global / residue / regional coefficient | Γ, Γ^i, Γ^[a,b] | Whole-solute, single-residue and residue-group sums. | VT12 (10.1016/j.bpj.2012.08.011); "local preferential interaction coefficients" VT12 abstract | — |
| **radical (power) tessellation** | — | Owner = argmin_i [\|r − r_i\|² − (R_i + r_lig + δ)²]. Faces are planar and cell volumes exact. Ownership moves with δ. | No published Γ use in the inputs. MS17 and Smith flag per-site volumes as a hard normalisation (10.1021/acs.jctc.7b00599; 10.1021/jp056100e) | The novelty claim rests on non-exhaustive searches. Say "to our knowledge". |
| **additively weighted Voronoi** | — | Owner = argmin_i(\|r − r_i\| − R_i), the nearest vdW surface. Ownership is δ-independent. Faces are hyperboloids. | BT03 p. 14062 (10.1021/jp0363996); ST11 (10.1021/jp108586b); VT12 (10.1016/j.bpj.2012.08.011) | Baynes & Trout 2003 are the origin of radius-weighted domains and exact group sums. Their scheme is *not* an equal-radius special case. |
| **ordinary Voronoi** | — | Owner = the closest atom centre, with equal radii. | MS17 Eq. 6 (10.1021/acs.jctc.7b00599); M22 (10.1016/j.molliq.2021.117945) | M22 gives per-atom counts but no per-atom excess, because the normalisation is global. |
| **Voronoi solvation shells** | S, ñ_ij(S), Ṽ(S) | Molecular polyhedra ordered by face-sharing neighbour shell. | Z17 p. 3497 (10.1039/c6ra24736a); Z18 Eqs. 14–17 (10.1063/1.5009802) | They resolve the excess by shell, not by solute site. They assign void volume to some molecule. |
| solvent-accessible surface | SASA, SAA, ASA | The probe surface, 1.4 Å for water. | SAA BT03 (10.1021/jp0363996); SASA VT12, ST11 (10.1016/j.bpj.2012.08.011; 10.1021/jp108586b); occupancy-based "limited accessibility" VT12 | The house D(0) is the *cosolute*-accessible surface, with probe r_lig. Distinguish it from the water SASA. |
| near/far split | Γ = Σγ_i(δ_loc) + Γ_far | Site-attributed near field plus an unattributed far-field excess. | No published precedent found (report; Bai 2007 decomposes by species, 10.1021/ja075020g) | Manuscript proposal (inference). Ionic far fields carry the −Z constraint (§7). |
| effective boundary (Tang–Bloomfield) | — | The local domain ends at "the outer limit of the first cosolvent (not water) layer". | Tang & Bloomfield 2002 (10.1016/S0006-3495(02)75629-4) | This supports a δ scan over a fixed water-monolayer boundary. |

Conflicts in brief:
- Bulk reference: BT03 uses a fixed far bulk (10.1021/jp0363996). SST09, ST11, VYT09 and VT12 use a
  moving bulk, "everything outside r" (10.1021/jp810949t). Name your choice.
- Assignment metric: centre of mass to the vdW *surface* (BT03, additive) versus the closest atom
  centre (MS17, ordinary) versus a whole-molecule polyhedron (Z17/Z18). None of them is power
  weighting.

---

## 7. Salts

| Term | Symbol | Definition | Variants by school (DOI) | Pitfalls / conflicts |
|---|---|---|---|---|
| **single-ion coefficients** | Γ+, Γ− | The preferential interaction coefficients of cation and anion with the solute. They decompose by site. | Γ+,2J, Γ−,2J RA95 (10.1016/S0006-3495(95)80254-7); Γ2,+3, Γ2,−3 ST11 Eq. 4 (10.1021/jp108586b), SST09 Eq. 8 (10.1021/jp810949t) | Index orders differ. Give Γ+ and Γ− with the solute implied. |
| salt (component) coefficient | Γ_salt (Γ3,2) | The neutral-salt derivative. For a polyanion it equals the coion coefficient, Γ− = Γ3,2. | RA95 Eq. 40 (10.1016/S0006-3495(95)80254-7); Γ_μ3 ACR02 (10.1021/jp012627p) | Only Γ+ + Γ− = \|Z\| + 2Γ_salt is a neutral-salt derivative (RA95 Eq. 41). |
| **electroneutrality term** | Z | Γ+ − Γ− = −Z, with Z the signed solute charge. For a polyanion, Γ+ − Γ− = +\|Z\|. | RA95 Eq. 29, "conservation of material" (10.1016/S0006-3495(95)80254-7); Z = absolute charge P08 Eq. 22 (10.1007/s12013-007-9005-0), S04 Eq. 15 (10.1021/jp0474879); ST11 labels the protein charge \|Z3\| (10.1021/jp108586b) | The notes once had the sign reversed. In RA95 neither the local nor the bulk domain is electroneutral alone. |
| **indistinguishable-ion approach** | ρ3 = ν±ρ_salt | Salt treated as one species of identical ions, so ν±Γ23 = N23 − (ρ3/ρ1)N21 − \|Z\|. | P08 p. 7, Eq. 22, n± (10.1007/s12013-007-9005-0); S04 abstract, ρ_c = n±C_c (10.1021/jp0474879) | With ν± = 2 and N23 − (ρ3/ρ1)N21 = Γ+ + Γ−, Pierce's Γ23 is Γ_salt. The \|Z\| term applies only when the released counterions match a salt ion; S06a and S06b drop it (10.1021/jp056100e). |
| common-ion indicator | δ_Ic | δ_Ic = 1 when the solute releases ion I that is identical to a cosolute ion. | S04 Eq. 15 (10.1021/jp0474879) | A Kronecker delta in disguise. |
| Donnan coefficient, ideal Donnan | Γ^ideal± | Polyanion: Γ^ideal+ = +½\|Z\|, Γ^ideal− = −½\|Z\|; generally \|Z\| ≥ Γ+ ≥ ½\|Z\|. | RA95 Eqs. 25–28 (10.1016/S0006-3495(95)80254-7) | P08 notes a small difference from Schellman's definition (10.1007/s12013-007-9005-0). |
| ion atmosphere | — | The far-field ionic excess that sets Γ+ − Γ− globally. | Bai 2007 decomposes by species (10.1021/ja075020g); Z18 outer-shell ion excess (10.1063/1.5009802) | A finite D(δ) recovers −Z only once it holds the atmosphere (inference). |
| mean ionic activity | a± | Salt activity per ion. | RA95 Eq. 2 (10.1016/S0006-3495(95)80254-7); S04 a_c = a± (10.1021/jp0474879) | The ACR02 form uses ν·ln a3 (10.1021/jp012627p). Do not mix the two. |

---

## 8. Sign and interpretation words

| Term | Symbol | Definition | Variants by school (DOI) | Pitfalls / conflicts |
|---|---|---|---|---|
| **accumulated** | Γ23 > 0 | The cosolute is in excess relative to the bulk ratio. Defined by the sign of Γ23 alone. | "preferentially accumulated" RA95 p. 787 (10.1016/S0006-3495(95)80254-7); ACR02 p. 424 with Γ_μ3 (10.1021/jp012627p); "preferential binding" P08 (10.1007/s12013-007-9005-0) | ACR02 classifies by Γ_μ3, whose sign can differ from Γ_μ1. |
| **excluded** | Γ23 < 0 | The cosolute is depleted relative to the bulk ratio. | "preferential exclusion" RA95 (10.1016/S0006-3495(95)80254-7), P08 p. 3 (10.1007/s12013-007-9005-0); "preferentially excluded" MS17 (10.1021/acs.jctc.7b00599) | An excluded cosolute can still show augmented contact density (MS17 ms p. 24; M22, 10.1016/j.molliq.2021.117945). Say so when that could mislead. |
| bound / preferential binding — **avoid** for Γ > 0 | n_bound | Reserve "bound" for a cutoff occupancy count, and say that it is one. | BT03 "excess … bound" (10.1021/jp0363996); MS17 "preferentially bound" (10.1021/acs.jctc.7b00599); P08 keeps "binding" as thermodynamic (10.1007/s12013-007-9005-0) | Sh04 says exclusion "is not merely a lack of binding" (10.1073/pnas.0305836101). |
| preferential solvation — **avoid** as a sign word | — | Means *opposite* things in different schools. | Water accumulation, Γ < 0: RA95 p. 787 (10.1016/S0006-3495(95)80254-7). Cosolute excess, Γ > 0: VT12 (10.1016/j.bpj.2012.08.011), VYT09 (10.1021/jp903413v), M22 (10.1016/j.molliq.2021.117945). Relative, "of S with respect to A": BN88 (10.1007/BF02918361) | Use accumulated/excluded instead. |
| preferential hydration — **avoid** as a sign word | Γ21 | A synonym for exclusion in Smith's papers. Shimizu defines it as the parameter ν21. | P08 p. 3, S06a p. 2866 (10.1007/s12013-007-9005-0; 10.1021/jp056100e); ν21 Sh04 (10.1073/pnas.0305836101); BT03, VT12 Γ < 0 (10.1021/jp0363996) | If used, write "preferential hydration (Γ21 = −(ρ1/ρ3)Γ23 > 0)". |
| preferential dehydration | Γ_uw < 0 | MS17's word for water depletion. | MS17 ms p. 22 (10.1021/acs.jctc.7b00599) | Avoid; it invites a binding picture. |
| excess / deficiency | G ≷ 0, N ≷ 0 | Signed excess number. | M84 (10.1063/1.447034); Z18 (10.1063/1.5009802); BN88 (10.1007/BF02918361) | A negative G for a solute is mostly excluded volume (Z18 Eqs. 8–9; BN12 Eq. 3.6, 10.1063/1.4772463). |
| local density augmentation | — | An MDDF contact peak. It is distinct from net excess. | MS17 (10.1021/acs.jctc.7b00599); M22 (10.1016/j.molliq.2021.117945) | — |
| affinity | — | "G_AS measures the affinity of S toward A". | BN77 p. 4884, G_αβ = −V_αβ + I_αβ Eq. 3.6 (10.1063/1.434669); BN88 p. 262 (10.1007/BF02918361); S04 p. 18717 (10.1021/jp0474879); M84 "net attraction" (10.1063/1.447034) | Z18 says I_ij, not G_ij, measures affinity (10.1063/1.5009802). M84: the integral loses the microscopic mechanism. |
| bulk reference — use instead of bare "ideal" | — | Random solvent at bulk density, equivalent to a non-interacting "phantom" solute. | MS17 App. (10.1021/acs.jctc.7b00599); M22 (10.1016/j.molliq.2021.117945) | M84's "ideal" means a Raoult ideal solution (10.1063/1.447034). Ploetz10 (10.1063/1.3398466) gives its nonzero G. |
| preferred solvation (free energy) | ΔA_j(shell) < 0 | A shell free energy for which negative means enriched. | Z17 Eq. 5 (10.1039/c6ra24736a) | Its sign runs opposite to Γ. |
| favourable / unfavourable coupling | Γ_μ3 ≷ 0 | μ2 is lowered as μ3 rises. | ACR02 p. 420 (10.1021/jp012627p); BT03 p. 14059 (10.1021/jp0363996) | — |
| stabilising / destabilising | ΔΓ23 ≶ 0 | ΔΓ23 < 0 favours the native state. | P08 p. 10 (10.1007/s12013-007-9005-0); S06a p. 2866 (10.1021/jp056100e) | It applies to the *difference* ΔΓ, not to Γ of one state. |

---

## 9. Symbol collisions

| Symbol | Meanings (DOI) | House use |
|---|---|---|
| Γ | Preferential interaction coefficient (all Γ papers). Thermodynamic-factor matrix Γ^GC (Simon22, 10.1063/5.0106162). | Γ23 and Γ± only. Rename the matrix. |
| δ | Kronecker δ_ij (P08, 10.1007/s12013-007-9005-0). Ben-Naim's preferential solvation δ_A,S (BN88, 10.1007/BF02918361). Shell indicator δ(jS) (Z18, 10.1063/1.5009802). Common ion δ_Ic (S04, 10.1021/jp0474879). Domain thickness. | δ alone means thickness. δ_ij always has two indices. Rename δ_A,S when you quote it (gap in house style). |
| n | Molarity (Sh04, 10.1073/pnas.0305836101). Molecule count (P08). Ions per formula unit n± (S04). Cumulative count n_ij(R). | Use ρ for densities, N for counts and ν± for ion stoichiometry. |
| ν | Preferential coefficient ν_sc (S04, 10.1021/jp0474879). ν21 (Sh04). Stoichiometry ν (ACR02, 10.1021/jp012627p). | Stoichiometry only. |
| s | Solute (S04). Solvent (MS17, 10.1021/acs.jctc.7b00599). Added "solute"/cosolute (BN12, 10.1063/1.4772463). | Do not use. |
| ~ (tilde) | Running KBI or canonical RDF (Simon22, 10.1063/5.0106162). Shell quantity (Z18, 10.1063/1.5009802). | Running KBI only, if at all. |
| L | Radius, diameter or 2R (Simon22; K13, 10.1021/jz301992u). Box side (G13, 10.1021/ct301017q). 6V/A (KV18, 10.1103/PhysRevE.97.051301). | Define it at each use. |
| ° / 0 | m2 → 0 (S06a, 10.1021/jp056100e; RA95, 10.1016/S0006-3495(95)80254-7). n3 → 0 (Sh04, 10.1073/pnas.0305836101). | Say which limit. |
| γ | Activity coefficient (P08, 10.1007/s12013-007-9005-0). Site excess γ_i. | Site excess γ_i. |
| B | Local-domain contents B_i,2 (RA95, 10.1016/S0006-3495(95)80254-7). Whole-solution binding B_i (P08). Fluctuation matrix B_ab (Simon22). Virial coefficients. | Name the meaning when you cite it. |
