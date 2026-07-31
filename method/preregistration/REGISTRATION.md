# Registration - Strengthening Batch 2026-07-08

Status: Pre-registration. This file records the strengthening quantities, decision rules,
and adverse-outcome triggers for Items 1-3, fixed before the analytics ran.

Canonical input: `data/FHA_Unified_Database.json`,
3,366 records, SHA256 `bcadb0ee59c8df54a201735eb5d09f58622d5402512c02d7bd9ac13e9671b178`.

Assurance: all empirical outputs from this batch are machine-classified-derived and are
EXTENDED at most.

## Mandatory Peek Disclosure

On 2026-07-08, before the main analysis ran, a feasibility peek computed two quantities from the canonical database: (a) corrected institutional shares of decided cases, P1 -> P3: DIS 19.3% -> 9.6%; RD-PURE 18.8% -> 7.8%; DT-PURE 11.5% -> 3.8%; RACE-DT 4.3% -> 1.4%; and (b) the represented decided disability docket: P1 n=176 (bucket mix RD-PURE 53.4%, MIXED 30.1%, DT-PURE 10.2%, OTHER 6.3%; institutional 41.5%) vs P3 n=81 (46.9% / 32.1% / 17.3% / 3.7%; institutional 37.0%). These quantities are therefore DISCLOSED, not registered.

## Registered Item 1: fn 90 Selection Audit

Universe: represented (`pro_se is False`) decided DIS cases, P1 and P3, with P2 reported
descriptively if cell size permits. DIS means `screening_result == YES` and
`disability_alleged is True`, which is narrower than the Note's Table 1 DIS_ANY cohort.

Registered secondary dimensions, P1 vs P3:

- Court-circuit mix, using the database `circuit` field.
- Defendant-type mix, using `defendant_type` if present; if absent, document absence.
- Procedural-posture-reached mix, using `procedural_posture`.
- 504/RA-overlay share, using `is_ra_case` and documenting that exact field.
- Bootstrap 95% confidence intervals on all shares, 2,000 reps, seed `20260708`.

Already disclosed but still reported for continuity:

- Bucket-mix shares: RD-PURE, MIXED, DT-PURE, OTHER.
- Institutional share within represented cases.

Decision rule:

- SUPPORTS-BOUNDING if every disclosed and registered mix dimension shifts <= 10 percentage points.
- INDETERMINATE if any disclosed or registered mix dimension shifts > 10 and <= 20 percentage points.
- SELECTION-EVIDENT if any disclosed or registered mix dimension shifts > 20 percentage points.

Interpretive rule: a selection-evident result is thesis-compatible because footnote 90 itself
identifies counsel selection as intermediary contraction; it must nevertheless be called selection,
not stability.

Context column: report the same table for RACE-DT represented cases as a thin descriptive
comparison only.

## Registered Item 2: Institutional Participation and Exit

Institutional set: exactly `{FAIR_HOUSING_ORG, GOVERNMENT, GROUP_HOME_OPERATOR}`.

Registered outputs:

- Corrected institutional share by cohort x period, with bootstrap 95% CIs, for DIS, RD-PURE,
  DT-PURE, RACE-DT, and DIS_ANY.
- Organization roster for every institutional plaintiff case: normalized plaintiff-side name,
  P1/P2/P3 case counts, first and last decision date, ambiguity flag.
- Roster churn counts: organizations active in P1 but absent in P3; organizations entering in P3.
- Conditional FHIP termination-match counts if and only if a full machine-readable or citable
  terminee roster exists. Phase 0 located aggregate FHIP termination records and four named
  organizational plaintiffs, but no full 66-organization terminee roster. Unless a full roster is
  supplied before Phase 3, matching is registered as CONDITIONAL-UNRESOLVED and no deterministic
  terminee matching will be performed.

No support threshold is registered for Item 2; it is descriptive.

## Registered Item 3: P1 Pre-Trend Split

Split:

- P1a: `date_filed < 2023-04-01` within P1.
- P1b: remainder of P1, i.e., `2023-04-01 <= date_filed < 2024-06-28`.

Quantities:

- Strict-win share and pro se share for RD-PURE, DT-PURE, MIXED, DIS, and RACE-DT in P1a and P1b.
- Cell sizes for every row.
- Bootstrap 95% CIs, 2,000 reps, seed `20260708`.

Decision rule:

- PARALLEL if the absolute value of `(RD-PURE strict-win change P1a->P1b) - (DT-PURE strict-win change P1a->P1b)` is <= 10 percentage points AND the analogous pro se-share difference is <= 10 percentage points.
- DIVERGING otherwise.

Reporting rule: if RD-PURE was already declining relative to DT-PURE by more than 10 percentage
points within P1, the A-6 patch must carry a prominent pre-trend caveat. Adverse results
are reported, not buried.

## What Would Count Against

- A > 20 percentage-point represented-mix shift in any disclosed or registered selection-audit dimension.
- A P1 pre-trend divergence under the rule above.
- An organization roster showing institutional ENTRY rather than exit.

## Implementation Commitments

- No LLM classification calls.
- No paywalled routes.
- No edits to the manuscript or the comparator package; this batch only produces its own outputs.
- All batch outputs remain within this batch's directory.
