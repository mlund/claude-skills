# Core relations in house notation

Notation: 1 = water, 2 = solute, 3 = cosolute. ρ_i is a number density and m_i = N_i/N1 a
molality, written as a number ratio, so m3/m1 = ρ3/ρ1. φ_i = ρ_iV̄_i. β = 1/k_BT, and RT replaces
k_BT on molar quantities. h_ij = g_ij − 1. G_ij = G_ji, but N_ij = ρ_jG_ij counts j around i, so
N_ij ≠ N_ji. The superscript ° denotes the solute at infinite dilution (m2 → 0).

Every relation below gives its source, the paper's equation number and the DOI. The equation
numbers were checked against the full texts (verification.md) unless a line says otherwise.
"(inference)" marks a step that no input paper states. When a paper's symbols differ from the
house symbols, the original notation is given under the relation.

Contents: 1 KB integrals · 2 excess numbers · 3 solution relations · 4 Γ23 · 5 linkage ·
6 ensemble offsets · 7 molal vs molar scale · 8 estimators · 9 bulk ratio · 10 salts ·
11 m-value · 12 finite-volume KBI (for contrast) · 13 partitions and site excess · 14 KB inversion ·
15 fluctuation theory: second derivatives, solute volume, interfaces · 16 dimensions and units ·
17 verification checks

---

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

## 4. The preferential interaction coefficient Γ23

**4.1 Definition** (equilibrium dialysis):

    Γ23 ≡ (∂m3/∂m2)_{T,μ1,μ3}

- Source: Pierce et al. 2008, Eq. 1 (10.1007/s12013-007-9005-0); Record & Anderson 1995, Eq. 4 (10.1016/S0006-3495(95)80254-7).
- Original notation: Record & Anderson write Γ3,2, with the cosolute index first, and Γ°3,2 for the m2 → 0 limit. Anderson et al. 2002 write Γ_μ1,μ3 (Eq. 4, 10.1021/jp012627p).
- Smith 2006a, p. 2865: V is implicitly fixed as well (10.1021/jp056100e).

**4.2 Infinite dilution of the solute**:

    Γ23° = ρ3(G23 − G21) = N23 − (ρ3/ρ1)N21

- Source: Pierce et al. 2008, Eq. 21 (10.1007/s12013-007-9005-0); Smith 2006a, Eq. 12 (10.1021/jp056100e).
- Original notation: Smith 2004, Eq. 6 writes ν_sc = ρ_c(G_sc − G_sw) (10.1021/jp0474879). Martínez & Shimizu 2017, Eq. 7 write Γ_uc ≈ ρ_c(G_uc − G_uw) (10.1021/acs.jctc.7b00599).

**4.3 Finite solute concentration**:

    Γ23 = (N23 − m3N21)/(1 + N22 − N12) = ρ3(G23 − G21)/[1 + ρ2(G22 − G21)]

- Source: Karunaweera et al. 2012, Eq. 16 (10.1021/ct300079v). The full text of this paper was not available.
- The identical expression is Smith 2006a, Eq. 11 (10.1021/jp056100e), which was checked.
- Here m3 = ρ3/ρ1, N12 = ρ2G12 and N22 = ρ2G22.

**4.4 Other scales and the water coefficient**:

    (∂x3/∂x2)°_{T,μ1,μ3} = −x3 + x1ρ3(G23 − G21)                  [Smith 2006a, Eq. 16; 10.1021/jp056100e]
    (∂ln K/∂ln a1)°_{T,P} = −(ρ1/ρ3)ΔΓ23 = ΔΓ21                   [Pierce 2008, Eqs. 39–41; 10.1007/s12013-007-9005-0]
    ν21 = (∂ρ1/∂ρ2)_{T,P,μ1} = N21 − (ρ1/ρ3)N23   (solute dilute)  [Shimizu 2004, Eqs. 1, 3; 10.1073/pnas.0305836101]

- Shimizu's original uses n_i for molarities.

**4.5 Ben-Naim preferential solvation index** (mole-fraction based, for contrast):

    δ_A,S = x_Ax_B(G_AS − G_BS)/(x_AG_AS + x_BG_BS + V_cor)

