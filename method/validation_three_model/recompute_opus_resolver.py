#!/usr/bin/env python3
"""Reanalysis under the hypothetical where the ORIGINAL pipeline is
K2.6 + GLM-5.1 + DeepSeek V3.2 with Opus 4.7 as the consensus resolver.

Uses only existing data (no API calls):
  - method/validation_three_model/{kimi,glm,deepseek}_raw_results.json (three coders)
  - method/validation_four_coder_full/fourth_coder_full_merged.json    (Opus 4.7 per-case)

Resolution rule:
  - Ensemble unanimous (3/3)        → adopt unanimous bucket
  - Ensemble majority (2/1) or split (1/1/1) → adopt Opus 4.7 bucket

Outputs:
  - opus_resolver_report.md
  - opus_resolver_results.json
"""
from __future__ import annotations
import io, json, math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
TM = HERE
FC = ROOT / "validation_four_coder_full"

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


def cohen_kappa(a, b):
    assert len(a) == len(b)
    n = len(a)
    if n == 0: return None
    labels = sorted(set(a) | set(b))
    idx = {l: i for i, l in enumerate(labels)}
    k = len(labels)
    mat = [[0]*k for _ in range(k)]
    for x, y in zip(a, b):
        mat[idx[x]][idx[y]] += 1
    rs = [sum(r) for r in mat]
    cs = [sum(mat[r][c] for r in range(k)) for c in range(k)]
    obs = sum(mat[i][i] for i in range(k)) / n
    exp = sum((rs[i]*cs[i])/(n*n) for i in range(k))
    if exp >= 1.0:
        return 1.0 if obs >= 1.0 else 0.0
    return round((obs - exp) / (1 - exp), 4)


def fleiss_kappa_three(triplets):
    if not triplets: return None
    cats = sorted({l for t in triplets for l in t})
    idx = {c: i for i, c in enumerate(cats)}
    N = len(triplets); r = 3
    nij = [[0]*len(cats) for _ in range(N)]
    for i, t in enumerate(triplets):
        for l in t:
            nij[i][idx[l]] += 1
    Pi = [sum(nij[i][j]*(nij[i][j]-1) for j in range(len(cats))) / (r*(r-1)) for i in range(N)]
    Pbar = sum(Pi)/N
    pj = [sum(nij[i][j] for i in range(N))/(N*r) for j in range(len(cats))]
    Pe = sum(p*p for p in pj)
    if 1 - Pe == 0:
        return 1.0 if Pbar >= 1.0 else 0.0
    return round((Pbar - Pe)/(1 - Pe), 4)


def pct(a, b):
    if not b: return None
    return round(100.0*a/b, 2)


def chi2_2x2(a, b, c, d):
    n = a+b+c+d
    if n == 0: return None, None
    r1, r2 = a+b, c+d
    c1, c2 = a+c, b+d
    if min(r1, r2, c1, c2) == 0: return None, None
    exp = [[r1*c1/n, r1*c2/n], [r2*c1/n, r2*c2/n]]
    obs = [[a,b],[c,d]]
    chi = 0.0
    for i in range(2):
        for j in range(2):
            diff = abs(obs[i][j] - exp[i][j]) - 0.5
            if diff < 0: diff = 0
            chi += diff*diff/exp[i][j]
    p = math.erfc(math.sqrt(chi/2.0)) if chi >= 0 else None
    return round(chi, 4), p


def diff_ci(ap, an, bp, bn, z=1.96):
    if an == 0 or bn == 0: return None
    p1, p2 = ap/an, bp/bn
    se = math.sqrt(p1*(1-p1)/an + p2*(1-p2)/bn)
    d = p1 - p2
    return {"diff": round(d,4), "ci95_low": round(d-z*se,4),
            "ci95_high": round(d+z*se,4), "se": round(se,4)}


def cramers_v(chi2, n, min_dim):
    """Cramér's V for an r×c table."""
    if n == 0 or min_dim <= 0: return None
    return round(math.sqrt(chi2 / (n * min_dim)), 4)


