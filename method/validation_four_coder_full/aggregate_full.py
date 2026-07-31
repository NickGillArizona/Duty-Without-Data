"""
Aggregate 22 fourth-coder subagent outputs into a full-universe (n=668)
fourth-coder dataset. Compute Cohen's kappa for fourth vs. ensemble and
fourth vs. original at both bucket and family levels. Replay the TRANSLATION
and PROCEDURAL_GATEWAY gaps with the fourth coder as the PRIMARY labeler.
"""
import io
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
THREE_MODEL = HERE.parent / "validation_three_model"

FAMILY_TO_BUCKET = {
    "TRANSLATION": "TRANSLATION",
    "PROCEDURAL_GATEWAY": "PROCEDURAL_GATEWAY",
    "NO_FAILURE_PLAINTIFF_WIN": "NO_FAILURE",
    "NO_FAILURE_DEFENDANT_WIN": "NO_FAILURE",
    "ELEMENT_MISMATCH": "OTHER",
    "CAUSAL_LINK": "OTHER",
    "FACTUAL_DETAIL": "OTHER",
    "MIXED": "OTHER",
    "UNCLEAR": "OTHER",
    "MERITS_EVIDENCE": "OTHER",
}
VALID_FAMILIES = set(FAMILY_TO_BUCKET.keys())
VALID_MECHS = {
    "REQUEST_NOT_ALLEGED", "ELEMENTS_NOT_TIED_TO_FACTS", "DISABILITY_NEXUS_MISSING",
    "NO_COGNIZABLE_FHA_THEORY", "STATUTORY_HOOK_UNCLEAR",
    "JURISDICTION_OR_STANDING", "EXHAUSTION_OR_PRECLUSION", "LIMITATIONS_OR_TIMELINESS",
    "ADVERSE_ACTION_NOT_CONNECTED", "COMPARATOR_OR_INTENT_GAP", "TECHNICAL_PROOF_GAP",
    "TIMING_OR_NOTICE_GAP",
    "MIXED", "UNCLEAR", "CLAIM_SURVIVES_OR_PLAINTIFF_PREVAILS",
}
BUCKETS = ["TRANSLATION", "PROCEDURAL_GATEWAY", "NO_FAILURE", "OTHER"]


def cohen_kappa(a, b):
    assert len(a) == len(b)
    n = len(a)
    if n == 0:
        return None
    cats = sorted(set(a) | set(b))
    idx = {c: i for i, c in enumerate(cats)}
    k = len(cats)
    m = [[0] * k for _ in range(k)]
    for x, y in zip(a, b):
        m[idx[x]][idx[y]] += 1
    po = sum(m[i][i] for i in range(k)) / n
    rs = [sum(m[i]) for i in range(k)]
    cs = [sum(m[i][j] for i in range(k)) for j in range(k)]
    pe = sum((rs[i] / n) * (cs[i] / n) for i in range(k))
    if pe >= 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def chi_square_2x2(a, b, c, d):
    n = a + b + c + d
    r1, r2 = a + b, c + d
    c1, c2 = a + c, b + d
    if 0 in (r1, r2, c1, c2):
        return None, None
    e = [[r1 * c1 / n, r1 * c2 / n], [r2 * c1 / n, r2 * c2 / n]]
    o = [[a, b], [c, d]]
    chi2 = 0.0
    for i in range(2):
        for j in range(2):
            diff = abs(o[i][j] - e[i][j]) - 0.5
            if diff < 0:
                diff = 0
            chi2 += diff * diff / e[i][j]
    p = math.erfc(math.sqrt(chi2 / 2.0))
    return chi2, p


def two_prop_ci(k1, n1, k2, n2, z=1.96):
    p1 = k1 / n1
    p2 = k2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    diff = p1 - p2
    return {"diff_pp": round(diff * 100, 2),
            "ci95_low_pp": round((diff - z * se) * 100, 2),
            "ci95_high_pp": round((diff + z * se) * 100, 2),
            "se_pp": round(se * 100, 3)}


