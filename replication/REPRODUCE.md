# Reproducing the Empirical Findings

This file maps each headline empirical claim in the Note to the script that produces it and the artifact the script writes. Run everything from the repository root with Python 3.11+ and the dependencies in `requirements.txt`.

**Contents.** [Quick start](#quick-start) · [Document-level composition diagnostics](#document-level-composition-diagnostics-part-iic-context) · [Bootstrap CIs](#bootstrap-cis-part-iic-appendix-a5) · [Hypothesis tests](#hypothesis-tests-part-iid-iie) · [PUMS cross-tabulations](#pums-cross-tabulations-part-ib) · [HUD administrative findings](#hud-administrative-findings-part-id-ie) · [Doctrinal / qualitative](#doctrinal--qualitative-analyses) · [Doctrinal audit memoranda](#doctrinal-audit-memoranda-footnote-apparatus) · [Canonical corpus tiers](#canonical-corpus-tier-counts) · [Dependencies](#dependencies)

## Quick start

```bash
pip install -r requirements.txt

# The Part II series of record: re-derive the case-level census, assert every
# registered value, then run the full eighteen-check release gate.
python scripts/build_case_level_series.py --check
python scripts/validate_claims.py
python scripts/run_release_checks.py
```

The document-level pipeline scripts below regenerate the corpus-level diagnostic
tables into `results/` (pipeline diagnostics, not the reported Part II series):

```bash
# From repo root, each script writes into results/
python scripts/recompute_stats_unified.py   # Core three-period tables
python scripts/recompute_stats_unified.py --narrow  # Protected-class-only robustness tables
python scripts/decomposition.py             # Kitagawa + Oaxaca-Blinder decomposition
python scripts/robustness_bootstrap.py      # 10,000-resample bootstrap CIs (seed 42)
python scripts/robustness_checks.py         # Reclassification + period-boundary sensitivity
python scripts/h1_h2_analysis.py            # Claim specificity + representation × complexity
python scripts/h5_analysis.py               # Institutional plaintiff hierarchy
python scripts/h6_analysis.py               # Physical evidence
python scripts/h7_analysis.py               # Three-period trajectory
python scripts/h8_analysis.py               # Private-enforcement adequacy by claim type
```

Scripts resolve paths through `scripts/config.py`, which reads `FHA_DATA_DIR` (default `./data/`) and writes into `./results/`. No hardcoded absolute paths.

### Case-level adjudication boundary

The Part II case-level series (N = 606: 287/68/251, eighteen qualifying judgments, and
every cell derived from them) is carried in `results/series_2026-07.json` and
`results/case_level_recount.csv`. Everything DERIVED from the base counts — rates,
shares, differences, and all exact Clopper-Pearson intervals — recomputes from those
artifacts and is asserted by `scripts/validate_claims.py`.

The case-level series is fully re-derivable from this repository. The per-row
record of the one-case-one-unit transformation -- every kept opinion row, its
case unit, its bounded keep code, and the dated fields the rules order on -- is
published at [`case_level_census.csv`](case_level_census.csv), with the complete
rule set in [`CASE_LEVEL_RULES.md`](CASE_LEVEL_RULES.md).
`scripts/build_case_level_series.py --check` re-derives every unit's outcome,
period, and representation from those rows alone -- including the terminal-row
rule, which orders on the published `row_decision_date` and breaks ties on
`db_index` -- recomputes every registered series value, and fails on any drift;
the release gate runs the same check. No unit's value is taken on trust from the
record's unit-level columns.

What remains outside that record is the classification itself. The row-level
labels are model outputs produced under frozen, published instruments, and which
opinions entered the decided census is governed by the tier definitions in
[`SAMPLE_DEFINITIONS.md`](SAMPLE_DEFINITIONS.md). Those stages are reproducible
as fresh classifications under the published instruments, not as byte-identical
reruns (see [`../method/AGILE_ELS.md`](../method/AGILE_ELS.md) section 8).

**What an independent reader can verify from this repository.** A reader can inspect the
public source and classification artifacts, rerun the document-level analyses end to end
from `data/FHA_Unified_Database.json` with the scripts above, recompute the case-level
series from the published per-row record, reproduce every downstream computation that
begins from it, compare those outputs to the registered claim values in
`CLAIMS_LEDGER.csv`, and run the full release gate.

When filtering the July 2026 corpus refresh, match BOTH source tags
(`p3ext_20260703` and `p3ext_20260703_r2`); see `SAMPLE_DEFINITIONS.md`.

## Claim → artifact map

### Document-level composition diagnostics (Part II.C context)

> [!NOTE]
> This section reproduces **document-level** pipeline diagnostics. The reported
> Part II series is the case-level series in
> [`../results/series_2026-07.json`](../results/series_2026-07.json)
> (qualifying-judgment rates 3.48 / 0.00 / 3.19 over the universal
> one-case-one-unit N 287/68/251); the manuscript reports no aggregate outcome
> trend and no document-level outcome rate. Document-level outcome-rate cells are
> not registered claim targets; the scripts remain runnable and their outputs are
> diagnostics of the classification pipeline, not reported results.

| Claim | Script | Output (key) | Note value |
|---|---|---|---|
| Pro se share P1 | `robustness_bootstrap.py` | `bootstrap_ci_results.json` `point_estimates_by_period.P1.pro_se_share` | 60.1% |
| Pro se share P3 | " | `point_estimates_by_period.P3.pro_se_share` | 77.9% |

### Bootstrap CIs (Part II.C, Appendix A5)

| Claim | Output key | Reproduced (95% percentile) |
|---|---|---|
| Pro se share P1 | `bootstrap_ci.P1_pro_se_share` | [55.7, 64.5] |
| Pro se share P3 | `bootstrap_ci.P3_pro_se_share` | [73.7, 82.0] |

### Hypothesis tests (Part II.D, II.E)

| Claim | Script | Output | Note value |
|---|---|---|---|
| Specific-duty broad-win rate | `h1_h2_analysis.py` | `h1_h2_results.json` `h1_win_rates.SPECIFIC_DUTY.broad_win_rate` | 39.3% |
| Open-textured broad-win rate | " | `h1_win_rates.OPEN_TEXTURED.broad_win_rate` | 1.05% |
| Institutional plaintiff hierarchy | `h5_analysis.py` | `h5_results.json` | see Note Part II.D |
| Physical evidence OR | `h6_analysis.py` | `h6_results.json` `phys_evidence.or` | 1.67 |
| MTD survival by period × representation | `h7_analysis.py` | `h7_results.json` `model1_mtd_survival` | rep stable, aggregate down |
| Private-enforcement adequacy by claim type | `h8_analysis.py` | `h8_results.json` | varies |

### PUMS cross-tabulations (Part I.B)

| Claim | Script | Output | Note value |
|---|---|---|---|
| Disability cost-burden penalty (race decomposition) | `pums_extended_crosstabs.py` | `extended_crosstabs_results.json` | 7.3 – 16.9 pp |
| Housing stock concentration | `pums_housing_stock_analysis.py` | `housing_stock_results.json` | archive-only support for Part I.B (former app. A-2 material; no current appendix) |
| Pre-1991 statutory gap analysis | `pums_pre1991_gap_analysis.py` | `pre1991_statutory_gap_analysis.json` | archive-only support for Part I.B (former app. A-2 material; no current appendix) |

### HUD administrative findings (Part I.D, I.E)

| Claim | Script | Output | Note value |
|---|---|---|---|
| CDBG activity-code accessibility gap | `cdbg_analysis.py` + `cdbg_accessibility_gap_analysis.py` | `cdbg_results.json`, `cdbg_accessibility_gap_quantification.md` | 2 of ~100 matrix codes are disability-specific |
| NSPIRE / REAC physical inspection gap | `reac_analysis.py` | `reac_results.json` | see Note Part I.E |
| POSH subsidized-housing disability rates | `posh_analysis.py` | `posh_results.json` | 39.3% weighted household rate |
| AHS 2023 accessibility module | `ahs_2023_accessibility_analysis.py` | `ahs_2023_accessibility_results.json` | see Note Part I.B |

### Doctrinal / qualitative analyses

| Claim | Script | Output |
|---|---|---|
| Iqbal / Twombly application at pleading gate | `fha_iqbal_analysis.py` | `extended_doctrinal_analysis.json` |
| Circuit-level variation in outcomes | `circuit_district_deep_dive.py` | `circuit_district_deep_dive_results.json` |
| Public-defendant process-claim underperformance | `public_defendant_analysis.py` | `public_defendant_process_failure_results.json` |
| Pro se pleading-mechanism divergence | `pro_se_mechanism_analysis.py` | `pro_se_mechanism_divergence_results.json` |
| LIHTC QAP accessibility audit (50 states + DC) | `lihtc_accessibility_audit.py`, `qap_accessibility_2025_2026_scan.py`, `make_qap_ledger.py` | `lihtc_accessibility_audit_results.json`, `qap_accessibility_2025_2026.json`, `qap_jurisdiction_ledger.csv` |

### Doctrinal audit memoranda (footnote apparatus)

The Note's footnote-level citations rely on a set of human-authored audit memoranda that document Federal Register and reginfo.gov records, HUD report coding, and ACS / POSH derivations. Each memorandum states its query / source, run date, and inclusion rule. Methodology and file-to-footnote crosswalk are in [`../article/appendices/Appendix_M_Doctrinal_Audit_Methodology.md`](../article/appendices/Appendix_M_Doctrinal_Audit_Methodology.md).

| Note claim | Audit file | Section(s) |
|---|---|---|
| Part 121 / DOJ § 3604(f)(3) population audit | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 8 | M.2.1 |
| § 3614a 42-opinion audit | `doctrinal_case_audits.md` (retained in the project's private research records) § 1 | M.2.2 |
| Part 121 eCFR / Federal Register / ICR verification | `record/hud-27061/cfr_part121_analysis.md` | M.3 |
| 2022–2023 HUD-27061 PRA record | `methodological_audits_and_validation.md` (retained in the project's private research records) § 6 | M.4 |
| AFFH-T disability-visualization gap | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 4 | M.5 |
| NSPIRE / UFAS § 504 17-category crosswalk | `program_specific_accessibility_gaps.md` (retained in the project's private research records) § 1 | M.6 |
| Part 8 stock-level verification gap + pre-1991 stock share | `design_construction_bottleneck.md` (retained in the project's private research records) § 4 | M.7 |
| 1988 FHAA preamble disability-data passages | `historical_disability_data_record.md` (retained in the project's private research records) § 1 | M.8 |
| LIHTC QAP 51-jurisdiction audit | `program_specific_accessibility_gaps.md` (retained in the project's private research records) § 2 | M.9 |
| 739-case pro se mechanism divergence | `pro_se_doctrine_production_filter.md` (retained in the project's private research records) § 2 | M.10 |
| 47-AFH disability-depth audit | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 1 | M.11 |
| FY 1989 – FY 2023 HUD annual-report longitudinal audit | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 5 | M.12 |
| HMDA disclosure-effect meta-analysis | `comparative_contextual_empirics.md` (retained in the project's private research records) § 4 | M.13 |
| Australia SDA comparative note | `comparative_contextual_empirics.md` (retained in the project's private research records) § 3 | M.14 |
| Mechanism-family Layer 1 re-code (Kimi K2.6 sample) | `method/validation_kimi_k2_6/agreement_report.md` | M.16.1 |
| Mechanism-family Layer 2 ensemble (K2.6 + GLM-5.1 + DeepSeek V3.2) | `method/validation_three_model/ensemble_report.md` | M.16.2 |
| Mechanism-family Layer 3 full-universe blind fourth-coder re-read (Claude Opus 4.7) | `method/validation_four_coder_full/confirmation_report.md` | M.16.3 |
| 47-AFH disability-depth audit — supplementary memo | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 2 | M.11 |
| AFH disability-goals funding trace | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 3 | M.11 |
| Voucher disability utilization analysis | `program_specific_accessibility_gaps.md` (retained in the project's private research records) § 4 | M.7 |
| HUD-27061 / OMB Control 2535-0113 live-status memo | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 7 | M.4 |
| ADA Title II transition-plan audit | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 10 | M.6 |
| Affirmative-administration information-systems survey | `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 6 | M.6 |

## Canonical corpus-tier counts

All Note-level claims are nested inside the following reproducible tiers on `data/FHA_Unified_Database.json`:

| Tier | Filter | n |
|---|---|---|
| T0 — Raw unified corpus | all records | 3,366 |
| T1 — Screened-in | `screening_result == "YES"` | 2,690 |
| T2 — Disability-screened (canonical) | T1 AND (`protected_classes` ∋ `"disability"` OR `disability_alleged` OR `is_ra_case`) | 1,900 |
| T2-narrow — Robustness sample | T1 AND `"disability" ∈ protected_classes` | 1,849 |
| T3 — Disability-wave tranche | T2 AND `date_filed ≥ 2022-01-01` | 1,347 |
| T4 — Pleading-loss universe | T2 AND pleading-stage loss filter (see Appendix A and Appendix M.10) | 739 |

T2's disjunctive filter is canonical because it mirrors the Note's doctrinal reasons for counting a disability allegation. T2-narrow is reported as a robustness check and produces substantively identical period comparisons.

## Dependencies

See `requirements.txt`. Core: pandas, numpy, statsmodels, scipy. Python 3.11+ recommended.

## Questions

Open an issue or email the author (see [`../CITATION.cff`](../CITATION.cff)).

## Body-statistic crosswalk (executable specifications)

Each headline statistic in the Note maps to a canonical filter and script. Population filters are
implemented once, in `scripts/analysis_filters.py` (`is_t2_canonical`, `assign_period`,
`is_decided`), and shared by every script below.

| Note statistic | Population / filter | Script | Output |
|---|---|---|---|
| Period composition — document-level (pro se share 60.1 -> 77.9, DIS_ANY sensitivity cohort); the reported Part II series is the case-level series in `results/series_2026-07.json` (qualifying-judgment rates 3.48 / 0.00 / 3.19 over N 287/68/251); document-level outcome rates are pipeline diagnostics, not reported results | T2 canonical; decided = {PLAINTIFF_WIN, DEFENDANT_WIN, MIXED}; P1/P2/P3 via `assign_period` | `scripts/recompute_stats_unified.py` | `results/unified_stats_report.md` |
| Kitagawa decomposition — document-level pipeline diagnostic, not reported in the manuscript; see the case-level series in `results/series_2026-07.json` | same decided universe, stratified on `pro_se` | `scripts/decomposition.py` | `results/decomposition_results.json` |
| Robustness checks 1-5 (reclassification, boundaries, exclusion, bootstrap, chi-squared) | per Appendix A-5 | `scripts/robustness_checks.py`, `scripts/robustness_bootstrap.py` | `results/robustness_checks_output.txt` |
| Pleading-loss universe (T4, n = 739) | T2 AND `procedural_posture` in {MOTION_TO_DISMISS, SCREENING_ORDER} AND `outcome` in {DEFENDANT_WIN, PROCEDURAL} | `method/validation_three_model/run_three_model.py` | `method/validation_three_model/ensemble_results.json` |
| TRANSLATION-family gap (45.3% / 13.7% / ~32 pp; directional, machine-based coding) | 728 of 739 T4 cases; family-bucket majority vote | `method/validation_three_model/compute_ensemble.py` | `method/validation_three_model/ensemble_report.md` |
| Plaintiff-type gradient (chi-squared(3) = 75.7) | dated decided n = 995; four classified plaintiff categories | `scripts/h5_analysis.py`; Appendix F tables via `scripts/recompute_all_appendices.py` | `results/h5_results.json` |
| Institutional share contraction (16.2% -> 8.1%) | dated any-outcome universe n = 1,347 | `scripts/recompute_all_appendices.py` (Appendix F section F.3.2) | `article/appendices/Appendix_F_Galanter_Plaintiff_Type.md` |
| Accommodation-type gradient | T2 decided, per-case field (document-level pipeline) | `scripts/recompute_all_appendices.py` (Appendix E section E.1) | `article/appendices/Appendix_E_Accommodation_Defendant_Analysis.md` |

## Comparator and robustness additions (apps. A-6 / A-7, added 2026-07-08)

| Claim | Universe | Script | Output |
|---|---|---|---|
| Comparator composition/outcome contrasts + Kitagawa shares (document-level arm series; pipeline diagnostics, not reported in the manuscript) | screened dated-decided, cohorts per app. A-6.2 | `replication/comparator/comparator_analysis.py` (deterministic; asserts DB SHA) | `replication/comparator/TABLE1_COMPARATOR.csv`, `replication/comparator/KITAGAWA_DECOMPOSITION.csv` |
| Family-A verified contrast (13.6% / 0.8% / 0.6% pro se pleading losses) | 476-row pleading-loss arms per app. A-6.4 | consensus: `replication/comparator/recoding_2026-07-07/scripts/compute_consensus.py`; verification triggers: `.../verification_compute.py` (model reruns need an OpenRouter key; the computations from committed raw outputs are deterministic) | `replication/comparator/RATIONALE_SUMMARY_CONSENSUS.csv`, `replication/comparator/recoding_2026-07-07/raw_text_verification/VERIFICATION_RESULTS.json` |
| Selection audit (max represented-mix shift 8.6pp); institutional participation series; P1 pre-trend (DIVERGING) | per `method/preregistration/REGISTRATION.md` | `scripts/strengthening_analysis.py`; independent checker `scripts/recompute_verification.py` | `results/supporting/selection_audit.csv`, `results/supporting/institutional_participation.csv`, `results/supporting/pretrend_p1_split.csv`, `results/supporting/registered_verification_results.txt` |

Every value is regression-checked against the manuscript by `scripts/validate_claims.py`.

## Opinion texts and the source manifest

The 853 opinion texts used by the validation and comparator runs are not distributed in this
repository; they are on file with the author. Per-row provenance for all 3,366 database records —
CourtListener cluster id, stable URL, availability status, and normalized-text SHA-256 for the
on-file texts — is in [`../opinion_sources.csv`](../opinion_sources.csv) (regenerate with
`python scripts/make_opinion_sources.py`; run without the on-file texts, regeneration carries the
registered hashes forward rather than recomputing them). Historical `case_texts/...` strings
retained inside frozen execution artifacts — including the comparator recoding inputs and
scripts (`comparator/recoding_2026-07-07/`) and the validation universes, samples, and
run scripts under `../method/validation_three_model/`, `../method/validation_kimi_k2_6/`, and
`../method/validation_four_coder_full/` — are source locators, not live repository paths;
re-running those analyses requires first materializing a local `case_texts/` store. Where a
CourtListener cluster id is available, `python scripts/fetch_opinion_texts.py` documents the
deterministic fetch-normalize-hash route; legacy rows without an embedded cluster id are reported
as SKIPPED-NO-ID rather than silently dropped.

## What is deterministic and what is not

Two different reproducibility claims apply to this archive; keep them separate:

- **Deterministic local recomputation (no network, no cost).** Every statistic cited in the Note
  recomputes from the frozen `data/FHA_Unified_Database.json` and the committed raw outputs of the
  headline mechanism ensemble — the three per-model result files and the disagreement log in
  [`../method/validation_three_model/`](../method/validation_three_model/): the analysis scripts in
  `scripts/`, the ensemble/consensus computations
  (`method/validation_three_model/compute_ensemble.py`, comparator `compute_consensus.py`,
  `verification_compute.py`), the comparator Table 1 (`replication/comparator/regenerate_table1.py`), and
  `scripts/validate_claims.py` all run offline and reproduce byte-stable results (bootstrap CIs are
  seed-fixed). The primary database pipeline is a different case: its tiered consensus resolution is
  documented in machine-readable form at
  [`../method/pipeline/adjudication_metadata.json`](../method/pipeline/adjudication_metadata.json),
  but its per-model Layer-1 raw outputs are not part of this release. Those classification stages are
  documented and bounded, not byte-replayable.
- **Model reruns (network, API cost, mutable hosted endpoints).** Re-executing the classification
  itself — `method/validation_three_model/run_three_model.py`, `method/validation_kimi_k2_6/run_kimi_k2_6.py`,
  the comparator verification recode — calls hosted LLM APIs (OpenRouter key required), costs
  money, and depends on models the vendors can change or retire. These reruns test reproducibility
  of the *method*; they are not required to verify any published number, because every published
  number derives from the frozen database and the committed ensemble outputs by the deterministic
  route above.
- **Corpus reconstruction** (re-harvesting and re-screening from CourtListener) is NOT supported
  end-to-end from this archive; `scripts/build_unified_db.py` documents the pipeline but requires
  upstream working files retained in the project's private research records (DATA_PROVENANCE.md). The frozen canonical JSON is the
  replication baseline.

## Environment

- Python >= 3.11 (published numbers last regenerated under CPython 3.13 on Windows 11; the
  deterministic release checks are OS-independent).
- `pip install -r requirements.txt` for supported floors, or `pip install -r requirements-lock.txt`
  for the exact tested versions.
- Deterministic local checks and analyses need NO network access, API keys, or spend. Model reruns
  need an OpenRouter key (order ~$5-$30 per run, see each directory's README) and, for
  `scripts/supplemental_batch.py`, an Anthropic key. Census PUMS scripts hit the public Census API
  (no key). The QAP scan additionally needs the external `pdftotext` binary (poppler-utils).
- One-command deterministic gate: `python scripts/run_release_checks.py` runs eighteen checks in
  sequence and exits 0 only if every one passes. What each check asserts — and what a green run does
  and does not establish — is in [`GATES.md`](GATES.md). `scripts/run_all.py` regenerates the core
  analyses; the comparator, registered-baseline, and QAP analyses have their own commands listed above.

## Release manifest

[`../RELEASE_MANIFEST.json`](../RELEASE_MANIFEST.json) hashes every tracked file in the release
(SHA-256 raw bytes, plus an LF-normalized hash for text files). Verify a clone with
`python scripts/check_release_manifest.py`; regenerate after any intentional change with
`python scripts/make_release_manifest.py`. The module hash manifests inside `comparator/`
(`comparator/HASH_MANIFEST.json`, `comparator/provenance/remediation_hash_manifest.json`,
`comparator/provenance/verification_stage_manifest.json`)
and `../method/preregistration/` (`HASH_MANIFEST.json`) pin the module artifacts and frozen instruments;
the release manifest above is the verification instrument for the tree as a whole.
