#!/usr/bin/env python3
"""Recompute the case-level outcome series from the published per-row census.

Reads exactly one input -- replication/case_level_census.csv, the per-row record
of the one-case-one-unit transformation -- applies the rules published in
replication/CASE_LEVEL_RULES.md, and recomputes the registered series.

  python scripts/build_case_level_series.py            print the recomputed series
  python scripts/build_case_level_series.py --check    compare against
                                                       results/series_2026-07.json

--check asserts three things and exits nonzero if any of them fails:

  1. Structural invariants of the record: 730 kept opinion rows, 595 case units,
     116 multi-row units, 479 singletons, closed field vocabularies, ISO dates,
     unique row keys, and unit-level columns constant within each unit.
  2. Rule re-derivation. Every unit's outcome, period and representation is
     re-derived from the row-level fields alone -- including the terminal-row
     rule (latest row_decision_date, ties broken to the higher db_index) -- and
     compared against the unit-level columns. One victory unit's
     qualifying-judgment row is not identifiable from its keep codes; for any
     such unit the terminal row is used ONLY under a member-homogeneity guard
     (all member rows agree on period and representation), and a heterogeneous
     member set fails the check loudly.
  3. The eleven registered cells, compared against the values READ AT RUNTIME
     from results/series_2026-07.json (no expected value is hard-coded here),
     plus the registered per-window representation cross-checks.

No third-party dependencies; no network access.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.join(REPO, "replication", "case_level_census.csv")
SERIES = os.path.join(REPO, "results", "series_2026-07.json")

# Structural invariants of the published record (shape, not series values).
EXPECT_ROWS = 730
EXPECT_UNITS = 595
EXPECT_MULTIROW = 116
EXPECT_SINGLETON = 479

PERIODS = ("P1", "P2", "P3")
OUTCOMES = ("VICTORY", "TRUE_BROAD", "NONFAV")
DATE_SOURCES = ("DECISION_DATE", "FILED_DATE")
UNIT_COLS = ("case_period", "case_outcome", "case_representation",
             "victory_id", "collapse_type", "member_of_multirow")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class CheckError(Exception):
    pass


def _fail(msg):
    raise CheckError(msg)


def rep_of(row):
    return "PRO_SE" if row["row_pro_se"] == "True" else "REPRESENTED"


def terminal_row(members):
    """The terminal row: latest row_decision_date; ties to the higher db_index."""
    return max(members, key=lambda r: (r["row_decision_date"], int(r["db_index"])))


def load_units(path):
    """Read the census and group rows into case units (rows sorted by db_index)."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        _fail("census CSV is empty: %s" % path)
    units = collections.OrderedDict()
    for r in rows:
        units.setdefault(r["case_id"], []).append(r)
    for c in units:
        units[c].sort(key=lambda r: int(r["db_index"]))
    return rows, units


