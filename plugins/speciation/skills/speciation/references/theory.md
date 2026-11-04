# Theory

## What the sources support

- **IUPAC (Gold Book, Buck 2002):** pH = −lg a(H⁺) on the molality scale, "only… a
  notional definition". Activity a = exp[(μ − μ°)/RT], with μ° set by the standard state.
  Combining them gives pH = (μ° − μ)/(RT ln 10). These entries don't address membranes; the Gold Book's
  μ would need the electrical convention below. The I ≤ 0.1 mol/kg condition is for the Bates–Guggenheim
  standardization, not a limit on the word pH.
- **Decomposition (Alberty 2001, IUPAC Technical Report, §3.2a, §3.2d):** "the activity a_i of an ion is
  defined in terms of its chemical potential μ_i and the electric potential φ_i": μ̃_i = μ_i° + RT ln a_i
  + z_iFφ_i, with μ_i° for a phase at zero potential. So here activity *excludes* the electrical term, which
  supports a_i and pH_sys ≠ pH_res over an activity containing φ_D. This defines activity given φ; it doesn't
  make φ measurable (Guggenheim 1930). μ_i in §3.2a–c means μ̃_i: "check which convention is being followed".
  The electric effect "cancels" in reaction constants across phases (§3.2a).
- **IUPAC on Donnan (Gold Book, PAC 1972, 31, 577):** *Donnan equilibrium* is "an unequal
  distribution of diffusible ions"; the membrane "may be replaced by other kinds of restraint,
  such as gelation, the field of gravity". *Donnan emf* E_D is the zero-current potential
  difference between two identical salt bridges in the two solutions. "Donnan potential" is
  listed as its synonym, so in IUPAC's usage the term names a measured quantity. E_D includes
  bridge junctions, so it equals the model ΔΦ only with further assumptions (our reading).
- **Guggenheim 1929:** Π a_i^λ is physically defined when Σλ_i z_i = 0; splitting μ̃ has
  meaning only in the same medium (p. 845).
- **Guggenheim 1930:** *modifies* this. A conventional potential difference is defined from
  the charge distribution, while "no measurements of E.M.F." can reveal it. The quote
  "quite arbitrary… without physical significance" summarizes what the paper then revises.
- **Bates & Popovych 1981:** pH is operational. In "suspensions, gels, tissues", "fundamental
  interpretations in terms of hydrogen ion are impossible and often unnecessary".
- **Rockwood 2015:** claims a measurable type II single-ion activity via gas-phase fugacity.
  A proposal, contrary to IUPAC's notes. Undefined in a primitive model, so our a_i is type I.
- **Fraenkel 2012:** single-ion activity remains disputed. Simulated values are model
  quantities; compare a_± or allowed combinations.
- **IUPAC on suspensions (Oman et al. 2007, Recommendations 2006; soil suspensions):** the
  suspension effect is operational, the potential difference between cells with both electrodes
  in sediment or suspension and both in the separated equilibrium solution (eqs). It is the sum
  of an indicator-electrode mixed potential (SE1) and an anomalous junction potential (SE2).
  "No measurable boundary potential", "therefore… no boundary (or Donnan) contribution". The eqs
  gives "the best-defined" E_cell and pH. This concerns measured potentials, not whether ions
  partition. E_D (Gold Book) is a different measurement, between two solutions; don't conflate them.
- **Oman et al. 2007, Part A (IUPAC Technical Report; ion-exchanger models):** "μ̃_H+ is the same
  throughout the whole equilibrated suspension", so "the pH of the eqs can be considered to be the
  true pH value of the whole interstitial solution". A Donnan potential "exists at the solid–solution
  interface around individual particles", not at the sediment/eqs boundary. Particles with their
  double layers may hold different H⁺, so "a suspension contains at least two phases of either
  similar or different activity of H⁺".
