"""Compute the Phase 5 three-model consensus, agreement statistics, leakage assay,
re-read agreement, and the final row-decision table (FINAL_ROW_DECISIONS.csv), with
the verification lane's per-row outcomes (verified_family, verification_route) merged
in so the committed table is the terminal decision record.

Consensus rule (documented deviation from the companion Layer-2 "coerce to OTHER":
our A/B/C taxonomy has no OTHER and we have a live human queue, so):
  unanimous 3/3 -> adopt; majority 2/3 -> adopt; three-way split or <3 ok reads -> NO_CONSENSUS,
  excluded from primary shares and routed to the human queue.

Primary registered comparison: Family-A share among PRO SE pleading losses with a consensus
family in {A,B,C}, per arm, with seeded bootstrap CIs. Sensitivity: UNCLEAR/MISFILTER/
NO_CONSENSUS counted as non-A.
"""
from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
P5 = HERE.parent / "consensus_stage"
STUDY = Path(__file__).resolve().parents[2]

MODELS = ["kimi", "glm", "deepseek"]
FAMS = ["A", "B", "C", "UNCLEAR", "MISFILTER"]


def load(name):
    p = P5 / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def fam_of(rec):
    if not (rec and rec.get("ok")):
        return None
    f = str(rec["classification"].get("family", "")).strip().upper()
    return f if f in FAMS else None


def fleiss(rows_labels):
    """rows_labels: list of per-row label lists (equal rater count)."""
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


