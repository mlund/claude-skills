# KBIs and Γ23 from MD and MC simulations: practical guide

Read this before writing or reviewing a Methods section that extracts KB integrals or a
preferential interaction coefficient from simulation, or before running such an analysis.
§ numbers refer to the equation files listed in SKILL.md. "(inference)" marks steps that no
cited source states.

Contents: 1 why raw integrals fail · 2 radial route (bulk mixtures) · 3 solute at infinite
dilution · 4 implicit-solvent MC · 5 salts · 6 tools · 7 reporting checklist · 8 PMF and B22
slopes, finite solute, slow states

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

**2a. Ganguly–van der Vegt RDF correction** (10.1021/ct301017q, Eq. 5; estimators.md §9):

    g^GvdV_ij(r) = g_ij(r) · N_j f(r) / [N_j f(r) − ΔN_ij(r) − δ_ij],   f(r) = 1 − (4π r³/3)/⟨V⟩
    ΔN_ij(r) = ρ_j ∫₀^r 4π r'² [g_ij(r') − 1] dr'

It removes the depletion of j from the rest of the box when j accumulates near i. (The KBKit
docstring writes the upper limit of ΔN as r_max; the code integrates cumulatively to r.)

**2b. Krüger finite-volume integral** (10.1021/jz301992u; estimators.md §12), on the corrected g:

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

- **Radial form**: Γ23 = ρ3(G23 − G21) from two solute-centred RDFs (gamma-linkage.md §4). The
  corrections of §2 apply to each RDF. siba-p/kbkit's `pb` command computes exactly this.
- **Counted-solvent form, preferred for nonspherical solutes** (Hervø-Hansen et al. 2023,
  10.1021/acs.jpcb.3c01085): Γ23(R) = n23(R) − (ρ3/ρ1)_bulk n21(R) over a layer or domain around
  the solute. Use the moving bulk ratio, (n3 − n23)/(n1 − n21) (Pierce et al. 2008 Eq. 56; Ploetz &
  Smith 2013 §13; estimators.md §9). The global box ratio underestimates Γ by the factor
  (1 − n21/n1). Judge convergence by a plateau in R or δ.
- The moving bulk ratio plays the role of the GvdV correction for this estimator: both remove the
  depletion of the finite box. (inference)
- The Krüger 1/L extrapolation applies to radial RDFs, also solute-centred ones, but not to a
  solute-shaped domain D(δ): there the surface law does not hold (estimators.md §12). Use the δ
  plateau.
- Plateaus reported in practice: caffeine Γ23 from running KBIs at r = 1.6–2.0 nm; group terms at
  ≈ 1.0 nm from the surface (Hervø-Hansen et al. 2023). Ploetz & Smith average over about one
  solvation shell where the integral flattens, and call the choice subjective.
- With a site partition, report Σγ_i alongside the radial Γ23 from the same trajectory as a check.

## 4. Implicit-solvent (McMillan–Mayer) MC

- No water particles: the estimator ⟨N3(D)⟩ − ρ3 Vol[D] gives the molar-scale ρ3G23, not the molal
  Γ23. Convert with gamma-linkage.md §7 before comparing with experiment or explicit-solvent results.
- ρ3 must be the bulk density far from the solute. In canonical MC, N3/V includes the solute's
  excess and overestimates ρ3 for an accumulated cosolute; measure ρ3 in a far region or use GCMC
  at fixed cosolute activity. (inference, the same depletion as §1)
- Hervø-Hansen et al. 2023 ran caffeine CG MC in both canonical and grand-canonical ensembles.
- The continuum has no volume of its own, so the model cannot supply V̄2°, which the conversion needs.
  At low cosolute φ1 ≈ 1 and k_BTκ_T ≈ 1 cm³ mol⁻¹ ≪ V̄2°, so Γ23 ≈ ρ3G23 + ρ3V̄2° (from Smith 2006a
  Eq. 34, 10.1021/jp056100e). Take V̄2° from experiment, an explicit-water run or an estimate, and say which.
- Differences survive better than absolute values: φ1 ∂lnK/∂ln a3 = Δ(ρ3G23) + ρ3ΔV̄2° (Smith 2006a,
  Eq. 46), so for a process with small ΔV̄2° the implicit-solvent Δ(ρ3G23) ≈ ΔΓ23. When V̄2° is unknown,
  report differences between states. (inference: the "small ΔV̄2°" criterion)
- Two-domain quantities need an assumed water content: without water particles, B1 (and so K_p, b1)
  is an assumption, e.g. the cosolute-accessible shell at bulk water density. State it.
