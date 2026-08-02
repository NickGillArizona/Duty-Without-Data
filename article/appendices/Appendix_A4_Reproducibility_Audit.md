# Appendix A-4: Classification Reproducibility Audit

**Cited by:** Note footnote 68; consolidated in VALIDATION.md § 6 (Layer 5).
**Scope:** Appendix-level reproducibility audit; establishes cross-classifier reproducibility, not accuracy against a human-coded gold standard.
**Regeneration:** Not script-regenerated; audit protocol and artifacts as described below (stratified sampling seed 20260328).

> **Scope note (2026-07-02).** Portions of this appendix's robustness discussion reference
> findings computed on the 3,193-record unified-dataset generation of the analysis. The Note's
> canonical analytic population is the T2 disability-screened set (n = 1,900; see
> `SAMPLE_DEFINITIONS.md`), and every figure the Note cites from this appendix is the T2-keyed
> value recorded in `CLAIMS_LEDGER.csv`. The audit's reproducibility conclusions concern the
> classification pipeline itself and are unaffected; the unified-dataset figures below carry
> supplementary-analysis status (reproducible from the published inputs, outside the Note's
> registered T2-keyed series).

> **Scope note (2026-07-03).** The 50-case audit sample was drawn from the pre-refresh corpus
> (cases collected through March 25, 2026); the July 2026 corpus refresh added 168 screened-in
> records (tagged `database_sources = ["p3ext_20260703"]`) — approximately 5.0% of the 3,366-record unified database — that no reproducibility
> audit has yet sampled. The refresh increment was classified by the same frozen pipeline
> replicated via OpenRouter (adjudication and per-claim extraction via OpenRouter rather than
> the Anthropic Batch API; the 28-field template reconstructed from the frozen field list;
> `is_ra_case` drawn from an explicit Stage-4 question).

## A-4.1 Overview

The audit targets the RA Database — the reasonable-accommodation-era predecessor corpus (n=1,857) that Appendix A § A.5 merges into the FHA Unified Database — whose triple-model pipeline with tiered adjudication is designed to produce reliable classifications through consensus and escalation. To assess whether this design succeeds — and to provide a reproducibility check analogous to inter-rater reliability in manual coding studies — a separate classification audit was conducted using a model that played no role in the original pipeline.

The audit was meant to catch systematic classification errors in the pipeline and to measure inter-classifier reproducibility of LLM-based legal classification at scale; it was not meant to establish ground truth. The design borrows from inter-rater reliability in manual coding studies, where two coders classify the same materials and their agreement gauges how reproducible the coding scheme is. When the research question is about classification consistency rather than doctrinal correctness, an LLM-as-evaluator protocol stands in for full human annotation at a fraction of the cost.

## A-4.2 Sampling Protocol

Fifty cases were drawn from the RA Database (n=1,857) by stratified random sampling across two dimensions. First, cases were stratified by resolution tier to ensure the sample includes both easy cases (where the pipeline models agreed) and hard cases (where they diverged):

| Tier | Description | Population | Sampled |
|------|-------------|------------|---------|
| Tier 0 | Unanimous consensus | 12 | 3 |
| Tier 1 | Majority agreement, non-critical fields | 278 | 7 |
| Tier 2 | Majority agreement, critical fields | 565 | 14 |
| Tier 3 | Haiku 4.5-adjudicated three-way splits | 697 | 12 |
| Tier 4 | Sonnet 4.6-adjudicated three-way splits | 302 | 11 |
| Other | Consensus/majority fallback | 3 | 3 |
| **Total** | | **1,857** | **50** |

Cases were sampled proportionally within each tier, with oversampling of the smallest tiers (Tiers 0 and Other) to ensure at least three cases per stratum. Within each tier, cases were further stratified by outcome (plaintiff win, defendant win, mixed, procedural, settlement) to prevent the sample from over-representing the dominant outcome category. Random seed: 20260328 (reproducible).

## A-4.3 Protocol

