# Appendix A: FHA Case Dataset — Construction Methodology

**Cited by:** Note footnote 66 (Part II.B; fns 64–65 cite the repository and app. A-5) and the corpus-tier apparatus (`SAMPLE_DEFINITIONS.md`).
**Evidentiary status:** Appendix-level methodology; classification-dependent figures are stakes evidence under the Note's posture.
**Regeneration:** Narrative sections are not script-generated; corpus tiers and downstream tables reproduce from `data/FHA_Unified_Database.json` via `scripts/` (see REPRODUCE.md).

## A.1 Overview

This Appendix describes the construction of the **FHA Unified Database**, the principal empirical dataset underlying the case-classification analysis in this Note.

**The FHA Unified Database** (raw union n = 3,366; screened-in n = 2,690; **disability population n = 1,900**) is the single source of truth for all statistical claims in this Note. It was constructed by merging two overlapping source corpora — the RA Database (raw 2,366 / screened-in 1,857 all-protected-class FHA cases, 2021–2026) and the 2015 FHA Database (raw 1,661 / screened-in 1,496 § 3604(f) disability cases, 2015–2026) — with 829 raw cases (796 screened-in) appearing in both. A corpus refresh pulled July 3, 2026 appended a third, CourtListener-only increment of 168 screened-in opinions (133 from the initial pull plus 35 restored by the cluster-ID audit described at Section A.5; all tagged `database_sources = ["p3ext_20260703"]`), extending the data endpoint to July 1, 2026 (maximum date filed); the RA and 2015 FHA source-database figures above are unchanged (see Section A.5). The three tiers are:

| Tier | Definition | n |
|---|---|---|
| T0 Raw corpus | Full union by `source_file` | 3,366 |
| T1 Screened-in | `screening_result == "YES"` | 2,690 |
| T2 Disability population | T1 AND (`protected_classes` contains `"disability"` OR `disability_alleged == True` OR `is_ra_case == True`) | 1,900 |

A per-claim structured extraction (the defined Stage 4 term; see the controlling definition in [`METHODOLOGY.md`](../../method/METHODOLOGY.md)) via Haiku 4.5 Batch API enriched each record with detailed claim-level data. For the Note's disability-focused analysis, the unified database is filtered to the T2 population of 1,900 screened-in disability cases. All downstream subsets (three-period cohorts, pleading-loss universe, disability-wave tranche) are nested inside T2.

A **narrower sensitivity cohort** (n = 1,849) restricts to cases with an explicit `"disability"` entry in `protected_classes`, excluding records flagged through `disability_alleged` or `is_ra_case` alone. The canonical T2 population (1,900) is used for all statistical claims; the n = 1,849 cohort is reported only as a robustness sensitivity.

**Three-Period Temporal Design.** Exact decision dates (resolved for all cases via CourtListener API, opinion text extraction, and Google Scholar) enable a three-period analysis:

| Period | Date Range | Dated Disability (any outcome) | Decided Document Rows | Decided Cases (case-level) |
|--------|-----------|:---:|:---:|:---:|
| P1 | Jan 1, 2022 – June 28, 2024 | 642 | 476 | 287 |
| P2 | June 28, 2024 – Feb 5, 2025 | 163 | 120 | 68 |
| P3 | Feb 5, 2025 – July 1, 2026 | 542 | 399 | 251 |

The windows are labeled by date rather than by event, per the Note's Part II.B convention; the boundary rationale is stated in the Note's margin (fn 67).

Of 1,900 disability cases, 1,347 have exact decision dates falling within the study period (2022-July 1, 2026); 995 recorded decided document rows among them carry resolved outcomes (`PLAINTIFF_WIN`, `DEFENDANT_WIN`, or `MIXED`). Because a single case can generate multiple decided document rows, decided rows are collapsed to one case-level unit per case before any outcome analysis. The resulting case-level decided census is **N = 606** (287 in P1, 68 in P2, 251 in P3); the full pipeline chain is 3,366 raw records -> 2,690 screened-in FHA -> 1,900 disability -> 1,347 dated in-window -> 995 recorded decided document rows -> 606 case-level decided units. All three-period outcome analysis in this Note is computed on the collapsed 606-case basis. The remaining 553 cases are undated or pre-2022; they are included in overall statistics but excluded from three-period analysis.

**Source corpora.** The unified database draws from:

- **RA Database** (n=1,857): All-protected-class FHA cases, 2021–2026, from a CourtListener "fair housing act" search.
- **2015 FHA Database** (n=1,496 screened-in): Section 3604(f) disability cases, 2015–2026, from a CourtListener search supplemented by Google Scholar.

Both source databases were classified across the thirty output keys including case outcome, claim types, accommodation type, disability category, and procedural posture, using a multi-model classification pipeline with automated consensus detection. The RA Database used tiered consensus adjudication with model adjudication for three-way splits; the 2015 FHA Database used the same triple-model classification pipeline but resolved three-way splits using MiniMax M2.7 as the tiebreaker rather than API adjudication. After deduplication and merging, all cases were subjected to per-claim structured extraction via Haiku 4.5 Batch API. See Section A.5 for the reconciliation analysis.

## A.1.1 Research Design and Database Rationale

