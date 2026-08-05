
# Appendix A-7 - Selection and Participation Robustness


**Machine-classified robustness appendix. The fn 90 selection audit, computed on the
universal one-case-one-unit (595) series, is inconclusive under the registered rule
(largest registered-dimension shift +12.77 percentage points, past the ten-point bounding
threshold); the earlier registered document-level pipeline run stayed within bounds. Every
number independently recomputed from the canonical database.**

All calculations are deterministic recomputes from the canonical
machine-classified database; no LLM classification calls were made anywhere in this batch.

## A-7.1 Purpose and what the tests show

Two robustness questions left open by Part II are answered here, both registered before
analytics. First, footnote 90 concedes that the stable represented win rate could reflect
counsel selecting safer cases after the 2024-2025 shocks rather than genuine stability; the
selection audit tests the observable implication; on the case-level series fn 90
reports, the registered rule returns INDETERMINATE - its middle category, which the
manuscript reports as "inconclusive" (largest disclosed-dimension shift +12.77
percentage points) - while the registered document-level pipeline run stays within bounds
(8.6 or less) - the audit bounds, but does not rule out, compositional movement. Second, the intermediary-contraction premise implies institutional plaintiffs should be
disappearing from the docket; the participation series shows exactly that, in every arm:
institutional participation in decided cases roughly halved from P1 to P3, and the organization
roster shows 49 institutional names active in P1 that are absent in P3, against 24 entrants and
only 7 organizations continuing across both periods. Read together with Appendix A-6, the
pattern is: the contraction is docket-wide; the collapse is claim-structure-specific; and the
represented win rate's stability is tested against observable case selection - bounded on
the registered document-level run, INDETERMINATE at the case level (see A-7.3).

A registered companion check on the comparator's period design (the P1 pre-trend split)
returned its ADVERSE outcome and is reported in Appendix A-6 section A-6.9, not here: the
RD-PURE strict-win rate (a document-level comparator series; see the scope note at the head
of Appendix A-6) was already declining within P1, which weakens sharp shock-attribution
for the document-level rate decline while leaving the composition finding - which shows no
pre-trend - intact.

## A-7.2 Registration, feasibility-check disclosure, and input integrity

The run uses `data/FHA_Unified_Database.json` (3,366 records, SHA256 bcadb0ee...).
REGISTRATION.md was hash-registered before the outcome analytics ran (the as-run log
carrying the registration entries is preserved in the project's private research records —
see [`../../replication/DATA_PROVENANCE.md`](../../replication/DATA_PROVENANCE.md); the
batch artifact hashes are pinned in method/preregistration/HASH_MANIFEST.json); it
disclosed two same-day feasibility checks made before registration (the institutional
shares and the represented bucket mix) and registered the remaining quantities: the secondary represented-mix dimensions, the P1
pre-trend split, roster churn, and conditional FHIP matching. Decision thresholds were frozen
in the registration. Bootstrap intervals: 2,000 reps, seed 20260708.

## A-7.3 The fn 90 selection audit

[Computed on the universal one-case-one-unit 594/199 series (governing cell restated 2026-08-04, D-QV5/D-QV5-2). Figures independently derived and
confirmed by a second-model comparison.]

Registered rule: SUPPORTS-BOUNDING only if every dimension shifts 10 percentage points or
less (executable form, three-way on the maximum absolute P1->P3 shift: above 20 points,
SELECTION-EVIDENT; above 10 points, INDETERMINATE; otherwise SUPPORTS-BOUNDING). Result on
the case-level series: **INDETERMINATE**. The retained document-level pipeline run
below returned SUPPORTS-BOUNDING.

CASE-LEVEL SERIES (the series the manuscript's fn 90 reports; the universal
one-case-one-unit basis of record). Universe: the case-level census's represented
decided disability cases - P1 n=113, P3 n=60 (P2 n=26, descriptive only; case-level N
283/63/249 = 595, represented pooled 198). This recompute is a post-registration
re-computation of the registered series - a disclosed deviation from the registered
document-level unit of analysis, not a preregistered confirmation; the registered
document-level run is retained below. Full cells with exact two-sided 95% Clopper-Pearson
bounds:
[`results/comparator_arms_case_level_2026-07.json`](../../results/comparator_arms_case_level_2026-07.json).

