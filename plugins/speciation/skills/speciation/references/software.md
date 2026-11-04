# Faunus and ESPResSo

Read at Faunus `bbf28e7` (3.0.0-beta.3) and ESPResSo `0636424a2`. Check syntax against the
installed version. General input: `faunus-input`, `faunus-run` skills.

## Faunus

No pH key: pH_in = −lg `activity` of the implicit proton.

```yaml
atoms:
  - {name: H+, activity: 7.94e-6}   # pH_in = 5.1
molecules:
  - {name: colloid, degrees_of_freedom: RigidAlchemical, keep_excluded_coulomb: true, atoms: [...]}
  - {name: Na+, atoms: [Na], atomic: true, activity: 0.0788}  # molar, salt reservoir
  - {name: Cl-, atoms: [Cl], atomic: true, activity: 0.0788}
```
```yaml
reactions:
  - ["⚛HA + Cl- = ⚛A + ~H+", !pK 5.4]     # GCT, DAP
  - ["⚛HA = Na+ + ⚛A + ~H+", !pK 5.4]     # GCT, ACP
  - ["= Na+ + Cl-", !dG 0.0]              # salt exchange, K=1
```

- ln K_eff = ln K + Σ ln a(implicit reactants) − Σ ln a(implicit products) − Σ ln a(molecular
  reactants) + Σ ln a(molecular products), with count factors (`src/montecarlo/speciation.rs`).
- `⚛HA = ⚛A + ~H+` alone is implicit-ion cpH. It changes net charge when Coulomb is on.
- Uncorrected cpH has no direct form, since insertions always carry an N/(c°V) factor.
- Closed RxMC: use an explicit hydronium molecule with no `activity`.
- `!ScaledWidomInsertion` gives single-ion μ^ex. Route to pH_sys (untested):
  pH_sys = pH_res + lg(a_Cl,sys/a_Cl,res). Check its convention against Φ_B first.
- Not reported: ΔΦ.

### Faunus traps

- **`Rigid` titrating molecules drop site–site Coulomb.** All 600 sites ionized at pH 5.1
  instead of about 125. `keep_excluded_coulomb: true` is what restores it (`RigidAlchemical`
  alone doesn't); the log says `Added excluded-pair Coulomb correction`. Energy drift still
  passes, nothing warns, and trials get slower.
- **Random insertion overlapping a hard core** gives infinite energy, so every move fails and
  drift is NaN. Start with `active: 0`, or place ions.
- **Missing `activity` on an inserted molecule means 1 M**, silently. On an atom entry it is
  ignored for molecular participants.
- **Activity isn't concentration:** a = 0.1 gives about 129 mM here. a ≈ 0.0788 gives 100 mM (CS+MSA, 4 Å ions).
- **Non-neutral start or reaction:** net charge is only logged, and persists.
- **`reservoir: true` is a finite counter-phase** (solubility; see `rxmc.md`), not the literature's infinite reservoir, which is `activity`.
- **`count` on `atomtype X` in a molecular group counts molecules.** Use charge balance.
- **Pool exhaustion rejects silently.** Allocate well above expected counts.
- **Periodic cells:** `!Cuboid` plus `- !Ewald {cutoff, accuracy}`, with no Coulomb in the
  nonbonded list.

## ESPResSo

Reaction methods moved from C++ to Python in #4765; read
`src/python/espressomd/reaction_methods.py`.

- `ConstantpHEnsemble`: ln P = ln[N_HA/(N_A+1)] − βΔE + ν̄ ln10 (pH + ν̄ lg γ). One reactant,
  two products; the counterion gets no term. Uncorrected cpH, ACP form.
- `ReactionEnsemble`: ln P = ln(factorials) − βΔE + ν̄ ln V + ln Γ. Convert Γ to σ units.
- Multi-product insertion: Γ "defines only the sum of their chemical potentials", the same
  invariance as GCT.
- GCT through `ReactionEnsemble` (our derivation; agrees with Faunus GCT within about 1% on Comment Table 1): HA + Cl ⇌ A with
  Γ = K_a/(a_H a_Cl), or HA ⇌ A + Na with Γ = K_a a_Na/a_H, in σ units.
- `check_for_electroneutrality` is on by default.
- Doc example `gamma=1/(10**-14/K_diss)` looks inverted if K_diss is K_b; convention unclear.

### ESPResSo traps

- **`gamma` differs by class:** K in `ConstantpHEnsemble`, Γ in simulation units in `ReactionEnsemble`.
- **Docs say cpH is "coupled to an infinite reservoir";** Landsgesell 2020 says system pH.
- **Bug at `0636424a2`:** a rejected displacement after `reaction()` raises `KeyError: 'type'` in
  `_restore_system`. Workaround: set `method._particle_numbers = {}` before displacing.
- **Displacement on an unknown type raises `KeyError`:** use a method whose reactions contain it.
- **MC-only hard spheres:** `exclusion_radius_per_type` sums by Lorentz–Berthelot, so a core of
  radius a and ions of radius r exclude at a + r. No integrator is needed.