def chi2_rxc(table):
    """General chi-square for r×c table (list of lists). Returns (chi2, df)."""
    r = len(table); c = len(table[0]) if r else 0
    if r == 0 or c == 0: return 0.0, 0
    rs = [sum(row) for row in table]
    cs = [sum(table[i][j] for i in range(r)) for j in range(c)]
    n = sum(rs)
    if n == 0: return 0.0, 0
    chi = 0.0
    for i in range(r):
        for j in range(c):
            e = rs[i]*cs[j]/n
            if e > 0:
                chi += (table[i][j] - e)**2 / e
    df = (r-1)*(c-1)
    return round(chi, 4), df


def chi2_p(chi, df):
    """P-value via series for chi-square with df>=1. Uses math.gamma."""
    if chi <= 0 or df < 1: return 1.0
    # Regularized lower incomplete gamma: P(df/2, chi/2)
    # Use series expansion: P(a,x) = x^a e^-x / Γ(a+1) * Σ x^n / (a+1)(a+2)...(a+n)
    a = df/2.0
    x = chi/2.0
    if x == 0: return 1.0
    # Series form (converges for x < a+1)
    try:
        term = 1.0/a
        s = term
        for n in range(1, 1000):
            term *= x / (a + n)
            s += term
            if abs(term) < 1e-12*abs(s):
                break
        lower = s * math.exp(-x + a*math.log(x) - math.lgamma(a))
        return max(0.0, min(1.0, 1.0 - lower))
    except (ValueError, OverflowError):
        return 0.0


# ----- Load data
kimi = load(TM / "kimi_raw_results.json")
glm  = load(TM / "glm_raw_results.json")
ds   = load(TM / "deepseek_raw_results.json")
fc_merged = load(FC / "fourth_coder_full_merged.json")
fc_rows = fc_merged["rows"]

# Index by source_file
def by_sf(recs):
    return {r["source_file"]: r for r in recs if r.get("ok") and r.get("classification")}

k_by = by_sf(kimi); g_by = by_sf(glm); d_by = by_sf(ds)
fc_by = {r["source_file"]: r for r in fc_rows}

# Intersection universe: all three models parseable AND fourth coder present
all_sf = set(k_by) & set(g_by) & set(d_by) & set(fc_by)
print(f"Universe: |intersection-with-fourth| = {len(all_sf)}")
print(f"  kimi={len(k_by)} glm={len(g_by)} deepseek={len(d_by)} fourth={len(fc_by)}")

# Build rows
rows = []
for sf in sorted(all_sf):
    ka = k_by[sf]["classification"]; ga = g_by[sf]["classification"]; da = d_by[sf]["classification"]
    fcr = fc_by[sf]
    k_fam = ka.get("pleading_failure_family", "UNKNOWN")
    g_fam = ga.get("pleading_failure_family", "UNKNOWN")
    d_fam = da.get("pleading_failure_family", "UNKNOWN")
    k_b, g_b, d_b = map(family_bucket, (k_fam, g_fam, d_fam))
    triplet = [k_b, g_b, d_b]
    cnt = Counter(triplet).most_common()
    if len(cnt) == 1:
        ens_bucket, resolution = cnt[0][0], "unanimous"
    elif cnt[0][1] == 2:
        ens_bucket, resolution = cnt[0][0], "majority"
    else:
        ens_bucket, resolution = None, "split"

    fam_cnt = Counter([k_fam, g_fam, d_fam]).most_common()
    ens_family = fam_cnt[0][0] if fam_cnt[0][1] >= 2 else None

    fourth_b = fcr.get("fourth_bucket") or "OTHER"
    fourth_f = fcr.get("fourth_family") or "UNKNOWN"

    # Opus-as-resolver bucket/family
    if resolution == "unanimous":
        opus_b = ens_bucket
        opus_f = ens_family  # unanimous at bucket, family may still differ; keep majority family when exists, else fourth
        if opus_f is None:
            opus_f = fourth_f
    else:
        opus_b = fourth_b
        opus_f = fourth_f

    # Majority-only resolver (existing ensemble rule): split → OTHER
    maj_b = ens_bucket if ens_bucket else "OTHER"
    maj_f = ens_family if ens_family else "UNRESOLVED"

    # Original (K2.5 + GLM-5.1)
    orig_fam = k_by[sf]["original_family"]
    orig_b = family_bucket(orig_fam)

    rows.append({
        "source_file": sf,
        "representation": k_by[sf].get("representation"),
        "orig_family": orig_fam, "orig_bucket": orig_b,
        "k_bucket": k_b, "g_bucket": g_b, "d_bucket": d_b,
        "k_family": k_fam, "g_family": g_fam, "d_family": d_fam,
        "fourth_bucket": fourth_b, "fourth_family": fourth_f,
        "maj_bucket": maj_b, "maj_family": maj_f,
        "opus_bucket": opus_b, "opus_family": opus_f,
        "resolution": resolution,
    })

