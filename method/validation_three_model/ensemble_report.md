# Three-model ensemble mechanism validation — report

Universe size (cases classified by all three models): **668**.

Models: kimi=kimi_raw_results.json, glm=glm_raw_results.json, deepseek=deepseek_raw_results.json.

Ensemble resolution: unanimous 424 / majority 235 / 3-way split 9.


## Headline: ensemble vs. original coding

| Metric | Value |
| --- | --- |
| Bucket exact match | **71.71%** (479/668) |
| Bucket kappa | **0.574** |
| Atomic family exact match | 60.48% (404/668) |
| Atomic family kappa | 0.4743 |

## Rater reliability (Fleiss' kappa across the three models)

- Bucket-level Fleiss kappa: **0.6292**
- Atomic family Fleiss kappa: 0.5636

Fleiss' kappa aggregates agreement across all three classifiers at once. Higher than 0.60 indicates substantial cross-model agreement independent of any one model.

## Each model vs. original (full 676)

| Model | n | Bucket match | Bucket kappa | Family match | Family kappa |
| --- | --- | --- | --- | --- | --- |
| kimi (kimi) | 668 | 68.41% | 0.5237 | 60.33% | 0.4532 |
| glm (glm) | 668 | 69.91% | 0.5477 | 60.33% | 0.4672 |
| deepseek (deepseek) | 668 | 66.62% | 0.5011 | 54.34% | 0.4095 |

## Each model vs. ensemble consensus

| Model | Bucket match with ensemble | Bucket kappa |
| --- | --- | --- |
| kimi | 88.17% | 0.8225 |
| glm | 86.68% | 0.8001 |
| deepseek | 87.28% | 0.8097 |

A model with meaningfully lower ensemble-agreement than the others is the most likely outlier.

## Pairwise cross-model agreement

| Pair | Bucket match | Bucket kappa |
| --- | --- | --- |
| kimi_vs_glm | 75.6% | 0.6348 |
| kimi_vs_deepseek | 76.05% | 0.6466 |
| glm_vs_deepseek | 73.95% | 0.6113 |

## TRANSLATION-family gap — full universe replay

| Coding | Pro se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | chi2(1df) | p |
| --- | --- | --- | --- | --- | --- |
| Original (Kimi K2.5 + GLM-5.1) | 47.74% | 15.38% | 32.36 | 32.2052 | 1.3871778852114836e-08 |
| **Ensemble (K2.6 + GLM-5.1 + DeepSeek V3.2 majority)** | **46.35%** | **14.29%** | **32.06** | **31.8765** | **1.642957150968543e-08** |
| kimi solo | 50.87% | 23.08% | 27.79 | 23.2585 | 1.4162584537293812e-06 |
| glm solo | 46.18% | 17.58% | 28.6 | 25.1775 | 5.228859338910187e-07 |
| deepseek solo | 38.19% | 17.58% | 20.61 | 13.7154 | 0.00021270658693179004 |

Pro se sample n = 576; represented sample n = 91.
Pro-se - represented gap CI (original): {'diff': 0.3236, 'ci95_low': 0.239, 'ci95_high': 0.4082, 'se': 0.0432}
Pro-se - represented gap CI (ensemble): {'diff': 0.3207, 'ci95_low': 0.2381, 'ci95_high': 0.4033, 'se': 0.0422}

## PROCEDURAL_GATEWAY family gap — full universe replay

| Coding | Pro se PG % | Represented PG % | Gap (pp) | chi2(1df) | p |
| --- | --- | --- | --- | --- | --- |
| Original | 17.88% | 31.87% | -13.99 | 8.8231 | 0.0029744471200681155 |
| Ensemble | 17.88% | 32.97% | -15.09 | 10.2769 | 0.0013470575692721325 |

## Confusion matrix (original bucket -> ensemble bucket)

| orig \ ens | TRANSLATION | PROCEDURAL_GATEWAY | NO_FAILURE | OTHER |
| --- | --- | --- | --- | --- |
| TRANSLATION | 203 | 7 | 3 | 77 |
| PROCEDURAL_GATEWAY | 9 | 113 | 3 | 7 |
| NO_FAILURE | 2 | 3 | 20 | 1 |
| OTHER | 67 | 10 | 0 | 143 |

## Disagreements: 189 cases

See `ensemble_disagreements.json` for full list. Each row includes per-model family labels, so you can see whether the ensemble flipped against the original because all three models converged or because two-of-three did.

## Decision rule status

**SOFTEN. Ensemble bucket kappa vs. original in [0.45, 0.60). Keep directional claim but drop precise percentages from main text.**

