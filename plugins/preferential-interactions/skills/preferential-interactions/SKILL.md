---
name: preferential-interactions
description: >-
  Review, write, and explain scientific text on preferential interaction
  coefficients (Γ23), Kirkwood–Buff (KB) integrals, preferential binding,
  exclusion and hydration, cosolute and salt effects on macromolecules, and
  their site- or residue-resolved decompositions from simulations. Use whenever
  a draft, manuscript, referee report, or explanation touches KB theory,
  Wyman linkage, local–bulk domain models, osmolytes/denaturants/salts around
  proteins or small solutes, or Voronoi/radical partitions of solvation excess —
  even if the user only asks to "check the wording", "fix notation", or
  "explain Γ". Supplies a sourced glossary with DOIs, a house style, and
  conflict notes between the Smith, Shimizu, Record, Trout, Ben-Naim and
  finite-volume KB schools.
---

# Preferential interactions: terminology and conventions

The literature on preferential interactions spans several schools that use the
same words for different things and different words for the same thing. The
same symbol Γ, the word "preferential solvation", or the phrase "finite-volume
KB integral" can mean opposite or unrelated quantities depending on the paper.
A reader who meets an inconsistency stops trusting the derivation. This skill
keeps text consistent with one house style, while knowing every school's usage
so that cited work is described in its own terms and translated correctly.

Pair it with a prose skill (e.g. scientific-writing) for sentence-level style;
this skill owns terms, symbols, ensembles, signs and citations.

## Modes

- **Review**: read the text, then report each terminology, notation, sign,
  ensemble or scale problem as *location — problem — fix — source (DOI)*. Rank
  substantive errors (wrong ensemble, wrong sign, wrong scale, a quantity
  mislabelled as another) above style deviations. When the text cites a paper
  that uses another convention, check that the translation is right rather than
  forcing house style onto the quotation.
- **Write**: draft or revise using the house style below. Define each symbol
  at first use, cite the source of each nontrivial relation at the claim, and
  state the ensemble and concentration scale whenever a Γ value appears.
  When the text goes into an existing document, follow that document's
  notation so the insert reads as one piece, and list each place where it
  departs from house style (e.g. c for density, "ligand" for cosolute) with
  the suggested replacement. A silent mix of two notations is worse than
  either one.
- **Explain**: explain a concept or derivation in house notation, mapping other
  schools' notation onto it, with DOIs for every relation used.

## Reference files

- `references/glossary.md` — every term and symbol, its definition, the house
  choice, variants by school, and DOIs. Read it for any term not covered below.
- `references/equations.md` — the core relations with equation numbers and
  DOIs (KB definitions, Γ23 forms, scale and ensemble conversions, salts,
  estimators). Read it before writing or checking an equation.
- `references/simulation.md` — practical route from MD/MC to KBIs and Γ23:
  finite-size corrections, solute-centred estimators, implicit solvent,
  salts, tools (KBKit and others) and a reporting checklist. Read it for any
  Methods text or analysis that extracts KBIs or Γ from simulation.
- `references/references.bib` — verified BibTeX for the cited works.

Never invent a citation or DOI. If a relation is not in the reference files,
say it needs a source.

## House style

### Components and roles

- Scatchard numbering: **1 = water (solvent), 2 = solute, 3 = cosolute**.
  "Solute" is the macromolecule or small molecule whose environment is studied
  (protein, caffeine); "cosolute" is the added species (osmolyte, denaturant,
  salt ions). Avoid "cosolvent" for salts and "biomolecule" for small solutes;
  keep other papers' words only inside quotations.
- In implicit-solvent (McMillan–Mayer) work, component 1 is absent as
  particles; say so when it matters.

### The coefficient

- Name: **preferential interaction coefficient**, symbol **Γ23**
  (solute index first), defined as (∂m3/∂m2)_{T,μ1,μ3}, the
  equilibrium-dialysis coefficient. Not "preferential binding coefficient",
  not "preferential interaction parameter": the latter is Timasheff's
  (∂μ2/∂m3), a different derivative.
- At infinite dilution of the solute, **Γ23 = ρ3(G23 − G21)**.
- Ions: Γ+ and Γ− (single-ion coefficients). Use the bare Γ only after Γ23 is
  defined and the meaning is unambiguous.
- Always state the **ensemble** (which variables are held constant) and the
  **concentration scale** when reporting or comparing Γ:
  - molal Γ23 = ρ3(G23 − G21): the explicit-solvent counted-solvent estimator
    converges here;
  - molar-scale coefficient **ρ3G23** (call it molar, never just "Γ"): the
    implicit-solvent estimator ⟨N⟩ − ρ3·Vol[D] converges here; it still
    contains the solute's excluded volume. Give the conversion when both
    appear (see equations.md).
- Pairing the dialysis Γ23 with a constant-(T, P) Wyman linkage is standard
  and exact; do not "correct" it. The offset to the (T, P, μ3) coefficient,
  φ3/(a33 φ1), is the same for every solute, so it cancels in ΔΓ23 only for
  1:1 processes (folding, conformational change). For association
  (A + B ⇌ AB) it does not cancel; say so when it matters.

### Sign words