n = len(rows)
res_cnt = Counter(r["resolution"] for r in rows)
print(f"Rows: {n}. Resolutions: {dict(res_cnt)}")

# Count how many non-unanimous cases Opus would actually flip
nonunan = [r for r in rows if r["resolution"] != "unanimous"]
flips_from_maj = sum(1 for r in nonunan if r["maj_bucket"] != r["opus_bucket"])
opus_agrees_maj = sum(1 for r in nonunan if r["maj_bucket"] == r["opus_bucket"] and r["resolution"] == "majority")
print(f"Non-unanimous cases: {len(nonunan)}. Opus disagrees with majority-rule on {flips_from_maj}.")

# Fleiss' kappa across the three coders (unchanged by resolver choice)
triplets = [(r["k_bucket"], r["g_bucket"], r["d_bucket"]) for r in rows]
fleiss_b = fleiss_kappa_three(triplets)
fam_triplets = [(r["k_family"], r["g_family"], r["d_family"]) for r in rows]
fleiss_f = fleiss_kappa_three(fam_triplets)

# --- TRANSLATION gap replays
pro_se = [r for r in rows if r["representation"] == "PRO_SE"]
repres = [r for r in rows if r["representation"] == "REPRESENTED"]
n_ps, n_rp = len(pro_se), len(repres)

def gap_for(key):
    ps_t = sum(1 for r in pro_se if r[key] == TRANSLATION)
    rp_t = sum(1 for r in repres if r[key] == TRANSLATION)
    chi, p = chi2_2x2(ps_t, n_ps - ps_t, rp_t, n_rp - rp_t)
    return {
        "pro_se_pct": pct(ps_t, n_ps),
        "repres_pct": pct(rp_t, n_rp),
        "gap_pp": round(pct(ps_t, n_ps) - pct(rp_t, n_rp), 2),
        "chi2_1df": chi, "p": p,
        "diff_ci": diff_ci(ps_t, n_ps, rp_t, n_rp),
        "pro_se_n_trans": ps_t, "pro_se_n": n_ps,
        "repres_n_trans": rp_t, "repres_n": n_rp,
    }

replay = {
    "original": gap_for("orig_bucket"),
    "majority_ensemble": gap_for("maj_bucket"),
    "opus_resolved": gap_for("opus_bucket"),
    "opus_alone_fourth": gap_for("fourth_bucket"),
    "kimi_solo": gap_for("k_bucket"),
    "glm_solo": gap_for("g_bucket"),
    "deepseek_solo": gap_for("d_bucket"),
}

# --- 9-cell Cramér's V on representation × bucket (collapsed to TRANSLATION/PG/OTHER or similar?)
# Original note reports χ²(8) = 33.23, Cramér's V = 0.22 on 9-cell. Let's replicate on mechanism-family atomic.
# 9 cells means 3×3 or 2×4+ .  Footnote 48 says "collapsed contingency χ²(8)", meaning df=8 → (r-1)(c-1)=8 → e.g., 3×5 or 5×3
# Likely representation (2) × family (5) = df 4, or pro_se×family with multiple strata.
# The note says "TRANSLATION-family share 48.3% vs 17.9%" with chi2(8) = 33.23. This is the full family taxonomy (9 categories) × 2 representations = df 8. Wait, (2-1)*(9-1)=8. Makes sense.
# Let's compute for each coding, family × representation table
FAMILIES_ORDER = [TRANSLATION, PROCEDURAL_GATEWAY, "ELEMENT_MISMATCH", "CAUSAL_LINK",
                  "FACTUAL_DETAIL", "MIXED", "UNCLEAR", "NO_FAILURE_PLAINTIFF_WIN",
                  "NO_FAILURE_DEFENDANT_WIN", "MERITS_EVIDENCE"]