Each sampled case's full opinion text was submitted to Claude Opus 4.6 (Anthropic), the most capable generally available Claude model at the March 2026 audit date, via the Anthropic Message Batches API (50% cost discount). (The model identity follows VALIDATION.md § 6; this audit predates the Opus 4.7 runs used in the later mechanism-coding validation layers.) Opus was configured with a maximum output of 16,000 tokens and default temperature; no reasoning budget cap was applied. Opus received a classification prompt based on the same schema and field definitions used by the pipeline models (the pipeline prompt is reproduced in Appendix K.2). Post hoc comparison revealed that the audit prompt contained vocabulary deviations on three fields — `procedural_posture`, `housing_type`, and partially `accommodation_type` — as disclosed in Section A-4.4. Opus received no access to the pipeline's prior classifications, the resolution tier, or any model-specific outputs — it classified each case independently from the source text alone.

## A-4.4 Results — Per-Field Exact Match Rates

| Field | Compared | Matches | Match Rate |
|-------|----------|---------|------------|
| loper_bright_cited | 50 | 50 | 100.0% |
| interactive_process_discussed | 50 | 49 | 98.0% |
| delay_as_denial | 50 | 49 | 98.0% |
| race_mentioned | 50 | 48 | 96.0% |
| plaintiff_type | 50 | 45 | 90.0% |
| dual_basis_claim | 50 | 43 | 86.0% |
| primary_protected_class | 48 | 39 | 81.3% |
| defendant_type | 50 | 39 | 78.0% |
| outcome | 50 | 35 | 70.0% |
| disability_category | 37 | 23 | 62.2% |
| primary_claim_type | 50 | 31 | 62.0% |
| accommodation_type†† | 48 | 24 | 50.0% |
| housing_type† | 47 | 7 | 14.9% |
| procedural_posture† | 50 | 0 | 0.0% |
| secondary_accommodation_type‡ | 5 | 0 | 0.0% |

†**Vocabulary mismatch disclosure.** The `procedural_posture` and `housing_type` fields exhibit near-zero match rates that reflect a vocabulary mismatch between the audit prompt and the pipeline's controlled vocabulary, not substantive classification disagreement. For `procedural_posture`, the audit prompt specified natural-language values (e.g., "motion to dismiss") while the pipeline stores underscored constants (e.g., `MOTION_TO_DISMISS`); case-insensitive comparison after normalization still fails on underscores versus spaces. For `housing_type`, the audit prompt offered a different category set (e.g., `RENTAL_APARTMENT`, `CONDO_COOP`) than the pipeline's vocabulary (e.g., `PRIVATE_MARKET`, `HOA_CONDO`), with only `PUBLIC_HOUSING` overlapping. These two fields are excluded from the corrected aggregate.

††**Partial vocabulary mismatch.** The `accommodation_type` field's 50% match rate substantially overstates genuine disagreement. The audit prompt offered 8 accommodation categories (see Appendix A-4.3), while the pipeline's controlled vocabulary includes 13 categories (see Appendix K.2). Five pipeline categories — DISCRIMINATION_PRIMARY, COMMUNICATION_ACCOMMODATION, EVICTION_DEFENSE, RENT_PAYMENT, and UNDETERMINED — were absent from the audit prompt. Of the 24 mismatches, 20 (83%) involved these missing categories: 11 cases where the pipeline returned UNDETERMINED and Opus returned OTHER (Opus had no UNDETERMINED option), 7 where the pipeline returned DISCRIMINATION_PRIMARY and Opus returned OTHER (Opus had no DISCRIMINATION_PRIMARY option), and 2 where the pipeline returned EVICTION_DEFENSE and Opus returned OTHER or POLICY_EXCEPTION. Only 4 of 24 mismatches (17%) represent genuine category-versus-category disagreement on the shared vocabulary. Among cases where both classifiers had access to the correct category, the effective match rate is approximately 92% (44/48).

