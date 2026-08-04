# Verify One Registered Claim

Ten minutes, mechanically checkable. This walkthrough verifies the article's headline
outcome claim -- that qualifying plaintiff-side judgments occur in about 3% of
decided cases (18 of 598), none of them pro se -- from the public per-row record
through the generated artifact and the release gate.

Requirements: a clone of this repository and Python 3.11+. No API keys, no
external services. Run all commands from the repository root.

## 1. Inspect the claim

Open [`../article/CLAIMS_LEDGER.csv`](../article/CLAIMS_LEDGER.csv) and find row
`C57` (note location "Part II.C Table 1; fns 70-71"), the pooled case-level
census claim. It names the artifact and the scripts behind every printed value in
the series.

## 2. Inspect the per-row record

Open [`case_level_census.csv`](case_level_census.csv): one row per kept opinion
row (730 rows), each carrying its public database key, its case unit, a bounded
keep code, its period, side, and representation fields, and the dated fields the
rules order on (`row_decision_date` and `date_source`). The complete
transformation rules are in [`CASE_LEVEL_RULES.md`](CASE_LEVEL_RULES.md). Spot-
check any row against the public database: its `source_file` matches a record in
[`../data/FHA_Unified_Database.json`](../data/FHA_Unified_Database.json).

## 3. Recompute the series

```bash
python scripts/build_case_level_series.py --check
```

The script collapses the 730 rows into case units, re-derives every unit's
outcome, period, and representation from the row-level fields under the published
rules, recomputes every registered series value, compares against
[`../results/series_2026-07.json`](../results/series_2026-07.json), and exits
nonzero on any mismatch. The run prints all eleven registered cells beside the
registered values -- 598 decided cases; 283/65/250 across the three windows; 201
represented and 397 pro se; eighteen qualifying judgments (10/0/8); zero pro se
victories -- and ends with an OK line.

## 4. Run the release gate

```bash
python scripts/run_release_checks.py
```

The full gate re-verifies this claim's chain along with every other registered
property: claim values, superseded-series denylist, links, pointers, hedges, and
the hash manifest of every tracked file.

## What this verifies -- and what it does not

You have verified that the committed transformation and all downstream
arithmetic reproduce the printed series exactly, from a public per-row record.
You have not verified the legal correctness of any case classification or the
accuracy of model-assigned labels; the classification instruments, disagreement
logs, and validation layers for that question are in
[`../method/`](../method/), and their results are reported as reproducibility,
not accuracy.
