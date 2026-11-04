# The Levin–Košovan exchange

Levin & Bakhshandeh (Comment) and Košovan et al. (Reply), Soft Matter 2023, on
Landsgesell et al. 2019.

| # | Question | Levin side | Košovan/Holm side | Status |
|---|---|---|---|---|
| 1 | Is pH − pK_a universal? | No | Agree; the claim had a proviso | Largely talking past each other |
| 2 | Is explicit-ion cpH biased? | Yes, "complete failure" (2024) | Yes; correct by a pH shift (2025) | Bias agreed; severity and remedy differ |
| 3 | Is pH equal in system and reservoir? | 2022 JCP (quoted in the Reply) and 2023 JCP: same. 2024 adopts pH_S ≠ pH_R "since this is the usual convention". Not stated in the Comment | No (2020 Eq. 6) | Converged in practice; principled objection kept |
| 4 | Is cpH input reservoir or system pH? | "The controlled pH is that of the reservoir" | "Uses the pH in the system"; "cannot be used to simulate a system in equilibrium with a reservoir" | Open. For paired moves the algebra is shared (our reading), but the Reply also disputes whether the competing algorithm handles system–reservoir pH differences |

**Checks that cut both ways**
- Alberty 2001 (IUPAC Technical Report) defines ion activity with the electrical term separated. This favours
  the convention behind pH_sys ≠ pH_res, against activity containing φ_D. Levin's Gibbs–Guggenheim objection is
  about measurability and meaning, which this doesn't settle.
- Oman et al. 2007, Part A: equal μ̃_H+ gives eqs pH as "the true pH value of the whole interstitial
  solution" (close to Levin's statement), with "at least two phases" of possibly different H⁺ activity
  (close to the Reply's). Neither side cites it, as far as we've read.
- The Comment keeps "all other conditions" but drops the K-sweeping context.
- "Intrinsically grand-canonical" is the Comment's own phrase, not L&J's. Ullner &
  Woodward 2000 called grand canonical "the natural ensemble", without discussing Donnan.
- The Reply says two-phase systems weren't addressed, but Review §3.3.1 and §2.3.1 touch them.
- Levin & Bakhshandeh 2023 (JCP) call theirs "our definition of pH", which concedes it
  is a choice.
- Blanco et al. 2023 (a Reply co-author) uses "reservoir at a fixed proton chemical
  potential" for cpH, and also "single-phase".
- Table 1's canonical-vs-GCpH agreement is nearly fixed by charge balance (tests.md, N4).
  This is our observation. The cpH-vs-GCpH gap is what needs an independent test: our runs give a smaller
  gap and don't reproduce the cpH column (tests.md, Reference data).
- The Reply says the Comment's pH ≈ pCl "is valid only in salt-free solutions". The Comment introduces it just
  after mentioning salt moves, without restating a salt-free condition, so its intended scope is unclear.

Present the shared mathematics and the remaining disagreement separately. Some of the heat comes
from different meanings of "pH", but the Reply's criticism is also algorithmic and physical (§§2–3).

## Citation and history notes

- **IUPAC on pH:** "pH is the chemical potential of H⁺" (Reply §3) isn't IUPAC's wording. pH is defined through
  activity. Alberty 2001 separates the electrical term. The Gold Book pH entry's Note 3 has apparent slips (E°
  for E; lg a without a sign), so cite Buck 2002 §4 for the Harned procedure.
- **Guggenheim:** "Quite arbitrary… without physical significance" (1930, p. 1540) summarizes the principle
  that paper then revises. Cite the modification.
- **Reed & Reed 1992:** "reservoir", "Donnan" and "grand" don't appear; explicit counterions are future work.
- **Rockwood 2015:** a proposed method that contradicts IUPAC's notes; not settled.
- **Preprint wording:** the Comment's arXiv version says "not explicitly depend on pH"; the published text says
  "not depend on pH", which is what the Reply attacks.
- **Two 2023 Levin & Bakhshandeh papers:** say which, Comment or JCP.
- **Barr citations differ:** Comment (PRE 86, 016703), Reply (JCP 137, 144704).
