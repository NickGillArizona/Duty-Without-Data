# Errata and Restatements

This file records corrections to published figures in this repository, newest first.
Each entry states what changed, why, the evidence, and which artifacts were restated.
Registered figures that deliberately remain on a superseded basis are listed with
their basis notes rather than silently rewritten.

## 2026-08-04 (third entry, same day) — Census restated 594 → 595 (W1B-ADJ: docket-identity sweep)

An author-commissioned bidirectional identity sweep re-keyed every case unit on
archived RECAP/CourtListener docket metadata — an identity source independent of the
caption and opinion-text keying used by the two earlier audits. The sweep's detector
was control-tested against all twenty previously executed corrections on
reconstructed pre-correction keying (16/20 recovered; every non-recovery explained at
the field level; hard-expected gate 14/14), and every candidate was verified by a
separate adversarial pass against the archived originals (110 string checks, 0
substantive mismatches). **The under-merge direction returned zero new candidates —
the third audit to converge on the current unit spine.** Three corrections were
adopted:

| Correction | Units | Identity evidence |
|---|---|---|
| MERGE: Torres v. MMS Group (S.D.N.Y. 1:22-cv-06142) | FH0801 dissolved into FH0130 | one docket (63602226) carries both units' opinions as its own entries 127 and 188; the differing captions are the full versus short party list of one action |
| SPLIT: Bell v. Weinreb Mgmt. (E.D.N.Y.) | 2025 action (1:25-cv-04207) out of FH0349 to a new unit | the court deciding the 2025 case describes the 2024 case (1:24-cv-02979, transferred in from S.D.N.Y. 1:24-cv-02436) as "a separate action pending before this Court" |
| SPLIT: Jones v. Blue Ocean Realty (D. Md.) | 8:23-cv-02739 rows out of FH1911 to a new unit | two actions with different judges, different office prefixes, separate terminations; full-coverage dockets show no consolidation |

Net: 594 − 1 + 2 = **595** (283/63/249; represented 198, pro se 397). A fourth
flag — the two Ninth Circuit docket numbers inside victory unit V13 (McClendon v.
Bresler) — was investigated and REJECTED: the second memorandum recites "on remand
from … McClendon I," and both dispositions are entries of the single district action
C.D. Cal. 2:20-cv-07758. There is no nineteenth victory.

**What did NOT change.** The eighteen qualifying plaintiff-side judgments (10/0/8;
nine contested, two default, seven liability-only), zero qualifying judgments in pro
se cases, and the sensitivity excluding the liability-only class (eleven).

**Restated figures** (all recomputed deterministically from the corrected
`replication/case_level_census.csv` by `scripts/build_case_level_series.py`):

| Quantity | Before | After |
|---|---|---|
| Decided case units | 594 (282/63/249) | 595 (283/63/249) |
| Represented / pro se units | 199 / 395 | 198 / 397 |
| Qualifying-judgment rate | 3.0% pooled; 3.55/0.00/3.21 | 3.0% pooled; 3.53/0.00/3.21 |
| Represented cell | 18 of 199 (9.0%) | 18 of 198 (9.1%) |
| Pro se cell | 0 of 395 (upper bound 0.9%) | 0 of 397 (upper bound 0.9%) |
| Case-level pro se share P1 → P3 | 59.9% → 75.9% | 60.1% → 75.9% |
| P1-vs-P3 strict difference | −0.33 pp | −0.32 pp |
| Within-corpus under-call bound | 1 of 594 (0.93%) | 1 of 595 (0.93%) |
| fn 140 pleading-stage floors | 141/282, 48/63, 143/249 | 142/283, 48/63, 144/249 (both historical anchors reproduce first: rows 167/59/151; 606-case replay 140/50/143) |

Provenance corrections adopted in the same motion: four census rows whose recorded
`courtlistener_cluster_id` resolved to unrelated cases (a numeric-filename-prefix
artifact) are re-pointed to their verified clusters — Hart (9884278), Sandpiper
(9997813), SoCal Recovery (9368386), Robinson (9533953). Full sweep record,
per-candidate evidence, and verification files: the project's
`w1b_identity_sweep_2026-08-04` lane (private research records).

## 2026-08-04 — Case-level census restated 606 → 598 (caption-split unit merges, D-QV5)

**What changed.** Eight case units in `replication/case_level_census.csv` were
appellate documents of civil actions whose district-court documents were already
counted as separate census units. CourtListener captions the district and appellate
documents of one action differently (for example, the district judgment under one
defendant's name and the appeal under another's), and the caption-keyed case-id
builder assigned them separate ids. Each appellate unit has been merged into its
district-action unit. One case, one unit — now enforced across courts.

**The eight merged actions** (appellate document → surviving unit; identity evidence):

