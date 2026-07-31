# Appendix M: Doctrinal Audit Methodology

**Cited by:** Note footnotes 87 (translation-family protocol), 141–142 (Part 121 reported-decision surface §§ M.2.1–M.2.2; annual-report audit), and 145 (transition-plan sweep). The 47-document AFH audit carries assurance level EXTENDED.
**Scope:** Methodology archive — audit-file pointers, coding rules, and validation layers; findings carry the evidentiary posture of the Note sites they support.
**Regeneration:** Not script-generated; each section names its underlying audit memorandum and run date.

## M.1 Overview

This Appendix documents the doctrinal and administrative-record audits cited in the footnotes of *Duty Without Data: Disability Fair Housing and the Record-Dependent Right* ([`manuscript/Duty_Without_Data.md`](../../manuscript/Duty_Without_Data.md)). It complements Appendix L (HUD Administrative Data) by specifically tying the Note's doctrinal footnote apparatus to the underlying audit memoranda, search strings, inclusion / exclusion rules, and data snapshots.

Every administrative-record claim these audits support relies only on cited Federal Register, OMB, Census / ACS, HUD, GAO, and OIG records (the litigation-database stakes evidence is documented separately in Appendices A–B and E–H). The sections below state, in terminal form, the query, run date, inclusion rule, and output on which each cited claim rests, so an independent reader can replicate the Note's quantitative and qualitative claims from the public sources without access to any private data.

**Record-to-section crosswalk.** The following audit records underlie the Note's footnote apparatus. The underlying working memoranda are retained in the project's private research records (see `../../replication/DATA_PROVENANCE.md`); this appendix's sections carry their terminal content, and rows below marked "retained privately" name the private record behind each section. Footnote keys of the form `I-D-part121` used below are stable symbolic anchors, not live manuscript footnote numbers (which are not stable across formatting and pagination); resolve them through this crosswalk and the repository-root `APPENDIX_CROSSWALK.md`:

| Underlying audit record | Note section | Appendix M section |
|---|---|---|
| `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 8 | Part I.E | § M.2.1 |
| `doctrinal_case_audits.md` (retained in the project's private research records) § 1 | Part I.E | § M.2.2 |
| `record/hud-27061/cfr_part121_analysis.md` | Part I.E | § M.3 |
| `methodological_audits_and_validation.md` (retained in the project's private research records) § 6 | Part I.E | § M.4 |
| `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 4 | Part I.A | § M.5 |
| `program_specific_accessibility_gaps.md` (retained in the project's private research records) § 1 | Part I.D | § M.6 |
| `design_construction_bottleneck.md` (retained in the project's private research records) § 4 | Part I.B | § M.7 |
| `historical_disability_data_record.md` (retained in the project's private research records) § 1 | Part I.E | § M.8 |
| `program_specific_accessibility_gaps.md` (retained in the project's private research records) § 2 | Part III.B (module architecture) | § M.9 |
| `pro_se_doctrine_production_filter.md` (retained in the project's private research records) § 2 | Part II.E | § M.10 |
| `method/validation_kimi_k2_6/` + `method/validation_three_model/` + `method/validation_four_coder_full/` | Part II.E | § M.16 |
| `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 1 | Part I.A | § M.11 |
| `comparative_contextual_empirics.md` (retained in the project's private research records) § 3 | Part III.B (module architecture) | § M.14 |

---

## M.1.1 Canonical corpus-tier definitions (mechanism-divergence audit)

Several audits in this Appendix are computed on subsets of `data/FHA_Unified_Database.json`. To avoid ambiguity about which population each number refers to, the Note uses five canonical tiers, each expressible as a reproducible filter on the committed database:

| Tier | Label | Filter | n |
|---|---|---|---|
| T0 | Raw unified corpus | all records (union of RA Database + 2015 § 3604(f) Database by `source_file`) | 3,366 |
| T1 | Screened-in federal FHA cases | T0 AND `screening_result == "YES"` | 2,690 |
| T2 | Screened-in disability cases (primary disability-analysis population) | T1 AND (`protected_classes` contains `"disability"` OR `disability_alleged == True` OR `is_ra_case == True`) | 1,900 |
| T3 | Disability-wave tranche (fully classified) | T2 AND `date_filed >= 2022-01-01` | 1,347 |
| T4 | Pleading-loss universe | T2 AND `procedural_posture ∈ {MOTION_TO_DISMISS, SCREENING_ORDER}` AND `outcome ∈ {DEFENDANT_WIN, PROCEDURAL}` | 739 |

Tier counts reflect the corpus refresh through the July 1, 2026 endpoint (pulled July 3, 2026). T4 decomposes into disability-wave and pre-wave cases. The mechanism-divergence contingency test in Part II.C uses T4. The narrower filter `protected_classes` contains `"disability"` alone (without the `disability_alleged` or `is_ra_case` disjuncts) yields 1,849 — the 51-case gap is records flagged through `disability_alleged=True` or `is_ra_case=True` but lacking an explicit disability protected-class entry. The narrow 1,849 population is preserved as a sensitivity cohort. T2 (1,900) is the canonical disability-analysis population for all current statistical claims in this Note; all downstream subsets are nested within it.

---

## M.2 Federal-Opinion Citation-Count Audits

### M.2.1 24 C.F.R. Part 121 / DOJ § 3604(f)(3) joint audit

**File:** `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 8

**Run date:** April 18, 2026. **Re-run:** July 1, 2026 — a CourtListener full-text search returned no decision citing Part 121 or § 121.2 beyond the unpublished 1998 *ADAPT* footnote and roughly three dozen citing § 3614a (Note fn 141), and the 7,638-file archive sweep was re-run the same day (Note fn 83). **Westlaw re-verification, July 7, 2026:** a full-text search of all state and federal cases ("24 C.F.R." /5 121) returns seven decisions, every one a proximity artifact (docket-entry numbers, reporter citations, or unrelated parts such as 24 C.F.R. Parts 206/966/3280 and 14 C.F.R. Part 121); the sole decision referring to Part 121 itself remains the unpublished *ADAPT* footnote, and a § 121.2 KeyCite Citing References pull contains zero cases. A Citing References pull on § 3614a returns 37 cases. These verified counts control over the April as-run query yields below.

**Scope (two paired queries):**

1. *8-PDF Part 121 set.* The as-run yield (eight documents) of a subscription federal-opinion-database query targeting 24 C.F.R. Part 121 in a fair-housing or disability context. The July 7, 2026 Westlaw re-verification (above) shows this yield should be read as a query artifact, not as a population of opinions citing Part 121: only *ADAPT* genuinely refers to the regulation.
2. *39-PDF DOJ set.* A subscription federal-opinion-database query capturing the complete reported population of decisions in which the United States was a captioned party in an FHA § 3604(f)(3) matter.

**Inclusion rule.** All reported federal opinions returned on each query with at least one substantive opinion text. Unpublished dispositions without opinion text are excluded. Subsequent history (aff'd, rev'd) is reported on the primary decision.

**Coding.** Each opinion is coded for (i) whether "24 C.F.R. Part 121" (or "Part 121") appears substantively, in a footnote, or not at all; (ii) whether 42 U.S.C. § 3614a is cited; (iii) whether the United States litigated a § 3604(f)(3) claim; (iv) the disposition of any Part 121 / § 3614a argument.

**Headline findings supporting footnotes:**

- Across the 47-opinion combined population (1978–2025), "24 C.F.R. Part 121" appears substantively in exactly one opinion — *ADAPT v. HUD*, 1998 WL 113802, at *6 n.20 (E.D. Pa. Mar. 12, 1998), where it is dismissed as "meritless." (Note footnotes `I-D-part121`, `I-D-adapt`, `I-D-other7`.)
- 42 U.S.C. § 3614a is cited exactly twice — *Noble Homes*, 173 F. Supp. 3d 568, 572 (N.D. Ohio 2016); *Scott*, 788 F. Supp. 1555, 1559 n.6 (D. Kan. 1992) — each time in a non-enforcement posture. (Note footnote `I-D-doj-zero`.)
- The remaining seven documents in the as-run query yield are false-positive or tangential hits that do not engage Part 121 substantively, and none engages § 121.2's enumeration of handicap or family characteristics. The July 7, 2026 Westlaw verification confirms no reported decision cites Part 121 as a substantive obligation. (Note footnote `I-D-other7`.)

### M.2.2 42 U.S.C. § 3614a audit

**File:** `doctrinal_case_audits.md` (retained in the project's private research records) § 1

**Run date:** April 18, 2026.

**Scope.** A subscription federal-opinion-database query whose as-run yield was 42 federal opinions citing 42 U.S.C. § 3614a. (The July 7, 2026 Westlaw Citing References pull returns 37 cases — the Note's "roughly three dozen," fn 141; counts vary with database and query form.)

**Inclusion rule.** All reported federal opinions returning the `3614a` citation string. Statutory-list recitations and deferential-framework boilerplate are retained but separately coded.

**Coding.** Each opinion is classified into one of four categories: BOILERPLATE (35 of 42) — § 3614a recited in a list of statutory grants with no substantive engagement; SUBSTANTIVE (2–3 of 42) — § 3614a invoked in reasoning about HUD's rulemaking authority; PARENTHETICAL (1 of 42 — *Snyder*) — § 3614a appears in a quoted statutory-text parenthetical; BACKGROUND (remainder) — non-substantive reference. Zero opinions in the 42-case set cross-cite Part 121 as the instrument implementing § 3614a.

**Headline finding (supports the Note's Part I.E § 3614a citation-pattern discussion).** An enforcement-live statute would show one-to-several substantive invocations per year and cross-citation to its implementing regulations. Neither shows up here. Read alongside the DOJ zero-invocation sweep in M.2.1, the thin reported-decision surface is consistent with the Note's finding of fragmented, program-specific implementation. (Part I.E claims no specific 5:1–100:1 citation-ratio benchmark; the pattern is offered descriptively.)

---

## M.3 24 C.F.R. Part 121 Text-and-History Verification

**File:** `record/hud-27061/cfr_part121_analysis.md`

**Sources combined.**

- eCFR snapshots of 24 C.F.R. Part 121 at three reference points: 2017 edition, September 27, 2022, and the current edition (April 2026).
- Federal Register publication history for Part 121: 54 Fed. Reg. 3,278, 3,317 (Jan. 23, 1989), and subsequent non-substantive codification entries.
- reginfo.gov ICR history for HUD information collections cross-referencing 24 C.F.R. Part 121.
- a federal-opinion-database query universe for text-level verification.

**Verification findings supporting note footnote `I-A-121-2` (and `I-A-121-2-text`).**

- Part 121 contains only § 121.1 (purpose) and § 121.2 (operative furnishing provision).
- § 121.2 enumerates "race, color, religion, sex, national origin, age, handicap, and family characteristics" as the categories program participants "shall furnish . . . such data . . . as the Secretary may determine to be necessary or appropriate."
- The 2017, 2022, and current eCFR snapshots are textually identical. Part 121 has not been materially amended since the 1989 Final Rule.
- § 121.2 is the only HUD rule that enumerates both handicap and family characteristics in a single data-collection command.

**Interpretive note.** The "necessary or appropriate" qualifier attaches to the Secretary's discretion over collection design and weighs against a § 706(1) compulsion remedy. The regulatory enumeration supplies the predicate for § 706(2)(A) review of the 2023 reversion. Parts I.A and III.C reflect this reading and do not treat § 3608(e)(6) as textually free of the qualifier.

---

## M.4 2022–2023 HUD-27061 PRA Cycle Record

**File:** `methodological_audits_and_validation.md` (retained in the project's private research records) § 6

**Sources.**

- 87 Fed. Reg. 58,524 (Sept. 27, 2022) — 60-Day Notice announcing intent to update Form HUD-27061 to "collect protected class data as required by the Fair Housing Act and HUD regulations at 24 CFR 121" and inviting comment on "particular data fields."
- 87 Fed. Reg. 71,432 (Nov. 22, 2022) — 30-Day Notice.
- 88 Fed. Reg. 32,089 (May 18, 2023) — Final Notice reverting to the narrower instrument.
- reginfo.gov ICR 2535-0113 supporting statements, public comments, and PRA approval history for the 2022–2023 cycle.
- Public comments from AAPD, SAGE, Williams Institute, and others.

**Verification findings.**

- The 8,625-hour annual PRA respondent-burden estimate is identical in the 2022 proposal and the 2023 reversion. Neither notice identifies increased PRA respondent burden as the reason for narrowing the instrument. (This is the empirical spine of the Note's *State Farm* argument in Part III.C.)
- The 2022 60-Day Notice expressly invokes "24 CFR 121" and expressly invites comment on "particular data fields." The 2023 Final Notice provides no paragraph-level explanation of why the disability and family-characteristics fields were not included in the final instrument.

---

## M.5 AFFH-T Disability-Visualization Gap

**File:** `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 4

**Sources.**

- U.S. Dep't of Hous. & Urban Dev., *AFFH Data and Mapping Tool User Guide*, v4.0 (July 2017).
- U.S. Dep't of Hous. & Urban Dev., *AFFHT0007 Data Documentation* (Aug. 2024).
- HUD AFFH-T endpoint `egis.hud.gov/affht/` (status check performed during audit).

**Coding rule.** Each map and each table in the AFFH-T is coded as (i) race-bearing, (ii) disability-bearing, or (iii) general/geographic. Opportunity-indicator cross-tabulations are coded on whether a disability-axis analog exists.

**Findings supporting note footnote `II-C-affht`.**

- Race-bearing map layers: 22. Disability-bearing map layers: 5 (raw layer-count ratio 4.4:1). On the weighted-granularity count (45 race-bearing layer-variants over 9 disability-bearing, per the deep-dive workbook), the ratio is 5:1.
- Maps 1–13 and 16–17 are race-or-general. Maps 14–15 are disability-standalone. There is no Map-14/15 disability cross-axis analog of the Maps 1–13 race cross-tabulations.
- Tables 1–12 use race cross-tabulation axes. Tables 13–15 are disability-standalone. There is no "Opportunity Indicators by Disability" analog to Table 12 "Opportunity Indicators by Race/Ethnicity."
- Tool endpoint returned HTTP 503 at audit date — consistent with the Note's point that the architectural gap persists beyond access windows.

---

## M.6 NSPIRE / UFAS § 504 Crosswalk

**File:** `program_specific_accessibility_gaps.md` (retained in the project's private research records) § 1

**Sources.**

- HUD, *NSPIRE Final Standards* (Apr. 2023).
- 24 C.F.R. Part 8 (§ 504 regulations) and Uniform Federal Accessibility Standards (UFAS).
- HUD REAC inspection score datasets (public housing and multifamily; see Appendix L.3).

**Coding rule.** 17 consolidated UFAS / § 504 accessibility-requirement categories are cross-walked against the NSPIRE inspection manual. Each category is scored FULL (NSPIRE inspects the category), PARTIAL (NSPIRE inspects a component, not the full standard), or NONE (NSPIRE does not inspect).

**Findings supporting note footnote `II-D-crosswalk`.**

| Category | Score | Count |
|---|---|---|
| FULL | 0 | 0 / 17 (0%) |
| PARTIAL | 4 | 4 / 17 (23.5%) — accessible routes / ramps, elevators, grab-bar secureness, alarms |
| NONE | 13 | 13 / 17 (76.5%) |

**Caveat.** The crosswalk measures inspection-protocol coverage only. Some on-site inspectors may observe uncoded accessibility conditions during visits; the published schema does not record such observations. See Appendix L.3 verification that no accessibility field exists in the published REAC/NSPIRE score dataset schema.

---

## M.7 Part 8 Stock-Level Verification Gap and Pre-1991 Stock Hardening

**File:** `design_construction_bottleneck.md` (retained in the project's private research records) § 4

**Sources.**

- 2023 American Community Survey 5-Year, Table B25034 (year-built) and Table B01003 (total population), joined by MSA GEOID.
- U.S. Dep't of Hous. & Urban Dev., *A Picture of Subsidized Households: 2024* (POSH; snapshot Dec. 31, 2024).
- Luke Bo'sher et al., *Accessibility of America's Housing Stock: Analysis of the 2011 American Housing Survey*, U.S. Dep't of Hous. & Urban Dev., Off. of Pol'y Dev. & Rsch. (2015).
- U.S. Gov't Accountability Office, *Housing Assistance: HUD Should Improve Data Collection on Accessibility of Rental Housing for People with Disabilities*, GAO-23-105083 (Apr. 2023).

**Derivation of the illustrative verification gap (supports the Note's stock-level verification-gap discussion, Part I.B).** Project-based federally assisted pool of 2,346,974 units (Public Housing + PBS8 + Sections 202/811) is drawn from POSH 2024Q4. § 8.22(b) 5% new-construction floor applied to that pool yields 117,349 units. Applying the 0.15%–3.8% band from the 2015 Bo'sher study to the 2,346,974-unit pool yields an illustrative gap of roughly 28,000 to 114,000 units (28,164–113,829 as computed) against the § 8.22 5% target. The range is reported not as a violation count but as an **illustrative verification gap**: the order-of-magnitude range that remains unresolved because HUD does not publish a Part 8-specific accessible-unit count. The GAO-23-105083 PHA self-reported medians (6% fully accessible in Public Housing; 9% in PBRA) are reproduced for comparison but flagged as unverified.

**Derivation of the 65.1% pre-1991 stock share supporting note footnote `II-E-65pct`.** 2023 ACS 5-Year Table B25034 is re-weighted within the 1990–1999 decade bin using coefficient 437/3,652 = 0.1197 to isolate the pre-March-1991 portion. Applied across all year-built bins, the within-decade-adjusted pre-March-1991 share is 65.1% of the national housing stock.

**Top-50 MSA statistics (carried in repository; not cited individually).** 2023 ACS 5-Year Tables B25034 and B01003 joined on MSA GEOID yield a top-50 MSA unit-weighted pre-March-1991 share of 65.8%, with a mean of 61.5% and a median of 61.0%. Representative shares: 84.7% Buffalo–Cheektowaga; 83.0% Providence–Warwick; 82.4% New York–Newark–Jersey City; 81.3% Los Angeles–Long Beach–Anaheim; 78.4% Boston–Cambridge–Newton.

**Conventions.** The Note names this figure the "stock-level verification gap" and explicitly flags it as illustrative, not a compliance-violation estimate. The Note's core diagnostic is that HUD does not publish a Part 8-specific accessible-unit count; the quantity range is secondary.

---

## M.8 1988 FHAA Legislative-History Disability-Data Preamble

**File:** `historical_disability_data_record.md` (retained in the project's private research records) § 1

**Sources.**

- 54 Fed. Reg. 3,278, 3,278–79 (Jan. 23, 1989) (preamble).
- H.R. Rep. No. 100-711 (1988).
- Relevant committee-report passages discussing disability-data integration into HUD's administrative collections under the 1988 Fair Housing Amendments.

**Content.** Collects and verifies the preamble passages that commit HUD to disability-data collection as an implementation component of the 1988 Amendments, with cross-references to the committee report.

**Use in note footnote `I-A-preamble`.** Supports the Note's claim that the 1989 codification of handicap and family characteristics in § 121.2 was not a drafting accident: the operative preamble language frames the enumeration as an implementation response to the 1988 Amendments.

---

## M.9 LIHTC QAP Accessibility — 51-Jurisdiction Audit

**File:** `program_specific_accessibility_gaps.md` (retained in the project's private research records) § 2

**Sources.** Qualified Allocation Plans (QAPs) for the 2025–2026 LIHTC cycle for all 51 jurisdictions (50 states + D.C.).

**Coding rule.** Each QAP is classified into one of four categories with respect to § 504 / disability accessibility:

- **Exceeds 504** — QAP imposes accessibility requirements beyond 504 (e.g., 20% Type-A / accessible-unit set-aside).
- **Requires 504** — QAP references § 504 / Part 8 as a condition precedent without exceeding it.
- **Incentives only** — QAP offers scoring incentives for accessibility but does not require it.
- **None** — QAP does not reference § 504 / accessibility at all.

**Findings supporting note footnote `II-E-qap`.**

- Exceeds 504: 2 (Oregon, Pennsylvania; both 20% Type-A / accessible).
- Requires 504: 26.
- Incentives only: 7.
- None: 13.

48 non-error records are classified above; 7 jurisdictions are flagged for manual review. Only two of 51 jurisdictions exceed § 504. That distribution supports the Note's feeder-program insight that stock-level accessibility is largely a floor-compliance regime at the LIHTC level.

---

## M.10 Pro Se Mechanism Divergence — 739-Case Pleading Universe

**File:** `pro_se_doctrine_production_filter.md` (retained in the project's private research records) § 2

**Sources.**

- FHA Unified Database: raw union n = 3,366; screened-in n = 2,690; disability population n = 1,900 (see Appendix A and data/dictionaries/fha_unified_database.md for tier definitions). 1,347-case dated disability-wave tranche (T2 AND `date_filed >= 2022-01-01`) fully classified.
- 739-case pleading-loss universe, constructed within T2 as disability-wave cases plus pre-wave cases, all with pleading-stage dispositions (`procedural_posture ∈ {MOTION_TO_DISMISS, SCREENING_ORDER}` AND `outcome ∈ {DEFENDANT_WIN, PROCEDURAL}`).

**Coding rule.** Each MTD/12(c) loss is assigned to one of nine mechanism families. Primary mechanism-family classification is performed by a three-model majority-vote ensemble (Kimi K2.6 + GLM-5.1 + DeepSeek V3.2) on 728 of 739 cases — the original 668 plus 60 rows added by the July 2026 corpus refresh, coded with the same frozen prompt and models (11 cases dropped for unparseable model output or as a pre-refresh residual uncoded row). An alternate two-model Kimi K2.5 + GLM-5.1 consensus on the original 676-case universe is preserved as a backward-compatibility check. Mechanism families include TRANSLATION (plaintiff failed to identify the operative legal theory), PROCEDURAL_GATEWAY (exhaustion, standing, ripeness), and seven others. Cases may appear in multiple families; the primary family is used for the contingency table.

**Findings supporting note footnotes `intro-translation` and `II-F-mech` (current primary coding).**

- TRANSLATION-family share: 45.3% pro se (286/632) vs. 13.7% represented (13/95).
- PROCEDURAL_GATEWAY-family share: 18.5% pro se (117/632) vs. 32.6% represented (31/95).
- 2 × 2 contingency on the gap: χ²(1) = 32.70; p = 1.1 × 10⁻⁸; 95 % CI on gap [23.64, 39.50] pp.
- Family × representation contingency: χ²(8) = 72.07; p = 1.9 × 10⁻¹²; Cramér's V = 0.315 (n = 727; 1 unknown-representation row excluded).
- Fleiss' κ across the three primary coders (bucket level, n = 728): 0.6297 (substantial).

The convergent-validation bracket of 29 – 32 pp across all coding variants is documented in M.16.

**Framing.** Parts II.E–F present this pattern as contextual stakes evidence, not as the legal predicate for a remand remedy. The TRANSLATION concentration is explicitly not offered as the *State Farm* predicate; the reasoned-engagement obligation attaches to the § 553(e) petition record (Part IV).

---

## M.11 47-AFH Analysis of Impediments Disability Audit

**File:** `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 1

**Sources.** 47 publicly available Analyses of Impediments (AIs), Assessments of Fair Housing (AFHs), and equivalent fair-housing-planning documents. Sampling is purposive (large jurisdictions + illustrative mid-size jurisdictions) and not representative of the national AFH universe.

**Coding rule.** Each AI / AFH is coded for: (i) presence of a disability section; (ii) presence of quantitative disability goals; (iii) presence of accessible-unit inventory; (iv) comparative depth of disability analysis versus race analysis.

**Findings supporting note footnote `II-F-afh`.**

| Metric | Count | Share |
|---|---|---|
| Disability section present | 45/47 | 95.7% |
| Quantitative disability goals | 13/47 | 27.7% |
| Accessible-unit inventory | 11/47 | 23.4% |
| Race analysis deeper than disability | 46/47 | 97.9% |

Representative illustrative example: Lake County, Indiana, *Assessment of Fair Housing* (Nov. 2017 final) ("Nearly seven percent of the population of the jurisdiction has an ambulatory disability, yet there is known accessible accommodation for fewer than 300 people.").

**Caveat.** Sampling is purposive, not stratified-random. The audit establishes an existence pattern, not a population-level estimate.

---

## M.12 HUD Annual Report Longitudinal Audit (FY 1989 – FY 2023)

**File:** `hud_administrative_record_deep_dives.md` (retained in the project's private research records) § 5

**Sources.** HUD Office of Fair Housing and Equal Opportunity (FHEO) annual reports on fair housing, FY 1989 through FY 2023. Coverage gap: FY 1992–2002 reports unrecovered.

**Coding rule.** Each recovered annual report is coded for: (i) number of disability / handicap complaint bases reported; (ii) disability share of total complaint bases; (iii) table schema (which cross-tabulations are presented).

**Findings (carried in repository as methodology archive).**

- FY 1989: 713 handicap bases at 19% share of total bases.
- FY 2018: disability share rises to 60.4%.
- FY 2023: 5,128 disability complaint bases.
- Schema instability: no two consecutive reports use identical cross-tabulation tables; FY 1992–2002 reports are unrecovered.

**Use in Note.** Part I.E presents the disability share trajectory (19% → 60.4%, with FY 2023 at 5,128 disability bases) alongside the point that no recovered annual report discloses a Part 121 collection. Part III.B uses the schema-instability finding to support the feasibility of a stable disaggregation module.

---

## M.13 Disclosure-Effect Meta-Analysis

**File:** `comparative_contextual_empirics.md` (retained in the project's private research records) § 4

**Sources.** Federal Reserve Board, *Annual Report on the Home Mortgage Disclosure Act* (annual series). Peer-reviewed disclosure-effect literature on HMDA, FCRA, and related financial-disclosure regimes.

**Content.** Reviews empirical estimates of the disclosure-effect magnitude under HMDA's "sunshine" architecture (annual lender outlier-screening referrals averaging ≈ 200 lenders). Synthesizes estimates across the disclosure-effect literature to anchor the Note's claim in Part III.B that a HUD-disability-data disclosure layer would have a non-zero deterrent effect.

**Use in note footnote `IV-A-hmda`.** The HMDA referral rate (≈200 lenders/year) is offered as an anchor, not as a quantitative prediction about what a HUD-disability-data disclosure layer would yield. Part IV explicitly disclaims that the HMDA analog is a cost or effect forecast.

---

## M.14 Australia SDA Comparative Note

**File:** `comparative_contextual_empirics.md` (retained in the project's private research records) § 3

**Source.** National Disability Insurance Agency, *Annual Report 2022–23* (Australia Specialist Disability Accommodation program).

**Content.** Summarizes the Australian SDA administrative architecture: nationally standardized accommodation-tier definitions, property-level registration, and participant-payment linkage. Reports aggregate registration counts, participant counts, and provider counts.

**Use.** The Note's comparator discussion (Part III) references SDA among the systems showing that disability-data collection is administrable, and the SDA figures serve as the peer-jurisdiction existence proof supporting the Note's Part IV phased-implementation discussion. The Note does not recommend cloning SDA; the comparative use is bounded.

---

## M.15 Reproducibility Convention

- **Snapshot discipline.** The Note reports the audits' run dates (April 18, 2026; key citation sweeps re-run July 1, 2026 — see § M.2.1) and the ACS / POSH / NSPIRE snapshot dates directly in the footnotes. Where a number is computed from a rolling source (e.g., reginfo.gov), the Note reports the retrieval date.
- **No private data.** No claim in the Note's main text depends on any source outside the Federal Register, OMB / reginfo.gov, Census / ACS, HUD, GAO, and OIG records that the audit memoranda above identify.
- **Update path.** If any audit memorandum in this Appendix is revised, the revision should be reflected in (i) the Note's footnote carrying the file pointer, and (ii) this Appendix's corresponding section. The file-to-footnote crosswalk in M.1 is the canonical index.

---

## M.16 Primary Three-Model Ensemble Coding and Validation Layers for the TRANSLATION-Family Gap

**Files:**
- `method/validation_kimi_k2_6/agreement_report.md` (sample-level re-code)
- `method/validation_kimi_k2_6/agreement_results.json`
- `method/validation_kimi_k2_6/kimi_k2_6_raw_results.json`
- `method/validation_kimi_k2_6/run_kimi_k2_6.py`
- `method/validation_kimi_k2_6/compute_agreement.py`
- `method/validation_kimi_k2_6/mechanism_prompt.txt`
- `method/validation_three_model/ensemble_report.md` (full-universe ensemble)
- `method/validation_three_model/ensemble_results.json`
- `method/validation_three_model/kimi_raw_results.json`
- `method/validation_three_model/glm_raw_results.json`
- `method/validation_three_model/deepseek_raw_results.json`
- `method/validation_three_model/compute_ensemble.py`
- `method/validation_three_model/run_three_model.py`
- `method/validation_three_model/build_merged_summary.py` + `method/validation_three_model/mechanism_merged_summary.json` (merged 668 + 60-row July-2026 extension = 728-coded summary)
- `method/validation_four_coder_full/confirmation_report.md` (full-universe blind fourth-coder re-read)
- `method/validation_four_coder_full/fourth_coder_full_merged.json`
- `method/validation_four_coder_full/universe_668.json`
- `method/validation_four_coder_full/chunk_{01..22}_blind.json`
- `method/validation_four_coder_full/coder_seat_{01..22}_results.json`
- `method/validation_four_coder_full/aggregate_full.py`

**Purpose.** The Part II.F TRANSLATION-family pro-se / represented pleading-loss gap is the Note's empirical headline: pro se plaintiffs lose on TRANSLATION-family defects at a materially higher rate than represented plaintiffs across the 739-case pleading-loss universe (T4 in the M.1.1 tier framework). Because the gap is computed from mechanism-family codes that large language models produced, independent revalidation is a first-order reliability question. Primary mechanism-family classification under the current pipeline is the full-universe three-model majority-vote ensemble documented in M.16.2 below (Kimi K2.6 + GLM-5.1 + DeepSeek V3.2 on 728 of 739 cases — the original 668 plus 60 rows added by the July 2026 corpus refresh, coded with the same frozen prompt and models). Two further subsections wrap validation layers around that primary coding. One is a 150-case stratified Kimi K2.6 subset run (M.16.1), retained as a backward-compatibility check now that K2.6 is one of the three primary coders. The other is a full-universe blind fourth-coder re-read by 22 parallel Claude Opus 4.7 subagents, each reading the underlying opinion fresh (M.16.3); this is the primary external validation layer. The Note's Part II.F mechanism-coding footnote points here for the full methodology and summary statistics.

### M.16.1 Backward-compatibility — Sample-level Kimi K2.6 re-code against earlier K2.5 + GLM-5.1 coding

**Design.** A stratified random sample of 150 pleading-loss opinions was drawn from the 676-case T4 universe (101 pro se, 49 represented; strata proportional to the bucketed mechanism-family distribution across TRANSLATION / PROCEDURAL_GATEWAY / NO_FAILURE / OTHER). The sample was classified by `moonshotai/kimi-k2.6` via OpenRouter with reasoning tokens disabled and temperature 0.2, using the identical mechanism-family prompt used for the original coding (`method/validation_kimi_k2_6/mechanism_prompt.txt`).

Scope note: this layer predates the July 2026 corpus refresh (which added 60 of the 728 ensemble-coded rows); its sample and statistics are computed on the pre-refresh 676-case universe and are unchanged.

**Agreement statistics.**

| Metric | Value | Interpretation |
|---|---|---|
| Family-bucket Cohen's κ | **0.6264** | Substantial (Landis & Koch) |
| Atomic family κ | 0.5751 | Moderate |
| Atomic mechanism κ | 0.3508 | Fair |
| Exact family-bucket match | 74.0% | — |
| Exact atomic-family match | 69.3% | — |

**Within-family-bias diagnostic.** Because the 535-case disability-wave subset of T4 was originally classified by `moonshotai/kimi-k2.5` (a prior-generation Kimi model) and the 141-case pre-wave remainder by `z-ai/glm-5.1`, there is a theoretical concern that Kimi K2.6's agreement is inflated on the K2.5-origin cases. The per-original-classifier subset κ disposes of this concern:

| Origin | Sample n | K2.6 bucket κ |
|---|---|---|
| K2.5-origin subset | 112 | 0.6285 |
| GLM-5.1-origin subset | 38 | 0.6122 |

The two subset κ values are materially identical. If within-family agreement were driving the aggregate κ, they would diverge.

**Substantive-claim replay on the sample.**

| Coding | Pro-se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | χ²(1) | p |
|---|---|---|---|---|---|
| Original (K2.5 + GLM-5.1) | — | — | 21.93 | 5.60 | 0.018 |
| Kimi K2.6 re-code | — | — | **28.16** | **10.02** | **0.0016** |

The sample's TRANSLATION gap is larger and more statistically significant under independent K2.6 recoding than under the original coding.

### M.16.2 Primary coding — Full-universe three-model majority-vote ensemble (Kimi K2.6 + GLM-5.1 + DeepSeek V3.2)

**Design.** To eliminate the shared-provider concern (the original two-model coding and the primary ensemble are all invoked through OpenRouter-provisioned endpoints, and the original's Kimi K2.5 and the ensemble's Kimi K2.6 are same-family models) and to extend revalidation from the 150-case sample to the full 676-case T4 universe, all 676 opinions were re-coded by three independently-provisioned models:

- `moonshotai/kimi-k2.6`
- `z-ai/glm-5.1`
- `deepseek/deepseek-v3.2`

All three at temperature 0.2, reasoning disabled where supported, same prompt. Ensemble resolution is majority vote at the family-bucket level; 3-way splits resolve to OTHER. The July 2026 corpus refresh extended the T4 universe from 676 to 739 rows; the 60 parseable refresh rows were coded with the same frozen prompt and models and merged into the primary coding, so merged corpus-level statistics below are reported on the 728-case coded universe.

**Coverage.** Three-model coverage on the merged universe is 728/739 (98.5%): 11 cases were dropped for unparseable model output or as a pre-refresh residual uncoded row.

**Cross-model agreement (Fleiss' κ).**

| Level | Fleiss' κ | Interpretation |
|---|---|---|
| Family bucket | **0.6297** | Substantial |
| Atomic family | 0.5636 | Moderate |

Bucket-level Fleiss' κ is reported on the merged 728-case coded universe (0.6292 on the original 668); the atomic-family value is from the original 668-case run.

**Pairwise cross-model bucket κ.**

| Pair | Bucket match | Bucket κ |
|---|---|---|
| Kimi K2.6 × GLM-5.1 | 75.60% | **0.6348** |
| Kimi K2.6 × DeepSeek V3.2 | 76.05% | **0.6466** |
| GLM-5.1 × DeepSeek V3.2 | 73.95% | **0.6113** |

Each pairing returns substantial agreement; no pair drops below 0.61. GLM-5.1 and DeepSeek V3.2 agree with Kimi K2.6 at essentially the same level they agree with each other. That symmetry is what defeats the shared-provider concern.

**Per-model agreement with ensemble consensus.**

| Model | Bucket match with ensemble | Bucket κ |
|---|---|---|
| Kimi K2.6 | 88.17% | 0.8225 |
| GLM-5.1 | 86.68% | 0.8001 |
| DeepSeek V3.2 | 87.28% | 0.8097 |

No outlier classifier — all three agree with ensemble consensus at κ ≈ 0.80–0.82.

**Ensemble vs. original coding.**

| Metric | Value |
|---|---|
| Bucket exact match | 71.71% (479/668) |
| Bucket κ | 0.574 |
| Atomic family exact match | 60.48% |
| Atomic family κ | 0.4743 |

Ensemble-vs.-original bucket κ (0.574) is above each individual model's solo κ against the original (Kimi K2.6 solo 0.5237; GLM-5.1 solo 0.5477; DeepSeek V3.2 solo 0.5011) — the expected behavior of majority vote when three models make partially uncorrelated errors.

Scope note: the pairwise, per-model, and ensemble-vs.-original agreement statistics above are computed on the original 668-case run and predate the July 2026 refresh increment (60 of the 728 coded rows); the two-model original coding was not extended to the refresh rows.

**Substantive-claim replay on the full universe.**

| Coding | Pro-se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | χ²(1) | p |
|---|---|---|---|---|---|
| Original (K2.5 + GLM-5.1) | 47.74% | 15.38% | **32.36** | 32.21 | 1.39 × 10⁻⁸ |
| Ensemble majority (merged, n = 728) | 45.25% | 13.68% | **31.57** | 32.70 | 1.1 × 10⁻⁸ |
| Kimi K2.6 solo | 50.87% | 23.08% | 27.79 | 23.26 | 1.42 × 10⁻⁶ |
| GLM-5.1 solo | 46.18% | 17.58% | 28.60 | 25.18 | 5.23 × 10⁻⁷ |
| DeepSeek V3.2 solo | 38.19% | 17.58% | 20.61 | 13.72 | 2.13 × 10⁻⁴ |

The merged ensemble TRANSLATION gap (31.57 pp, p = 1.1 × 10⁻⁸) is essentially identical to the original (32.36 pp, p = 1.4 × 10⁻⁸). The 95% confidence intervals overlap almost completely: ensemble [23.64, 39.50] pp and original [23.90, 40.82] pp. Even the most conservative individual classifier (DeepSeek V3.2 solo) returns a 20.61-pp gap at p = 2 × 10⁻⁴, which leaves the effect substantial and highly significant under the least-favorable read. The original and solo rows are computed on the pre-refresh 668-case run.

**PROCEDURAL_GATEWAY mirror gap.** The opposite-direction PROCEDURAL_GATEWAY family gap is likewise robust:

| Coding | Pro-se PG % | Represented PG % | Gap (pp) | χ²(1) | p |
|---|---|---|---|---|---|
| Original | 17.88% | 31.87% | −13.99 | 8.82 | 0.003 |
| Ensemble (merged, n = 728) | 18.51% | 32.63% | −14.12 | 9.30 | 0.002 |

### M.16.3 External validation — Full-universe blind fourth-coder re-read (Claude Opus 4.7, 22 independent coder seats)

**Design.** The prior two layers revalidate the gap under LLM re-coding but all classifiers are invoked through OpenRouter-provisioned API endpoints with closely matched prompts. To add a fourth independent read by a model from a different provider and a different prompt execution path, all 668 opinions in the three-model ensemble universe were re-coded by Claude Opus 4.7 across 22 independent coder seats. Each seat was given the verbatim mechanism prompt (`mechanism_prompt.txt`) and a blind manifest containing only `source_file` and `file_path` — no prior classifications from any model, no metadata about representation status, no hint of the gap being tested. Each seat was instructed to read every opinion file before classifying. The 668 cases were distributed round-robin across 22 chunks; chunk size ≈ 30 cases. Ten of the 22 seats returned server-side rate-limit errors on the first attempt and were re-run with identical blind manifests; all 22 completed with no case coded from incomplete reads.

Scope note: this layer predates the July 2026 corpus refresh (which added 60 of the 728 ensemble-coded rows); all statistics in this subsection, including the ensemble comparison rows, are computed on the pre-refresh 668-case universe and are unchanged.

**Substantive-claim replay on the full universe — three pipelines compared.**

| Coding | Pro se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | χ²(1) | p | 95% CI on gap (pp) |
|---|---|---|---|---|---|---|
| Original (K2.5 + GLM-5.1) | 47.74% (275/576) | 15.38% (14/91) | **32.36** | 32.21 | 1.4 × 10⁻⁸ | [23.90, 40.83] |
| Ensemble (K2.6 + GLM-5.1 + DeepSeek V3.2) | 46.35% (267/576) | 14.29% (13/91) | **32.07** | 31.88 | 1.6 × 10⁻⁸ | [23.81, 40.33] |
| Fourth coder (Claude Opus 4.7, blind, full read) | 44.62% (257/576) | 15.38% (14/91) | **29.23** | 26.64 | 2.4 × 10⁻⁷ | [20.78, 37.69] |

All three independent coding pipelines return the pro se / represented TRANSLATION gap in the approximately 29.2–32.4 pp range, with p well below 10⁻⁶ and the lower 95% confidence bound above 20 pp in every specification. The fourth coder yields the lowest point estimate of the three, yet even that value runs roughly 2.9× the represented rate, which preserves the Note's "more than twice as likely" directional claim.

**Inter-coder reliability on the full universe.**

| Comparison | Bucket κ | Family κ | Bucket exact match |
|---|---|---|---|
| Fourth coder × ensemble | **0.6024** | 0.5652 (n=622) | 73.20% (489/668) |
| Fourth coder × original | 0.4793 | 0.4131 (n=667) | 64.97% (434/668) |
| Ensemble × original (M.16.2 baseline) | 0.574 | 0.4743 | 71.71% |

Fourth-coder vs. ensemble bucket κ = 0.6024 sits at the Landis & Koch "substantial" threshold and at the boundary of the KEEP band (≥ 0.60) in the ensemble_report decision rule. Fourth-coder vs. original κ (0.4793) is in the same band as ensemble vs. original (0.574). The fourth coder agrees with the ensemble more than with the original, which is external corroboration that the ensemble sits closer to a careful independent read than the two-model original coding does.

**Bucket confusion — original vs. fourth coder.**

| orig \ 4th | TRANSLATION | PG | NO_FAILURE | OTHER |
|---|---|---|---|---|
| TRANSLATION | 183 | 14 | 8 | 85 |
| PROCEDURAL_GATEWAY | 12 | 101 | 9 | 10 |
| NO_FAILURE | 1 | 0 | 24 | 1 |
| OTHER | 76 | 15 | 3 | 126 |

**Bucket confusion — ensemble vs. fourth coder.**

| ens \ 4th | TRANSLATION | PG | NO_FAILURE | OTHER |
|---|---|---|---|---|
| TRANSLATION | 204 | 9 | 5 | 63 |
| PROCEDURAL_GATEWAY | 7 | 110 | 10 | 6 |
| NO_FAILURE | 0 | 0 | 24 | 2 |
| OTHER | 61 | 11 | 5 | 151 |

The ensemble → fourth-coder diagonal is visibly denser than the original → fourth-coder diagonal, which is the qualitative picture behind the κ gap (0.60 vs. 0.48). Of the 85 original-TRANSLATION cases the fourth coder re-coded to OTHER, 61 were cases the ensemble also re-coded to OTHER — a shared, reproducible reclassification pattern rather than coder noise.

**PROCEDURAL_GATEWAY mirror gap.** Under fourth-coder primary labeling, pro se PG = 18.23% (105/576) and represented PG = 27.47% (25/91); gap = −9.24 pp (χ²(1) = 3.71, two-sided p = 0.054; one-sided p ≈ 0.027). The ensemble put this gap at −15.09 pp (p = 0.001); the fourth coder recovers a smaller version of the same directional effect at borderline two-sided significance.

**Caveats.**

- *Off-taxonomy mechanism residue.* The fourth coder invented ~65 mechanism-level labels outside the 15-code taxonomy across ~28 distinct labels (most common: `DISABILITY_NOT_PLEADED` ×15, `CONCLUSORY_NO_FACTS` ×5). These are substantively reasonable labels that map cleanly to taxonomy codes via a post-hoc crosswalk; every off-taxonomy mechanism was paired with a valid family code, so the bucket-level κ and gap replay are unaffected. The family-level κ (0.5652 vs. ensemble) is pulled down slightly by a single invalid family code (`NO_FAILURE_DISMISSED_OTHER_GROUNDS`, used once out of 668).
- *Subagent output schema drift.* Two of 22 subagents (chunks 17 and 19) emitted classifications with `family`/`mechanism` or `family_code`/`mechanism_code` keys instead of the canonical `pleading_failure_family`/`pleading_failure_mechanism`. The aggregation script normalizes both forms; substantive classifications were unaffected.
- *Filter-stage noise.* Subagents flagged ~15 cases where the opinion on its face did not adjudicate a pleading defect (amended-complaint-survived, MTD denied as moot, FCA-not-FHA misfile, Rule 41(b) failure-to-prosecute, counterclaim dismissals). These are absorbed into the OTHER / NO_FAILURE buckets and cannot flip the gap direction: the pro se cohort dominates the universe 576:91.
- *The fourth coder is still an LLM.* All coders in the revalidation pipeline — Kimi K2.5, Kimi K2.6, GLM-5.1, DeepSeek V3.2, and Claude Opus 4.7 — are LLMs. No human-coded validation sample is included. The available defense is that four independently-prompted models — three in an ensemble over API endpoints, one operating blind on the raw opinion files through a different provider and a different execution path — converge on the same pro-se / represented gap within ~3 pp.
- *The 0.60 κ is at the threshold, not comfortably above it.* Bucket κ = 0.6024 is arithmetically in the KEEP band but clings to the boundary. A conservative reading rounds this as "high end of SOFTEN" rather than clean KEEP. The Note therefore preserves directional language rather than reporting a specific percentage in main text.

### M.16.4 Specification-stability robustness check — all classifier combinations

The four independent codings of the 668-case universe (Kimi K2.6, GLM-5.1, DeepSeek V3.2, and Claude Opus 4.7) can be combined into five distinct three-model majority-vote ensembles plus a four-model majority-vote ensemble. The table below reports the TRANSLATION gap under every combination, along with κ against the original two-model coding. All combinations in this subsection are computed on the pre-refresh 668-case universe and predate the July 2026 refresh increment (60 of the 728 coded rows).

| Combination | Pro se T% | Rep T% | Gap (pp) | p | 95% CI (pp) | κ vs. original |
|---|---|---|---|---|---|---|
| Original (K2.5+GLM-5.1) | 47.74% | 15.38% | **32.36** | 7.1 × 10⁻⁹ | [23.9, 40.8] | — |
| K2.6+GLM+DeepSeek (Layer 2 ensemble) | 46.35% | 14.29% | **32.07** | 8.4 × 10⁻⁹ | [23.8, 40.3] | 0.574 |
| K2.6+GLM+Opus | 47.57% | 14.29% | **33.28** | 2.5 × 10⁻⁹ | [25.0, 41.5] | 0.579 |
| K2.6+DeepSeek+Opus | 45.14% | 14.29% | **30.85** | 2.7 × 10⁻⁸ | [22.6, 39.1] | 0.552 |
| GLM+DeepSeek+Opus | 42.19% | 14.29% | **27.90** | 3.7 × 10⁻⁷ | [19.7, 36.1] | 0.572 |
| All four (majority; 2-2 → OTHER) | 48.78% | 14.29% | **34.49** | 7.3 × 10⁻¹⁰ | [26.2, 42.8] | 0.574 |
| Opus 4.7 solo (Layer 3) | 44.62% | 15.38% | **29.23** | 1.3 × 10⁻⁷ | [20.8, 37.7] | 0.479 |

**Pairwise bucket κ among the four independent coders.**

| Pair | κ |
|---|---|
| K2.6 × GLM-5.1 | 0.635 |
| K2.6 × DeepSeek V3.2 | 0.647 |
| GLM-5.1 × DeepSeek V3.2 | 0.611 |
| K2.6 × Opus 4.7 | 0.541 |
| GLM-5.1 × Opus 4.7 | 0.554 |
| DeepSeek V3.2 × Opus 4.7 | **0.516** |

**Interpretation.**

1. *Stability.* Every combination — three-model or four-model, with or without Opus — returns a gap in the **27.9 to 34.5 pp range**, with p < 10⁻⁶ in every specification. No combination puts the lower 95% CI bound below 19.7 pp, and no combination reduces the gap below ≈28 pp.

2. *The most conservative specification is GLM+DeepSeek+Opus* (27.9 pp). It includes the least-correlated pairing (DeepSeek × Opus, κ = 0.516) and drops K2.6, the model with the highest individual TRANSLATION rate. Even this specification returns a gap 1.9× the represented rate.

3. *Opus is the most independent coder.* Pairwise κ between Opus and any of the three OpenRouter-provisioned models (0.52–0.55) is lower than any pairwise κ among those three (0.61–0.65). This supports treating Opus as a genuinely distinct revalidation signal rather than a near-duplicate of K2.6/GLM/DeepSeek.

4. *The four-model majority-vote ensemble is methodologically awkward.* Odd-numbered ensembles avoid tie-breaking rules; even-numbered ensembles require a tie-break convention. Only 1 of 668 cases reached a 2-2 split in this data, and that case was resolved to OTHER, but the tie-break rule itself is ad hoc. The three-model Layer 2 ensemble (K2.6+GLM+DeepSeek) was pre-registered before Opus was added as external validation; collapsing the two into one four-model ensemble retroactively eliminates the external-check structure without a compensating reliability gain.

5. *No combination motivates a specification change.* All seven specifications support the Note's directional phrasing ("approximately 30 pp," "more than twice as likely," p < 10⁻⁶). Stability across the full set of classifier combinations carries more methodological weight than any single number drawn from one chosen specification.

**Script.** `method/validation_four_coder_full/best3_ensemble.py` replicates all rows of the table above. `best3_ensemble_results.json` stores the case-level best-3 classifications.

### M.16.5 What the current pipeline and its validation layers establish

1. The gap is directionally robust. It replays under the primary three-model majority-vote ensemble (M.16.2; K2.6 + GLM + DeepSeek, 31.57 pp on the merged 728-case universe; 32.06 pp on the pre-refresh 668), the blind Opus 4.7 full-universe re-read (M.16.3; 29.23 pp), the Opus-4.7-as-resolver sensitivity (29.24 pp; `method/validation_three_model/opus_resolver_report.md`), the backward-compatibility K2.5 + GLM-5.1 coding (31.9 pp on 676), and every individual primary-coder solo run (20.6 – 27.8 pp). The direction, sign, and order of magnitude reproduce across all pipelines.
2. The gap's magnitude is not classifier-specific. Point estimates across the three full-universe pipelines cluster at 29.23 pp (Opus 4.7 full, pre-refresh 668), 31.57 pp (primary ensemble, merged 728), and 31.9 pp (backward-compat K2.5 + GLM on 676); 95% confidence intervals overlap substantially, and the lower bound sits above 20 pp in every specification.
3. The shared-provider concern is addressed by the cross-provider agreement. GLM-5.1 and DeepSeek V3.2 agree with Kimi K2.6 at substantial κ inside the primary ensemble (§ M.16.2); Claude Opus 4.7 agrees with the primary ensemble at bucket κ = 0.60 on the full 668-case universe through a different provider and different execution path (§ M.16.3). The gap is not an artifact of any one provisioning channel or prompt-execution path.
4. The within-family-bias concern does not survive the subset comparison. Per-original-classifier subset κ on the K2.5-origin and GLM-5.1-origin subsets of the backward-compat M.16.1 sample are materially identical (0.6285 vs. 0.6122).
5. The fourth coder's read is more consistent with the ensemble's read than with the earlier two-model coding; the comparison measures reproducibility, not which coding is correct. Fourth-coder agreement with the ensemble (κ = 0.60) exceeds its agreement with the original (κ = 0.48) on the same 668 cases, and the 61 original-TRANSLATION → OTHER reclassifications shared by the ensemble and the fourth coder are the main driver of the gap compression from 32.36 pp to 29.23 pp.
6. Residual uncertainty is bounded. Specific point estimates carry moderate-to-substantial κ uncertainty, reflected in the Note's directional phrasing (≈30 pp, "more than twice as likely") rather than a single percentage claim.

**Use in the Note's Part II.F mechanism-coding footnote.** The Note's Part II.F footnote summarizes this Appendix section in three sentences and points here for the full methodology. The tables, per-model statistics, bucket confusion matrices, and the specification-stability table in M.16.4 stay in the appendix rather than the footnote, which follows ordinary law-review practice for methodology apparatus.
## M.17 Institutional Record-Building and Voucher Record-Flow Audits (cited by fn 178)

This section reports, at full detail, two bounded author-run audits -- institutional
pre-suit record-building and voucher record flow -- that the manuscript carries in
summary form (fn 178). No figure, floor, or convention differs between this section
and the underlying audit record of July 27, 2026. Provenance: the prespecified
two-coder instruments, adjudication records, and citation-and-quotation verification
preserved with the project archive (verification run July 26, 2026).

### M.17.1 Institutional pre-suit record-building (60-unit audit)

The mechanism is measurable in the litigation record. In the author's audit of the
institutional plaintiffs in the case census -- every government,
fair-housing-organization, and group-home-operator unit with a resolvable opinion,
sixty in all, coded fresh under a prespecified two-coder protocol with adjudicated
disagreements --
forty-eight of sixty opinions expressly describe pre-suit record-building by the
institutional plaintiff -- described exchanges with the respondent, formal
accommodation demands, organizational investigations, fair-housing testing,
administrative complaints, and full administrative-enforcement chains -- and the
pattern holds across all three plaintiff classes. Counts are floors on expressly
described activity, not incidence estimates, and silence is recorded as unavailable,
never as evidence of absence; the institutional classification derives from a
pre-census database layer joined read-only to the adjudicated case set, disclosed as
such; coding was by two independent machine coders with adjudication under recorded
rules of decision, and every citation pin was mechanically verified (July 26, 2026).

### M.17.2 Voucher record-flow audit (retrieval-frame counts)

Across the expressly voucher-identified opinions in the author's retrieval frame, the
record-flow question -- whether an earlier PHA record expressly reached the later
decision -- is codeable in twelve of twenty-five; voucher-extension requests appear
in thirteen and extension decisions in eleven; exception payment standards appear in
twelve; and the section 8.28(a)(3) subject matter -- accessible-unit information held
or provided by the PHA -- appears in six. Basis: the author's audit of the full
retrieval frame underlying the voucher search-and-extension screening (fifty-five
files, forty-two distinct opinion texts after byte-identical deduplication);
twenty-five texts are expressly voucher-identified (two single-seat on adjudicated
screens, contributing nothing to the figures here); two more carry only voucher terms
of art and are excluded. The frame is not an exhaustive census of voucher litigation,
so the counts support "at least" statements only, never rates. Record flow is coded
in both directions -- records expressly carried into a later decision, and
affirmative statements that a record did not reach it. Floors, silence-handling,
two-coder conventions, adjudication, and citation-verification conventions as in M.17.1
(here with a three-way program-identification screen; July 26, 2026).

**Manuscript cross-references.** Manuscript fn 178 retains the 48-of-60 finding
and points here; the former manuscript voucher-counts sentence and its fn 180 were
relocated here in full. Nothing in this section alters the Part II case-level census
or its protected series.
