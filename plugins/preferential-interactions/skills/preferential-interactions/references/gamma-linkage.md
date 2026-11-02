# Equations: Γ23 definitions, Wyman linkage, ensemble offsets, molal vs molar scale, m-value

Notation: 1 = water, 2 = solute, 3 = cosolute. ρ_i is a number density and m_i = N_i/N1 a
molality, written as a number ratio, so m3/m1 = ρ3/ρ1. φ_i = ρ_iV̄_i. β = 1/k_BT, and RT replaces
k_BT on molar quantities. h_ij = g_ij − 1. G_ij = G_ji, but N_ij = ρ_jG_ij counts j around i, so
N_ij ≠ N_ji. The superscript ° denotes the solute at infinite dilution (m2 → 0).

Sources give the paper's equation number and DOI; equation numbers were checked against
full texts unless marked. "(inference)" marks a step no cited paper states. Section numbers (§N)
are shared across the equation files; SKILL.md maps each § to its file.

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
- Resolved by pair distance, and for B22: simulation.md §8.

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