def check_structure(rows, units, log):
    """Invariant 1: shape of the record."""
    log("rows", len(rows), EXPECT_ROWS)
    log("case units", len(units), EXPECT_UNITS)
    multirow = [c for c, m in units.items() if len(m) > 1]
    singleton = [c for c, m in units.items() if len(m) == 1]
    log("multi-row units", len(multirow), EXPECT_MULTIROW)
    log("singleton units", len(singleton), EXPECT_SINGLETON)
    log("absorbed rows (rows - units)", len(rows) - len(units),
        EXPECT_ROWS - EXPECT_UNITS)

    dbs = [r["db_index"] for r in rows]
    log("distinct db_index", len(set(dbs)), len(dbs))
    log("blank source_file", sum(1 for r in rows if not r["source_file"].strip()), 0)

    bad = sorted({r["row_period"] for r in rows} - set(PERIODS))
    log("row_period vocabulary closed", bad or "closed", "closed")
    bad = sorted({r["case_period"] for r in rows} - set(PERIODS))
    log("case_period vocabulary closed", bad or "closed", "closed")
    bad = sorted({r["case_outcome"] for r in rows} - set(OUTCOMES))
    log("case_outcome vocabulary closed", bad or "closed", "closed")
    bad = sorted({r["row_pro_se"] for r in rows} - {"True", "False"})
    log("row_pro_se vocabulary closed", bad or "closed", "closed")
    bad = sorted({r["case_representation"] for r in rows} - {"PRO_SE", "REPRESENTED"})
    log("case_representation vocabulary closed", bad or "closed", "closed")
    log("keep_code vocabulary size", len({r["keep_code"] for r in rows}), 11)

    log("row_decision_date all ISO yyyy-mm-dd",
        sum(1 for r in rows if not ISO_DATE.match(r["row_decision_date"])), 0)
    bad = sorted({r["date_source"] for r in rows} - set(DATE_SOURCES))
    log("date_source vocabulary closed", bad or "closed", "closed")
    print("    date provenance   : %s"
          % dict(collections.Counter(r["date_source"] for r in rows)))

    nonconstant = [(c, col) for c, m in units.items() for col in UNIT_COLS
                   if len({r[col] for r in m}) > 1]
    log("unit columns constant within unit", nonconstant or "constant", "constant")

    vids = sorted({m[0]["victory_id"] for m in units.values() if m[0]["victory_id"]})
    expect_vids = ["V%02d" % i for i in range(1, len(vids) + 1)]
    log("victory_id values contiguous from V01",
        "%s..%s" % (vids[0], vids[-1]) if vids == expect_vids else vids,
        "%s..%s" % (expect_vids[0], expect_vids[-1]) if expect_vids else "none")
    vic_units = [c for c, m in units.items() if m[0]["case_outcome"] == "VICTORY"]
    log("victory_id count == victory unit count", len(vids), len(vic_units))
    stray = [c for c, m in units.items()
             if bool(m[0]["victory_id"]) != (m[0]["case_outcome"] == "VICTORY")]
    log("victory_id set == VICTORY outcome set", stray or "aligned", "aligned")


def derive(units, log):
    """Invariant 2: re-derive outcome, period and representation from the rows."""
    outcome_mismatch, period_mismatch, rep_mismatch = [], [], []
    attrib_source = collections.Counter()
    fallback_units, guard_violations, tb_ambiguous = [], [], []
    surviving_tb = []

    for cid, mem in units.items():
        unit = mem[0]
        tb_rows = [r for r in mem if r["keep_code"] == "TRUE_BROAD_ROW"]
        terminal = terminal_row(mem)

        # -- outcome rule: VICTORY > surviving TRUE_BROAD > NONFAV ------------
        if unit["victory_id"]:
            outcome = "VICTORY"
        elif tb_rows:
            outcome = "TRUE_BROAD"
            surviving_tb.extend(r["db_index"] for r in tb_rows)
        else:
            outcome = "NONFAV"
        if outcome != unit["case_outcome"]:
            outcome_mismatch.append((cid, outcome, unit["case_outcome"]))

        # -- period and representation rules ----------------------------------
        if outcome == "VICTORY":
            vp = [r for r in mem if r["keep_code"] == "VICTORY_PRIMARY"]
            if len(vp) == 1:
                attrib, src = vp[0], "victory row (VICTORY_PRIMARY)"
            elif not vp and len(tb_rows) == 1:
                attrib, src = tb_rows[0], "victory row (promoted TRUE_BROAD_ROW)"
            else:
                # No qualifying-judgment row is identifiable from the keep codes.
                # Fall back to the terminal row ONLY where every member row agrees
                # on period and representation, so the fallback cannot decide a
                # value; a heterogeneous member set is a hard failure.
                attrib, src = terminal, "terminal row (guarded fallback)"
                fallback_units.append(cid)
                if (len({r["row_period"] for r in mem}) > 1
                        or len({rep_of(r) for r in mem}) > 1):
                    guard_violations.append(cid)
            period_row, rep_row = attrib, attrib
        elif outcome == "TRUE_BROAD":
            if len(tb_rows) != 1:
                tb_ambiguous.append(cid)
            period_row, rep_row, src = tb_rows[0], terminal, "true-broad row"
        else:
            period_row, rep_row, src = terminal, terminal, "terminal row"
        attrib_source[src] += 1

        if period_row["row_period"] != unit["case_period"]:
            period_mismatch.append((cid, period_row["row_period"], unit["case_period"]))
        if rep_of(rep_row) != unit["case_representation"]:
            rep_mismatch.append((cid, rep_of(rep_row), unit["case_representation"]))

    tb_units = [c for c, m in units.items() if m[0]["case_outcome"] == "TRUE_BROAD"]
    log("outcome re-derived for every unit",
        "%d mismatches" % len(outcome_mismatch), "0 mismatches")
    log("surviving true-broad rows", len(surviving_tb), 3)
    log("  each in its own unit", len(tb_units), len(surviving_tb))
    log("  no true-broad tiebreak needed", tb_ambiguous or "none", "none")
    log("period re-derived for every unit",
        "%d mismatches" % len(period_mismatch), "0 mismatches")
    log("representation re-derived for every unit",
        "%d mismatches" % len(rep_mismatch), "0 mismatches")
    if guard_violations:
        print("    !! HOMOGENEITY GUARD VIOLATED for %s: the fallback attribution "
              "row is not determined by the published record" % guard_violations)
    log("victory fallback homogeneity guard",
        guard_violations or "held for %s" % (fallback_units or "no unit"),
        "held for %s" % (fallback_units or "no unit"))
    print("    attribution rows  : %s" % dict(attrib_source))
    for label, mism in (("outcome", outcome_mismatch), ("period", period_mismatch),
                        ("representation", rep_mismatch)):
        for cid, got, want in mism[:10]:
            print("      MISMATCH %-14s %s derived=%s published=%s"
                  % (label, cid, got, want))


