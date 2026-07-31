#!/usr/bin/env python3
"""Compute agreement metrics between original mechanism classifier and Kimi K2.6
validator. Writes agreement_report.md and agreement_results.json."""

from __future__ import annotations

import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
RAW_PATH = HERE / "kimi_k2_6_raw_results.json"
REPORT_PATH = HERE / "agreement_report.md"
RESULTS_PATH = HERE / "agreement_results.json"

TRANSLATION = "TRANSLATION"
PROCEDURAL_GATEWAY = "PROCEDURAL_GATEWAY"
NO_FAILURE = "NO_FAILURE"
NO_FAILURE_FAMILIES = {"NO_FAILURE_PLAINTIFF_WIN", "NO_FAILURE_DEFENDANT_WIN"}


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
    """Compute Cohen's kappa for two label sequences."""
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


def pct(part, whole):
    if not whole:
        return None
    return round(100.0 * part / whole, 2)


def chi_square_2x2(a, b, c, d):
    """2x2 chi-square with continuity correction; returns chi2 and p (via survival approx)."""
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
    # Survival of chi-square with 1 df: p = erfc(sqrt(chi2/2))
    p = math.erfc(math.sqrt(chi2 / 2.0)) if chi2 >= 0 else None
    return round(chi2, 4), p


def two_proportion_diff_ci(a_pos, a_n, b_pos, b_n, z=1.96):
    """Wald CI for difference in proportions, with continuity warning if cells are small."""
    if a_n == 0 or b_n == 0:
        return None
    p1 = a_pos / a_n
    p2 = b_pos / b_n
    se = math.sqrt(p1 * (1 - p1) / a_n + p2 * (1 - p2) / b_n)
    diff = p1 - p2
    return {"diff": round(diff, 4), "ci95_low": round(diff - z * se, 4), "ci95_high": round(diff + z * se, 4), "se": round(se, 4)}


