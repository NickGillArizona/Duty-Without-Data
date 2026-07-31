# Kimi K2.6 mechanism-classification validation — agreement report

> **Status of this report.** This 150-case Kimi K2.6 re-classification serves two purposes in the archive: (a) a backward-compatibility κ against an earlier two-model Kimi K2.5 + GLM-5.1 coding (**κ = 0.6264** bucket-level; value is load-bearing for CLAIMS_LEDGER C31), and (b) a self-consistency check showing K2.6 labels on the 150-case subset match the primary three-model ensemble at κ = 0.7301 on that subset (see [`validation_three_model/opus_resolver_report.md`](../validation_three_model/opus_resolver_report.md)). The primary TRANSLATION-family headline cited in the Note is **45.3% pro se / 13.7% represented / 31.6 pp gap** on the merged 728-of-739 pleading-loss universe (July 2026 endpoint extension; see [`VALIDATION.md`](../VALIDATION.md) § 3.2). The three-model anchor that this report's comparisons run against is 46.4% pro se (267/576) / 14.3% represented (13/91) / 32.1 pp (668 of 676 cases; family × representation χ²(8) = 68.49, V = 0.33).

Sample size (successful classifications): **150** of 150 attempted.


## Headline

| Metric | Value |
| --- | --- |
| Family (atomic) exact match | **69.33%** (104/150), kappa = 0.5751 |
| Family bucket {TRANSLATION, PROCEDURAL_GATEWAY, NO_FAILURE, OTHER} | **74.0%** (111/150), kappa = 0.6264 |
| Atomic mechanism code | 41.33% (62/150), kappa = 0.3508 |

## Kappa interpretation

Landis & Koch: < 0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, > 0.80 almost perfect.

The load-bearing metric for the note's TRANSLATION-family claim is **bucket kappa**.

## Agreement by original classifier

| Original model | n | Family exact match | Bucket match | Family kappa | Bucket kappa |
| --- | --- | --- | --- | --- | --- |
| moonshotai/kimi-k2.5 | 112 | 71.43% | 74.11% | 0.6026 | 0.6285 |
| z-ai/glm-5.1 | 38 | 63.16% | 73.68% | 0.4914 | 0.6122 |

Kimi K2.6 is a sibling model of Kimi K2.5 (the classifier used in the original coding pass). If K2.6 agrees with K2.5 materially more than with GLM-5.1, within-family consistency is flagged; cross-model agreement is a stronger independence signal.

## Directional bias check — TRANSLATION share by representation

**Pro se** (n=101): original TRANSLATION = 50.5%, Kimi TRANSLATION = 46.53%, delta = -3.96 pp.
**Represented** (n=49): original TRANSLATION = 28.57%, Kimi TRANSLATION = 18.37%, delta = -10.2 pp.

If the deltas are similar sign and magnitude for pro se and represented, reclassification is roughly unbiased across representation; if they differ materially, the TRANSLATION gap could be partly a coding artifact.

## Replay of the note's TRANSLATION-family headline

| Source | Pro se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | chi2(1df) | p |
| --- | --- | --- | --- | --- | --- |
| Original coding | 50.5% | 28.57% | 21.93 | 5.5961 | 0.018000663097019216 |
| Kimi K2.6 recoding | 46.53% | 18.37% | 28.16 | 10.0172 | 0.0015508278210324316 |

Pro-se - represented gap CI (original): {'diff': 0.2192, 'ci95_low': 0.0595, 'ci95_high': 0.3789, 'se': 0.0815}
Pro-se - represented gap CI (Kimi): {'diff': 0.2817, 'ci95_low': 0.136, 'ci95_high': 0.4273, 'se': 0.0743}

The full-universe figure on the original coding (`48.3% pro se vs 17.9% represented`, 676 cases) is the population comparator; the row above is the sample replay. A survived gap (Kimi gap within ~10 pp of original gap and chi2 significant) indicates the gap is robust to independent re-coding.

## Bucket confusion matrix (original -> Kimi)

| orig \ kimi | TRANSLATION | PROCEDURAL_GATEWAY | NO_FAILURE | OTHER |
| --- | --- | --- | --- | --- |
| TRANSLATION | 44 | 5 | 4 | 12 |
| PROCEDURAL_GATEWAY | 3 | 41 | 1 | 0 |
| NO_FAILURE | 2 | 2 | 10 | 1 |
| OTHER | 7 | 2 | 0 | 16 |

## Disagreements (39 cases)

See agreement_results.json `disagreements` array for the full list. The disagreement set is available to a reader assessing whether the Kimi or the original coding is closer to the opinion's reasoning.

## Decision rule status

**KEEP. Bucket kappa >= 0.60 supports the TRANSLATION claim as-is.**

## Independence caveat

Kimi K2.6 is architecturally related to Kimi K2.5 (the original classifier for 532/676 cases). For a stronger independence check, re-run the same sample with a model from a different provider (e.g., `anthropic/claude-sonnet-4.6` or `google/gemini-3-pro`). The `run_kimi_k2_6.py` script can be generalized by changing MODEL_SLUG; the agreement pipeline here takes the validator's output as an input.