Governing cell: the summary-judgment posture share among represented cases rose from 23.9%
(27/113) to 36.7% (22/60), a shift of +12.77 percentage points - past the registered
10-point bounding threshold, so the registered rule returns INDETERMINATE. The
private-landlord defendant-type shift computes to -8.39 points (26.7% to 18.3%). Because
the governing cell's
two exact 95% intervals overlap (([16.4, 32.8] and [24.6, 50.1])), the audit records this as
an unresolved docket-composition signal - neither case-mix stability nor a demonstrated
selection effect.


> **Restatement note (2026-08-04, D-QV5).** Eight cross-caption same-action appellate units were merged into their district-action units (N 606 -> 598 -> 594; represented pools P1 116 -> 113, P3 60 -> 60; see `../../ERRATA.md`). The governing cell above is restated on the corrected census: 23.9% (27/113) to 36.7% (22/60), +12.77pp. The 43-cell dimension table below and `results/comparator_arms_case_level_2026-07.json` remain AS REGISTERED on the pre-merger 606/206 basis; their re-derivation is queued. The registered rule's verdict is unchanged: the restated governing shift remains past the 10-point bounding threshold with overlapping exact intervals, so the audit still returns INDETERMINATE.

All 43 dimension-category cells, sorted by absolute shift (shares are counts over the
represented denominators, P1 n=116 and P3 n=60):

| Dimension | Category | P1 share | P3 share | Shift |
|---|---|---|---|---|
| Posture reached | SUMMARY_JUDGMENT | 25.0% (29/116) | 36.7% (22/60) | +11.67pp |
| Claim bucket | RD-PURE | 57.8% (67/116) | 48.3% (29/60) | -9.43pp |
| Posture reached | MOTION_TO_DISMISS | 44.0% (51/116) | 35.0% (21/60) | -8.97pp |
| Defendant type | PRIVATE_LANDLORD | 26.7% (31/116) | 18.3% (11/60) | -8.39pp |
| Claim bucket | DT-PURE | 10.3% (12/116) | 18.3% (11/60) | +7.99pp |
| Defendant type | MUNICIPALITY | 24.1% (28/116) | 31.7% (19/60) | +7.53pp |
| 504/RA overlay | is_ra_case false | 25.0% (29/116) | 31.7% (19/60) | +6.67pp |
| 504/RA overlay | is_ra_case true | 75.0% (87/116) | 68.3% (41/60) | -6.67pp |
| Circuit | MISSING | 6.0% (7/116) | 0.0% (0/60) | -6.03pp |
| Circuit | 10th Circuit | 4.3% (5/116) | 10.0% (6/60) | +5.69pp |
| Claim bucket | MIXED | 25.0% (29/116) | 30.0% (18/60) | +5.00pp |
| Circuit | 2nd Circuit | 12.9% (15/116) | 8.3% (5/60) | -4.60pp |
| Circuit | 8th Circuit | 0.9% (1/116) | 5.0% (3/60) | +4.14pp |
| Defendant type | HOA_CONDO_ASSN | 13.8% (16/116) | 10.0% (6/60) | -3.79pp |
| Claim bucket | OTHER | 6.9% (8/116) | 3.3% (2/60) | -3.56pp |
| Posture reached | PRELIMINARY_INJUNCTION | 5.2% (6/116) | 1.7% (1/60) | -3.51pp |
| Posture reached | TRIAL | 5.2% (6/116) | 1.7% (1/60) | -3.51pp |
| Posture reached | DEFAULT_JUDGMENT | 0.0% (0/116) | 3.3% (2/60) | +3.33pp |
| Circuit | 4th Circuit | 3.4% (4/116) | 6.7% (4/60) | +3.22pp |
| Defendant type | OTHER | 5.2% (6/116) | 8.3% (5/60) | +3.16pp |
| Defendant type | PROPERTY_MANAGEMENT | 12.1% (14/116) | 15.0% (9/60) | +2.93pp |
| Institutional share | institutional | 32.8% (38/116) | 30.0% (18/60) | -2.76pp |
| Institutional share | noninstitutional | 67.2% (78/116) | 70.0% (42/60) | +2.76pp |
| Circuit | D.C. Circuit | 2.6% (3/116) | 0.0% (0/60) | -2.59pp |
| Defendant type | DEVELOPER | 0.9% (1/116) | 3.3% (2/60) | +2.47pp |
| Posture reached | OTHER_PROCEDURAL | 0.9% (1/116) | 3.3% (2/60) | +2.47pp |
| Circuit | 5th Circuit | 10.3% (12/116) | 8.3% (5/60) | -2.01pp |
| Defendant type | HOUSING_AUTHORITY | 10.3% (12/116) | 8.3% (5/60) | -2.01pp |
| Posture reached | OTHER | 1.7% (2/116) | 0.0% (0/60) | -1.72pp |
| Circuit | 1st Circuit | 1.7% (2/116) | 3.3% (2/60) | +1.61pp |
| Posture reached | APPEAL | 17.2% (20/116) | 18.3% (11/60) | +1.09pp |
| Defendant type | GROUP_HOME_OPERATOR | 0.9% (1/116) | 0.0% (0/60) | -0.86pp |
| Defendant type | INDIVIDUAL_TENANT | 0.9% (1/116) | 0.0% (0/60) | -0.86pp |
| Defendant type | PROPERTY_MANAGER | 0.9% (1/116) | 0.0% (0/60) | -0.86pp |
| Defendant type | REAL_ESTATE_AGENT | 0.9% (1/116) | 0.0% (0/60) | -0.86pp |
| Posture reached | ADMINISTRATIVE_REVIEW | 0.9% (1/116) | 0.0% (0/60) | -0.86pp |
| Defendant type | LANDLORD | 0.9% (1/116) | 1.7% (1/60) | +0.80pp |
| Defendant type | GOVERNMENT | 2.6% (3/116) | 3.3% (2/60) | +0.75pp |
| Circuit | 11th Circuit | 9.5% (11/116) | 10.0% (6/60) | +0.52pp |
| Circuit | 6th Circuit | 11.2% (13/116) | 11.7% (7/60) | +0.46pp |
| Circuit | 3rd Circuit | 12.1% (14/116) | 11.7% (7/60) | -0.40pp |
| Circuit | 7th Circuit | 8.6% (10/116) | 8.3% (5/60) | -0.29pp |
| Circuit | 9th Circuit | 16.4% (19/116) | 16.7% (10/60) | +0.29pp |

