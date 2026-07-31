# Reanalysis: K2.6 + GLM-5.1 + DeepSeek V3.2 with Opus 4.7 as the immediate consensus resolver

Universe size: **668** cases (same 668 as the three-model ensemble report; the 8 unparseable cases remain outside this resolver universe because Opus was only given cases the three coders could classify).

Resolution distribution among the three coders: **unanimous 424 / majority 235 / split 9**.

Non-unanimous cases: **244**. Of these, Opus 4.7's bucket diverges from the majority-vote rule on **88** (36.07%).


## Headline — TRANSLATION gap under each coding rule

| Coding | Pro se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | χ²(1) | p | 95% CI on gap |
| --- | --- | --- | --- | --- | --- | --- |
| Original (K2.5 + GLM-5.1) | 47.74% (275/576) | 15.38% (14/91) | 32.36 | 32.2052 | 1.39e-08 | [23.9, 40.82] |
| Majority-vote ensemble (split→OTHER) | 46.35% (267/576) | 14.29% (13/91) | 32.06 | 31.8765 | 1.64e-08 | [23.81, 40.33] |
| **Opus 4.7 as resolver (K2.6+GLM+DS unanimous, else Opus)** | 44.62% (257/576) | 15.38% (14/91) | 29.24 | 26.6423 | 2.45e-07 | [20.78, 37.69] |
| Opus 4.7 alone (fourth coder) | 44.62% (257/576) | 15.38% (14/91) | 29.24 | 26.6423 | 2.45e-07 | [20.78, 37.69] |
| Kimi K2.6 solo | 50.87% (293/576) | 23.08% (21/91) | 27.79 | 23.2585 | 1.42e-06 | [18.22, 37.36] |
| GLM-5.1 solo | 46.18% (266/576) | 17.58% (16/91) | 28.6 | 25.1775 | 5.23e-07 | [19.78, 37.42] |
| DeepSeek V3.2 solo | 38.19% (220/576) | 17.58% (16/91) | 20.61 | 13.7154 | 2.13e-04 | [11.84, 29.38] |

Pro se sample n = 576; represented sample n = 91.

## Family-level contingency (representation × mechanism family)

| Coding | χ² | df | p | Cramér's V | Families observed |
| --- | --- | --- | --- | --- | --- |
| Original (K2.5 + GLM-5.1) | 61.9553 | 7 | 6.20e-11 | 0.3048 | 8 |
| Majority-vote ensemble | 68.4902 | 8 | 1.04e-11 | 0.3318 | 9 |
| **Opus 4.7 as resolver** | 60.9842 | 9 | 8.66e-10 | 0.3024 | 10 |
| Opus 4.7 alone | 79.862 | 9 | 5.39e-13 | 0.346 | 10 |

The Note's footnote 48 reports χ²(8) = 68.49, p = 1.04 × 10⁻¹¹, Cramér's V = 0.33 on the majority-vote ensemble (row 2 of the table above) on the 668-case subset covered by all three primary coders. An earlier two-model K2.5 + GLM-5.1 coding on the full 676-case universe returned χ²(8) = 33.23, p = 5.6 × 10⁻⁵, Cramér's V = 0.22, kept as a backward-compatibility check. The values in the table above operate on the 668-case subset covered by all four coders (three primary + Opus 4.7 fourth coder).

## Rater reliability — Fleiss' κ across the three primary coders

- Bucket-level Fleiss κ (K2.6, GLM-5.1, DeepSeek V3.2): **0.6292**
- Family-level Fleiss κ: 0.5636

These numbers are identical to the current ensemble report because they describe the three coders' mutual reliability, independent of how ties are resolved.

## Pairwise κ across all coding variants (bucket)

| Comparison | Cohen's κ |
| --- | --- |
| d_bucket vs fourth_bucket | 0.516 |
| d_bucket vs g_bucket | 0.6113 |
| d_bucket vs k_bucket | 0.6466 |
| d_bucket vs maj_bucket | 0.8097 |
| d_bucket vs opus_bucket | 0.7156 |
| d_bucket vs orig_bucket | 0.5011 |
| fourth_bucket vs g_bucket | 0.554 |
| fourth_bucket vs k_bucket | 0.5407 |
| fourth_bucket vs maj_bucket | 0.6024 |
| fourth_bucket vs opus_bucket | 0.7994 |
| fourth_bucket vs orig_bucket | 0.4793 |
| g_bucket vs k_bucket | 0.6348 |
| g_bucket vs maj_bucket | 0.8001 |
| g_bucket vs opus_bucket | 0.755 |
| g_bucket vs orig_bucket | 0.5477 |
| k_bucket vs maj_bucket | 0.8225 |
| k_bucket vs opus_bucket | 0.7414 |
| k_bucket vs orig_bucket | 0.5237 |
| maj_bucket vs opus_bucket | 0.8036 |
| maj_bucket vs orig_bucket | 0.574 |
| opus_bucket vs orig_bucket | 0.5597 |