The corpus was assembled in stages. A pilot corpus (the FHA Pilot Database, n=331; see Section A.4) sampled FHA opinions on race-and-zoning search terms; disability-based claims were the largest single category within it at 38.1% of cases, despite search terms designed to favor race-and-zoning matters. The two principal databases were then drawn to sample disability enforcement directly, on the filing-date filters and post-classification scopes described below. Earlier pilot iterations (v1–v3) were discarded and their cases fully re-coded under the final design (Section A.2.7).

Both principal databases were constructed using the same automated download pipeline, which queries the CourtListener REST API (v4) for the exact phrase "fair housing act" across all federal courts (Supreme Court, all circuits, all districts), including published, unpublished, and unknown-status opinions, with results deduplicated by cluster ID. The two databases differ in their filing-date filter, post-classification scope, and supplemental sources:

The **2015 FHA Database** (n=1,496) used a filing-date filter beginning January 1, 2015, chosen to coincide with HUD's promulgation of the Affirmatively Furthering Fair Housing Rule, 80 Fed. Reg. 42,272 (July 16, 2015), and retained for the decade of pre-*Loper Bright* baseline it provides ahead of *Loper Bright Enterprises v. Raimondo*, 144 S. Ct. 2244 (2024). The CourtListener download (1,446 opinions) was supplemented by 215 case texts identified through Google Scholar to capture opinions not indexed in CourtListener, producing a corpus of 1,661 documents. The screening and classification pipeline then identified the subset involving § 3604(f) disability claims. The Google Scholar supplement consists entirely of post-*Loper Bright* cases (2024+) with a higher plaintiff win rate (18.9% strict) than the CourtListener-only post-*Loper Bright* cases (11.9% strict); including these cases attenuates the reported post-*Loper Bright* decline from 9.6 to 7.8 percentage points, making the reported effect size a conservative estimate.

The **RA Database** (n=1,857) used a filing-date filter of January 1, 2021 and retained all FHA protected classes after classification — no post-classification narrowing to disability. This broader scope enables cross-class comparisons that the disability-only 2015 FHA Database cannot support.

## A.2 RA Database (n=1,857)

### A.2.1 Source Documents

Case texts were obtained from CourtListener (Free Law Project) using the CourtListener REST API (v4). A Java application queried the search endpoint for the exact phrase "fair housing act" across all federal courts (Supreme Court, all circuit courts of appeals, and all district courts), filtered to opinions filed after January 1, 2021, and including published, unpublished, and unknown-status opinions. The application paginated through all results, collected case metadata (cluster ID, opinion IDs, case caption, date filed, court, circuit, judge, panel members, citations, and docket number), then downloaded full opinion text for each case using 10-thread parallel retrieval from the opinions endpoint. Results were deduplicated by cluster ID. Each case was stored as a plain-text file derived from the full text of the court opinion or order. The corpus comprises 2,366 documents. The 2021 start date and all-protected-class scope were chosen to enable cross-class comparisons that the 2015 FHA Database (§ 3604(f) only, 2015–2026) cannot support; see Section A.1.1. The final dataset and all analysis scripts are committed in this repository (`data/FHA_Unified_Database.json`, `scripts/`); the as-run Java download application is retained in the project's private research records (it does not compile stand-alone); the committed query specifications at [`../../replication/queries/courtlistener_api.md`](../../replication/queries/courtlistener_api.md) document the retrieval.

### A.2.2 FHA Relevance Screening

Each document was first screened for FHA relevance using Google's Gemini 3.1 Flash Lite model, a lightweight classifier configured at zero temperature. The screening prompt instructed the model to determine whether the document was a legal decision adjudicating a claim under the Fair Housing Act, returning only "YES" or "NO." Documents classified as non-FHA were excluded from further processing. Of 2,366 documents screened, 1,857 passed the relevance filter (78.5%).

### A.2.3 Triple-Model Independent Classification

Each FHA-relevant case was independently classified by three large language models via the OpenRouter API:

| Model | Provider | Suffix | Role |
|-------|----------|--------|------|
| MiniMax M2.7 | MiniMax | `_minmax` | Primary extraction model |
| DeepSeek V3.2 | DeepSeek | `_deepseek` | Independent verification |
| Kimi K2.5 | Moonshot AI | `_kimi` | Independent verification |

All three models received identical inputs: (1) a system prompt specifying the classification schema with controlled vocabulary for each field, and (2) the full case text (truncated to 50,000 characters for longer opinions, preserving the first 25,000 and last 25,000 characters). The system prompt enforced a flat JSON output structure with thirty output keys, grouped here by function:

- **Case identification**: case name, citation, court, year
- **Substantive classification**: FHA section cited, accommodation type, disability category, claim types, outcome
- **Party identification**: plaintiff type, defendant type
- **Procedural context**: procedural posture, housing type, property location
- **Doctrinal indicators**: interactive process discussion, delay-as-denial, *Loper Bright* citation, race-disability intersection
- **Narrative fields**: key holding, brief summary, accommodation description, key cases cited

Each model was configured at temperature 0.2 with explicit reasoning budget caps. An earlier GLM-5 (Zhipu) evaluation, later cancelled on cost grounds, had shown that reasoning-enabled models produce unpredictable output token volumes when their reasoning budgets run unconstrained, which made cost estimation and pipeline reliability hard to control. Per-model reasoning budget limits followed for all subsequent runs.

