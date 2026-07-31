# Note-to-Repository Crosswalk

This document maps each section of the Note (*Duty Without Data: Disability Fair Housing and the Record-Dependent Right*) to the specific repository materials that support it. The goal is to let a law-review editor, peer reviewer, or future researcher locate the evidentiary basis for any passage without reading the entire archive.

For appendix-letter-to-file mappings, see [`APPENDIX_CROSSWALK.md`](APPENDIX_CROSSWALK.md). For per-claim provenance, see [`CLAIMS_LEDGER.csv`](CLAIMS_LEDGER.csv).

The section mapping below is keyed to the Note's four-Part structure
(Part I sections A–E; Part III sections A–E; Part IV sections A–D). Part I.E and Part IV
additionally draw on
**app. C** ([appendices/Appendix_C_HUD_Administrative_Record.md](appendices/Appendix_C_HUD_Administrative_Record.md) —
the HUD-27061 chronology, FHIP docket history, OIRA cycle record, and the author's 2026
PRA-comment module at `article/appendices/admin_record_c/pra_comment_2026/`), and Part IV.B on **app. D**
([appendices/Appendix_D_Standing_Reviewability_Annex.md](appendices/Appendix_D_Standing_Reviewability_Annex.md) —
the extended ADAPT/P&A/petitioner standing analysis). Per-citation resolution:
[`APPENDIX_CROSSWALK.md`](APPENDIX_CROSSWALK.md). New claims: `CLAIMS_LEDGER.csv` rows C45–C48.

---

## Introduction (Ely vignette; record-architecture thesis; § 553(e) preview)

| Material | Repository location |
|---|---|
| *Ely v. Mobile Hous. Bd.* narrative | Case is in `data/FHA_Unified_Database.json`; doctrinal analysis is the author's |
| 1.80 million disabled households | [`appendices/Appendix_L_HUD_Administrative_Data.md`](appendices/Appendix_L_HUD_Administrative_Data.md) (per-program breakdown) |
| NSPIRE accessibility scope | [`appendices/Appendix_T_NSPIRE_UFAS_Crosswalk.md`](appendices/Appendix_T_NSPIRE_UFAS_Crosswalk.md) |
| 2022-2023 PRA cycle (fn 6) | [`../record/hud-27061/`](../record/hud-27061/) — 87 FR 58,524, 88 FR 5,370, SSA_2023, ICR landing pages |
| Data Repository citation (fn 7) | This repository; orientation files: [`CLAIMS_LEDGER.csv`](CLAIMS_LEDGER.csv), [`../replication/SAMPLE_DEFINITIONS.md`](../replication/SAMPLE_DEFINITIONS.md), [`../replication/REPRODUCE.md`](../replication/REPRODUCE.md), [`../method/VALIDATION.md`](../method/VALIDATION.md) |

---

## Part I: The Anatomy of a Record-Dependent Right

### Part I lead — Two Modalities of Civil-Rights Verification

Doctrinal material carried in the Part I lead. No repository-specific empirical material; the pattern/feature distinction is developed from the AFFH-T Data Documentation and HMDA architecture cited in the footnotes.

### I.A — The Enacted Disability Package

| Material | Repository location |
|---|---|
| Per-program disability prevalence and 1.80M figure | [`appendices/Appendix_L_HUD_Administrative_Data.md`](appendices/Appendix_L_HUD_Administrative_Data.md) |
| Duty-to-record matrix (Table in text) | Author's synthesis; underlying duties are statutory |
| UFAS/§ 504 crosswalk | [`appendices/Appendix_T_NSPIRE_UFAS_Crosswalk.md`](appendices/Appendix_T_NSPIRE_UFAS_Crosswalk.md) |

### I.B — Section 504's Missing Compliance Baseline

Doctrinal section. Cases cited (*Schwarz*, *Keys Youth*, *Ely*) are in `data/FHA_Unified_Database.json`.

### I.C — Reasonable Accommodation as the Paradigm Record-Dependent Duty