- Source: Ben-Naim 1988, Eq. 2.11 (10.1007/BF02918361).
- Its sign is that of G_AS − G_BS. With A = 3 and B = 1, that is the sign of Γ23 (inference).
- The δ is not the house thickness.

## 5. Wyman linkage

**5.1 Activity form** (constant T, P, solute dilute):

    (∂ln K/∂ln a3)°_{T,P} = ΔΓ23 = ΔN23 − (ρ3/ρ1)ΔN21

- Source: Pierce et al. 2008, Eq. 5 (10.1007/s12013-007-9005-0); Smith 2006a, Eq. 45 (10.1021/jp056100e); Record & Anderson 1995, Eq. 1 (10.1016/S0006-3495(95)80254-7).
- a3 may be on any scale (Pierce).
- Record & Anderson pair this (T, P) derivative with the *dialysis* Γ3,2J. Smith states that the relation is "valid for the molality based preferential interactions in any ensemble". Pierce adds the condition "only for processes with a 1:1 stoichiometry" (p. 9).
- (inference) For A + B ⇌ AB the solute-independent offset of §6 does not cancel in Δ. It contributes φ3/(a33φ1) per molecule lost.

**5.2 Concentration form and pseudo-chemical potential**:

    −β(∂μ2*/∂ln ρ3)°_{T,P} = ρ3(G23 − G21)/[1 + ρ3(G33 − G13)] = Γ23 a33
    (∂ln K/∂ln ρ3)°_{T,P}  = ΔΓ23 a33

- Source: Pierce et al. 2008, Eqs. 26 and 32 (10.1007/s12013-007-9005-0); Smith 2004, Eqs. 4–5, 9 (10.1021/jp0474879).
- The factor multiplies; it does not divide. The note gamma_in_kb.md wrote ÷a33, which is wrong.

## 6. Ensemble offsets (solute at infinite dilution)

    (∂m3/∂m2)°_{T,P,μ3} = Γ23 + φ3/(a33φ1) = Γ23 + (ρ3/φ1)(RTκ_T − G13)
                       = ρ3/ρ1 + ρ3(G23 − G21 + G11 − G13)
    (∂m3/∂m2)°_{T,P,μ1} = Γ23 − 1/a33 = −1 + ρ3(G23 − G21 + G13 − G33)
    Γ23 = φ1(∂m3/∂m2)°_{T,P,μ3} + φ3(∂m3/∂m2)°_{T,P,μ1}

- Source: Pierce et al. 2008, Eqs. 23–25 and Table 1 (10.1007/s12013-007-9005-0); Smith 2006a, Eqs. 25–27, 30–31 and 37–38, Table 1 (10.1021/jp056100e).
- Original notation: Smith 2004 writes Γ′23 (constant μ3, Eq. 16) and Γ″23 (constant μ1, Eq. 17) (10.1021/jp0474879). Anderson et al. 2002 write Γ_μ3 and Γ_μ1 (Table 1, 10.1021/jp012627p). Their Γ_μ1 is *not* the dialysis coefficient.
- The φ3/(a33φ1) offset depends only on the 1–3 solution and is the same for every solute. It is ≈ ρ3V̄3 at low cosolute.
- Notes estimate, not from a paper: the offset is ≈ 0.05 at 1 M urea and ≈ 0.4–0.5 at 8 M urea. That is negligible beside a protein Γ of order 10, but not beside a small-solute Γ ≲ 1. Pierce: it "can become significant" for TFE, where a33 ≈ 0.2.
- Anderson et al. 2002, Eq. 13a: Γ_μ3 − Γ_μ1 = (|Z_M| + 1)RT/(m3μ33°), with μ33 = ∂μ3/∂m3.
  (inference) For Z = 0 this has the same form as the difference of Pierce Eqs. 23 and 24, (φ1 + φ3)/(a33φ1), up to the molal-versus-molar activity derivative.

## 7. Molal vs molar scale

    (∂ρ3/∂ρ2)°_{T,μ1,μ3} = ρ3G23 = N23                                  [Smith 2006a, Eq. 14]
    ρ3G23 = φ1Γ23 − ρ3(V̄2° − RTκ_T)                                     [Smith 2006a, Eq. 34]
    φ1(∂ln K/∂ln a3)°_{T,P} = Δ(ρ3G23) + ρ3ΔV̄2°                          [Smith 2006a, Eq. 46]

