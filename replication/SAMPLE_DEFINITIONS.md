# Sample Definitions

This document is the single source of truth for every population, filter, and denominator used in the Note. Every empirical claim in the manuscript resolves to exactly one of the tiers below.

## 1. Canonical corpus

All analyses operate on `data/FHA_Unified_Database.json` — a unified, deduplicated merge of federal Fair Housing Act opinions retrieved from CourtListener via the Free Law Project API, supplemented with docket metadata harvested through the queries documented in [`DATA_PROVENANCE.md`](DATA_PROVENANCE.md). The corpus endpoint is July 1, 2026; the final CourtListener re-pull was executed July 3, 2026, and the 168 records it added carry two source tags: 133 records carry `database_sources = ["p3ext_20260703"]`, and 35 records — distinct later opinions in cases already in the corpus, restored by a cluster-ID deduplication audit — carry `database_sources = ["p3ext_20260703_r2"]`. A reproduction filtering on the refresh must match BOTH tokens.

## 2. Tier framework

```mermaid
flowchart TB
    T0["T0 — Raw unified corpus<br/>n = 3,366"]
    T1["T1 — FHA-screened<br/>n = 2,690"]
    T2["T2 — Disability-screened (canonical)<br/>n = 1,900"]
    T2N["T2-narrow — Robustness sample<br/>n = 1,849"]
    T3["T3 — Disability wave<br/>(date_filed ≥ 2022-01-01)<br/>n = 1,347"]
    T4["T4 — Pleading-loss universe<br/>n = 739 (736 classified)"]
    T0 -->|screening_result != NO<br/>AND case_name present| T1
    T1 -->|disability_alleged OR<br/>is_ra_case OR<br/>protected_classes ∋ disability| T2
    T1 -.->|protected_classes ∋ disability<br/>(only)| T2N
    T2 --> T3
    T2 --> T4
    style T2 fill:#fff4e0
    style T2N fill:#f0f0f0,stroke-dasharray: 5 5
```

*Text equivalent of the diagram: T0 is the raw unified corpus, n = 3,366. Records with
`screening_result != NO` and a `case_name` present become T1, FHA-screened, n = 2,690.
Records in T1 with `disability_alleged` or `is_ra_case` or `disability` among
`protected_classes` become T2, disability-screened (canonical), n = 1,900. A separate
robustness branch off T1, using `protected_classes` containing `disability` only, gives
T2-narrow, n = 1,849. T2 divides into T3, the disability wave (`date_filed` on or after
2022-01-01), n = 1,347, and T4, the pleading-loss universe, n = 739 (736 classified).*

| Tier | Label | Filter (expressed against record `r`) | n |
|------|-------|---------------------------------------|---|
| T0 | Raw unified corpus | All records in `FHA_Unified_Database.json` | 3,366 |
| T1 | FHA-screened | `r["screening_result"] != "NO"` AND `r["case_name"]` present | 2,690 |
| T2 | Disability-screened (canonical) | T1 AND (`r["disability_alleged"]` OR `r["is_ra_case"]` OR `"disability" ∈ r["protected_classes"]`) | 1,900 |
| T2-narrow | Disability-screened (robustness) | T1 AND `"disability" ∈ [p.lower() for p in r["protected_classes"]]` | 1,849 |
| T3 | Disability wave | T2 AND `r["date_filed"] ≥ "2022-01-01"` | 1,347 |
| T4 | Pleading-loss universe | T2 AND `is_pleading_loss(r) == True` | 739 (736 classified) |

All counts refer to the committed `data/FHA_Unified_Database.json`. `is_pleading_loss` is defined in [`../scripts/pro_se_mechanism_analysis.py`](../scripts/pro_se_mechanism_analysis.py) and captures Rule 12(b)(6), Rule 12(c), Rule 8 / Twombly–Iqbal, and pre-discovery Rule 56 dismissals where the defendant or the court, not the plaintiff, is the dispositive actor. The T4 filter returns 739 database rows; 736 of those were classified for the mechanism-family analysis (three uncoded: one original residual plus two July-2026 refresh rows dropped for unparseable ensemble output), and 728 carry a merged three-model ensemble coding, so ensemble mechanism denominators report 728 (`results/pro_se_mechanism_divergence_results.json` reflects the pre-refresh universe — `screened_disability_pleading_stage_losses_total` = 677, `classified_target_cases` = 676; the July 2026 increment is documented in [`../method/VALIDATION.md`](../method/VALIDATION.md) § 3). T4 is not a subset of the 995 dated-decided universe: it retains undated and pre-2022 pleading losses.

## 3. Dated-decided subsets

Several analyses — particularly the document-level three-period win-rate comparisons and the archived Kitagawa–Oaxaca–Blinder decomposition (not reported in the Note) — require a non-null `date_filed`. The dated-decided subset of T2 is n = 995 and partitions into:

