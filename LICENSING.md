# Licensing Map

Plain-language guide to what license covers which files. Three classes:

## 1. Code — MIT ([`LICENSE`](LICENSE))

All project-authored source code and runnable instruments:

- `scripts/` (analysis, guards, generators)
- `method/pipeline/` (classification pipeline documentation; the as-run Java clients are retained in the project's private research records)
- `replication/queries/` (query specifications)
- `method/prompts/` (classification prompts and controlled vocabularies)
- `replication/comparator/` code (`comparator_analysis.py`, `regenerate_table1.py`,
  `recoding_2026-07-07/scripts/`, and the other `.py` files in the module)
- the registered-baseline analysis scripts in `scripts/` (`strengthening_analysis.py`,
  `compute_registered_baselines.py`, `recompute_verification.py`)
- `method/validation_three_model/`, `method/validation_kimi_k2_6/`, `method/validation_four_coder_full/` runner and
  computation scripts (`.py`)
- `action/` generator scripts (`.py`)

## 2. Project-authored data and documentation — CC BY 4.0 ([`LICENSE-DATA`](LICENSE-DATA))

- `article/appendices/` (project-authored appendix text)
- Root documentation (`README.md`, `METHODOLOGY.md`, `VALIDATION.md`, `REPRODUCE.md`,
  `DATA_PROVENANCE.md`, `data/dictionaries/*.md`, `SAMPLE_DEFINITIONS.md`, crosswalks, ledgers,
  `THE_ARGUMENT.md`, `EVIDENCE_AND_LIMITS.md`, `action/TAKE_ACTION.md`, and this file)
- The classification labels, screening results, and structured metadata in
  `data/FHA_Unified_Database.json` and the two source-corpus JSONs (the underlying docket facts
  are factual public records and are not claimed)
- Project-generated outputs: `results/` memoranda and tables, `replication/comparator/`
  non-code outputs, validation artifacts, `CLAIMS_LEDGER.csv`, `opinion_sources.csv`,
  `RELEASE_MANIFEST.json`
- `action/` templates (author-drafted; see the not-legal-advice disclaimer there)

The manuscript (`manuscript/`) is (c) Nicholas Gill and forthcoming in the Arizona Law
Review. The repository's code and data licenses do not apply to the manuscript or any
material governed by the journal's publication agreement.

## 3. Third-party and public-record materials — NOT relicensed

Neither license above covers materials the author did not create. They remain under their own
terms, inventoried in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md):

- Federal court opinion texts used for validation and comparator work are not distributed in this
  repository; they are on file with the author. Their provenance is recorded in
  `opinion_sources.csv`.
- `record/hud-27061/` primary-record files — Federal Register notices, OMB/OIRA supporting
  statements and landing pages, and public docket comments
- Government datasets in `data/` — HUD releases (LIHTCPUB, CDBG, POSH/REAC extracts) and Census
  ACS PUMS extracts
- `data/Disability-Forward-QAP-Advocacy-Guide.pdf` — third-party publication
- The PRA-comment module's regulations.gov materials (posted attachment and API record)

GitHub's automatic license detection reports `NOASSERTION` because `LICENSE` carries this scoping
preamble; that is expected. `CITATION.cff` expresses the combination as `MIT AND CC-BY-4.0`,
scoped as above.