def family_bucket(fam):
    return FAMILY_TO_BUCKET.get(fam, "OTHER")


# --- Load fourth coder from all 22 chunks with position-based canonical source_file ---
fourth = {}
len_mismatch = []
for i in range(1, 23):
    sub_path = HERE / f"coder_seat_{i:02d}_results.json"
    chunk_path = HERE / f"chunk_{i:02d}_blind.json"
    if not sub_path.exists():
        print(f"MISSING: {sub_path}")
        continue
    with io.open(sub_path, encoding="utf-8") as f:
        results = json.load(f)
    with io.open(chunk_path, encoding="utf-8") as f:
        chunk = json.load(f)
    if len(results) != len(chunk):
        len_mismatch.append((i, len(results), len(chunk)))
        print(f"WARN coder_seat_{i:02d}: results={len(results)} chunk={len(chunk)}")
    for j, row in enumerate(results):
        canonical = chunk[j]["source_file"] if j < len(chunk) else row.get("source_file", "")
        row_copy = dict(row)
        row_copy["source_file"] = canonical
        # Normalize key variants used by subagents 17 and 19
        if "pleading_failure_family" not in row_copy:
            row_copy["pleading_failure_family"] = row_copy.get("family") or row_copy.get("family_code")
        if "pleading_failure_mechanism" not in row_copy:
            row_copy["pleading_failure_mechanism"] = row_copy.get("mechanism") or row_copy.get("mechanism_code")
        fourth[canonical] = row_copy
print(f"Fourth-coder rows loaded: {len(fourth)}")

# --- Load universe_668 for representation, original_family, etc. ---
with io.open(HERE / "universe_668.json", encoding="utf-8") as f:
    universe = json.load(f)
print(f"Universe: {len(universe)}")

# --- Load ensemble_results.json for per-case ensemble family/bucket ---
with io.open(THREE_MODEL / "ensemble_results.json", encoding="utf-8") as f:
    ensemble_results = json.load(f)

# ensemble_results.json stores a subset in disagreements_sample; we need the per-case
# ensemble label. The compute_ensemble.py script did not save per-row ensemble labels
# to JSON. We recompute ensemble from raw results inline.
def load_json(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)

kimi = {r["source_file"]: r for r in load_json(THREE_MODEL / "kimi_raw_results.json")}
glm = {r["source_file"]: r for r in load_json(THREE_MODEL / "glm_raw_results.json")}
deepseek = {r["source_file"]: r for r in load_json(THREE_MODEL / "deepseek_raw_results.json")}


def model_family(rec):
    if not rec or not rec.get("ok") or not rec.get("classification"):
        return None
    return rec["classification"].get("pleading_failure_family")


def resolve_ensemble_family_bucket(sf):
    fams = [model_family(kimi.get(sf)), model_family(glm.get(sf)), model_family(deepseek.get(sf))]
    if None in fams:
        return None, None, "missing"
    buckets = [family_bucket(f) for f in fams]
    bc = Counter(buckets)
    bmost = bc.most_common()
    if len(bmost) == 1:
        ens_bucket, bres = bmost[0][0], "unanimous"
    elif bmost[0][1] == 2:
        ens_bucket, bres = bmost[0][0], "majority"
    else:
        ens_bucket, bres = "OTHER", "split"  # effective bucket for split
    fc = Counter(fams)
    fmost = fc.most_common()
    if fmost[0][1] >= 2:
        ens_family = fmost[0][0]
    else:
        ens_family = None
    return ens_family, ens_bucket, bres


