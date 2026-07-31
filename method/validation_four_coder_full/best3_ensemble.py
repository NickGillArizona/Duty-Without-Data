"""
Best-3 ensemble: Kimi K2.6 + GLM-5.1 + Claude Opus 4.7 (drops DeepSeek V3.2 and Kimi K2.5).

Computes majority-vote bucket ensemble, TRANSLATION gap replay, and inter-coder kappas
against original (K2.5+GLM-5.1) and against the existing three-model ensemble.
"""
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
THREE_MODEL = HERE.parent / "validation_three_model"

NO_FAILURE_FAMILIES = {"NO_FAILURE_PLAINTIFF_WIN", "NO_FAILURE_DEFENDANT_WIN"}


def family_to_bucket(fam):
    if fam is None:
        return None
    if fam in NO_FAILURE_FAMILIES:
        return "NO_FAILURE"
    if fam == "TRANSLATION":
        return "TRANSLATION"
    if fam == "PROCEDURAL_GATEWAY":
        return "PROCEDURAL_GATEWAY"
    return "OTHER"


def majority_bucket(buckets):
    """Majority vote across three buckets; 3-way split resolves to OTHER."""
    buckets = [b for b in buckets if b is not None]
    if not buckets:
        return None, "all_none"
    c = Counter(buckets)
    top, top_n = c.most_common(1)[0]
    if top_n >= 2:
        return top, "majority"
    return "OTHER", "three_way_split"


def load_raw(path):
    with open(path) as f:
        rows = json.load(f)
    idx = {}
    for r in rows:
        cls = r.get("classification") or {}
        fam = cls.get("pleading_failure_family")
        idx[r["source_file"]] = {
            "representation": r.get("representation"),
            "original_family": r.get("original_family"),
            "family": fam,
            "bucket": family_to_bucket(fam),
        }
    return idx


def cohens_kappa(a, b):
    """Cohen's kappa for paired categorical labels (ignore positions where either is None)."""
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    n = len(pairs)
    if n == 0:
        return None, 0
    cats = sorted(set([p[0] for p in pairs] + [p[1] for p in pairs]))
    agree = sum(1 for x, y in pairs if x == y)
    po = agree / n
    pe = 0.0
    for c in cats:
        pa = sum(1 for x, _ in pairs if x == c) / n
        pb = sum(1 for _, y in pairs if y == c) / n
        pe += pa * pb
    if pe == 1.0:
        return 1.0, n
    return (po - pe) / (1 - pe), n


def two_prop_gap(k1, n1, k2, n2):
    """Return gap (p1-p2 in pp), chi2(1), p-value, 95% CI on gap in pp."""
    from scipy.stats import chi2_contingency  # local
    p1, p2 = k1 / n1, k2 / n2
    gap_pp = (p1 - p2) * 100
    table = [[k1, n1 - k1], [k2, n2 - k2]]
    try:
        chi2, p, _, _ = chi2_contingency(table, correction=False)
    except ValueError:
        chi2, p = float("nan"), float("nan")
    # Normal-approx CI on difference
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z = 1.959963984540054
    lo = (p1 - p2 - z * se) * 100
    hi = (p1 - p2 + z * se) * 100
    return gap_pp, chi2, p, lo, hi


# --- Load three sources ---
kimi = load_raw(THREE_MODEL / "kimi_raw_results.json")
glm = load_raw(THREE_MODEL / "glm_raw_results.json")

with open(HERE / "fourth_coder_full_merged.json") as f:
    merged = json.load(f)

opus_rows = merged["rows"]

# Build the 668-case universe keyed on source_file (Opus is authoritative scope).
universe = []
for r in opus_rows:
    sf = r["source_file"]
    if sf not in kimi or sf not in glm:
        continue
    universe.append({
        "source_file": sf,
        "representation": r["representation"],
        "original_bucket": r["original_bucket"],
        "ensemble_bucket": r["ensemble_bucket"],
        "k26_bucket": kimi[sf]["bucket"],
        "glm_bucket": glm[sf]["bucket"],
        "opus_bucket": r["fourth_bucket"],
    })

print(f"universe rows: {len(universe)}")

# Compute best-3 majority vote
for row in universe:
    b, how = majority_bucket([row["k26_bucket"], row["glm_bucket"], row["opus_bucket"]])
    row["best3_bucket"] = b
    row["best3_resolution"] = how

# --- TRANSLATION gap replay ---
pro_se = [r for r in universe if r["representation"] == "PRO_SE"]
rep = [r for r in universe if r["representation"] == "REPRESENTED"]
n_ps, n_rep = len(pro_se), len(rep)
print(f"pro_se: {n_ps}  represented: {n_rep}")

