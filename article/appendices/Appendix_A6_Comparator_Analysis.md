# Appendix A-6 - Comparator Analysis (Claim-Structure and Cross-Class Robustness)

**Assurance: EXTENDED (machine-classified). Variant A of the comparator design (selected by
pre-registered triggers); cross-referenced from the Note's footnotes 87, 89, and 90.**

> **Outcome series.** The disability-arm strict-win, Kitagawa, and MTD-survival figures in this
> appendix are computed on the document-level series. On the case-level series the Note reports
> in Part II, the disability-arm strict-win rates are RD-PURE 3.36% (P1) to 2.48% (P3), DT-PURE
> 2.13% to 5.26%, and MIXED 3.49% to 2.90% (5/149 to 3/121; 2/94 to 3/57; 3/86 to 2/69) — the
> directional asymmetry described below (record-dependent claims fall while disparate-treatment
> claims do not) survives, but the magnitudes are small and the aggregate change is near zero,
> so no rate/composition decomposition is reported at the case level. The composition contrast
> also survives at the case level: recomputed on the case-level series
> ([`results/comparator_arms_case_level_2026-07.json`](../../results/comparator_arms_case_level_2026-07.json)),
> the RD-PURE pro se share moves 41.6% to 71.9% (62/149 to 87/121, +30.3pp) while DT-PURE stays
> flat and pro se heavy (78.7% to 77.2%), and institutional participation roughly halves in
> every pure disability arm (the MIXED arm declines more modestly, 23.3% to 17.4%). The census-sustained discriminating result is the
> institutionally-held-fact pleading-deficit contrast in section A-6.4 (13.6% / 0.8% / 0.6%),
> which does not depend on the victory-rate series and survives case-level deduplication
> (12.7% / 0.8% / 0.7%; `scripts/rationale_dedup_sensitivity.py`). The race comparator's cells
> are on the document-level series only (the census covered the disability docket), and no
> case-level MTD-survival event census exists (a feasibility review found one not soundly
> constructible from the case-level data). The document-level tables below are retained so the
> reproducible pipeline is intact.

## A-6.1 Purpose and what the test shows

The most predictable objection to Part II's empirics is generic contraction: after 2024-2025,
every fair-housing claimant lost counsel and institutional support, so nothing in the observed
shift is specific to record-dependent rights. This appendix reports the test of that objection.
The design holds protected class constant and varies claim structure - within the disability
docket, it contrasts record-dependent claims (reasonable accommodation, modification,
design-and-construction), whose elements live in institutional records, against
disparate-treatment claims, whose elements are facts within the plaintiff's own knowledge - and
then varies protected class against a race comparator.

The result, in one sentence: the collapse is not generic. The pro se influx (+28.3 percentage
points), the strict-win collapse (-18.2 points), and the institutionally-held-fact pleading
failures (13.6% of pro se pleading losses, versus under 1% in both comparison arms) all
concentrate in record-dependent claims; disability disparate-treatment claims - same protected
class, same courts, same period, same contraction - show none of these signatures, and the race
comparator shows the contraction's footprint (institutional thinning, modest pro se drift)
without the record-dependent collapse. That is the record-dependence thesis's fingerprint: when
the facts a claim needs are facts only the defendant institution records, the claimants least
able to compel those records fail at the pleading gate for want of them.

A candor note matching the manuscript's empirical footnote conventions: every figure here is
machine-classified and carries an assurance label; predictions were registered and hash-logged
before outcome analytics, after one feasibility check disclosed in the registration; the rationale coding was run
three ways (a first-pass deterministic keyword proxy, disclosed and replaced by the ensemble
coding; a masked three-model consensus; and a blind
full-opinion verification pass), and only the verified figures carry weight; no human coded any
row, and section A-6.5a states exactly what was done instead. Two adverse measurements are
reported alongside the findings: a material race-arm retrieval-capture differential and a high
measured masking-leakage rate.

## A-6.2 Design and registered predictions

Cohorts (canonical database, 3,366 records, SHA256 bcadb0ee...; periods P1/P2/P3 as in Table 1):

- DIS: screened-in, disability_alleged true. Note: narrower than the document-level pipeline's
  Table 1 cohort (which also counts protected-class membership and Rehabilitation Act
  retrieval); that cohort's document-level strict series is 17.9/8.3/9.8 and this arm's is
  21.1/9.9/11.8, both reproducing from the database at the document level. (The Note's Table 1
  itself now reports the case-level census series; see the scope note above.) The label matters
  and is kept explicit throughout.