# --- Build merged rows ---
rows = []
missing_fourth = []
missing_ensemble = []
for u in universe:
    sf = u["source_file"]
    fc = fourth.get(sf)
    if not fc:
        missing_fourth.append(sf)
        continue
    ens_family, ens_bucket, bres = resolve_ensemble_family_bucket(sf)
    if ens_bucket is None:
        missing_ensemble.append(sf)
        continue
    fam = fc["pleading_failure_family"]
    mech = fc["pleading_failure_mechanism"]
    rows.append({
        "source_file": sf,
        "representation": u.get("representation"),
        "original_family": u.get("original_family"),
        "original_bucket": family_bucket(u.get("original_family")),
        "ensemble_family": ens_family,
        "ensemble_bucket": ens_bucket,
        "ensemble_resolution": bres,
        "fourth_family": fam,
        "fourth_mechanism": mech,
        "fourth_confidence": fc.get("confidence"),
        "fourth_family_valid": fam in VALID_FAMILIES,
        "fourth_mechanism_valid": mech in VALID_MECHS,
        "fourth_bucket": family_bucket(fam),
    })

print(f"Matched rows: {len(rows)}   Missing fourth: {len(missing_fourth)}   Missing ensemble: {len(missing_ensemble)}")

# Off-taxonomy
bad_fams = Counter(r["fourth_family"] for r in rows if not r["fourth_family_valid"])
bad_mechs = Counter(r["fourth_mechanism"] for r in rows if not r["fourth_mechanism_valid"])
print(f"Off-taxonomy families: {dict(bad_fams)}")
print(f"Off-taxonomy mechanisms: {dict(bad_mechs)}")

# --- Cohen's kappa ---
# Full universe: bucket-level
k_fe_b = cohen_kappa([r["fourth_bucket"] for r in rows], [r["ensemble_bucket"] for r in rows])
k_fo_b = cohen_kappa([r["fourth_bucket"] for r in rows], [r["original_bucket"] for r in rows])
k_eo_b = cohen_kappa([r["ensemble_bucket"] for r in rows], [r["original_bucket"] for r in rows])

# Family-level kappa: only rows with valid fourth family AND non-None ensemble family
vrows = [r for r in rows if r["fourth_family_valid"]]
vrows_ens = [r for r in vrows if r["ensemble_family"] is not None]
k_fe_f = cohen_kappa([r["fourth_family"] for r in vrows_ens], [r["ensemble_family"] for r in vrows_ens])
k_fo_f = cohen_kappa([r["fourth_family"] for r in vrows], [r["original_family"] for r in vrows])

# Bucket match rates
match_fe = sum(1 for r in rows if r["fourth_bucket"] == r["ensemble_bucket"])
match_fo = sum(1 for r in rows if r["fourth_bucket"] == r["original_bucket"])

# Confusion matrices
def confusion(a_key, b_key):
    mat = {x: {y: 0 for y in BUCKETS} for x in BUCKETS}
    for r in rows:
        mat[r[a_key]][r[b_key]] += 1
    return mat

conf_orig_fourth = confusion("original_bucket", "fourth_bucket")
conf_ens_fourth = confusion("ensemble_bucket", "fourth_bucket")

# --- TRANSLATION gap with fourth coder as PRIMARY ---
ps_rows = [r for r in rows if (r.get("representation") or "").upper() == "PRO_SE"]
rp_rows = [r for r in rows if (r.get("representation") or "").upper() == "REPRESENTED"]

def bucket_ct(subset, key, bucket):
    return sum(1 for r in subset if r[key] == bucket)

# Fourth coder primary
ps_T_fourth = bucket_ct(ps_rows, "fourth_bucket", "TRANSLATION")
rp_T_fourth = bucket_ct(rp_rows, "fourth_bucket", "TRANSLATION")
chi_f, p_f = chi_square_2x2(ps_T_fourth, len(ps_rows) - ps_T_fourth, rp_T_fourth, len(rp_rows) - rp_T_fourth)
ci_f = two_prop_ci(ps_T_fourth, len(ps_rows), rp_T_fourth, len(rp_rows))
gap_f_pp = 100 * (ps_T_fourth / len(ps_rows) - rp_T_fourth / len(rp_rows))

