# Selection Audit and Pre-Trend Check (fn 90 / app. A-6.9) — Terminal Summary

Two registered robustness checks from the strengthening batch, one supportive-with-limits
and one adverse. Both are reported in the manuscript and appendices; neither is waived.
Registration of record: [`preregistration/REGISTRATION.md`](preregistration/REGISTRATION.md).

## Counsel-selection audit (fn 90)

Question: did the represented, decided disability docket's observable case mix shift
P1 to P3 in a way that could explain outcome differences by selection rather than by
the record mechanism?

- Registered rule: SUPPORTS-BOUNDING only if every disclosed and registered mix
  dimension shifted 10 percentage points or less.
- Document-level registered run: SUPPORTS-BOUNDING — largest shift 8.6pp
  (defendant-type mix, MUNICIPALITY). Evidence:
  [`../results/supporting/selection_audit.csv`](../results/supporting/selection_audit.csv).
- Case-level reapplication (what the Note's fn 90 prints): INDETERMINATE — the
  summary-judgment posture share moved 25.0% (29/116) to 36.7% (22/60), roughly
  11.7pp, just past the registered threshold; recorded as an unresolved
  docket-composition signal (app. A-7).
- Limitation: observables only. Within-bucket selection — counsel choosing stronger
  cases inside stable labels — remains possible and fn 90 says so.

## P1 pre-trend check (app. A-6.9) — ADVERSE

Question: were RD-PURE and DT-PURE already diverging inside P1, before the 2024-2025
doctrinal shocks?

- Registered rule: PARALLEL only if the RD-vs-DT strict-win change difference and the
  pro se-share change difference were both within 10 percentage points.
- Outcome: DIVERGING — RD-PURE strict wins fell 39.3% to 18.6% within P1 while DT-PURE
  stayed flat (differential -22.2pp, CI [-40.7, -2.4]). This weakens shock-attribution
  for the RATE decline and is reported prominently at app. A-6.9 and flagged in fn 89.
- The COMPOSITION shift shows no pre-trend; the manuscript's composition claim is
  compositional by its own terms.
- Evidence: [`../results/supporting/pretrend_p1_split.csv`](../results/supporting/pretrend_p1_split.csv)
  and [`../results/supporting/pretrend_decision_rule.csv`](../results/supporting/pretrend_decision_rule.csv).

## Verification

Every reported number in the batch re-derives from the canonical database via
[`../scripts/recompute_verification.py`](../scripts/recompute_verification.py)
(release-gate check 10); the standalone run record is
[`../results/supporting/registered_verification_results.txt`](../results/supporting/registered_verification_results.txt).