- RD-PURE / DT-PURE / MIXED (featured axis): within DIS, claim-type buckets - record-dependent
  only, disparate-treatment only, or both; MIXED is analyzed as its own stratum and never
  silently merged.
- RACE-DT (featured cross-class arm): screened-in, primary class race, excluding any
  disparate-impact claim type - the January 14, 2026 proposed disparate-impact rescission is a
  race-specific period-3 shock, handled by design. RACE-ALL runs as a sensitivity arm.

Registered predictions (PREDICTIONS.md, SHA256 bcd5598e... over the body below that file's frozen-instrument banner, logged before analytics): (1) race
pro se share rises less than disability's; (2) disability's strict-win decline and composition
share exceed race's; (3) within disability, RD-PURE declines harder and more compositionally
than DT-PURE; (4) under a class-neutral rubric, institutionally-held-fact pleading deficits
concentrate in RD-PURE pro se losses relative to DT-PURE and race; (5) race disparate-treatment
merits outcomes are comparatively stable. The registration disclosed a prior same-day
feasibility check of crude bucket win rates and registered only quantities not yet computed. A
pre-specified "against-the-thesis" list accompanied the predictions; its resolution is section
A-6.7. The verification protocol and its decision thresholds were separately pre-registered and
hash-logged before any verification call (section A-6.5a).

## A-6.3 Composition and outcome contrasts (document-level registered arms)

Assurance: EXTENDED (machine-classified; independently reproduced from the canonical
database by a standalone audit script).

| Arm | N decided P1/P2/P3 | Strict win P1 -> P3 | Change | Pro se share P1 -> P3 | Change | MTD survival P1 -> P3 |
|---|---|---|---|---|---|---|
| RD-PURE | 170/33/141 | 28.8% -> 10.6% | -18.2pp | 44.7% -> 73.0% | +28.3pp | 44.6% -> 17.9% (-26.6pp) |
| DT-PURE | 78/23/53 | 10.3% -> 15.1% | +4.8pp | 76.9% -> 73.6% | -3.3pp | 16.4% -> 5.3% (-11.1pp) |
| MIXED | 107/36/99 | 18.7% -> 12.1% | -6.6pp | 50.5% -> 73.7% | +23.2pp | 32.3% -> 21.2% |
| DIS | 383/101/314 | 21.1% -> 11.8% | -9.4pp | 54.0% -> 74.2% | +20.2pp | 32.3% -> 15.7% |
| RACE-DT | 138/37/71 | 8.7% -> 5.6% | -3.1pp | 69.6% -> 73.2% | +3.7pp | 22.1% -> 10.6% |
| RACE-ALL | 185/46/94 | 8.6% -> 6.4% | -2.2pp | 55.7% -> 64.9% | +9.2pp | 25.4% -> 18.6% |

P2 cells with n < 60 are descriptive only. Two features do the work. First, the pro se influx is
an RD-PURE phenomenon: +28.3pp, against an essentially flat DT-PURE (which was always pro se
heavy) and +3.7pp in RACE-DT. Second, the strict-win collapse follows the same line: RD-PURE
-18.2pp while DT-PURE moved +4.8pp and RACE-DT -3.1pp. Institutional plaintiffs (fair-housing
organizations, government, group-home operators) thinned across EVERY arm - DIS 19.3% -> 9.6%
of decided cases; RD-PURE 18.8% -> 7.8%; DT-PURE 11.5% -> 3.8%; RACE-DT 4.3% -> 1.4% - which is
the docket-wide contraction footprint; what distinguishes the arms is what follows it.

Kitagawa decomposition (representation-stratified, path-symmetric; APPENDIX-READY): the
composition share of the P1->P3 strict-win decline is 57.5% (DIS), 42.6% (RD-PURE), and 17.2%
(RACE-DT); DT-PURE has no decline to decompose (its rate rose); NONDIS sensitivity 44.1%. (These
composition shares are on the document-level series; on the case-level series the aggregate strict
change is near zero, so a composition share of that change is ill-conditioned and is not reported --
see the scope note at the top of this appendix.)
Logistic diff-in-diff interaction models were fit (both axes, robust HC1, MIXED-reassignment
sensitivities) but are quasi-separated on thin cells and live in the repository as DIRECTIONAL
DIAGNOSTICS ONLY; nothing in this appendix or the manuscript rests on their p-values.

## A-6.4 The discriminating test: common-rubric rationale mix

Design: the dismissal-rationale passages of every pleading-loss row in DT-PURE (145) and
RACE-DT (186), and a same-size seed-fixed random sample of RD-PURE (145 of 192), were coded
under a frozen class-neutral rubric: family A (institutionally-held-fact deficit:
request/response, notice, timing, internal decisions, premises facts), family B
(plaintiff-known-fact deficit), family C (legal insufficiency independent of factual detail),
plus UNCLEAR and misfilter flags. The primary coding used the archive's Layer-2 consensus
architecture (Kimi K2.6 + GLM-5.1 + DeepSeek V3.2, majority vote, raw outputs preserved) on
class-masked passages; a first-pass deterministic keyword proxy is disclosed and replaced by the
consensus coding (row-level agreement with the consensus: 38.2% - the proxy measured keyword
incidence, not
judicial rationale, and none of its figures carry weight).

Family-A share among PRO SE pleading losses, three coding passes (Assurance: EXTENDED,
machine-classified and machine-verified per section A-6.5a; body use per the manuscript's fn 89):

| Arm | Masked consensus | Verified primary (after blind full-opinion audit) | Raw-text robustness check |
|---|---|---|---|
| RD-PURE | 16.4% [10.3, 23.3] (n=116) | 13.6% [7.6, 20.3] (n=118) | 12.2% [6.1, 18.3] (n=115) |
| DT-PURE | 1.5% [0.0, 3.8] (n=132) | 0.8% [0.0, 2.3] (n=132) | 0.0% [0.0, 0.0] (n=129) |
| RACE-DT | 1.9% [0.0, 4.4] (n=159) | 0.6% [0.0, 1.9] (n=158) | 1.9% [0.0, 4.4] (n=158) |

Reading the result: in every pass, institutionally-held-fact deficits are rare everywhere
except in record-dependent claims, where they account for roughly one in seven pro se pleading
losses - an order-of-magnitude concentration with non-overlapping confidence intervals in the
verified pass. The verification cut the RD-PURE point estimate (16.4% to 13.6%) while cutting
the comparators' rates further still, so the contrast sharpened under scrutiny. Equally
important is what did not happen: the pre-registered alternative under which DT-PURE pro se
losses would be dominated by family A (accommodation grievances mispleaded as disparate
treatment) did not materialize - DT-PURE and race pro se losses fail overwhelmingly on facts
within the plaintiff's own knowledge (conclusory motive and differential-treatment allegations,
family B at 57-59%) or on class-independent legal grounds (family C at 39-41%). The finding is
a concentrated asymmetry, not a dominant failure mode: even in record-dependent claims, most
pro se pleading losses fail on B or C grounds; what distinguishes the claim structures is the
14-point slice of failures that turn on facts only the defendant institution records.

Case-level deduplication sensitivity: the coding universe is document-level, and a small
number of cases contribute more than one pleading-loss document (two of the verified RD-PURE
Family-A cases appear twice). Collapsing to distinct case names — a case counts as Family-A if
any of its classifiable pro se rows is verified A — leaves the contrast intact: 12.7% (14/110)
versus 0.8% (1/128) versus 0.7% (1/145). Reproducible from committed inputs via
`scripts/rationale_dedup_sensitivity.py`.

## A-6.5 Agreement, masking leakage, and validation of the primary coding

- Three-coder Fleiss kappa 0.729 over the full five-label space (0.752 restricted to A/B/C),
  above the archive's Layer-2 benchmark of 0.629. Per arm: RD-PURE 0.611, DT-PURE 0.745,
  RACE-DT 0.799 - the A/B boundary is genuinely harder inside accommodation fact patterns,
  which is why every consensus Family-A row went to the verification audit (A-6.5a).
- Independent stratified re-read by a fourth model (MiniMax M2.7, 150 rows): Cohen kappa 0.608
  against the consensus - at the archive's fourth-coder benchmark (0.602).
- Masking leakage, measured (an initial exact-match scan reported 0.0%; that metric was broken by
  construction and is not relied on): 61.3% of masked excerpts retain class-identifying residue by
  an extended-lexicon scan; a model probe asked to guess the protected class from masked text is
  right 70.8% of the time overall and 96.6% of the time in RD-PURE - accommodation context is
  inherently identifying. The design claim is therefore masking-attempted, not
  blinding-achieved. The decisive comparison is within a single protected class, so class
  recognition alone cannot produce it; the residual risk - a coder recognizing accommodation
  context and expecting institutional-fact defects - is exactly what the blind full-opinion
  audit in A-6.5a was built to check, and the audit sustained the finding.
- Substrate: the primary coding ran on the database's rationale fields (Layer-1 machine
  distillations of opinion text). The raw-text passes in A-6.5a recode from the opinions
  themselves; their agreement with the primary coding (86% row-level) retires the substrate
  caveat as a threat to the contrast while leaving it disclosed as a design fact.

