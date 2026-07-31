"""Compute step for the raw-text verification lanes.

Subcommands:
  build-adjudication  - after Lane R1: panel majorities, build adjudication_record.json for rows
                        where the panel disagrees with the masked consensus (or has no majority)
  finalize            - after adjudication + Lane R2: verified codes, error matrix, R2 shares,
                        cross-lane agreement, PRE-COMMITTED trigger evaluation, variant selection

Triggers are pre-committed (SHA256
c95b02de...): (i) verified RD-PURE pro se Family-A >= 8.0% with CI lower bound above both
comparators' CI upper bounds; (ii) R2 RD-PURE >= 2x max(DT, RACE) point estimates;
(iii) <= 20% of B/C control rows flip into A. A+B+C(iii) all pass -> Variant A;
non-inverting failure -> Variant B; ordering inversion in either lane -> Variant C.
"""
from __future__ import annotations

import csv
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTV = HERE.parent / "raw_text_verification"
STUDY = Path(__file__).resolve().parents[2]

R1_MODELS = ["sonnet5", "gpt55", "gemini31pro"]
R2_MODELS = ["kimi", "glm", "deepseek"]
FAMS = {"A", "B", "C", "UNCLEAR", "MISFILTER"}


def load(name):
    p = RTV / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def fam_of(rec, key="family"):
    if not (rec and rec.get("ok")):
        return None
    f = str(rec["classification"].get(key, "")).strip().upper()
    return f if f in FAMS else None


def majority(fams):
    got = [f for f in fams if f]
    if not got:
        return None, "no_reads"
    c = Counter(got).most_common(1)[0]
    if len(got) >= 2 and c[1] >= 2:
        return c[0], ("unanimous" if c[1] == len(got) == 3 else "majority")
    if len(got) == 1:
        return None, "single_read"
    return None, "split"


def boot_ci(vals, reps=2000, seed=20260709):
    if not vals:
        return None, None, None
    rng = random.Random(seed + len(vals))
    n = len(vals)
    means = sorted(sum(rng.choice(vals) for _ in range(n)) / n for _ in range(reps))
    return sum(vals) / n, means[int(0.025 * reps)], means[int(0.975 * reps)]


def fleiss(rows_labels):
    if not rows_labels:
        return None
    cats = sorted({x for row in rows_labels for x in row})
    n, m = len(rows_labels), len(rows_labels[0])
    if m < 2:
        return None
    p_j = {c: sum(row.count(c) for row in rows_labels) / (n * m) for c in cats}
    p_i = [(sum(v * v for v in Counter(row).values()) - m) / (m * (m - 1)) for row in rows_labels]
    pbar = sum(p_i) / n
    pe = sum(v * v for v in p_j.values())
    return (pbar - pe) / (1 - pe) if (1 - pe) else None


