# Evidence and Limits

A replication archive earns trust by what it discloses against itself. This page is the
canonical statement of what the archive establishes, its principal limitations, adverse
preregistered findings, and superseded analyses. Detail and artifacts are in the linked
appendices; the private research records behind them are described in
[`replication/DATA_PROVENANCE.md`](../replication/DATA_PROVENANCE.md).

## What is mechanically reproducible — and what requires judgment

| Mechanically reproducible from released materials | Requires independent judgment |
|---|---|
| Case-unit counts and period denominators | Whether the captured corpus is complete |
| Qualifying-judgment arithmetic and representation cells | Whether each underlying legal classification is correct |
| Registered figures, tables, and exact intervals | Whether model-coded labels are substantively accurate |
| File integrity, links, and claim-block consistency | Whether an observed pattern is causal |
| The release gate's twenty deterministic checks | Whether the Note's legal conclusions are correct |

## The series of record, and what was superseded

The reported Part II outcome series is the **case-level census**: 595 decided cases (one
case, one unit; 283/63/249 across P1/P2/P3), eighteen qualifying plaintiff-side judgments
(3.48% / 0.00% / 3.19% per period), none pro se, with **no aggregate trend asserted in
either direction**. An earlier document-level analysis (995 decided document rows; 730
consolidation-input rows) supported decline framings that the case-level census does not:
those document-level outcome series are **superseded for outcome reporting** and are
retained only as labeled pipeline output and registered-study artifacts. Guard scripts in
[`scripts/`](../scripts/) (`denylist_superseded_series.py`, `check_retired_claims.py`) fail
the release gate if a superseded number-and-claim combination reappears on a reader-facing
surface.

## Adverse preregistered findings (reported, not buried)

- **Pre-trend (adverse to sharp shock-attribution).** A registered within-P1 split found
  the record-dependent arm's document-level strict-win rate already declining before the
  period boundary. The comparator contrast must therefore be read to include pre-boundary
  deterioration; the composition finding shows no pre-trend. Reported at
  [Appendix A-6 § A-6.9](appendices/Appendix_A6_Comparator_Analysis.md) and
  flagged in the manuscript's own footnote 89.
- **Case-mix audit (inconclusive).** The registered selection audit on the case-level
  series is inconclusive: the largest registered-dimension shift (summary-judgment
  posture, +11.67 percentage points) sits just past the registered ten-point bounding
  threshold with overlapping exact 95% intervals — neither case-mix stability nor a
  demonstrated selection effect. Within-category case-quality selection invisible to the
  database remains possible. Reported at
  [Appendix A-7 § A-7.3](appendices/Appendix_A7_Selection_and_Participation.md).
- **A non-replication, disclosed.** On the full corpus, institutional status was
  associated with reaching the merits; an exploratory screening-stage HUD-assisted subset
  computed before case consolidation on a 730-record document series did not reproduce
  the direction. Because the document-level series is not comparable to the final census,
  no subset estimate is reported (manuscript fn 76; Appendix A-4).
- **A field that failed validation.** The claim-specificity field failed blind validation
  (66.6% agreement on determinate rows; 74.7% after adjudication — below the 85% bar the
  driver fields cleared), so no claim-specificity outcome analysis is reported
  (manuscript fn 86; Appendix E § E.1).

## Structural limitations

- **The corpus measures the decisional pipeline, not violations.** Settlements,
  administrative dispositions, voluntary dismissals, and unreported orders sit outside
  the denominator; nothing in Part II is a claim-success rate.
- **No causal estimates.** The design does not identify the causal effect of
  representation, records, or case selection, and does not measure the regulated
  population of the proposed rule.
- **Machine-coded layers are labeled.** Every coding layer of the pleading-rationale
  analysis is machine-based; the archive measures reproducibility, not accuracy against
  a human-coded benchmark (see [AI_USE.md](../AI_USE.md)).
- **Negative existence claims are located, not absolute.** Statements that no instrument,
  report, or decision was found are claims about the located record after the documented
  searches; gaps are recorded as unavailable, never as proof of absence.
- **Known reproduction boundary.** End-to-end corpus reconstruction requires upstream
  working files retained privately; the frozen canonical JSON is the replication
  baseline, and the release gate re-derives the published figures from it
  ([`replication/REPRODUCE.md`](../replication/REPRODUCE.md)).