# Ensemble primary (should match ensemble_report.md)
ps_T_ens = bucket_ct(ps_rows, "ensemble_bucket", "TRANSLATION")
rp_T_ens = bucket_ct(rp_rows, "ensemble_bucket", "TRANSLATION")
chi_e, p_e = chi_square_2x2(ps_T_ens, len(ps_rows) - ps_T_ens, rp_T_ens, len(rp_rows) - rp_T_ens)
ci_e = two_prop_ci(ps_T_ens, len(ps_rows), rp_T_ens, len(rp_rows))
gap_e_pp = 100 * (ps_T_ens / len(ps_rows) - rp_T_ens / len(rp_rows))

# Original primary
ps_T_orig = bucket_ct(ps_rows, "original_bucket", "TRANSLATION")
rp_T_orig = bucket_ct(rp_rows, "original_bucket", "TRANSLATION")
chi_o, p_o = chi_square_2x2(ps_T_orig, len(ps_rows) - ps_T_orig, rp_T_orig, len(rp_rows) - rp_T_orig)
ci_o = two_prop_ci(ps_T_orig, len(ps_rows), rp_T_orig, len(rp_rows))
gap_o_pp = 100 * (ps_T_orig / len(ps_rows) - rp_T_orig / len(rp_rows))

# PROCEDURAL_GATEWAY gap with fourth as primary
ps_PG_fourth = bucket_ct(ps_rows, "fourth_bucket", "PROCEDURAL_GATEWAY")
rp_PG_fourth = bucket_ct(rp_rows, "fourth_bucket", "PROCEDURAL_GATEWAY")
chi_pg_f, p_pg_f = chi_square_2x2(ps_PG_fourth, len(ps_rows) - ps_PG_fourth, rp_PG_fourth, len(rp_rows) - rp_PG_fourth)
gap_pg_f_pp = 100 * (ps_PG_fourth / len(ps_rows) - rp_PG_fourth / len(rp_rows))

# Confidence distribution
conf_counter = Counter(r["fourth_confidence"] for r in rows)

# --- Print summary ---
print("\n=== Cohen's kappa on full universe ===")
print(f"  fourth vs ensemble  (bucket, n={len(rows)}):  {k_fe_b:.4f}")
print(f"  fourth vs original  (bucket, n={len(rows)}):  {k_fo_b:.4f}")
print(f"  ensemble vs original (bucket, n={len(rows)}): {k_eo_b:.4f}")
print(f"  fourth vs ensemble  (family, n={len(vrows_ens)}): {k_fe_f:.4f}")
print(f"  fourth vs original  (family, n={len(vrows)}):     {k_fo_f:.4f}")

print(f"\n  bucket match fourth vs ensemble: {match_fe}/{len(rows)} = {match_fe/len(rows):.2%}")
print(f"  bucket match fourth vs original: {match_fo}/{len(rows)} = {match_fo/len(rows):.2%}")

print(f"\nSample sizes: pro_se={len(ps_rows)}  represented={len(rp_rows)}  other={len(rows)-len(ps_rows)-len(rp_rows)}")

print("\n=== TRANSLATION gap — fourth coder as primary ===")
print(f"  original: pro_se {ps_T_orig}/{len(ps_rows)} ({100*ps_T_orig/len(ps_rows):.2f}%)  rep {rp_T_orig}/{len(rp_rows)} ({100*rp_T_orig/len(rp_rows):.2f}%)  gap {gap_o_pp:.2f}pp  chi2={chi_o:.4f}  p={p_o:.4e}")
print(f"  ensemble: pro_se {ps_T_ens}/{len(ps_rows)} ({100*ps_T_ens/len(ps_rows):.2f}%)  rep {rp_T_ens}/{len(rp_rows)} ({100*rp_T_ens/len(rp_rows):.2f}%)  gap {gap_e_pp:.2f}pp  chi2={chi_e:.4f}  p={p_e:.4e}")
print(f"  fourth:   pro_se {ps_T_fourth}/{len(ps_rows)} ({100*ps_T_fourth/len(ps_rows):.2f}%)  rep {rp_T_fourth}/{len(rp_rows)} ({100*rp_T_fourth/len(rp_rows):.2f}%)  gap {gap_f_pp:.2f}pp  chi2={chi_f:.4f}  p={p_f:.4e}")
print(f"  CI fourth: {ci_f}")

