# Equations: KB integrals, excess numbers, solution relations, inversion

Notation: 1 = water, 2 = solute, 3 = cosolute. ρ_i is a number density and m_i = N_i/N1 a
molality, written as a number ratio, so m3/m1 = ρ3/ρ1. φ_i = ρ_iV̄_i. β = 1/k_BT, and RT replaces
k_BT on molar quantities. h_ij = g_ij − 1. G_ij = G_ji, but N_ij = ρ_jG_ij counts j around i, so
N_ij ≠ N_ji. The superscript ° denotes the solute at infinite dilution (m2 → 0).

Sources give the paper's equation number and DOI; equation numbers were checked against
full texts unless marked. "(inference)" marks a step no cited paper states. Section numbers (§N)
are shared across the equation files; SKILL.md maps each § to its file.

## 1. Kirkwood–Buff integrals

**1.1 Definition** (open system, infinite range):

    G_ij = 4π ∫₀^∞ [g_ij^{μVT}(r) − 1] r² dr

- Source: Pierce et al. 2008, Eq. 11 (10.1007/s12013-007-9005-0).
- Also: Simon et al. 2022, Eq. 3, written G^∞_ab (10.1063/5.0106162); Ganguly & van der Vegt 2013, Eq. 1 (10.1021/ct301017q).
- Original theory: Kirkwood & Buff 1951 (10.1063/1.1748352). Its wording and equation numbers were not checked.

**1.2 Fluctuation form** (an open region of volume V):

    G_ij = V [ (⟨N_iN_j⟩ − ⟨N_i⟩⟨N_j⟩) / (⟨N_i⟩⟨N_j⟩) − δ_ij/⟨N_i⟩ ]

- Source: Pierce et al. 2008, Eq. 12 (10.1007/s12013-007-9005-0).
- In a closed system the same expression gives ρ_jG_ij = −δ_ij, so it is not the KBI. See Pierce p. 5 and Ben-Naim 1988, Eq. 2.6 (10.1007/BF02918361).

**1.3 Open-system derivative**:

    k_BT (∂ρ_i/∂μ_j)_{T,V,μ′} = ρ_iρ_jG_ij + ρ_iδ_ij

- Source: Pierce et al. 2008, Eq. 13 (10.1007/s12013-007-9005-0); Smith 2006a, Eq. 4 (10.1021/jp056100e).
- Matrix form: B_ab = ρ_aρ_bG_ab + ρ_aδ_ab (Simon et al. 2022, Eq. 16, 10.1063/5.0106162). Simon Eq. 27 prints −δ_abρ_a, which is a typo.
- Free-energy curvature: since βμ_i = ∂(βf)/∂ρ_i, with f the Helmholtz free energy per volume, B is
  the inverse Hessian, B = [∂²(βf)/∂ρ_i∂ρ_j]⁻¹. Kumari & Podgornik 2024 (10.1063/5.0187324, abstract) use this
  Legendre-transform relation between the Hessians of f(ρ) and of the pressure p(μ). A quantity
  defined by "second derivatives of the free energy with respect to concentrations" is therefore
  a KB fluctuation quantity. For ions, see salts.md §10 before using it.

## 2. Excess numbers

**2.1 Excess coordination number**:

    N_ij = ρ_j G_ij

- Source: Pierce et al. 2008, p. 5 (10.1007/s12013-007-9005-0).
- Shimizu 2004, Eq. 4 writes N_2i = n_iN_AG_2i, with n_i a molarity (10.1073/pnas.0305836101).

**2.2 Truncated count** (a sphere of radius R):

    N_ij(R) = n_ij(R) − (4/3)πR³ρ_j,    n_ij(R) = 4πρ_j ∫₀^R g_ij r² dr

- Source: Pierce et al. 2008, Eqs. 54–55 (10.1007/s12013-007-9005-0). Eq. 55 is printed with a typo "n₂₃".
- Pierce p. 16: for differences such as G23 − G21 "the second term … will disappear".

**2.3 Ben-Naim finite-domain count**:

    N_3(R_c) = ρ3G23 + ρ3V_cor

- Source: Ben-Naim 1988, Eq. 2.8 (10.1007/BF02918361). The original reads N_A,S(R_c) = ρ_AG_AS + ρ_AV_cor, with A a solvent component and S the solute.

## 3. Solution relations used below

    a33 ≡ (∂ln a3/∂ln ρ3)_{T,P} = 1/[1 + ρ3(G33 − G13)] ≈ φ1/(1 + N33)

- Source: Pierce et al. 2008, Eqs. 15 and 19 (10.1007/s12013-007-9005-0). Pierce gives the error of the approximation as < 1 %.
- Smith 2004 writes the same quantity as a_cc (10.1021/jp0474879).

```
V̄2° = RTκ_T − N21V̄1 − N23V̄3
```

- Source: Pierce et al. 2008, Eq. 28 (10.1007/s12013-007-9005-0).
- Shimizu 2004, Eq. 12: V2 = −V1N21 − V3N23 + RTκ_T (10.1073/pnas.0305836101).

Binary 1–3 solution, with η = ρ1 + ρ3 + ρ1ρ3(G11 + G33 − 2G13):

    V̄1 = [1 + ρ3(G33 − G13)]/η,    k_BTκ_T = ζ/η,    ζ = 1 + ρ1G11 + ρ3G33 + ρ1ρ3(G11G33 − G13²)

- Source: Simon et al. 2022, Eqs. 25–28, translated from components 1, 2 to 1, 3 (10.1063/5.0106162).
- Ideal-solution KBIs are nonzero: Ploetz et al. 2010 (10.1063/1.3398466).

