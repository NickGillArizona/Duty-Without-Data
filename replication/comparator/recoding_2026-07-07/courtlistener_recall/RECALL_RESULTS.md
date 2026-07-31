# CourtListener Recall Spot-Counts (correction to the first pass)

Run 2026-07-07 with the author's CourtListener API token, held in the CL_TOKEN
environment variable only - the token appears in no file, and the archived URLs are
credential-free (auth is an Authorization header). Method mirrors the p3-extension collection
run: v4 search endpoint,
type=o, filed_after 01/01/2022, filed_before 07/01/2026, all precedential statuses on. Raw
first-page JSON archived per query in this directory; machine-readable results in
`recall_results.json`.

Assurance: EXTENDED as a bounded calibration; the ratios are capture proxies, not
true recall (limits below).

## Counts

| Query | q string | CL count (all jurisdictions) |
|---|---|---|
| anchor_fha_all | "fair housing act" | 2,522 |
| disability_arm | "fair housing act" AND (disability OR handicap) | 1,400 |
| race_arm | "fair housing act" AND (race OR racial) | 1,027 |
| race_arm_narrow | "fair housing act" AND race AND discrimination | 872 |

## Capture ratios (corpus dated screened-in yield / CL keyword count)

| Numerator convention | Disability | Race | Race-vs-disability differential |
|---|---|---|---|
| Primary/alleged (race = primary class; disability = disability_alleged) | 1,021/1,400 = 0.729 | 380/1,027 = 0.370 | 0.507 |
| Any-basis symmetric (race = primary OR protected_classes; disability = DIS_ANY) | 1,347/1,400 = 0.962 | 552/1,027 = 0.538 | 0.559 |

## Reading

Under both numerator conventions, the corpus captures roughly HALF as large a share of
race-mention FHA opinions as of disability-mention FHA opinions (differential 0.51-0.56). The
recall differential the first pass left unbounded is therefore REAL, MATERIAL, and in the
direction the confound register predicted (the disability arm is enriched by the RA/504
retrieval architecture; race rides on the class-general FHA-name pull only).

Consequences for the comparator findings:

1. The race arm's LEVEL comparisons (win rates, pro se shares) rest on the assumption that the
   captured race cases are representative of race FHA litigation; that assumption is now known to
   sit on roughly half-capture. Any race-arm number must carry this caveat.
2. The WITHIN-DISABILITY featured contrast (RD-PURE vs DT-PURE) is UNAFFECTED: both buckets come
   from the same retrieval architecture, so the differential does not bias the note's featured
   mechanism test. This asymmetry is the strongest reason the within-disability axis, not the
   race axis, carries the mechanism weight.
3. Trend comparisons in the race arm (P1 vs P3 within the same capture regime) are less exposed
   than level comparisons, unless capture changed differentially over time - not measurable from
   these counts and disclosed as unresolved.

## Limits (do not overstate)

- CL counts include all jurisdictions; the corpus filtered federal client-side. If the
  state-court share of race-mention FHA opinions differs from disability-mention ones, the
  differential moves.
- A keyword mention is not a claim: the race keyword set is likely more over-inclusive (incidental
  demographic references, 1981/1982 companion claims), which INFLATES the apparent differential
  by inflating the race denominator. The narrow race query (872) bounds this partially: using it,
  the any-basis differential is 552/872 = 0.633 vs 0.962 -> 0.658.
- Corpus numerators are screened-in classified labels; CL denominators are raw hits. The ratio of
  ratios is informative only under broadly similar over-inclusiveness across arms.

Bottom line, as carried into the appendix: the corpus captures roughly half to
two-thirds as large a share of race-mention FHA opinions as disability-mention ones (capture
differential 0.51-0.66 across query and numerator conventions). That caveat attaches to every
cross-class level claim, and the within-disability contrast does not inherit it.