## A-6.5a Verification without a human coder

No human coded any row in this study. Verification is machine-only by design; no human-coded
sample exists at this scale. That posture is the archive's standing one: reproducibility across
independent machine coders rather than accuracy against a human gold standard
(VALIDATION.md section 1). The verification protocol and its decision thresholds were
pre-registered and hash-logged before any verification call, and it has three parts:

1. BLIND FULL-OPINION AUDIT. All 26 consensus Family-A rows - the load-bearing and
   least-unanimous category - plus every no-consensus row, every misfilter flag, the queue's
   B/C rows, and a seeded 36-row B/C control sample (96 rows total) were recoded from full
   opinion text by three strong models from three different providers (Claude Sonnet 5, GPT-5.5,
   Gemini 3.1 Pro), blind to all prior codes. Each read was required to return a single
   contiguous verbatim evidence quote, programmatically matched against the opinion text
   (87.2% verbatim-match rate; failures flagged in the raw artifacts). Panel-consensus
   disagreements (28 rows) were adjudicated by a fourth model (Claude Opus 4.8) under the same
   quote requirement. Results: 19 of 26 Family-A rows sustained (73.1%); 6 recoded to B, 1 to
   UNCLEAR; only 1 of 36 control rows flipped into A (2.8%) - the category boundary is stable,
   and the audit was not generous to the thesis.