- KB inversion of implicit-solvent output (Hervø-Hansen et al. 2023, 10.1021/acs.jpcb.3c01085,
  section "Kirkwood–Buff Analysis of Experimental and/or Simulation Data", Eqs. 11–15; the
  inversion equations are in kb-integrals.md §14): the MC excess chemical potential of the solute,
  μ2^ex = ln γ2, is fitted to

      ln γ2 = 2A2m2 + (3/2)B2m2² + C1m3 + C2m2m3                           [Eq. 13]
      −(1/M1) ln a1 = m2 + A2m2² + B2m2³ + ν3m3 + A3m3^{3/2} + B3m3² + C1m2m3 + C2m2²m3   [Eq. 14]
      ln γ3± = (1/ν3)[3A3m3^{1/2} + 2B3m3 + C1m2 + ½C2m2²]                 [Eq. 15, printed as (6/2)A3]

  A2, B2 from salt-free data; C1, C2 per salt; A3, B3 binary salt parameters from experimental
  water–salt data; Eq. 14 is the Gibbs–Duhem-consistent water activity (ν3 = ions per salt unit).
  V̄_i and κ_T are infinite-dilution values, held constant. The inversion then returns all six
  G_ij, including the water ones. The same fit takes experimental input instead: VPO residual
  osmolalities give C1, C2 directly (Eq. 3, Table 2), so the route works for experiment or simulation.
  - MC-SASA treats both water and salt implicitly (salt enters through a surface-tension term), so
    the simulation contains only solute particles. What the model supplies is the m2- and
    m3-dependence of ln γ2. G13 and G33 are set mainly by the experimental water–salt data, and G11, G12
    lean on the external volumes and compressibility; the cosolute–solute information sits in
    ∂ln γ2/∂m3. The
    authors justify constant V̄_i because the KBIs "are only weakly dependent on" them and "are
    dominated by changes in activity data".
  - The inversion and the direct estimator need the same outside input (V̄2°); the inversion just
    makes it explicit. It also gives a33 and so k_S without counting cosolute.
  - (inference) The MC μ2^ex is a McMillan–Mayer quantity (constant solvent chemical potential, molar
    concentrations). Using it as a Lewis–Randall molal ln γ2 at constant P neglects the scale and
    ensemble conversion (gamma-linkage.md §7). The error is small at low solute and cosolute
    concentration.
- Salts in a primitive model: Γ+ − Γ− = −Z still holds and is a convergence check (checks.md §17);
  hydration-layer effects enter only through ion radii and whatever effective potentials the model has.

## 5. Salts

- Ion–ion and ion–molecule RDFs are computed per ion; KBIs for the neutral salt component then
  follow from mole-fraction-weighted sums: G_iI = x₊G_i+ + x₋G_i−, and G_II′ = Σ x x′ G over the four
  ion pairs (KBKit, after Ploetz, Smyers & Smith 2025, 10.1021/acs.jpcb.4c07583).
- This is the indistinguishable-ion or salt-component view (salts.md §10). Single-ion Γ±
  are well-defined counts, but only Γ+ + Γ− enters the linkage.
- Check per-ion RDFs with the running charge Q_C(R) = z_C + Σ_j z_jρ_jG_Cj(R), which must reach
  zero (salts.md §10).
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

Before reporting, run the verification checks in checks.md §17; the relabelled-water test
(item 10) and electroneutrality for salts (item 11) catch most estimator errors.

## 7. Reporting checklist

1. Ensemble, box length, run length, number of each species, force fields.
2. Which estimator (raw, GvdV, Krüger extrapolated, fluctuation, counted-solvent) and fit or
   plateau range; show running KBI or Γ(δ) plots.
3. Sampling error from blocks; systematic error from the spread between estimators.
4. For Γ: ensemble and concentration scale (molal Γ23 versus molar ρ3G23), bulk-ratio choice.
5. For salts: ion or salt-component quantities, and the electroneutrality treatment.
6. Software and version, with DOI or repository URL.

## 8. PMF and B22 slopes, finite solute, slow states

Translated from Hill 1955 I (10.1063/1.1742068) and II (10.1063/1.1740737). Hill works at the
McMillan–Mayer level with explicit binding and writes no G_ij or Γ. Hill's a is cosolute 3, P is
solute 2, x is the absolute activity of 3, and 𝔅2 is B22. Everything here is (inference) unless an
equation is cited, and it still needs a literature source before being called established.

Tested by `scripts/check_pair_linkage.py` (exact 1D lattice, implicit solvent) and by hand against
the analytic limits noted below. The (T, P) forms rest on Gibbs–Duhem algebra only, and nothing
has been run on a protein. To check an analysis that uses this section, see checks.md §17,
items 24–27; the script tests the relations, not your data.

Notation: ΔX(r) = X(pair held at r) − 2X(isolated solute), with the excess counted in D(δ) around
the pair or the single solute.