def build_adjudication():
    inputs = {r["row_id"]: r for r in load("verification_inputs_r1.json")}
    raw = {m: {r["row_id"]: r for r in (load(f"r1_{m}_raw_results.json") or [])} for m in R1_MODELS}
    queue, agree = [], []
    for rid, inp in inputs.items():
        votes = []
        for m in R1_MODELS:
            rec = raw[m].get(rid)
            f = fam_of(rec)
            if f:
                c = rec["classification"]
                votes.append({"model": rec["model_slug"], "family": f,
                              "subcode": c.get("subcode"), "confidence": c.get("confidence"),
                              "evidence_quote": c.get("evidence_quote"),
                              "quote_verified": rec.get("quote_verified", False)})
        maj, mtype = majority([v["family"] for v in votes])
        masked = inp["masked_consensus_family"]
        row = {"row_id": rid, "arm": inp["arm"], "r1_role": inp["r1_role"], "case_name": inp["case_name"],
               "pro_se": inp["pro_se"], "text_path": inp["text_path"],
               "masked_consensus_family": masked, "panel_majority": maj, "panel_majority_type": mtype,
               "panel_votes": votes}
        if maj is not None and maj == masked:
            agree.append(row)
        else:
            queue.append(row)
    (RTV / "adjudication_record.json").write_text(json.dumps(queue, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    (RTV / "r1_panel_agreements.json").write_text(json.dumps(agree, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"R1 rows: {len(inputs)}; panel==masked: {len(agree)}; to adjudicate: {len(queue)}")
    print("rows to adjudicate by role:", dict(Counter(r["r1_role"] for r in queue)))


def finalize():
    # ---- R1 verified codes
    r1_inputs = {r["row_id"]: r for r in load("verification_inputs_r1.json")}
    agree = {r["row_id"]: r for r in (load("r1_panel_agreements.json") or [])}
    queue = {r["row_id"]: r for r in (load("adjudication_record.json") or [])}
    adj = {r["row_id"]: r for r in (load("adjudication_opus48_raw_results.json") or [])}
    verified = {}
    adjudication_rows = []
    for rid, inp in r1_inputs.items():
        if rid in agree:
            verified[rid] = {"verified_family": agree[rid]["panel_majority"], "route": "panel_agrees_masked"}
        elif rid in queue:
            a = adj.get(rid)
            f = fam_of(a, key="final_family")
            if f:
                verified[rid] = {"verified_family": f, "route": "adjudicated",
                                 "agrees_with": a["classification"].get("agrees_with"),
                                 "adj_quote_verified": a.get("quote_verified", False)}
                adjudication_rows.append(rid)
            else:
                # adjudicator failed: fall back to panel majority if any, else masked code, flagged
                pm = queue[rid]["panel_majority"]
                verified[rid] = {"verified_family": pm or inp["masked_consensus_family"],
                                 "route": "adjudicator_failed_fallback"}
        else:
            verified[rid] = {"verified_family": inp["masked_consensus_family"], "route": "not_audited"}

    # error matrix on the audited roles
    matrix = defaultdict(Counter)
    for rid, v in verified.items():
        inp = r1_inputs[rid]
        matrix[inp["r1_role"]][f"{inp['masked_consensus_family']}->{v['verified_family']}"] += 1
    a_rows = [rid for rid, i in r1_inputs.items() if i["r1_role"] == "A_row"]
    a_sustained = sum(1 for rid in a_rows if verified[rid]["verified_family"] == "A")
    control = [rid for rid, i in r1_inputs.items() if i["r1_role"] == "control_bc"]
    control_flips_to_A = sum(1 for rid in control if verified[rid]["verified_family"] == "A")

    # ---- primary estimator: masked consensus with verified substitutions
    all_rows = load("verification_inputs_r2.json")
    primary = {}
    for arm in ["RD-PURE", "DT-PURE", "RACE-DT"]:
        vals = []
        for r in all_rows:
            if r["arm"] != arm or r["pro_se"] != "True":
                continue
            fam = verified.get(r["row_id"], {}).get("verified_family", r["masked_consensus_family"])
            if fam in {"A", "B", "C"}:
                vals.append(1 if fam == "A" else 0)
        point, lo, hi = boot_ci(vals)
        primary[arm] = {"n": len(vals), "family_A": point, "ci": [lo, hi]}

    # ---- Lane R2 shares
    r2_raw = {m: {r["row_id"]: r for r in (load(f"r2_{m}_raw_results.json") or [])} for m in R2_MODELS}
    r2_codes, labels_full = {}, []
    for r in all_rows:
        fams = [fam_of(r2_raw[m].get(r["row_id"])) for m in R2_MODELS]
        maj, mtype = majority(fams)
        r2_codes[r["row_id"]] = maj
        if all(fams):
            labels_full.append(fams)
    r2 = {}
    for arm in ["RD-PURE", "DT-PURE", "RACE-DT"]:
        vals = [1 if r2_codes[r["row_id"]] == "A" else 0
                for r in all_rows if r["arm"] == arm and r["pro_se"] == "True"
                and r2_codes[r["row_id"]] in {"A", "B", "C"}]
        point, lo, hi = boot_ci(vals)
        r2[arm] = {"n": len(vals), "family_A": point, "ci": [lo, hi]}
    both = [(r["masked_consensus_family"], r2_codes[r["row_id"]]) for r in all_rows
            if r["masked_consensus_family"] in {"A", "B", "C"} and r2_codes[r["row_id"]] in {"A", "B", "C"}]
    crosslane_agree = sum(1 for a, b in both if a == b) / len(both) if both else None
    r2_misfilter = sum(1 for v in r2_codes.values() if v == "MISFILTER")

    # ---- quote integrity stats
    quote_stats = {}
    for lane, models in [("r1", R1_MODELS), ("r2", R2_MODELS)]:
        tot = ver = 0
        for m in models:
            for rec in (load(f"{lane}_{m}_raw_results.json") or []):
                if rec.get("ok"):
                    tot += 1
                    ver += 1 if rec.get("quote_verified") else 0
        quote_stats[lane] = {"ok_reads": tot, "quote_verified": ver, "rate": round(ver / tot, 4) if tot else None}

    # ---- triggers (frozen)
    t1 = (primary["RD-PURE"]["family_A"] is not None and primary["RD-PURE"]["family_A"] >= 0.08
          and primary["RD-PURE"]["ci"][0] is not None
          and primary["RD-PURE"]["ci"][0] > max(primary["DT-PURE"]["ci"][1] or 0, primary["RACE-DT"]["ci"][1] or 0))
    t2 = (r2["RD-PURE"]["family_A"] is not None
          and r2["RD-PURE"]["family_A"] >= 2 * max(r2["DT-PURE"]["family_A"] or 0, r2["RACE-DT"]["family_A"] or 0)
          and (r2["DT-PURE"]["family_A"] is not None and r2["RACE-DT"]["family_A"] is not None))
    t3 = control_flips_to_A <= round(0.20 * len(control))
    inverted = ((primary["RD-PURE"]["family_A"] or 0) <= (primary["DT-PURE"]["family_A"] or 0)
                or (primary["RD-PURE"]["family_A"] or 0) <= (primary["RACE-DT"]["family_A"] or 0)
                or (r2["RD-PURE"]["family_A"] or 0) <= (r2["DT-PURE"]["family_A"] or 0)
                or (r2["RD-PURE"]["family_A"] or 0) <= (r2["RACE-DT"]["family_A"] or 0))
    if inverted:
        variant = "C"
    elif t1 and t2 and t3:
        variant = "A"
    else:
        variant = "B"

    results = {
        "r1": {
            "rows_audited": len(r1_inputs),
            "panel_agrees_masked": sum(1 for v in verified.values() if v["route"] == "panel_agrees_masked"),
            "adjudicated": len(adjudication_rows),
            "adjudicator_failed_fallback": sum(1 for v in verified.values() if v["route"] == "adjudicator_failed_fallback"),
            "A_rows_total": len(a_rows), "A_rows_sustained": a_sustained,
            "A_sustain_rate": round(a_sustained / len(a_rows), 4) if a_rows else None,
            "control_n": len(control), "control_flips_to_A": control_flips_to_A,
            "error_matrix_by_role": {k: dict(v) for k, v in matrix.items()},
        },
        "primary_estimator_verified": primary,
        "r2_raw_text_lane": r2,
        "r2_fleiss_kappa": fleiss(labels_full),
        "r2_full_triple_reads": len(labels_full),
        "crosslane_row_agreement_masked_vs_raw": round(crosslane_agree, 4) if crosslane_agree else None,
        "r2_misfilter_count": r2_misfilter,
        "quote_integrity": quote_stats,
        "triggers": {"t1_verified_rd_ge_8pct_ci_separated": t1,
                     "t2_r2_ordering_2x": t2,
                     "t3_control_stability_le_20pct": t3,
                     "ordering_inverted": inverted},
        "VARIANT_SELECTED": variant,
    }
    (RTV / "VERIFICATION_RESULTS.json").write_text(json.dumps(results, indent=2), encoding="utf-8", newline="\n")

    # verified codes CSV for the record
    with (RTV / "R1_VERIFIED_CODES.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "arm", "r1_role", "pro_se", "masked_consensus_family", "verified_family", "route"])
        for rid, v in verified.items():
            i = r1_inputs[rid]
            w.writerow([rid, i["arm"], i["r1_role"], i["pro_se"], i["masked_consensus_family"],
                        v["verified_family"], v["route"]])
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build-adjudication":
        build_adjudication()
    elif cmd == "finalize":
        finalize()
    else:
        sys.exit("usage: verification_compute.py {build-adjudication|finalize}")