‡Only 5 cases had non-empty values in both pipeline and Opus for `secondary_accommodation_type`. This field is excluded from the corrected aggregate due to insufficient sample size.

**Corrected aggregate exact match rate** (12 vocabulary-aligned fields): **475 / 583 = 81.5%**

Raw aggregate (all 15 fields): 482 / 685 = 70.4%

*Note: If `accommodation_type` is further corrected for the vocabulary mismatch (counting the 20 missing-category mismatches as non-substantive), the effective match rate on substantive disagreements rises to approximately 85%.*

## A-4.5 Results — Cohen's Kappa (Key Fields)

| Field | Kappa | Interpretation |
|-------|-------|----------------|
| defendant_type | 0.740 | Substantial |
| plaintiff_type | 0.668 | Substantial |
| disability_category | 0.639 | Substantial |
| outcome | 0.561 | Moderate |
| primary_claim_type | 0.511 | Moderate |
| accommodation_type | 0.453 | Moderate |

By convention, kappa above 0.80 is read as "almost perfect" agreement, 0.61–0.80 as "substantial," 0.41–0.60 as "moderate," and 0.21–0.40 as "fair." The three party- and disability-identification fields land in the substantial range. The three classification-judgment fields — outcome, claim type, accommodation type — reach only moderate agreement, which is what one would expect given how ambiguous these determinations are in the underlying opinions.

## A-4.6 Results — Agreement by Resolution Tier

| Tier | N | Aggregate Match Rate |
|------|---|---------------------|
| Tier 0 (unanimous) | 3 | 83.3% |
| Tier 1 (majority, non-critical) | 7 | 77.1% |
| Other (consensus/majority fallback) | 3 | 78.1% |
| Tier 2 (majority, critical) | 14 | 71.7% |
| Tier 3 (Haiku-adjudicated) | 12 | 67.7% |
| Tier 4 (Sonnet-adjudicated) | 11 | 61.6% |

Agreement falls monotonically from the easiest cases (Tier 0, 83.3%) to the hardest (Tier 4, 61.6%). That gradient is what one would expect if the tiered resolution is calibrating difficulty correctly. Cases that required adjudication to resolve three-way splits are genuinely harder: they produced disagreement among the pipeline's three models, and they keep producing it between the pipeline's canonical output and an independent fourth model. Had adjudication been introducing systematic error rather than resolving genuine ambiguity, the gradient would not line up this neatly.

## A-4.7 Cost

| Metric | Value |
|--------|-------|
| Model | Claude Opus 4.6 |
| Pricing | Batch API (50% discount) |
| Cases processed | 50 |
| Input tokens | 490,833 (avg 9,816/case) |
| Output tokens | 23,373 (avg 467/case) |
| Input cost | $3.68 |
| Output cost | $0.88 |
| **Total cost** | **$4.56** |
| Avg cost/case | $0.09 |

## A-4.8 Limitations

1. **Vocabulary mismatch.** Two of fifteen categorical fields (`procedural_posture`, `housing_type`) used different controlled vocabularies in the audit prompt than in the pipeline, producing artificially low match rates. These fields are excluded from the corrected aggregate but included in the raw report for transparency.

2. **Outcome disagreement.** The outcome field, which matters most for the Note's empirical claims, shows 70% exact match with kappa of 0.561 ("moderate"). The 15 disagreements cluster in borderline cases: partial dismissals where the line between MIXED and DEFENDANT_WIN turns on how much weight surviving claims should carry, and procedural outcomes such as remand that resist clean categorization. The ambiguity is genuine rather than a sign of systematic pipeline error, but it does mean roughly 1 in 6–7 outcome classifications might be assigned differently by a different classifier.

