#!/usr/bin/env python3
"""Build 676-case pleading-loss universe, join to representation and case-text
paths, and draw a stratified 150-case validation sample keyed by (pro_se,
family, original_classifier_model). Outputs sample to sample.json."""

from __future__ import annotations

import io
import json
import random
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "FHA_Unified_Database.json"
WAVE_PATH = ROOT / "results" / "unified_overnight_openrouter_disability_wave_r1_final_resolved_results.json"
GAP_PATH = ROOT / "results" / "unified_overnight_openrouter_screened_disability_pleading_loss_gap_final_results.json"
CASE_TEXT_DIRS = [
    ROOT.parent / "allFHAcases",
    ROOT.parent / "allFHAcases" / "recentcases",
    ROOT.parent / "allFHAcases" / "3604",
]
OUT_SAMPLE = Path(__file__).parent / "sample.json"
OUT_UNIVERSE = Path(__file__).parent / "universe.json"

PLEADING_POSTURES = {"MOTION_TO_DISMISS", "SCREENING_ORDER"}
PLEADING_LOSS_OUTCOMES = {"DEFENDANT_WIN", "PROCEDURAL"}
NO_FAILURE_FAMILIES = {"NO_FAILURE_PLAINTIFF_WIN", "NO_FAILURE_DEFENDANT_WIN"}
NO_FAILURE_MECHS = {"CLAIM_SURVIVES_OR_PLAINTIFF_PREVAILS"}

SAMPLE_SEED = 20260420
SAMPLE_TARGET_N = 150