- Source: Smith 2006a (10.1021/jp056100e).
- The molal Γ23 is "always larger in magnitude". The molar coefficient "includes the excluded volume effect of the protein" and is "not well suited for the analysis of simulation data" when distances are measured from the surface (pp. 2866–2867).
- Two-domain molar form: Γ^exp3,2 = B3,2(1 − C3V̄3) − C3V̄2 − C3B1,2V̄1 (Record & Anderson 1995, Eq. A6, 10.1016/S0006-3495(95)80254-7). It contains the −C3V̄2 excluded-volume term.
- Notes estimate: the molal–molar gap is ≈ ρ3V̄2 at low cosolute. That is ≈ 0.14 per mol L⁻¹ for a caffeine-sized solute (V̄2 ≈ 140 cm³ mol⁻¹, approximate) and ≈ 10 per mol L⁻¹ for a 10⁴ cm³ mol⁻¹ protein.

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

    Γ_molar(D) = ⟨N3(D)⟩ − ρ3Vol[D] = ρ3G23(D)  →  ρ3G23 (molar, §7)

- The scale identification is cited: Smith 2006a, Eq. 14 (10.1021/jp056100e).
- (inference) The McMillan–Mayer level fixes μ1, which makes the ensemble (T, μ1, μ3).
- D contains the solute, so for a solute core impenetrable to cosolute, Γ_molar(D(0)) = −ρ3Vol[D(0)]: pure excluded volume. Compare Ben-Naim 2012, Eqs. 3.6–3.7 (10.1063/1.4772463).
- Zeindlhofer et al. 2018, Eqs. 5–7 give the same form, Δn_ij = n_ij − N_Ac_jV, with V including the solute (10.1063/1.5009802).
- This estimator does not give the molal Γ23. Convert with §7.

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

- Source: Pierce et al. 2008, Eq. 56 (10.1007/s12013-007-9005-0); Shukla et al. 2009, Eq. 3 (10.1021/jp810949t). Vagenende et al. 2009, Eq. 7 (10.1021/jp903413v) uses the same form.
- Notation: n1 and n3 are the box totals. n2j(R) is the raw count within R. Shukla writes n_i(r,t).
- Pierce: "The correction can be significant for protein systems … as the value of n21 can be large."
- Ploetz & Smith 2013, §13 (10.1002/9781118571767.ch4) give the same adjustment: the bulk ratio is the box totals minus what sits in the local region, "especially … for small systems and/or large values of Γ".
- A fixed far bulk instead takes the ratio from a region beyond r* (Baynes & Trout 2003, Eq. 18, 10.1021/jp0363996).

Global-box ratio bias (inference: exact algebra on Pierce Eq. 56):

    n23 − (n3/n1)·n21 = Γ23(R)·(1 − n21/n1)

- The relative underestimate is n21/n1 ≈ V_local/V_box.

RDF analogue, for contrast (Ganguly & van der Vegt 2013, Eq. 5, 10.1021/ct301017q; Simon et al. 2022, Eq. 6):

    g^corr_ij(r) = g_ij(r) · N_j(1 − V_r/V) / [N_j(1 − V_r/V) − ΔN_ij(r) − δ_ij],   V_r = 4πr³/3

## 10. Salts

Record & Anderson 1995 (10.1016/S0006-3495(95)80254-7). The solute (2) is a polyanion together with its |Z| univalent cations, and the cosolute (3) is a 1:1 salt.

    Γ+° = |Z| + Γ−°        (conservation; so Γ+ − Γ− = −Z, Z signed)        [Eq. 29]
    Γ+° = ½(|Z| + B− + B+) − B1 m3/m1                                         [Eq. 40]
    Γ−° = −½(|Z| − B− − B+) − B1 m3/m1 = Γ°3,2                                 [Eq. 40]
    Γ+° + Γ−° = |Z| + 2Γ°3,2 = B+ + B− − 2B1 m3/m1                            [Eq. 41]
    S_aK_obs ≡ (∂ln K_obs/∂ln a±)_{T,P} = Δ(Γ+ + Γ−) = Δ(|Z| + 2Γ3,2)          [Eqs. 2, 42]
    Γ^ideal+ = +½|Z|,  Γ^ideal− = −½|Z|;  |Z| ≥ Γ+° ≥ ½|Z|                     [Eqs. 27–28]