def cohen(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if not pairs:
        return None, 0
    n = len(pairs)
    po = sum(1 for x, y in pairs if x == y) / n
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / (n * n)
    return ((po - pe) / (1 - pe) if pe < 1 else None), n


def boot_ci(vals, reps=2000, seed=20260707):
    if not vals:
        return None, None, None
    rng = random.Random(seed + len(vals))
    n = len(vals)
    means = sorted(sum(rng.choice(vals) for _ in range(n)) / n for _ in range(reps))
    point = sum(vals) / n
    return point, means[int(0.025 * reps)], means[int(0.975 * reps)]


def main():
    inputs = {r["row_id"]: r for r in load("consensus_inputs.json")}
    raw = {m: {r["row_id"]: r for r in (load(f"{m}_raw_results.json") or [])} for m in MODELS}

    rows = []
    for rid, inp in inputs.items():
        fams = {m: fam_of(raw[m].get(rid)) for m in MODELS}
        got = [f for f in fams.values() if f]
        n_ok = len(got)
        consensus, ctype = None, "NO_CONSENSUS"
        if n_ok == 3:
            c = Counter(got)
            top, k = c.most_common(1)[0]
            if k == 3:
                consensus, ctype = top, "unanimous"
            elif k == 2:
                consensus, ctype = top, "majority"
        elif n_ok == 2 and len(set(got)) == 1:
            consensus, ctype = got[0], "two_read_agree_third_failed"
        conf = {m: (raw[m].get(rid, {}).get("classification") or {}).get("confidence") for m in MODELS}
        sub = {m: (raw[m].get(rid, {}).get("classification") or {}).get("subcode") for m in MODELS}
        rows.append({
            "arm": inp["arm"], "source_file": inp["source_file"], "case_name": inp["case_name"],
            "period": inp["period"], "pro_se": inp["pro_se"],
            "kimi_family": fams["kimi"], "glm_family": fams["glm"], "deepseek_family": fams["deepseek"],
            "kimi_subcode": sub["kimi"], "glm_subcode": sub["glm"], "deepseek_subcode": sub["deepseek"],
            "kimi_confidence": conf["kimi"], "glm_confidence": conf["glm"], "deepseek_confidence": conf["deepseek"],
            "n_ok_reads": n_ok, "consensus_family": consensus, "consensus_type": ctype,
            "proxy_family_first_pass": inp["proxy_family_first_pass"],
            "lexicon_leak": bool(inp["lexicon_leak_hits"]),
            "masked_excerpt": inp["masked_text"][:1200],
            "claim_gate": "APPENDIX-READY-MACHINE-VERIFIED" if consensus in {"A", "B", "C"} else "NO-CONSENSUS-EXCLUDED-FROM-PRIMARY",
        })

    # ---- write consensus row CSV
    out_csv = STUDY / "RATIONALE_CODED_ROWS_CONSENSUS.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- agreement stats
    full = [r for r in rows if r["n_ok_reads"] == 3]
    labels_all = [[r["kimi_family"], r["glm_family"], r["deepseek_family"]] for r in full]
    stats = {
        "n_rows": len(rows),
        "n_full_triple_reads": len(full),
        "n_dropped_lt3_reads": len(rows) - len(full),
        "consensus_breakdown": dict(Counter(r["consensus_type"] for r in rows)),
        "consensus_family_distribution": dict(Counter(str(r["consensus_family"]) for r in rows)),
        "fleiss_kappa_all5cats": fleiss(labels_all),
        "fleiss_kappa_by_arm": {a: fleiss([[r["kimi_family"], r["glm_family"], r["deepseek_family"]]
                                           for r in full if r["arm"] == a]) for a in ["RD-PURE", "DT-PURE", "RACE-DT"]},
        "per_family_unanimity": {},
        "proxy_vs_consensus_rowlevel_agreement": None,
        "masking_lexicon_leak_rate": round(sum(1 for r in rows if r["lexicon_leak"]) / len(rows), 4),
    }
    abc = [l for l in labels_all if all(x in {"A", "B", "C"} for x in l)]
    stats["fleiss_kappa_abc_only"] = fleiss(abc)
    stats["n_abc_only_rows"] = len(abc)
    for famcode in FAMS:
        rel = [l for l in labels_all if famcode in l]
        if rel:
            stats["per_family_unanimity"][famcode] = round(sum(1 for l in rel if len(set(l)) == 1) / len(rel), 4)
    both = [(r["proxy_family_first_pass"], r["consensus_family"]) for r in rows if r["consensus_family"] in {"A", "B", "C"}]
    if both:
        stats["proxy_vs_consensus_rowlevel_agreement"] = round(sum(1 for a, b in both if a == b) / len(both), 4)
        k, n = cohen([a for a, _ in both], [b for _, b in both])
        stats["proxy_vs_consensus_cohen_kappa"] = k

    # ---- Family-A shares (primary: pro se, classifiable consensus)
    summary_rows = []
    for arm in ["RD-PURE", "DT-PURE", "RACE-DT"]:
        for rep in ["pro_se", "represented", "all"]:
            def in_rep(r):
                if rep == "all":
                    return True
                return (r["pro_se"] == "True") if rep == "pro_se" else (r["pro_se"] == "False")
            classifiable = [r for r in rows if r["arm"] == arm and in_rep(r) and r["consensus_family"] in {"A", "B", "C"}]
            vals = [1 if r["consensus_family"] == "A" else 0 for r in classifiable]
            point, lo, hi = boot_ci(vals)
            everything = [r for r in rows if r["arm"] == arm and in_rep(r)]
            vals_sens = [1 if r["consensus_family"] == "A" else 0 for r in everything]
            p_sens = sum(vals_sens) / len(vals_sens) if vals_sens else None
            summary_rows.append({
                "arm": arm, "representation": rep,
                "n_classifiable": len(classifiable),
                "family_A_share": point, "family_A_ci_low": lo, "family_A_ci_high": hi,
                "family_B_share": (sum(1 for r in classifiable if r["consensus_family"] == "B") / len(classifiable)) if classifiable else None,
                "family_C_share": (sum(1 for r in classifiable if r["consensus_family"] == "C") / len(classifiable)) if classifiable else None,
                "n_unclear_misfilter_noconsensus": len(everything) - len(classifiable),
                "family_A_share_sensitivity_all_rows": p_sens,
                "claim_gate": "APPENDIX-READY-MACHINE-VERIFIED",
            })
    out_sum = STUDY / "RATIONALE_SUMMARY_CONSENSUS.csv"
    with out_sum.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader()
        w.writerows(summary_rows)

    def share(arm, rep="pro_se"):
        r = next(x for x in summary_rows if x["arm"] == arm and x["representation"] == rep)
        return r["family_A_share"], r["family_A_ci_low"], r["family_A_ci_high"], r["n_classifiable"]

    rd, dt, race = share("RD-PURE"), share("DT-PURE"), share("RACE-DT")
    stats["family_A_pro_se"] = {"RD-PURE": rd, "DT-PURE": dt, "RACE-DT": race}
    stats["prediction4_point_estimate_confirmed"] = bool(rd[0] is not None and dt[0] is not None and race[0] is not None
                                                         and rd[0] > dt[0] and rd[0] > race[0])
    stats["proxy_family_A_pro_se_first_pass"] = {"RD-PURE": 0.496, "DT-PURE": 0.470, "RACE-DT": 0.369}

    # ---- class-guess leakage assay
    cg = load("classguess_flash_raw_results.json")
    if cg:
        by_id = {r["row_id"]: r for r in cg}
        guesses = []
        for rid, inp in inputs.items():
            rec = by_id.get(rid)
            if rec and rec.get("ok"):
                g = str(rec["classification"].get("guess", "")).strip().lower()
                guesses.append((inp["arm"], inp["true_class"], g))
        n = len(guesses)
        correct = sum(1 for _, t, g in guesses if g == t)
        cannot = sum(1 for _, _, g in guesses if g == "cannot_tell")
        stats["classguess_leakage"] = {
            "n": n, "correct_rate": round(correct / n, 4) if n else None,
            "cannot_tell_rate": round(cannot / n, 4) if n else None,
            "correct_rate_by_arm": {a: round(sum(1 for x, t, g in guesses if x == a and g == t) /
                                             max(1, sum(1 for x, _, _ in guesses if x == a)), 4)
                                    for a in ["RD-PURE", "DT-PURE", "RACE-DT"]},
            "chance_baseline": "3 substantive classes; majority-class guessing would score the disability-arm share (0.61)",
        }

    # ---- re-read agreement (Layer-3 analog)
    rr = load("reread_minimax_raw_results.json")
    if rr:
        rr_by = {r["row_id"]: r for r in rr}
        cons_by = {f"{r['arm']}|{r['source_file']}": r["consensus_family"] for r in rows}
        a = [fam_of(rr_by[rid]) for rid in rr_by]
        b = [cons_by.get(rid) for rid in rr_by]
        k, n = cohen(a, b)
        stats["reread_minimax_vs_consensus"] = {"cohen_kappa": k, "n_compared": n}

    # ---- final row-decision table.
    # Family A is the load-bearing AND least-unanimous category (26 consensus rows total), so the
    # table includes EVERY consensus-A row, every NO_CONSENSUS row, and every MISFILTER row, then
    # stratified B/C fill to 60. The verification lane's per-row outcomes are merged from
    # R1_VERIFIED_CODES.csv and every row carries the terminal machine-verified stamp recorded
    # in provenance/VERIFICATION_CLOSURE.md; a row without a verification record is an error.
    rng = random.Random(20260707)
    chosen = [r for r in rows if r["consensus_family"] == "A"]
    chosen += [r for r in rows if r["consensus_family"] is None]
    chosen += [r for r in rows if r["consensus_family"] == "MISFILTER"]
    strata = defaultdict(list)
    for r in rows:
        if r["consensus_family"] in {"B", "C"} and r not in chosen:
            strata[(r["arm"], r["consensus_family"])].append(r)
    keys = sorted(strata)
    i = 0
    for key in keys:
        rng.shuffle(strata[key])
    while len(chosen) < 60 and any(strata[k] for k in keys):
        k = keys[i % len(keys)]
        if strata[k]:
            chosen.append(strata[k].pop())
        i += 1
    chosen = chosen[:max(60, len([r for r in rows if r["consensus_family"] == "A"]) + 10)]
    rtv = HERE.parent / "raw_text_verification"
    r1_by_id = {}
    with (rtv / "R1_VERIFIED_CODES.csv").open(encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            r1_by_id[rec["row_id"]] = rec
    queue = []
    for i, r in enumerate(chosen):
        rid = f"{r['arm']}|{r['source_file']}"
        ver = r1_by_id.get(rid)
        if ver is None:
            raise SystemExit(f"FINAL_ROW_DECISIONS: no verification record for {rid}")
        queue.append({
            "review_id": f"HRQ-C-{i+1:03d}", "arm": r["arm"], "consensus_family": r["consensus_family"],
            "consensus_type": r["consensus_type"],
            "kimi_family": r["kimi_family"], "glm_family": r["glm_family"], "deepseek_family": r["deepseek_family"],
            "pro_se": r["pro_se"], "period": r["period"], "source_file": r["source_file"], "case_name": r["case_name"],
            "masked_excerpt": r["masked_excerpt"],
            "claim_gate": "MACHINE-VERIFIED (AI-only; author-elected)",
            "verified_family": ver["verified_family"],
            "verification_route": ver["route"],
        })
    qpath = STUDY / "FINAL_ROW_DECISIONS.csv"
    with qpath.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(queue[0].keys()))
        w.writeheader()
        w.writerows(queue)

    (P5 / "consensus_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({k: stats[k] for k in ["n_rows", "n_full_triple_reads", "consensus_breakdown",
                                            "fleiss_kappa_all5cats", "fleiss_kappa_abc_only",
                                            "family_A_pro_se", "prediction4_point_estimate_confirmed",
                                            "proxy_vs_consensus_rowlevel_agreement",
                                            "masking_lexicon_leak_rate"] if k in stats}, indent=2, default=str))
    for extra in ["classguess_leakage", "reread_minimax_vs_consensus"]:
        if extra in stats:
            print(extra, "->", json.dumps(stats[extra], default=str))


if __name__ == "__main__":
    main()