def load_json_utf8(path: Path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def has_disability(record):
    pc = record.get("protected_classes") or []
    if isinstance(pc, str):
        pc = [pc]
    if any("disability" in str(x).lower() for x in pc):
        return True
    return bool(record.get("disability_alleged"))


def is_pleading_loss(record):
    posture = str(record.get("procedural_posture", "")).strip().upper()
    outcome = str(record.get("outcome", "")).strip().upper()
    return posture in PLEADING_POSTURES and outcome in PLEADING_LOSS_OUTCOMES


def is_screened(record):
    sr = str(record.get("screening_result", "")).strip().upper()
    return sr != "" and sr != "NO" and bool(record.get("case_name"))


def representation(record):
    v = record.get("pro_se")
    if v is True:
        return "PRO_SE"
    if v is False:
        return "REPRESENTED"
    return "UNKNOWN"


def find_case_text_path(source_file):
    if not source_file:
        return None
    for d in CASE_TEXT_DIRS:
        p = d / f"{source_file}.txt"
        if p.exists():
            return str(p)
    return None


def build_universe():
    db = load_json_utf8(DB_PATH)
    db_by_source = {}
    for r in db:
        sf = str(r.get("source_file", "")).strip()
        if sf:
            db_by_source[sf] = r

    wave = load_json_utf8(WAVE_PATH)
    gap = load_json_utf8(GAP_PATH)

    classifications = {}
    for row in wave:
        sf = row.get("source_file")
        if not sf:
            continue
        cls = row.get("classification") or {}
        model = None
        trace = row.get("provider_trace") or []
        if trace:
            model = trace[0].get("model")
        classifications[sf] = {
            "classification": cls,
            "original_model": model,
            "classification_source": "DISABILITY_WAVE",
        }
    for row in gap:
        sf = row.get("source_file")
        if not sf:
            continue
        cls = row.get("classification") or {}
        model = None
        trace = row.get("provider_trace") or []
        if trace:
            model = trace[0].get("model")
        # gap takes precedence over wave only if wave was missing
        if sf not in classifications:
            classifications[sf] = {
                "classification": cls,
                "original_model": model,
                "classification_source": "GAP",
            }

    universe = []
    for sf, cls_info in classifications.items():
        rec = db_by_source.get(sf)
        if not rec:
            continue
        if not has_disability(rec):
            continue
        if not is_screened(rec):
            continue
        if not is_pleading_loss(rec):
            continue
        cls = cls_info["classification"]
        family = str(cls.get("pleading_failure_family") or "UNKNOWN").upper()
        mechanism = str(cls.get("pleading_failure_mechanism") or "UNKNOWN").upper()
        universe.append({
            "source_file": sf,
            "case_name": rec.get("case_name"),
            "year": rec.get("year"),
            "date_filed": rec.get("date_filed"),
            "pro_se_bool": rec.get("pro_se"),
            "representation": representation(rec),
            "original_family": family,
            "original_mechanism": mechanism,
            "original_model": cls_info["original_model"],
            "classification_source": cls_info["classification_source"],
            "case_text_path": find_case_text_path(sf),
        })
    return universe


def stratified_sample(universe, n_target, seed):
    random.seed(seed)

    def family_bucket(fam):
        if fam in NO_FAILURE_FAMILIES:
            return "NO_FAILURE"
        if fam == "TRANSLATION":
            return "TRANSLATION"
        if fam == "PROCEDURAL_GATEWAY":
            return "PROCEDURAL_GATEWAY"
        return "OTHER"

    buckets = defaultdict(list)
    for row in universe:
        if row["representation"] == "UNKNOWN":
            continue
        if not row["case_text_path"]:
            continue
        key = (row["representation"], family_bucket(row["original_family"]))
        buckets[key].append(row)

    # Target allocation
    targets = {
        ("PRO_SE", "TRANSLATION"): 40,
        ("PRO_SE", "PROCEDURAL_GATEWAY"): 25,
        ("PRO_SE", "OTHER"): 15,
        ("PRO_SE", "NO_FAILURE"): 10,
        ("REPRESENTED", "TRANSLATION"): 25,
        ("REPRESENTED", "PROCEDURAL_GATEWAY"): 20,
        ("REPRESENTED", "OTHER"): 10,
        ("REPRESENTED", "NO_FAILURE"): 5,
    }
    assert sum(targets.values()) == n_target, f"targets sum = {sum(targets.values())}"

    chosen = []
    notes = []
    for key, target in targets.items():
        pool = buckets.get(key, [])
        take = min(target, len(pool))
        notes.append(f"{key}: pool={len(pool)}, target={target}, taken={take}")
        if pool and take > 0:
            picks = random.sample(pool, take)
            for p in picks:
                p = dict(p)
                p["strata_key"] = f"{key[0]}|{key[1]}"
                chosen.append(p)

    # Backfill from pro_se_translation / pro_se_procedural pools if short
    short = n_target - len(chosen)
    if short > 0:
        # Backfill order: pro_se TRANSLATION, pro_se PROCEDURAL, pro_se OTHER
        taken_sources = {c["source_file"] for c in chosen}
        fill_order = [
            ("PRO_SE", "TRANSLATION"),
            ("PRO_SE", "PROCEDURAL_GATEWAY"),
            ("PRO_SE", "OTHER"),
        ]
        for key in fill_order:
            if short <= 0:
                break
            pool = [r for r in buckets.get(key, []) if r["source_file"] not in taken_sources]
            take = min(short, len(pool))
            if take > 0:
                picks = random.sample(pool, take)
                for p in picks:
                    p = dict(p)
                    p["strata_key"] = f"{key[0]}|{key[1]}_BACKFILL"
                    chosen.append(p)
                    taken_sources.add(p["source_file"])
                short -= take
                notes.append(f"BACKFILL {key}: added {take}")

    return chosen, notes


def main():
    universe = build_universe()
    print(f"Universe size (pleading-loss disability): {len(universe)}")
    rep_counts = Counter(r["representation"] for r in universe)
    fam_counts = Counter(r["original_family"] for r in universe)
    model_counts = Counter(r["original_model"] for r in universe)
    text_paths_found = sum(1 for r in universe if r["case_text_path"])
    print(f"Case-text paths found: {text_paths_found}/{len(universe)}")
    print(f"Representation counts: {dict(rep_counts)}")
    print(f"Family counts: {dict(fam_counts)}")
    print(f"Original-model counts: {dict(model_counts)}")

    with io.open(OUT_UNIVERSE, "w", encoding="utf-8") as f:
        json.dump(universe, f, indent=2, ensure_ascii=False)
    print(f"Wrote universe to {OUT_UNIVERSE}")

    sample, notes = stratified_sample(universe, SAMPLE_TARGET_N, SAMPLE_SEED)
    print(f"Sample size: {len(sample)}")
    for n in notes:
        print(f"  {n}")

    with io.open(OUT_SAMPLE, "w", encoding="utf-8") as f:
        json.dump({
            "seed": SAMPLE_SEED,
            "target_n": SAMPLE_TARGET_N,
            "actual_n": len(sample),
            "allocation_notes": notes,
            "cases": sample,
        }, f, indent=2, ensure_ascii=False)
    print(f"Wrote sample to {OUT_SAMPLE}")


if __name__ == "__main__":
    main()