2. FULL-UNIVERSE RAW-TEXT ROBUSTNESS CHECK. All 476 rows were independently recoded from
   full opinion text by the archive's Layer-2 trio (Fleiss kappa 0.687; 1,427 of 1,428 reads;
   80.5% verbatim-quote rate). The concentration reproduces on raw text: 12.2% vs 0.0% vs 1.9%.
3. COMPLETENESS GATE AND TRIGGERS. A 27-check completeness gate (read coverage, schema, quote
   integrity, adjudication closure, prompt-hash registration, artifact manifest) passed in full
   before the pre-registered decision thresholds were evaluated. All three thresholds passed:
   the verified estimate exceeded its 8% floor with confidence intervals separated from both
   comparators; the raw-text run preserved at least twofold ordering; control-row instability
   stayed under its 20% cap. The result-contingent text in the manuscript's fn 89 was selected
   by these thresholds, mechanically, with no post-hoc discretion.

Residual limits, stated rather than waived: model-correlated error across the seven models used
(five labs) cannot be excluded by adding more models; the verified estimate rests on 16
verified-A pro se rows of 118 classifiable (the interval [7.6, 20.3] prices that thinness); and
a reader who requires human-coded ground truth will not find it here - or anywhere in this
literature at this scale.

## A-6.6 Confound register

