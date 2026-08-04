# Case-Level Census Rules

This file states the complete rule set that transforms the published per-row
census record ([`case_level_census.csv`](case_level_census.csv), one row per kept
opinion row) into the registered case-level outcome series
([`../results/series_2026-07.json`](../results/series_2026-07.json)). The
transformation is deterministic:
[`../scripts/build_case_level_series.py`](../scripts/build_case_level_series.py)
recomputes the series from the CSV and fails on any drift, and the release gate
runs that check.

## The unit of analysis

One case, one unit. Opinion documents belonging to the same case or proceeding
share a harmonized case identifier (`case_id`); the 730 kept opinion rows resolve
to 598 distinct decided case units. 111 units contain more than one kept row (243
rows in total; 124 rows are absorbed into their unit); 501 units are singletons.
Two units carry split-format identifiers (`FHV2SPLIT02`, `FHV2SPLIT03`) from the
harmonization audit; both are singletons.

## Row-level fields

Each row carries the public database join key (`source_file`), the document
identifiers (`db_index`, `cl_id`; `cl_id` is blank on 14 rows where the upstream
source lacked one), its case unit (`case_id`), a bounded keep code (`keep_code`,
an 11-value closed vocabulary recording why the row is in the decided census),
and the row-level period, side, and representation status (`row_period`,
`row_side`, `row_pro_se`).

Each row also carries the date the rules order on. `row_decision_date` is an ISO
`yyyy-mm-dd` date on every one of the 730 rows, and `date_source` records where
that date comes from: `DECISION_DATE`, the row's stated decision date (364 rows),
or `FILED_DATE`, the filing date used as the fallback where the row states no
decision date (366 rows). The terminal-row rule below reads `row_decision_date`
and nothing else.

## Unit-level fields

Each row also carries its unit's adjudicated attributes, repeated identically on
every row of the unit: `case_period`, `case_outcome`, `case_representation`,
`victory_id` (blank outside the eighteen qualifying judgments), `collapse_type`,
and `member_of_multirow`.

## Case-level rules

- **Outcome.** A unit is VICTORY if it contains a qualifying-judgment row;
  otherwise TRUE_BROAD if it contains a surviving true-broad row; otherwise
  NONFAV. A surviving true-broad row is a row coded TRUE_BROAD_ROW that is
  neither a qualifying-judgment row nor a member of a victory unit; three rows
  qualify, each in its own unit, so no tiebreak among multiple surviving rows in
  one unit has ever been needed.
- **Terminal row.** A unit's terminal row is its latest-dated member row by
  `row_decision_date`; ties break to the higher `db_index`.
- **Period.** A victory unit takes its qualifying-judgment row's period; a
  true-broad unit takes its surviving true-broad row's period; every other unit
  takes its terminal row's period.
- **Representation.** A victory unit takes the qualifying-judgment row's
  representation status; every other unit takes its terminal row's status.
- **Victories.** The eighteen qualifying plaintiff-side judgments carry unit-level
  identifiers `V01`-`V18` (P1: 10, P2: 0, P3: 8). One additional merits
  disposition was reviewed and does not qualify; it contributes no kept rows and
  is outside the 598-unit census.

## What the published record determines

Every unit's outcome, period, and representation re-derives from the published
rows alone. The qualifying-judgment set is published as `victory_id`; the three
surviving true-broad rows fall out of `keep_code` and unit membership; and the
terminal-row rule runs on the published dates. No unit's value is taken on trust
from the unit-level columns -- the build script derives all 598 independently and
compares, reporting any mismatch.

One attribution step deserves a precise statement. In seventeen of the eighteen
victory units the qualifying-judgment row is identifiable by its keep code
(`VICTORY_PRIMARY` in fifteen units, a promoted `TRUE_BROAD_ROW` in two). Where a unit
carries both codes, the `VICTORY_PRIMARY` row controls. In the
eighteenth, `FH0607`, neither member row carries a victory keep code, so the
build script falls back to that unit's terminal row -- but only under an asserted
guard that every member row of the unit agrees on both period and representation,
which they do. The fallback therefore cannot decide either value, and a
heterogeneous member set would fail the check loudly rather than resolve silently.

## The registered series

Applying these rules to the CSV yields, exactly: 598 decided case units, split
283 / 65 / 250 across P1 / P2 / P3; 201 represented and 397 pro se units;
eighteen qualifying judgments (10 / 0 / 8); zero qualifying judgments in pro se
cases. The build script asserts every one of these values and exits nonzero on
any mismatch.

## What this record does and does not establish

The CSV publishes the transformation from kept opinion rows to case units --
which rows exist, how they group, and how each unit's outcome, period, and
representation are determined. It does not establish the legal correctness of
any classification, and upstream screening (which opinions entered the decided
census) is governed by the published tier definitions in
[`SAMPLE_DEFINITIONS.md`](SAMPLE_DEFINITIONS.md).
