"""Phase 0 recall spot-counts, correcting the first pass's unbounded recall differential.

Mirrors the p3-extension collection run's documented API mechanics:
v4 search endpoint,
Token auth from the CL_TOKEN env var (never written to disk; URLs are credential-free),
same date format, same status flags.

Runs count queries for the disability and race arms plus the class-general anchor,
archives the exact URL + first-page raw JSON per query, and computes rough capture-ratio
bounds against the corpus yields. Rough bounds are the registered target; the
interpretation limits are stated in the output.
"""
# As-run execution record from the author's research environment; the input paths
# below do not resolve in this archive. The recorded outputs are committed in this
# study directory.
from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "courtlistener_recall"
ROOT = Path(__file__).resolve().parents[4]
DATA_PATH = ROOT / "data" / "FHA_Unified_Database.json"
BASE = "https://www.courtlistener.com/api/rest/v4/"
STAT = ["stat_Published", "stat_Unpublished", "stat_Errata", "stat_Separate",
        "stat_In-chambers", "stat_Relating-to", "stat_Unknown"]

QUERIES = [
    ("anchor_fha_all", '"fair housing act"'),
    ("disability_arm", '"fair housing act" AND (disability OR handicap)'),
    ("race_arm", '"fair housing act" AND (race OR racial)'),
    ("race_arm_narrow", '"fair housing act" AND race AND discrimination'),
]


def tok() -> str:
    t = os.environ.get("CL_TOKEN", "").strip()
    if not t:
        sys.exit("CL_TOKEN not set")
    return t


def get(url: str, retries: int = 4):
    req = urllib.request.Request(url, headers={"Authorization": f"Token {tok()}", "User-Agent": "dwd-comparator-recall/1.0"})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(5 * (i + 1))


def corpus_counts():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    PER = {"P1": ("2022-01-01", "2024-06-28"), "P2": ("2024-06-28", "2025-02-05"), "P3": ("2025-02-05", "2026-07-02")}

    def in_window(r):
        d = str(r.get("date_filed") or "")
        return bool(d) and any(a <= d < b for a, b in PER.values())

    scr = [r for r in data if r.get("screening_result") == "YES" and in_window(r)]
    return {
        "screened_dated_total": len(scr),
        "race_primary_dated": sum(1 for r in scr if str(r.get("primary_protected_class") or "").lower() == "race"),
        "disability_alleged_dated": sum(1 for r in scr if r.get("disability_alleged") is True),
        "nondisability_dated": sum(1 for r in scr if r.get("disability_alleged") is False),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for label, q in QUERIES:
        p = {"q": q, "type": "o", "filed_after": "01/01/2022", "filed_before": "07/01/2026"}
        for s in STAT:
            p[s] = "on"
        url = BASE + "search/?" + urllib.parse.urlencode(p)
        d = get(url)
        count = d.get("count")
        (OUT / f"{label}_page1_raw.json").write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
        results.append({"label": label, "query": q, "url": url, "count": count})
        print(f"{label}: count={count}")
        time.sleep(0.5)

    corpus = corpus_counts()
    by = {r["label"]: r["count"] for r in results}
    ratio_dis = corpus["disability_alleged_dated"] / by["disability_arm"] if by.get("disability_arm") else None
    ratio_race = corpus["race_primary_dated"] / by["race_arm"] if by.get("race_arm") else None
    differential = (ratio_race / ratio_dis) if ratio_race and ratio_dis else None

    payload = {
        "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "api": "courtlistener /api/rest/v4/search/ (Token auth via header; token held in env only)",
        "queries": results,
        "corpus_yields_dated_screened": corpus,
        "capture_ratio_disability": ratio_dis,
        "capture_ratio_race": ratio_race,
        "race_vs_disability_capture_differential": differential,
        "interpretation_limits": [
            "CL counts include all jurisdictions (the corpus pull filtered federal client-side), so ratios are capture proxies, not recall.",
            "CL keyword counts are over-inclusive (a mention is not a claim); the informative quantity is the RATIO of ratios, under the assumption that over-inclusiveness and state-court mix are broadly similar across arms.",
            "Corpus yields are screened-in classified labels; CL counts are raw keyword hits.",
        ],
    }
    (OUT / "recall_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({k: payload[k] for k in ["capture_ratio_disability", "capture_ratio_race", "race_vs_disability_capture_differential"]}, indent=2))


if __name__ == "__main__":
    main()