def compute_series(units):
    """The recomputed series, from the verified unit-level values."""
    vals = [m[0] for m in units.values()]
    n_by_period = collections.Counter(u["case_period"] for u in vals)
    rep_ct = collections.Counter(u["case_representation"] for u in vals)
    vic = [u for u in vals if u["case_outcome"] == "VICTORY"]
    vic_by_period = collections.Counter(u["case_period"] for u in vic)
    vic_rep = collections.Counter(u["case_representation"] for u in vic)
    rows = sum(len(m) for m in units.values())
    multirow = sum(1 for m in units.values() if len(m) > 1)
    return {
        "basis": "one_case_one_unit_case_level",
        "unit_definition": "harmonized case id (case_id)",
        "kept_opinion_rows": rows,
        "decided_cases_total": len(units),
        "decided_cases_by_period": {p: n_by_period.get(p, 0) for p in PERIODS},
        "represented_total": rep_ct.get("REPRESENTED", 0),
        "pro_se_total": rep_ct.get("PRO_SE", 0),
        "represented_by_period": {
            p: sum(1 for u in vals if u["case_period"] == p
                   and u["case_representation"] == "REPRESENTED") for p in PERIODS},
        "pro_se_by_period": {
            p: sum(1 for u in vals if u["case_period"] == p
                   and u["case_representation"] == "PRO_SE") for p in PERIODS},
        "victories_total": len(vic),
        "victories_by_period": {p: vic_by_period.get(p, 0) for p in PERIODS},
        "pro_se_victories": vic_rep.get("PRO_SE", 0),
        "pro_se_victories_by_period": {
            p: sum(1 for u in vic if u["case_period"] == p
                   and u["case_representation"] == "PRO_SE") for p in PERIODS},
        "victories_among_represented": [len(vic), rep_ct.get("REPRESENTED", 0)],
        "victories_among_pro_se": [vic_rep.get("PRO_SE", 0), rep_ct.get("PRO_SE", 0)],
        "multirow_cases": multirow,
        "singleton_cases": len(units) - multirow,
        "absorbed_rows": rows - len(units),
    }


def registered_cells(series_path):
    """The eleven registered cells, READ AT RUNTIME from the series of record."""
    with open(series_path, encoding="utf-8") as fh:
        s = json.load(fh)
    n = s["case_level_n_decided"]
    v = s["distinct_qualifying_judgments"]
    cells = [
        ("decided case units (pooled)", s["case_level_n_pooled"]),
        ("decided case units P1", n[0]),
        ("decided case units P2", n[1]),
        ("decided case units P3", n[2]),
        ("represented units (pooled)", s["represented_pooled"]),
        ("pro se units (pooled)", s["pro_se_pooled"]),
        ("qualifying judgments (total)", sum(v)),
        ("qualifying judgments P1", v[0]),
        ("qualifying judgments P2", v[1]),
        ("qualifying judgments P3", v[2]),
        ("qualifying judgments in pro se cases", s["pro_se_victory_cell"]["numerator"]),
    ]
    extra = [
        ("represented per window", s["represented_per_window"]),
        ("pro se per window", s["pro_se_per_window"]),
        ("represented victory cell denominator", s["represented_victory_cell"]["denominator"]),
        ("represented victory cell numerator", s["represented_victory_cell"]["numerator"]),
        ("pro se victory cell denominator", s["pro_se_victory_cell"]["denominator"]),
        ("pro se victories per window", s["pro_se_victories"]),
    ]
    return cells, extra


