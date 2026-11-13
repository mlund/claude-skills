# Interview

Ask only what the files don't answer, one topic per question, and offer the values you found as
options so the user confirms rather than types. Record each answer where listed.

| Topic | Ask | Goes to |
|---|---|---|
| Publication | Title, journal, DOI (or "in review"), preprint DOI | `.zenodo.json` `related_identifiers` (`isSupplementTo`, `publication-article`), `CITATION.cff` `preferred-citation`, README |
| Deposit title and description | Short title; one paragraph on what the deposit reproduces | `.zenodo.json` `title`, `description`; `CITATION.cff` `title`; README heading; `pyproject.toml` `description` |
| Keywords | 3–6 terms | `.zenodo.json` `keywords`, `CITATION.cff` `keywords` |
| Creators | Full names in author order, ORCIDs, affiliations | `.zenodo.json` `creators` ("Family, Given"), `CITATION.cff` `authors` (ORCID as URL) |
| Contributors | People who helped but aren't authors, and their role (e.g. `DataCurator`, `Researcher`) | `.zenodo.json` `contributors` |
| Funding | Funder and grant number | `.zenodo.json` `grants` (`{"id": "<funder DOI>::<grant>"}`); ask the user to confirm the funder exists in Zenodo |
| License | Code license and data/text license, if different | `LICENSE`, `LICENSE-DATA`, `pyproject.toml` `license`, `.zenodo.json` `license`, `CITATION.cff` `license`, README badge |
| Access | Open, embargoed (until when), restricted | `.zenodo.json` `access_right`, `embargo_date` |
| Upload type | `workflow` for notebooks + code; `dataset` when data dominates; `software` for a tool | `.zenodo.json` `upload_type` |
| Community | Zenodo community to submit to, if any | `.zenodo.json` `communities` |
| Structure (adapt) | Confirm the source → destination mapping table; what to leave out | the new repository |
| Large files | Which raw outputs readers need; acceptable deposit size | see `large-files.md` |
| Documentation | What a reader must run to get each figure or table; data origin, formats, units | README, `data/raw/` description |
| Repository | GitHub owner/name, and whether it may be made public | README links, `.zenodo.json` |
| Python | Minimum Python version, if the code needs an old one | `pyproject.toml` `requires-python`, `.python-version` |

Never invent ORCIDs, DOIs, grant numbers or affiliations; leave a visible placeholder and list it.