def fam_table(key):
    """Collapse family; returns table rows=[pro_se,repres], cols=families_observed, chi2/df/V."""
    fams_seen = sorted({r[key] for r in rows if r[key] and r[key] != "UNRESOLVED"})
    tbl = []
    for grp in (pro_se, repres):
        row = []
        for fm in fams_seen:
            row.append(sum(1 for r in grp if r[key] == fm))
        tbl.append(row)
    chi, df = chi2_rxc(tbl)
    ntot = sum(sum(r) for r in tbl)
    V = cramers_v(chi, ntot, min(len(tbl)-1, len(fams_seen)-1))
    return {"fams": fams_seen, "table": tbl, "chi2": chi, "df": df,
            "p": chi2_p(chi, df), "n": ntot, "cramers_v": V}

fam_analysis = {
    "original": fam_table("orig_family"),
    "majority_ensemble": fam_table("maj_family"),
    "opus_resolved": fam_table("opus_family"),
    "fourth_alone": fam_table("fourth_family"),
}

# --- Kappa matrix: compare each coding to each other
def kappa_pair(key_a, key_b):
    return cohen_kappa([r[key_a] for r in rows], [r[key_b] for r in rows])

kappa_grid = {}
coding_keys = ["orig_bucket", "maj_bucket", "opus_bucket", "fourth_bucket",
               "k_bucket", "g_bucket", "d_bucket"]
for a in coding_keys:
    for b in coding_keys:
        if a < b:
            kappa_grid[f"{a} vs {b}"] = kappa_pair(a, b)

# Per-model vs opus-resolved
per_model_vs_opus = {}
for m, key in [("kimi", "k_bucket"), ("glm", "g_bucket"), ("deepseek", "d_bucket"),
               ("original", "orig_bucket"), ("majority", "maj_bucket"),
               ("fourth_alone", "fourth_bucket")]:
    a = [r[key] for r in rows]; b = [r["opus_bucket"] for r in rows]
    match = sum(1 for x, y in zip(a, b) if x == y)
    per_model_vs_opus[m] = {
        "bucket_match_pct": pct(match, n),
        "bucket_kappa": cohen_kappa(a, b),
    }

# --- PROCEDURAL_GATEWAY replay
def pg_for(key):
    ps_g = sum(1 for r in pro_se if r[key] == PROCEDURAL_GATEWAY)
    rp_g = sum(1 for r in repres if r[key] == PROCEDURAL_GATEWAY)
    chi, p = chi2_2x2(ps_g, n_ps - ps_g, rp_g, n_rp - rp_g)
    return {"pro_se_pct": pct(ps_g, n_ps), "repres_pct": pct(rp_g, n_rp),
            "gap_pp": round(pct(ps_g, n_ps) - pct(rp_g, n_rp), 2),
            "chi2_1df": chi, "p": p}

pg_analysis = {
    "original": pg_for("orig_bucket"),
    "majority_ensemble": pg_for("maj_bucket"),
    "opus_resolved": pg_for("opus_bucket"),
    "fourth_alone": pg_for("fourth_bucket"),
}

# --- Confusion matrix: original vs opus_resolved
confusion = {o: {e: 0 for e in BUCKETS} for o in BUCKETS}
for r in rows:
    confusion[r["orig_bucket"]][r["opus_bucket"]] += 1

# Majority vs opus_resolved (where they differ)
maj_vs_opus_conf = {o: {e: 0 for e in BUCKETS} for o in BUCKETS}
for r in rows:
    maj_vs_opus_conf[r["maj_bucket"]][r["opus_bucket"]] += 1

