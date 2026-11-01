# KBIs and Γ23 from MD and MC simulations: practical guide

Read this before writing or reviewing a Methods section that extracts KB integrals or a
preferential interaction coefficient from simulation, or before running such an analysis.
Equations referred to by § number are in `equations.md`. "(inference)" marks steps that no
cited source states.

Contents: 1 why raw integrals fail · 2 radial route (bulk mixtures) · 3 solute at infinite
dilution · 4 implicit-solvent MC · 5 salts · 6 tools · 7 reporting checklist

## 1. Why raw running integrals fail

KBIs are defined in the open (μVT) ensemble at infinite volume (§1). MD runs closed (NVT, NpT):
fixed N_j makes g_ij(r) tend to 1 − O(1/N) instead of 1, and the running integral G_ij(R) =
4π∫₀^R [g − 1]r²dr drifts linearly instead of reaching a plateau. The bias is largest for small
boxes, dilute species and large excesses. Sources: Ganguly & van der Vegt 2013 (10.1021/ct301017q);
Simon et al. 2022 review (10.1063/5.0106162); Peroutka et al. 2026, p. 6823 (10.1021/acs.jcim.6c00344).

Two families of remedies (Peroutka et al. 2026, p. 6823):
- **RDF route**: correct g(r) for the finite particle number, integrate over a finite open
  subvolume with a geometric weight, extrapolate to the thermodynamic limit (§2).
- **Fluctuation route**: particle-number fluctuations in subvolumes of the box, no RDF integral
  (Cortes-Huerto et al. 2016, 10.1063/1.4964779; Heidari et al. 2018, 10.1080/00268976.2018.1482429;
  Sevilla & Cortes-Huerto 2022, 10.1063/5.0076744).

Grand-canonical MC exchanges particles with a reservoir, so the closed-box depletion in step 2a
does not arise; the finite range of the integral still does. (inference)

## 2. Radial route for bulk mixtures (Simon et al. 2022 pipeline)

Applied sequentially by KBKit (Peroutka et al. 2026), following Simon et al. 2022:

**2a. Ganguly–van der Vegt RDF correction** (10.1021/ct301017q, Eq. 5; equations.md §9):

    g^GvdV_ij(r) = g_ij(r) · N_j f(r) / [N_j f(r) − ΔN_ij(r) − δ_ij],   f(r) = 1 − (4π r³/3)/⟨V⟩
    ΔN_ij(r) = ρ_j ∫₀^r 4π r'² [g_ij(r') − 1] dr'

It removes the depletion of j from the rest of the box when j accumulates near i. (The KBKit
docstring writes the upper limit of ΔN as r_max; the code integrates cumulatively to r.)

**2b. Krüger finite-volume integral** (10.1021/jz301992u; equations.md §12), on the corrected g:

    G^V_ij(L) = ∫₀^L [g_ij(r) − 1] 4π r² (1 − 3x/2 + x³/2) dr,   x = r/L,   L = sphere diameter

L cannot exceed the largest r of the RDF, i.e. about half the box length.

**2c. Extrapolation to the thermodynamic limit** (Dawass et al. 2020, 10.3390/nano10040771):

    L·G^V(L) = G^∞ L + F^∞    → G^∞ is the slope of L·G^V versus L

Convergence criterion used by KBKit: a linear region at least 1.0 nm wide with R² ≥ 0.99; otherwise
it raises `KBIConvergenceError` (Peroutka et al. 2026, p. 6825). Passing the criterion "is not a
guarantee of accurate values" (same page): check box size and run length too.

Alternatives without extrapolation (Krüger & Vlugt 2018, 10.1103/PhysRevE.97.051301; as implemented
in KBKit): truncated weights u0 = 1 (poor), u1 = 1 − x³, and u2 = w(r)(1 + 3x/2 + 9x²/4) =
1 − 23x³/8 + 3x⁴/4 + 9x⁵/8 give G^∞ directly; KBKit falls back to u2 when the extrapolation fails.

**Sizes and lengths that worked**:
- 40 vol% ethanol–water, SPC/E + OPLS-AA, boxes 3.2–10 nm, 10–200 ns: 3.2 and 4 nm boxes did not
  converge at any length, and 10 ns failed even at 10 nm; box size and run length must be checked
  together (Peroutka et al. 2026, Fig. 4 and p. 6825).
- Ploetz & Smith 2013 §13 (10.1002/9781118571767.ch4): > 6 nm boxes and > 10 ns help; κ_T from
  plain integration is "questionable at best"; PMVs and chemical-potential derivatives converge better
  because they involve differences of KBIs.

**Errors**: the fit error of G^∞ is not a sampling error. Estimate sampling error by block
averaging (e.g. first versus second half of the trajectory) (siba-p/kbkit README; Peroutka et al.
2026, p. 6823). Report the spread between estimators (raw plateau, GvdV plateau, extrapolated) as a
systematic error.

## 3. Solute at infinite dilution (Γ23)

One solute molecule (protein, caffeine) in a water–cosolute box.