print("\n=== PROCEDURAL_GATEWAY gap — fourth coder as primary ===")
print(f"  pro_se {ps_PG_fourth}/{len(ps_rows)} ({100*ps_PG_fourth/len(ps_rows):.2f}%)  rep {rp_PG_fourth}/{len(rp_rows)} ({100*rp_PG_fourth/len(rp_rows):.2f}%)  gap {gap_pg_f_pp:.2f}pp  chi2={chi_pg_f:.4f}  p={p_pg_f:.4e}")

print(f"\nFourth-coder confidence: {dict(conf_counter)}")

print("\nConfusion (original -> fourth):")
for o in BUCKETS:
    print(f"  {o}: {conf_orig_fourth[o]}")
print("\nConfusion (ensemble -> fourth):")
for o in BUCKETS:
    print(f"  {o}: {conf_ens_fourth[o]}")

# --- Save merged dataset ---
out = {
    "n_universe": len(rows),
    "n_missing_fourth": len(missing_fourth),
    "missing_fourth": missing_fourth,
    "n_missing_ensemble": len(missing_ensemble),
    "missing_ensemble": missing_ensemble,
    "chunk_length_mismatches": len_mismatch,
    "kappa": {
        "fourth_vs_ensemble_bucket": round(k_fe_b, 4),
        "fourth_vs_original_bucket": round(k_fo_b, 4),
        "ensemble_vs_original_bucket": round(k_eo_b, 4),
        "fourth_vs_ensemble_family": round(k_fe_f, 4),
        "fourth_vs_original_family": round(k_fo_f, 4),
        "n_family_kappa_ens": len(vrows_ens),
        "n_family_kappa_orig": len(vrows),
    },
    "bucket_match": {
        "fourth_vs_ensemble": round(match_fe / len(rows), 4),
        "fourth_vs_original": round(match_fo / len(rows), 4),
    },
    "taxonomy_violations": {
        "invalid_families": dict(bad_fams),
        "invalid_mechanisms": dict(bad_mechs),
    },
    "confidence_distribution": dict(conf_counter),
    "sample_sizes": {
        "pro_se": len(ps_rows),
        "represented": len(rp_rows),
    },
    "translation_gap": {
        "original": {
            "pro_se_T": ps_T_orig, "pro_se_n": len(ps_rows),
            "rep_T": rp_T_orig, "rep_n": len(rp_rows),
            "gap_pp": round(gap_o_pp, 2), "chi2": round(chi_o, 4), "p": p_o, "ci_pp": ci_o,
        },
        "ensemble": {
            "pro_se_T": ps_T_ens, "pro_se_n": len(ps_rows),
            "rep_T": rp_T_ens, "rep_n": len(rp_rows),
            "gap_pp": round(gap_e_pp, 2), "chi2": round(chi_e, 4), "p": p_e, "ci_pp": ci_e,
        },
        "fourth": {
            "pro_se_T": ps_T_fourth, "pro_se_n": len(ps_rows),
            "rep_T": rp_T_fourth, "rep_n": len(rp_rows),
            "gap_pp": round(gap_f_pp, 2), "chi2": round(chi_f, 4), "p": p_f, "ci_pp": ci_f,
        },
    },
    "procedural_gateway_gap_fourth": {
        "pro_se_PG": ps_PG_fourth, "pro_se_n": len(ps_rows),
        "rep_PG": rp_PG_fourth, "rep_n": len(rp_rows),
        "gap_pp": round(gap_pg_f_pp, 2), "chi2": round(chi_pg_f, 4), "p": p_pg_f,
    },
    "confusion_orig_to_fourth": conf_orig_fourth,
    "confusion_ens_to_fourth": conf_ens_fourth,
    "rows": rows,
}
with io.open(HERE / "fourth_coder_full_merged.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print(f"\nWrote {HERE / 'fourth_coder_full_merged.json'}")