**Bound and thermodynamic excess.** Hill I, Eq. 38 splits the excess into a cutoff-dependent bound
count and a free remainder; only their sum is thermodynamic. Per solute at m2 → 0, with fixed V,
μ1 and μ3:

    N23 = ρ3G23 = ⟨s⟩ + free excess                [Hill I, Eq. 38; Smith 2006a, Eq. 14]

- The sum is the molar coefficient. Hill notes that dialysis work customarily neglects the free
  term, but it holds the excluded volume (Hill I, p. 629), which is ≈ −ρ3V̄2 and dominates for
  weak cosolutes (gamma-linkage.md §7).
- Hill advises dropping explicit binding when it is weak, because the split is then arbitrary.

**Slope of the PMF at each distance.** One run at one composition gives the slope of the PMF:

    implicit (T, μ1):  ∂ln g22(r)/∂ln a3 = ΔN23(r)
    explicit (T, P):   ∂ln g22(r)/∂ln a3 = ΔΓ23(r) = ΔN23(r) − (ρ3/ρ1)ΔN21(r)
    salt:              ∂ln g22(r)/∂ln a± = Δ(Γ+ + Γ−)(r)   (molar scale if implicit; fixed pH)

- g22 is normalized to bulk, so the association offset of gamma-linkage.md §5 does not enter here.
- The implicit and explicit forms are different derivatives. Adding cosolute in implicit MC holds
  μ1 fixed and lets P rise, so convert before comparing with experiment at fixed P
  (gamma-linkage.md §7).
- Check, cosolute: ideal cosolute and hard spheres give ΔN23 = ρ3V_overlap, the Asakura–Oosawa
  result βw = −ρ3V_overlap.
- Check, salt: Debye–Hückel point charges give ½κZ²ℓ_B e^(−κr) from both sides, to leading order.

**Slope of B22.** B22 = −½G22° (Hill I, Eq. 89), measured at dialysis equilibrium, so:

    ∂B22/∂ln a3 = −½ ∫ g22(r) ΔN23(r) dr          (ΔΓ23 if explicit at T, P)

For an aggregating solute, B22 = B22(monomer) − K2 with K2 = c010/c100² (Hill II, Eqs. 19, 23).
The split depends on the cutoff for "aggregate"; B22 does not.

**Finite solute concentration.** Hill II, Eq. 9 gives the series for the bound count at fixed γ and
W. With all derivatives free it applies to the thermodynamic excess:

    per solute:    (ρ3 − ρ3°)/ρ2 = ∂ln c1/∂ln a3 − ρ2∂B22/∂ln a3 − ½ρ2²∂B3/∂ln a3 − …
    differential:  (∂ρ3/∂ρ2)_{T,μ1,μ3} = ∂ln c1/∂ln a3 − 2ρ2∂B22/∂ln a3 − (3/2)ρ2²∂B3/∂ln a3 − …
                                       = ρ3G23/(1 + ρ2G22)

- ρ3° is the density at the same μ1, μ3 without solute, and the derivatives are at fixed ρ2. The two
  quantities agree only at ρ2 → 0; the second is the derivative of ρ2 times the first.
- Counting cosolute around a protein in a box gives the per-solute form, which sizes the error of
  one protein in a box, ρ2 = 1/V. Periodic images are not an isotropic g22, so treat it as an order
  of magnitude. The differential form is the molar counterpart of the molal form in
  gamma-linkage.md §4.
- Ions: the per-solute term reduces to the Donnan result, N2+ + N2− rising by Z²ρ2/(4ρ_s), with ρ_s
  the salt density (Z²ρ2/(2ρ_s) in the differential form). For Z = 10, a (10 nm)³ box and 100 mM
  salt, that is ≈ 0.4 ions per solute.

**Slowly exchanging states.** Counting does not converge for a site with a long residence time.
Treat each slow state σ (site occupancy, protonation, conformation) as its own solute, and take pσ
from a separate binding or titration free energy:

    Γ23 = Σσ pσ (s3σ − m3s1σ + Γ23^σ)
    ∂pσ/∂ln a3 = pσ (Γσ,total − ⟨Γ⟩)                 (Γσ,total = s3σ − m3s1σ + Γ23^σ)
    g22(r) = Σσσ′ pσpσ′ gσσ′(r)                      [Hill I, Eq. 87; pσ at m2 → 0]

- Γ23^σ counts only cosolute and water outside the state's bound set. On the implicit scale, drop
  the water terms and read N23.
- The label must be identical in pσ and in the conditional runs; the total is then independent of
  the definition (Hill I, Eq. 36).
- The binding polynomial c1 = Σ x^s H (Hill I, Eq. 71) carries these weights. Fixed-charge MC runs
  can be combined this way, which includes charge-regulation attraction (Hill I, Eq. 87, after
  Kirkwood & Shumaker).