- Original notation: Γ±,2J, B±,2J, B1,2 and Z_J. K_obs is in molar concentrations.
- For a polycation, replace |Z| by −|Z| in Eq. 40.
- (inference) Then Γ− − Γ+ = |Z|, and the sum rule holds with Γ_salt = the cation (coion) coefficient.
- Anderson et al. 2002, Eqs. 6–7: S_aK_obs ≡ ν(∂ln K_obs/∂ln a3)_{T,P} = Δ|Z| + νΔΓ_μ3, with ν = ν+ + ν− (10.1021/jp012627p). This form differentiates against ln a3 with the factor ν, not against ln a±.

Indistinguishable ions (KB school), with ρ3 = ν±ρ_salt:

    ν±Γ23 = N23 − (ρ3/ρ1)N21 − |Z|                                           [Pierce 2008, Eq. 22]
    n±Γ23 = f_Dν_Dc + f_Nν_Nc − Zδ_Ic   (ν_Dc, ν_Nc = ρ_c(G_sc − G_sw) of D, N)  [Smith 2004, Eq. 15]
    Γ23 = ½(Γ+ + Γ− − |Z|)                                                  [Shukla et al. 2009, Eq. 8]

- Sources: Pierce (10.1007/s12013-007-9005-0), written n± with Z the absolute charge. Smith 2004 (10.1021/jp0474879). Shukla et al. 2009 (10.1021/jp810949t), which writes Γ2,±3 and |Z3|.
- The −|Z| term applies when the solute releases counterions identical to a salt ion (δ_Ic = 1). Smith 2006a and 2006b drop it.
- With ν± = 2 and N23 − (ρ3/ρ1)N21 = Γ+ + Γ−, Pierce Eq. 22 is Record & Anderson Eq. 41, so Pierce's Γ23 is Γ_salt (verification.md).
- In simulations, the cosolute count is the sum of the ion counts, n_sc(R) = n_s+(R) + n_s−(R) (Smith 2004, p. 18722).
- Why ions are not independent species: with cation, anion and solvent as independent variables, electroneutrality makes the number-fluctuation matrix singular (Friedman & Ramanathan 1970, 10.1021/j100715a009; Kusalik & Patey 1987, 10.1063/1.452629). The usual fix is a salt "molecule" or indistinguishable ions; the latter matches Kusalik & Patey (Ploetz & Smith 2013, §16, 10.1002/9781118571767.ch4).
- Dissent: Ben-Naim (Molecular Theory of Solutions, 2006, cited by Ploetz & Smith §16) holds that KB theory is valid for salts with independent ions, since KBIs are grand-canonical and electroneutrality is an unnecessary constraint on them; only the data to vary ion concentrations separately are missing. Ploetz & Smith adopt dependent ions for lack of data. Substituting N_2 = N_+ + N_− is an index change; electroneutrality then leaves one independent salt fluctuation.
- (inference) For the house style: single-ion Γ± from simulation are well defined counts (Ben-Naim's view), but only Γ+ + Γ− is a thermodynamic derivative (§10 above). Say which view a sentence relies on.

## 11. m-value

    βΔΔG = −mρ3                                                  [Pierce 2008, Eq. 42]
    m^app = (∂ln K/∂ρ3)°_{T,P} = ΔΓ23 a33/ρ3                       [Pierce 2008, Eq. 43]
    exact linearity requires ΔΓ23 = mρ3[1 + ρ3(G33 − G13)]        [Pierce 2008, Eq. 44]
    ΔΔG = ΔG°(C3) − ΔG°(0) = −mC3   (linear extrapolation)        [Smith 2004, Eq. 21]

- Sources: Pierce (10.1007/s12013-007-9005-0); Smith 2004 (10.1021/jp0474879).
- Heyda & Dzubiella 2014, Eq. 3 (10.1021/jp5041635), writes the same relation as Pierce Eq. 43 with molar c3: ∂ΔG_u/∂c3 = −k_BT ΔΓ23 a33/c3. They define Γ23 as the molal dialysis derivative. Their second-order model, ΔΓ23(c) = ΔΓ′23c + ΔΓ″23c²/2, gives a nonlinear ΔΔG(c) and a sign change of ΔΓ23 with c for chaotropic salts (pp. 10983–10984). An m-value therefore describes only the linear regime.
- (inference) For a salt, check the ν convention. HD14 take a33 ≈ 1 for 1:1 salts, which holds for the mean ionic activity a± but not for the salt activity (≈ ν). Pegram & Record 2008, Eq. 1 (10.1021/jp800816a), carries the factor ν explicitly. When citing an m-value from either, state whether Γ counts ions (Γ+ + Γ−) or salt units (Γ_salt).
- Units differ between the two: in Pierce m is in M⁻¹, while Smith 2004 quotes m in kJ mol⁻¹ M⁻¹. State the units.
- Sign: m > 0 for a denaturant, i.e. for ΔΓ23 > 0 (Pierce p. 13; Smith 2006a, p. 2868, 10.1021/jp056100e).

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
- Other G_ij follow by index changes, e.g. G32^∞ from Eq. 34 with 1 ↔ 3. Then Γ23 = ρ3(G23 − G21) (§4).
- Stability: μ_ii ≥ 0 and μ_ij < 0 for i ≠ j (Eq. 23). A negative N12 constrains the data (Eqs. 28–29).
- Salts: Smith keeps μ_ij general because activity-coefficient relations for salts are system dependent (Discussion). Applied to caffeine–salt with fitted ln γ and VPO: Hervø-Hansen et al. 2023 (10.1021/acs.jpcb.3c01085).
- Matteoli & Lepori (10.1063/1.447034): G_ij are insensitive to κ_T and PMVs away from critical points, so SI values often suffice for those terms (Smith 2008, Conclusions).
- Smith reads N_ij as the change in j within a "local spherical volume" on placing i at the centre (p. 124509-2). The house text keeps that reading for radial KBIs only.

## 15. Fluctuation theory: second derivatives, solute volume, interfaces

Source: Ploetz & Smith 2013, Adv. Chem. Phys. 153, 311 (10.1002/9781118571767.ch4). The PMC text
lacks the equations, so the statements below are from prose; check equation forms in the original.

- **Second cosolute derivative of K (§11.4)**: ∂²lnK/∂(ln a3)² is set by fluctuations of an
  instantaneous preferential interaction coefficient Γ(t) in the local region (form presumably
  N3(t) − (ρ3/ρ1)N1(t); the equation is stripped)
  around each solute form. A near-zero second derivative (constant m-value) means similar Γ
  fluctuations for both forms. Compare the nonlinear ΔΓ″23 of Heyda & Dzubiella 2014 (§11).
- (inference) With an exact site partition, Γ(t) = Σγ_i(t), so the variance splits into site
  covariances ⟨δγ_iδγ_j⟩. This would attribute the curvature to sites the way Σγ_i attributes Γ.
- **Solute volume and reaction compressibility (§11.4)**: an instantaneous infinite-dilution pseudo
  volume follows from the local solvent count, N1(t) versus the same volume of bulk. The pressure
  second derivative of K involves fluctuations of that volume. (inference) The explicit-solvent counts
  in D(δ) give the same quantity per site.
- **Do not** apply bulk-system fluctuation formulas to each solute form: "a solute, even the size of
  a protein, cannot be formally treated as a system", and the two forms are not independent species
  (§11.4). This applies to any per-site compressibility or heat capacity.
- **Convergence in practice (§13)**: they average running KBIs over about one solvation shell where
  they flatten, and call the choice subjective. κ_T from plain integration is "questionable at best";
  PMVs and chemical-potential derivatives converge better because they involve only *differences*
  of KBIs. Γ23 = ρ3(G23 − G21) is such a difference.
- **Planar analogue of a surface-anchored domain (§8.5)**: Gibbs adsorption at a liquid–vapour
  interface uses Γ_j relative to the primary solvent, from ∫[g_j(z) − g_1(z)] dz along the normal,
  integrated until the value stops changing ("many solvation shells"). Sign of Γ_j sets the sign of the
  surface-tension change, since the activity derivative is positive. Likely underlying paper (not
  checked against the review's reference list): Chen & Smith 2008 (10.1021/jp711062a).
- Terminology: Ploetz & Smith's "local region" is an open sub-volume of bulk solution with random
  origin (finite-volume KBI sense; see §12 above). Do not use it for the solute-anchored D(δ).

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
| ρ3G23 (molar scale) | dimensionless | molecules | differs from Γ23 by ≈ ρ3V̄2 (§7) |
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
| surface excess Γ_j at an interface (Ploetz & Smith §8.5) | number / area | nm⁻² | not the solute Γ23 |

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
4. Inversion round trip: G_ij → (κ_T, V̄_i, a33 or μ_ij) by the forward relations (§3, BN77 Eqs. 2.1–2.6) → G_ij by inversion (§14). Inputs must return to machine precision. (inference)
5. Γ23 = φ1(∂m3/∂m2)_{T,P,μ3} + φ3(∂m3/∂m2)_{T,P,μ1}, and (∂m3/∂m2)_{T,P,μ1} = Γ23 − 1/a33 (§6).
6. Σγ_i = Γ and Σv_i = Vol[D] for an exact partition (§13).

**Limits with known answers**
7. Ideal gas: all G = 0, k_BTκ_T = 1/ρ, a33 = 1. A closed box biases the raw integral (−0.456 nm³ in the siba-p/kbkit validation); corrections must remove it.
8. Hard spheres: G = (S(0) − 1)/ρ with Carnahan–Starling S(0) (siba-p/kbkit validation).
9. Symmetric ideal mixture: G_ij^SI = k_BTκ_T − V̄_i − V̄_j + Σ_kρ_kV̄_k² (Smith 2008, Eq. 35) gives Δ_AB = 0 (BN77 Eq. 2.14) and ∂ln a/∂ln x = 1.
10. Relabelled water: relabel a random fraction of water molecules as "cosolute". Then G23 = G21 and Γ23 = 0 exactly; any nonzero value is bulk-ratio, closed-box or bookkeeping error. Implicit-solvent analogue: a cosolute interacting with the solute only by excluded volume, whose ρ3G23(δ) must plateau at −ρ3 × excluded volume. (inference)

**Physical constraints**
11. Salts: Γ+ − Γ− = −Z with Z signed (Record & Anderson 1995, Eq. 29, 10.1016/S0006-3495(95)80254-7). Simulated single-ion counts must satisfy it at the plateau; failure means too small a domain or a contaminated bulk region.
12. Stability: η > 0, a33 > 0, μ_ii ≥ 0, μ_ij < 0 for i ≠ j (Smith 2008, Eq. 23); the fluctuation matrix B is positive definite.
13. Closed-box normalisation: ∫ h_ij over the whole periodic box equals −δ_ij/ρ_i (§1). Checks RDF normalisation and the integrator.

**Cross-checks between estimators, one trajectory**
14. Molal vs molar with explicit water: Γ23(δ) − ρ3G23(δ) = −ρ3G21(δ), and G21 → k_BTκ_T − V̄2 at infinite dilution without cosolute (Smith 2008, Eq. 34). This yields V̄2 per molecule; compare it with the NpT box-volume difference with and without solute. (inference)
15. Σγ_i plateau versus ρ3(G23 − G21) from solute-centred RDFs with GvdV correction and Krüger extrapolation (simulation.md §2–3).
16. Partition invariance: total Γ must not depend on power, additive or ordinary Voronoi assignment; only site terms may. (inference)
17. r_3 invariance: at large δ the plateau must not depend on the cosolute radius used to build D(δ). (inference)
18. Bulk ratio: n23 − (n3/n1)n21 = Γ23(R)(1 − n21/n1) (§9); compare global and moving ratios numerically.
19. Two-domain round trip: Γ = b1·ASA·(m3/m1)(K_p − 1) (Pierce 2008, Eq. 50) must reproduce γ_i where v_i^acc > 0. (inference)
20. Linkage routes: ΔΓ23 (molal) equals [Δ(ρ3G23) + ρ3ΔV̄2]/φ1 (Smith 2006a, Eq. 46, 10.1021/jp056100e).

**Convergence**
21. Converged Γ23 is independent of box size, and agrees between GCMC and NVT with GvdV correction. (inference)
22. Krüger extrapolation: L·G^V linear in L over ≥ 1 nm with R² ≥ 0.99 (KBKit criterion, Peroutka et al. 2026); F^∞ in nm⁴ (§16).
23. Block averages (first versus second half) give sampling error; the spread between estimators gives systematic error (simulation.md §2).