| Model | Role | Temperature | Reasoning Budget | Max Output Tokens | Output Cost/M |
|-------|------|-------------|-----------------|-------------------|---------------|
| MiniMax M2.7 | Primary extraction | 0.2 | 2,048 tokens | 8,192 | $1.20 |
| DeepSeek V3.2 | Consensus verification | 0.2 | 16,384 tokens | 8,192 | $0.38 |
| Kimi K2.5 | Consensus verification | 0.2 | 1,024 tokens | 8,192 | $2.20 |
| Gemini 3.1 Flash Lite | FHA relevance screening | 0.0 | 0 (disabled) | — | — |
| Haiku 4.5 | Tier 3 adjudication (Batch API) | default | default | default | — |
| Claude Sonnet 4.6 | Tier 4 adjudication (Batch API) | default | 2,000 (thinking) | 4,000 | — |

Reasoning budgets were calibrated primarily by cost. MiniMax M2.7 served as the primary extraction model; DeepSeek V3.2 and Kimi K2.5 served as independent verification models whose role was to confirm or dispute MiniMax's classifications. DeepSeek received the largest reasoning budget (16,384 tokens) because its output pricing ($0.38/M) made extended reasoning inexpensive. Kimi K2.5's smaller budget (1,024 tokens), despite its higher output cost ($2.20/M), reflected a verification role that did not require extended deliberation. MiniMax's budget (2,048 tokens) balanced extraction quality against its moderate output cost ($1.20/M).

The three models processed each case concurrently, producing three independent classification records per case.

**Coding protocol.** Each case was coded for the following fields:

| Field | Description | Coding Method |
|-------|-------------|---------------|
| outcome | Case outcome | PLAINTIFF_WIN, DEFENDANT_WIN, MIXED, PROCEDURAL, SETTLEMENT, UNDETERMINED |
| accommodation_type | Primary accommodation at issue | 13 categories (see Appendix K.2); UNDETERMINED if not determinable |
| secondary_accommodation | Secondary accommodation if any | Same categories as above; NONE if single issue |
| defendant_type | Institutional category of defendant | PRIVATE_LANDLORD, PROPERTY_MANAGEMENT, HOA_CONDO_ASSN, HOUSING_AUTHORITY, DEVELOPER, MUNICIPALITY, OTHER |
| plaintiff_type | Institutional category of plaintiff | INDIVIDUAL_TENANT, GROUP_HOME_OPERATOR, FAIR_HOUSING_ORG, GOVERNMENT, OTHER |
| disability_category | Primary disability type | MENTAL_HEALTH, SUBSTANCE_USE, MOBILITY, SENSORY, INTELLECTUAL_DEVELOPMENTAL, MULTIPLE_UNSPECIFIED, OTHER |
| procedural_posture | Stage at which decision occurred | MOTION_TO_DISMISS, SUMMARY_JUDGMENT, PRELIMINARY_INJUNCTION, TRIAL, DEFAULT_JUDGMENT, APPEAL, SETTLEMENT_CONSENT, ADMINISTRATIVE_REVIEW, DISCOVERY, OTHER_PROCEDURAL |
| property_state | State where property is located | Two-letter abbreviation |
| housing_type | Type of housing | PRIVATE_MARKET, PUBLIC_HOUSING, SECTION_8_VOUCHER, SECTION_8_PBV, LIHTC, SECTION_811, SECTION_202, SUPPORTIVE_HOUSING, OTHER_SUBSIDIZED, HOA_CONDO, MANUFACTURED_HOUSING, UNDETERMINED |
| year | Year of decision | Numeric |
| court | Deciding court | Standard abbreviation |

### A.2.4 Consensus Detection and Tiered Adjudication

The three-model outputs were consolidated into a single canonical record using a tiered resolution strategy designed to minimize cost while preserving classification accuracy:

**Tier 0 — Full Consensus (No API Call).** Where all three models returned identical values for every categorical field, that value was adopted as canonical. Twelve records achieved full consensus across all categorical fields (0.6% of FHA-relevant records).

**Tier 1 — Majority Agreement, Non-Critical Fields (No API Call).** Where two of three models agreed on all fields, with dissent limited to non-critical fields (any field other than outcome, primary claim type, or claim types), the majority value was adopted. 278 records fell into this tier (15.0%).

**Tier 2 — Majority Agreement, Critical Fields (No API Call).** Where two of three models agreed on outcome, primary claim type, or claim types but one model dissented, the 2-of-3 consensus was treated as sufficient. 565 records fell into this tier (30.4%).

**Tier 3 — Three-Way Split, Non-Critical Fields → Haiku 4.5 Adjudication.** Where all three models returned different values for non-critical fields (e.g., accommodation type, defendant type, disability category) with no majority, the case was submitted to Claude Haiku 4.5 (Anthropic) for adjudication. Haiku received the original case text alongside each model's answer for the disputed fields and was instructed to determine the correct classification using the same controlled vocabulary. 697 cases were adjudicated by Haiku (37.5%).

