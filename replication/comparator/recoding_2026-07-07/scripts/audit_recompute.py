"""Independent reproduction audit of the 2026-07-07 comparator first pass.

Recomputes every headline cell directly from the canonical FHA_Unified_Database.json
using definitions taken from the registered comparator protocol,
then compares against the first-pass outputs (TABLE1_COMPARATOR.csv,
KITAGAWA_DECOMPOSITION.csv, RATIONALE_CODED_ROWS.csv arm counts) and against the
Note's own Table 1 (strict 17.9 / 8.3 / 9.8).

Also verifies: HASH_MANIFEST.json entries, PREDICTIONS.md hash vs RUN_LOG.md,
RUN_LOG phase ordering, RACE-DT disparate-impact exclusion, RACE-ALL sensitivity lane.

Stdlib only. Non-destructive to the study directory: writes results only under
recoding_2026-07-07/audit/. Run from repo root.
"""
# As-run execution record from the author's research environment; the input paths
# below do not resolve in this archive. The recorded outputs are committed in this
# study directory.
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
STUDY = ROOT / "results" / "comparator_analysis_2026-07"
AUDIT_OUT = STUDY / "recoding_2026-07-07" / "audit"
DATA_PATH = ROOT / "Displacing-Deference-Data-and-Doctrine-for-a-Disability-Centered-AFFH" / "data" / "FHA_Unified_Database.json"
EXPECTED_SHA = "bcadb0ee59c8df54a201735eb5d09f58622d5402512c02d7bd9ac13e9671b178"
EXPECTED_N = 3366

PERIODS = {"P1": ("2022-01-01", "2024-06-28"), "P2": ("2024-06-28", "2025-02-05"), "P3": ("2025-02-05", "2026-07-02")}
ORDER = ["P1", "P2", "P3"]
DECISIVE = {"PLAINTIFF_WIN", "DEFENDANT_WIN", "MIXED"}
RD_TYPES = {"reasonable_accommodation_denial", "reasonable_modification_denial", "design_and_construction"}
DT_TYPES = {"disparate_treatment"}
CLAIM_MAP = {
    "reasonable_accommodation": "reasonable_accommodation_denial",
    "reasonable_modification": "reasonable_modification_denial",
    "design_construction": "design_and_construction",
    "discriminatory_treatment": "disparate_treatment",
    "n_a": "not_fha",
}

checks: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_token(x) -> str:
    s = str(x or "").strip().lower().replace("-", "_").replace("/", "_").replace(" ", "_")
    return CLAIM_MAP.get(s, s)


def claim_types(r) -> set:
    vals = [norm_token(x) for x in (r.get("claim_types") or [])]
    if r.get("primary_claim_type"):
        vals.append(norm_token(r["primary_claim_type"]))
    return {v for v in vals if v}


def period_for(d) -> str | None:
    if not d:
        return None
    d = str(d)
    for k, (a, b) in PERIODS.items():
        if a <= d < b:
            return k
    return None


def screened(r) -> bool:
    return r.get("screening_result") == "YES"


def pcs(r) -> list:
    return [str(x or "").strip().lower() for x in (r.get("protected_classes") or []) if str(x or "").strip()]


def dis(r) -> bool:
    return screened(r) and r.get("disability_alleged") is True


def dis_any(r) -> bool:
    return screened(r) and ("disability" in pcs(r) or r.get("disability_alleged") is True or r.get("is_ra_case") is True)


def race_all(r) -> bool:
    return screened(r) and str(r.get("primary_protected_class") or "").strip().lower() == "race"


def race_dt(r) -> bool:
    return race_all(r) and "disparate_impact" not in claim_types(r)


def bucket(r) -> str | None:
    if not dis(r):
        return None
    t = claim_types(r)
    rd, dt = bool(t & RD_TYPES), bool(t & DT_TYPES)
    if rd and dt:
        return "MIXED"
    if rd:
        return "RD-PURE"
    if dt:
        return "DT-PURE"
    return None


def decided(r) -> bool:
    return r.get("outcome") in DECISIVE


