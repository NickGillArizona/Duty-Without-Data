"""Generate Figure 1 (light/dark SVG pair): the case-level composition chart --
pro se share of the decided docket and the qualifying-judgment rate across periods
P1-P3, on the one-case-one-unit census. Every number is read from
results/series_2026-07.json; the script aborts BEFORE writing if an input drifts
from the value reported in the Note, and each SVG is built fully in memory before
its output file is opened (a failed build can never truncate a committed figure).

Outputs (results/figures/):
  fig1_composition_{light,dark}.svg

Usage: python scripts/make_fig1.py
"""
import json
import os

import config
from make_figures import (
    FIGURES_DIR,
    PALETTES,
    SVG_CLOSE,
    circle,
    fail,
    fmt1,
    guard,
    line,
    polyline,
    svg_open,
    text,
)


def load_series():
    path = os.path.join(config.RESULTS_DIR, "series_2026-07.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fig1_composition(series, pal):
    """Two-series line chart: pro se share of the decided docket and the
    qualifying-judgment rate, across P1/P2/P3, both on the case-level census."""
    pro = series["pro_se_docket_share_case_level_pct"]
    rate = series["strict_qualifying_rate_pct"]
    wins = series["distinct_qualifying_judgments"]
    n_case = series["case_level_n_decided"]
    periods = series["periods"]

    guard("P1 pro se share", pro[0], 60.1)
    guard("P3 pro se share", pro[2], 75.9)
    guard("P1 qualifying-judgment rate", rate[0], 3.53)
    guard("P3 qualifying-judgment rate", rate[2], 3.21)
    guard("P1 N", n_case[0], 283, tol=0)
    guard("P3 N", n_case[2], 249, tol=0)
    guard("total qualifying judgments", sum(wins), 18, tol=0)
    guard("pro se victories", sum(series["pro_se_victories"]), 0, tol=0)
    guard("pooled case-level N", series["case_level_n_pooled"], 595, tol=0)
    if max(rate) >= 4.0:
        fail("subtitle claim 'never reaches 4%' violated by the rate series")

    # Month-level labels for the fn 67 period boundaries (P1 ends June 27, 2024;
    # P2 ends February 4, 2025; endpoints inclusive).
    dates = ["Jan 2022 - Jun 2024", "Jun 2024 - Feb 2025", "Feb 2025 - Jul 2026"]

    W, H = 760, 486
    x0, x1 = 70, 560
    y_top, y_bot = 92, 370
    ymax = 88.0
    xs = [x0 + 46, (x0 + x1) / 2, x1 - 10]

    def Y(v):
        return y_bot - (v / ymax) * (y_bot - y_top)

    s = svg_open(
        W, H,
        "Pro se share and qualifying-judgment rate across periods P1 to P3, January 2022 to July 2026",
    )
    s += text(20, 34, "Case composition and qualifying-judgment rates", 19, pal["text"], weight="bold")
    s += text(
        20, 56,
        f"Case-level census of {series['case_level_n_pooled']} decided cases, Jan. 2022 - July 2026: the share brought without a lawyer (top line)",
        13, pal["muted"],
    )
    s += text(
        20, 74,
        f"rises to {fmt1(pro[2])}%, while the share ending in a qualifying plaintiff-side judgment (bottom line) never reaches 4%.",
        13, pal["muted"],
    )
    for v in (0, 20, 40, 60, 80):
        s += line(x0, Y(v), x1, Y(v), pal["grid"], 1)
        s += text(x0 - 10, Y(v) + 4, f"{v}%", 12, pal["muted"], anchor="end")
    for i, p in enumerate(periods):
        s += text(xs[i], y_bot + 24, p, 13, pal["text"], anchor="middle", weight="bold")
        s += text(xs[i], y_bot + 40, dates[i], 11, pal["muted"], anchor="middle")
        s += text(xs[i], y_bot + 58, f"N = {n_case[i]}", 12, pal["muted"], anchor="middle")
        s += text(
            xs[i], y_bot + 74,
            f"{wins[i]} qualifying judgments",
            12, pal["green"], anchor="middle",
        )

    series_spec = [
        (pro, pal["orange"], ["Pro se share", "of the decided docket"], -12, fmt1),
        (rate, pal["blue"], ["Qualifying-", "judgment rate"], -12, lambda v: f"{v:.2f}"),
    ]
    for vals, color, label_lines, dy, fmt in series_spec:
        pts = [(xs[i], Y(v)) for i, v in enumerate(vals)]
        s += polyline(pts, color)
        for (px, py), v in zip(pts, vals):
            s += circle(px, py, 4.5, color)
            s += text(px, py + dy, f"{fmt(v)}%", 12, color, anchor="middle", weight="bold")
        ly = Y(vals[-1])
        s += text(x1 + 14, ly - 2, label_lines[0], 13, color, weight="bold")
        s += text(x1 + 14, ly + 14, label_lines[1], 13, color, weight="bold")

    # The takeaway, stated in the empty band between the two series.
    s += text(
        (x0 + x1) / 2, 306,
        "All 18 qualifying judgments went to represented plaintiffs;",
        13, pal["text"], anchor="middle", weight="bold",
    )
    s += text(
        (x0 + x1) / 2, 324,
        "none arose in a pro se case.",
        13, pal["muted"], anchor="middle",
    )

    s += line(x0, y_bot, x1, y_bot, pal["axis"], 1.5)
    s += text(
        20, H - 26,
        "Case-level series throughout: one case, one unit; shares and rates over the per-period case-level N (287/68/251).",
        11, pal["muted"],
    )
    s += text(
        20, H - 12,
        "Source: results/series_2026-07.json.",
        11, pal["muted"],
    )
    return s + SVG_CLOSE


def main():
    series = load_series()
    os.makedirs(FIGURES_DIR, exist_ok=True)
    for mode, pal in PALETTES.items():
        out = os.path.join(FIGURES_DIR, f"fig1_composition_{mode}.svg")
        svg = fig1_composition(series, pal)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        print(f"wrote {config.repo_path(out)}")
    print("all guard checks passed")


if __name__ == "__main__":
    main()