def recomputed_cells(series):
    d = series["decided_cases_by_period"]
    v = series["victories_by_period"]
    cells = [
        ("decided case units (pooled)", series["decided_cases_total"]),
        ("decided case units P1", d["P1"]),
        ("decided case units P2", d["P2"]),
        ("decided case units P3", d["P3"]),
        ("represented units (pooled)", series["represented_total"]),
        ("pro se units (pooled)", series["pro_se_total"]),
        ("qualifying judgments (total)", series["victories_total"]),
        ("qualifying judgments P1", v["P1"]),
        ("qualifying judgments P2", v["P2"]),
        ("qualifying judgments P3", v["P3"]),
        ("qualifying judgments in pro se cases", series["pro_se_victories"]),
    ]
    r = series["represented_by_period"]
    p = series["pro_se_by_period"]
    ps_vic = series["pro_se_victories_by_period"]
    extra = [
        ("represented per window", [r["P1"], r["P2"], r["P3"]]),
        ("pro se per window", [p["P1"], p["P2"], p["P3"]]),
        ("represented victory cell denominator", series["represented_total"]),
        ("represented victory cell numerator", series["victories_total"]),
        ("pro se victory cell denominator", series["pro_se_total"]),
        ("pro se victories per window", [ps_vic[x] for x in PERIODS]),
    ]
    return cells, extra


def run_check():
    failures = []

    def log(label, got, want):
        ok = got == want
        if not ok:
            failures.append((label, got, want))
        print("  [%s] %-42s got=%s want=%s"
              % ("PASS" if ok else "FAIL", label, got, want))

    rows, units = load_units(CENSUS)
    print("Input: replication/case_level_census.csv")
    print()
    print("1. STRUCTURAL INVARIANTS OF THE PUBLISHED RECORD")
    check_structure(rows, units, log)
    print()
    print("2. RULE RE-DERIVATION (replication/CASE_LEVEL_RULES.md)")
    derive(units, log)

    series = compute_series(units)
    print()
    print("3. REGISTERED CELLS vs results/series_2026-07.json (read at runtime)")
    reg, reg_extra = registered_cells(SERIES)
    got, got_extra = recomputed_cells(series)
    print("  %-40s %14s %14s  RESULT" % ("CELL", "RECOMPUTED", "REGISTERED"))
    print("  " + "-" * 76)
    for (label, want), (label2, have) in zip(reg, got):
        assert label == label2
        ok = have == want
        if not ok:
            failures.append((label, have, want))
        print("  %-40s %14s %14s  %s"
              % (label, have, want, "PASS" if ok else "FAIL"))
    print("  " + "-" * 76)
    print("  eleven registered cells compared")
    print()
    print("   additional registered cross-checks")
    for (label, want), (label2, have) in zip(reg_extra, got_extra):
        assert label == label2
        ok = have == want
        if not ok:
            failures.append((label, have, want))
        print("  %-40s %14s %14s  %s"
              % (label, have, want, "PASS" if ok else "FAIL"))

    print()
    if failures:
        print("FAIL: %d check(s) failed" % len(failures))
        for label, have, want in failures:
            print("  %s: recomputed=%s registered=%s" % (label, have, want))
        return 1
    print("OK: all eleven registered cells, the structural invariants, and the "
          "rule re-derivation reproduce from replication/case_level_census.csv.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="compare the recomputed series against "
                         "results/series_2026-07.json and exit nonzero on drift")
    args = ap.parse_args()
    try:
        if args.check:
            return run_check()
        _rows, units = load_units(CENSUS)
        print(json.dumps(compute_series(units), indent=2, sort_keys=True))
        return 0
    except CheckError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    except (OSError, KeyError, ValueError) as exc:
        print("ERROR: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
