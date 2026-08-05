#!/usr/bin/env python3
"""Validate key statistics reported in the note against the database and the
case-level series of record (results/series_2026-07.json; UNIVERSAL
one-case-one-unit basis, N = 595; restated 2026-08-04, D-QV5 + D-QV5-2 + W1B-ADJ).

Three layers: (1) document-level pipeline counts recomputed from
data/FHA_Unified_Database.json; (2) the case-level series asserted field by
field against series_2026-07.json (incl. fn 140 floors, broad rates, and the
exact Clopper-Pearson cells); (3) text assertions on the Appendix A-7
case-level selection-audit surface.

Loads FHA_Unified_Database.json and checks counts, win rates, and pro-se rates
against the values cited in the article. The first block asserts the raw
document-level pipeline output (computed from the database; UNCHANGED by the
case-level collapse, by construction). The second asserts the case-level
outcome series reported in Part II on the universal 595 basis. Both must pass.

Usage:
  python scripts/validate_claims.py                # both layers (needs the DB)
  python scripts/validate_claims.py --series-only  # case-level layer only
"""
import json
import sys
import os

# -- paths --------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import UNIFIED_DB_PATH
from analysis_filters import (
    DECIDED_OUTCOMES as DECIDED,
    assign_period,
    is_decided,
    is_screened_in,
    is_t2_canonical,
)

TOLERANCE_PP = 0.15  # percentage-point tolerance for rounded manuscript rates

# The case-level series artifact checked by layer (2).
SERIES_FILENAME = "series_2026-07.json"


def load_db(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def strict_win_rate(cases):
    decided = [c for c in cases if c.get("outcome") in DECIDED]
    if not decided:
        return 0.0, 0
    wins = sum(1 for c in decided if c.get("outcome") == "PLAINTIFF_WIN")
    return (wins / len(decided)) * 100.0, len(decided)


def pro_se_rate(cases):
    if not cases:
        return 0.0
    pro_se = sum(1 for c in cases
                 if str(c.get("pro_se", "")).lower() in ("true", "yes", "1")
                 or c.get("pro_se") is True)
    return (pro_se / len(cases)) * 100.0


def check_case_level_series():
    """Assert the case-level outcome series reported in Part II on the
    UNIVERSAL 595 basis (results/series_2026-07.json)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "results", SERIES_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        cs = json.load(f)

    def eq(a, b):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return abs(float(a) - float(b)) <= 1e-9
        return len(a) == len(b) and all(
            abs(float(x) - float(y)) <= 1e-9 for x, y in zip(a, b))

    fc = cs["finality_classes"]
    rvc = cs["represented_victory_cell"]
    psc = cs["pro_se_victory_cell"]
    f140 = cs["fn140_pleading_share"]
    ucb = cs["under_call_bound"]
    cp = cs["clopper_pearson_95_pct"]
    checks = [
        ("case-level N (283/63/249)",  cs["case_level_n_decided"],            [283, 63, 249]),
        ("case-level N pooled",        cs["case_level_n_pooled"],             595),
        ("qualifying judgments",       cs["distinct_qualifying_judgments"],   [10, 0, 8]),
        ("strict rate % (per window)", cs["strict_qualifying_rate_pct"],      [3.53, 0.00, 3.21]),
        ("strict rate % (pooled)",     cs["strict_qualifying_rate_pooled_pct"], 3.03),
        ("finality classes 9/2/7",     [fc["final_contested"], fc["final_default"],
                                        fc["liability_only"]],                [9, 2, 7]),
        ("sensitivity excl. liab.",    cs["sensitivity_excluding_liability_only"], 11),
        ("represented per window",     cs["represented_per_window"],          [113, 25, 60]),
        ("represented pooled",         cs["represented_pooled"],              198),
        ("pro se per window",          cs["pro_se_per_window"],               [170, 38, 189]),
        ("pro se pooled",              cs["pro_se_pooled"],                   397),
        ("represented cell 18/198",    [rvc["numerator"], rvc["denominator"]], [18, 198]),
        ("represented cell 9.1%",      rvc["pct"],                            9.1),
        ("pro se victories 0/397",     [psc["numerator"], psc["denominator"]], [0, 397]),
        ("pro se victories (zero)",    cs["pro_se_victories"],                [0, 0, 0]),
        ("pro se exact upper bound",   psc["exact_upper_bound_pct"],          0.925),
        ("docket shares 60.1->75.9",   cs["pro_se_docket_share_case_level_pct"],
                                                                             [60.1, 60.3, 75.9]),
        ("broad numerators",           cs["broad_favorable_numerators"],      [12, 0, 9]),
        ("broad favorable rate %",     cs["broad_favorable_rate_pct"],        [4.24, 0.00, 3.61]),
        ("P1-vs-P3 diff pp",           cs["p1_vs_p3_strict_diff_pp"],         -0.32),
        ("fn 140 floor numerators",    f140["numerators"],                    [142, 48, 144]),
        ("fn 140 floor denominators",  f140["denominators"],                  [283, 63, 249]),
        ("fn 140 floor pct",           f140["pct"],                           [50.2, 76.2, 57.8]),
        ("represented cell 95% CI",    rvc["ci95_pct"],                       [5.477, 13.987]),
        ("under-call bound 1/595",     [ucb["numerator"], ucb["denominator"]], [1, 595]),
        ("under-call upper bound %",   ucb["exact_upper_bound_pct"],          0.933),
        ("CP interval 18/595",         cp["18_595"],                          [1.8026, 4.7391]),
        ("CP interval 0/397",          cp["0_397"],                           [0.0, 0.925]),
        ("CP interval 1/595",          cp["1_595"],                           [0.0043, 0.933]),
    ]
    passes = fails = 0
    print()
    print("Case-level outcome series (reported in Part II; universal 595 basis)")
    print(f"{'FIELD':<28} {'EXPECTED':>20} {'ACTUAL':>20}  RESULT")
    print("-" * 78)
    for label, actual, expected in checks:
        ok = eq(actual, expected)
        passes += int(ok)
        fails += int(not ok)
        print(f"  {label:<26} {str(expected):>20} {str(actual):>20}  {'PASS' if ok else 'FAIL'}")
    print("-" * 78)
    print(f"  {passes} passed, {fails} failed out of {passes + fails} corrected-series checks")
    return passes, fails


def check_a7_case_level_text():
    """Text-level guard: Appendix A-7 must carry the printed case-level
    selection-audit result (fn 90: INDETERMINATE, +11.67pp SJ-posture shift).
    The registered document-level run is asserted numerically by the
    strengthening recompute; this check protects the CASE-LEVEL surface, whose
    per-case inputs are upstream of the public repo."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "article", "appendices",
                        "Appendix_A7_Selection_and_Participation.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    required = [
        ("A-7 case-level INDETERMINATE", "INDETERMINATE"),
        ("A-7 max shift +12.77pp",       "+12.77"),
        ("A-7 SJ cell 23.9% (27/113)",   "23.9% (27/113)"),
        ("A-7 SJ cell 36.7% (22/60)",    "36.7% (22/60)"),
    ]
    passes = fails = 0
    print()
    print("Appendix A-7 case-level selection-audit surface (text assertions)")
    for label, needle in required:
        ok = needle in text
        passes += int(ok)
        fails += int(not ok)
        print(f"  {label:<32} {'PASS' if ok else 'FAIL'}")
    print(f"  {passes} passed, {fails} failed out of {passes + fails} A-7 text assertions")
    return passes, fails