**Tier 4 — Three-Way Split, Critical Fields → Sonnet 4.6 Adjudication.** Where all three models returned different values for outcome, primary claim type, or claim types, the case was submitted to Claude Sonnet 4.6 (Anthropic) — a more capable model — for adjudication. In addition to resolving the disputed categorical fields, Sonnet re-extracted the four free-text narrative fields (key holding, brief summary, accommodation description, key cases cited) fresh from the source text. 302 cases were adjudicated by Sonnet (16.3%).

Both adjudication tiers used the Anthropic Message Batches API, which processes requests asynchronously at a 50% cost discount. Each adjudication request included the original case text and a structured presentation of each model's answer for the disputed fields. The adjudicating model was required to provide reasoning for each resolution, which was stored as metadata in the final record.

**Free-Text Field Resolution.** For narrative fields (key holding, brief summary, accommodation description, key cases cited), exact consensus is not meaningful because models produce different phrasings of equivalent content. For Tier 4 (Sonnet-adjudicated) records, Sonnet re-extracted these fields from the source text. For all other records, the MiniMax M2.7 version was adopted as the canonical text, as it consistently produced the most detailed extractions.

### A.2.5 Agreement Rates Across Models

The following table reports inter-model agreement rates for key classification fields prior to adjudication (n=1,857 FHA-relevant records):

| Field | Unanimous (3/3) | Majority (2/3) | No Majority |
|-------|-----------------|----------------|-------------|
| Court | 96.9% | 2.9% | 0.2% |
| Year | 98.7% | 1.2% | 0.2% |
| Outcome | 69.1% | 28.0% | 2.9% |
| Primary Claim Type | 62.6% | 32.2% | 5.2% |
| Claim Types | 44.2% | 43.4% | 12.4% |
| Accommodation Type | 34.7% | 45.8% | 19.5% |
| Disability Category | 47.9% | 47.4% | 4.7% |
| Plaintiff Type | 87.3% | 10.8% | 1.9% |
| Defendant Type | 57.6% | 34.8% | 7.6% |
| Procedural Posture | 69.2% | 28.8% | 2.0% |
| Housing Type | 70.9% | 26.8% | 2.3% |