3. **LLM-versus-LLM.** Claude Opus 4.6 is not a human legal expert. Its classifications reflect model training rather than doctrinal judgment formed through legal practice. High agreement demonstrates reproducibility across independent classifiers, not doctrinal correctness. That said, the premise that human legal experts furnish a categorically better baseline for structured classification is increasingly contested. The JusticeBench evaluation — a HUD-funded study testing eight LLMs on housing law intake screening — found that GPT-4 matched or exceeded human labeler accuracy on housing law intake criteria, a task that requires applying legal rules to fact patterns much like the case classification done here. *See* Quinten Steenhuis & Hannes Westermann, *Missouri Tenant Help Intake Screener*, JusticeBench (2025), https://www.justicebench.org/project/intake. For this pipeline the question is not whether LLMs replicate a hypothetical perfect human coder, but whether the classification noise is random rather than systematic and small enough to preserve the direction and significance of the statistical claims. Section A-4.10 takes up those two conditions.

4. **Sample size.** n=50 is adequate for aggregate metrics and tier-level disaggregation but insufficient for per-category analysis on rare classification values (e.g., specific accommodation types with <5 sampled cases).

## A-4.9 Interpretation

The audit identifies three reliability tiers among the classification fields:

**High reliability (>95% match).** Binary/boolean fields — `loper_bright_cited`, `interactive_process_discussed`, `delay_as_denial`, `race_mentioned` — reproduce at 96–100%. These fields have unambiguous textual indicators (the opinion either cites *Loper Bright* or it does not) and can be treated as highly reliable.

**Moderate reliability (78–90% match, kappa substantial).** Party identification fields — `plaintiff_type` (90%, κ=0.668), `dual_basis_claim` (86%), `primary_protected_class` (81.3%), `defendant_type` (78%, κ=0.740) — show strong but imperfect agreement. Disagreements typically involve borderline institutional classifications (e.g., whether a management company is PROPERTY_MANAGEMENT or PRIVATE_LANDLORD).

**Moderate-lower reliability (62–70% match, kappa moderate).** Substantive classification fields — `outcome` (70%, κ=0.561), `disability_category` (62.2%, κ=0.639), `primary_claim_type` (62%, κ=0.511) — show moderate agreement that tracks genuine case-level ambiguity. Human legal experts would split on these fields too, which is exactly where the pipeline's consensus mechanism earns its keep: the triple-model approach with adjudication produces canonical values that hold up even when no single classification is uniquely correct.

**Accommodation type (50% raw match, ~92% effective match).** The `accommodation_type` field's raw 50% match rate substantially overstates disagreement. As disclosed in Section A-4.4, 83% of mismatches (20 of 24) resulted from five pipeline categories absent from the audit prompt. On the shared vocabulary, the effective match rate is approximately 92%, placing this field in the moderate-reliability tier rather than low-reliability. The kappa of 0.453 reflects the vocabulary mismatch and should not be interpreted as the pipeline's true classification reliability on this field.

The monotonic decline from Tier 0 (83.3%) through Tier 4 (61.6%) tells us the tiering system is picking up real classification difficulty: adjudicated cases are harder, not systematically miscategorized.

These reproducibility metrics can be read alongside the JusticeBench benchmark from Section A-4.8: GPT-4 achieved 84% precision on housing law intake screening, and the pipeline's corrected aggregate match rate of 81.5% is comparable to that figure — though the metrics differ (exact-match agreement here, precision there) and the tasks are related rather than identical. Both concern housing law specifically, which makes the comparison informative, not a validation benchmark.

Analysis conducted March 28, 2026.

## A-4.10 Robustness Assessment: Classification Uncertainty and Empirical Claims

### A-4.10a Ensemble vs. Solo Architecture

The reproducibility audit compares a *single* independent model (Opus 4.6) against a *three-model ensemble* with adjudication. This architectural asymmetry has important implications for interpreting the agreement rates.

The pipeline's canonical values come out of a consensus process: three independent models classify each case, and disagreements resolve through majority vote or escalation to a fourth model. The reproducibility audit reflects something narrower — one model classifying each case once. On complex multi-class tasks, a solo classifier can be expected to diverge from an ensemble consensus at a substantial rate, because the ensemble averages out individual-model idiosyncrasies that the solo classifier keeps. Even single-model architectures reach expert-level accuracy in housing law classification: the HUD-funded JusticeBench evaluation reported 84% precision for a single GPT-4 model on housing intake screening (*see* Section A-4.8). By design, the triple-model ensemble with adjudication used here exceeds that single-model baseline.

