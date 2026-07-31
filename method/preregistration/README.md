# Strengthening Batch (Appendix A-7 and A-6 section A-6.9)

Registered robustness batch run 2026-07-08 under a pre-registered protocol.
[`REGISTRATION.md`](REGISTRATION.md) records the registered quantities, decision rules, and
adverse-outcome triggers, and was hash-registered before any analytics ran; decision
thresholds were fixed in the registration. The analysis instrument's LF-normalized SHA-256
(`9962DADC...`) was likewise registered before the run; the as-run run log carrying both
registrations is preserved in the project's private research records (see
[`../../replication/DATA_PROVENANCE.md`](../../replication/DATA_PROVENANCE.md)), and the batch artifact hashes are pinned
in [`HASH_MANIFEST.json`](HASH_MANIFEST.json). Decline-framed figures in this module (for example the RD-PURE within-P1
pre-trend) are the as-run document-level registration record; the manuscript prints no decline
components — the reported Part II series is the case-level census
(`results/series_2026-07.json`), on which no aggregate trend is asserted.

Contents and outcomes:

- SELECTION_AUDIT.* - the fn 90 counsel-selection audit. Registered outcome SUPPORTS-BOUNDING
  on the DOCUMENT-LEVEL registration inputs: every disclosed and registered represented-docket
  mix dimension shifted 8.6pp or less P1 -> P3 (largest: defendant-type mix, MUNICIPALITY).
  The case-level reapplication that the Note's fn 90 reports is inconclusive under the registered rule — registered verdict INDETERMINATE — (largest shift:
  summary-judgment posture, roughly 11.7pp, just past the registered 10-point threshold).
  Both reported in app. A-7.
- institutional_participation.* + org_roster.csv + org_churn_summary.csv - corrected
  institutional-participation series (roughly halves in every arm) and organization roster
  churn (49 exits / 24 entrants / 7 continuing). FHIP terminee matching is
  CONDITIONAL-UNRESOLVED (no full roster located; no matching claimed). Reported in app. A-7.
- PRETREND_P1_SPLIT.* - the P1 pre-trend check. Registered outcome DIVERGING (adverse):
  RD-PURE strict wins fell 39.3% -> 18.6% within P1 while DT-PURE stayed flat (differential
  -22.2pp, CI [-40.7, -2.4]); the pro se COMPOSITION shift shows no pre-trend. Reported
  prominently at app. A-6 sec. A-6.9 and flagged in the manuscript's footnote 89 itself.
- The integrated text lives in the manuscript and in
  article/appendices/Appendix_A7_Selection_and_Participation.md and Appendix A-6 section
  A-6.9. Manifest rows naming `editcycle_package/` point to working files held outside this
  repository; the registered artifacts they produced are the ones listed above.
- scripts/ + registered_verification_results.txt - every reported number re-derived from the canonical
  database by a standalone checker (RESULT: PASS).

**The as-run analysis instrument.** The registered instrument whose LF-normalized
SHA-256 appears above was a working execution document addressed to the project's
private research environment (internal paths, model assignments, and workflow
vocabulary). It is preserved byte-exact in the project's private research records under
that registered hash and is not reproduced in this archive; `REGISTRATION.md` records
the registered quantities, decision rules, and adverse-outcome triggers in full, and
`HASH_MANIFEST.json` pins the batch artifacts.
