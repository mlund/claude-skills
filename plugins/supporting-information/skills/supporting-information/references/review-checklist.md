# Review checklist

Run what can be run; note what couldn't be checked and why.

## Findable
- `.zenodo.json` present with title, description, creators with ORCIDs, keywords.
- Title consistent across `.zenodo.json`, `CITATION.cff`, README, `pyproject.toml`.
- Related publication DOI in `related_identifiers` (`isSupplementTo`) and `CITATION.cff`.
- After release: README carries the Zenodo concept-DOI badge (all versions).

## Accessible
- Repository public (required by Zenodo's GitHub integration); `access_right` set.
- Large data either in the deposit or with a stated, persistent location; nothing needed lives only
  on a lab disk or personal cloud.

## Interoperable
- Open, documented formats (CSV, JSON, HDF5, PDB, NetCDF) rather than proprietary or pickles.
- Units and column meanings stated; file naming consistent.

## Reusable
- License present and appropriate: software license for code, CC-BY or similar for data/text.
  CC-BY alone on code is a finding. License consistent in `LICENSE*`, `pyproject.toml`,
  `.zenodo.json`, `CITATION.cff`, README.
- README says how to install and what to run, in order, for each figure or table.
- Provenance: every processed file and figure is produced by code in the repository.

## Zenodo
Validate against the legacy deposit schema used by the GitHub integration:

    uvx check-jsonschema --schemafile https://raw.githubusercontent.com/zenodo/zenodo/master/zenodo/modules/deposit/jsonschemas/deposits/records/legacyrecord.json .zenodo.json

- Creator names as "Family, Given"; contributor `type` from Zenodo's list.
- No repository URL duplicated in `related_identifiers` (the integration adds it).
- `CITATION.cff` agrees with `.zenodo.json` (Zenodo ignores it when both exist).
- Deposit size sensible; large raw files handled as in `large-files.md`.

## Reproducibility
- `pyproject.toml` + committed `uv.lock` + `.python-version`; `uv lock --check` passes.
  `environment.yml`, unpinned `requirements.txt` or no dependency list are findings.
- `uv sync` then each notebook runs, in order, from a clean checkout; no absolute or home paths.
- Random seeds set where results depend on them.
- CI runs `uv sync --locked`, ruff check, ruff format check, pytest, and the schema check; actions
  pinned to versions, not `@main`.

## Code
- Ruff policy as in the template: `PTH`, `PLW1514`, `D` (numpy), notebooks included.
- Apply the codebase-design and tdd skills (URLs in SKILL.md): duplicated logic, shallow modules,
  logic living in notebooks, untested numerics, magic constants without units or source.
- Comments explain why; standard library preferred; dependencies justified.