| Period | Window | n (T2 dated-decided) |
|--------|--------|----------------------|
| P1 | 2022-01-01 through 2024-06-27 (pre-*Loper Bright*) | 476 |
| P2 | 2024-06-28 through 2025-02-04 (post-*Loper Bright*, pre-HUD enforcement withdrawal) | 120 |
| P3 | 2025-02-05 onward through the 2026-07-01 corpus endpoint (post-HUD enforcement withdrawal) | 399 |

The T2-narrow dated-decided subset is n = 972 and partitions identically in period assignment; numerical values under both filters are directionally identical.

## 4. Canonical-filter decision rule

The Note and the committed scripts adopt **T2 (disjunctive) as canonical** for every disability-case claim. The decision rule is:

1. `disability_alleged` and `is_ra_case` are fields assigned by the multi-model consensus pipeline on independent grounds from `protected_classes`. An opinion can allege disability discrimination, or involve a § 504 / Rehabilitation Act claim, without the classifier having populated `"disability"` into `protected_classes` — particularly where the opinion pleads accommodation facts without explicit statutory framing.
2. Omitting either flag would systematically drop cases that the Note treats as disability cases — and that any reasonable federal judge would treat as disability cases under the FHA or § 504.
3. Consequently, T2-narrow (`"disability" ∈ protected_classes` alone) under-counts disability litigation by 51 opinions (≈ 2.7% of T2 canonical) and under-counts the dated-decided subset by 23 opinions (≈ 2.4%). The under-count is not uniform across periods but the period-relative pattern is stable.

To guard against the concern that the canonical filter is selected to produce a larger denominator, every headline statistic is also reported under T2-narrow as a robustness read. Where the two filters disagree on direction, the Note flags it. Where they converge, as they do on every headline finding in the current snapshot, the canonical T2 number is reported in the manuscript and the T2-narrow number is reported in a companion footnote or in [`../results/unified_stats_t2_narrow.json`](../results/unified_stats_t2_narrow.json).

## 5. Which tier each headline claim uses

The per-claim mapping is specified in [`../article/CLAIMS_LEDGER.csv`](../article/CLAIMS_LEDGER.csv). The pattern is:

- **Stock and flow counts** (e.g., "1,900 disability opinions"): T2.
- **Win-rate levels and trajectory**: T2 dated-decided (n = 995 document rows) at the document level; the reported outcome figures are the case-level series over the universal one-case-one-unit collapsed core (N = 606: 287/68/251).
- **Kitagawa–Oaxaca–Blinder decomposition** (document-level archive; not reported in the Note — its fn 71): T2 dated-decided; pro se / represented strata defined by `is_pro_se` field.
- **Three-period analyses**: T2 dated-decided partitioned by `date_filed` on the period boundaries in § 3.
- **Pleading-failure mechanism analysis** (TRANSLATION family, 45.3% / 13.7% split, ≈ 32 pp gap under the merged three-model majority-vote ensemble primary on 727 contingency rows of 728 ensemble-coded cases; the finding is directional and machine-based): T4 (739-row pleading-loss universe, of which 736 classified).
- **Institutional-plaintiff robustness** (n = 74, broad-win 67.6% at the document level): decided T2 opinions restricted to institutional plaintiff classifier flag (h5 full cohort, not restricted to the 2022+ dated window).
- **Wave-specific checks** (post-2022 filings): T3.

## 6. Exclusions

The following records are present in T0 but excluded from every downstream tier:

- Opinions with `screening_result == "NO"` — excluded from T1 and below. The screening prompt requires the opinion to plead or adjudicate a federal Fair Housing Act, § 504, or associated statutory claim.
- Opinions with a missing `case_name` — excluded from T1 and below. These are parsing failures in the retrieval layer, not substantive exclusions.
- Opinions classified as disability cases but lacking `date_filed` in the study window or with non-decisive outcomes (PROCEDURAL, SETTLEMENT, UNDETERMINED) — retained in T2 / T3 / T4 counts, but excluded from all dated-decided analyses. Of the 1,900 T2 opinions, 553 lack `date_filed` and an additional 352 are dated within the study window but have non-decisive outcomes; the dated-decided T2 subset is n = 995 (1,900 − 553 − 352).

No opinions are excluded on the basis of outcome direction, jurisdiction, circuit, or any classifier-assigned field used on the right-hand side of a reported regression or comparison.

## 7. Replicating every n in this document

```bash
python scripts/recompute_stats_unified.py        # T2-narrow populations and win-rate levels
python scripts/decomposition.py                  # T2 canonical populations; KOB decomposition
python scripts/pro_se_mechanism_analysis.py      # T4 populations; TRANSLATION and mechanism splits
python scripts/h5_analysis.py                    # Institutional-plaintiff robustness (n = 74)
python scripts/h1_h2_analysis.py                 # Period-boundary sensitivity reads
```

Every script reads `data/FHA_Unified_Database.json` from the repository root and writes to `results/`. The tier counts above are produced by running these scripts on a clean checkout.

## 8. Robustness convention

T2-narrow (`"disability" ∈ protected_classes` only; n = 1,849; 972 dated-decided) is reported alongside T2 canonical wherever the win-rate level is sensitive to filter choice. Period-level findings reproduce directionally under both filters.
