# Third-Party Notices

Inventory of materials in this repository that the author did not create. Nothing in
[`LICENSE`](LICENSE) or [`LICENSE-DATA`](LICENSE-DATA) relicenses these; they remain under the
terms of their sources. See [`LICENSING.md`](LICENSING.md) for the overall map and
[`replication/DATA_PROVENANCE.md`](replication/DATA_PROVENANCE.md) for retrieval dates and URLs.

| Material | Where | Source | Terms |
|---|---|---|---|
| Federal court opinions used for validation and comparator work (853 texts) | Not distributed; on file with the author | CourtListener REST API v4 (Free Law Project) | Court opinions are public records. Per-file provenance and normalized hashes are preserved in `opinion_sources.csv`. |
| Federal Register notices (60-day/30-day PRA notices and related) | `record/hud-27061/` | Federal Register / GPO | U.S. government works, 17 U.S.C. § 105 (public domain). |
| OMB/OIRA supporting statements and ICR landing pages | `record/hud-27061/` | reginfo.gov | U.S. government works (public domain). |
| Public docket comments (SAGE/Jones Day; Williams Institute) | `record/hud-27061/comment_*.pdf` (with `.txt` extractions where generated; the two byte-identical Williams postings share one extraction) | regulations.gov Docket HUD-2006-0214 | Public administrative-record filings reproduced as posted; any copyright remains with their authors. |
| The author's posted PRA comment (redacted attachment + API record) | `article/appendices/admin_record_c/pra_comment_2026/` | regulations.gov (Comment HUD-2006-0214-0011) | Author-written text; the committed copies are the government's public redacted postings. |
| HUD datasets (LIHTCPUB release zip; CDBG accomplishment/expenditure workbooks; POSH/REAC extracts) | `data/` | HUD / huduser.gov / HUD Exchange | U.S. government data (public domain); cite HUD as source. |
| Census ACS PUMS extracts and derived cross-tabulations' inputs | `data/`, via `scripts/census_pums_replication.py` | U.S. Census Bureau public API | U.S. government data (public domain). |
| Disability-Forward QAP Advocacy Guide | `data/Disability-Forward-QAP-Advocacy-Guide.pdf`/`.txt` | Its publisher (retrieved from the publisher's public website; see `DATA_PROVENANCE.md`) | Third-party publication; rights remain with its publisher. Included as source material for the QAP analysis; contact the publisher for reuse beyond this archive. |
| GAO / HUD OIG reports (quoted excerpts) | quoted in memoranda and appendices | gao.gov / hudoig.gov | U.S. government works (public domain). |
| State QAP documents | NOT committed (scan cache is untracked) | State housing finance agencies | Per-jurisdiction URLs and retrieval dates in `results/qap_jurisdiction_ledger.csv`. |
| Subscription-database-derived fields | factual fields only (case name, date, citation) in the database | subscription legal databases | Factual, non-copyrightable fields only; opinion text from those sources is NOT redistributed (see `DATA_PROVENANCE.md` § 2.5). |

## Service and data attributions

**CourtListener / Free Law Project.** Court opinion text was obtained via the
[CourtListener REST API v4](https://www.courtlistener.com/api/rest/v4/), provided by the
[Free Law Project](https://free.law), a 501(c)(3) nonprofit. If you use data derived from
CourtListener, please attribute the Free Law Project accordingly.

**U.S. Census Bureau.** Housing cost-burden and disability analyses use data from the
U.S. Census Bureau,
[American Community Survey 2020-2024 5-Year Public Use Microdata Sample](https://api.census.gov/data/2024/acs/acs5/pums).
"This product uses the Census Bureau Data API but is not endorsed or certified by the
Census Bureau."

**OpenRouter.** Multi-model LLM access for the classification pipeline was provided
through the [OpenRouter API](https://openrouter.ai/). Individual model attributions
(MiniMax M2.7, DeepSeek V3.2, Kimi K2.5, Claude Haiku 4.5, Claude Sonnet 4.6, Claude
Opus 4.6) are documented in
[`method/pipeline/model_configuration.md`](method/pipeline/model_configuration.md).

## Software dependencies

Open-source Python libraries, under permissive licenses:

| Package | License |
|---------|---------|
| pandas | BSD 3-Clause |
| numpy | BSD 3-Clause |
| scipy | BSD 3-Clause |
| statsmodels | BSD 3-Clause |
| requests | Apache 2.0 |
| httpx | BSD 3-Clause |
| openpyxl | MIT |
| python-dotenv | BSD 3-Clause |