## Each coder vs. the Opus-4.7 resolver (bucket)

| Coder | Bucket match % | Cohen's κ vs. Opus-resolved |
| --- | --- | --- |
| kimi | 82.63% | 0.7414 |
| glm | 83.53% | 0.755 |
| deepseek | 80.84% | 0.7156 |
| original | 70.51% | 0.5597 |
| majority | 86.83% | 0.8036 |
| fourth_alone | 86.38% | 0.7994 |

## Confusion matrices

### Original (K2.5+GLM) vs. Opus-resolved

| orig \ opus | TRANSLATION | PROCEDURAL_GATEWAY | NO_FAILURE | OTHER |
| --- | --- | --- | --- | --- |
| TRANSLATION | 196 | 14 | 6 | 74 |
| PROCEDURAL_GATEWAY | 9 | 112 | 3 | 8 |
| NO_FAILURE | 0 | 1 | 23 | 2 |
| OTHER | 67 | 12 | 1 | 140 |

### Majority-vote ensemble vs. Opus-resolved

| maj \ opus | TRANSLATION | PROCEDURAL_GATEWAY | NO_FAILURE | OTHER |
| --- | --- | --- | --- | --- |
| TRANSLATION | 241 | 6 | 4 | 30 |
| PROCEDURAL_GATEWAY | 2 | 126 | 2 | 3 |
| NO_FAILURE | 0 | 0 | 24 | 2 |
| OTHER | 29 | 7 | 3 | 189 |

## PROCEDURAL_GATEWAY replay

| Coding | Pro se PG % | Represented PG % | Gap (pp) | χ²(1) | p |
| --- | --- | --- | --- | --- | --- |
| Original | 17.88% | 31.87% | -13.99 | 8.8231 | 2.974e-03 |
| Majority ensemble | 17.88% | 32.97% | -15.09 | 10.2769 | 1.347e-03 |
| **Opus 4.7 as resolver** | 19.27% | 30.77% | -11.5 | 5.6205 | 1.775e-02 |
| Opus 4.7 alone | 18.23% | 27.47% | -9.24 | 3.7101 | 5.408e-02 |

## 150-case stratified audit — under the three-model ensemble

Under the two-model coding, K2.6 re-coded a stratified 150-case sample vs. K2.5+GLM → κ = 0.6264.

Under the three-model ensemble, K2.6 is already one of the three primary coders, so its 150-case re-code is no longer an *external* check. 
For reference, the same K2.6 labels compared against the **Opus-resolved** ensemble on the overlapping subset:

- Overlap with resolver universe: **150 cases**
- Bucket match: 80.67%
- Bucket κ (K2.6 vs. Opus-resolved): **0.7301**
- Family match: 78.67%
- Family κ: 0.7159

A high κ here reflects the self-consistency of K2.6 with a pipeline it is part of, not external validation.

## Summary of what changes

| Metric | Original (K2.5+GLM, n=676) | Majority ensemble (n=668) | **Opus 4.7 resolver (n=668)** |
| --- | --- | --- | --- |
| Pro se TRANSLATION % | 48.3% | 46.35% | **44.62%** |
| Represented TRANSLATION % | 17.9% | 14.29% | **15.38%** |
| Gap (pp) | 30.4 | 32.06 | **29.24** |
| χ²(1) (2×2) | — | 31.8765 | **26.6423** |
| p (2×2) | — | 1.64e-08 | **2.45e-07** |
| χ²(family×representation) | 33.23 (df=8) | 68.4902 (df=8) | **60.9842 (df=9)** |
| Cramér's V | 0.22 | 0.3318 | **0.3024** |
| Fleiss κ across three coders | — | 0.6292 | **0.6292** (same) |
| Validation layer κ (vs. original) | — | 0.574 | κ vs K2.5+GLM: **0.5597** |