- **Interstitial vs cell-averaged (our reading):** pH_sys is a cell-level model label. It isn't the
  interstitial pH, which equals the eqs value where double layers don't overlap. A uniform gel with
  overlapping layers has no such interstitial region. State which is meant.
- **Simulation vs experiment:** ΔΦ is well defined in a model. Experiment gives E_D, not ΔΦ (Guggenheim 1930 denies that EMF reveals the potential difference).
  Measured pH must state both electrode positions. B&L 2023 and 2024 equate both electrodes in
  one phase with that phase's pH; for suspensions, IUPAC 2006 says such a reading carries SE1 and
  SE2. Compare pH_res with the eqs value; don't claim a measured pH_sys (our mapping).
- **Bethe potential Φ_B (Levin & Bakhshandeh 2023; B&L 2024):** the "crystal" is the lattice of replicated
  cells. ϕ_B = −(2π/3εV) Σq_ir_i² + πQ_t/(6εL), and the model drop to the reservoir is ϕ_B + φ_D. It cancels in
  pair moves. It is absent from the Comment, Reply, Landsgesell 2020 and Beyer 2025.
- **Φ_B in a fluid (our derivation):** the first term needs no lattice. For a neutral sphere it is ⟨φ⟩ − φ(edge), the
  whole-cell mean including the macroion's interior. So it's a simulation reference question, not a physical drop.
  Ewald without k = 0 zeroes that mean, so a single-ion Ewald energy needs Φ_B to refer to outside the cell, as
  B&L's surface Widom does. Plain Widom inside the system: check this (our inference, untested).
- **Size (our shell estimate, not simulated; Table 1 colloid, η = 29.6%, 400 net charges, 4–16 Å shell):** whole-cell
  Φ_B 0.24–1.04 pH units; ion-accessible mean 0.03–0.36; ideal Donnan 0.19.

## pH_in

Acceptance, for deprotonation:

- DAP: min[1, (N_Cl/c°V) · K_a/(a_H a_Cl) · N_HA/(N_A+1) · e^(−βΔU)]
- ACP: min[1, (c°V/(N_Na+1)) · K_a a_Na/a_H · N_HA/(N_A+1) · e^(−βΔU)]
- Salt: a_Na a_Cl (c°V)²/((N_Na+1)(N_Cl+1)) · e^(−βΔU)

These use only Guggenheim's allowed combinations, so a_i → a_i exp(−z_i βeΔΦ) changes nothing.
So pH_in can be read as pH_res with reservoir counterion activity. Reading it as pH_sys also needs a
consistent activity convention and an independently established system activity.

Uncorrected cpH has neither reading. **Status:** our derivation. Identical Faunus trajectories under relabelling show algebraic invariance
only; they don't identify an input as physical system pH. Cancellation means paired moves need no
explicit potential term, not that partitioning disappears.

Published positions, by method:
- Ordinary cpH: Landsgesell 2020 say it "uses the pH in the system" and can't simulate reservoir
  equilibrium. Bakhshandeh & Levin 2024 say "the controlled pH is that of the reservoir".
- G-RxMC (Landsgesell 2020): controls the reservoir and distinguishes pH_sys from pH_res.
- Uncorrected cpH drops the counterion term, and adding ion exchange to it misses the Donnan contribution
  (Landsgesell 2020). Beyer et al. 2025 correct its results afterwards by a pH shift; "reservoir" and "Donnan" don't occur there, so this doesn't settle which pH the input is.

## Relations

- pH_sys = pH_res + βeΔΦ/ln 10. Neutral combinations are equal across phases.
- Route to pH_sys from pair moves (untested): pH_sys = pH_res + lg(a_Cl,sys/a_Cl,res).
- Ideal, macroscopic limit: N_+N_- = N_res², N_+ − N_- = Z, βeΔΦ = ln(N_-/N_res). Exactly, at finite N,
  only ⟨N_+N_-⟩ = λ² holds; means differ (⟨N⟩ = 0.698, not 1, at Z = 0, λ = 1).
