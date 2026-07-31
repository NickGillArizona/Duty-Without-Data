"""Phase 0 of the AI verification protocol.

Resolves raw opinion text for all 476 comparator rows and builds the R1 (decisive-row audit)
and R2 (full raw-text recode) input sets. Coverage gate: >= 95% per arm.

Resolution order:
  1. <repo>/case_texts/{source_file}.txt      (committed store; clean-clone primary)
  2. allFHAcases/**/{source_file}.txt         (author-archive master store, if present)
  3. results/v128/p3_extension_2026-07-03/opinions/{cluster_id}.txt (author archive)
  4. (left to a fetch step) CourtListener API by cluster id — scripts/fetch_opinion_texts.py

Outputs under recoding_2026-07-07/raw_text_verification/:
  verification_inputs_r2.json  - all rows with resolved text path + masked-lane consensus code
  verification_inputs_r1.json  - the audit subset with r1_role labels
  coverage_report.json
"""
from __future__ import annotations

import csv
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

# Repo-relative layout: this script lives at <repo>/replication/comparator/recoding_2026-07-07/scripts/.
REPO = Path(__file__).resolve().parents[3]
STUDY = Path(__file__).resolve().parents[2]
OUT = STUDY / "recoding_2026-07-07" / "raw_text_verification"
P5 = STUDY / "recoding_2026-07-07" / "consensus_stage"

# Opinion-text stores in resolution order. The committed case_texts/ store is primary so this
# build runs from a clean clone; the remaining entries are author-archive fallbacks that exist
# only in the author's working environment.
STORES = {
    "case_texts": REPO / "case_texts",
    "allFHAcases": REPO.parent / "allFHAcases",
    "p3ext": REPO.parent / "results" / "v128" / "p3_extension_2026-07-03" / "opinions",
}


def cluster_id(sf: str):
    m = re.match(r"^(\d{6,9})_", sf or "")
    return m.group(1) if m else None


def build_all_fha_index():
    idx = {}
    store = STORES["allFHAcases"]
    if store.exists():
        for p in store.rglob("*.txt"):
            idx.setdefault(p.stem, p)  # stem == source_file
    return idx


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = json.loads((P5 / "consensus_inputs.json").read_text(encoding="utf-8"))
    consensus = {}
    with (STUDY / "RATIONALE_CODED_ROWS_CONSENSUS.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            consensus[f"{r['arm']}|{r['source_file']}"] = r

    afc = build_all_fha_index()
    rows, misses = [], []
    res_counter = Counter()
    for inp in inputs:
        sf = inp["source_file"]
        cid = cluster_id(sf)
        path, source = None, None
        if (STORES["case_texts"] / f"{sf}.txt").exists():
            path, source = STORES["case_texts"] / f"{sf}.txt", "case_texts"
        elif sf in afc:
            path, source = afc[sf], "allFHAcases"
        elif cid and (STORES["p3ext"] / f"{cid}.txt").exists():
            path, source = STORES["p3ext"] / f"{cid}.txt", "p3ext"
        res_counter[source or "MISSING"] += 1
        # Emit repo-relative POSIX paths (no local user paths in committed artifacts);
        # author-archive fallbacks outside the repo get a neutral placeholder prefix.
        if path is not None:
            try:
                path_out = path.relative_to(REPO).as_posix()
            except ValueError:
                path_out = "<AUTHOR_ARCHIVE>/" + path.name
        else:
            path_out = None
        c = consensus.get(inp["row_id"], {})
        row = {
            "row_id": inp["row_id"],
            "arm": inp["arm"],
            "source_file": sf,
            "case_name": inp["case_name"],
            "period": inp["period"],
            "pro_se": inp["pro_se"],
            "masked_consensus_family": c.get("consensus_family") or None,
            "masked_consensus_type": c.get("consensus_type"),
            "text_path": path_out,
            "text_source": source,
            "text_chars": path.stat().st_size if path else 0,
        }
        rows.append(row)
        if not path:
            misses.append({"row_id": inp["row_id"], "cluster_id": cid})

    per_arm = defaultdict(lambda: [0, 0])
    for r in rows:
        per_arm[r["arm"]][0] += 1
        if r["text_path"]:
            per_arm[r["arm"]][1] += 1
    coverage = {a: {"n": t, "resolved": k, "share": round(k / t, 4)} for a, (t, k) in per_arm.items()}
    gate_pass = all(v["share"] >= 0.95 for v in coverage.values())

    (OUT / "verification_inputs_r2.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")

    # ---- R1 subset
    resolved = [r for r in rows if r["text_path"]]
    a_rows = [r for r in resolved if r["masked_consensus_family"] == "A"]
    nc_rows = [r for r in resolved if r["masked_consensus_family"] is None]
    mf_rows = [r for r in resolved if r["masked_consensus_family"] == "MISFILTER"]
    queue_ids = set()
    with (STUDY / "FINAL_ROW_DECISIONS.csv").open(encoding="utf-8") as f:
        for q in csv.DictReader(f):
            queue_ids.add(f"{q['arm']}|{q['source_file']}")
    queue_bc = [r for r in resolved if r["row_id"] in queue_ids and r["masked_consensus_family"] in {"B", "C"}]
    # 36-row seeded stratified B/C control (arm x family), non-queue
    rng = random.Random(20260708)
    strata = defaultdict(list)
    for r in resolved:
        if r["masked_consensus_family"] in {"B", "C"} and r["row_id"] not in queue_ids:
            strata[(r["arm"], r["masked_consensus_family"])].append(r)
    control = []
    keys = sorted(strata)
    for k in keys:
        rng.shuffle(strata[k])
    i = 0
    while len(control) < 36 and any(strata[k] for k in keys):
        k = keys[i % len(keys)]
        if strata[k]:
            control.append(strata[k].pop())
        i += 1

    r1 = []
    for role, group in [("A_row", a_rows), ("no_consensus", nc_rows), ("misfilter", mf_rows),
                        ("queue_bc", queue_bc), ("control_bc", control)]:
        for r in group:
            rr = dict(r)
            rr["r1_role"] = role
            r1.append(rr)
    # dedupe by row_id, keeping first role assignment
    seen = set()
    r1_final = []
    for r in r1:
        if r["row_id"] not in seen:
            seen.add(r["row_id"])
            r1_final.append(r)
    (OUT / "verification_inputs_r1.json").write_text(json.dumps(r1_final, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")

    report = {
        "coverage_by_arm": coverage,
        "coverage_gate_95_pass": gate_pass,
        "resolution_sources": dict(res_counter),
        "misses": misses,
        "r1_composition": dict(Counter(r["r1_role"] for r in r1_final)),
        "r1_total": len(r1_final),
        "r2_total": len(rows),
    }
    (OUT / "coverage_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