- **Radial form**: Γ23 = ρ3(G23 − G21) from two solute-centred RDFs (equations.md §4). The
  corrections of §2 apply to each RDF. siba-p/kbkit's `pb` command computes exactly this.
- **Counted-solvent form, preferred for nonspherical solutes** (Hervø-Hansen et al. 2023,
  10.1021/acs.jpcb.3c01085): Γ23(R) = n23(R) − (ρ3/ρ1)_bulk n21(R) over a layer or domain around
  the solute. Use the moving bulk ratio, (n3 − n23)/(n1 − n21) (Pierce et al. 2008 Eq. 56; Ploetz &
  Smith 2013 §13; equations.md §9). The global box ratio underestimates Γ by the factor
  (1 − n21/n1). Judge convergence by a plateau in R or δ.
- The moving bulk ratio plays the role of the GvdV correction for this estimator: both remove the
  depletion of the finite box. (inference)
- The Krüger 1/L extrapolation applies to radial RDFs, also solute-centred ones, but not to a
  solute-shaped domain D(δ): there the surface law does not hold (equations.md §12). Use the δ
  plateau.
- Plateaus reported in practice: caffeine Γ23 from running KBIs at r = 1.6–2.0 nm; group terms at
  ≈ 1.0 nm from the surface (Hervø-Hansen et al. 2023). Ploetz & Smith average over about one
  solvation shell where the integral flattens, and call the choice subjective.
- With a site partition, report Σγ_i alongside the radial Γ23 from the same trajectory as a check.

## 4. Implicit-solvent (McMillan–Mayer) MC

- No water particles: the estimator ⟨N3(D)⟩ − ρ3 Vol[D] gives the molar-scale ρ3G23, not the molal
  Γ23. Convert with equations.md §7 before comparing with experiment or explicit-solvent results.
- ρ3 must be the bulk density far from the solute. In canonical MC, N3/V includes the solute's
  excess and overestimates ρ3 for an accumulated cosolute; measure ρ3 in a far region or use GCMC
  at fixed cosolute activity. (inference, the same depletion as §1)
- Hervø-Hansen et al. 2023 ran caffeine CG MC in both canonical and grand-canonical ensembles.

## 5. Salts

- Ion–ion and ion–molecule RDFs are computed per ion; KBIs for the neutral salt component then
  follow from mole-fraction-weighted sums: G_iI = x₊G_i+ + x₋G_i−, and G_II′ = Σ x x′ G over the four
  ion pairs (KBKit, after Ploetz, Smyers & Smith 2025, 10.1021/acs.jpcb.4c07583).
- This is the indistinguishable-ion or salt-component view (equations.md §10). Single-ion Γ±
  are well-defined counts, but only Γ+ + Γ− enters the linkage.
- Lbadaoui-Darvas & Takahama 2019 (10.1021/acs.jpcb.9b06735) applied the Krüger and Dawass
  corrections to aqueous salts and recovered activity-coefficient derivatives close to experiment
  (as reported by Peroutka et al. 2026).

## 6. Tools

| tool | what it does | notes |
|---|---|---|
| **KBKit** (anl-sepsci/kbkit; Peroutka, Stephenson & Servis 2026, 10.1021/acs.jcim.6c00344) | Full Simon et al. pipeline (GvdV → Krüger → Dawass), convergence check, multicomponent and electrolyte KBIs, activity coefficients, G^E and its H/S split, S(q→0). Reads GROMACS .edr, .xvg, .gro/.top. | The user supplies RDFs. Activity and G^E need a composition grid and pure-component runs. No preferential-interaction output (none found in code or docs, Nov 2026). Calls the stability term "thermodynamic factor" (glossary: avoid the symbol Γ for it). |
| **kbkit** (siba-p/kbkit; Panigrahy 2026, GitHub, MIT) | Raw, GvdV and Krüger estimators side by side; binary KB thermodynamics; `pb` for preferential binding ν_pc = ρ_c(G_pc − G_pw); web app. | Validated on hard spheres and the ideal gas. Defaults: plateau over the last 30% of r, fit over 40–90%. Unrelated to KBKit despite the name; cite by repository URL. Its "ν" is the house Γ23. |
| **pyKBI** (Dawass et al. 2019, 10.1016/j.fluid.2018.12.027) | Finite-volume corrected KBIs. | KBKit reproduces its published values. |
| **ComplexMixtures.jl** (Martínez 2022, 10.1016/j.molliq.2021.117945) | Minimum-distance distributions around solutes of any shape, per-atom contributions. | Ordinary Voronoi assignment of counts; global normalization (glossary). |

## 7. Reporting checklist

1. Ensemble, box length, run length, number of each species, force fields.
2. Which estimator (raw, GvdV, Krüger extrapolated, fluctuation, counted-solvent) and fit or
   plateau range; show running KBI or Γ(δ) plots.
3. Sampling error from blocks; systematic error from the spread between estimators.
4. For Γ: ensemble and concentration scale (molal Γ23 versus molar ρ3G23), bulk-ratio choice.
5. For salts: ion or salt-component quantities, and the electroneutrality treatment.
6. Software and version, with DOI or repository URL.