def main():
    raw = load(RAW_PATH)
    ok_rows = [r for r in raw if r.get("ok") and r.get("classification")]
    bad_rows = [r for r in raw if not (r.get("ok") and r.get("classification"))]
    print(f"Records: total={len(raw)}, ok={len(ok_rows)}, bad={len(bad_rows)}")

    rows = []
    for r in ok_rows:
        orig_fam = r["original_family"]
        kimi_fam = (r["classification"] or {}).get("pleading_failure_family", "UNKNOWN")
        orig_bucket = family_bucket(orig_fam)
        kimi_bucket = family_bucket(kimi_fam)
        rows.append({
            "source_file": r["source_file"],
            "representation": r["representation"],
            "original_model": r["original_model"],
            "orig_family": orig_fam,
            "kimi_family": kimi_fam,
            "orig_bucket": orig_bucket,
            "kimi_bucket": kimi_bucket,
            "orig_mech": r["original_mechanism"],
            "kimi_mech": (r["classification"] or {}).get("pleading_failure_mechanism"),
            "kimi_confidence": (r["classification"] or {}).get("confidence"),
        })

    # Exact match rates
    atomic_fam_matches = sum(1 for x in rows if x["orig_family"] == x["kimi_family"])
    bucket_matches = sum(1 for x in rows if x["orig_bucket"] == x["kimi_bucket"])
    mech_matches = sum(1 for x in rows if x["orig_mech"] == x["kimi_mech"])

    n = len(rows)

    atomic_fam_kappa = cohen_kappa([x["orig_family"] for x in rows], [x["kimi_family"] for x in rows])
    bucket_kappa = cohen_kappa([x["orig_bucket"] for x in rows], [x["kimi_bucket"] for x in rows])
    mech_kappa = cohen_kappa([x["orig_mech"] for x in rows], [x["kimi_mech"] for x in rows])

    # By original model
    per_model = {}
    for model in sorted(set(x["original_model"] for x in rows if x["original_model"])):
        subset = [x for x in rows if x["original_model"] == model]
        sn = len(subset)
        if sn == 0:
            continue
        atomic_mt = sum(1 for x in subset if x["orig_family"] == x["kimi_family"])
        bucket_mt = sum(1 for x in subset if x["orig_bucket"] == x["kimi_bucket"])
        per_model[model] = {
            "n": sn,
            "family_exact_match_pct": pct(atomic_mt, sn),
            "bucket_match_pct": pct(bucket_mt, sn),
            "family_kappa": cohen_kappa([x["orig_family"] for x in subset], [x["kimi_family"] for x in subset]),
            "bucket_kappa": cohen_kappa([x["orig_bucket"] for x in subset], [x["kimi_bucket"] for x in subset]),
        }

    # Directional bias check: TRANSLATION-share by representation
    def trans_share(subset):
        if not subset:
            return None
        orig_t = sum(1 for x in subset if x["orig_bucket"] == TRANSLATION)
        kimi_t = sum(1 for x in subset if x["kimi_bucket"] == TRANSLATION)
        return {
            "n": len(subset),
            "orig_translation_n": orig_t,
            "orig_translation_pct": pct(orig_t, len(subset)),
            "kimi_translation_n": kimi_t,
            "kimi_translation_pct": pct(kimi_t, len(subset)),
            "delta_pp": round((kimi_t - orig_t) * 100.0 / len(subset), 2) if subset else None,
        }

    pro_se = [x for x in rows if x["representation"] == "PRO_SE"]
    repres = [x for x in rows if x["representation"] == "REPRESENTED"]

    pro_se_trans = trans_share(pro_se)
    repres_trans = trans_share(repres)

    # Replay: does Kimi's relabeling preserve the TRANSLATION pro-se excess vs represented?
    replay = None
    if pro_se and repres:
        kimi_pro_se_t = sum(1 for x in pro_se if x["kimi_bucket"] == TRANSLATION)
        kimi_rep_t = sum(1 for x in repres if x["kimi_bucket"] == TRANSLATION)
        orig_pro_se_t = sum(1 for x in pro_se if x["orig_bucket"] == TRANSLATION)
        orig_rep_t = sum(1 for x in repres if x["orig_bucket"] == TRANSLATION)

        chi_orig, p_orig = chi_square_2x2(orig_pro_se_t, len(pro_se) - orig_pro_se_t, orig_rep_t, len(repres) - orig_rep_t)
        chi_kimi, p_kimi = chi_square_2x2(kimi_pro_se_t, len(pro_se) - kimi_pro_se_t, kimi_rep_t, len(repres) - kimi_rep_t)

        replay = {
            "n_pro_se": len(pro_se),
            "n_represented": len(repres),
            "orig": {
                "pro_se_translation_pct": pct(orig_pro_se_t, len(pro_se)),
                "represented_translation_pct": pct(orig_rep_t, len(repres)),
                "chi2_1df": chi_orig,
                "p": p_orig,
                "gap_pp": round(pct(orig_pro_se_t, len(pro_se)) - pct(orig_rep_t, len(repres)), 2) if len(repres) else None,
                "diff_ci": two_proportion_diff_ci(orig_pro_se_t, len(pro_se), orig_rep_t, len(repres)),
            },
            "kimi": {
                "pro_se_translation_pct": pct(kimi_pro_se_t, len(pro_se)),
                "represented_translation_pct": pct(kimi_rep_t, len(repres)),
                "chi2_1df": chi_kimi,
                "p": p_kimi,
                "gap_pp": round(pct(kimi_pro_se_t, len(pro_se)) - pct(kimi_rep_t, len(repres)), 2) if len(repres) else None,
                "diff_ci": two_proportion_diff_ci(kimi_pro_se_t, len(pro_se), kimi_rep_t, len(repres)),
            },
        }

    # Confusion matrix: original bucket vs kimi bucket
    buckets = [TRANSLATION, PROCEDURAL_GATEWAY, NO_FAILURE, "OTHER"]
    confusion = {orig: {kimi: 0 for kimi in buckets} for orig in buckets}
    for x in rows:
        confusion[x["orig_bucket"]][x["kimi_bucket"]] += 1

    # Disagreement triage list
    disagreements = [
        {
            "source_file": x["source_file"],
            "representation": x["representation"],
            "original_model": x["original_model"],
            "orig_family": x["orig_family"],
            "kimi_family": x["kimi_family"],
            "orig_mech": x["orig_mech"],
            "kimi_mech": x["kimi_mech"],
            "kimi_confidence": x["kimi_confidence"],
        }
        for x in rows if x["orig_bucket"] != x["kimi_bucket"]
    ]

    results = {
        "n_sample": n,
        "overall": {
            "family_exact_match_n": atomic_fam_matches,
            "family_exact_match_pct": pct(atomic_fam_matches, n),
            "family_kappa": atomic_fam_kappa,
            "bucket_match_n": bucket_matches,
            "bucket_match_pct": pct(bucket_matches, n),
            "bucket_kappa": bucket_kappa,
            "mechanism_match_n": mech_matches,
            "mechanism_match_pct": pct(mech_matches, n),
            "mechanism_kappa": mech_kappa,
        },
        "by_original_model": per_model,
        "by_representation": {
            "pro_se": pro_se_trans,
            "represented": repres_trans,
        },
        "replay_translation_gap": replay,
        "bucket_confusion_matrix": confusion,
        "disagreements": disagreements,
    }

    with io.open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Build the report
    lines = []
    lines.append("# Kimi K2.6 mechanism-classification validation — agreement report\n")
    lines.append(f"Sample size (successful classifications): **{n}** of {len(raw)} attempted.\n")
    if bad_rows:
        lines.append(f"API or parse failures: {len(bad_rows)} (see kimi_k2_6_raw_results.json).\n")
    lines.append("")
    lines.append("## Headline\n")

    ov = results["overall"]
    lines.append(f"| Metric | Value |\n| --- | --- |\n| Family (atomic) exact match | **{ov['family_exact_match_pct']}%** ({ov['family_exact_match_n']}/{n}), kappa = {ov['family_kappa']} |")
    lines.append(f"| Family bucket {{TRANSLATION, PROCEDURAL_GATEWAY, NO_FAILURE, OTHER}} | **{ov['bucket_match_pct']}%** ({ov['bucket_match_n']}/{n}), kappa = {ov['bucket_kappa']} |")
    lines.append(f"| Atomic mechanism code | {ov['mechanism_match_pct']}% ({ov['mechanism_match_n']}/{n}), kappa = {ov['mechanism_kappa']} |")
    lines.append("")

    lines.append("## Kappa interpretation\n")
    lines.append("Landis & Koch: < 0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, > 0.80 almost perfect.\n")
    lines.append("The load-bearing metric for the note's TRANSLATION-family claim is **bucket kappa**.\n")

    lines.append("## Agreement by original classifier\n")
    lines.append("| Original model | n | Family exact match | Bucket match | Family kappa | Bucket kappa |\n| --- | --- | --- | --- | --- | --- |")
    for model, vals in per_model.items():
        lines.append(f"| {model} | {vals['n']} | {vals['family_exact_match_pct']}% | {vals['bucket_match_pct']}% | {vals['family_kappa']} | {vals['bucket_kappa']} |")
    lines.append("")
    lines.append(
        "Kimi K2.6 is a sibling model of Kimi K2.5 (the original wave classifier). If K2.6 agrees with K2.5 materially more than with GLM-5.1, within-family consistency is flagged; cross-model agreement is a stronger independence signal.\n"
    )

    lines.append("## Directional bias check — TRANSLATION share by representation\n")
    if pro_se_trans:
        lines.append(f"**Pro se** (n={pro_se_trans['n']}): original TRANSLATION = {pro_se_trans['orig_translation_pct']}%, Kimi TRANSLATION = {pro_se_trans['kimi_translation_pct']}%, delta = {pro_se_trans['delta_pp']} pp.")
    if repres_trans:
        lines.append(f"**Represented** (n={repres_trans['n']}): original TRANSLATION = {repres_trans['orig_translation_pct']}%, Kimi TRANSLATION = {repres_trans['kimi_translation_pct']}%, delta = {repres_trans['delta_pp']} pp.")
    lines.append("")
    lines.append("If the deltas are similar sign and magnitude for pro se and represented, reclassification is roughly unbiased across representation; if they differ materially, the TRANSLATION gap could be partly a coding artifact.\n")

    if replay:
        lines.append("## Replay of the note's TRANSLATION-family headline\n")
        lines.append("| Source | Pro se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | chi2(1df) | p |\n| --- | --- | --- | --- | --- | --- |")
        o = replay["orig"]
        k = replay["kimi"]
        lines.append(f"| Original coding | {o['pro_se_translation_pct']}% | {o['represented_translation_pct']}% | {o['gap_pp']} | {o['chi2_1df']} | {o['p']} |")
        lines.append(f"| Kimi K2.6 recoding | {k['pro_se_translation_pct']}% | {k['represented_translation_pct']}% | {k['gap_pp']} | {k['chi2_1df']} | {k['p']} |")
        lines.append("")
        lines.append(f"Pro-se - represented gap CI (original): {o['diff_ci']}")
        lines.append(f"Pro-se - represented gap CI (Kimi): {k['diff_ci']}")
        lines.append("")
        lines.append(
            "The note's in-text stat (`48.3% pro se vs 17.9% represented` from the 676-case full universe) is the population figure; the row above is the sample replay. A survived gap (Kimi gap within ~10 pp of original gap and chi2 significant) is the evidence the note can cite.\n"
        )

    lines.append("## Bucket confusion matrix (original -> Kimi)\n")
    hdr = "| orig \\ kimi | " + " | ".join(buckets) + " |"
    lines.append(hdr)
    lines.append("| --- |" + " --- |" * len(buckets))
    for orig in buckets:
        row = f"| {orig} | " + " | ".join(str(confusion[orig][k]) for k in buckets) + " |"
        lines.append(row)
    lines.append("")

    lines.append(f"## Disagreements ({len(disagreements)} cases)\n")
    lines.append("See agreement_results.json `disagreements` array for full list. Hand-read these cases to triage whether Kimi or original is closer to the opinion's reasoning.\n")

    lines.append("## Decision rule status\n")
    bucket_k = ov["bucket_kappa"] or 0
    if bucket_k >= 0.60:
        verdict = "KEEP. Bucket kappa >= 0.60 supports the TRANSLATION claim as-is."
    elif bucket_k >= 0.45:
        verdict = "SOFTEN. Bucket kappa in [0.45, 0.60) — keep the directional claim but remove in-text precision of 48.3%/17.9%; move numbers to appendix with kappa disclosed."
    else:
        verdict = "PULL the numeric claim. Bucket kappa < 0.45 — retain only the Ely narrative and the structural argument."
    lines.append(f"**{verdict}**\n")

    lines.append("## Independence caveat\n")
    lines.append(
        "Kimi K2.6 is architecturally related to Kimi K2.5 (the original classifier for 532/676 cases). "
        "For a stronger independence check, re-run the same sample with a model from a different provider "
        "(e.g., `anthropic/claude-sonnet-4.6` or `google/gemini-3-pro`). The `run_kimi_k2_6.py` script can be "
        "generalized by changing MODEL_SLUG; the agreement pipeline here takes the validator's output as an input.\n"
    )

    with io.open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Report: {REPORT_PATH}")
    print(f"Results: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