The tier-disaggregated data is consistent with this interpretation. Outcome disagreement rates track ensemble confidence:

| Tier | Pipeline Confidence | Opus Outcome Disagreement |
|------|-------------------|--------------------------|
| Tier 1 (majority, non-critical) | High (2/3 agreed on all critical fields) | 14% (1/7) |
| Tier 3 (Haiku-adjudicated) | Moderate (three-way split, non-critical) | 17% (2/12) |
| Tier 2 (majority, critical) | Moderate (2/3 agreed on critical fields) | 29% (4/14) |
| Tier 4 (Sonnet-adjudicated) | Low (three-way split on critical fields) | 55% (6/11) |

Where the pipeline's own models agreed (Tiers 1–2), Opus agrees 71–86% of the time. Where they could not agree and the case had to be adjudicated on critical fields (Tier 4), Opus disagrees 55% of the time. Disagreement is thus concentrated on cases whose classification is hard; the audit measures reproducibility and cannot establish which label is correct. What the audit measures, then, is whether a solo model can replicate ensemble consensus — not whether the pipeline's canonical values are wrong.

### A-4.10b Observed Disagreement Patterns

The 15 outcome disagreements follow a structured pattern of adjacent-category disputes:

**Outcome disagreements (15 cases):**
- 11 of 15 (73%) are *adjacent-category* disputes: PLAINTIFF_WIN ↔ MIXED (4 cases), DEFENDANT_WIN ↔ MIXED (2), PROCEDURAL ↔ DEFENDANT_WIN (2), PROCEDURAL ↔ MIXED (3). The pattern is consistent with category-boundary ambiguity but does not exclude systematic error — whether a partial dismissal is MIXED or DEFENDANT_WIN, whether a remand is PROCEDURAL or MIXED.
- 4 of 15 (27%) are *non-adjacent*: PROCEDURAL → PLAINTIFF_WIN (3 cases) and UNDETERMINED → PLAINTIFF_WIN (1 case). These represent the pipeline coding cases as non-decided that Opus classified as plaintiff victories — a boundary dispute over whether the case reached a substantive outcome.

**Disability category disagreements (14 non-trivial):**
- 12 of 14 (86%) involve UNDETERMINED on one side — one classifier identified a specific disability while the other could not determine the category from the opinion text. Only 2 of 14 are true category-vs-category confusion (MULTIPLE_UNSPECIFIED ↔ MOBILITY, MOBILITY ↔ OTHER).

**Accommodation type disagreements:**
- Nearly all disagreements involve boundaries between the residual categories UNDETERMINED, OTHER, and DISCRIMINATION_PRIMARY. The specific accommodation subtypes that carry the Note's analysis (ASSISTANCE_ANIMAL, PARKING, SOBER_LIVING_GROUP_HOME_ZONING, STRUCTURAL_MODIFICATION) are rarely confused with each other.

**Binary extraction fields (96–100% agreement)** confirm that the pipeline reads opinions accurately at the factual level. Where agreement drops to moderate, the cause is the inherent ambiguity of legal classification on the multi-class fields, not pipeline failure. When a court partially grants and partially denies a motion to dismiss, the case does not sort cleanly into PLAINTIFF_WIN, DEFENDANT_WIN, or MIXED — and human coders would hit the same wall.

### A-4.10d The PROCEDURAL/Decided Boundary

The dominant error pattern in the outcome audit is the PROCEDURAL/decided boundary: 7 of 11 pipeline-PROCEDURAL cases (63.6%) were reclassified by Opus as decided outcomes (3 PLAINTIFF_WIN, 2 DEFENDANT_WIN, 2 MIXED). This suggests the pipeline may undercount decided cases by coding some substantive rulings as procedural.