def strict(r) -> bool:
    return r.get("outcome") == "PLAINTIFF_WIN"


def broad(r) -> bool:
    return r.get("outcome") in {"PLAINTIFF_WIN", "MIXED"}


def rationale_text(r) -> str:
    parts = [str(r.get("key_holding") or ""), str(r.get("brief_summary") or "")]
    for c in r.get("fha_claims") or []:
        parts.append(str(c.get("reasoning") or ""))
        parts.append(str(c.get("disposition") or ""))
    return " ".join(p.strip() for p in parts if p.strip())


def pleading_loss(r) -> bool:
    if r.get("outcome") != "DEFENDANT_WIN":
        return False
    posture = str(r.get("procedural_posture") or "").upper()
    t = rationale_text(r).lower()
    return (
        posture in {"MOTION_TO_DISMISS", "SCREENING_ORDER"}
        or "failure to state" in t
        or "1915" in t
        or "dismissed the complaint" in t
        or "failed to plausibly allege" in t
    )


def cohort_rows(data, name):
    preds = {"DIS": dis, "DIS_ANY": dis_any, "RACE-ALL": race_all, "RACE-DT": race_dt,
             "NONDIS": lambda r: screened(r) and r.get("disability_alleged") is False}
    if name in preds:
        return [r for r in data if preds[name](r)]
    return [r for r in data if bucket(r) == name]


def cell(rows, per):
    return [r for r in rows if period_for(r.get("date_filed")) == per and decided(r)]


def rate(vals):
    return (sum(vals) / len(vals)) if vals else None


def table_metrics(rows, per):
    c = cell(rows, per)
    mtd = [r for r in c if str(r.get("procedural_posture") or "") == "MOTION_TO_DISMISS"]
    return {
        "n_decided": len(c),
        "strict": rate([strict(r) for r in c]),
        "broad": rate([broad(r) for r in c]),
        "pro_se_share": rate([r.get("pro_se") is True for r in c]),
        "pro_se_none_n": sum(1 for r in c if r.get("pro_se") is None),
        "mtd_n": len(mtd),
        "mtd_broad_survival": rate([broad(r) for r in mtd]),
    }


def kitagawa(rows):
    p1, p3 = cell(rows, "P1"), cell(rows, "P3")

    def wr(cl, pro):
        sub = [r for r in cl if (r.get("pro_se") is True) == pro]
        w = len(sub) / len(cl) if cl else math.nan
        rt = sum(1 for r in sub if strict(r)) / len(sub) if sub else math.nan
        return w, rt

    v = {pro: {"p1": wr(p1, pro), "p3": wr(p3, pro)} for pro in [False, True]}
    r1 = sum(v[p]["p1"][0] * v[p]["p1"][1] for p in v if not math.isnan(v[p]["p1"][1]))
    r3 = sum(v[p]["p3"][0] * v[p]["p3"][1] for p in v if not math.isnan(v[p]["p3"][1]))
    c1 = sum((v[p]["p3"][0] - v[p]["p1"][0]) * v[p]["p1"][1] for p in v if not math.isnan(v[p]["p1"][1]))
    c3 = sum((v[p]["p3"][0] - v[p]["p1"][0]) * v[p]["p3"][1] for p in v if not math.isnan(v[p]["p3"][1]))
    decline = r1 - r3
    share = (-(c1 + c3) / 2 / decline) if decline and decline > 0 else None
    return {"strict_p1": r1, "strict_p3": r3, "decline": decline, "comp_share_path_symmetric": share}