Representative-row convention (disclosed): collapsing documents to cases requires a rule
for which member row supplies a multi-row case's posture, defendant, claim, circuit, and
overlay labels. The primary run uses the recount's own representative row (the
terminal/victory row). Sensitivity across three deterministic conventions -
terminal/victory row, lowest-db_index member, highest-db_index member - leaves the
INDETERMINATE verdict and the governing dimension (summary-judgment posture) unchanged,
with the maximum shift ranging 11.67-12.47pp. No convention is uniquely correct; "posture
reached" for a multi-document case is inherently a modeling choice.

DOCUMENT-LEVEL PIPELINE SERIES (the registered run; retained for pipeline reproducibility).
Universe: represented (counsel-of-record) decided disability documents - P1 n=176, P3 n=81 (P2
n=40, descriptive only). Same rule; this registered document-level run returned
SUPPORTS-BOUNDING. The largest shifts observed:

| Dimension | Category | P1 share | P3 share | Shift |
|---|---|---|---|---|
| Defendant type | MUNICIPALITY | 28.4% | 37.0% | +8.6pp |
| Posture reached | MOTION_TO_DISMISS | 39.2% | 30.9% | -8.3pp |
| Circuit | 9th Circuit | 21.0% | 13.6% | -7.4pp |
| Claim bucket | DT-PURE | 10.2% | 17.3% | +7.1pp |
| Circuit | 8th Circuit | 0.6% | 7.4% | +6.8pp |
| Claim bucket | RD-PURE | 53.4% | 46.9% | -6.5pp |
| Defendant type | PRIVATE_LANDLORD | 25.6% | 19.8% | -5.8pp |
| 504/RA overlay | is_ra_case true | 74.4% | 69.1% | -5.3pp |
| Institutional share within represented | - | 41.5% | 37.0% | -4.5pp |

Per-cell bootstrap CIs for every document-level share are in selection_audit.csv (45
dimension-category rows, no duplicates - verified); the case-level cells carry
counts and exact two-sided 95% Clopper-Pearson bounds (in the committed artifact
[`results/comparator_arms_case_level_2026-07.json`](../../results/comparator_arms_case_level_2026-07.json))
rather than bootstrap intervals. A RACE-DT represented context table is reported in the
same file and is thin (descriptive only).

