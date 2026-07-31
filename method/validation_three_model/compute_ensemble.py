#!/usr/bin/env python3
"""Ensemble consensus + agreement analysis for the three-model full-universe run.

Reads per-model raw_results and produces:
 - Ensemble canonical family / bucket for each case (majority vote; OTHER on 3-way split)
 - Agreement vs. original coding (full 676) at family and bucket levels
 - Per-model vs. ensemble agreement (identifies outliers)
 - Full-universe chi-square pro se vs. represented TRANSLATION share under ensemble
 - ensemble_report.md and ensemble_results.json
"""

from __future__ import annotations

import io
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent

RAW_FILES = {
    "kimi": HERE / "kimi_raw_results.json",
    "glm": HERE / "glm_raw_results.json",
    "deepseek": HERE / "deepseek_raw_results.json",
}

REPORT_PATH = HERE / "ensemble_report.md"
RESULTS_PATH = HERE / "ensemble_results.json"

TRANSLATION = "TRANSLATION"
PROCEDURAL_GATEWAY = "PROCEDURAL_GATEWAY"
NO_FAILURE = "NO_FAILURE"
NO_FAILURE_FAMILIES = {"NO_FAILURE_PLAINTIFF_WIN", "NO_FAILURE_DEFENDANT_WIN"}
BUCKETS = [TRANSLATION, PROCEDURAL_GATEWAY, NO_FAILURE, "OTHER"]


