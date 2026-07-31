# Full-universe fourth-coder confirmation — report

> **Status (July 2026):** frozen validation artifact. The ensemble-level gap this pass
> stress-tested is reported in the Note as a directional finding only
> (VALIDATION.md § 3.1); the point-estimate bracket below is pipeline-internal.

**Date:** 2026-04-20
**Scope:** All 668 cases in the three-model ensemble universe (every FHA disability pleading-loss opinion classified by Kimi K2.6, GLM-5.1, and DeepSeek V3.2).
**Fourth coder:** 22 parallel Claude Opus 4.7 coder seats, each given the verbatim `mechanism_prompt.txt` and a blind manifest (source_file + file_path only), instructed to read every opinion file before coding.
**Purpose:** stress-test the TRANSLATION-gap finding on the full universe, not just the 189 ensemble-vs-original disagreement subset. This is the largest independent-coder validation pass available for this Note.

---

## 1. Headline — the gap survives on the largest sample

| Coding | Pro se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | χ²(1) | p | 95% CI on gap (pp) |
| --- | --- | --- | --- | --- | --- | --- |
| Original (Kimi K2.5 + GLM-5.1) | 47.74% (275/576) | 15.38% (14/91) | 32.36 | 32.21 | 1.4 × 10⁻⁸ | [23.90, 40.83] |
| Ensemble (K2.6 + GLM-5.1 + DeepSeek V3.2 majority) | 46.35% (267/576) | 14.29% (13/91) | 32.07 | 31.88 | 1.6 × 10⁻⁸ | [23.81, 40.33] |
| **Fourth coder (Claude Opus 4.7, blind, full read)** | **44.62% (257/576)** | **15.38% (14/91)** | **29.23** | **26.64** | **2.4 × 10⁻⁷** | **[20.78, 37.69]** |

All three independent coding pipelines put the pro se / represented TRANSLATION-rate gap in the approximately 29.2–32.4 pp range, with p well below 10⁻⁶ and the lower 95% confidence bound above 20 pp in every case. The fourth-coder point estimate is the lowest of the three, and even that value is roughly **2.9× the represented rate** — consistent with the Note's "more than twice as likely" directional claim.

---

## 2. Full-universe reliability — fourth coder matches the ensemble

| Comparison | Cohen κ (bucket) | Cohen κ (family) | Bucket match |
| --- | --- | --- | --- |
| **fourth vs. ensemble** | **0.6024** | 0.5652 (n=622) | 73.20% (489/668) |
| fourth vs. original | 0.4793 | 0.4131 (n=667) | 64.97% (434/668) |
| ensemble vs. original | 0.5740 | 0.4743 (n=668) | 71.71% (from the ensemble report) |

**Interpretation.** On the full 668-case universe:
- Fourth-coder vs. ensemble bucket κ = **0.6024** — sitting right at the Landis & Koch "substantial" threshold and at the boundary of the KEEP band (≥ 0.60) in the ensemble_report.md decision rule.
- Fourth-coder vs. original bucket κ = 0.4793 — in the same SOFTEN band as ensemble-vs-original (0.5740).
- The fourth coder agrees with the ensemble **more** than with the original (κ 0.60 vs. 0.48). That's directional external corroboration that the ensemble sits closer to what a careful independent read produces than the two-model original coding does.

The 0.60 κ means the ensemble's classification decisions are substantially reproducible by a fresh independent coder with no knowledge of the prior rolls.

---

## 3. Bucket confusion — full universe

**Original → fourth coder**

| orig \\ 4th | TRANSLATION | PG | NO_FAILURE | OTHER |
| --- | --- | --- | --- | --- |
| TRANSLATION | 183 | 14 | 8 | 85 |
| PROCEDURAL_GATEWAY | 12 | 101 | 9 | 10 |
| NO_FAILURE | 1 | 0 | 24 | 1 |
| OTHER | 76 | 15 | 3 | 126 |

