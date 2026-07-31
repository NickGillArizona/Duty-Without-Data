# Methods, Limitations, and QA — Comparator and Registered-Baseline Analyses

This is the consolidated, reader-facing register of every substantive quality-assurance
disclosure from the comparator study (app. A-6) and the selection/participation
registered-baseline batch (app. A-7). Each item links the artifact that documents it. Nothing
here is sanitized: the adverse results and failed first attempts are part of the scientific
record. Decline-framed figures below are the document-level record as computed; the current
manuscript prints no decline components from these modules.

## 1. The first-pass rationale coding failed and was replaced

The first pass coded pleading-loss rationales with a deterministic keyword proxy rather than the
required three-model consensus. When the real three-model consensus ran (Kimi K2.6 + GLM-5.1 +
DeepSeek V3.2, majority vote), the proxy's row-level agreement with it was only 38.2% (kappa
0.13). The proxy figures (Family-A 49.6% / 47.0% / 36.9%) are not used; they were replaced first by the
consensus estimates and then by the verified estimates (RD-PURE 13.6% [7.6, 20.3] vs DT-PURE
0.8% [0.0, 2.3] vs RACE-DT 0.6% [0.0, 1.9]). Artifacts:
`recoding_2026-07-07/consensus_stage/consensus_stats.json` (consensus statistics,
including the proxy-vs-consensus agreement); `provenance/VERIFICATION_CLOSURE.md`.

## 2. The original masking-leakage metric was broken by construction

The first pass reported 0.0% masking leakage; that metric could not detect leakage at all.
Measured honestly, class-identification leakage was substantial: 61.3% at the lexicon level and
70.8% by model class-guess (96.6% within RD-PURE). The correct description is
"masking attempted," never "blind." The within-disability design (RD-PURE vs DT-PURE, both
disability cohorts) neutralizes the cross-class recognition component of this concern; it does
not eliminate leakage as a limitation. Artifact:
`recoding_2026-07-07/consensus_stage/consensus_stats.json` (leakage assay fields).

## 3. Retrieval-capture differs by class; cross-class LEVEL claims carry it

CourtListener recall spot-counts (run as a correction after the first pass skipped them for lack
of an API token) bound the race-arm capture differential at
0.51–0.66 across counting conventions. Cross-class LEVEL comparisons carry that differential;
the within-disability contrast does not inherit it. Artifact:
`recoding_2026-07-07/courtlistener_recall/RECALL_RESULTS.md`.

## 4. No human coded any comparator row

Verification was machine-only by author election, under a pre-registered protocol with frozen
thresholds: a blind three-lab full-opinion audit of 96 rows (all 26 consensus-A rows + 36
controls; 19/26 A rows sustained; 1/36 control flips) plus a 476-row full raw-text recode
(Fleiss 0.687). Disclosed in the manuscript's app. A-6.5a ("Verification without a human
coder"). Artifact: `provenance/VERIFICATION_CLOSURE.md`.

## 5. The P1 pre-trend result is adverse and is reported

Registered pre-trend check: RD-PURE strict wins fell 39.3% → 18.6% WITHIN P1 while DT-PURE was
flat (differential −22.2pp, CI [−40.7, −2.4]) — DIVERGING, which weakens shock-attribution for
the RATE decline. The COMPOSITION shift shows no pre-trend (RD pro se share fell within P1,
then rose sharply by P3), and the manuscript's composition claim is compositional by its own
terms. Artifacts: `../../results/supporting/pretrend_p1_split.csv`; `../../method/preregistration/REGISTRATION.md`.

## 6. Selection-mix changes are bounded, not zero

The represented-case selection audit found a maximum represented-mix shift of 8.6 percentage
points (defendant_type/MUNICIPALITY), with all dimensions ≤ 10pp — SUPPORTS-BOUNDING, not
no-change. The case-level reapplication (what the Note's fn 90 prints) is INDETERMINATE: the
summary-judgment posture share moved roughly 11.7pp, just past the registered threshold, and
is recorded as an unresolved docket-composition signal (see
[`../../method/selection_and_pretrend.md`](../../method/selection_and_pretrend.md)).
Artifact: `../../results/supporting/selection_audit.csv`.

## 7. FHIP terminee matching remains unresolved

The registered-baseline batch located aggregate and partial named-plaintiff records but no full
66-organization FHIP terminee roster; no matching was performed (CONDITIONAL-UNRESOLVED). A
public-records request is the identified route. Artifact:
`../../method/preregistration/PROVENANCE_FHIP.md`.

## 8. Claim-status ledger (what may be cited, and how)

- APPENDIX-READY (machine-classified ceiling): the descriptive comparator tables
  (`TABLE1_COMPARATOR.csv`), the P1→P3 contrasts, the Kitagawa composition shares, the recall
  bounds, and the outcome-coverage/UNDETERMINED sensitivity checks.
- DIRECTIONAL DIAGNOSTICS ONLY (never promote): the logistic interaction models —
  quasi-separation on thin cells (`MODELS.md`); published text rests on descriptive contrasts
  and the decomposition, not model p-values.
- NOT USED (replaced): the proxy rationale figures and the broken 0.0% leakage metric (item 1-2).

## 9. Run-integrity events

- A pre-analysis stop fired when a registered assertion compared the canonical 3,366-record
  database against a stale 3,331-record staging copy; the run stopped rather than guessed, and
  the canonical input has been hash-asserted (`bcadb0ee…`) in every subsequent run. (The stale
  copy lived in the author's working archive, not in this repository.)
- The institutional-share column of the first-run Table 1 was silently zero from an
  UPPERCASE/lowercase vocabulary mismatch; found and fixed, and the table
  regenerated — only the institutional columns changed.
- The registered-baseline batch normalized non-ASCII punctuation in quoted manuscript anchors (ASCII
  build rule) while preserving wording; source line numbers in the batch outputs identify the
  exact manuscript text.

## Where the details live

The first-pass disclosure records and run logs are preserved in git history and the
project's private research records; the batch artifact hashes are pinned in `HASH_MANIFEST.json` and
`../../method/preregistration/HASH_MANIFEST.json`. Independent reproduction audit:
`recoding_2026-07-07/audit/AUDIT_RECOMPUTE.json` (24/25 exact, one expected
cohort-labeling flag). Verification protocol and closure:
`provenance/VERIFICATION_CLOSURE.md`. Registration: `../../method/preregistration/REGISTRATION.md`.
