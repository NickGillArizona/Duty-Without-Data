#!/usr/bin/env python3
"""Build a merged (original-668 + July-2026 extension: 60 coded across two rounds) mechanism summary
using this module's own stat conventions, so figures and the Note draw from one
source. Does NOT modify the original raw_results or ensemble_results (which
anchor the vs-original validation layer). Writes mechanism_merged_summary.json.
"""
import io
import json
from collections import Counter
from pathlib import Path

import compute_ensemble as ce

HERE = Path(__file__).resolve().parent
# July-2026 mechanism-extension coding results. The raw per-case extension input is not
# redistributed in the public archive; place it alongside this script (or regenerate it via
# the extension pipeline) to rebuild the merged summary. mechanism_merged_summary.json
# (the committed output) already reflects it.
EXT = HERE / "mechanism_extension_results.json"

TRANSLATION = "TRANSLATION"


def load_original_triplets():
    raws = {k: ce.load(HERE / f"{k}_raw_results.json") for k in ("kimi", "glm", "deepseek")}
    idx = {k: {r["source_file"]: r for r in v} for k, v in raws.items()}
    sfs = set(idx["kimi"]) & set(idx["glm"]) & set(idx["deepseek"])
    rows = []
    for sf in sfs:
        fams, ok = {}, True
        for m in ("kimi", "glm", "deepseek"):
            r = idx[m][sf]
            cls = r.get("classification") if r.get("ok") else None
            if not cls:
                ok = False
                break
            fams[m] = cls.get("pleading_failure_family", "UNKNOWN")
        if not ok:
            continue
        rep = idx["kimi"][sf].get("representation")
        rows.append((fams, rep))
    return rows


def resolve(fams):
    c = Counter(fams.values())
    lab, n = c.most_common(1)[0]
    return lab if n >= 2 else "OTHER"


def main():
    orig = load_original_triplets()
    ext_rows = []
    ext_sources = [EXT]
    r2 = EXT.parent / "round2_results.json"
    if r2.exists():
        ext_sources.append(r2)
    for src in ext_sources:
        data = json.load(open(src, encoding="utf-8"))
        for r in data["rows"]:
            fams = {m: r["families"][m] for m in ("kimi", "glm", "deepseek")}
            rep = ("PRO_SE" if r["pro_se"] is True else
                   "REPRESENTED" if r["pro_se"] is False else "UNKNOWN")
            ext_rows.append((fams, rep))

    all_rows = orig + ext_rows  # list of (fams dict, representation)

    # ensemble bucket per row
    def bucket_of(fams):
        return ce.family_bucket(resolve(fams))

    merged = [(bucket_of(f), rep) for f, rep in all_rows]
    pro = [b for b, rep in merged if rep == "PRO_SE"]
    rep = [b for b, rep in merged if rep == "REPRESENTED"]
    n_pro, n_rep = len(pro), len(rep)
    pro_t = sum(1 for b in pro if b == TRANSLATION)
    rep_t = sum(1 for b in rep if b == TRANSLATION)
    pro_pct = round(100 * pro_t / n_pro, 2)
    rep_pct = round(100 * rep_t / n_rep, 2)
    gap = round(pro_pct - rep_pct, 2)
    chi2, p = ce.chi_square_2x2(pro_t, n_pro - pro_t, rep_t, n_rep - rep_t)
    ci = ce.two_proportion_diff_ci(pro_t, n_pro, rep_t, n_rep)

    # family x representation chi2(8) + Cramer's V, and bucket Fleiss
    fams_present = sorted({resolve(f) for f, rp in all_rows if rp in ("PRO_SE", "REPRESENTED")})
    def collapse(f):
        return "NO_FAILURE" if str(f).startswith("NO_FAILURE") else f
    cats = sorted({collapse(x) for x in fams_present})
    psc = Counter(collapse(resolve(f)) for f, rp in all_rows if rp == "PRO_SE")
    rpc = Counter(collapse(resolve(f)) for f, rp in all_rows if rp == "REPRESENTED")
    ntot = n_pro + n_rep
    chi8 = 0.0
    for c in cats:
        for cnt, tot in ((psc[c], n_pro), (rpc[c], n_rep)):
            exp = (psc[c] + rpc[c]) * tot / ntot
            if exp > 0:
                chi8 += (cnt - exp) ** 2 / exp
    import math
    cramers_v = math.sqrt(chi8 / ntot)
    triplets = [tuple(ce.family_bucket(f[m]) for m in ("kimi", "glm", "deepseek"))
                for f, rp in all_rows]
    fleiss = ce.fleiss_kappa_three(triplets)

    # Per-bucket x representation breakdown (makes PROCEDURAL_GATEWAY etc. traceable
    # on the merged 728-case universe; consumed by Appendix M M.10 / M.16.2).
    per_bucket = {}
    for bkt in ce.BUCKETS:
        pc = sum(1 for b, rp in merged if rp == "PRO_SE" and b == bkt)
        rc = sum(1 for b, rp in merged if rp == "REPRESENTED" and b == bkt)
        cb, pb = ce.chi_square_2x2(pc, n_pro - pc, rc, n_rep - rc)
        per_bucket[bkt] = {
            "pro_se_count": pc, "pro_se_pct": round(100 * pc / n_pro, 2),
            "represented_count": rc, "represented_pct": round(100 * rc / n_rep, 2),
            "gap_pp": round(100 * pc / n_pro - 100 * rc / n_rep, 2),
            "chi2_1df": cb, "p": pb,
        }

    summary = {
        "description": "Merged mechanism ensemble: original 668 + July-2026 extension (60 coded: 47 round 1 + 13 round 2; 62 attempted, 2 dropped unparseable). "
                       "Built by build_merged_summary.py using compute_ensemble stat functions. "
                       "Original ensemble_results.json is unchanged (anchors vs-original layer).",
        "n_coded_total": len(all_rows),
        "translation_replay_full_universe": {
            "n_pro_se": n_pro,
            "n_represented": n_rep,
            "ensemble": {
                "pro_se_translation_pct": pro_pct,
                "represented_translation_pct": rep_pct,
                "pro_se_translation_count": pro_t,
                "represented_translation_count": rep_t,
                "gap_pp": gap,
                "chi2_1df": chi2,
                "p": p,
                "diff_ci": ci,
            },
        },
        "family_x_representation": {
            "n": ntot, "chi2_8df": round(chi8, 2), "cramers_v": round(cramers_v, 3),
            "per_bucket": per_bucket,
        },
        "fleiss_bucket_kappa": fleiss,
    }
    out = HERE / "mechanism_merged_summary.json"
    with io.open(out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2))
    print("\nWROTE", out)


if __name__ == "__main__":
    main()
