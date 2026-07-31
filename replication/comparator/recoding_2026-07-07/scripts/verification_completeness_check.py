"""Completeness gate for the raw-text verification lanes (author requirement 2026-07-07):
verify the verification data itself is COMPLETE before any trigger evaluation runs.

Checks (hard gate = every check must PASS or carry an explicit documented exception):
  1. Input integrity: R1 has 96 rows in the designed role mix; R2 has 476; all text paths exist.
  2. Read coverage: every row x model pair has a successful read, or the drop is counted and
     below tolerance (>= 97% reads ok per model; >= 99% rows with >= 2 ok reads per lane).
  3. Schema integrity: every ok read carries a valid family and a non-empty evidence quote.
  4. Quote integrity: per-model verbatim-match rates reported; overall >= 60% (quotes that fail
     matching are retained but flagged; the rate is a disclosure item, not a validity filter).
  5. Adjudication closure: every row routed for adjudication has an ok adjudicator ruling (or is
     explicitly listed as fallback).
  6. Determinism inputs: prompts on disk hash-match the verification_stage_manifest.json registration.
  7. Raw-file manifest: SHA256 for every lane artifact, written to VERIFICATION_MANIFEST.json.
Output: COMPLETENESS_CHECK.json + console PASS/FAIL lines. Exit code 1 on any hard failure.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTV = HERE.parent / "raw_text_verification"
STUDY = Path(__file__).resolve().parents[2]

R1_MODELS = ["sonnet5", "gpt55", "gemini31pro"]
R2_MODELS = ["kimi", "glm", "deepseek"]
FAMS = {"A", "B", "C", "UNCLEAR", "MISFILTER"}

checks = []


def check(name, ok, detail, hard=True):
    checks.append({"check": name, "status": "PASS" if ok else ("FAIL" if hard else "WARN"), "detail": detail})
    return ok


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def load(name):
    p = RTV / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def lane_checks(lane, models, inputs):
    ids = {r["row_id"] for r in inputs}
    ok_by_row = Counter()
    hard_ok = True
    for m in models:
        recs = load(f"{lane}_{m}_raw_results.json") or []
        by_id = {r["row_id"]: r for r in recs}
        ok_recs = [r for r in recs if r.get("ok")]
        missing = ids - set(by_id)
        bad_schema = [r for r in ok_recs
                      if str((r.get("classification") or {}).get("family", "")).strip().upper() not in FAMS
                      or not str((r.get("classification") or {}).get("evidence_quote", "")).strip()]
        qv = sum(1 for r in ok_recs if r.get("quote_verified"))
        rate_ok = len(ok_recs) / len(ids) if ids else 0
        hard_ok &= check(f"{lane}_{m}_read_coverage", rate_ok >= 0.97 and not missing,
                         f"{len(ok_recs)}/{len(ids)} ok ({rate_ok:.1%}); missing_rows={len(missing)}")
        hard_ok &= check(f"{lane}_{m}_schema", not bad_schema, f"{len(bad_schema)} invalid ok-reads")
        check(f"{lane}_{m}_quote_match_rate", qv / max(1, len(ok_recs)) >= 0.60,
              f"{qv}/{len(ok_recs)} verbatim-verified ({qv / max(1, len(ok_recs)):.1%})", hard=False)
        for r in ok_recs:
            ok_by_row[r["row_id"]] += 1
    two_plus = sum(1 for rid in ids if ok_by_row[rid] >= 2)
    hard_ok &= check(f"{lane}_rows_with_2plus_reads", two_plus / len(ids) >= 0.99,
                     f"{two_plus}/{len(ids)} rows have >=2 ok reads")
    return hard_ok


def main():
    hard_ok = True

    r1 = load("verification_inputs_r1.json") or []
    r2 = load("verification_inputs_r2.json") or []
    roles = Counter(r["r1_role"] for r in r1)
    hard_ok &= check("r1_input_composition",
                     roles == Counter({"control_bc": 36, "A_row": 26, "queue_bc": 24, "no_consensus": 6, "misfilter": 4}),
                     f"{dict(roles)}")
    hard_ok &= check("r2_input_count", len(r2) == 476, f"{len(r2)} rows")
    missing_text = [r["row_id"] for r in r2 if not r.get("text_path") or not Path(r["text_path"]).exists()]
    hard_ok &= check("text_paths_exist", not missing_text, f"{len(missing_text)} missing")

    hard_ok &= lane_checks("r1", R1_MODELS, r1)
    hard_ok &= lane_checks("r2", R2_MODELS, r2)

    queue = load("adjudication_record.json") or []
    adj = {r["row_id"]: r for r in (load("adjudication_opus48_raw_results.json") or [])}
    unresolved = [r["row_id"] for r in queue if not (adj.get(r["row_id"], {}).get("ok"))]
    hard_ok &= check("adjudication_closure", not unresolved,
                     f"{len(queue) - len(unresolved)}/{len(queue)} adjudicated; unresolved={unresolved[:5]}")

    stage = json.loads((STUDY / "provenance" / "verification_stage_manifest.json").read_text(encoding="utf-8"))
    fl = stage["files"]
    entries = fl.items() if isinstance(fl, dict) else ((e["file"], e["sha256"]) for e in fl)
    registered = {str(k).split("/")[-1]: v for k, v in entries}
    for name in ["verification_recode_prompt.txt", "verification_adjudicator_prompt.txt"]:
        h = sha(RTV / name)
        hard_ok &= check(f"prompt_hash_registered_{name}", registered.get(name) == h, h[:16])

    manifest = []
    for p in sorted(RTV.glob("*")):
        if p.is_file():
            manifest.append({"file": p.name, "sha256": sha(p), "bytes": p.stat().st_size})
    (RTV / "VERIFICATION_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    check("manifest_written", True, f"{len(manifest)} files hashed")

    (RTV / "COMPLETENESS_CHECK.json").write_text(json.dumps(checks, indent=2), encoding="utf-8", newline="\n")
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")
    for c in checks:
        print(f"[{c['status']}] {c['check']}: {c['detail'][:180]}")
    print(f"COMPLETENESS: {len(checks)} checks, {n_fail} FAIL")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()