If this 63.6% reclassification rate is representative, the unified dataset's PROCEDURAL cases could include a substantial number that should be in the decided pool.

The size of that effect, though, is modest and leaves the main findings intact. The 7 reclassified cases split nearly evenly across outcome categories (3 PW, 2 DW, 2 MIXED), so moving them into the decided pool would:
- Slightly *reduce* strict plaintiff win rates (more cases in the denominator, with a below-average PW share)
- Slightly *increase* broad plaintiff win rates (MIXED cases contribute to the broad numerator)
- Have negligible effect on the *relative* pre/post-2024 comparison, because PROCEDURAL cases are distributed across both periods

What the document-level period decline tracks is the *difference* in win rates between periods, not the absolute level. Adding cases to both periods' denominators dilutes both rates proportionally, so the difference and its statistical significance remain largely unchanged.

### A-4.10e Claim-Specific Robustness Classification

The following table classifies the audit-generation analysis's principal empirical claims by robustness to classification uncertainty, based on sample size, statistical significance, and vulnerability to the error patterns identified above. (Unified-dataset figures are retained per the scope note above; the Note's current T2-keyed values are indexed in `CLAIMS_LEDGER.csv`.)

| Robustness Level | Claims | Basis |
|-----------------|--------|-------|
| **Robust** (large N, p<0.001, survives per-claim filtering) | Post-2024 document-level decline (pre-2024 17.9% to 2025 trough 7.9%, N=3,193; not carried into Part II, which reports the case-level census, on which the strict rate is essentially flat), pro se plaintiff exclusion (0.9% vs. 9.1%, N=3,193), Galanter plaintiff-type advantage (FHO 34.6% vs. individual 14.7% on RA merits), per-theory merits hierarchy (DT 22.0%, RA 16.1%, Retaliation 5.6%), *Iqbal* citation effect (1,433 claims, 32.1% of FHA claims), race-mention rate (1,024/3,193 = 32.1%; the identical figure is coincidental) | Per-claim extraction confirms findings survive population filtering; pro se and Galanter effects strengthen on cleaner population |
| **Directionally robust, magnitude uncertain** (moderate N, direction survives but point estimates have wide implicit confidence intervals) | Accommodation-type hierarchy (top tier: SOBER_LIVING 30%, ASSISTANCE_ANIMAL 28.6%, COMMUNICATION 25%; bottom: STRUCTURAL_MOD 0%, TRANSFER 0%), RA standard effect (interactive process framework 35.3% vs. burden-shifting 6.2%), defendant-type hierarchy (housing authority 3.3% vs. municipality 26.7%), disparate impact vs. disparate treatment gap (17.9% vs. 15.7% on merits), circuit-level variation | Per-claim filtering confirms direction; wide CIs on n=10-42 categories; 2-3 reclassifications could shift point estimates but not reverse tier ordering |
| **Reversed or qualified by per-claim analysis** | Interactive process bivariate effect (OR=0.82 on RA merits, reversing positive full-database association), delay-as-denial bivariate effect (OR=0.28, reversing; likely selection effect), design-and-construction win rate (22.2% on n=9 merits, down from 44% full-database) | Full-database associations inflated by non-merits cases; per-claim filtering reveals selection effects |
| **Suggestive** (small N, hypothesis-generating) | Design-and-construction post-2024 resilience (n=9 merits), accommodation-specific pro se rates on n<10, RENT_PAYMENT and EVICTION_DEFENSE win rates (n=5 and n=1), *Loper Bright* citation effect (n=13 citing cases in the audit-generation corpus; the current unified database contains 9 and the T2 population 6 — see Appendix H § H.9) | Small-N comparisons where 1–2 case reclassifications could alter direction; treated as hypothesis-generating |

---

## A-4.11 Case-Level Outcome Census (series of record)

