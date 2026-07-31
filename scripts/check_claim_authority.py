"""Gate check: the front-door claim blocks are derivations of the machine
authority, not hand-maintained copies.

The series of record (results/series_2026-07.json) is the sole machine
authority for the case-level census. Each guarded front-door page carries one
marker-delimited claim block:

    <!-- claim-block: census-headline -->
    ...prose stating the headline census...
    <!-- /claim-block -->

Every literal this check requires INSIDE a block is computed at runtime from
the series JSON -- nothing here restates a number. If the series of record
ever changes, the derived literals change with it and every page that still
carries the old prose fails loudly, with the file, the block, and the missing
literal printed. This complements check_advocacy_claims.py (the registry
layer, which asserts the registered strings): this check binds the pages to
the machine object itself.

Usage:
  python scripts/check_claim_authority.py             # gate mode
  python scripts/check_claim_authority.py --selftest  # fixture tests
"""
from __future__ import annotations

import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIES_PATH = os.path.join(REPO, "results", "series_2026-07.json")

OPEN_RE = re.compile(r"<!--\s*claim-block:\s*census-headline\s*-->")
CLOSE_RE = re.compile(r"<!--\s*/claim-block\s*-->")

WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
         6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
         12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
         16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
         20: "twenty"}


def derive_literals(series: dict) -> dict[str, str]:
    """Every front-door literal, computed from the series of record."""
    n_pooled = series["case_level_n_pooled"]
    quals = series["distinct_qualifying_judgments"]
    rates = series["strict_qualifying_rate_pct"]
    rvc = series["represented_victory_cell"]
    psc = series["pro_se_victory_cell"]
    shares = series["pro_se_docket_share_case_level_pct"]
    word = WORDS[int(sum(quals))]
    return {
        "n_decided_cases": f"{n_pooled} decided cases",
        "qualifying_word": word,
        "qualifying_phrase": f"{word} qualifying plaintiff-side judgments",
        "rates_slash": " / ".join(f"{v:.2f}%" for v in rates),
        "rates_prose": "{}, {}, and {}".format(*(f"{v:.2f}%" for v in rates)),
        "represented_cell": f"{rvc['numerator']} of {rvc['denominator']} ({rvc['pct']}%)",
        "pro_se_zero": f"0 of {psc['denominator']}",
        "pro_se_none": f"none of the {psc['denominator']} pro se cases",
        "share_span": f"{shares[0]}% to {shares[-1]}%",
    }


# page -> literal keys that must appear inside its census-headline block
PAGES: dict[str, tuple[str, ...]] = {
    "README.md": ("n_decided_cases", "qualifying_phrase", "rates_slash",
                  "represented_cell", "pro_se_zero", "share_span"),
    "index.md": ("n_decided_cases", "qualifying_word", "pro_se_none"),
    os.path.join("article", "THE_ARGUMENT.md"): (
        "qualifying_phrase", "n_decided_cases", "rates_prose", "share_span"),
}


def check_page(rel: str, text: str, literals: dict[str, str],
               keys: tuple[str, ...]) -> list[str]:
    problems: list[str] = []
    opens = list(OPEN_RE.finditer(text))
    closes = list(CLOSE_RE.finditer(text))
    if len(opens) != 1 or len(closes) != 1:
        problems.append(
            f"{rel}: expected exactly one census-headline claim block "
            f"(found {len(opens)} open / {len(closes)} close markers)")
        return problems
    if opens[0].end() > closes[0].start():
        problems.append(f"{rel}: claim-block close marker precedes the open marker")
        return problems
    block = text[opens[0].end():closes[0].start()]
    for key in keys:
        lit = literals[key]
        if lit not in block:
            problems.append(
                f"{rel}: claim block is missing the series-derived literal "
                f"{lit!r} ({key})")
    return problems


def run_gate() -> int:
    with open(SERIES_PATH, "r", encoding="utf-8") as f:
        series = json.load(f)
    literals = derive_literals(series)
    problems: list[str] = []
    for rel, keys in PAGES.items():
        path = os.path.join(REPO, rel)
        try:
            text = open(path, "r", encoding="utf-8").read()
        except OSError as exc:
            problems.append(f"{rel}: unreadable ({exc})")
            continue
        problems.extend(check_page(rel.replace(os.sep, "/"), text, literals, keys))
    if problems:
        print("Claim-authority failures:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1
    n = sum(len(k) for k in PAGES.values())
    print(f"OK: {len(PAGES)} front-door claim blocks carry all {n} "
          "series-derived literals (authority: results/series_2026-07.json)")
    return 0


def run_selftest() -> int:
    series = {
        "case_level_n_pooled": 606,
        "distinct_qualifying_judgments": [10, 0, 8],
        "strict_qualifying_rate_pct": [3.48, 0.00, 3.19],
        "represented_victory_cell": {"numerator": 18, "denominator": 206, "pct": 8.7},
        "pro_se_victory_cell": {"numerator": 0, "denominator": 400},
        "pro_se_docket_share_case_level_pct": [59.6, 55.9, 76.1],
    }
    lits = derive_literals(series)
    good_block = ("x\n<!-- claim-block: census-headline -->\n"
                  "Of the 606 decided cases, eighteen qualifying plaintiff-side "
                  "judgments appear (3.48% / 0.00% / 3.19%); 18 of 206 (8.7%) "
                  "represented; 0 of 400 pro se; share rose 59.6% to 76.1%.\n"
                  "<!-- /claim-block -->\ny\n")
    cases = [
        ("derives rates", lits["rates_slash"] == "3.48% / 0.00% / 3.19%", True),
        ("derives word", lits["qualifying_word"] == "eighteen", True),
        ("derives cell", lits["represented_cell"] == "18 of 206 (8.7%)", True),
        ("good block passes", not check_page("f.md", good_block, lits,
                                             PAGES["README.md"]), True),
        ("missing marker fails", bool(check_page("f.md", "no markers here",
                                                 lits, ("qualifying_word",))), True),
        ("mutated literal fails", bool(check_page(
            "f.md", good_block.replace("eighteen", "sixteen"), lits,
            ("qualifying_phrase",))), True),
        ("literal outside block fails", bool(check_page(
            "f.md", "606 decided cases\n<!-- claim-block: census-headline -->\n"
            "empty\n<!-- /claim-block -->\n", lits, ("n_decided_cases",))), True),
        ("double marker fails", bool(check_page(
            "f.md", good_block + good_block, lits, ("qualifying_word",))), True),
    ]
    passed = 0
    for name, got, want in cases:
        ok = got == want
        passed += int(ok)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"self-test: {passed}/{len(cases)} passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(run_selftest() if "--selftest" in sys.argv[1:] else run_gate())