def load(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def family_bucket(fam):
    if fam in NO_FAILURE_FAMILIES:
        return NO_FAILURE
    if fam == TRANSLATION:
        return TRANSLATION
    if fam == PROCEDURAL_GATEWAY:
        return PROCEDURAL_GATEWAY
    return "OTHER"


def cohen_kappa(labels_a, labels_b):
    assert len(labels_a) == len(labels_b)
    n = len(labels_a)
    if n == 0:
        return None
    all_labels = sorted(set(labels_a) | set(labels_b))
    idx = {lab: i for i, lab in enumerate(all_labels)}
    k = len(all_labels)
    mat = [[0] * k for _ in range(k)]
    for a, b in zip(labels_a, labels_b):
        mat[idx[a]][idx[b]] += 1
    row_sums = [sum(row) for row in mat]
    col_sums = [sum(mat[r][c] for r in range(k)) for c in range(k)]
    observed = sum(mat[i][i] for i in range(k)) / n
    expected = sum((row_sums[i] * col_sums[i]) / (n * n) for i in range(k))
    if expected >= 1.0:
        return 1.0 if observed >= 1.0 else 0.0
    return round((observed - expected) / (1 - expected), 4)


def fleiss_kappa_three(labels_per_rater):
    """Fleiss' kappa for N items x 3 raters. labels_per_rater is list of tuples of len 3."""
    if not labels_per_rater:
        return None
    categories = sorted({lab for triplet in labels_per_rater for lab in triplet})
    cat_idx = {c: i for i, c in enumerate(categories)}
    N = len(labels_per_rater)
    n_raters = 3
    nij = [[0] * len(categories) for _ in range(N)]
    for i, triplet in enumerate(labels_per_rater):
        for lab in triplet:
            nij[i][cat_idx[lab]] += 1
    # P_i for each subject
    P_i = []
    for i in range(N):
        s = sum(nij[i][j] * (nij[i][j] - 1) for j in range(len(categories)))
        P_i.append(s / (n_raters * (n_raters - 1)))
    P_bar = sum(P_i) / N
    # p_j for each category
    p_j = [sum(nij[i][j] for i in range(N)) / (N * n_raters) for j in range(len(categories))]
    P_e = sum(p * p for p in p_j)
    if 1 - P_e == 0:
        return 1.0 if P_bar >= 1.0 else 0.0
    return round((P_bar - P_e) / (1 - P_e), 4)


def pct(part, whole):
    if not whole:
        return None
    return round(100.0 * part / whole, 2)


def chi_square_2x2(a, b, c, d):
    n = a + b + c + d
    if n == 0:
        return None, None
    row1, row2 = a + b, c + d
    col1, col2 = a + c, b + d
    if row1 == 0 or row2 == 0 or col1 == 0 or col2 == 0:
        return None, None
    expected = [[row1 * col1 / n, row1 * col2 / n], [row2 * col1 / n, row2 * col2 / n]]
    observed = [[a, b], [c, d]]
    chi2 = 0.0
    for i in range(2):
        for j in range(2):
            diff = abs(observed[i][j] - expected[i][j]) - 0.5
            if diff < 0:
                diff = 0
            chi2 += diff * diff / expected[i][j]
    p = math.erfc(math.sqrt(chi2 / 2.0)) if chi2 >= 0 else None
    return round(chi2, 4), p


def two_proportion_diff_ci(a_pos, a_n, b_pos, b_n, z=1.96):
    if a_n == 0 or b_n == 0:
        return None
    p1 = a_pos / a_n
    p2 = b_pos / b_n
    se = math.sqrt(p1 * (1 - p1) / a_n + p2 * (1 - p2) / b_n)
    diff = p1 - p2
    return {
        "diff": round(diff, 4),
        "ci95_low": round(diff - z * se, 4),
        "ci95_high": round(diff + z * se, 4),
        "se": round(se, 4),
    }


def resolve_ensemble(triplet_buckets):
    """Majority vote at bucket level. On 3-way split returns (None, 'split'); on 2-1 returns (winner, 'majority'); 3-0 returns (winner, 'unanimous')."""
    c = Counter(triplet_buckets)
    most = c.most_common()
    if len(most) == 1:
        return most[0][0], "unanimous"
    if most[0][1] == 2:
        return most[0][0], "majority"
    return None, "split"


def main():
    # Load per-model rows keyed by source_file
    by_model = {}
    for model, path in RAW_FILES.items():
        if not path.exists():
            print(f"WARN: missing {path}, skipping model {model}")
            continue
        recs = load(path)
        by_model[model] = {r["source_file"]: r for r in recs}
        print(f"[{model}] {len(recs)} total records, {sum(1 for r in recs if r.get('ok') and r.get('classification'))} ok with classification")

    if not by_model:
        raise SystemExit("No model results found.")

    models_present = list(by_model.keys())
    # Build set of source_files present in ALL models with a valid classification
    sf_sets = []
    for m in models_present:
        sf_sets.append({sf for sf, r in by_model[m].items() if r.get("ok") and r.get("classification")})
    all_sf = set.intersection(*sf_sets) if sf_sets else set()
    union_sf = set.union(*sf_sets) if sf_sets else set()
    print(f"\nUniverse coverage: intersection={len(all_sf)}, union={len(union_sf)}")

    # Build per-case row
    rows = []
    for sf in sorted(all_sf):
        anchor = by_model[models_present[0]][sf]
        per_model_fam = {}
        per_model_mech = {}
        for m in models_present:
            cls = by_model[m][sf]["classification"]
            per_model_fam[m] = cls.get("pleading_failure_family", "UNKNOWN")
            per_model_mech[m] = cls.get("pleading_failure_mechanism", "UNKNOWN")
        per_model_bucket = {m: family_bucket(per_model_fam[m]) for m in models_present}
        triplet_buckets = [per_model_bucket[m] for m in models_present]
        ens_bucket, resolution = resolve_ensemble(triplet_buckets)

        # Atomic family ensemble: majority if one; else None
        fam_counter = Counter(per_model_fam.values())
        fam_most = fam_counter.most_common()
        if fam_most[0][1] >= 2:
            ens_family = fam_most[0][0]
        else:
            ens_family = None

        rows.append({
            "source_file": sf,
            "representation": anchor["representation"],
            "pro_se_bool": anchor.get("pro_se_bool"),
            "year": anchor.get("year"),
            "original_family": anchor["original_family"],
            "original_mechanism": anchor["original_mechanism"],
            "original_model": anchor["original_model"],
            "original_bucket": family_bucket(anchor["original_family"]),
            "per_model_family": per_model_fam,
            "per_model_bucket": per_model_bucket,
            "per_model_mechanism": per_model_mech,
            "ensemble_bucket": ens_bucket,
            "ensemble_family": ens_family,
            "bucket_resolution": resolution,
        })

    n = len(rows)
    print(f"Rows used for agreement (all three models classified): {n}")

    # Ensemble resolution distribution
    res_counts = Counter(r["bucket_resolution"] for r in rows)
    print("Bucket resolution counts:", dict(res_counts))

    # Cases where ensemble couldn't resolve (3-way split): assign ensemble_bucket = "OTHER" for aggregation
    for r in rows:
        if r["ensemble_bucket"] is None:
            r["ensemble_bucket_effective"] = "OTHER"
        else:
            r["ensemble_bucket_effective"] = r["ensemble_bucket"]

    # ---- Agreement metrics: ensemble vs. original
    ens_buckets = [r["ensemble_bucket_effective"] for r in rows]
    orig_buckets = [r["original_bucket"] for r in rows]
    ens_families = [r["ensemble_family"] or "UNRESOLVED" for r in rows]
    orig_families = [r["original_family"] for r in rows]

    bucket_match = sum(1 for a, b in zip(ens_buckets, orig_buckets) if a == b)
    family_match = sum(1 for a, b in zip(ens_families, orig_families) if a == b)
    bucket_kappa = cohen_kappa(ens_buckets, orig_buckets)
    family_kappa = cohen_kappa(ens_families, orig_families)

    # Per-model vs. original (full universe)
    per_model_vs_orig = {}
    for m in models_present:
        m_buckets = [r["per_model_bucket"][m] for r in rows]
        m_fams = [r["per_model_family"][m] for r in rows]
        per_model_vs_orig[m] = {
            "bucket_match_pct": pct(sum(1 for a, b in zip(m_buckets, orig_buckets) if a == b), n),
            "bucket_kappa": cohen_kappa(m_buckets, orig_buckets),
            "family_match_pct": pct(sum(1 for a, b in zip(m_fams, orig_families) if a == b), n),
            "family_kappa": cohen_kappa(m_fams, orig_families),
        }

    # Per-model vs. ensemble (which model is outlier?)
    per_model_vs_ensemble = {}
    for m in models_present:
        m_buckets = [r["per_model_bucket"][m] for r in rows]
        per_model_vs_ensemble[m] = {
            "bucket_match_pct": pct(sum(1 for a, b in zip(m_buckets, ens_buckets) if a == b), n),
            "bucket_kappa": cohen_kappa(m_buckets, ens_buckets),
        }

    # Pairwise model agreement (triangle)
    pairwise = {}
    for i, a in enumerate(models_present):
        for b in models_present[i + 1:]:
            ab = [r["per_model_bucket"][a] for r in rows]
            bb = [r["per_model_bucket"][b] for r in rows]
            key = f"{a}_vs_{b}"
            pairwise[key] = {
                "bucket_match_pct": pct(sum(1 for x, y in zip(ab, bb) if x == y), n),
                "bucket_kappa": cohen_kappa(ab, bb),
            }

    # Fleiss' kappa across the three raters at bucket level
    triplets = [tuple(r["per_model_bucket"][m] for m in models_present) for r in rows]
    fleiss_bucket = fleiss_kappa_three(triplets)
    fam_triplets = [tuple(r["per_model_family"][m] for m in models_present) for r in rows]
    fleiss_family = fleiss_kappa_three(fam_triplets)

    # ---- Full-universe replay: TRANSLATION share by representation (ensemble vs. original)
    def bucket_share(subset, bucket_key):
        if not subset:
            return None
        return sum(1 for r in subset if r[bucket_key] == TRANSLATION), len(subset)

    pro_se = [r for r in rows if r["representation"] == "PRO_SE"]
    repres = [r for r in rows if r["representation"] == "REPRESENTED"]

    orig_ps_t, orig_ps_n = bucket_share(pro_se, "original_bucket")
    orig_rep_t, orig_rep_n = bucket_share(repres, "original_bucket")
    ens_ps_t, ens_ps_n = bucket_share(pro_se, "ensemble_bucket_effective")
    ens_rep_t, ens_rep_n = bucket_share(repres, "ensemble_bucket_effective")

    orig_chi, orig_p = chi_square_2x2(orig_ps_t, orig_ps_n - orig_ps_t, orig_rep_t, orig_rep_n - orig_rep_t)
    ens_chi, ens_p = chi_square_2x2(ens_ps_t, ens_ps_n - ens_ps_t, ens_rep_t, ens_rep_n - ens_rep_t)

    full_replay = {
        "n_pro_se": orig_ps_n,
        "n_represented": orig_rep_n,
        "orig": {
            "pro_se_translation_pct": pct(orig_ps_t, orig_ps_n),
            "represented_translation_pct": pct(orig_rep_t, orig_rep_n),
            "gap_pp": round(pct(orig_ps_t, orig_ps_n) - pct(orig_rep_t, orig_rep_n), 2) if orig_rep_n else None,
            "chi2_1df": orig_chi,
            "p": orig_p,
            "diff_ci": two_proportion_diff_ci(orig_ps_t, orig_ps_n, orig_rep_t, orig_rep_n),
        },
        "ensemble": {
            "pro_se_translation_pct": pct(ens_ps_t, ens_ps_n),
            "represented_translation_pct": pct(ens_rep_t, ens_rep_n),
            "gap_pp": round(pct(ens_ps_t, ens_ps_n) - pct(ens_rep_t, ens_rep_n), 2) if ens_rep_n else None,
            "chi2_1df": ens_chi,
            "p": ens_p,
            "diff_ci": two_proportion_diff_ci(ens_ps_t, ens_ps_n, ens_rep_t, ens_rep_n),
        },
    }

    # Per-model replay (each single model, full universe)
    per_model_replay = {}
    for m in models_present:
        def sub_t(subset):
            return sum(1 for r in subset if r["per_model_bucket"][m] == TRANSLATION)
        mt_ps = sub_t(pro_se)
        mt_rep = sub_t(repres)
        ch, pv = chi_square_2x2(mt_ps, orig_ps_n - mt_ps, mt_rep, orig_rep_n - mt_rep)
        per_model_replay[m] = {
            "pro_se_translation_pct": pct(mt_ps, orig_ps_n),
            "represented_translation_pct": pct(mt_rep, orig_rep_n),
            "gap_pp": round(pct(mt_ps, orig_ps_n) - pct(mt_rep, orig_rep_n), 2) if orig_rep_n else None,
            "chi2_1df": ch,
            "p": pv,
        }

    # PROCEDURAL_GATEWAY replay too
    orig_ps_pg = sum(1 for r in pro_se if r["original_bucket"] == PROCEDURAL_GATEWAY)
    orig_rep_pg = sum(1 for r in repres if r["original_bucket"] == PROCEDURAL_GATEWAY)
    ens_ps_pg = sum(1 for r in pro_se if r["ensemble_bucket_effective"] == PROCEDURAL_GATEWAY)
    ens_rep_pg = sum(1 for r in repres if r["ensemble_bucket_effective"] == PROCEDURAL_GATEWAY)
    ch_pg_orig, p_pg_orig = chi_square_2x2(orig_ps_pg, orig_ps_n - orig_ps_pg, orig_rep_pg, orig_rep_n - orig_rep_pg)
    ch_pg_ens, p_pg_ens = chi_square_2x2(ens_ps_pg, orig_ps_n - ens_ps_pg, ens_rep_pg, orig_rep_n - ens_rep_pg)
    pg_replay = {
        "orig": {
            "pro_se_pct": pct(orig_ps_pg, orig_ps_n),
            "represented_pct": pct(orig_rep_pg, orig_rep_n),
            "gap_pp": round(pct(orig_ps_pg, orig_ps_n) - pct(orig_rep_pg, orig_rep_n), 2),
            "chi2_1df": ch_pg_orig,
            "p": p_pg_orig,
        },
        "ensemble": {
            "pro_se_pct": pct(ens_ps_pg, orig_ps_n),
            "represented_pct": pct(ens_rep_pg, orig_rep_n),
            "gap_pp": round(pct(ens_ps_pg, orig_ps_n) - pct(ens_rep_pg, orig_rep_n), 2),
            "chi2_1df": ch_pg_ens,
            "p": p_pg_ens,
        },
    }

    # Confusion matrix (original vs ensemble)
    confusion = {o: {e: 0 for e in BUCKETS} for o in BUCKETS}
    for r in rows:
        confusion[r["original_bucket"]][r["ensemble_bucket_effective"]] += 1

    # Disagreement list
    disagreements = [
        {
            "source_file": r["source_file"],
            "representation": r["representation"],
            "original_model": r["original_model"],
            "original_family": r["original_family"],
            "per_model_family": r["per_model_family"],
            "ensemble_family": r["ensemble_family"],
            "original_bucket": r["original_bucket"],
            "ensemble_bucket": r["ensemble_bucket_effective"],
            "bucket_resolution": r["bucket_resolution"],
        }
        for r in rows if r["original_bucket"] != r["ensemble_bucket_effective"]
    ]

    results = {
        "n_universe": n,
        "coverage": {
            "intersection_all_three": len(all_sf),
            "union_any": len(union_sf),
            "expected_676": True,
        },
        "bucket_resolution_distribution": dict(res_counts),
        "agreement_ensemble_vs_original": {
            "bucket_match_n": bucket_match,
            "bucket_match_pct": pct(bucket_match, n),
            "bucket_kappa": bucket_kappa,
            "family_match_n": family_match,
            "family_match_pct": pct(family_match, n),
            "family_kappa": family_kappa,
        },
        "fleiss_three_raters": {
            "bucket": fleiss_bucket,
            "family": fleiss_family,
        },
        "per_model_vs_original": per_model_vs_orig,
        "per_model_vs_ensemble": per_model_vs_ensemble,
        "pairwise_models": pairwise,
        "translation_replay_full_universe": full_replay,
        "per_model_translation_replay": per_model_replay,
        "procedural_gateway_replay_full_universe": pg_replay,
        "confusion_original_vs_ensemble": confusion,
        "n_disagreements": len(disagreements),
        "disagreements_sample": disagreements[:50],  # full list in disagreements.json if needed
    }

    with io.open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Write full disagreements separately
    with io.open(HERE / "ensemble_disagreements.json", "w", encoding="utf-8") as f:
        json.dump(disagreements, f, indent=2, ensure_ascii=False)

    # ---- Report
    L = []
    L.append("# Three-model ensemble mechanism validation — report\n")
    L.append(f"Universe size (cases classified by all three models): **{n}**.\n")
    L.append(f"Models: kimi={RAW_FILES['kimi'].name}, glm={RAW_FILES['glm'].name}, deepseek={RAW_FILES['deepseek'].name}.\n")
    L.append(f"Ensemble resolution: unanimous {res_counts.get('unanimous', 0)} / majority {res_counts.get('majority', 0)} / 3-way split {res_counts.get('split', 0)}.\n")
    L.append("")

    L.append("## Headline: ensemble vs. original coding\n")
    a = results["agreement_ensemble_vs_original"]
    L.append("| Metric | Value |")
    L.append("| --- | --- |")
    L.append(f"| Bucket exact match | **{a['bucket_match_pct']}%** ({a['bucket_match_n']}/{n}) |")
    L.append(f"| Bucket kappa | **{a['bucket_kappa']}** |")
    L.append(f"| Atomic family exact match | {a['family_match_pct']}% ({a['family_match_n']}/{n}) |")
    L.append(f"| Atomic family kappa | {a['family_kappa']} |")
    L.append("")

    L.append("## Rater reliability (Fleiss' kappa across the three models)\n")
    f = results["fleiss_three_raters"]
    L.append(f"- Bucket-level Fleiss kappa: **{f['bucket']}**")
    L.append(f"- Atomic family Fleiss kappa: {f['family']}")
    L.append("")
    L.append("Fleiss' kappa aggregates agreement across all three classifiers at once. Higher than 0.60 indicates substantial cross-model agreement independent of any one model.\n")

    L.append("## Each model vs. original (full 676)\n")
    L.append("| Model | n | Bucket match | Bucket kappa | Family match | Family kappa |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for m, v in per_model_vs_orig.items():
        L.append(f"| {RAW_FILES[m].stem.replace('_raw_results','')} ({m}) | {n} | {v['bucket_match_pct']}% | {v['bucket_kappa']} | {v['family_match_pct']}% | {v['family_kappa']} |")
    L.append("")

    L.append("## Each model vs. ensemble consensus\n")
    L.append("| Model | Bucket match with ensemble | Bucket kappa |")
    L.append("| --- | --- | --- |")
    for m, v in per_model_vs_ensemble.items():
        L.append(f"| {m} | {v['bucket_match_pct']}% | {v['bucket_kappa']} |")
    L.append("")
    L.append("A model with meaningfully lower ensemble-agreement than the others is the most likely outlier.\n")

    L.append("## Pairwise cross-model agreement\n")
    L.append("| Pair | Bucket match | Bucket kappa |")
    L.append("| --- | --- | --- |")
    for k, v in pairwise.items():
        L.append(f"| {k} | {v['bucket_match_pct']}% | {v['bucket_kappa']} |")
    L.append("")

    L.append("## TRANSLATION-family gap — full universe replay\n")
    L.append("| Coding | Pro se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | chi2(1df) | p |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    o = full_replay["orig"]
    e = full_replay["ensemble"]
    L.append(f"| Original (Kimi K2.5 + GLM-5.1) | {o['pro_se_translation_pct']}% | {o['represented_translation_pct']}% | {o['gap_pp']} | {o['chi2_1df']} | {o['p']} |")
    L.append(f"| **Ensemble (K2.6 + GLM-5.1 + DeepSeek V3.2 majority)** | **{e['pro_se_translation_pct']}%** | **{e['represented_translation_pct']}%** | **{e['gap_pp']}** | **{e['chi2_1df']}** | **{e['p']}** |")
    for m in models_present:
        pm = per_model_replay[m]
        L.append(f"| {m} solo | {pm['pro_se_translation_pct']}% | {pm['represented_translation_pct']}% | {pm['gap_pp']} | {pm['chi2_1df']} | {pm['p']} |")
    L.append("")
    L.append(f"Pro se sample n = {orig_ps_n}; represented sample n = {orig_rep_n}.")
    L.append(f"Pro-se - represented gap CI (original): {full_replay['orig']['diff_ci']}")
    L.append(f"Pro-se - represented gap CI (ensemble): {full_replay['ensemble']['diff_ci']}")
    L.append("")

    L.append("## PROCEDURAL_GATEWAY family gap — full universe replay\n")
    L.append("| Coding | Pro se PG % | Represented PG % | Gap (pp) | chi2(1df) | p |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    og = pg_replay["orig"]
    eg = pg_replay["ensemble"]
    L.append(f"| Original | {og['pro_se_pct']}% | {og['represented_pct']}% | {og['gap_pp']} | {og['chi2_1df']} | {og['p']} |")
    L.append(f"| Ensemble | {eg['pro_se_pct']}% | {eg['represented_pct']}% | {eg['gap_pp']} | {eg['chi2_1df']} | {eg['p']} |")
    L.append("")

    L.append("## Confusion matrix (original bucket -> ensemble bucket)\n")
    L.append("| orig \\ ens | " + " | ".join(BUCKETS) + " |")
    L.append("| --- |" + " --- |" * len(BUCKETS))
    for orig in BUCKETS:
        row = f"| {orig} | " + " | ".join(str(confusion[orig][e]) for e in BUCKETS) + " |"
        L.append(row)
    L.append("")

    L.append(f"## Disagreements: {len(disagreements)} cases\n")
    L.append("See `ensemble_disagreements.json` for full list. Each row includes per-model family labels, so you can see whether the ensemble flipped against the original because all three models converged or because two-of-three did.\n")

    L.append("## Decision rule status\n")
    bk = a["bucket_kappa"] or 0
    if bk >= 0.60:
        v = "KEEP. Ensemble bucket kappa vs. original >= 0.60. The TRANSLATION claim survives ensemble validation on the full 676-case universe."
    elif bk >= 0.45:
        v = "SOFTEN. Ensemble bucket kappa vs. original in [0.45, 0.60). Keep directional claim but drop precise percentages from main text."
    else:
        v = "PULL. Ensemble bucket kappa vs. original < 0.45 — the original coding diverges materially from ensemble consensus."
    L.append(f"**{v}**\n")

    with io.open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"Report: {REPORT_PATH}")
    print(f"Results: {RESULTS_PATH}")
    print(f"Disagreements: {HERE / 'ensemble_disagreements.json'}")


if __name__ == "__main__":
    main()