for label, key in [
    ("original", "original_bucket"),
    ("ensemble (K2.6+GLM+DeepSeek)", "ensemble_bucket"),
    ("Opus 4.7 solo", "opus_bucket"),
    ("K2.6 solo", "k26_bucket"),
    ("GLM-5.1 solo", "glm_bucket"),
    ("BEST-3 (K2.6+GLM+Opus)", "best3_bucket"),
]:
    ps_trans = sum(1 for r in pro_se if r[key] == "TRANSLATION")
    rep_trans = sum(1 for r in rep if r[key] == "TRANSLATION")
    gap_pp, chi2, p, lo, hi = two_prop_gap(ps_trans, n_ps, rep_trans, n_rep)
    print(f"\n{label}")
    print(f"  pro_se TRANSLATION: {ps_trans}/{n_ps} = {ps_trans/n_ps*100:.2f}%")
    print(f"  rep TRANSLATION:    {rep_trans}/{n_rep} = {rep_trans/n_rep*100:.2f}%")
    print(f"  gap: {gap_pp:.2f} pp   chi2={chi2:.2f}  p={p:.2e}  CI=[{lo:.2f}, {hi:.2f}] pp")

# --- PROCEDURAL_GATEWAY mirror gap under BEST-3 ---
ps_pg = sum(1 for r in pro_se if r["best3_bucket"] == "PROCEDURAL_GATEWAY")
rep_pg = sum(1 for r in rep if r["best3_bucket"] == "PROCEDURAL_GATEWAY")
gap_pp, chi2, p, lo, hi = two_prop_gap(ps_pg, n_ps, rep_pg, n_rep)
print(f"\nBEST-3 PROCEDURAL_GATEWAY mirror")
print(f"  pro_se PG: {ps_pg}/{n_ps} = {ps_pg/n_ps*100:.2f}%   rep PG: {rep_pg}/{n_rep} = {rep_pg/n_rep*100:.2f}%")
print(f"  gap: {gap_pp:.2f} pp   chi2={chi2:.2f}  p={p:.2e}  CI=[{lo:.2f}, {hi:.2f}] pp")

# --- Inter-coder kappa on full universe ---
def kcol(rows, key):
    return [r[key] for r in rows]

print("\n--- Cohen's kappa (bucket) ---")
for a_label, a_key in [
    ("BEST-3", "best3_bucket"),
    ("Opus", "opus_bucket"),
    ("K2.6", "k26_bucket"),
    ("GLM", "glm_bucket"),
    ("ensemble", "ensemble_bucket"),
]:
    for b_label, b_key in [
        ("original", "original_bucket"),
        ("ensemble", "ensemble_bucket"),
        ("BEST-3", "best3_bucket"),
        ("Opus", "opus_bucket"),
        ("K2.6", "k26_bucket"),
        ("GLM", "glm_bucket"),
    ]:
        if a_key == b_key:
            continue
        k, n = cohens_kappa(kcol(universe, a_key), kcol(universe, b_key))
        if k is None:
            continue
        if (a_label, b_label) in [
            ("BEST-3", "original"), ("BEST-3", "ensemble"), ("BEST-3", "Opus"), ("BEST-3", "K2.6"), ("BEST-3", "GLM"),
            ("Opus", "K2.6"), ("Opus", "GLM"), ("K2.6", "GLM"),
            ("Opus", "ensemble"),
        ]:
            print(f"  {a_label} x {b_label}: kappa={k:.4f}  n={n}")

# --- Pairwise agreement rate for the three best-3 members ---
print("\n--- Pairwise bucket match rates (BEST-3 members) ---")
for a_label, a_key in [("Opus","opus_bucket"), ("K2.6","k26_bucket"), ("GLM","glm_bucket")]:
    for b_label, b_key in [("Opus","opus_bucket"), ("K2.6","k26_bucket"), ("GLM","glm_bucket")]:
        if a_key >= b_key: continue
        match = sum(1 for r in universe if r[a_key] == r[b_key] and r[a_key] is not None)
        valid = sum(1 for r in universe if r[a_key] is not None and r[b_key] is not None)
        print(f"  {a_label} x {b_label}: {match}/{valid} = {match/valid*100:.2f}%")

# --- Ensemble resolution breakdown ---
res_counter = Counter(r["best3_resolution"] for r in universe)
print("\n--- BEST-3 resolution breakdown ---")
for k, v in res_counter.items():
    print(f"  {k}: {v}")

# --- Rows where BEST-3 and current ensemble disagree ---
disagree = [r for r in universe if r["best3_bucket"] != r["ensemble_bucket"]]
print(f"\n--- BEST-3 vs ensemble bucket disagreements: {len(disagree)}/{len(universe)} ---")
disagree_conf = Counter((r["ensemble_bucket"], r["best3_bucket"]) for r in disagree)
for (a, b), n in sorted(disagree_conf.items(), key=lambda x: -x[1]):
    print(f"  ensemble={a} -> best3={b}: {n}")

# Save merged best-3 universe
out = {
    "n_universe": len(universe),
    "resolution_breakdown": dict(res_counter),
    "rows": universe,
}
with open(HERE / "best3_ensemble_results.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"\nwrote best3_ensemble_results.json ({len(universe)} rows)")
