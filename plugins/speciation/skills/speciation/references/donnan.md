# The word "Donnan"

Five things carry the name. Separate them before judging a paper:

1. **Potential in simulations:** house ΔΦ, the phase potential difference.
2. **Partitioning:** unequal ion concentrations, a computed result.
3. **Equilibrium:** Gibbs–Donnan theory, the ideal product rule.
4. **Pressure:** protein osmometry ("Donnan pressure"; IUPAC: colloid osmotic pressure).
5. **Emf:** E_D, IUPAC's measured quantity (salt bridges, zero current). Later IUPAC guidance
   on suspensions finds "no boundary (or Donnan) contribution" to the suspension effect.

IUPAC defines equilibrium, emf and exclusion, and lists "Donnan potential" as a synonym of the
emf. So house text avoids the phrase. In a cited paper it may mean E_D or ΔΦ: check which.

## Why authors omit it

In a keyword count of 71 papers from one library, 15 use the word (indicative only).

| Reason | Examples |
|---|---|
| Nothing is partitioned: implicit ions or fixed composition | Reed & Reed 1992; Ullner & Jönsson 1996 |
| Closed cell | Ullner & Woodward 2000 |
| Reservoir at infinity: a surface or dilute particle next to bulk, where the potential decays to the reference (our reading) | Ninham & Parsegian 1971; Labbez & Jönsson 2007 |
| Pair moves: it cancels and never appears | Ross et al. 2018; Curk et al. 2022 |
| Absorbed in a gauge: sinh[βφ] with φ′(R) = 0 and φ(R) free (our reading of φ(R)) | Bakhshandeh et al. 2022, Langmuir |
| Different words: salt or ion partitioning, the product rule | Warren 2002 |

These are legitimate choices. Don't flag omission unless it causes a real error.

## Where it is needed

- Relating pH_sys and pH_res, or converting open results to a closed system.
- Algorithms with unpaired ion moves, where it enters the acceptance (Barr 2012; rGCMCD).
- Two-phase physics reported as such: dialysis, gels, coacervates, crystal–solution.

## Where it isn't

- Pair moves or GCT, reporting against reservoir conditions.
- Single-phase closed systems and implicit-ion models.
- Dilute or high-salt limits, where it vanishes (B&L 2024).

## Traps

- **Absent word ≠ absent effect:** partitioning is present in any salt-exchange run.
- **Salt exchange ≠ captured effect:** G-cpH "fails to capture the Donnan contribution,
  even when the simulation includes ion" exchange (Landsgesell 2020).
- **No membrane required:** IUPAC lists gelation and gravity as restraints. Levin & Bakhshandeh 2023 (JCP) use a gravity column.
- **Lagrange multiplier:** source is Tamashiro, Levin & Barbosa 1998, "traditionally
  referred to as the Donnan potential". The word isn't in Barr 2012, which the Comment cites.
- **Not Bethe:** Φ_B is a cell property; Donnan is "inherently an interfacial effect". Levin's total model drop is ϕ_B + φ_D; pH_S − pH_R uses φ_D alone.
- **Measurable?** E_D is; whether it equals ΔΦ isn't settled by these sources. See theory.md.
- **Finite concentration:** shifts relative to reservoir pH include a Donnan part, even when ΔΦ is never named.
