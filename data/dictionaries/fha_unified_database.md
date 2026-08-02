# Data Dictionary: FHA Unified Database

This dictionary defines the public fields and coding conventions of the FHA Unified Database. Fields produced through model-assisted coding are classifications under fixed questions and permitted answers; they do not independently establish the facts of a case.

**Contents.** [Case Identification](#case-identification) · [Substantive Classification](#substantive-classification) · [Doctrinal Markers](#doctrinal-markers) · [Narrative Fields](#narrative-fields) · [Per-Claim Decomposition](#per-claim-decomposition) · [Pipeline Metadata](#pipeline-metadata) · [Source Databases](#source-databases) · [Complete Stored Schema](#data-dictionary--complete-stored-schema-generated) · [Exploratory Within-Group Analysis](#exploratory-within-group-analysis-strong-case-represented-subset) · [HUD Administrative Datasets](hud_administrative_datasets.md) · [Mechanism-Coding Artifacts](mechanism_coding_artifacts.md)

The FHA Unified Database (`data/FHA_Unified_Database.json`) contains **3,366 federal FHA opinions** in the raw corpus: 3,198 from the two source databases (RA Database 2,366 ∪ 2015 § 3604(f) Database 1,661; 829 overlap by `source_file`) plus 168 records added by the July 3, 2026 CourtListener re-pull extending the corpus endpoint to July 1, 2026 (tagged `database_sources = ["p3ext_20260703"]` or `["p3ext_20260703_r2"]`); the re-pull screened in 168 records — 133 carried by the `p3ext_20260703` tag, plus 35 distinct later opinions in cases already in the corpus that name-based deduplication wrongly dropped and a cluster-ID deduplication audit restored under the `p3ext_20260703_r2` tag. Of these, **2,690** are screened-in federal FHA cases (`screening_result == "YES"`), and **1,900** are screened-in disability cases (`screening_result == "YES"` AND (`protected_classes` contains `"disability"` OR `disability_alleged == True` OR `is_ra_case == True`)). The narrower filter `protected_classes` contains `"disability"` alone yields **1,849**; the 51-case gap is records flagged via `disability_alleged` or `is_ra_case` without `"disability"` appearing in `protected_classes`. **1,900** is the canonical disability-analysis population; all downstream subsets (disability-wave tranche, pleading-loss universe, etc.) are nested within it. See [`../../replication/SAMPLE_DEFINITIONS.md`](../../replication/SAMPLE_DEFINITIONS.md) § 2 for the full tier framework.

This curated dictionary documents the model-classified fields produced by the multi-model consensus pipeline, as published. The classifier's full 28-field output includes five free-text and property-level fields that the published database omits under the data-minimization policy described in [Narrative Fields](#narrative-fields) (`scripts/minimize_public_dataset.py`). Stored records carry additional keys beyond the classified fields — screening results, source flags, and refresh metadata — and screened-out records carry only a small subset (record-level key counts range from 4 to 39). The complete observed schema is in [Complete Stored Schema](#data-dictionary--complete-stored-schema-generated) below, with a machine-readable JSON Schema at [`../FHA_Unified_Database.schema.json`](../FHA_Unified_Database.schema.json) (regenerate both with `python scripts/make_data_dictionary.py`).

## Case Identification

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `case_name` | string | Full case caption | "Smith v. ABC Apartments" |
| `citation` | string | Reporter citation or docket number | "2024 WL 1234567" |
| `court` | string | Deciding court | "D. Ariz." |
| `year` | integer | Decision year (year component of `date_filed`) | 2024 |
| `date_filed` | string (ISO 8601) | Date the **opinion** was filed by the court — i.e., the CourtListener `OpinionCluster.date_filed` field. **Equivalent to "decision date" in the Note's prose**, because for opinions the cluster filing date is the date the opinion issued. Distinct from the underlying *case docket* filing date, which would be `Docket.date_filed` in CourtListener; the docket filing date is a separate field that is not part of this canonical dataset. The Note's three-period framework is keyed to `date_filed` (P1 < 2024-06-28; P2 < 2025-02-05; P3 ≥ 2025-02-05, through the 2026-07-01 corpus endpoint). | "2024-07-08" |
| `circuit` | string | Federal circuit | "9th Cir." |

## Substantive Classification

| Field | Type | Description | Values |
|-------|------|-------------|--------|
| `procedural_posture` | enum | Procedural stage at decision | MTD, summary_judgment, trial, preliminary_injunction, default_judgment, appeal, other |
| `fha_section_cited` | array | FHA sections invoked | ["3604(f)", "3604(c)"] |
| `primary_protected_class` | enum | Dominant protected class | disability, race, national_origin, familial_status, religion, sex, color |
| `accommodation_type` | enum | Type of accommodation sought | structural_modification, equipment, service_animal, emotional_support_animal, policy_exception, parking, transfer, other |
| `outcome` | enum | Case disposition | plaintiff_win, defendant_win, mixed, settled, procedural |
| `primary_claim_type` | enum | Lead FHA theory | reasonable_accommodation, disparate_treatment, disparate_impact, design_and_construction, retaliation, interference |
| `claim_types` | array | All FHA theories raised | ["reasonable_accommodation", "disparate_treatment"] |
| `plaintiff_type` | enum | Plaintiff category | individual, fair_housing_org, government, group_home_operator, class_action |
| `defendant_type` | enum | Defendant category | landlord, hoa, municipality, property_manager, developer, other |
| `disability_category` | enum | Primary disability type | mobility, mental_health, substance_abuse, sensory, intellectual, chronic_illness, other |
| `housing_type` | enum | Housing context | apartment, single_family, group_home, public_housing, condo, assisted_living, other |
| `subsidy_program` | string | Federal housing program | "Section 8", "LIHTC", "none" |

## Doctrinal Markers

| Field | Type | Description |
|-------|------|-------------|
| `iqbal_twombly_cited` | boolean | Whether *Iqbal*/*Twombly* pleading standards are invoked |
| `loper_bright_cited` | boolean | Whether *Loper Bright Enterprises v. Raimondo* is cited |
| `interactive_process_discussed` | boolean | Whether the reasonable-accommodation interactive process is analyzed |

## Narrative Fields

| Field | Type | Description |
|-------|------|-------------|
| `key_cases_cited` | array | Principal authorities cited |

The published database is a minimized projection of the full research database: five
free-text and property-level fields (model-written case summaries and holdings, the
accommodation narrative, free-text race detail, and property city) are removed by
`scripts/minimize_public_dataset.py`, which also documents the registered digest of the
full source. No published claim reads a removed field, and
`scripts/recompute_verification.py` re-derives the registered baselines from the
minimized file on every release-gate run.

## Per-Claim Decomposition

| Field | Type | Description |
|-------|------|-------------|
| `fha_claims` | array of objects | Individual legal claims extracted by Haiku 4.5. Each object contains `claim_type`, `outcome`, `reasoning`, and `protected_class`. |

## Pipeline Metadata

| Field | Type | Description |
|-------|------|-------------|
| `resolution_tier` | integer (0-4) | Consensus tier that resolved this record. 0 = unanimous, 1-2 = majority vote, 3 = Haiku adjudication, 4 = Sonnet adjudication. |
| `model_agreement` | object | Per-field agreement metadata across three classifiers (MiniMax, DeepSeek, Kimi) |
| `adjudicator` | string | Model that adjudicated disagreements, if escalated ("haiku-4.5", "sonnet-4.6", or null) |
| `source_corpus` | enum | Origin corpus: "ra_database" (2021+ RA cases), "fha_2015_database" (2015 FHA Database § 3604(f)), or "recent_supplement" |

## Source Databases

The unified database merges records from two source corpora plus a July 2026 endpoint-extension re-pull:

| Database | File | Scope | Raw n | Screened-in n |
|----------|------|-------|-------|---------------|
| RA Database | `FHA_RA_Database_unified_20260328_090852.json` | Reasonable accommodation cases, all protected classes, 2021+ | 2,366 | 1,857 |
| 2015 FHA Database | `FHA_3604_Database_unified_20260328_104352.json` | § 3604(f) cases from 2015 FHA Database, 2015+ | 1,661 | 1,461 |
| July 2026 refresh | `FHA_Unified_Database.json`, `database_sources` ∋ `"p3ext_20260703"` OR `"p3ext_20260703_r2"` | July 3, 2026 CourtListener re-pull (original query, all precedential statuses including Unknown); endpoint 2026-07-01; 168 screened in — 133 tagged `p3ext_20260703` plus 35 tagged `p3ext_20260703_r2`, the latter distinct later opinions in cases already in the corpus, restored by a cluster-ID deduplication audit | 168 | 168 |
| **Unified (raw)** | `FHA_Unified_Database.json` | Two-source union (by `source_file`; 829 raw overlap) + 168 refresh records | **3,366** | — |
| **Unified (screened)** | `FHA_Unified_Database.json`, filtered | `screening_result != "NO"` AND `case_name` present (the canonical T1 predicate in `scripts/analysis_filters.py`; equivalent to `screening_result == "YES"` on this snapshot); 796 screened overlap | — | **2,690** |
| **Disability population** | `FHA_Unified_Database.json`, filtered | Screened-in AND (`protected_classes` ∋ `"disability"` OR `disability_alleged` OR `is_ra_case`) | — | **1,900** |

<!-- BEGIN GENERATED: complete stored schema -->

## Data Dictionary — Complete Stored Schema (generated)

Generated by `scripts/make_data_dictionary.py` from `data/FHA_Unified_Database.json` (3,366 records; T1 screened-in = 2,690; T2 disability-screened = 1,900).

This is the complete observed key inventory: it covers every stored key, including screening and source metadata, with presence/null rates by tier. Machine-readable schema: [`../FHA_Unified_Database.schema.json`](../FHA_Unified_Database.schema.json).

Records are heterogeneous by design: screened-out records (screening_result == "NO" or unscreened retrieval failures) carry as few as 4 keys; fully classified records carry up to 44.

| Key | Types | Present (all) | Null (all) | Present T1 | Present T2 | Distinct values | Enumerated values |
|---|---|---|---|---|---|---|---|
| `_not_fha_flag` | boolean | 52/3366 | 0 | 52/2690 | 25/1900 |  |  |
| `accommodation_type` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 17 | `ASSISTANCE_ANIMAL`; `COMMUNICATION_ACCOMMODATION`; `DESIGN_AND_CONSTRUCTION`; `DISCRIMINATION_PRIMARY`; `EVICTION_DEFENSE`; `LIVE_IN_AIDE`; `NONE`; `OTHER`; `PARKING`; `POLICY_EXCEPTION`; `RENT_PAYMENT`; `SECTION_8_VOUCHER`; `SOBER_LIVING_… |
| `case_name` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | >24 |  |
| `circuit` | string | 3088/3366 | 0 | 2662/2690 | 1878/1900 | 14 | `10th Circuit`; `11th Circuit`; `1st Circuit`; `2nd Circuit`; `3rd Circuit`; `4th Circuit`; `5th Circuit`; `6th Circuit`; `7th Circuit`; `8th Circuit`; `9th Circuit`; `D.C. Circuit`; `Federal Circuit`; `Supreme Court` |
| `citation` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | >24 |  |
| `claim_types` | array | 2690/3366 | 0 | 2690/2690 | 1900/1900 |  |  |
| `counsel_named` | boolean | 3356/3366 | 0 | 2688/2690 | 1899/1900 |  |  |
| `court` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | >24 |  |
| `database_sources` | array | 3366/3366 | 0 | 2690/2690 | 1900/1900 |  |  |
| `date_filed` | string | 2282/3366 | 0 | 1856/2690 | 1347/1900 | >24 |  |
| `defendant_type` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 18 | `DEVELOPER`; `GOVERNMENT`; `GROUP_HOME_OPERATOR`; `HOA_CONDO_ASSN`; `HOA_CONDO_COOP`; `HOUSING_AUTHORITY`; `INDIVIDUAL_TENANT`; `LANDLORD`; `LENDER`; `MUNICIPALITY`; `OTHER`; `OTHER: Non-profit transitional housing program operator and its … |
| `delay_as_denial` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 3 | `NO`; `UNDETERMINED`; `YES` |
| `disability_alleged` | boolean | 3357/3366 | 0 | 2688/2690 | 1899/1900 |  |  |
| `disability_category` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 11 | `INTELLECTUAL_DEVELOPMENTAL`; `MENTAL_HEALTH`; `MOBILITY`; `MULTIPLE`; `MULTIPLE_UNSPECIFIED`; `N/A`; `OTHER`; `OTHER: No disability alleged`; `SENSORY`; `SUBSTANCE_USE`; `UNDETERMINED` |
| `dual_basis_claim` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 3 | `NO`; `UNDETERMINED`; `YES` |
| `fha_claims` | array | 3059/3366 | 0 | 2627/2690 | 1856/1900 |  |  |
| `fha_section_cited` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | >24 |  |
| `housing_type` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 18 | `ASSISTED_LIVING`; `CONDO_COOP`; `HOA_CONDO`; `LIHTC`; `MANUFACTURED_HOUSING`; `OTHER`; `OTHER_SUBSIDIZED`; `PRIVATE_MARKET`; `PUBLIC_HOUSING`; `RENTAL_APARTMENT`; `SECTION_202`; `SECTION_811`; `SECTION_8_PBRA`; `SECTION_8_PBV`; `SECTION_8_… |
| `in_iqbal_twombly_db` | boolean | 3366/3366 | 0 | 2690/2690 | 1900/1900 |  |  |
| `interactive_process_discussed` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 3 | `NO`; `UNDETERMINED`; `YES` |
| `iqbal_twombly_cited` | boolean | 3357/3366 | 0 | 2688/2690 | 1899/1900 |  |  |
| `is_ra_case` | boolean | 3357/3366 | 0 | 2688/2690 | 1899/1900 |  |  |
| `key_cases_cited` | array | 2690/3366 | 0 | 2690/2690 | 1900/1900 |  |  |
| `loper_bright_cited` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 3 | `NO`; `UNDETERMINED`; `YES` |
| `loper_bright_era` | string | 3366/3366 | 0 | 2690/2690 | 1900/1900 | 3 | `post_loper_bright`; `pre_loper_bright`; `unknown` |
| `outcome` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 6 | `DEFENDANT_WIN`; `MIXED`; `PLAINTIFF_WIN`; `PROCEDURAL`; `SETTLEMENT`; `UNDETERMINED` |
| `plaintiff_type` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 11 | `ASSOCIATION`; `FAIR_HOUSING_ORG`; `GOVERNMENT`; `GROUP_HOME_OPERATOR`; `HOA_CONDO_ASSN`; `INDIVIDUAL_PROSPECTIVE`; `INDIVIDUAL_TENANT`; `OTHER`; `OTHER: Individual property owner and loan applicant`; `PRIVATE_LANDLORD`; `UNDETERMINED` |
| `primary_claim_type` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 16 | `DESIGN_AND_CONSTRUCTION`; `DISPARATE_TREATMENT`; `NOT_FHA`; `REASONABLE_ACCOMMODATION`; `UNCLEAR`; `UNDETERMINED`; `design_and_construction`; `discriminatory_advertising`; `discriminatory_lending`; `disparate_impact`; `disparate_treatment`… |
| `primary_protected_class` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 12 | ``; `N/A`; `NONE`; `UNDETERMINED`; `disability`; `familial_status`; `national_origin`; `race`; `religion`; `sex`; `undetermined`; `veteran_status` |
| `pro_se` | boolean | 3356/3366 | 0 | 2688/2690 | 1899/1900 |  |  |
| `procedural_posture` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 15 | `ADMINISTRATIVE_REVIEW`; `APPEAL`; `DEFAULT_JUDGMENT`; `DISCOVERY`; `MOTION_IN_LIMINE`; `MOTION_TO_DISMISS`; `OTHER`; `OTHER_PROCEDURAL`; `PRELIMINARY_INJUNCTION`; `PROCEDURAL`; `SCREENING_ORDER`; `SETTLEMENT_CONSENT`; `SUMMARY_JUDGMENT`; `… |
| `property_state` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | >24 |  |
| `protected_classes` | array/string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | >24 |  |
| `race_mentioned` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | 3 | `NO`; `UNDETERMINED`; `YES` |
| `screening_result` | string | 3331/3366 | 0 | 2690/2690 | 1900/1900 | 2 | `NO`; `YES` |
| `secondary_accommodation_type` | null/string | 2690/3366 | 1 | 2690/2690 | 1900/1900 | 13 | `ASSISTANCE_ANIMAL`; `COMMUNICATION_ACCOMMODATION`; `EVICTION_DEFENSE`; `LIVE_IN_AIDE`; `NONE`; `PARKING`; `POLICY_EXCEPTION`; `REASONABLE_MODIFICATION_DENIAL`; `RENT_PAYMENT`; `STRUCTURAL_MODIFICATION`; `TRANSFER`; `UNDETERMINED`; `VISITOR… |
| `source_file` | string | 3366/3366 | 0 | 2690/2690 | 1900/1900 | >24 |  |
| `subsidy_program` | string | 2690/3366 | 0 | 2690/2690 | 1900/1900 | >24 |  |
| `year` | integer | 2690/3366 | 0 | 2690/2690 | 1900/1900 |  |  |

Tier predicates (canonical, from `scripts/analysis_filters.py`): T1 = `screening_result != "NO"` AND `case_name` present; on this snapshot that is equivalent to `screening_result == "YES"` (2,690 records either way). T2 = T1 AND (`"disability" in protected_classes` OR `disability_alleged` OR `is_ra_case`).

<!-- END GENERATED: complete stored schema -->

## Exploratory Within-Group Analysis: Strong-Case Represented Subset

The data dictionary documents a "strong-case represented subset" intended to test whether represented plaintiffs experienced deterioration beyond the composition effect. The subset is defined as:

1. **Represented**: `pro_se` = false (plaintiff has counsel)
2. **Specific-duty claim**: `primary_claim_type` in {`reasonable_accommodation`, `design_and_construction`} (excludes open-textured discrimination claims)
3. **Dated**: case has an exact decision date within the P1 or P3 period windows

An audit did not reproduce a broad-win-rate pair for this subset under this documented filter, so no such pair is reported here. Do not use this subsection as support for a manuscript claim unless the exact derivation code, denominator, and regenerated output are provided. The manuscript relies instead on the represented-plaintiff period comparison documented in the empirical outputs.

## Notes

- Enum values are lowercase with underscores. Array fields may contain multiple values.
- The `fha_claims` array enables claim-level analysis (7,284 total claims across 3,059 cases).
- Pipeline metadata fields allow tier-disaggregated reliability analysis.
- For the per-claim extraction schema, see [`../../method/pipeline/per_claim_extraction_schema.json`](../../method/pipeline/per_claim_extraction_schema.json).