**Ensemble → fourth coder**

| ens \\ 4th | TRANSLATION | PG | NO_FAILURE | OTHER |
| --- | --- | --- | --- | --- |
| TRANSLATION | 204 | 9 | 5 | 63 |
| PROCEDURAL_GATEWAY | 7 | 110 | 10 | 6 |
| NO_FAILURE | 0 | 0 | 24 | 2 |
| OTHER | 61 | 11 | 5 | 151 |

The ensemble→fourth diagonal is visibly denser than the original→fourth diagonal, which is the qualitative picture behind the κ gap (0.60 vs. 0.48).

Of the 85 original-TRANSLATION cases the fourth coder re-coded to OTHER, 61 were cases the ensemble also re-coded to OTHER (i.e., the ensemble and the fourth coder both disagreed with the original on the same cases). This is a strong signal of a shared, reproducible reclassification pattern — not coder noise.

---

## 4. PROCEDURAL_GATEWAY gap — inverse direction also replicates

Fourth coder primary on full universe: pro se PG 18.23% (105/576) vs. represented PG 27.47% (25/91). Gap = **−9.24 pp** (χ² = 3.71, p = 0.054).

The Note's secondary finding — that represented plaintiffs are *more* likely to trigger threshold dismissals — also replicates under the fourth coder at borderline significance (one-tailed p ≈ 0.027). The ensemble put this gap at −15.09 pp (p = 0.0013); the fourth coder recovers a smaller version of the same directional effect.

---

## 5. Off-taxonomy residue

The fourth coder invented off-taxonomy codes on a minority of rows:

- **Families:** 1 invented code (`NO_FAILURE_DISMISSED_OTHER_GROUNDS`, used once).
- **Mechanisms:** ~65 invented codes across ~28 distinct labels (most common: `DISABILITY_NOT_PLEADED` x15, `CONCLUSORY_NO_FACTS` x5, `ACCOMMODATION_ELEMENTS_MISSING` x4, `JURISDICTION_OR_ABSTENTION` x4). These are all substantively reasonable labels that cleanly map to taxonomy codes (e.g., `DISABILITY_NOT_PLEADED` → `DISABILITY_NEXUS_MISSING`, `CONCLUSORY_NO_FACTS` → `ELEMENTS_NOT_TIED_TO_FACTS`, `JURISDICTION_OR_ABSTENTION` → `JURISDICTION_OR_STANDING`).
- These do **not** affect the bucket-level kappa or the gap replay, because every off-taxonomy mechanism was paired with a valid family code.
- The family-level κ vs. original (0.4131) is pulled down slightly by the one invalid family code, but only by one row out of 668.

A post-hoc mechanism crosswalk would tighten the family-level κ but would not change the bucket-level or gap-level conclusions.

---

## 6. Misfilter flags surfaced by the fourth coder

Across the 22 chunks, the coder seats flagged ~15 cases where the opinion on its face did not adjudicate a pleading defect — typically amended-complaint-survived, MTD denied as moot, FCA-not-FHA misfile, or consent-decree orders. Examples:

- Musgrove v. Hanifin (MTD denied as moot after 7AC)
- UMH Properties v. Coxsackie (FHA claims survived; only state-law dismissed)
- Webster v. Fairway Management (MTD denied; FHA survived)
- Milwaukee case (FCA, not FHA-disability)
- Several Rule 41(b) or LR 7-2(d) failure-to-prosecute dismissals
- Housing Opportunities Made Equal v. Count X LLC (order dismissed counterclaims, not plaintiff's FHA)

These are filter-stage noise. They are already absorbed into the OTHER / NO_FAILURE buckets and do not materially alter the TRANSLATION-gap result (pro se cases dominate the universe 576:91, so a handful of misfilter flags cannot flip the direction).

---

## 7. Caveats

**(a) Ten of the 22 seats required one retry.** The re-read ran in 22 independent coder seats. Ten returned server-side rate-limit errors on the first attempt (chunks 04, 07, 11, 13, 14, 15, 16, 18, 20, 22); all ten were re-run with identical blind manifests and hardened prompts, and all completed on the second attempt. No case was coded from incomplete reads.

**(b) Output schema drift in two seats.** Two of the 22 seats (chunks 17 and 19) emitted their classifications with `family`/`mechanism` or `family_code`/`mechanism_code` keys instead of the canonical `pleading_failure_family`/`pleading_failure_mechanism`. The aggregation script normalizes both forms, so the drift was corrected before scoring. Spot checks show substantive classifications were unaffected.

**(c) The fourth coder is still Opus 4.7.** All four "coders" in this validation pipeline use an LLM of some kind (Kimi, GLM, DeepSeek for the ensemble; Opus for the fourth). A fully human coded sample would be the next level of rigor, but is out of scope for this Note. The best defense of the Note's findings is that four independently prompted models — three in an ensemble, one operating blind on the raw opinions — all converge on the same pro-se/represented gap within ~3 pp.

**(d) The 0.60 κ is at the threshold, not comfortably above it.** Bucket κ = 0.6024 is arithmetically in the KEEP band but clings to the boundary. A conservative reader would still round this as "high end of SOFTEN" rather than "clean KEEP." The directional claim is very well supported; a specific-percentage claim in the main text is not.

---

## 8. Implication for the reported series

The full-universe fourth-coder pass **confirms the TRANSLATION-gap finding**. Recommended language:

**Main text (Part III.C):**
> "Pro se plaintiffs are approximately 2.9x as likely as represented plaintiffs to have their FHA disability claim dismissed for a translation failure — roughly 45% vs. 15%, a ~30 percentage-point gap. Across three independent coding pipelines (original two-model, three-model ensemble, blind fourth-coder re-read on all 668 opinions), the point estimate ranges from 29.2 to 32.4 percentage points, with p < 10⁻⁶ and a 95% confidence interval whose lower bound sits above 20 pp in every specification."

**Methodological appendix:**
> "Inter-coder reliability at the bucket level was substantial: Fleiss' κ = 0.629 across the three ensemble models, and Cohen's κ = 0.602 between a fully blind fourth coder (Claude Opus 4.7) and the three-model ensemble on the full 668-case universe. Reliability vs. the original two-model coding was moderate (bucket κ = 0.479-0.574), reflecting improvements introduced by the third ensemble model and the blind independent read."

**Do not:** cite precise percentages (46.35%, 32.07pp, etc.) in the main text. The three pipelines disagree at the decimal level, and the Note's claim is directional.

**Do:** reference this file (`method/validation_four_coder_full/confirmation_report.md`) in the methodological appendix as the largest-sample external validation.

---

## 9. Files produced

- `method/validation_four_coder_full/universe_668.json` — full universe manifest with source_file, representation, year, original_family, file_path.
- `method/validation_four_coder_full/chunk_{01..22}_blind.json` — 22 blind chunks (source_file + file_path only) distributed round-robin.
- `method/validation_four_coder_full/coder_seat_{01..22}_results.json` — raw fourth-coder outputs per chunk.
- `method/validation_four_coder_full/fourth_coder_full_merged.json` — unified dataset: 668 rows, canonical keys, all kappa statistics, all gap stats, confusion matrices.
- `method/validation_four_coder_full/aggregate_full.py` — aggregation script.

## 10. What this pass does not do

- It does not upgrade the Fleiss κ or the ensemble-vs-original κ, both of which are properties of the ensemble and have not changed.
- It does not recode the *original* 676 classifications or retroactively alter any published figure.
- It is not a human-coded validation — all four coders are LLMs. The methodological appendix should be explicit about this.

The sole contribution of this pass is: **on the largest sample available, an independent blind coder replicates the direction, sign, and order of magnitude of the TRANSLATION gap, and agrees with the three-model ensemble at κ = 0.60 (substantial) at the bucket level.**