| Material | Repository location |
|---|---|
| AFFH-T race-to-disability layer ratio (~5:1) | [`appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](appendices/Appendix_M_Doctrinal_Audit_Methodology.md) (AFFH-T analysis) |
| 47-AFH disability-depth audit | [`appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](appendices/Appendix_M_Doctrinal_Audit_Methodology.md) §§ M.7-M.10 (the underlying research memoranda are retained in the project's private research records; see `../replication/DATA_PROVENANCE.md`) |
| Analyses-of-impediments supplementary coding (AFH-audit methodology; the study is at app. M) | [`appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](appendices/Appendix_M_Doctrinal_Audit_Methodology.md) § M.11 (underlying memoranda retained privately) |
| GAO-23-105083 findings | [`../record/hud-27061/GAO_23_105083.pdf`](../record/hud-27061/GAO_23_105083.pdf) |
| HUD OIG 2022-BO-0001 | [`../record/hud-27061/HUD_OIG_2022-BO-0001.pdf`](../record/hud-27061/HUD_OIG_2022-BO-0001.pdf) |

### I.D — Existing Fragments Prove Feasibility, Not Completion

| Material | Repository location |
|---|---|
| NSPIRE/UFAS crosswalk (17 categories) | [`appendices/Appendix_T_NSPIRE_UFAS_Crosswalk.md`](appendices/Appendix_T_NSPIRE_UFAS_Crosswalk.md) |
| NSPIRE final rule (88 FR 30,442) | [`../record/hud-27061/88FR30442_nspire_final.pdf`](../record/hud-27061/88FR30442_nspire_final.pdf) |
| PIH Notice 2022-03 | [`../record/hud-27061/PIH_2022_03.pdf`](../record/hud-27061/PIH_2022_03.pdf) |
| HUD-50058 / HUD-50059 / HEMS PIA references | Doctrinal; form numbers cited from HUD publications |

### I.E — Part 121, § 3608(e)(6), and the Mandate-Instrument Mismatch

| Material | Repository location |
|---|---|
| 60-day notice (87 FR 58,524) | [`../record/hud-27061/87FR58524_proposal.pdf`](../record/hud-27061/87FR58524_proposal.pdf) |
| 30-day notice (88 FR 5,370) | [`../record/hud-27061/88FR5370_30day_notice.pdf`](../record/hud-27061/88FR5370_30day_notice.pdf) |
| Part 121 preamble (54 FR 3,232) | [`../record/hud-27061/54FR3232_part_121_promulgation.pdf`](../record/hud-27061/54FR3232_part_121_promulgation.pdf) |
| OMB ICR record (2535-0113) | [`../record/hud-27061/icr_202301-2535-001.html`](../record/hud-27061/icr_202301-2535-001.html); [`../record/hud-27061/SSA_2023.txt`](../record/hud-27061/SSA_2023.txt) |
| Supporting Statement A | [`../record/hud-27061/2535-0113_supporting_statement_A.docx`](../record/hud-27061/2535-0113_supporting_statement_A.docx) |
| § 3614a reported-decision sweep (fn 141: the Note prints seven decisions returned, all proximity artifacts, and no substantive Part 121 invocation; the archived query records the underlying runs) | [`../replication/queries/3614a_comparator.query.txt`](../replication/queries/3614a_comparator.query.txt) (the as-run audit memorandum is retained in the project's private research records) |
| Public comments on HUD-27061 | [`../record/hud-27061/comment_SAGE.pdf`](../record/hud-27061/comment_SAGE.pdf); [`../record/hud-27061/comment_Williams1.txt`](../record/hud-27061/comment_Williams1.txt) |
| Full oira_harvest manifest | [`../record/hud-27061/file_inventory.csv`](../record/hud-27061/file_inventory.csv) |
| Part 121 reported-decision surface (the manuscript describes fragmented, program-specific implementation; no citation-ratio benchmark is claimed) | [`appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](appendices/Appendix_M_Doctrinal_Audit_Methodology.md) §§ M.2.1–M.2.2 |
| FY 1989–FY 2023 HUD annual-report longitudinal audit | [`appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](appendices/Appendix_M_Doctrinal_Audit_Methodology.md) § M.12 (the underlying deep-dive memorandum is retained privately) |

---

## Part II: Private Enforcement and the Record Gap

### II.A — Why the Private-Enforcement Fallback Falls Short

Doctrinal section. Institutional-contraction evidence cited from NFHA 2025 and related public sources.

### II.B — Database and Methodology

| Material | Repository location |
|---|---|
| FHA Unified Database | [`../data/FHA_Unified_Database.json`](../data/FHA_Unified_Database.json) |
| Corpus tiers T0-T4 | [`../replication/SAMPLE_DEFINITIONS.md`](../replication/SAMPLE_DEFINITIONS.md) |
| Classification pipeline | [`../method/pipeline/`](../method/pipeline/) — model configuration, prompts, consensus resolution |
| Validation design | [`../method/VALIDATION.md`](../method/VALIDATION.md) |
| Field schema | [`../data/dictionaries/fha_unified_database.md`](../data/dictionaries/fha_unified_database.md) |
| Pipeline code | [`../scripts/build_unified_db.py`](../scripts/build_unified_db.py) |
| Model registry | [`../method/pipeline/model_metadata.json`](../method/pipeline/model_metadata.json); [`../method/pipeline/adjudication_metadata.json`](../method/pipeline/adjudication_metadata.json) |
| Period-boundary sensitivity (fn 70: disposition-lag check, 77.7%) | [`appendices/Appendix_A4_Reproducibility_Audit.md`](appendices/Appendix_A4_Reproducibility_Audit.md) § A-4.11 |

### II.C — The Composition Effect

| Material | Repository location |
|---|---|
| Table 1 (case-level census series) | [`../results/series_2026-07.json`](../results/series_2026-07.json); verification guards in [`../scripts/validate_claims.py`](../scripts/validate_claims.py) |
| Rate decomposition (not reported in the Note; fn 71: the P1-to-P3 aggregate change is approximately zero, so there is no decline to decompose) | [`../scripts/decomposition.py`](../scripts/decomposition.py) (document-level archive) |
| Counsel-timing audit over the eighteen qualifying cases (fn 164) | [`../results/counsel_timing_audit/`](../results/counsel_timing_audit/) (per-case CSV, audit report, frame note) |
| Bootstrap CIs | [`../scripts/robustness_bootstrap.py`](../scripts/robustness_bootstrap.py) |
| Robustness checks | [`../scripts/robustness_checks.py`](../scripts/robustness_checks.py) (document-level robustness write-ups retained in the project's private research records) |
| Selective-screening diagnostic | Document-level interaction diagnostic retained in the project's private research records |

### II.D — Repeat Players as Substitute Record Infrastructure

| Material | Repository location |
|---|---|
| Institutional-plaintiff hierarchy | [`../scripts/h5_analysis.py`](../scripts/h5_analysis.py) |
| Procedural-depth tabulation | [`appendices/Appendix_H_Supplementary_Data.md`](appendices/Appendix_H_Supplementary_Data.md) § H.5 |
| Document-level plaintiff-type and regression analyses | Retained in the project's private research records (see `../replication/DATA_PROVENANCE.md`); nothing the Note prints relies on them |

### II.E — Pleading Gates and the Translation Problem

| Material | Repository location |
|---|---|
| MTD survival rates | [`appendices/Appendix_H_Supplementary_Data.md`](appendices/Appendix_H_Supplementary_Data.md); [`appendices/Appendix_B_Results_Tables.md`](appendices/Appendix_B_Results_Tables.md) |
| Claim-type hierarchy | [`../scripts/h1_h2_analysis.py`](../scripts/h1_h2_analysis.py); [`appendices/Appendix_E_Accommodation_Defendant_Analysis.md`](appendices/Appendix_E_Accommodation_Defendant_Analysis.md) |
| TRANSLATION-family mechanism coding | [`../method/validation_three_model/`](../method/validation_three_model/) (three-model ensemble); [`appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](appendices/Appendix_M_Doctrinal_Audit_Methodology.md) |
| 45.3% / 13.7% / 31.6 pp headline | [`CLAIMS_LEDGER.csv`](CLAIMS_LEDGER.csv) entries C29-C30 |

### II.F — Causation Limits and Transition

| Material | Repository location |
|---|---|
| Period-boundary sensitivity | [`appendices/Appendix_A4_Reproducibility_Audit.md`](appendices/Appendix_A4_Reproducibility_Audit.md) § A-4.11 |
| Document-level circuit tabulations | Retained in the project's private research records |

---

## Part III: The Statutory Data Floor

### III.A — The Authority Stack -- Field by Field

| Material | Repository location |
|---|---|
| § 3614a federal-opinion sweep | [`appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](appendices/Appendix_M_Doctrinal_Audit_Methodology.md) §§ M.2.1-M.2.2 |
| § 3614a comparator query (archived run; the Note's printed count is fn 141's seven-decision, all-proximity-artifact result) | [`../replication/queries/3614a_comparator.query.txt`](../replication/queries/3614a_comparator.query.txt) |
| Part 121 / 24 C.F.R. § 100.200 comparator | [`../replication/queries/100_200_comparator.query.txt`](../replication/queries/100_200_comparator.query.txt) |

### III.B — Minimum Viable Data Categories and Privacy Architecture

| Material | Repository location |
|---|---|
| PIH 2022-03 four-category vocabulary | [`../record/hud-27061/PIH_2022_03.pdf`](../record/hud-27061/PIH_2022_03.pdf) |
| Archived perimeter census and its mandatory disclosures (body text: "the archived perimeter census and its mandatory disclosures are in the repository") | [`../results/supporting/perimeter_census.md`](../results/supporting/perimeter_census.md) |

### III.C — HUD-27061 Is Evidence, Not Remedy

| Material | Repository location |
|---|---|
| Form HUD-27061 | [`../record/hud-27061/form_HUD-27061_current.pdf`](../record/hud-27061/form_HUD-27061_current.pdf) |
| Supporting Statement A | [`../record/hud-27061/2535-0113_supporting_statement_A.docx`](../record/hud-27061/2535-0113_supporting_statement_A.docx) |

### III.B–III.C — Feature-verification module material

| Material | Repository location |
|---|---|
| Australia SDA comparative note | [`../data/australia_sda/`](../data/australia_sda/) (data extract; the comparative memorandum is retained in the project's private research records) |
| Massachusetts Housing Navigator; architecture design | Architecture appendix in companion research in preparation; not part of this Note |
| GAO aggregate-data finding (fn 109: GAO-23-105083 at 18-19 — aggregate request and disposition data would let HUD identify patterns warranting inquiry) | [`../record/hud-27061/GAO_23_105083.pdf`](../record/hud-27061/GAO_23_105083.pdf) |

### III.D — Disability Data as a Floor, Not a Substitute (includes the "Race Is Not the Ceiling" material)

Doctrinal section. A supplementary *Loper Bright* ratchet analysis (not cited in the Note) is retained in the project's private research records.

### III.E — Records, Not Reports

Doctrinal section on the 2026 federal actions (the OLC opinion, the DOJ *Olmstead* guidance notice, and the EEOC report-rescission NPRM) and the record/report distinction. Cited from primary sources in the Note's footnotes; the petition-side treatment of the same distinction is at [`../action/553e_petition_individual.md`](../action/553e_petition_individual.md) §§ 5.7–5.8 and 9.2–9.3.

---

## Part IV: Petition, Administrative Record, and Contingent Review

### IV.A — The § 553(e) Petition and Its Administrative Predicate

| Material | Repository location |
|---|---|
| Petition template (organizational sections) | [`../action/553e_petition_template.md`](../action/553e_petition_template.md) |
| Petition template (individual sections) | [`../action/553e_petition_individual.md`](../action/553e_petition_individual.md) |
| 2026 public-comment template | [`../action/2026_comment_template.md`](../action/2026_comment_template.md) |
| PRA evidentiary record | [`../record/hud-27061/`](../record/hud-27061/) (full manifest at [`../record/hud-27061/file_inventory.csv`](../record/hud-27061/file_inventory.csv)) |

No litigation template is published: any complaint would need to respond to an actual
agency disposition, an identified plaintiff, the governing venue, and the resulting
administrative record, none of which presently exists. Litigation-development analyses
are retained in the project's private research records (see
`../replication/DATA_PROVENANCE.md`).

### IV.B — If HUD Denies: Standing, Review, and Remedy

| Material | Repository location |
|---|---|
| *ADAPT v. HUD* context | [`appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](appendices/Appendix_M_Doctrinal_Audit_Methodology.md) §§ M.2.1-M.2.2 (thin reported-decision surface) |
| Part 121 preamble | [`../record/hud-27061/54FR3232_part_121_promulgation.pdf`](../record/hud-27061/54FR3232_part_121_promulgation.pdf) |

### IV.C — The Reasoned-Denial Floor: *Coinbase*, *State Farm*, and Architecture Mismatch

| Material | Repository location |
|---|---|
| Identical 8,625-hour burden estimate | [`../record/hud-27061/SSA_2023.txt`](../record/hud-27061/SSA_2023.txt); [`../record/hud-27061/87FR58524_proposal.pdf`](../record/hud-27061/87FR58524_proposal.pdf) |
| Part 121 regulatory text | [`../record/hud-27061/research_outputs/24CFR121_current_raw.html`](../record/hud-27061/research_outputs/24CFR121_current_raw.html) |

### IV.D — HUD's Strongest Defenses

Doctrinal section.

---

## Conclusion

The Conclusion synthesizes Parts I-IV. No new empirical material is introduced.

---

## Data Availability Statement

| Material | Repository location |
|---|---|
| Replication archive | This repository |
| Reproduction commands | [`../replication/REPRODUCE.md`](../replication/REPRODUCE.md) |
| Claims ledger | [`CLAIMS_LEDGER.csv`](CLAIMS_LEDGER.csv) |


## Part II.E-II.F comparator and robustness cross-references

- **fn 87** (translation-family finding) now cross-cites **app. A-6**: the comparator's
  common-rubric rationale mix corroborates the translation gap from a second instrument
  (replication/comparator/RATIONALE_SUMMARY_CONSENSUS.csv; verification in
  replication/comparator/recoding_2026-07-07/raw_text_verification/).
- **fn 89** (bundled-shocks) reports the comparator contrast direction-only and carries the
  pre-trend candor clause; the exploratory comparator shares live at appendix level in
  **app. A-6** (design, contrasts, verification, confound register, and sec. A-6.9
  pre-trend check), with underlying artifacts in replication/comparator/ and results/supporting/.
- **fn 90** (selection) carries the registered selection audit: **app. A-7** (selection audit +
  institutional participation/exit), artifacts in results/supporting/.