# --- 150-case stratified audit under new framing
# Under new framing: K2.6 IS a member of the original pipeline, so K2.6-vs-original (κ=0.6264) is
# no longer an independent external validation. Instead we can compute K2.6-alone vs opus_resolved
# on the stratified-sample subset (the 150 cases), if we have overlap.
agr = load(ROOT / "validation_kimi_k2_6" / "agreement_results.json")
# The 150-case sample's source_files aren't in the summary agr; we need them for overlap analysis.
# Try to load the raw K2.6 audit results.
k26_audit_raw_path = ROOT / "validation_kimi_k2_6" / "kimi_k2_6_raw_results.json"
audit_overlap = None
if k26_audit_raw_path.exists():
    audit_raw = load(k26_audit_raw_path)
    # Each record has source_file + classification
    by_sf_a = {r["source_file"]: r for r in audit_raw if r.get("ok") and r.get("classification")}
    stratified_sfs = set(by_sf_a.keys())
    # Overlap with our Opus-resolved universe
    shared = stratified_sfs & all_sf
    if shared:
        a_b, o_b = [], []
        a_f, o_f = [], []
        for sf in sorted(shared):
            a_b.append(family_bucket(by_sf_a[sf]["classification"].get("pleading_failure_family", "UNKNOWN")))
            a_f.append(by_sf_a[sf]["classification"].get("pleading_failure_family", "UNKNOWN"))
        # opus labels for those
        row_by_sf = {r["source_file"]: r for r in rows}
        for sf in sorted(shared):
            o_b.append(row_by_sf[sf]["opus_bucket"])
            o_f.append(row_by_sf[sf]["opus_family"])
        match_b = sum(1 for x, y in zip(a_b, o_b) if x == y)
        match_f = sum(1 for x, y in zip(a_f, o_f) if x == y)
        audit_overlap = {
            "n_overlap": len(shared),
            "bucket_match_pct": pct(match_b, len(shared)),
            "bucket_kappa": cohen_kappa(a_b, o_b),
            "family_match_pct": pct(match_f, len(shared)),
            "family_kappa": cohen_kappa(a_f, o_f),
        }

# --- Emit results
out = {
    "n_universe": n,
    "resolution_distribution": dict(res_cnt),
    "nonunanimous_cases": len(nonunan),
    "opus_flips_vs_majority": flips_from_maj,
    "fleiss_three_coders": {"bucket": fleiss_b, "family": fleiss_f},
    "translation_gap_replay": replay,
    "family_table_analysis": fam_analysis,
    "procedural_gateway_replay": pg_analysis,
    "kappa_pairwise_coding": kappa_grid,
    "per_coder_vs_opus_resolver": per_model_vs_opus,
    "confusion_original_vs_opus_resolved": confusion,
    "confusion_majority_vs_opus_resolved": maj_vs_opus_conf,
    "audit_150_overlap_vs_opus_resolved": audit_overlap,
    "n_pro_se": n_ps,
    "n_represented": n_rp,
}

RESULTS = HERE / "opus_resolver_results.json"
REPORT  = HERE / "opus_resolver_report.md"
with io.open(RESULTS, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False, default=str)

# --- Build markdown report
L = []
L.append("# Reanalysis: K2.6 + GLM-5.1 + DeepSeek V3.2 with Opus 4.7 as the immediate consensus resolver\n")
L.append(f"Universe size: **{n}** cases (same 668 as the three-model ensemble report; the 8 unparseable cases remain outside this resolver universe because Opus was only given cases the three coders could classify).\n")
L.append(f"Resolution distribution among the three coders: **unanimous {res_cnt.get('unanimous',0)} / majority {res_cnt.get('majority',0)} / split {res_cnt.get('split',0)}**.\n")
L.append(f"Non-unanimous cases: **{len(nonunan)}**. Of these, Opus 4.7's bucket diverges from the majority-vote rule on **{flips_from_maj}** ({pct(flips_from_maj, len(nonunan))}%).\n")
L.append("")

