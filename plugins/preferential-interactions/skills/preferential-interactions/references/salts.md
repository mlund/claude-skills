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
- Origin of the moment conditions. Neutrality is a property of the equilibrium state, not a
  constraint on the partition function: a uniform state satisfying the BGY equations cannot
  sustain a bulk electric field, so Σ_α z_αρ_α = 0 (Martin 1988, Eqs. 2.10–2.12 and footnote 3,
  10.1103/RevModPhys.60.1075). For the one-component plasma, Martin derives Ĉ(k) → −βv̂(k) at
  small k from the BGY hierarchy (Eq. 2.47). Taking the multicomponent analogue (inference from
  here), Ĉ(k) = −4πℓ_B zzᵀ/k² + Ĉ^SR(k) with Ĉ^SR regular at k = 0, the Ornstein–Zernike relation
  B(k)⁻¹ = diag(1/ρ) − Ĉ(k) and the Sherman–Morrison formula give

      zᵀB(k)z = (k²/4πℓ_B) κ_eff²/(k² + κ_eff²),    κ_eff² = 4πℓ_B zᵀ[diag(1/ρ) − Ĉ^SR]⁻¹z.

  Order k⁰ vanishes (zeroth moment), order k² is 1/(4πℓ_B) (second moment; Martin Eq. 1.28), and
  a screening constant first appears at order k⁴. Check: for the OCP, κ_eff² = 4πℓ_B ρk_BT ∂ρ/∂P
  and the k⁴ term reproduces Martin's compressibility sum rule (Eq. 2.58, whose χ_T is ∂ρ/∂P by
  dimensions). The moment conditions hold in conducting phases; Martin notes that the second
  moment fails where ions bind into non-screening dipoles (Sec. II.D). A large open subvolume
  has charge fluctuations proportional to its surface, not its volume (Martin Eq. 1.33). This
  supports Ben-Naim's reading (Dissent item below): ion KBIs are well defined, and B is singular
  because of the interaction, not an added constraint. A model whose electrostatics is truncated
  (finite û(k → 0)) has a nonsingular B; any neutrality then comes from neutral-pair moves.
- Running charge as a simulation check: Q_C(R) from per-ion running KBIs around a charged solute
  should reach zero once R exceeds the ion atmosphere (Ploetz et al. 2025 show it as an intensive,
  non-diverging diagnostic). A residual plateau signals unconverged RDFs or a box too small for
  the atmosphere. A truncated or short-ranged electrostatic kernel (decaying faster than r^−3) is
  outside the Stillinger–Lovett conditions, so the residual then partly reflects the model. The
  Z = 0, R → ∞ case is the Gee/Hervø-Hansen relation above.
- Effective charge depends on the cutoff; its limit does not. Hill's isoelectric condition,
  z + Σ_i z_iM̄_i/M̄_P = 0 (Hill 1955 II, Eq. 10, 10.1063/1.1740737), counts bound ions only and
  holds at one activity. (inference) Over D(δ), with bulk neutrality cancelling the volume term,
  Z_eff(δ) = ⟨Z⟩ + Σ_i z_i⟨N_i(D(δ))⟩ → 0 at every activity, the solute form of Q_C(∞) = 0, with
  ⟨Z⟩ including titrated protons and i running over all other ions. An
  isoelectric point based on Z_eff therefore depends on δ. Hill defers ions to a 1954 chapter
  (not read), and ∂/∂ln x_i of one ion alone cannot be realized, so use ∂/∂ln a±.
- Caution, screening lengths: Kumari & Podgornik 2024 (10.1063/5.0187324; equations checked in
  arXiv:2311.10602v1) write κ² = (4πℓ_B/e²)[Σ_ij e_ie_j(∂²f/∂c_i∂c_j)⁻¹ + c₁e²N₁(∂²g̃/∂φ²)⁻¹]
  (Eq. 19), the second term from macroion charge regulation, and equivalently as charge
  fluctuations at fixed charges (Eq. 17). Their f (Eq. 5) is ideal mixing plus the
  charge-regulation free energy; electrostatics enters only through the mean-field potential ψ
  (Poisson–Boltzmann, Eq. 14). With exact Coulomb correlations the first term is 4πℓ_B zᵀBz
  (kb-integrals.md §1), which is zero (Stillinger & Lovett Eq. 22). Do not evaluate the formula
  with simulated or experimental KBIs of independent ions; a finite screening length then needs
  the Coulomb-subtracted response of the previous items.
- Dissent: Ben-Naim (Molecular Theory of Solutions, 2006, cited by Ploetz & Smith 2013, §16) holds that KB theory is valid for salts with independent ions, since KBIs are grand-canonical and electroneutrality is an unnecessary constraint on them; only the data to vary ion concentrations separately are missing. Ploetz & Smith adopt dependent ions for lack of data. Substituting N_2 = N_+ + N_− is an index change; electroneutrality then leaves one independent salt fluctuation.
- (inference) For the house style: single-ion Γ± from simulation are well defined counts (Ben-Naim's view), but only Γ+ + Γ− is a thermodynamic derivative (§10 above). Say which view a sentence relies on.
- Experimental salt data: Arakawa & Timasheff 1982 (10.1021/bi00268a034) measure (∂g3/∂g2)_{T,μ1,μ3} by densimetry for BSA and lysozyme, with the salt as one component and no charge term in Eq. 1. Activities follow a3 = m3²γ±² for NaCl, NaOAc, KSCN and MgSO4, and 4m3³γ±³ for CaCl2, Na2SO4 and MgCl2 (Eqs. 4–5). NaCl, acetate, Na2SO4 and MgSO4 are excluded; KSCN and CaCl2 are slightly positive and MgCl2 is near zero, all within error. Add the charge term yourself before comparing with Γ+ + Γ− (inference).
