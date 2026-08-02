# Dictionary: Mechanism-Coding Artifacts

This dictionary describes the schemas, controlled vocabularies, and artifacts used for mechanism and per-claim classification. `Per-claim structured extraction` is the fixed name of Stage 4; its outputs are classifications generated through answers to fixed questions and do not independently establish case facts.

Assurance and field conventions for all three dictionaries are in [`README.md`](README.md).

The Part II.E TRANSLATION-family pro-se / represented gap reported in the Note (45.3% / 13.7% / ≈ 32 pp on 727 contingency rows; family × representation χ²(8) = 72.07, p = 1.9 × 10⁻¹², Cramér's V = 0.315) is produced by a three-model majority-vote ensemble on the refreshed 739-row pleading-loss universe (736 classified, 728 ensemble-coded), with three convergent validation layers. The three validation layers cover the pre-refresh 668-case universe. All artifacts live in validation subdirectories keyed off `source_file` from the FHA Unified Database. Full methodology is documented in [Appendix M § M.16](../../article/appendices/Appendix_M_Doctrinal_Audit_Methodology.md) and [`../../method/VALIDATION.md`](../../method/VALIDATION.md) § 3–5.

## Primary mechanism-family coding — three-model majority-vote ensemble (n = 728 / 736)

**Directory:** `method/validation_three_model/` | **Report:** `ensemble_report.md` | **Merged dataset:** `ensemble_results.json` | **Raw per model:** `kimi_raw_results.json`, `glm_raw_results.json`, `deepseek_raw_results.json`

Three separately run coders — Kimi K2.6, GLM-5.1, and DeepSeek V3.2 — are run on each pleading-loss case. Each row in `ensemble_results.json` carries `source_file`, per-model `pleading_failure_family` and `pleading_failure_mechanism`, `ensemble_bucket` (majority vote; 3-way splits resolve to OTHER), and the earlier K2.5 + GLM-5.1 coding for reference. 668 of the original 676 cases were successfully coded by all three primary models (8 dropped where at least one coder returned unparseable output); the July 3, 2026 corpus refresh added pleading-loss rows coded under the same frozen prompt and majority-vote rule, for a merged universe of 728 ensemble-coded cases of 736 classified (see [`../../method/VALIDATION.md`](../../method/VALIDATION.md) § 3 for the increment artifacts). Merged bucket-level Fleiss' κ = 0.6297 across the three primary coders (pre-refresh 0.6292; substantial agreement under Landis & Koch). Merged primary-ensemble headline: TRANSLATION-family pro se 45.3% vs. represented 13.7% on 727 contingency rows (632 pro se, 95 represented), gap ≈ 32 pp; χ²(8) = 72.07, p = 1.9 × 10⁻¹², Cramér's V = 0.315 (pre-refresh: 46.35% / 14.29% / 32.06 pp; χ²(8) = 68.49 and Cramér's V = 0.33 over the 622 rows outside the OTHER family).

<details>
<summary><strong>Validation Layer (i)</strong> — Blind Claude Opus 4.7 fourth-coder re-read (n = 668)</summary>

**Directory:** `method/validation_four_coder_full/` | **Report:** `confirmation_report.md` | **Merged dataset:** `fourth_coder_full_merged.json` | **Raw per chunk:** `coder_seat_{01..22}_results.json` | **Blind manifests:** `chunk_{01..22}_blind.json` | **Universe manifest:** `universe_668.json` | **Aggregation script:** `aggregate_full.py`

22 parallel Claude Opus 4.7 subagents, each given the verbatim mechanism prompt and a blind manifest containing only `source_file` and `file_path`. Each row in `fourth_coder_full_merged.json` carries `source_file`, `pleading_failure_family`, `pleading_failure_mechanism`, `confidence`, subagent chunk identifier, and — after aggregation — the primary-ensemble and earlier-coding comparisons. Fourth-coder vs. primary-ensemble bucket κ = 0.6024 (substantial agreement); Opus 4.7 TRANSLATION-family gap ≈ 29.24 pp. Subagents 17 and 19 emitted `family`/`family_code` key variants; `aggregate_full.py` normalizes both forms to the canonical `pleading_failure_family`/`pleading_failure_mechanism`.

</details>

<details>
<summary><strong>Validation Layer (ii)</strong> — Backward-compatibility against the earlier K2.5 + GLM-5.1 coding (n = 150 sample; n = 676 full)</summary>

**Directory:** `method/validation_kimi_k2_6/` | **Report:** `agreement_report.md` | **Merged dataset:** `agreement_results.json` | **Raw:** `kimi_k2_6_raw_results.json`

Stratified random sample of 150 pleading-loss opinions carrying `source_file`, `pleading_failure_family`, `pleading_failure_mechanism`, `confidence`, and an earlier two-model K2.5 + GLM-5.1 coding. Cohen's κ = 0.6264 on the 150-case sample under a single-model K2.6 re-read. At full-universe scale, the primary three-model ensemble returns κ = 0.574 against the two-model K2.5 + GLM-5.1 coding (31.9 pp gap on 676), confirming directional stability across coding pipelines.

</details>

<details>
<summary><strong>Validation Layer (iii)</strong> — Opus-4.7-as-resolver sensitivity</summary>

**Directory:** `method/validation_three_model/` | **Report:** `opus_resolver_report.md`

Sensitivity variant in which the majority-vote rule is replaced by Opus 4.7 as tiebreaker on disputed cases. Opus-as-resolver coding κ = 0.80 vs. primary ensemble; gap = 29.24 pp; p = 2.45 × 10⁻⁷. All three validation-layer gaps sit inside the 29 – 32 pp band around the 32.1 pp pre-refresh primary headline (merged post-refresh headline ≈ 32 pp).

</details>
