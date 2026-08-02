"""Generate _data/series.yml -- the Pages site's census data file.

Every census figure a site page displays comes from this file through Liquid
({{ site.data.series.KEY }}), and this file is generated from the series of
record (results/series_2026-07.json). No census number is hand-typed into a
site page; if the series of record changes, regenerate this file and every
page follows. Print forms follow the canonical presentation: the pooled rate
and the pro se exact upper bound print at one decimal (per-period rates keep
their registered two-decimal form).

Usage:
  python scripts/make_site_data.py           # write _data/series.yml
  python scripts/make_site_data.py --check   # exit 1 if the committed file drifts
"""
from __future__ import annotations

import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIES_PATH = os.path.join(REPO, "results", "series_2026-07.json")
OUT = os.path.join(REPO, "_data", "series.yml")

WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
         6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
         12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
         16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
         20: "twenty"}

HEADER = (
    "# Generated from results/series_2026-07.json by scripts/make_site_data.py.\n"
    "# Do not edit by hand; regenerate after any change to the series of record.\n"
    "# The release gate fails if this file drifts from the series JSON.\n"
)


def derive(series: dict) -> dict[str, str]:
    """Every exposed site-data value, computed from the series of record."""
    n = series["case_level_n_pooled"]
    n_by = series["case_level_n_decided"]
    quals = series["distinct_qualifying_judgments"]
    total = int(sum(quals))
    rates = series["strict_qualifying_rate_pct"]
    pooled = series["strict_qualifying_rate_pooled_pct"]
    fin = series["finality_classes"]
    rvc = series["represented_victory_cell"]
    psc = series["pro_se_victory_cell"]
    shares = series["pro_se_docket_share_case_level_pct"]
    word = WORDS[total]
    pooled_print = f"{round(pooled, 1):.1f}%"
    return {
        "n_pooled": str(n),
        "n_by_period": "{} / {} / {}".format(*n_by),
        "qualifying_total": str(total),
        "qualifying_word": word,
        "qualifying_by_period": "{} / {} / {}".format(*quals),
        "qualifying_phrase": f"{word} qualifying plaintiff-side judgments",
        "rates_prose": "{}, {}, and {}".format(*(f"{v:.2f}%" for v in rates)),
        "pooled_rate_print": pooled_print,
        "combined_print": f"{total}/{n} ({pooled_print})",
        "represented_cell": (
            f"{rvc['numerator']} of {rvc['denominator']} ({rvc['pct']}%)"
        ),
        "pro_se_cell": f"{psc['numerator']} of {psc['denominator']}",
        "pro_se_upper_bound": f"{round(psc['exact_upper_bound_pct'], 1):.1f}%",
        "final_contested": str(fin["final_contested"]),
        "final_default": str(fin["final_default"]),
        "liability_only": str(fin["liability_only"]),
        "finality_phrase": (
            f"{WORDS[fin['final_contested']]} final contested judgments awarding "
            f"relief, {WORDS[fin['final_default']]} final default judgments, and "
            f"{WORDS[fin['liability_only']]} liability determinations"
        ),
        "share_span": f"{shares[0]}% to {shares[-1]}%",
    }


def render() -> str:
    with open(SERIES_PATH, "r", encoding="utf-8") as f:
        series = json.load(f)
    lines = [HEADER]
    for key, value in derive(series).items():
        lines.append(f'{key}: "{value}"\n')
    return "".join(lines)


def main() -> int:
    rendered = render()
    if "--check" in sys.argv[1:]:
        try:
            with open(OUT, encoding="utf-8", newline="") as f:
                committed = f.read()
        except OSError:
            print("FAIL: _data/series.yml is missing; regenerate it with "
                  "scripts/make_site_data.py.")
            return 1
        if committed.replace("\r\n", "\n") != rendered:
            print("FAIL: _data/series.yml does not match the series of record; "
                  "regenerate with scripts/make_site_data.py.")
            return 1
        print("OK: _data/series.yml matches results/series_2026-07.json.")
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(rendered)
    print("wrote _data/series.yml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