| Action | Appellate doc | Merged into | Evidence |
|---|---|---|---|
| Fair Housing Justice Center v. Pelican Mgmt. (S.D.N.Y. 18-cv-1564) | CA2 23-7348 (2025) | FH0125 (V04, the S.D.N.Y. 2023 bench-trial judgment, captioned Goldfarb Properties) | CA2 order recites the district docket, judgment date, and parties verbatim |
| Lloyd v. Manbel Devco I LP (E.D. Pa. 23-cv-2261) | CA3 (2026) | FH0419 | docket number verbatim in both documents |
| McGinn v. Broadmead (D. Md. 23-cv-02609) | CA4 25-1028 (2026) | FH0322 | docket number and district-judge initials verbatim in both |
| Humphries v. HUD (E.D. Pa. 24-cv-4184) | CA3 25-1740 (2026) | FH0314 | docket number verbatim in both |
| Arthur v. Windsor Shadows HOA (D. Ariz. 20-cv-00435) | CA9 22-16039 (2024) | FH1541 | docket number and judge initials verbatim in both |
| Rice v. City & County of San Francisco (N.D. Cal. 19-cv-04250) | CA9 23-16013 (2026) | FH1620 | docket number and magistrate-judge initials verbatim in both |
| Conn. Fair Housing Ctr. v. CoreLogic (D. Conn. 18-cv-705) | CA2 23-1118 (2026) | FH1670 | docket number and identical parties in both |
| Debity v. Vintage Village HOA (E.D. Tenn. 3:22-cv-00017) | CA6 23-5897 (2024) | FH2409 | exact parties, court, and unique case facts recited in both documents (CA6 order prints no district docket) |

**What did NOT change.** The eighteen qualifying plaintiff-side judgments (10/0/8 by
window; nine contested, two default, seven liability-only), zero qualifying judgments
in pro se cases, the sensitivity excluding the liability-only class (eleven), and the
document-level pipeline counts. The Pelican merge adds the CA2 affirmance to victory
V04's unit; it was always the same victory.

**Restated figures** (all recomputed deterministically from the corrected
`replication/case_level_census.csv` by `scripts/build_case_level_series.py`):

| Quantity | Before | After |
|---|---|---|
| Decided case units | 606 (287/68/251) | 598 (283/65/250) |
| Represented / pro se units | 206 / 400 | 201 / 397 |
| Qualifying-judgment rate | 3.0% pooled; 3.48/0.00/3.19 | 3.0% pooled; 3.53/0.00/3.20 |
| Represented cell | 18 of 206 (8.7%) | 18 of 201 (9.0%) |
| Pro se cell | 0 of 400 (upper bound 0.9%) | 0 of 397 (upper bound 0.9%) |
| Case-level pro se share P1 → P3 | 59.6% → 76.1% | 60.1% → 76.0% |
| P1-vs-P3 strict difference | −0.30 pp | −0.33 pp |
| Within-corpus under-call bound | 1 of 606 (0.92%) | 1 of 598 (0.93%) |
| Disposition-lag sensitivity (P3) | 77.7% (129/166) | 77.6% (128/165) |

One unit-level convention consequence is disclosed rather than hidden: under the
published terminal-row representation rule (`replication/CASE_LEVEL_RULES.md`), the
merged *Rice* unit codes PRO_SE — the plaintiff was counseled at the district phase
and pro se on the terminal appellate document.

**Registered-series follow-up.** The fn 140 pleading-stage defense-win floors have
now been rederived on the final 594-case spine: 141/282, 48/63, and 143/249. The
historical replay reproduces the registered 140/50/143 numerators before application
to the final case spine. Figures still deliberately kept on the pre-merger basis are
Appendix A-7's 43-cell dimension table and
`results/comparator_arms_case_level_2026-07.json` (the governing cell is restated);
the perimeter-census program-nexus classification.

**How this was found.** A blind cross-model validation sweep flagged one appellate
unit (Pelican) whose keep code identified it as an extra document of a victory while
its unit carried no victory. Docket-identity tracing confirmed the caption split, and
a systematic sweep of all 50 appellate singleton units against the district units'
docket numbers found the remaining seven. The sweep instrument recovered the known
positive before being trusted.

## 2026-08-04 (second entry, same day) — Census restated 598 → 594 (D-QV5-2: residual lane)

The author-commissioned residual lane extended the caption-split audit to the
district-district seam, the no-docket rows, and the converse defect (over-merged
units). **Eight further dissolutions**: Hiatt v. Sun City Festival (D. Ariz. 23-552);
Baptist Homes v. City of Madison (S.D. Miss. 24-92); Israel v. Guinn (N.D.N.Y.
25-248); Taylor v. Royal (E.D. Pa. 26-164); Prince v. Pajela (D.N.J. 22-1939);
McClain/McLain v. Johnson County (D. Kan. 25-4036, caption spelling variant);
Players Place II Condo. Ass'n v. K.P. (one N.J. Supreme Court opinion captured
twice); Partee v. Powers Properties (D.S.C. 3:23-4777, docket verbatim in both
documents). **Four splits curing confirmed over-merges** — units that had fused
distinct actions by the same serial litigant: Morris (D. Md.; 18-3399 vs 25-968),
Alvarez (E.D. Pa.; 22-3631 v. HUD vs 24-3127 v. Philadelphia), and Johnson (D. Or.;
Simonson 23-1561 and Guardian 19-485 split out of the Brenneke 21-582 consolidated
unit). Net: 598 − 8 + 4 = **594** (282/63/249; represented 199, pro se 395).

Convention documented: companion or consolidated actions with their own document
rows remain distinct units (Honkala/Chick, per the census's existing hand-split);
consolidated actions decided only in unified documents remain one unit (Brenneke;
Avila's parallel-cases opinion). The eighteen qualifying judgments, their classes,
and the zero pro se cell are again unchanged; rates move at the second decimal
(qualifying-judgment rate 3.0% throughout; represented cell 9.0% throughout).
Verification as in the first entry: deterministic rebuild, full checker suite,
release gate.