L.append("## Headline — TRANSLATION gap under each coding rule\n")
L.append("| Coding | Pro se TRANSLATION % | Represented TRANSLATION % | Gap (pp) | χ²(1) | p | 95% CI on gap |")
L.append("| --- | --- | --- | --- | --- | --- | --- |")
for lbl, key in [("Original (K2.5 + GLM-5.1)", "original"),
                 ("Majority-vote ensemble (split→OTHER)", "majority_ensemble"),
                 ("**Opus 4.7 as resolver (K2.6+GLM+DS unanimous, else Opus)**", "opus_resolved"),
                 ("Opus 4.7 alone (fourth coder)", "opus_alone_fourth"),
                 ("Kimi K2.6 solo", "kimi_solo"),
                 ("GLM-5.1 solo", "glm_solo"),
                 ("DeepSeek V3.2 solo", "deepseek_solo")]:
    g = replay[key]
    ci = g["diff_ci"] or {}
    ci_lo = round(ci.get("ci95_low",0)*100,2); ci_hi = round(ci.get("ci95_high",0)*100,2)
    L.append(f"| {lbl} | {g['pro_se_pct']}% ({g['pro_se_n_trans']}/{g['pro_se_n']}) | {g['repres_pct']}% ({g['repres_n_trans']}/{g['repres_n']}) | {g['gap_pp']} | {g['chi2_1df']} | {g['p']:.2e} | [{ci_lo}, {ci_hi}] |")
L.append("")
L.append(f"Pro se sample n = {n_ps}; represented sample n = {n_rp}.\n")

L.append("## Family-level contingency (representation × mechanism family)\n")
L.append("| Coding | χ² | df | p | Cramér's V | Families observed |")
L.append("| --- | --- | --- | --- | --- | --- |")
for lbl, key in [("Original (K2.5 + GLM-5.1)", "original"),
                 ("Majority-vote ensemble", "majority_ensemble"),
                 ("**Opus 4.7 as resolver**", "opus_resolved"),
                 ("Opus 4.7 alone", "fourth_alone")]:
    a = fam_analysis[key]
    L.append(f"| {lbl} | {a['chi2']} | {a['df']} | {a['p']:.2e} | {a['cramers_v']} | {len(a['fams'])} |")
L.append("")
L.append("Footnote 48 currently reports χ²(8) = 33.23, p = 5.6 × 10⁻⁵, Cramér's V = 0.22 on the original K2.5+GLM coding of the full 676-case universe. The values above operate on the 668-case subset covered by all four coders.\n")

L.append("## Rater reliability — Fleiss' κ across the three primary coders\n")
L.append(f"- Bucket-level Fleiss κ (K2.6, GLM-5.1, DeepSeek V3.2): **{fleiss_b}**")
L.append(f"- Family-level Fleiss κ: {fleiss_f}")
L.append("")
L.append("These numbers are identical to the current ensemble report because they describe the three coders' mutual reliability, independent of how ties are resolved.\n")

L.append("## Pairwise κ across all coding variants (bucket)\n")
L.append("| Comparison | Cohen's κ |")
L.append("| --- | --- |")
for k, v in sorted(kappa_grid.items()):
    L.append(f"| {k} | {v} |")
L.append("")

L.append("## Each coder vs. the Opus-4.7 resolver (bucket)\n")
L.append("| Coder | Bucket match % | Cohen's κ vs. Opus-resolved |")
L.append("| --- | --- | --- |")
for m, v in per_model_vs_opus.items():
    L.append(f"| {m} | {v['bucket_match_pct']}% | {v['bucket_kappa']} |")
L.append("")

L.append("## Confusion matrices\n")
L.append("### Original (K2.5+GLM) vs. Opus-resolved\n")
L.append("| orig \\ opus | " + " | ".join(BUCKETS) + " |")
L.append("| --- |" + " --- |"*len(BUCKETS))
for ob in BUCKETS:
    row = f"| {ob} | " + " | ".join(str(confusion[ob][eb]) for eb in BUCKETS) + " |"
    L.append(row)
L.append("")