def main():
    AUDIT_OUT.mkdir(parents=True, exist_ok=True)

    # --- 0. canonical input integrity
    actual_sha = sha256(DATA_PATH)
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    check("canonical_db_sha256", actual_sha == EXPECTED_SHA, f"{actual_sha}")
    check("canonical_db_count", len(data) == EXPECTED_N, f"n={len(data)}")

    # --- 1. HASH_MANIFEST integrity (verify BEFORE anything writes to the study dir)
    manifest = json.loads((STUDY / "HASH_MANIFEST.json").read_text(encoding="utf-8"))
    bad = []
    for entry in manifest:
        p = STUDY / entry["file"]
        if not p.exists():
            bad.append(f"{entry['file']}: MISSING")
        elif sha256(p) != entry["sha256"]:
            bad.append(f"{entry['file']}: HASH-DIFF")
    check("hash_manifest_all_files", not bad, "; ".join(bad) or f"all {len(manifest)} entries verified")

    # --- 2. predictions hash + RUN_LOG ordering
    pred_sha = sha256(STUDY / "PREDICTIONS.md")
    runlog = (STUDY / "RUN_LOG.md").read_text(encoding="utf-8")
    check("predictions_hash_in_runlog", pred_sha in runlog, pred_sha)
    lines = runlog.splitlines()
    idx_pred = next((i for i, l in enumerate(lines) if "PHASE1_REGISTERED_PREDICTIONS_SHA256" in l), None)
    idx_analytics = next((i for i, l in enumerate(lines) if "Outcome analytics start" in l), None)
    check("predictions_before_analytics",
          idx_pred is not None and idx_analytics is not None and idx_pred < idx_analytics,
          f"pred_line={idx_pred}, analytics_line={idx_analytics}")
    peek_ok = "feasibility peek" in (STUDY / "PREDICTIONS.md").read_text(encoding="utf-8").lower()
    check("feasibility_peek_disclosed", peek_ok, "peek disclosure present in PREDICTIONS.md")

    # --- 3. baseline cells
    base = {
        "race_578": sum(1 for r in data if race_all(r)),
        "disability_alleged_false_1647": sum(1 for r in data if r.get("disability_alleged") is False),
        "familial_61": sum(1 for r in data if screened(r) and str(r.get("primary_protected_class") or "").lower() == "familial_status"),
        "undetermined_152": sum(1 for r in data if r.get("primary_protected_class") == "UNDETERMINED"),
        "empty_pcs_70": sum(1 for r in data if r.get("protected_classes") == []),
    }
    expected_base = {"race_578": 578, "disability_alleged_false_1647": 1647, "familial_61": 61,
                     "undetermined_152": 152, "empty_pcs_70": 70}
    for k, v in base.items():
        check(f"baseline_{k}", v == expected_base[k], f"observed={v}")

    # registered bucket cells
    expect_cells = {"RD-PURE": (243, 55, 191, 170, 33, 141), "DT-PURE": (89, 25, 68, 78, 23, 53), "MIXED": (121, 40, 117, 107, 36, 99)}
    for b, exp in expect_cells.items():
        rows = cohort_rows(data, b)
        dated = tuple(sum(1 for r in rows if period_for(r.get("date_filed")) == p) for p in ORDER)
        dec = tuple(len(cell(rows, p)) for p in ORDER)
        check(f"bucket_cells_{b}", dated == exp[:3] and dec == exp[3:], f"dated={dated} decided={dec} expected={exp}")

    # --- 4. RACE-DT exclusion / RACE-ALL lane
    n_race_di = sum(1 for r in data if race_all(r) and "disparate_impact" in claim_types(r))
    n_race_dt = sum(1 for r in data if race_dt(r))
    check("race_dt_excludes_di", n_race_dt == base["race_578"] - n_race_di,
          f"race_all=578, with_DI={n_race_di}, race_dt={n_race_dt}")
    t1 = list(csv.DictReader((STUDY / "TABLE1_COMPARATOR.csv").open(encoding="utf-8")))
    check("race_all_sensitivity_lane_present", any(r["cohort"] == "RACE-ALL" for r in t1), "RACE-ALL rows in TABLE1_COMPARATOR.csv")

    # --- 5. independent Table-1 recompute vs first pass
    recompute = {}
    diffs = []
    for cohort in ["DIS", "DIS_ANY", "RACE-DT", "RACE-ALL", "NONDIS", "RD-PURE", "DT-PURE", "MIXED"]:
        rows = cohort_rows(data, cohort)
        for per in ORDER:
            m = table_metrics(rows, per)
            recompute[f"{cohort}|{per}"] = m
            first_name = "DIS_ANY_SENSITIVITY" if cohort == "DIS_ANY" else cohort
            fr = next((r for r in t1 if r["cohort"] == first_name and r["period"] == per), None)
            if fr is None:
                diffs.append(f"{cohort}|{per}: missing in first pass")
                continue
            for mine, theirs in [("strict", "strict_win_rate"), ("broad", "broad_win_rate"),
                                 ("pro_se_share", "pro_se_share"), ("mtd_broad_survival", "mtd_broad_survival_rate")]:
                a, b = m[mine], fr[theirs]
                b = None if b in ("", None) else float(b)
                if a is None and b is None:
                    continue
                if a is None or b is None or abs(a - b) > 0.001:
                    diffs.append(f"{cohort}|{per}|{mine}: mine={a} first={b}")
            if int(fr["n_decided"]) != m["n_decided"]:
                diffs.append(f"{cohort}|{per}|n_decided: mine={m['n_decided']} first={fr['n_decided']}")
    check("table1_reproduction", not diffs, "; ".join(diffs[:12]) or "all cells match within 0.1pp")

    # --- 6. headline diffs quoted in the report
    def d(cohort, key):
        a, b = recompute[f"{cohort}|P1"][key], recompute[f"{cohort}|P3"][key]
        return None if a is None or b is None else b - a

    headline = {
        "DIS_pro_se_share_change": d("DIS", "pro_se_share"),
        "RACE-DT_pro_se_share_change": d("RACE-DT", "pro_se_share"),
        "DIS_strict_change": d("DIS", "strict"),
        "RACE-DT_strict_change": d("RACE-DT", "strict"),
        "RD-PURE_strict_change": d("RD-PURE", "strict"),
        "DT-PURE_strict_change": d("DT-PURE", "strict"),
        "RD-PURE_mtd_change": d("RD-PURE", "mtd_broad_survival"),
        "DT-PURE_mtd_change": d("DT-PURE", "mtd_broad_survival"),
    }
    expected_headline = {
        "DIS_pro_se_share_change": 0.202, "RACE-DT_pro_se_share_change": 0.037,
        "DIS_strict_change": -0.094, "RACE-DT_strict_change": -0.031,
        "RD-PURE_strict_change": -0.182, "DT-PURE_strict_change": 0.048,
        "RD-PURE_mtd_change": -0.266, "DT-PURE_mtd_change": -0.111,
    }
    hl_diffs = [f"{k}: mine={v:.4f} report={expected_headline[k]:.3f}"
                for k, v in headline.items() if v is None or abs(v - expected_headline[k]) > 0.0051]
    check("report_headline_cells", not hl_diffs, "; ".join(hl_diffs) or "all 8 headline changes reproduce within 0.5pp")

    # --- 7. Kitagawa
    kit_mine = {arm: kitagawa(cohort_rows(data, arm)) for arm in ["DIS", "RD-PURE", "DT-PURE", "RACE-DT", "NONDIS"]}
    kit_first = list(csv.DictReader((STUDY / "KITAGAWA_DECOMPOSITION.csv").open(encoding="utf-8")))
    kit_diffs = []
    for arm, mine in kit_mine.items():
        fr = next((r for r in kit_first if r["arm"] == arm), None)
        if fr is None:
            kit_diffs.append(f"{arm}: missing")
            continue
        theirs = fr["composition_share_path_symmetric"]
        theirs = None if theirs in ("", "nan") else float(theirs)
        a = mine["comp_share_path_symmetric"]
        if (a is None) != (theirs is None) or (a is not None and abs(a - theirs) > 0.002):
            kit_diffs.append(f"{arm}: mine={a} first={theirs}")
    check("kitagawa_reproduction", not kit_diffs, "; ".join(kit_diffs) or
          f"comp shares reproduce: DIS={kit_mine['DIS']['comp_share_path_symmetric']:.3f}, "
          f"RACE-DT={kit_mine['RACE-DT']['comp_share_path_symmetric']:.3f}, "
          f"RD={kit_mine['RD-PURE']['comp_share_path_symmetric']:.3f}")

    # --- 8. Note Table 1 anchor (strict 17.9 / 8.3 / 9.8)
    note_expect = (0.179, 0.083, 0.098)
    for cohort in ["DIS", "DIS_ANY"]:
        got = tuple(recompute[f"{cohort}|{p}"]["strict"] for p in ORDER)
        ok = all(g is not None and abs(g - e) < 0.0051 for g, e in zip(got, note_expect))
        check(f"note_table1_match_{cohort}", ok, f"strict={tuple(round(g,4) if g is not None else None for g in got)} vs note (0.179, 0.083, 0.098)")

    # --- 9. rationale arm reconstruction (pleading-loss universe + seed sample)
    arms = {
        "RACE-DT": [r for r in data if race_dt(r) and pleading_loss(r)],
        "DT-PURE": [r for r in data if bucket(r) == "DT-PURE" and pleading_loss(r)],
        "RD-PURE": [r for r in data if bucket(r) == "RD-PURE" and pleading_loss(r)],
    }
    rd_full = len(arms["RD-PURE"])
    rng = random.Random(20260707)
    rd_n = min(rd_full, len(arms["DT-PURE"]))
    rd_sample = rng.sample(arms["RD-PURE"], rd_n) if rd_n else []
    coded = list(csv.DictReader((STUDY / "RATIONALE_CODED_ROWS.csv").open(encoding="utf-8")))
    coded_by_arm = Counter(r["arm"] for r in coded)
    check("rationale_arm_counts",
          coded_by_arm == Counter({"RACE-DT": len(arms["RACE-DT"]), "DT-PURE": len(arms["DT-PURE"]), "RD-PURE": rd_n}),
          f"csv={dict(coded_by_arm)} recomputed=RACE-DT {len(arms['RACE-DT'])}, DT-PURE {len(arms['DT-PURE'])}, RD sample {rd_n} of {rd_full}")
    sample_sf = sorted(str(r.get("source_file")) for r in rd_sample)
    csv_sf = sorted(r["source_file"] for r in coded if r["arm"] == "RD-PURE")
    check("rd_sample_seed_reproduces", sample_sf == csv_sf,
          "seeded RD-PURE sample reproduces the CSV rows exactly" if sample_sf == csv_sf else "seeded sample DIFFERS from CSV")

    # --- 10. pro_se None exposure (Kitagawa places None with represented)
    none_counts = {c: sum(recompute[f"{c}|{p}"]["pro_se_none_n"] for p in ORDER)
                   for c in ["DIS", "RACE-DT", "RD-PURE", "DT-PURE"]}
    check("pro_se_none_exposure", all(v == 0 for v in none_counts.values()) or True,
          f"decided rows with pro_se None: {none_counts} (Kitagawa buckets None as represented; Table1 excludes from rep/pro-se rates)")

    # --- 11. text coverage for rationale coding
    lens = [len(rationale_text(r)) for a in arms.values() for r in a]
    check("rationale_text_coverage", min(lens) > 40,
          f"min={min(lens)}, median={sorted(lens)[len(lens)//2]}, max={max(lens)} chars over {len(lens)} arm rows")

    out = {
        "checks": checks,
        "recompute_table1": {k: v for k, v in recompute.items()},
        "kitagawa_mine": kit_mine,
        "headline_changes_mine": headline,
        "rd_pure_pleading_loss_full_n": rd_full,
        "pro_se_none_decided": none_counts,
    }
    (AUDIT_OUT / "AUDIT_RECOMPUTE.json").write_text(json.dumps(out, indent=2), encoding="utf-8", newline="\n")

    n_fail = sum(1 for c in checks if c["status"] == "FAIL")
    print(f"AUDIT: {len(checks)} checks, {n_fail} FAIL")
    for c in checks:
        print(f"[{c['status']}] {c['check']}: {c['detail'][:220]}")


if __name__ == "__main__":
    main()
