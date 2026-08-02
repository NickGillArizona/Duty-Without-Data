# Tiered Consensus Resolution Algorithm

## Overview

Three-model outputs are consolidated into a single canonical record using a
tiered resolution strategy designed to minimize cost while preserving accuracy.

## Algorithm

### Tier 0 — Full Consensus (No API Call)
All three models return identical values for every categorical field.
→ Adopt as canonical.

### Tier 1 — Majority Agreement, Non-Critical Fields (No API Call)
Two of three models agree on all fields; dissent is limited to non-critical
fields (any field other than `outcome`, `primary_claim_type`, or `claim_types`).
→ Adopt majority value.

### Tier 2 — Majority Agreement, Critical Fields (No API Call)
Two of three models agree on `outcome`, `primary_claim_type`, or `claim_types`
but one model dissents.
→ Adopt 2-of-3 consensus.

### Tier 3 — Three-Way Split, Non-Critical → Haiku 4.5
All three models return different values for non-critical fields with no majority.
→ Submit to Haiku 4.5 (Batch API) with original case text
  and each model's answer for disputed fields.
→ Haiku determines correct classification using the same controlled vocabulary.

### Tier 4 — Three-Way Split, Critical → Sonnet 4.6
All three models return different values for `outcome`, `primary_claim_type`,
or `claim_types`.
→ Submit to Sonnet 4.6 (Batch API) with original case text
  and each model's answer.
→ Sonnet also re-extracts four free-text narrative fields fresh from source.

## Critical vs. Non-Critical Fields

**Critical fields** (require Tier 4 / Sonnet adjudication if no majority):
- `outcome`
- `primary_claim_type`
- `claim_types`

**Non-critical fields** (Tier 3 / Haiku adjudication sufficient):
- All other categorical fields (accommodation_type, defendant_type,
  disability_category, plaintiff_type, housing_type, procedural_posture, etc.)

## Free-Text Field Resolution

For narrative fields (`key_holding`, `brief_summary`, `accommodation_description`,
`key_cases_cited`):
- Tier 4 records: Sonnet re-extracts from source text
- All other records: MiniMax M2.7 version adopted (most detailed extractions)

## Output Files

- **Unified database** (`FHA_RA_Database_unified_[timestamp].json`):
  Canonical fields only + resolution metadata. ~27 fields/record.

- **Audit database** (`FHA_RA_Database_audit_[timestamp].json`):
  All three model-specific values (suffixed `_minmax`, `_deepseek`, `_kimi`)
  + canonical values + adjudication reasoning. ~91 fields/record.

## Implementation

The consensus resolution logic is implemented in:
- Java — the as-run classes are retained in the project's private research records (non-buildable, credential-redacted inspection copies); this document is the authoritative specification:
  - `OpenRouterConfirmationClient.java` — multi-model classification driver (OpenRouter API integration)
  - `OpusDisagreementResolver.java` — adjudication dispatch
- Python — [`scripts/build_unified_db.py`](../../scripts/build_unified_db.py): merge and consensus resolution into the unified database.
- The resolution algorithm itself is specified in full in this document.

## Mechanism-Family Classification — Separate Majority-Vote Layer

The tiered algorithm above governs the **general-pipeline categorical fields**
(`outcome`, `primary_claim_type`, `claim_types`, and the non-critical bucket).
**Mechanism-family classification** — the four-bucket taxonomy (TRANSLATION /
PROCEDURAL_GATEWAY / NO_FAILURE / OTHER) used for the pleading-loss analysis in
Note footnote 48 — is produced by a **separate three-model ensemble with its
own majority-vote rule**, not by the tiered Haiku/Sonnet adjudication described
above.

### Primary mechanism-family ensemble (N = 676 pleading-loss cases)

Three separately run coders are run on each case:
- **Kimi K2.6**
- **GLM-5.1**
- **DeepSeek V3.2**

### Majority-vote resolution

- **Unanimous (3/3)**: 424 cases → adopt unanimous label.
- **Majority (2/3)**: 235 cases → adopt 2-of-3 label.
- **Three-way split (1/1/1)**: 9 cases → coerce to OTHER (no adjudicator call;
  ensemble output is the canonical primary label and dissent is logged in the
  audit artifact).
- **Unparseable output from any primary coder**: 8 cases dropped from the
  coded universe (668 cases are carried forward into the mechanism-family
  analysis out of the 676-case pleading-loss universe).

No Haiku/Sonnet adjudication is invoked for mechanism-family classification.
The majority-vote rule above is deterministic given the three model outputs.

### Inter-rater reliability

Fleiss' κ across the three primary coders on the 668-case coded universe =
**0.6292** (0.61-0.80 band of the Landis & Koch scale).

### Validation layers sitting outside the primary ensemble

- **Blind Claude Opus 4.7 fourth-coder re-read** on all 668 cases
  (Cohen's κ = 0.6024 vs. primary ensemble majority label; TRANSLATION-family
  gap under Opus 4.7 alone ≈ 29.24 pp).
- **Backward-compatibility against an earlier two-model K2.5 + GLM-5.1 coding** on the
  original 676-case universe (κ = 0.574; alternate split 47.3% / 15.4% / 31.9 pp on
  676), confirming directional stability across coding pipelines.
- **Opus-4.7-as-resolver sensitivity** — replacing the majority-vote rule with
  Opus 4.7 as tiebreaker on disputed cases (κ = 0.80 vs. primary ensemble;
  gap = 29.24 pp; p = 2.45 × 10⁻⁷).

Artifacts: [`validation_three_model/ensemble_results.json`](../validation_three_model/ensemble_results.json)
and [`validation_three_model/ensemble_report.md`](../validation_three_model/ensemble_report.md)
for the primary ensemble; [`validation_four_coder_full/best3_ensemble_results.json`](../validation_four_coder_full/best3_ensemble_results.json)
for the Opus-4.7 fourth-coder re-read.