1. Claim-type pleading endogeneity (the design's central caveat): the pleader chooses the claim
   type, so a pro se grievance mis-framed as disparate treatment lands in DT-PURE. The rationale
   mix is the check, and it did not show the mispleading signature; but endogeneity cannot be
   excluded at the margin, and MIXED-bucket reassignment sensitivities are reported in the
   repository.
2. Race-arm retrieval capture (measured; previously unbounded): live CourtListener spot counts
   show the corpus captures roughly half to two-thirds as large a share of race-mention FHA
   opinions as disability-mention ones (capture differential 0.51-0.66 across query and
   numerator conventions; archived credential-free URLs and raw JSON in the repository).
   Race-arm LEVEL comparisons carry this caveat. The featured within-disability contrast does
   not inherit it: both buckets come from the same retrieval architecture.
3. Disparate-impact rescission shock: handled by design (RACE-DT excludes disparate-impact
   claim types; RACE-ALL sensitivity reported).
4. Section 504-arm enrichment asymmetry: the disability corpus is enriched by RA/504 retrieval;
   race rides the class-general FHA pull only - the mechanism behind confound 2 and the reason
   the cross-class arm is secondary to the within-disability arm.
5. Thin cells: DT-PURE P2 decided = 23; RACE-DT P2 decided = 37; rough minimum detectable
   effects at those sizes are 23-29pp, so P2 cells are descriptive only. DT-PURE MTD survival
   rests on 55/18/38 motions.
6. Outcome coverage and class assignment: all 834 dated screened-in non-disability records have
   complete outcome/posture/representation fields; consensus reclassification of the 152
   UNDETERMINED-class and 70 empty-class rows moves at most 3 dated-decided rows into the race
   arm (under 1.2%) - immaterial.
7. Feasibility check: disclosed verbatim in the registration; registered quantities exclude the
   pre-checked ones.
8. Missing filing dates: 29-34% of records lack date_filed and drop from period analysis;
   differential-missingness proxy tests are reported in the repository.

## A-6.7 What would have counted against the thesis - resolution

Pre-registered adverse outcomes and their resolutions: identical rationale mixes across arms -
NOT observed (order-of-magnitude family-A separation, sustained under blind full-opinion
audit); race composition share at or above disability's - NOT observed (17.2% vs 57.5%);
DT-PURE decline matching RD-PURE after stratification - NOT observed (DT-PURE rose); DT-PURE
pro se losses dominated by family A - NOT observed (0.8% verified); sharper race merits decline
than disability without a class-specific shock - NOT observed (-3.1pp vs -9.4pp). Two adverse
findings OUTSIDE the registered list are reported anyway: the masking-leakage and
capture-differential measurements both came back materially worse than the first pass assumed,
and both are carried as standing caveats; and the verification audit overturned 7 of 26
Family-A codes, which is reflected in the verified estimates above.

## A-6.8 Assurance summary and reproducibility

- Composition/outcome tables and decomposition (A-6.3): EXTENDED (machine-classified),
  independently reproduced from the canonical database.
- Rationale mix (A-6.4): EXTENDED (machine-classified and machine-verified under the A-6.5a
  protocol); body use per the manuscript's fn 89.
- Interaction models: directional diagnostics only, repository-only.
- Recall bounds and leakage assays: EXTENDED, reported as measured bounds.

Reproducibility. Every number in this appendix recomputes from the committed canonical database
(`data/FHA_Unified_Database.json`, SHA256 bcadb0ee...) plus the comparator directory: the
deterministic pipeline (`comparator_analysis.py`), the standalone audit script that reproduces
every descriptive cell, the frozen and hash-logged prompts (masked pass, raw-text pass,
adjudicator), the raw per-model outputs for all seven models across all passes, the verified
codes and evidence quotes, the completeness-gate results, the trigger evaluation
(`VERIFICATION_RESULTS.json`), run logs whose prediction and prompt hashes were recorded before
the corresponding analytics, and SHA256 manifests covering first pass, remediation, and
verification. The verification protocol was registered and hash-logged before analytics. Total
model-inference cost for classification, verification, and audit: 25.69 USD across 4,346
model reads.

## A-6.9 Pre-trend check on the period design

A registered check split P1 into P1a (before April 1, 2023) and P1b (April 1, 2023 through June 27, 2024) to test whether RD-PURE and DT-PURE were already diverging before the 2024-2025 shocks. The rule was frozen before analytics: PARALLEL only if both the RD-vs-DT strict-win change difference and the RD-vs-DT pro se-share change difference were within 10 percentage points.

The result is DIVERGING. RD-PURE strict-win change was -20.7pp; DT-PURE strict-win change was 1.5pp; difference -22.2pp. RD-PURE pro se-share change was -8.1pp; DT-PURE pro se-share change was 8.6pp; difference -16.7pp. Because the registered rule returns DIVERGING, this section must be carried as a prominent pre-trend caveat and not as support for clean parallel trends.

Cell-size caution: RD-PURE decided cells were 84 and 86; DT-PURE cells were 32 and 46. The
blind full-opinion audit's independent bootstrap places the strict-win differential's 95% interval at
[-40.7, -2.4] percentage points - wide, but excluding zero. This check is descriptive and
machine-classified; it is not a causal pre-trends proof.

What the divergence does and does not reach: the pre-trend appears in the strict-win RATE, not in composition. Within P1 the RD-PURE
pro se share FELL (48.8% to 40.7%) while the win rate fell 20.7pp; the pro se composition shift
that carries Part II's body claim arrives at and after the period boundary (40.7% at the end of
P1 to 73.0% by P3) and shows no pre-trend. The divergence therefore weakens sharp
shock-attribution for the RD-PURE win-rate decline - a substantial fraction of that decline
predates *Loper Bright* and every other named shock - and it does not weaken the composition
finding, the record-dependence contrast in the rationale mix (which is period-free), or the
manuscript's own framing, which states that "the claim is compositional, not monotonic" and
subordinates period-level outcome estimates to the representation-mix shift and the translation
evidence. Footnote 89's bundled-shocks concession should be read to include pre-boundary
deterioration within the record-dependent docket.

Full table, CIs, registration, and verification artifacts: this repository's
results/supporting/ (pretrend_p1_split.csv, registered_verification_results.txt) and
method/preregistration/ (REGISTRATION.md, HASH_MANIFEST.json; the as-run run log is
preserved in the project's private research records — see
[`../../replication/DATA_PROVENANCE.md`](../../replication/DATA_PROVENANCE.md)).