Near-perfect agreement on court and year confirms that all three models correctly identified basic case metadata. The lower rates for accommodation type and disability category trace to three sources of disagreement. The first is genuine classification ambiguity, where cases involve overlapping accommodation types or multiple disabilities. The second is claim-mix breadth: cases whose primary claims are disparate treatment, design-and-construction enforcement, or non-FHA theories passed the FHA relevance screen — they are FHA cases, but not accommodation cases (a supplemental per-claim extraction found that 68.1% of cases in the database contain no reasonable accommodation claim; see Section A.2.7). The third is systematic positional bias, where models anchor to different accommodations in multi-claim opinions: MiniMax anchors to the first-mentioned accommodation (57% of informative cases), while Kimi anchors to the most-discussed (79%), with the three-model ensemble partially self-correcting via these opposing biases (Fisher's exact test: OR=4.89, p=0.12, n=14 informative cases). Even on accommodation type, the most contested field at 34.7% unanimous, majority agreement and adjudication together resolved 100% of records to a canonical value.

### A.2.6 Final Dataset Composition

The final consolidated dataset contains 1,857 FHA-relevant records, each with canonical (unsuffixed) values for the thirty output keys. Treating null or absent values as missing, twenty-five of the thirty output keys are 100% populated on the RA-sourced component (n = 1,857); the partial keys are citation (99.9%), key_cases_cited (99.2%), primary_protected_class (98.5%), claim_types (97.4%), and protected_classes (97.2%). The shortfalls reflect cases where no model could determine the value and the adjudicating model likewise returned no result, indicating genuine indeterminacy in the source opinion.

Two database files are produced:

- **Unified database** (`FHA_RA_Database_unified_[timestamp].json`): Contains only canonical fields, resolution metadata, and identity fields — the single source of truth for analysis. Average of 27 fields per record.
- **Audit database** (`FHA_RA_Database_audit_[timestamp].json`): Preserves all three model-specific values with suffixes (`_minmax`, `_deepseek`, `_kimi`) alongside canonical values and adjudication reasoning — the full provenance trail. Average of 91 fields per record.

| Resolution Method | Records | Percentage |
|-------------------|---------|------------|
| Unanimous (all 3 models agree on every field) | 12 | 0.6% |
| Majority (non-critical field dissent only) | 278 | 15.0% |
| Majority (critical field dissent, 2-of-3 trusted) | 565 | 30.4% |
| Haiku 4.5 adjudicated (non-critical 3-way splits) | 697 | 37.5% |
| Sonnet 4.6 adjudicated (critical 3-way splits) | 302 | 16.3% |
| Other (consensus/majority fallback) | 3 | 0.2% |
| **Total FHA-relevant** | **1,857** | **100%** |

Of the 1,857 FHA-relevant records, 858 (46.2%) were resolved entirely through consensus or majority vote with no additional API calls (Tiers 0–2 plus 3 Other cases). The remaining 999 (53.8%) required adjudication by an Anthropic model to resolve at least one three-way disagreement (Tiers 3–4).

### A.2.7 Supplemental Per-Claim Extraction (Haiku 4.5)

A supplemental extraction pass was conducted on all 2,366 source documents (including the 509 that failed the initial FHA relevance screen) using Claude Haiku 4.5 (Anthropic) via the Message Batches API at temperature 0.1. Unlike the pipeline's single-case-single-classification approach, this pass decomposed each case into its constituent legal claims, extracting an independent record for each FHA claim the court addressed.

**Extraction schema.** Each case produced a JSON record containing: (1) case-level fields (pro se status, counsel identification, disability alleged, plaintiff type, defendant type, disability category, housing type, FHA sections cited, interactive process discussed, delay-as-denial, *Loper Bright* cited, *Iqbal*/*Twombly* cited, race mentioned); and (2) an array of claim-level objects, one per distinct FHA claim, each classified by legal theory (REASONABLE_ACCOMMODATION, DISPARATE_TREATMENT, DISPARATE_IMPACT, RETALIATION, DESIGN_AND_CONSTRUCTION, INTERFERENCE_COERCION, NOT_FHA, or UNCLEAR), accommodation type (for RA claims only), RA standard applied, procedural stage, disposition, merits reached (YES/NO/PARTIAL/SETTLEMENT), dismissal reason, outcome, and reasoning. Non-FHA claims were collapsed into a single object per case.

**Results.** The unified per-claim extraction produced 6,718 total claims from 3,193 cases (average 2.1 claims per case); five source records were dropped for parser failure or empty source text (see Section A.5), and the returned outputs contained zero parse errors. Key findings:

| Metric | Value |
|--------|-------|
| Total claims | 6,718 |
| FHA claims | 4,464 |
| Non-FHA claims | 2,254 |
| DISPARATE_TREATMENT claims | 1,731 (38.8% of FHA) |
| REASONABLE_ACCOMMODATION claims | 1,257 (28.2% of FHA) |
| RETALIATION claims | 601 (13.5% of FHA) |
| DISPARATE_IMPACT claims | 392 (8.8% of FHA) |
| INTERFERENCE_COERCION claims | 243 (5.4% of FHA) |
| UNCLEAR claims | 168 (3.8% of FHA) |
| DESIGN_AND_CONSTRUCTION claims | 72 (1.6% of FHA) |

**Merits distribution.** Of all FHA claims in the unified dataset: merits_reached=NO 72.0%, merits_reached=YES 24.7%, merits_reached=PARTIAL 2.6%, merits_reached=SETTLEMENT 0.8%.

**Per-theory merits win rates.** Among claims reaching merits adjudication:

| Theory | Merits Claims | Plaintiff Wins | Win Rate |
|--------|--------------|----------------|----------|
| DESIGN_AND_CONSTRUCTION | 18 | 5 | 27.8% |
| DISPARATE_TREATMENT | 499 | 110 | 22.0% |
| DISPARATE_IMPACT | 118 | 22 | 18.6% |
| REASONABLE_ACCOMMODATION | 367 | 59 | 16.1% |
| INTERFERENCE_COERCION | 68 | 6 | 8.8% |
| RETALIATION | 142 | 8 | 5.6% |

Accommodation-type win rates and RA-specific findings in the Note are computed on the RA merits population (367 claims reaching merits) unless otherwise noted. (This 367 is a full-corpus per-claim count from the supplemental extraction, distinct from any case-level period count.)

**Cross-validation.** The Haiku per-claim extraction achieved 65.9% exact match (87/132 cases) with the pipeline's canonical accommodation-type classification on RA merits cases. Most divergences were taxonomic boundary disputes: sober-living zoning cases that Haiku classified as POLICY_EXCEPTION but the pipeline classified as SOBER_LIVING_GROUP_HOME_ZONING (7 cases), and pipeline residual categories (DISCRIMINATION_PRIMARY, UNDETERMINED) that Haiku refined into specific categories (4 cases). Neither direction predominated.

**Merits_reached classification rule.** The extraction enforced a stage-dependent rule for merits_reached: at the motion-to-dismiss or § 1915 screening stage, *Iqbal*/*Twombly* and nexus-failure dismissals were classified as merits_reached=NO (the court assessed pleading sufficiency, not the substantive legal standard); at the summary judgment or trial stage, all outcomes were classified as merits_reached=YES (the court evaluated the evidentiary record against the substantive elements of the claim, even if the plaintiff lost). This distinction is critical for separating pro se pleading failures from substantive merits losses.

**Cost.** The Haiku extraction cost approximately $17.58 via the Batch API (50% discount): 26.4M input tokens + 1.7M output tokens.

**Pilot iterations and re-coding.** The RA Database was assembled in stages. Pilot iterations (v1–v3, n=802–1,029) refined the classification schema and the search methodology, but their single-model classification (Claude Sonnet 4.6) was cost-prohibitive at scale. The final design (v4, n=1,857) adopted the triple-model pipeline described above (MiniMax, DeepSeek, Kimi via OpenRouter), which is cheaper and gains reliability through consensus. The pilot iterations were discarded and their cases fully re-coded under v4; v4 supplies every statistical claim in this Note.

## A.3 2015 FHA Database (n=1,496) — Disability Enforcement Cases

**Source documents.** The corpus comprises 1,661 case texts from two sources: 1,446 opinions downloaded from the CourtListener REST API using the same automated pipeline as the RA Database (the exact phrase "fair housing act" across all federal courts) with a filing-date filter of January 1, 2015 (see Section A.1.1 for rationale), and 215 supplemental opinions identified through Google Scholar to capture cases not indexed in CourtListener. The search downloaded all FHA opinions regardless of protected class; the § 3604(f) disability narrowing was performed during screening and classification.

**Screening.** Each of 1,661 downloaded case texts was screened for FHA relevance using Google Gemini 3.1 Flash Lite at zero temperature. 1,496 cases (90.1%) passed the relevance filter; 165 were excluded as non-FHA.

**Classification pipeline.** The same triple-model classification pipeline used for the RA Database v4, with independent classification by MiniMax M2.7, DeepSeek V3.2, and Kimi K2.5 (via OpenRouter API), followed by tiered consensus resolution:

| Resolution Method | Records | Percentage |
|-------------------|---------|------------|
| Unanimous (all 3 agree on every field) | 48 | 3.2% |
| Majority (non-critical field dissent only) | 271 | 18.1% |
| Majority (critical field dissent, 2-of-3 trusted) | 435 | 29.1% |
| MiniMax tiebreaker (non-critical 3-way splits) | 171 | 11.4% |
| MiniMax tiebreaker (critical 3-way splits) | 571 | 38.2% |
| **Total FHA-relevant** | **1,496** | **100%** |

Unlike the RA Database, three-way splits in the 2015 FHA Database were resolved using the MiniMax model as tiebreaker rather than Anthropic model adjudication. The three-way-split rate (49.6%) is comparable to the RA Database's 53.8% adjudication rate, reflecting similar classification ambiguity across the two corpora. Field-level agreement rates: outcome 68.3% unanimous, accommodation_type 38.0%, disability_category 50.7%, court 93.3%, year 97.5%.

**Coding protocol.** The same thirty-key output schema as the RA Database v4, with identical controlled vocabulary. The unified database contains canonical values for all fields, with an audit trail preserving all three model-specific values.

**Normalization.** Free-text fields (race_if_mentioned, subsidy_program, defendant_type, disability_category) were normalized to controlled vocabulary using a separate normalization pipeline that maps synonyms to canonical categories (e.g., "African American" → "Black"; "Section 8" / "Housing Choice Voucher" → "SECTION_8_HCV").

## A.4 FHA Pilot Database (n=331)

**Search methodology.** Cases were downloaded from the CourtListener REST API using a query requiring all three terms — "fair housing act," "race," and "zoning" — across all federal courts, over a search period running 2012 through 2026. The query was designed to investigate the intersection of racial zoning disputes and Fair Housing Act enforcement, and specifically whether race-based exclusionary zoning claims produced different litigation outcomes than other FHA theories. What the resulting dataset showed instead was disability-based reasonable accommodation claims dominating the federal docket, with distinctive enforcement patterns the race-and-zoning framing did not capture. That finding sent the research toward § 3604(f)(3)(B) and the post-*Loper Bright* period, and prompted the construction of the RA Database and 2015 FHA Database described above.

**Coding protocol.** The same schema as the RA Database, with additional fields for protected class identification and *Iqbal* citation tracking. Because the pilot query captured cases across all FHA protected classes (not limited to disability), this database enabled cross-class comparisons — particularly the *Iqbal* citation disparity analysis — that the disability-only RA Database could not support.

**Protected-class distribution.** Of the 331 pilot cases, disability-based claims constituted 38.1% (n=126) — the largest single category — compared with race at 30.8% (n=102), despite search terms requiring "race" and "zoning." This unexpected dominance of disability claims prompted the dedicated disability analysis that became this Note.

| Protected Class | n | Share of Cases |
|----------------|---|----------------|
| Disability | 126 | 38.1% |
| Race | 102 | 30.8% |
| Sex | 26 | 7.9% |
| Familial Status | 25 | 7.6% |
| National Origin | 22 | 6.6% |
| Unclear | 17 | 5.1% |
| Religion | 13 | 3.9% |

HUD administrative complaint data shows disability at **54.6%** of all complaints (2024), versus 15.58% for race. That the pilot database's 38.1% litigation share falls below the administrative complaint share admits two readings: disability claims may be less likely to reach federal court, or the pilot's "race" and "zoning" search terms may simply over-represent race-related cases and so understate disability. The RA Database (Section A.2), built on a broader "fair housing act" query without race or zoning restrictions, gives a more representative cross-class distribution: disability 59.1%, race 22.8%.

## A.5 Deduplication and Unified Dataset Construction

The RA Database (2,366 source documents) and 2015 FHA Database (1,661 source documents) were deduplicated by source file to produce 3,198 unique cases; a refresh pulled July 3, 2026 re-ran the original CourtListener v4 query (the exact phrase "fair housing act," all federal courts, all precedential statuses including unknown) over the full January 1, 2022 – July 1, 2026 window, yielding new federal opinions after cluster-ID deduplication, of which 168 passed the FHA relevance screen and were appended to the unified database (tagged `database_sources = ["p3ext_20260703"]`), bringing the T0 raw corpus to 3,366. A cluster-ID audit identified 35 distinct later opinions wrongly removed by name-based deduplication; they were restored and coded identically, and they make up 35 of the 168 (the other 133 came from the initial pull). The refresh increment is CourtListener-only — no subscription-database cross-checks, PACER fills, or Google Scholar supplement — and was classified by replicating the classification pipeline stage-for-stage via OpenRouter. The combined original corpus was subjected to per-claim structured extraction via Haiku 4.5 Batch API. Five records dropped from the per-claim extraction pass for parser failures or empty source text, producing a per-claim dataset of 3,193 cases and 6,718 claims; the dropped records remain in the case-level T0 corpus for case-level analyses. All case-level statistical claims in this Note use the 3,366-case T0 corpus or its T1/T2 sub-tiers; per-claim claim-level statistics use the 3,193-case sub-corpus.

The unified dataset contains 4,464 FHA claims and 2,254 non-FHA claims. Theory distribution among FHA claims: DISPARATE_TREATMENT 1,731 (38.8%), REASONABLE_ACCOMMODATION 1,257 (28.2%), RETALIATION 601 (13.5%), DISPARATE_IMPACT 392 (8.8%), INTERFERENCE_COERCION 243 (5.4%), UNCLEAR 168 (3.8%), DESIGN_AND_CONSTRUCTION 72 (1.6%).

**Defendant type distribution** (N=3,193 cases): OTHER 800 (25.1%), PROPERTY_MANAGEMENT 755 (23.6%), MUNICIPALITY 624 (19.5%), PRIVATE_LANDLORD 384 (12.0%), HOUSING_AUTHORITY 287 (9.0%), HOA_CONDO 267 (8.4%).

**Race mentioned**: 1,024 of 3,193 cases (32.1%).

## A.6 Cost and Reproducibility

| Pipeline Stage | Model | Records | Estimated Cost |
|----------------|-------|---------|----------------|
| Screening | Gemini 3.1 Flash Lite | 2,366 | *See note below* |
| Triple classification | MiniMax M2.7 ($14.85) + DeepSeek V3.2 ($31.33) + Kimi K2.5 ($39.41) (via OpenRouter) | 1,857 x 3 | $85.59 |
| Partial model evaluation (GLM-5) | GLM-5 via OpenRouter (partial run, not used in final pipeline) | — | $49.32 |
| Tier 3 adjudication | Claude Haiku 4.5 (Anthropic Batch API) | 697 | *See note below* |
| Tier 4 adjudication | Claude Sonnet 4.6 (Anthropic Batch API) | 302 | *See note below* |
| **OpenRouter subtotal** | | | **$134.91** |
| **Total (all providers)** | | | **$134.91 + Gemini + Anthropic Batch** |

*Note: OpenRouter API costs were extracted from the provider activity export dated March 28, 2026 (12,290 generation records). A partial GLM-5 (Zhipu) evaluation was not used in the final pipeline: its outputs entered neither the consensus pipeline nor any statistical claim. The $49.32 is the cost of that partial run, and the 12,290 generation records in the OpenRouter export include it alongside the triple-model classification passes. Gemini 3.1 Flash Lite screening costs (Google API) and Anthropic Batch API adjudication costs are billed separately and are not included in the OpenRouter total. Gemini Flash Lite pricing at the time of the screening run was approximately $0.01–0.02 per 1M input tokens; the screening stage's total token volume (2,366 documents × average prompt length) places the estimated screening cost below $5. Anthropic Batch API costs for Haiku 4.5 and Sonnet 4.6 adjudication were billed through the Anthropic console and are not itemized in the OpenRouter export.*

The final dataset is committed at `data/FHA_Unified_Database.json`; opinion source texts are redistributable only to the extent documented in `DATA_PROVENANCE.md`; the consolidation code and the audit database preserving all model-specific outputs are available from the author. The classification prompts are reproduced in Appendix K. The adjudication model's field-by-field reasoning is preserved in the `_adjudication_reasoning` metadata field of each adjudicated record, enabling post-hoc review of every resolution decision.

## A.7 Known Limitations

1. **Convenience sampling.** The unified dataset is a convenience sample drawn from published and electronically available opinions, not census data. Cases resolved through settlement, unpublished orders, or state courts are excluded. The dataset cannot claim representativeness of all disability FHA litigation.

2. **Production extraction schema.** All statistical claims in this Note use the v4 extraction schema exclusively; the pilot extractions (v1–v3) were discarded before analysis.

3. **Accommodation type classification.** Approximately 30% of v4 cases received a specific accommodation-type classification; the remainder were classified as DISCRIMINATION_PRIMARY (24.5%), OTHER (12.6%), or UNDETERMINED (32.8%), reflecting cases where discrimination rather than accommodation was the central claim or where the accommodation type could not be determined from the opinion text. The supplemental per-claim extraction (Section A.2.7) revealed that 68.1% of the database contains no reasonable accommodation claim at all, explaining much of the residual-category concentration. Accommodation-type analyses therefore appear in two forms: the per-case accommodation-type table at Appendix E.1 (computed on T2 decided cases; the current Note cites § E.1 only for the grounds on which no outcome analysis is reported), and the per-claim RA-merits analyses (175 claims within the T2 disability population; the full-corpus RA-merits population is 367 claims; see Section A.2.7 and Appendix A-3 § D).

4. **UNDETERMINED values (v4).** UNDETERMINED rates by field: disability_category 55.1%, accommodation_type 32.8%, housing_type 15.5%, defendant_type varies. The high disability_category UNDETERMINED rate reflects many opinions that do not specify the plaintiff's particular disability. The per-claim extraction confirmed that 52.1% of cases involve no disability allegation at all, explaining the high UNDETERMINED rate.

5. **No regression adjustment.** All win rates are unadjusted bivariate comparisons. Confounders including defendant type, circuit, procedural posture, time period, and accommodation type have not been isolated through multivariate regression. Descriptive patterns should not be interpreted as causal. (Multivariate regression results are reported separately in Appendix A-3.)

6. **Full population parameters unknown.** Without knowing the total universe of disability FHA cases filed in federal court during the study period, selection bias cannot be ruled out.

7. **50,000-character truncation.** The truncation applied to longer opinions means that analysis in the middle sections of lengthy decisions may be lost, though the head-and-tail preservation strategy retains the caption, introduction, and conclusion where courts typically state their holdings.

8. **Claim-mix composition (bears on RA-specific analyses only).** The FHA relevance screen (Gemini Flash Lite) passed 1,857 cases as FHA-relevant; the per-claim extraction (Section A.2.7) found that 755 (31.9%) contain a reasonable accommodation claim, while the remaining 68.1% involve disparate treatment, retaliation, design-and-construction, or non-FHA claims. That mix is by design for the Note's analysis — the T2 disability population deliberately includes non-RA disability claims — but it means RA-specific statistics must be computed on the RA populations rather than the full corpus. Human validation of 20 randomly sampled cases with model disagreements confirmed the mix: 7 of 20 (35%) were not RA cases, including design-and-construction consent decrees, pure racial discrimination claims, and insurance disputes with no housing nexus. The three-population segmentation described in Section A.2.7 enforces the discipline by computing RA-specific statistics only on the merits-RA population.

9. **Pro se pleading failure population — denominators differ across analyses.** The per-claim extraction identified 1,643 pro se cases (51.5% of the 3,193-case per-claim sub-corpus, including non-decided outcomes), with a win rate of 0.9% compared to 9.1% for represented plaintiffs (1,550 cases) under that broad denominator. Appendix A-3 § C.2 uses the regenerated dated-decided three-period representation rates as the current support surface; any superseded denominator pair must be re-derived from the current dataset, with exact code and denominator documentation, before it is cited. The 0.9% / 9.1% pair captures the all-FHA, all-outcomes denominator and is presented for cross-class comparison only. *Iqbal*/*Twombly* dismissals account for 1,433 claims (32.1% of FHA claims, or 21.3% of all 6,718 claims), confirming the centrality of the motion-to-dismiss stage as the primary gatekeeping mechanism.

10. **Design-and-construction unit-of-analysis disclosure.** Three different D&C counts appear in the data because they measure different units of analysis:
    - **Per-case primary-claim-type field** (Appendix E.4): n=31 cases where Design & Construction is the case's *primary* legal theory, with 48.4% strict / 71.0% broad win rates on the current run; an archived earlier run of the same field returned n=30 with 46.7% / 70.0%.
    - **Claim-level, per-claim extraction** (Section A.2.7): 72 D&C claims (1.6% of FHA claims) appear in the per-claim sub-corpus, of which 18 reached merits adjudication with a 27.8% plaintiff success rate. Cases may contribute multiple claims; case-level totals are smaller than claim-level totals.
    - **Disability-restricted, claim-level** (this limitation): 42 D&C claims appear within the T2 disability population, of which 9 reached merits adjudication, achieving a 22.2% plaintiff success rate (95% CI: 6.3%–54.7%).

    The current Note prints no D&C outcome statistic (its fn 86 reports no claim-specificity outcome analysis); the per-case primary-claim-type figure and the claim-level totals are reported in the appendix suite for completeness only.

11. **Positional bias in multi-claim cases.** Full-text scanning revealed that 38.5% of cases mention two or more accommodation categories in the opinion text. In 14 informative cases where the first-mentioned and most-discussed accommodations differ, MiniMax anchored to the first-mentioned accommodation (57%) while Kimi anchored to the most-discussed (79%). The three-model ensemble partially self-corrects: the majority-vote canonical resolution favored the most-discussed accommodation 8:5 over the first-mentioned. Fisher's exact test (MiniMax vs. Kimi): OR=4.89, p=0.12 — suggestive but not significant at n=14. Pooled across all models, no overall positional bias was detected (binomial test: 18 first vs. 22 most, p=0.64).

These limitations notwithstanding, the triple-model-with-adjudication methodology improves on single-model classification. The supplemental per-claim extraction addresses the single-case-single-classification constraint, the most significant limitation, by decomposing cases into independent claims and enabling proper population segmentation. Unanimous agreement on objective fields runs to 97–99% (court, year), evidence that the models reliably extract factual information; the tiered adjudication process then routes genuinely ambiguous classifications to a more capable model for resolution.

## A.8 Classification Prompts

The FHA relevance screening prompt and case classification prompt constitute the instruments used to generate all classification data in both databases. They are reproduced in full in Appendix K to enable replication. Cross-references to the prompt controlled vocabulary (e.g., "13 categories (see Section A.8.2)") refer to Appendix K.

---
