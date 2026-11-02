# Equations: salts: single-ion and salt-component coefficients, electroneutrality, validity debate

Notation: 1 = water, 2 = solute, 3 = cosolute. ρ_i is a number density and m_i = N_i/N1 a
molality, written as a number ratio, so m3/m1 = ρ3/ρ1. φ_i = ρ_iV̄_i. β = 1/k_BT, and RT replaces
k_BT on molar quantities. h_ij = g_ij − 1. G_ij = G_ji, but N_ij = ρ_jG_ij counts j around i, so
N_ij ≠ N_ji. The superscript ° denotes the solute at infinite dilution (m2 → 0).

Sources give the paper's equation number and DOI; equation numbers were checked against
full texts unless marked. "(inference)" marks a step no cited paper states. Section numbers (§N)
are shared across the equation files; SKILL.md maps each § to its file.

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
- Neutral solute, salt A_ν+B_ν− at ρ_s, ρ± = ν±ρ_s, ρ3 = (ν+ + ν−)ρ_s (total ion density):

      z+N2+ = z+ρ+G2+ = |z−|ρ−G2− = |z−|N2−,   N23 = N2+ + N2−,
      G23 = (ν+G2+ + ν−G2−)/(ν+ + ν−)

  Source: Hervø-Hansen et al. 2023, SI p. S2 (10.1021/acs.jpcb.3c01085), after Gee et al. 2011 (10.1021/ct100517z). The first relation is electroneutrality of the excess, the Z = 0 case of Γ+ − Γ− = −Z, and a convergence check on per-ion RDFs. Here ρ3 counts ions, not salt units, so Γ23 = ρ3(G23 − G21) is per ion; divide by ν = ν+ + ν− for per salt unit.
- Why ions are not independent species: with cation, anion and solvent as independent variables, electroneutrality makes the number-fluctuation matrix singular (Friedman & Ramanathan 1970, 10.1021/j100715a009; Kusalik & Patey 1987, 10.1063/1.452629). The usual fix is a salt "molecule" or indistinguishable ions; the latter matches Kusalik & Patey (Ploetz & Smith 2013, §16, 10.1002/9781118571767.ch4).
- Local electroneutrality in KB form (Ploetz, Smyers & Smith 2025, 10.1021/acs.jpcb.4c07583; the
  PMC text lacks the equations, so the form is from the prose): the charge within radius R of a
  particle C,

      Q_C(R) = z_C + Σ_j z_jρ_jG_Cj(R),        Q_C(∞) = 0,

  where C is any ion or a neutral molecule (z_C = 0) and j runs over all ions. Ploetz et al. note
  that Q_C deviates from zero over several nm at ambient conditions. Stillinger & Lovett 1968
  (10.1063/1.1670358) add a second-moment condition on the same distributions.
- Why the matrix is singular: in matrix form Q_i(∞) = 0 reads Bz = 0, with B from
  kb-integrals.md §1 and z the vector of ion charges (inference: an algebraic step from the
  relation above). The charge vector is the null vector, so zᵀBz = ⟨δQ²⟩/V = 0: a large open subvolume has no net
  charge fluctuation per volume. This is the singularity in the next item.
- Running charge as a simulation check: Q_C(R) from per-ion running KBIs around a charged solute
  should reach zero once R exceeds the ion atmosphere (Ploetz et al. 2025 show it as an intensive,
  non-diverging diagnostic). A residual plateau signals unconverged RDFs, a box too small for the
  atmosphere, or a truncated electrostatic kernel. The Z = 0, R → ∞ case is the Gee/Hervø-Hansen
  relation above.
- Caution, screening lengths: Kumari & Podgornik 2024 (10.1063/5.0187324) define κ² =
  4πℓ_B Σ_ij z_iz_j[(∂²βf/∂c∂c)⁻¹]_ij. With the identity in kb-integrals.md §1 this is 4πℓ_B zᵀBz,
  which vanishes when B carries the exact Coulomb correlations (inference). The finite values come
  from a free energy whose net-charge Coulomb energy is removed, as in mean-field theory. Do not
  evaluate the expression with simulated or experimental KBIs of independent ions; a finite
  screening length needs a Coulomb-subtracted (short-range direct-correlation) response.
- Dissent: Ben-Naim (Molecular Theory of Solutions, 2006, cited by Ploetz & Smith 2013, §16) holds that KB theory is valid for salts with independent ions, since KBIs are grand-canonical and electroneutrality is an unnecessary constraint on them; only the data to vary ion concentrations separately are missing. Ploetz & Smith adopt dependent ions for lack of data. Substituting N_2 = N_+ + N_− is an index change; electroneutrality then leaves one independent salt fluctuation.
- (inference) For the house style: single-ion Γ± from simulation are well defined counts (Ben-Naim's view), but only Γ+ + Γ− is a thermodynamic derivative (§10 above). Say which view a sentence relies on.
