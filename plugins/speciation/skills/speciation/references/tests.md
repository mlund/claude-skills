# Verification tests

Choose tests that could fail if the claim were wrong. Report seeds, error bars, and
what each test can't show. For any simulation, also check energy drift, net charge
and acceptance rates.

## Exact checks

| # | Test | Pass | Shows |
|---|---|---|---|
| E1 | Implicit-ion independent sites, no interactions (`⚛HA = ⚛A + ~H+`) | α = x/(1 + x), x = 10^(pH_in − pK_a) | Sign, units, K convention. Holds only for this ensemble |
| E1b | Paired moves with ideal ions, Z sites, salt | P(n) ∝ C(Z,n) xⁿ I_n(2λ), λ = a c°V (a_Na = a_Cl). Not Henderson–Hasselbalch unless Z ≪ λ | Counterion and volume factors. `--paired` in the script |
| E2 | No interactions, salt pair, fixed charge Z | ⟨N_+N_-⟩ = λ² exactly, λ = a c°V_free. ⟨N_+⟩⟨N_-⟩ differs; for Z = 0, ⟨N⟩ = λ I₁(2λ)/I₀(2λ) | Activity folding, volume factor. Compare the mean of the product |
| E3 | Cycle closure | ln K_eff(DAP) − ln K_eff(ACP) = ln K_eff(salt reverse) | Consistent activities |
| E4 | Relabelling: a_i → a_i exp(−z_i βeΔΦ) for any ΔΦ, same seed | Identical trajectory | Move uses only Donnan-free combinations. **Algebra and code, not physics** |
| E5 | Reversal: for any states o, n, P(o→n)/P(n→o) | Equals π(n) g(n→o) / [π(o) g(o→n)], with proposals g and all activity, count, volume and energy factors in π | Detailed balance bookkeeping |

| E6 | Two sites at pH_in = pK_a, distance d = l_B, no ions | ⟨N_A⟩ = 0.812 with site–site Coulomb, 1.000 without | Intramolecular Coulomb is on. E1 and E2 can't see this |

| E7 | Ideal 2A ⇌ B and A + B ⇌ C at low N | ⟨N_i⟩ match the exact sum over N with weights Π(c°V)^N/N! · K^ξ | ν̄, volume and factorial terms. Small N exposes wrong count factors that large N hides |
| E9 | Solubility: excess solid, then too little | s = (K_sp/4)^(1/3) for M(OH)₂ when ideal; full dissolution when depleted | Finite reservoir, no count factor |
| E8 | Two routes to one product | Same composition; K_eff multiply around the cycle | Consistent constants |

`scripts/ideal_reference.py` gives E1, E1b, E2 and E4 values. Faunus check of E1b, Z = 10, x = 1: 0.4701 ± 0.0004 at
λ = 20 (exact 0.47019), but 0.3118 at λ = 2 (exact 0.31215), a small significant gap that is unexplained.

## Numerical checks

| # | Test | Pass | Shows |
|---|---|---|---|
| N1 | ACP only vs DAP only, with salt exchange | Same α within error | L&J self-consistency. Uncorrected cpH must **fail** this, so also run it as a control |
| N2 | Salt-only bulk run at chosen a | Recovers target c (±error) | Reservoir activity. Widom or CS+MSA input |
| N3 | Ideal Donnan limit, N_res ≫ 1 | N± approach the macroscopic rule (theory.md). Use `--Z` exact values at small N | Partitioning machinery |
| N4 | Closed RxMC at open-run ion counts | α agrees | **Weak.** Charge balance gives Z = N_+ − N_- + N_H, so with few free H⁺, the seeded counts nearly fix α |
| N5 | Limits: η → 0, or salt → high | ΔΦ → 0, GCT → uncorrected cpH trend | Comment's dilute/high-salt limit |
| N6 | Beyer shift on uncorrected cpH | Shifted curve meets GCT | Shift, with its stated limits for multivalent ions |
| N7 | Size and shape | α stable with cell size | Finite-size and boundary effects |
| N8 | d⟨N_A⟩/dpH_in = ln 10 · Var(N_A) at fixed salt activities | Equal within error | Sampling of the titration ensemble |
| N9 | Start from all HA and all A | Same α | Equilibration |

To test physics independently of N4, compare with a different measurement of pH_sys in
a closed run (Widom or surface Widom), or against published data at matched labels.

## Reference data

Comment Table 1 (Z = 600, a = 80 Å, pK_a = 5.4, 100 mM NaCl, N_A⁻; arXiv values, check
against the published table):

| pH_in | η = 29.6%: canonical, cpH, GCpH | η = 6.4%: canonical, cpH, GCpH |
|---|---|---|
| 5.1 | 124.2, 168.3, 124.0 | 124.1, 143.9, 124.2 |
| 5.6 | 205.0, 284.1, 205.3 | 205.0, 235.3, 205.0 |
| 6.1 | 305.0, 411.4, 305.1 | 305.0, 344.4, 305.1 |
| 6.6 | 412.0, 512.9, 412.3 | 412.0, 453.0, 412.5 |

Our GCT at η = 29.6%: ESPResSo `ReactionEnsemble`, cubic P3M (2 seeds): 123.3, 203.7, 301.4,
402.8. Faunus cubic Ewald (2 seeds): 123.3, 205.1, 303.5, 403.8.

Faunus GCT reproduction at η = 29.6% (mean of 3 seeds ± s.e., our run): 125.4 ± 0.4,
206.1 ± 0.1, 303.2 ± 0.9, 406.2 ± 0.5. About 1.5% low at pH 6.6, unexplained. Geometry
is assumed, since Table 1 doesn't state it: spherical cell R = 120 Å, hard ions of radius
2 Å, sites at r = a + 2 Å, ε = 78, T = 298.15 K, a_salt from CS+MSA.

Use the canonical and GCpH columns as targets, not cpH: its salt count isn't stated, and
our uncorrected cpH doesn't reproduce it (ESPResSo, cubic: 134.1, 233.8, 353.8, 463.9 with
297 pairs; 143.1, 247.7, 367.2, 473.2 with 436). A mismatch with that column alone
doesn't indicate a bug.

## Documents

- Every pH has a phase, or a stated reason why none is needed.
- Every equation with a potential gives a sign convention. Check the pH_sys relation's sign
  against a negatively charged example.
- Standard state and scale are stated for every activity and K.
- Each claim about a paper was read in that paper; quotations match the published version.
- Claims from us are marked as ours.