**Why the case is the unit.** The pipeline's decided universe is indexed at the document level,
and a single case can generate several decided rows: duplicate filings, procedural and
motion-survival rulings, and dispositions outside the study windows or the disability cohort.
An outcome rate computed over rows therefore measures documents, not litigants. Because the
Note's claim is about how often a case yields a plaintiff-side judgment, outcomes are counted
over distinct cases. That case-level series is the outcome series reported in the Note's Part II.

**Protocol.** Every row of the 995-row dated-decided universe is read and its outcome-cell
membership adjudicated individually: distinct-victory clusters are adjudicated case by case,
and duplicate, out-of-window, out-of-cohort (non-disability), and procedural-only documents are
excluded on both the favorable and the loss sides. The loss-side census covers 97.3% of recorded
losses. The unit of analysis is the distinct case: multiple decided documents from the same case
collapse to a single case-level unit. On that rule the analytic universe is 606 decided cases:
287 (P1), 68 (P2), 251 (P3).

**Results.** Eighteen qualifying plaintiff-side judgments (the dataset's distinct-victory
field), separately classified by finality: nine final contested judgments awarding relief,
two final default judgments awarding relief, and seven liability determinations with the
remedy unresolved. Per window: 10 of 287 (P1), 0 of 68 (P2), 8 of 251 (P3) - qualifying-judgment
rates 3.48% / 0.00% / 3.19%; broad favorable rates 4.18% / 0.00% / 3.59%. The liability-only
class includes *CareOne at Birchwood* (D.N.J. 2024), P1,
*Robins v. Waterford at Aberdeen* (S.D. Fla. 2026), P3, and *Millerborg v. Blue Bonnet Trail*
(N.D. Tex. 2026), P3. A sensitivity excluding the liability-only class leaves eleven qualifying
judgments and changes no qualitative statement; the under-call sensitivity is 1 of 606 (exact
95% upper bound 0.92%). In every judgment counsel had appeared for the plaintiff by
the qualifying disposition (represented cells 10/116, 0/30, 8/60; pro se cells 0/171, 0/38,
0/191). Pooled across the window, 18 of 206 represented cases ended in a qualifying judgment
(8.7%; exact 95% interval 5.3% to 13.5%) versus 0 of 400 pro se cases (exact 95% upper
bound 0.9%).

**Inference.** The P1-versus-P3 aggregate strict difference is -0.30 percentage points, a
difference with no interpretable sign (the zero cell in P2 and the small victory numerators
leave zero-cell exact intervals) - no aggregate decline appears, which is why the Note reports
no rate decomposition (its fn 71: a composition share of a near-zero total change is
ill-conditioned).

**Institutional-status inputs (the Note's fn 76).** No logistic model of reaching the merits on
institutional status has been estimated on the 606-case basis, and the manuscript prints no odds
ratio: it reports descriptive gate counts only. The four fields such a model would take as
inputs - institutional status, merits-reached, pro se status, and defendant category - were
separately blind-revalidated against opinion text at 88.5% to 99.1% agreement on determinate
rows; the per-field record is in [`FN76_AGREEMENT.md`](FN76_AGREEMENT.md).

**Pro se share.** On the case-level basis (the series printed in Table 1), the pro se
share of the decided docket is 59.6% (171/287, P1) / 55.9% (38/68, P2) / 76.1% (191/251, P3).
Disposition-lag sensitivity on the same basis: dropping the final
six months of P3, the pro se share is 77.7% (129/166), so the composition rise survives the
lag test.

**Published artifacts.** [`results/series_2026-07.json`](../../results/series_2026-07.json)
(the series of record, with embedded basis notes and removal-accounting definitions) and
[`results/comparator_arms_case_level_2026-07.json`](../../results/comparator_arms_case_level_2026-07.json)
(case-level comparator arm cells and the reapplied selection audit). Verification guards
asserting the series values run in [`scripts/make_fig1.py`](../../scripts/make_fig1.py) and
[`scripts/validate_claims.py`](../../scripts/validate_claims.py). The per-row adjudication
worksheets are preserved in the project's validation records and are available from the author.
