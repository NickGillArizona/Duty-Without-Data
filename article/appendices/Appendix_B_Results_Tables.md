# Appendix B: Case-Level Results Tables

**Cited by:** Note footnote 140 (pleading-stage defense-win lower bounds, with app. H) and the period-total apparatus.
**Source / regeneration:** the case-level series of record ([`results/series_2026-07.json`](../../results/series_2026-07.json)), built from the FHA Unified Database (`data/FHA_Unified_Database.json`) by `scripts/build_case_level_series.py`.
**Unit convention:** one case, one unit. The case-level N is 598 (283/65/250 across P1/P2/P3) after removing duplicate, out-of-window, out-of-cohort, and procedural-only documents. This appendix reports the outcome series of record; superseded document-level pipeline tabulations are retained in the project's private research records, not here (see [`../../replication/DATA_PROVENANCE.md`](../../replication/DATA_PROVENANCE.md)).

## B.1 Case-Level Outcome Census (the series of record)

**Periods (date-labeled per the Note's Part II.B convention):** P1: January 1, 2022 -- June 27, 2024; P2: June 28, 2024 -- February 4, 2025; P3: February 5, 2025 -- July 1, 2026 (endpoints inclusive). The boundary rationale is stated in the Note's margin (fn 67).

| Metric | Pooled census |
|---|---|
| Decided cases (case-level N) | 598 (283 / 65 / 250) |
| Final contested judgments awarding relief | 9 |
| Final default judgments awarding relief | 2 |
| Liability determinations, remedy reserved at entry | 7 |
| Qualifying plaintiff-side judgments (combined) | 18 (3.0%) |
| Per-period qualifying judgments | 10/283 (3.53%) / 0/65 (0.00%) / 8/250 (3.20%) |
| Represented cases: qualifying judgments | 18 of 201 (9.0%) |
| Pro se cases: qualifying judgments | 0 of 397 (exact 95% upper bound 0.9%) |
| Case-level pro se share, P1 -> P3 | 60.1% -> 76.0% |

No aggregate cross-period trend is asserted in either direction: the P1-vs-P3 qualifying-judgment
difference is -0.30 percentage points, with no interpretable sign, and the pooled census is
reported because no difference between the substantive windows is detected -- establishing
neither decline nor equivalence (Note fns 70-71). Finality classes are archived case by case as
of July 17, 2026; a sensitivity excluding the liability-only class leaves eleven qualifying
judgments and changes no qualitative statement. Intervals are exact 95% Clopper-Pearson.

## B.2 Pleading-Stage Defense-Win Lower Bounds (the Note's fn 140)

On the registered pre-merger 606-basis census (see the basis note in Appendix H SS H.5.3 and ERRATA.md; 2026-08-04 D-QV5), the pleading-stage defense-win floors are 140/287 (48.8%) in P1,
50/68 (73.5%) in P2, and 143/251 (57.0%) in P3. These are lower bounds, not point estimates:
not every coded record includes a complete pleading-stage flag, so the numerators exclude
decided cases whose records do not surface the flag. No cross-period trend is asserted on this
series; see Appendix H § H.5.3.

---