def main():
    series_only = "--series-only" in sys.argv[1:]

    passes = fails = 0
    if not series_only:
        print("Loading database:", UNIFIED_DB_PATH)
        db = load_db(UNIFIED_DB_PATH)
        if isinstance(db, dict):
            db = list(db.values())

        fha_cases = [c for c in db if is_screened_in(c)]
        disability_cases = [c for c in db if is_t2_canonical(c)]

        p1 = [c for c in disability_cases if assign_period(c) == "P1" and is_decided(c)]
        p2 = [c for c in disability_cases if assign_period(c) == "P2" and is_decided(c)]
        p3 = [c for c in disability_cases if assign_period(c) == "P3" and is_decided(c)]
        dated_decided = p1 + p2 + p3

        p1_wr, p1_n = strict_win_rate(p1)
        p2_wr, p2_n = strict_win_rate(p2)
        p3_wr, p3_n = strict_win_rate(p3)

        pro_se_p1 = pro_se_rate(p1)
        pro_se_p3 = pro_se_rate(p3)

        # -- claims -----------------------------------------------------------
        # Dataset dimensions: DB = 3,366; T2 = 1,900; endpoint July 1, 2026.
        # Raw DOCUMENT-LEVEL pipeline output computed from the database;
        # unchanged by the case-level collapse by construction. These are
        # document-level counts and composition shares only. Document-level
        # OUTCOME rates are not registered claim targets; the reported Part II
        # series is the case-level series asserted by check_case_level_series()
        # below.
        claims = [
            ("Total FHA cases",       2690,  len(fha_cases),  0,             "count"),
            ("T2 disability cases",    1900,  len(disability_cases), 0,       "count"),
            ("Dated-decided T2",        995,  len(dated_decided),    0,       "count"),
            ("P1 decided n",          476,   p1_n,            0,             "count"),
            ("P2 decided n",          120,   p2_n,            0,             "count"),
            ("P3 decided n",          399,   p3_n,            0,             "count"),
            ("P1 pro se share %",     60.1,  pro_se_p1,       TOLERANCE_PP,  "pct"),
            ("P3 pro se share %",     77.9,  pro_se_p3,       TOLERANCE_PP,  "pct"),
        ]

        print()
        print(f"{'CLAIM':<25} {'EXPECTED':>10} {'ACTUAL':>10}  RESULT")
        print("-" * 60)

        for label, expected, actual, tol, kind in claims:
            if kind == "pct":
                exp_s = f"{expected:.1f}%"
                act_s = f"{actual:.1f}%"
                ok = abs(expected - actual) <= tol
            else:
                exp_s = str(expected)
                act_s = str(actual)
                ok = abs(expected - actual) <= tol

            status = "PASS" if ok else "FAIL"
            if ok:
                passes += 1
            else:
                fails += 1
            print(f"  {label:<23} {exp_s:>10} {act_s:>10}  {status}")

        print("-" * 60)
        print(f"  {passes} passed, {fails} failed out of {passes + fails} document-level claims")
        print()
    else:
        print("--series-only: skipping document-level DB layer")

    cs_passes, cs_fails = check_case_level_series()
    a7_passes, a7_fails = check_a7_case_level_text()
    total_fails = fails + cs_fails + a7_fails
    print()
    print(f"TOTAL: {passes + cs_passes + a7_passes} passed, {total_fails} failed "
          "(document-level + case-level + A-7 text layers)")

    sys.exit(1 if total_fails > 0 else 0)


if __name__ == "__main__":
    main()
