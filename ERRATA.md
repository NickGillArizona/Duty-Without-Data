# Errata and Restatements

This file records corrections to published figures in this repository, newest first.
Each entry states what changed, why, the evidence, and which artifacts were restated.
Registered figures that deliberately remain on a superseded basis are listed with
their basis notes rather than silently rewritten.

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

**Figures deliberately kept on the registered pre-merger basis** (each carries a
dated basis note at its surface; re-derivation queued): the fn 140 pleading-stage
defense-win floors (their per-case lane-union flag list is not derivable from the
published record); Appendix A-7's 43-cell dimension table and
`results/comparator_arms_case_level_2026-07.json` (the governing cell is restated);
the perimeter-census program-nexus classification.

**How this was found.** A blind cross-model validation sweep flagged one appellate
unit (Pelican) whose keep code identified it as an extra document of a victory while
its unit carried no victory. Docket-identity tracing confirmed the caption split, and
a systematic sweep of all 50 appellate singleton units against the district units'
docket numbers found the remaining seven. The sweep instrument recovered the known
positive before being trusted.