## 14. KB inversion

Binary original, Ben-Naim 1977 (10.1063/1.434669), species A and B:

    η = ρ_A + ρ_B + ρ_Aρ_B(G_AA + G_BB − 2G_AB)                       [Eq. 2.1]
    ζ = 1 + ρ_AG_AA + ρ_BG_BB + ρ_Aρ_B(G_AAG_BB − G_AB²)               [Eq. 2.2]
    κ_T = ζ/(kTη),   V̄_A = [1 + ρ_B(G_BB − G_AB)]/η                    [Eqs. 2.3–2.4]
    μ_AA = ρ_BkT/(ρ_AηV),   μ_AB = −kT/(ηV),   μ_αβ = (∂μ_α/∂N_β)_{T,P,N_γ}   [Eq. 2.6]
    x_A(∂ln P_A/∂x_A)_{T,P} = ρ/η          (ideal vapour)             [Eq. 2.12]
    V̄_AV̄_B = (ζ − ηG_AB)/η²                                            [Eq. 2.13]
    Δ_AB = G_AA + G_BB − 2G_AB;  Δ_AB = 0 ⇔ symmetric ideal            [Eq. 2.14]
    G_αβ = −V_αβ + I_αβ                                                [Eq. 3.6]

- Procedure: η from vapour pressures (2.12), ζ from κ_T (2.3), G_AB from (2.13), then G_BB, G_AA from (2.4)–(2.5).
- Eq. 2.11 is the corrected form of Eq. 4.88 in BN77's Ref. 4 (stated in BN77).
- V_αβ is a nearly composition-independent exclusion volume (sphere of radius σ_αβ); I_αβ is the "affinity" part beyond σ_αβ. Z18 uses the same split (I_ij as affinity).
- BN77 counts the c-component inversion as c(c + 1)/2 unknowns from 1 + c + c(c+1)/2 equations minus the c + 1 identities; it gave no ternary data.
- Δ_AB collides with any rename of Ben-Naim's δ_A,S to Δ_A,S; use Δ^PS_A,S for the latter.

Multicomponent, Smith 2008 (10.1063/1.2982171):

Inversion gives the n(n+1)/2 integrals G_ij from κ_T, n − 1 independent PMVs and n(n − 1)/2
independent chemical-potential derivatives.

    μ_ij ≡ β(∂μ_i/∂ln N_j)_{T,P,N_k≠j}                                 [Eq. 2]
    (∂ln ρ_i/∂μ_j)_{T,μ_k≠j} = β(δ_ij + N_ij)                         [Eq. 4]
    δ_ik − ρ_kV̄_k = Σ_j (δ_ij + N_ij) μ_jk                            [Eq. 6]
    RTκ_T = Σ_j (δ_ij + N_ij) V̄_j                                     [Eq. 7]
    δ_1i + N_1i = ρ_iRTκ_T − (ρ_i/M_n,i) Σ_j M_j,i φ_{j+1}           [Eq. 13; M_n cofactors, Eq. 8]

Ternary, solute 2 at infinite dilution (1 = water, 3 = cosolute):

    G12^∞ = RTκ_T − V̄2^∞ + V̄3(μ23^∞ + φ3)/μ33                        [Eq. 34]
    G_ij^SI = RTκ_T − V̄_i − V̄_j + Σ_k ρ_kV̄_k²                         [Eq. 35, symmetric ideal]

- μ_ij is not a33. Smith notes the definition is "slightly different" from his earlier ones; it uses ln N_j at constant P and the other N_k. Translate before combining with §3.
- Other G_ij follow by index changes, e.g. G32^∞ from Eq. 34 with 1 ↔ 3. Then Γ23 = ρ3(G23 − G21) (gamma-linkage.md §4).
- Stability: μ_ii ≥ 0 and μ_ij < 0 for i ≠ j (Eq. 23). A negative N12 constrains the data (Eqs. 28–29).
- Salts: Smith keeps μ_ij general because activity-coefficient relations for salts are system dependent (Discussion). Applied by Hervø-Hansen et al. 2023 (10.1021/acs.jpcb.3c01085) to caffeine–salt: inverted implicit-solvent MC output (fitted ln γ2 from μ2^ex, experimental salt activities, Gibbs–Duhem, infinite-dilution V̄_i and κ_T); the same fit accepts experimental VPO input (simulation.md §4).
- Hervø-Hansen et al. 2023 (10.1021/acs.jpcb.3c01085) write the same inversion as

      δ_ik − c_kV̄_k = Σ_j (δ_ij + N_ij) μ_jk                            [Eq. 11]
      RTκ_T = Σ_j (δ_ij + N_ij) V̄_j                                      [Eq. 12]
      μ_ij = (∂ln a_i/∂ln m_j)_{T,p,m_k≠j},   N_ij = G_ijρ_j

  solved for i = 1 and k ≠ 1. These are Smith 2008 Eqs. 6–7 with c_k for ρ_k: for j ≠ 1, ln N_j at
  fixed N_k (k ≠ j, including N1) changes as ln m_j, so the molal derivative equals Smith's μ_ij.
  RT pairs with molar V̄ and c (per-molecule form: k_BT with ρ).
- Matteoli & Lepori (10.1063/1.447034): G_ij are insensitive to κ_T and PMVs away from critical points, so SI values often suffice for those terms (Smith 2008, Conclusions).
- Smith reads N_ij as the change in j within a "local spherical volume" on placing i at the centre (p. 124509-2). The house text keeps that reading for radial KBIs only.
