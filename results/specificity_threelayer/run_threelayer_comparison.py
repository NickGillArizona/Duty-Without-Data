"""Three-layer claim_specificity comparison (G2 decision evidence).

Deterministic joins and counts ONLY. No LLM classification anywhere. This script
adjudicates the 136 claim_specificity disagreement rows (82 code-vs-code + 54
SOL1-UNCLEAR) between:

  Layer 1 - recorded key / census codes  (db_claim_specificity)
  Layer 2 - SOL-1 blind re-read           (my_claim_specificity, SOL1_RECODES_MERGED)
  Layer 3 - blind THIRD read of disputes  (my_claim_specificity, SPEC_RECODES)

It reports, per disputed row, which layer the third read corroborates, and what the
field's adjudicated agreement would look like under majority vote. It does NOT make the
keep/caveat/cut call; that call is made elsewhere. This is exploratory evidence, not
relied on by the Note.

Modes
  --allow-partial : run on whatever third-read rows exist now; outputs are labeled
                    PARTIAL and written to *.PARTIAL.csv / *.PARTIAL.md.
  (default/final) : hard-fail unless the third-read covers all 136 disagreement rows,
                    OR covers (136 minus rows that are a persistent no-text opinion).
                    Writes the canonical THREELAYER_COMPARISON.csv / THREELAYER_SUMMARY.md.

Writes are batch-atomic (temp file then os.replace).
No network. ASCII only. Reads the external re-read inputs read-only; writes only into
this directory.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolved input paths. The re-read inputs are held outside this repository; the
# committed CSVs in this directory are the reproducible record of the comparison.
# ---------------------------------------------------------------------------
SPEC_DIR = Path(r"<external>/specificity_reread")
SPEC_TOPUP = SPEC_DIR / "SPEC_RECODES_WITH_TOPUP.csv"   # preferred at run time if present
SPEC_MAIN = SPEC_DIR / "SPEC_RECODES.csv"

SOL1_MERGED = Path(r"<external>/secondary_field_audit\RECODES_MERGED.csv")
KEY_CSV = Path(r"<external>/secondary_field_audit_key\audit_key.csv")

OUT_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Column names (verified against live file headers 2026-07-16)
# ---------------------------------------------------------------------------
COL_KEY_SPEC = "db_claim_specificity"       # layer 1 recorded key
COL_SOL1_SPEC = "my_claim_specificity"      # layer 2 SOL-1 re-read
COL_THIRD_SPEC = "my_claim_specificity"     # layer 3 third read
JOIN_COL = "sol1_ordinal"

# Expected constants (sanity cross-check; the universe is recomputed from data).
EXPECTED_DISAGREEMENTS = 136
EXPECTED_BASELINE_AGREE = 271
EXPECTED_BASELINE_DET = 407

# Markers / vocab.
NO_TEXT_MARKERS = {"UNRESOLVED_TEXT"}       # persistent no-text marker
UNCLEAR = "UNCLEAR"
NON_KEY_CODES = {"", "MISSING"}             # key values that carry no adjudicable class


def norm(v) -> str:
    return (v or "").strip().upper()


def read_dicts(path: Path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def load_layers():
    """Return (sol1 dict, key dict) keyed by int ordinal."""
    sol1 = {}
    for r in read_dicts(SOL1_MERGED):
        try:
            sol1[int(r[JOIN_COL])] = r
        except (KeyError, ValueError):
            continue
    key = {}
    for r in read_dicts(KEY_CSV):
        try:
            key[int(r[JOIN_COL])] = r
        except (KeyError, ValueError):
            continue
    return sol1, key


def load_third():
    """Return (dict keyed by int ordinal, path used, dup_count, stray_ordinals).

    Prefers SPEC_RECODES_WITH_TOPUP.csv if present. On duplicate ordinals within a
    file, keeps the row with the highest 'increment' if that column exists, else the
    last-appended row.
    """
    path = SPEC_TOPUP if SPEC_TOPUP.exists() else SPEC_MAIN
    rows = read_dicts(path)
    has_increment = bool(rows) and "increment" in rows[0]
    third = {}
    order = {}
    dup = 0
    for i, r in enumerate(rows):
        try:
            o = int(r[JOIN_COL])
        except (KeyError, ValueError):
            continue
        if o in third:
            dup += 1
            if has_increment:
                try:
                    prev = float(third[o].get("increment") or 0)
                    cur = float(r.get("increment") or 0)
                except ValueError:
                    prev, cur = 0.0, 1.0
                if cur >= prev:
                    third[o] = r
                    order[o] = i
            else:
                third[o] = r
                order[o] = i
        else:
            third[o] = r
            order[o] = i
    return third, path, dup, has_increment


def build_disagreements(sol1, key):
    """Recompute the disagreement universe from layer1 vs layer2.

    Returns (disagree_ordinals set, baseline_agree, baseline_det, indeterminate).
    A row is a disagreement when both codes are present (non-empty) and differ.
    'MISSING' is treated as a determinate literal key code (never equals a SOL-1 class),
    matching the recorded 271/407 baseline.
    """
    joined = sorted(set(sol1) & set(key))
    agree = det = indet = 0
    disagree = set()
    for o in joined:
        a = norm(sol1[o].get(COL_SOL1_SPEC))
        b = norm(key[o].get(COL_KEY_SPEC))
        if not a or not b:
            indet += 1
            continue
        det += 1
        if a == b:
            agree += 1
        else:
            disagree.add(o)
    return disagree, agree, det, indet


def adjudicate(o, sol1, key, third, persistent_notext, partial):
    """Return (row_dict, adjudication, disagreement_type)."""
    key_code = norm(key[o].get(COL_KEY_SPEC))
    sol1_code = norm(sol1[o].get(COL_SOL1_SPEC))
    dtype = "SOL1_UNCLEAR" if sol1_code == UNCLEAR else "CODE_VS_CODE"

    src = (sol1[o].get("source_file") or "").strip()
    third_code = ""
    third_obs = ""
    third_txt = ""

    if o in third:
        tr = third[o]
        third_code = norm(tr.get(COL_THIRD_SPEC))
        third_obs = norm(tr.get("observability"))
        third_txt = norm(tr.get("text_status"))
        if (tr.get("source_file") or "").strip():
            src = (tr.get("source_file") or "").strip()

        if third_txt in NO_TEXT_MARKERS or third_code == "":
            adj = "NO_TEXT"
        elif third_code == UNCLEAR:
            adj = "THIRD_UNCLEAR"
        elif key_code not in NON_KEY_CODES and third_code == key_code:
            adj = "KEY_CORROBORATED"
        elif sol1_code not in (UNCLEAR, "") and third_code == sol1_code:
            adj = "SOL1_CORROBORATED"
        else:
            adj = "NEITHER"
    else:
        # Not present in the third read.
        if o in persistent_notext:
            adj = "NO_TEXT"
            third_txt = norm(sol1[o].get("text_status"))  # persistent per SOL-1 layer
        else:
            adj = "NOT_YET_CODED"  # partial only; the final-mode gate forbids this

    row = {
        "sol1_ordinal": o,
        "source_file": src,
        "key_code": key_code,
        "sol1_code": sol1_code,
        "third_code": third_code,
        "third_observability": third_obs,
        "third_text_status": third_txt,
        "adjudication": adj,
        "disagreement_type": dtype,
    }
    return row, adj, dtype


def atomic_write_text(path: Path, text: str):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="ascii", newline="\n") as fh:
        fh.write(text)
    os.replace(tmp, path)


def atomic_write_csv(path: Path, fieldnames, rows):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="ascii", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    os.replace(tmp, path)


def pct(n, d):
    return f"{(100.0 * n / d):.1f}%" if d else "n/a"


def main():
    ap = argparse.ArgumentParser(description="Three-layer claim_specificity comparison (G2 evidence).")
    ap.add_argument("--allow-partial", action="store_true",
                    help="Run on whatever third-read rows exist now; label output PARTIAL.")
    args = ap.parse_args()
    partial = args.allow_partial

    for p in (SOL1_MERGED, KEY_CSV):
        if not p.exists():
            sys.stderr.write("FATAL: missing required input: %s\n" % p)
            return 2

    sol1, key = load_layers()
    third, spec_path, dup_count, has_increment = load_third()
    if not spec_path.exists():
        sys.stderr.write("FATAL: no third-read file found in %s\n" % SPEC_DIR)
        return 2

    disagree, base_agree, base_det, base_indet = build_disagreements(sol1, key)
    n_dis = len(disagree)

    # Persistent no-text: disagreement ordinals absent from the third read whose SOL-1
    # layer already marked the opinion no-text (text was never obtainable across reads).
    third_present = disagree & set(third)
    absent = disagree - set(third)
    persistent_notext = {o for o in absent
                         if norm(sol1[o].get("text_status")) in NO_TEXT_MARKERS}
    non_persistent_absent = absent - persistent_notext

    present_count = len(third_present)
    tolerance_lo = n_dis - len(persistent_notext)

    # Third-read rows that are not in the disagreement universe (should be none).
    stray = sorted(set(third) - disagree)

    # ---- final-mode gate --------------------------------------------------
    gate_ok = (present_count == n_dis) or (len(non_persistent_absent) == 0)
    if not partial and not gate_ok:
        sys.stderr.write(
            "FATAL (final mode): third-read coverage incomplete.\n"
            "  disagreement rows expected : %d\n"
            "  third-read rows present    : %d\n"
            "  absent rows                : %d\n"
            "  of which persistent no-text: %d\n"
            "  NON-persistent still missing: %d  -> %s\n"
            "  Tolerance rule: pass when present == %d, OR every absent ordinal is a\n"
            "  persistent no-text opinion (SOL-1 text_status in %s), i.e. present == %d.\n"
            "  Re-run with --allow-partial to produce PARTIAL outputs, or wait for the\n"
            "  plan-3.6 lane (and SPEC_RECODES_WITH_TOPUP.csv) to finish.\n"
            % (n_dis, present_count, len(absent), len(persistent_notext),
               len(non_persistent_absent), sorted(non_persistent_absent)[:25],
               n_dis, sorted(NO_TEXT_MARKERS), tolerance_lo))
        return 1

    # ---- adjudicate every disagreement row --------------------------------
    out_rows = []
    adj_counts = {}
    adj_by_type = {"CODE_VS_CODE": {}, "SOL1_UNCLEAR": {}}
    adj_by_class = {}
    obs_dist = {}
    for o in sorted(disagree):
        row, adj, dtype = adjudicate(o, sol1, key, third, persistent_notext, partial)
        out_rows.append(row)
        adj_counts[adj] = adj_counts.get(adj, 0) + 1
        adj_by_type.setdefault(dtype, {})
        adj_by_type[dtype][adj] = adj_by_type[dtype].get(adj, 0) + 1
        kc = row["key_code"] or "(blank)"
        adj_by_class.setdefault(kc, {})
        adj_by_class[kc][adj] = adj_by_class[kc].get(adj, 0) + 1
        if o in third_present and adj != "NO_TEXT":
            ob = row["third_observability"] or "(blank)"
            obs_dist[ob] = obs_dist.get(ob, 0) + 1

    # ---- majority-vote arithmetic -----------------------------------------
    k_all = adj_counts.get("KEY_CORROBORATED", 0)
    s_all = adj_counts.get("SOL1_CORROBORATED", 0)
    cvc = adj_by_type.get("CODE_VS_CODE", {})
    k_cvc = cvc.get("KEY_CORROBORATED", 0)
    s_cvc = cvc.get("SOL1_CORROBORATED", 0)

    # Branch (a): full universe (base_det determinate rows).
    a_num = base_agree + k_all
    a_den_full = base_det
    a_resolved_den = base_agree + k_all + s_all

    # Branch (b): code-vs-code only. Baseline excludes the SOL1_UNCLEAR rows.
    n_cvc = sum(cvc.values())
    b_baseline_den = base_agree + n_cvc            # 271 + 82 = 353
    b_num = base_agree + k_cvc
    b_resolved_den = base_agree + k_cvc + s_cvc

    label = "PARTIAL" if partial else "FINAL"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # ---- CSV --------------------------------------------------------------
    csv_name = "THREELAYER_COMPARISON.PARTIAL.csv" if partial else "THREELAYER_COMPARISON.csv"
    md_name = "THREELAYER_SUMMARY.PARTIAL.md" if partial else "THREELAYER_SUMMARY.md"
    fieldnames = ["sol1_ordinal", "source_file", "key_code", "sol1_code", "third_code",
                  "third_observability", "third_text_status", "adjudication",
                  "disagreement_type"]

    # ---- SUMMARY ----------------------------------------------------------
    L = []
    L.append("# SCREENING-ONLY (2026-07-16). Deterministic comparison; no model coding.")
    L.append("")
    L.append("Three-layer claim_specificity comparison -- G2 decision evidence.")
    L.append("Run mode: %s. Generated: %s." % (label, now))
    if partial:
        L.append("")
        L.append("**PARTIAL RUN** -- the plan-3.6 third-read lane is still in progress. "
                 "Third read covers %d of %d disagreement rows (%s). Counts below are "
                 "provisional and will change as more rows are coded. NOT the G2 evidence "
                 "of record." % (present_count, n_dis, pct(present_count, n_dis)))
    L.append("")
    L.append("## Inputs")
    L.append("")
    L.append("- Layer 1 recorded key : %s (col %s)" % (KEY_CSV, COL_KEY_SPEC))
    L.append("- Layer 2 re-read      : %s (col %s)" % (SOL1_MERGED, COL_SOL1_SPEC))
    L.append("- Layer 3 third read   : %s (col %s)" % (spec_path, COL_THIRD_SPEC))
    L.append("- Join column          : %s" % JOIN_COL)
    if dup_count:
        L.append("- Note: %d duplicate third-read ordinal(s) collapsed (%s)."
                 % (dup_count, "max increment" if has_increment else "last row wins"))
    if stray:
        L.append("- WARNING: %d third-read ordinal(s) not in the disagreement universe: %s"
                 % (len(stray), stray[:25]))
    L.append("")
    L.append("## Disagreement universe (recomputed from Layer 1 vs Layer 2)")
    L.append("")
    L.append("- Joined rows                : %d" % (len(set(sol1) & set(key))))
    L.append("- Determinate (both coded)   : %d" % base_det)
    L.append("- Baseline agreement (key=SOL1): %d/%d = %s"
             % (base_agree, base_det, pct(base_agree, base_det)))
    L.append("- Indeterminate (one blank)  : %d" % base_indet)
    L.append("- Disagreement rows          : %d" % n_dis)
    L.append("    - CODE_VS_CODE           : %d" % sum(adj_by_type.get("CODE_VS_CODE", {}).values()))
    L.append("    - SOL1_UNCLEAR           : %d" % sum(adj_by_type.get("SOL1_UNCLEAR", {}).values()))
    sanity = "OK" if (n_dis == EXPECTED_DISAGREEMENTS and base_agree == EXPECTED_BASELINE_AGREE
                      and base_det == EXPECTED_BASELINE_DET) else "MISMATCH vs expected 271/407/136"
    L.append("- Cross-check vs expected 271/407/136: %s" % sanity)
    L.append("")
    L.append("## Third-read coverage")
    L.append("")
    L.append("- Present in third read      : %d/%d (%s)"
             % (present_count, n_dis, pct(present_count, n_dis)))
    L.append("- Absent                     : %d" % len(absent))
    L.append("- Absent & persistent no-text: %d" % len(persistent_notext))
    L.append("- Absent & not-yet-coded     : %d" % len(non_persistent_absent))
    L.append("- Tolerance rule (final mode): pass when present == %d, OR every absent "
             "ordinal is a persistent no-text opinion (SOL-1 text_status in %s), "
             "i.e. present == %d." % (n_dis, sorted(NO_TEXT_MARKERS), tolerance_lo))
    L.append("")
    L.append("## Adjudication counts -- overall")
    L.append("")
    L.append("| adjudication | n |")
    L.append("|---|---|")
    for kk in ["KEY_CORROBORATED", "SOL1_CORROBORATED", "NEITHER", "THIRD_UNCLEAR",
               "NO_TEXT", "NOT_YET_CODED"]:
        if adj_counts.get(kk, 0) or kk in ("KEY_CORROBORATED", "SOL1_CORROBORATED", "NEITHER", "THIRD_UNCLEAR"):
            L.append("| %s | %d |" % (kk, adj_counts.get(kk, 0)))
    L.append("| TOTAL | %d |" % n_dis)
    L.append("")
    L.append("## Adjudication counts -- by disagreement_type")
    L.append("")
    for dtype in ("CODE_VS_CODE", "SOL1_UNCLEAR"):
        d = adj_by_type.get(dtype, {})
        tot = sum(d.values())
        L.append("### %s (n=%d)" % (dtype, tot))
        L.append("")
        L.append("| adjudication | n |")
        L.append("|---|---|")
        for kk in ["KEY_CORROBORATED", "SOL1_CORROBORATED", "NEITHER", "THIRD_UNCLEAR",
                   "NO_TEXT", "NOT_YET_CODED"]:
            if d.get(kk, 0):
                L.append("| %s | %d |" % (kk, d[kk]))
        L.append("")
    L.append("## Adjudication counts -- by specificity class (recorded key code)")
    L.append("")
    L.append("| key_code | KEY_CORR | SOL1_CORR | NEITHER | THIRD_UNCLEAR | NO_TEXT | NOT_YET | total |")
    L.append("|---|---|---|---|---|---|---|---|")
    for kc in sorted(adj_by_class):
        d = adj_by_class[kc]
        L.append("| %s | %d | %d | %d | %d | %d | %d | %d |" % (
            kc, d.get("KEY_CORROBORATED", 0), d.get("SOL1_CORROBORATED", 0),
            d.get("NEITHER", 0), d.get("THIRD_UNCLEAR", 0), d.get("NO_TEXT", 0),
            d.get("NOT_YET_CODED", 0), sum(d.values())))
    L.append("")
    L.append("## Third-read observability distribution (coded rows only)")
    L.append("")
    L.append("| observability | n |")
    L.append("|---|---|")
    for ob in sorted(obs_dist):
        L.append("| %s | %d |" % (ob, obs_dist[ob]))
    if not obs_dist:
        L.append("| (none coded yet) | 0 |")
    L.append("")
    L.append("## Two-branch adjudicated field agreement")
    L.append("")
    L.append("Majority vote = 2 of 3 layers (recorded key, SOL-1, third read). A "
             "disagreement row is scored KEY_CORROBORATED when the independent third "
             "read matches the recorded key (key + third = majority), which *confirms* "
             "the recorded key value for that row. SOL1_CORROBORATED overturns the key. "
             "NEITHER / THIRD_UNCLEAR / NO_TEXT%s leave the row unresolved."
             % (" / NOT_YET_CODED" if partial else ""))
    L.append("")
    L.append("### (a) Full universe -- recorded-key agreement under majority-vote adjudication")
    L.append("")
    L.append("Start from the baseline recorded-key vs SOL-1 agreement, then add the "
             "disagreement rows the third read resolves in the key's favor:")
    L.append("")
    L.append("- Baseline agreement                : %d / %d = %s"
             % (base_agree, base_det, pct(base_agree, base_det)))
    L.append("- + KEY_CORROBORATED (all types)    : + %d" % k_all)
    L.append("- Adjudicated key-agreement (num)   : %d + %d = %d" % (base_agree, k_all, a_num))
    L.append("- Over full determinate universe    : %d / %d = %s"
             % (a_num, a_den_full, pct(a_num, a_den_full)))
    L.append("  (unresolved rows -- SOL1_CORROBORATED=%d, NEITHER=%d, THIRD_UNCLEAR=%d, "
             "NO_TEXT=%d%s -- counted as non-agreement)"
             % (s_all, adj_counts.get("NEITHER", 0), adj_counts.get("THIRD_UNCLEAR", 0),
                adj_counts.get("NO_TEXT", 0),
                (", NOT_YET_CODED=%d" % adj_counts.get("NOT_YET_CODED", 0)) if partial else ""))
    L.append("- Resolved-rows-only rate           : %d / %d = %s"
             % (a_num, a_resolved_den, pct(a_num, a_resolved_den)))
    L.append("  (denominator = agreements + KEY_CORROBORATED + SOL1_CORROBORATED)")
    L.append("")
    L.append("### (b) Code-vs-code disputes only (SOL1_UNCLEAR rows excluded)")
    L.append("")
    L.append("- Baseline agreement (excl. SOL1_UNCLEAR): %d / %d = %s"
             % (base_agree, b_baseline_den, pct(base_agree, b_baseline_den)))
    L.append("- + KEY_CORROBORATED (code-vs-code)  : + %d" % k_cvc)
    L.append("- Adjudicated key-agreement (num)   : %d + %d = %d" % (base_agree, k_cvc, b_num))
    L.append("- Over code-vs-code universe        : %d / %d = %s"
             % (b_num, b_baseline_den, pct(b_num, b_baseline_den)))
    L.append("- Resolved-rows-only rate           : %d / %d = %s"
             % (b_num, b_resolved_den, pct(b_num, b_resolved_den)))
    L.append("  (SOL1_CORROBORATED code-vs-code = %d, NEITHER=%d, THIRD_UNCLEAR=%d)"
             % (s_cvc, cvc.get("NEITHER", 0), cvc.get("THIRD_UNCLEAR", 0)))
    L.append("")
    if partial:
        L.append("_Branch arithmetic is PARTIAL: %d of %d disagreement rows still lack a "
                 "third-read code and are held out of KEY_CORROBORATED/SOL1_CORROBORATED._"
                 % (len(non_persistent_absent), n_dis))
        L.append("")
    L.append("---")
    L.append("")
    L.append("G2 (keep / caveat / cut) is an AUTHOR decision; this memo is evidence only.")
    L.append("")

    # ---- batch-atomic write (both temps, then rename both) ----------------
    csv_path = OUT_DIR / csv_name
    md_path = OUT_DIR / md_name
    csv_tmp = csv_path.with_suffix(csv_path.suffix + ".tmp")
    md_tmp = md_path.with_suffix(md_path.suffix + ".tmp")
    with open(csv_tmp, "w", encoding="ascii", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    with open(md_tmp, "w", encoding="ascii", newline="\n") as fh:
        fh.write("\n".join(L))
    os.replace(csv_tmp, csv_path)
    os.replace(md_tmp, md_path)

    print("[%s] wrote %s (%d rows) and %s" % (label, csv_path.name, len(out_rows), md_path.name))
    print("  third-read coverage: %d/%d present" % (present_count, n_dis))
    print("  adjudication:", {k: adj_counts[k] for k in sorted(adj_counts)})
    print("  branch(a) key-agreement full: %d/%d = %s | resolved-only %d/%d = %s"
          % (a_num, a_den_full, pct(a_num, a_den_full), a_num, a_resolved_den,
             pct(a_num, a_resolved_den)))
    print("  branch(b) code-vs-code:       %d/%d = %s | resolved-only %d/%d = %s"
          % (b_num, b_baseline_den, pct(b_num, b_baseline_den), b_num, b_resolved_den,
             pct(b_num, b_resolved_den)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
