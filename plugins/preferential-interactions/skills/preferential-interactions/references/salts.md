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
- Local electroneutrality (zeroth moment): the ion atmosphere of an α ion carries charge −z_α
  exactly (Stillinger & Lovett 1968, Eq. 24, 10.1063/1.1670358, there written with g_αγ; the
  bulk neutrality Σ_γ z_γρ_γ = 0, their Eq. 21, lets g be replaced by h). In KB notation, and as
  a running quantity (Ploetz, Smyers & Smith 2025, 10.1021/acs.jpcb.4c07583; the PMC text lacks
  the equations, so the form is from the prose):

      Q_C(R) = z_C + Σ_j z_jρ_jG_Cj(R),        Q_C(∞) = 0,

  where C is any ion or a neutral molecule (z_C = 0) and j runs over all ions. Stillinger & Lovett
  derive it for real electrolytes (molecular solvent, ion pairs or complexes as species), and note
  that it would also hold for pair potentials ∝ r^−p with 1 ≤ p ≤ 3. Ploetz et al. note that Q_C
  deviates from zero over several nm at ambient conditions.
- Why the matrix is singular: Q_i(∞) = 0 for every ion reads Bz = 0, with B from
  kb-integrals.md §1 and z the vector of ion charges. Summed with weights z_iρ_i it is
  zᵀBz = Σ_i z_i²ρ_i + Σ_ij z_iz_jρ_iρ_jG_ij = 0, which is Stillinger & Lovett Eq. 22 (with
  g → h). The charge vector is the null vector, so ⟨δQ²⟩/V = 0: a large open subvolume has no net
  charge fluctuation per volume. This is the singularity in the next item.
- Second moment: −6/κ_D² = (Σ_i z_i²ρ_i)⁻¹ Σ_ij z_iz_jρ_iρ_j ∫h_ij(r) r² d³r (Stillinger & Lovett
  1968, Eq. 23, with κ_D² = 4πℓ_B Σ_i z_i²ρ_i and ℓ_B from the solution's dielectric constant at
  fixed ions, ε0(0), their Eq. 19). Expanding the transform (their Eq. 20) gives the small-k
  charge fluctuation zᵀB(k)z → k²/(4πℓ_B), independent of composition and ion correlations. It
  holds only for Coulomb (p = 1). Debye–Hückel point ions satisfy it; DH with ion sizes in general
  does not.
- Origin of the moment conditions (inference: the algebra below is ours; Martin 1988,
  10.1103/RevModPhys.60.1075, reviews the sum rules). Neutrality is not a constraint on the
  partition function; it follows from the 1/k² Coulomb kernel. With the multicomponent
  Ornstein–Zernike relation B(k)⁻¹ = diag(1/ρ) − Ĉ(k), and Ĉ(k) = −4πℓ_B zzᵀ/k² + Ĉ^SR(k) with
  Ĉ^SR regular at k = 0, the Sherman–Morrison formula gives

      zᵀB(k)z = (k²/4πℓ_B) κ_eff²/(k² + κ_eff²),    κ_eff² = 4πℓ_B zᵀ[diag(1/ρ) − Ĉ^SR]⁻¹z.

  Order k⁰ vanishes (zeroth moment), order k² is 1/(4πℓ_B) (second moment), and a screening
  constant first appears at order k⁴. Bulk neutrality has the same origin: a net charge Q in a
  region of size L costs ∝ Q²ℓ_B/L, which outgrows every extensive term, so excess charge goes to
  the boundary and only neutral combinations of ionic μ are measurable (Lieb & Lebowitz 1972,
  10.1016/0001-8708(72)90023-0, prove the thermodynamic limit of Coulomb matter). This supports
  Ben-Naim's reading (Dissent item below): ion KBIs are well defined, and B is singular because
  of the interaction, not because of an added constraint. A model whose electrostatics is
  truncated (finite û(k → 0)) has a nonsingular B; any neutrality then comes from neutral-pair
  moves.
- Running charge as a simulation check: Q_C(R) from per-ion running KBIs around a charged solute
  should reach zero once R exceeds the ion atmosphere (Ploetz et al. 2025 show it as an intensive,
  non-diverging diagnostic). A residual plateau signals unconverged RDFs or a box too small for
  the atmosphere. A truncated or short-ranged electrostatic kernel (decaying faster than r^−3) is
  outside the Stillinger–Lovett conditions, so the residual then partly reflects the model. The
  Z = 0, R → ∞ case is the Gee/Hervø-Hansen relation above.
- Caution, screening lengths: Kumari & Podgornik 2024 (10.1063/5.0187324) define κ² =
  4πℓ_B Σ_ij z_iz_j[(∂²βf/∂c∂c)⁻¹]_ij. With the identity in kb-integrals.md §1 this is 4πℓ_B zᵀBz,
  which is zero for exact correlations (Stillinger & Lovett Eq. 22). Their finite values come
  from a free energy whose net-charge Coulomb energy is removed, as in mean-field theory. Do not
  evaluate the expression with simulated or experimental KBIs of independent ions; a finite
  screening length needs a Coulomb-subtracted (short-range direct-correlation) response.
- Dissent: Ben-Naim (Molecular Theory of Solutions, 2006, cited by Ploetz & Smith 2013, §16) holds that KB theory is valid for salts with independent ions, since KBIs are grand-canonical and electroneutrality is an unnecessary constraint on them; only the data to vary ion concentrations separately are missing. Ploetz & Smith adopt dependent ions for lack of data. Substituting N_2 = N_+ + N_− is an index change; electroneutrality then leaves one independent salt fluctuation.
- (inference) For the house style: single-ion Γ± from simulation are well defined counts (Ben-Naim's view), but only Γ+ + Γ− is a thermodynamic derivative (§10 above). Say which view a sentence relies on.