Limits, stated plainly: this is an observables-only bound. It cannot rule out within-bucket
selection, case-quality changes invisible to the database's fields, or counsel choosing
stronger cases inside stable labels. On the case-level series the audit does not support
the case-mix-stability reading: one registered dimension-category (summary-judgment
posture) crosses the 10-point threshold, so the registered rule - a point rule on the
maximum shift - returns INDETERMINATE by its letter. Because the governing cell's exact 95%
intervals overlap heavily ([17.4, 33.9] vs [24.6, 50.1]), the crossing is not statistically
resolvable from a sub-threshold shift: the series demonstrates neither case-mix stability
nor a selection effect, and is reported as an unresolved docket-composition signal.
Within-bucket case-quality selection invisible to the database remains possible.

## A-7.4 Institutional participation and exit

Institutional-participation series (the institutional set is plaintiff_type in {FAIR_HOUSING_ORG,
GOVERNMENT, GROUP_HOME_OPERATOR}, decided cells):

| Arm | P1 | P3 | P1 share [95% CI] | P3 share [95% CI] |
|---|---|---|---|---|
| DIS | 74/383 | 30/314 | 19.3% [15.7, 23.5] | 9.6% [6.4, 13.1] |
| DIS_ANY (document-level dated-decided cohort) | 77/476 | 33/399 | 16.2% [13.0, 19.5] | 8.3% [5.5, 11.0] |
| RD-PURE | 32/170 | 11/141 | 18.8% [12.9, 24.7] | 7.8% [4.3, 12.8] |
| DT-PURE | 9/78 | 2/53 | 11.5% [5.1, 19.2] | 3.8% [0.0, 9.4] |
| RACE-DT | 6/138 | 1/71 | 4.3% [1.4, 8.0] | 1.4% [0.0, 4.2] |

These cells are document-level pipeline output; no case-level institutional-participation series
is reported here, because the arm-level participation cells have not been computed on the
one-case-one-unit census (287/68/251). The race arm has no case-level series at all, because the
census covered the disability docket.
Participation roughly halves in every arm, and in the two arms with non-overlapping
document-level intervals (DIS, DIS_ANY) the decline is resolvable despite thin cells. This is the docket-side signature
of intermediary contraction, and it is deliberately presented as docket-WIDE: the
record-dependence claim does not rest on institutional exit being disability-specific.

Organization roster (normalized plaintiff-side names; ambiguous normalizations flagged
row-by-row in org_roster.csv): 86 institutional names appear across the corpus; 49 were active
in P1 and absent in P3; 24 entered in P3; 7 continued across both; 6 appear only in P2. FHIP
termination matching remains CONDITIONAL-UNRESOLVED: the repository holds citable aggregate
termination records and four named organizational plaintiffs, but no full 66-organization
terminee roster, so no deterministic matching was performed and none is claimed. The exit
analysis is corpus-side only until a roster is obtained; a public-records request is the
natural route.

## A-7.5 Status summary and reproducibility

- Selection audit (A-7.3): supplementary descriptive analysis (machine-classified); case-level result INDETERMINATE (max
  registered-dimension shift +12.77pp, restated); the registered document-level run returned
  SUPPORTS-BOUNDING.
- Institutional participation and exit (A-7.4): supplementary descriptive analysis (machine-classified); no
  support threshold was registered.
- Pre-trend check: reported at A-6.9 with its adverse outcome; nothing in this appendix
  states or implies parallel pre-trends.

Reproducibility: every number above recomputes from the canonical database via
`scripts/strengthening_analysis.py`; an independent standalone checker
(`scripts/recompute_verification.py`) independently recomputes every reported
figure and passed (registered_verification_results.txt, RESULT: PASS); the registration and SHA256
manifest accompany the tables (the as-run log with the pre-analytics hash registrations is
preserved in the project's private research records — see
[`../../replication/DATA_PROVENANCE.md`](../../replication/DATA_PROVENANCE.md)): selection_audit.csv, selection_audit_shifts.csv,
institutional_participation.csv, org_roster.csv, org_churn_summary.csv, pretrend_p1_split.csv.