L.append("### Majority-vote ensemble vs. Opus-resolved\n")
L.append("| maj \\ opus | " + " | ".join(BUCKETS) + " |")
L.append("| --- |" + " --- |"*len(BUCKETS))
for ob in BUCKETS:
    row = f"| {ob} | " + " | ".join(str(maj_vs_opus_conf[ob][eb]) for eb in BUCKETS) + " |"
    L.append(row)
L.append("")

L.append("## PROCEDURAL_GATEWAY replay\n")
L.append("| Coding | Pro se PG % | Represented PG % | Gap (pp) | χ²(1) | p |")
L.append("| --- | --- | --- | --- | --- | --- |")
for lbl, key in [("Original", "original"), ("Majority ensemble", "majority_ensemble"),
                 ("**Opus 4.7 as resolver**", "opus_resolved"),
                 ("Opus 4.7 alone", "fourth_alone")]:
    g = pg_analysis[key]
    L.append(f"| {lbl} | {g['pro_se_pct']}% | {g['repres_pct']}% | {g['gap_pp']} | {g['chi2_1df']} | {g['p']:.3e} |")
L.append("")

L.append("## 150-case stratified audit — under new framing\n")
if audit_overlap:
    L.append("Under the current framing, K2.6 re-coded a stratified 150-case sample vs. K2.5+GLM → κ = 0.6264.\n")
    L.append("Under the new framing, K2.6 is already one of the three primary coders, so its 150-case re-code is no longer an *external* check. ")
    L.append("For reference, the same K2.6 labels compared against the **Opus-resolved** ensemble on the overlapping subset:\n")
    a = audit_overlap
    L.append(f"- Overlap with resolver universe: **{a['n_overlap']} cases**")
    L.append(f"- Bucket match: {a['bucket_match_pct']}%")
    L.append(f"- Bucket κ (K2.6 vs. Opus-resolved): **{a['bucket_kappa']}**")
    L.append(f"- Family match: {a['family_match_pct']}%")
    L.append(f"- Family κ: {a['family_kappa']}")
    L.append("")
    L.append("A high κ here reflects the self-consistency of K2.6 with a pipeline it is part of, not external validation.\n")
else:
    L.append("_(150-case audit overlap not recomputed — raw K2.6 audit file not found.)_\n")

L.append("## Summary of what changes\n")
or_ = replay["original"]; op_ = replay["opus_resolved"]; maj = replay["majority_ensemble"]
L.append("| Metric | Original (K2.5+GLM, n=676) | Majority ensemble (n=668) | **Opus 4.7 resolver (n=668)** |")
L.append("| --- | --- | --- | --- |")
L.append(f"| Pro se TRANSLATION % | 48.3% | {maj['pro_se_pct']}% | **{op_['pro_se_pct']}%** |")
L.append(f"| Represented TRANSLATION % | 17.9% | {maj['repres_pct']}% | **{op_['repres_pct']}%** |")
L.append(f"| Gap (pp) | 30.4 | {maj['gap_pp']} | **{op_['gap_pp']}** |")
L.append(f"| χ²(1) (2×2) | — | {maj['chi2_1df']} | **{op_['chi2_1df']}** |")
L.append(f"| p (2×2) | — | {maj['p']:.2e} | **{op_['p']:.2e}** |")
L.append(f"| χ²(family×representation) | 33.23 (df=8) | {fam_analysis['majority_ensemble']['chi2']} (df={fam_analysis['majority_ensemble']['df']}) | **{fam_analysis['opus_resolved']['chi2']} (df={fam_analysis['opus_resolved']['df']})** |")
L.append(f"| Cramér's V | 0.22 | {fam_analysis['majority_ensemble']['cramers_v']} | **{fam_analysis['opus_resolved']['cramers_v']}** |")
L.append(f"| Fleiss κ across three coders | — | 0.6292 | **{fleiss_b}** (same) |")
L.append(f"| Validation layer κ (vs. original) | — | 0.574 | κ vs K2.5+GLM: **{kappa_grid.get('opus_bucket vs orig_bucket')}** |")
L.append("")

with io.open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print(f"\nReport: {REPORT}")
print(f"Results: {RESULTS}")
