# Glossary and translations

Sections: Conventions, pH and activity, Potentials, Moves and methods, Ensembles and phases, Quantities,
Translation by author.

House notation is fixed; translations aren't automatic. Map a source through its equations, units, phase
and method, not by name. Other usage is different, not wrong: preserve it and explain it.

## Conventions

- **Molar:** μ̃_i = μ_i° + RT ln a_i + z_iFφ_i (Alberty 2001, Eq. 3.2d-1, citing IUPAC's Green Book usage),
  where μ_i° is for a phase at zero electric potential. Our stated convention, writing Φ for the model
  potential. Activity excludes the electrical term. Alberty's μ_i and μ̃_i are the same quantity in two
  conventions, so check which a source uses.
- **Per particle (simulation):** use k_BT and z_i eΦ. Convert explicitly; don't mix with molar forms.
- **Simulation pH:** pH_c,α = −lg a_H,c^α, with a_H,c^α = γ_H,c^α c_H^α/c°. Once declared, pH_sys and
  pH_res are short labels for α = sys, res. Not numerically identical to molality-based pH.

## pH and activity

| House | Definition | Notes |
|---|---|---|
| pH (IUPAC) | −lg[m(H⁺)γ_m(H⁺)/m°], m° = 1 mol/kg | Notional. The I ≤ 0.1 mol/kg condition is for the Bates–Guggenheim standardization, not a limit on the word pH |
| pH_sys, pH_res | See above; state the phase in open or two-phase contexts | |
| pH_in | Input to the acceptance rule | Landsgesell 2017 defines it by a virtual concentration; we don't assume that |
| pc_H(r) | Local proton concentration index, −lg[c_H(r)/c°] | Preserve an author's "local pH" and give their definition |
| a_i (simulated) | (c_i/c°) exp(βμ_i^ex), c° = 1 M, type I (Rockwood) | State the ideal reference and electrical convention |
| a_± | Mean ionic activity; for 1:1, √(a_+a_-) (Gold Book M03774) | |
| Activity product, ratio | a_H a_Cl; a_H/a_Na | Both cancel the electrical term. Neither is a_±. Allowed under Guggenheim 1929 |
| γ_i | exp(βμ_i^ex), when μ^ex excludes the electrical term | |
| λ_i | exp(βμ_i), absolute activity, no standard state | Never just "activity" |
| Type I, type II | Chemical part vs gas-phase fugacity (Rockwood 2015) | Type II has no counterpart in a primitive model |
| eqs | Separated equilibrium solution (IUPAC 2006); compare with pH_res (our mapping) | |
| Suspension effect | Operational: E(sediment or suspension) − E(eqs) = SE1 + SE2 | Not a Donnan potential, per IUPAC 2006 |

## Potentials

| House | Definition | Others |
|---|---|---|
| ΔΦ | Model phase-potential difference Φ_sys − Φ_res. Preferred term | Authors' "Donnan potential"; φ_D (Levin), ψ^Don (Beyer & Holm; ESPResSo), μ_don (Landsgesell 2020) |
| E_D | Measured Donnan emf, salt bridges at zero current (Gold Book D01830; synonym "Donnan potential") | Not ΔΦ without assuming the junctions cancel |
| Φ_B | Periodic model: cell-mean potential relative to outside, from the charge second moment; "modified" adds a net-charge background term. Not ΔΦ, and not a physical membrane potential (theory.md) | ϕ_B, "Bethe potential" (Levin) |
| μ̃_i | Electrochemical potential; independent of phase at equilibrium | μ_i in Alberty §3.2a–c and in Gibbs's sense; μ̂ (Beyer & Holm) |
| μ_i^ex | Excess chemical potential; state the ideal reference and electrical convention | Don't translate "excess electrochemical potential" (B&L 2024) by dropping a contribution |
| EMF | Potential difference at zero current (IUPAC) | |
| Outer, inner, surface | IUPAC: ψ outer, Φ inner, χ = Φ − ψ (PAC 1974, 37, 499) | Reading a model's mean potential as Φ is our step. State once |

## Moves and methods

| House | Meaning | Others |
|---|---|---|
| implicit-ion cpH | Reed & Reed 1992, Debye–Hückel | "original cpH" |
| uncorrected cpH | Explicit ion, ±ln10(pH_in − pK_a) only | OT (Labbez), RR-cpH (Levin), ESPResSo `ConstantpHEnsemble` |
| GCT | L&J move with counterion term; state separately whether salt exchange is included | GCpH (Levin); pair insertion; Faunus coupled reactions |
| ACP, DAP | Add a cation; delete an anion (L&J) | Beyer 2025 prints "ADP" once |
| shifted cpH | Uncorrected cpH with a-posteriori pH shift (Beyer 2025) | |
| closed RxMC | Fixed total protons, pH_sys an output | RMC, RCMC, canonical titration |
| G-RxMC | Reactions plus reservoir exchange (Landsgesell 2020) | Grand-reaction method |
| G-cpH | Uncorrected cpH plus salt exchange; misses the Donnan contribution (Landsgesell 2020) | |
| rGCMCD | Reservoir exchange with explicit ΔΦ (Levin) | |
| K sweeping | RxMC varying pK_a, pH an output (Review) | |

## Ensembles and phases

- **Ensemble:** describe exchanged species and conserved quantities first, then preserve the paper's name.
  Fixed macromolecules alone don't settle the classification (Ullner & Woodward 2000 say grand canonical).
- **Phases:** describe physical phases separately from whether the reservoir is explicit. An implicit
  reservoir can represent two-phase equilibrium.
- **Neutrality:** instantaneous (paired moves); on average (Barr 2012); background (Levin 2023 JCP).

## Quantities

- **α:** degree of ionization, a fraction. N_A⁻ for a count of deprotonated sites.
- **pK_a:** specify the reaction, standard state, and whether intrinsic, thermodynamic or apparent. Bare
  pK_a doesn't universally mean intrinsic. pK_app is the pH at α = 0.5 in the Review.
- **Speciation:** distribution of a system over its chemical states. Working definition, no external source.

## Translation by author

| Source term | Maps to | Condition |
|---|---|---|
| Landsgesell 2020 "extended chemical potential" | μ̃_i | After matching units and the reservoir potential reference |
| Landsgesell 2020 pH_sys, pH_res; bare pH | Same | Their bare pH means reservoir |
| Levin 2023 (JCP): a₊ with qβφ_D | Preserve as theirs | Factor out the electrical term before mapping to a_i |
| pH_gc, pH_R (Levin; B&L 2024) | pH_res | Check the activity convention |
| pH_c, pH_S | pH_sys | Only for the specified closed composition and activity convention. A closed and an open run at the same number need not be the same state |
| GCpH (Comment) | GCT | Identify the corrected paired move; say if salt exchange is included |
| cpH (Comment) | uncorrected cpH | Check the counterion treatment |
| Z_eff (Comment) | N_A⁻ | Only where defined as deprotonated sites, not a renormalized effective charge |
| OT, pK₀ (L&J) | uncorrected cpH, pK_a | State that pK₀ is intrinsic |
| pH_in via virtual c(H⁺) (Landsgesell 2017) | pH_in | Note their definition |
| ψ^Don, μ̂ (Beyer & Holm) | ΔΦ, μ̃ | Check units and reference |
| ESPResSo `constant_pH`, `gamma` | pH_in; K (cpH) or Γ (RxMC) | Check dimensions |
| Software `activity` | a_i | Check dimensions first. A concentration-valued activity needs division by c°; a fugacity or insertion parameter needs its own conversion. Faunus: molar, c° = 1 M |
