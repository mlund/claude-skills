# Terminology review checklist

For reviewing prose. For numbers, algebra and code, use checks.md §17. Report in this order, and
apply only the items the request and text call for.

**Scientific errors**

1. Scale: each reported or compared Γ has its scale stated. A molar count ⟨N3(D)⟩ − ρ3Vol[D] is
   not called molal Γ23 (gamma-linkage.md §7).
2. Ensemble: held-constant variables are stated. Dialysis Γ23 in a constant-(T, P) linkage is
   valid; check stoichiometry for association (gamma-linkage.md §5).
3. Sign: accumulated and excluded follow the sign of Γ23 alone. Γ23 > 0 is not called "bound" in
   the text's own voice, and "excluded" is not read as no local enrichment.
4. Mislabelled quantity: "finite-volume KBI" for a solute-anchored domain (estimators.md §12);
   Timasheff's preferential interaction parameter for Γ23; K_p for anything but Record's ratio.
5. Partitions: the rule is named and exclusive, and the sum carries the right scale. Earlier work
   is credited, for example Baynes & Trout 2003 for radius-weighted domains and exact group sums
   (estimators.md §13).
6. Salts: single-ion and salt-component quantities are kept apart, the charge term is present, and
   only neutral combinations are treated as derivatives (salts.md §10).
7. Translation: other schools' index order and species are mapped correctly, for example
   "Γ_XP (Γ23 here)" and indistinguishable ions into Γ±.
8. Sources: each nontrivial relation is cited at the claim, and inference is not presented as a
   source statement.
9. Dimensions: every equation balances, and units match the constant used (checks.md §16).

**Ambiguity**

10. "Preferential solvation" or "hydration" used as a sign word; it has opposite meanings across
    schools. Ask for or state the meaning.
11. A symbol reused for two quantities, such as Γ for a thermodynamic-factor matrix, or δ for both
    thickness and a Kronecker delta.

**Optional house preferences** (label as optional; never override the document's notation)

12. ρ for number density rather than c; δ_ij with two indices; Scatchard numbering.
13. "Cosolute" rather than "ligand" or "cosolvent"; "preferential interaction coefficient" as the
    name of Γ23.
14. m-values in kJ mol⁻¹ M⁻¹, with units always stated (gamma-linkage.md §11).