- Γ23 > 0: the cosolute is **accumulated**; Γ23 < 0: it is **excluded**.
  Define these by the sign of Γ23 alone.
- Never say "bound" for Γ23 > 0. Reserve "bound" for a cutoff occupancy count,
  and say that it is one.
- Avoid "preferential solvation/hydration" as a sign word: it means water
  enrichment in some papers and cosolute excess in others.
- Remember that "excluded" can coexist with an increased local cosolute
  density (excluded volume dominates); say so when it could mislead.

### KB quantities

- Kirkwood–Buff integral (KBI) **G_ij** = ∫[g_ij(r) − 1] dr in the open
  (grand-canonical) system, infinite range.
- **Excess coordination number N_ij = ρ_j G_ij**, j counted around i.
- Number densities **ρ_i**; molality m_i; molarity C_i. Do not use c for
  number density.
- **Running KBI**: an integral truncated at finite R (radial). The quantity
  over a solute-shaped domain is a **solute-anchored running KBI**. It is *not*
  a finite-volume KBI: that term means the fluctuation integral G^V of an open
  subvolume (Schnell, Krüger, Simon), whose 1/L surface law does not apply to a
  solute-anchored domain. Convergence is judged by a plateau in δ.
- Kronecker delta always with two indices, **δ_ij**. When quoting Ben-Naim's
  preferential-solvation index δ_{A,S}, rename it (e.g. Δ^PS_{A,S}) and note
  the renaming once. Plain Δ_AB is taken: Ben-Naim (1977) uses it for
  G_AA + G_BB − 2G_AB.

### Domains and partitions

- **Integration domain D(δ)**: the union of spheres of radius R_i + r_3 + δ
  around solute atoms, where r_3 is the cosolute exclusion radius; **δ** is its thickness beyond the cosolute-accessible
  surface. Present D(δ) as a region of integration whose estimate converges,
  not as a physical bound layer ("local domain" carries Record's two-domain
  assumptions; use it only when describing that model).
- **Radical (power) tessellation**: each solute atom owns the points with the
  smallest power distance |r − r_i|² − (R_i + r_3 + δ)². Site excess
  γ_i = ⟨N_i⟩ − ρ3 v_i, with Σγ_i = Γ exactly.
- Distinguish other partition rules by name: **ordinary Voronoi**
  (closest atom; equal radii; Martínez & Shimizu, ComplexMixtures),
  **additively weighted Voronoi** (nearest van der Waals surface,
  |r − r_i| − R_i; Baynes & Trout 2003), and **Voronoi solvation shells**
  (molecular cells ordered by neighbour shell; Schröder group). Power and
  additive weighting both reduce to ordinary Voronoi at equal radii; power
  ownership moves with δ, additive ownership does not.
- **K_p**: the local-to-bulk partition coefficient in Record's sense
  (local/bulk cosolute-to-water ratio); do not reuse the symbol for other
  local enrichment measures.

### Salts

- Report single-ion coefficients Γ+ and Γ− (these decompose by site) and use
  their sum in the linkage, ∂ln K_obs/∂ln a± = Δ(Γ+ + Γ−) (Record & Anderson
  1995, Eq. 42).
- State the electroneutrality term: with Z the signed solute charge,
  Γ+ − Γ− = −Z, so Γ+ − Γ− = +|Z| for a polyanion (Record & Anderson 1995,
  Eq. 29); and Γ+ + Γ− = |Z| + 2Γ_salt. Only the sum is a neutral-salt
  derivative.
- When citing Smith or Pierce, translate their **indistinguishable-ion**
  species (ρ3 = ν±ρ_salt, ν±Γ23 = N23 − (ρ3/ρ1)N21 − |Z|) into Γ±.

### Units and other schools' indices

- m-values: state units and the sign convention (Pierce et al. use M⁻¹ with
  β absorbed; Smith 2004 uses kJ mol⁻¹ M⁻¹). Prefer kJ mol⁻¹ M⁻¹ for reporting.
- Papers with letter labels (Γ_XP in Baynes & Trout; Γ3,2 in Record & Anderson)
  put the cosolute first. Map them to Γ23 when citing, e.g. "Γ_XP (Γ23 here)".

## Review checklist

1. Each Γ: ensemble stated? Scale (molal vs molar) stated? Name and index
   order per house style?
2. Sign words: accumulated/excluded, never "bound" for Γ > 0.
3. Symbols: ρ for densities, δ_ij with two indices, δ alone only for thickness,
   Γ not reused (e.g. for a thermodynamic-factor matrix) without comment.
4. "Finite-volume KBI" used for a solute-anchored quantity? Replace.
5. Partition rule named precisely; prior schemes attributed correctly
   (Baynes & Trout 2003 for radius-weighted domains and exact group sums).
6. Salts: single-ion vs salt-component quantities kept apart; |Z| term present.
7. Each nontrivial relation cited at the claim with a DOI from the bib.
8. Dimensions: every equation balances; KBIs carry units (nm³ or cm³ mol⁻¹);
   R with per-mole, k_B with per-molecule quantities; Γ23, γ_i, N_ij and ρ3G23
   are dimensionless (equations.md §16).
