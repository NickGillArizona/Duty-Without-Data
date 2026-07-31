# AI Use in This Project

This page is the single, complete statement of how language models were used in *Duty
Without Data* and this archive. Every other page's disclosure summarizes this one.

**Summary disclosure.** Language models were used for document classification, code
development, analysis support, and editorial assistance. The author conceived and directs
the project, reviewed the case-level census, made all legal and interpretive judgments,
and is responsible for the manuscript and this repository. No model output is cited as
legal authority.

## Roles

| Role | What models did | What the author did | Where documented |
|---|---|---|---|
| Corpus assembly | Retrieval and screening of federal opinion and order records from the CourtListener API | Defined the queries, screens, and inclusion rules | [`method/METHODOLOGY.md`](method/METHODOLOGY.md) |
| Classification | Multi-model classification of screened records under frozen prompts (the primary three-model ensemble: Kimi K2.6, GLM-5.1, DeepSeek V3.2), with prespecified adjudication rules | Ratified the coding rules; adjudicated the case-level outcome census case by case with final inclusion and finality determinations | [`method/VALIDATION.md`](method/VALIDATION.md); [`article/appendices/Appendix_K_Classification_Prompts.md`](article/appendices/Appendix_K_Classification_Prompts.md) |
| Validation | Independent re-reads by separately run models from different providers, including a blind full-universe fourth-coder re-read; programmatic quotation checks | Specified the validation design; reviewed disagreements and adverse findings | [`method/VALIDATION.md`](method/VALIDATION.md); [`article/appendices/Appendix_A4_Reproducibility_Audit.md`](article/appendices/Appendix_A4_Reproducibility_Audit.md) |
| Software | Drafting and revision of the analysis and verification scripts | Specified, reviewed, and ran the pipeline; the release gate re-derives published numbers | [`scripts/`](scripts/); [`replication/REPRODUCE.md`](replication/REPRODUCE.md) |
| Research support | Drafting of working research memoranda (retained privately, not published here) | Directed the research; nothing the Note prints relies on an unverified memorandum | [`replication/DATA_PROVENANCE.md`](replication/DATA_PROVENANCE.md) |
| Editorial | Editorial assistance on the manuscript and this archive's pages | Reviewed and approved all text; made every editorial decision of record | this page |

## Limitations that travel with every model-derived figure

- **Reproducibility, not accuracy.** The validation layers are machine re-reads: they
  measure whether independent pipelines reproduce the coding, not accuracy against a
  human-coded benchmark. This project includes no corpus-scale human-coded benchmark.
- **Cross-model agreement is not ground truth.** Separately run models can share errors;
  agreement statistics are reported numerically without qualitative labels, and the
  ensemble is not asserted to be more accurate than any single model.
- **Models are instruments, not authorities.** Model output is treated as a locator until
  verified; quotations and pincites printed in the Note were verified against archived
  originals, and no model output is cited as legal authority.
- **The case-level outcome census is the series of record.** It was adjudicated case by
  case under prespecified rules with the author's final inclusion and finality
  determinations; machine-only layers are labeled as such wherever they appear.
