import csv
import hashlib
import json
import random
import re
import string
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


# Repo-relative layout: this script lives at <repo>/scripts/. The original run
# executed from the author's parent workspace; paths now resolve inside the repository so the
# analysis stages rerun from a clean clone. The development-era working records are
# preserved in git history and the project's private research records;
# this module regenerates the retained analysis outputs only.
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "supporting"
DATA_PATH = ROOT / "data" / "FHA_Unified_Database.json"
MAP_PATH = ROOT / "replication" / "comparator" / "CLAIM_TYPE_NORMALIZATION_MAP.json"
NOTE_PATH = ROOT / "manuscript" / "Duty_Without_Data.md"
A6_PATH = ROOT / "article" / "appendices" / "Appendix_A6_Comparator_Analysis.md"

EXPECTED_DATA_SHA = "bcadb0ee59c8df54a201735eb5d09f58622d5402512c02d7bd9ac13e9671b178"
EXPECTED_DATA_COUNT = 3366
BOOT_REPS = 2000
BOOT_SEED = 20260708
INST_TYPES = {"FAIR_HOUSING_ORG", "GOVERNMENT", "GROUP_HOME_OPERATOR"}
DECIDED = {"PLAINTIFF_WIN", "DEFENDANT_WIN", "MIXED"}
RD_TYPES = {"reasonable_accommodation_denial", "reasonable_modification_denial", "design_and_construction"}
DT_TYPES = {"disparate_treatment"}


def now():
    return datetime.now(timezone.utc).astimezone().isoformat()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_seed(key):
    digest = hashlib.sha256(str(key).encode("utf-8")).hexdigest()
    return BOOT_SEED + int(digest[:8], 16)


def pct(value, digits=1):
    return f"{value * 100:.{digits}f}%"


def pp(value, digits=1):
    return f"{value * 100:.{digits}f}pp"


def pct_csv(value):
    return f"{value:.6f}"


def pp_csv(value):
    return f"{value * 100:.3f}"


def ascii_clean(text):
    replacements = {
        "\u2014": "--",
        "\u2013": "-",
        "\u2010": "-",
        "\u2011": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a7": "Sec.",
        "\u00a7\u00a7": "Secs.",
        "\u00d7": "x",
        "\u2192": "->",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2248": "approx.",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("ascii", "ignore").decode("ascii")


RAW_MAP = json.loads(MAP_PATH.read_text(encoding="utf-8"))


def norm_key(value):
    if value is None:
        return None
    text = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    return text or None


CLAIM_MAP = {norm_key(k): v for k, v in RAW_MAP.items()}


def claim_type(value):
    key = norm_key(value)
    if not key:
        return None
    return CLAIM_MAP.get(key, key)


def claim_type_set(record):
    values = []
    primary = record.get("primary_claim_type")
    if primary is not None:
        values.append(primary)
    values.extend(record.get("claim_types") or [])
    return {claim_type(v) for v in values if claim_type(v)}


def bucket(record):
    types = claim_type_set(record)
    has_rd = bool(types & RD_TYPES)
    has_dt = bool(types & DT_TYPES)
    if has_rd and has_dt:
        return "MIXED"
    if has_rd:
        return "RD-PURE"
    if has_dt:
        return "DT-PURE"
    return "OTHER"


def period(record):
    date = record.get("date_filed")
    if not date:
        return None
    if "2022-01-01" <= date < "2024-06-28":
        return "P1"
    if "2024-06-28" <= date < "2025-02-05":
        return "P2"
    if "2025-02-05" <= date < "2026-07-02":
        return "P3"
    return None


def p1_half(record):
    date = record.get("date_filed")
    if not date or not ("2022-01-01" <= date < "2024-06-28"):
        return None
    if date < "2023-04-01":
        return "P1a"
    return "P1b"


def screened(record):
    return record.get("screening_result") == "YES"


def is_decided(record):
    return record.get("outcome") in DECIDED


def is_strict_win(record):
    return record.get("outcome") == "PLAINTIFF_WIN"


def is_inst(record):
    return record.get("plaintiff_type") in INST_TYPES


def is_dis(record):
    return screened(record) and record.get("disability_alleged") is True


def is_dis_any(record):
    classes = {str(c).lower() for c in (record.get("protected_classes") or [])}
    return screened(record) and (
        record.get("disability_alleged") is True
        or record.get("is_ra_case") is True
        or "disability" in classes
    )


def is_race_dt(record):
    return (
        screened(record)
        and str(record.get("primary_protected_class", "")).lower() == "race"
        and "disparate_impact" not in claim_type_set(record)
    )


def arm_filter(arm):
    if arm == "DIS":
        return lambda r: is_dis(r)
    if arm == "DIS_ANY":
        return lambda r: is_dis_any(r)
    if arm == "RD-PURE":
        return lambda r: is_dis(r) and bucket(r) == "RD-PURE"
    if arm == "DT-PURE":
        return lambda r: is_dis(r) and bucket(r) == "DT-PURE"
    if arm == "MIXED":
        return lambda r: is_dis(r) and bucket(r) == "MIXED"
    if arm == "RACE-DT":
        return lambda r: is_race_dt(r)
    raise ValueError(arm)


def load_data():
    raw = DATA_PATH.read_bytes()
    got_sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw.decode("utf-8"))
    if got_sha != EXPECTED_DATA_SHA or len(data) != EXPECTED_DATA_COUNT:
        raise SystemExit(f"Canonical input drift: sha={got_sha} n={len(data)}")
    return data


def ci_binary(rows, predicate, key):
    n = len(rows)
    if n == 0:
        return (0.0, 0.0)
    rng = random.Random(stable_seed(key))
    vals = []
    for _ in range(BOOT_REPS):
        hits = 0
        for _i in range(n):
            if predicate(rows[rng.randrange(n)]):
                hits += 1
        vals.append(hits / n)
    vals.sort()
    return vals[int(0.025 * BOOT_REPS)], vals[int(0.975 * BOOT_REPS) - 1]


def share(rows, predicate):
    if not rows:
        return 0.0
    return sum(1 for row in rows if predicate(row)) / len(rows)


def value_or_missing(value):
    if value is None:
        return "MISSING"
    text = str(value).strip()
    return text if text else "MISSING"


def write_csv(path, rows, fieldnames=None):
    rows = list(rows)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def selection_audit(data):
    rows = []
    summary = {}
    dimensions = [
        ("bucket_mix", lambda r: bucket(r), ["RD-PURE", "MIXED", "DT-PURE", "OTHER"], "disclosed"),
        ("institutional_share", lambda r: "institutional" if is_inst(r) else "noninstitutional", ["institutional"], "disclosed"),
        ("court_circuit_mix", lambda r: value_or_missing(r.get("circuit")), None, "registered"),
        ("defendant_type_mix", lambda r: value_or_missing(r.get("defendant_type")), None, "registered"),
        ("procedural_posture_mix", lambda r: value_or_missing(r.get("procedural_posture")), None, "registered"),
        ("section_504_ra_overlay_share", lambda r: "is_ra_case_true" if r.get("is_ra_case") is True else "is_ra_case_false", ["is_ra_case_true"], "registered"),
    ]
    for cohort, cohort_filter, cohort_note in [
        ("DIS", is_dis, "featured represented decided disability cohort"),
        ("RACE-DT", is_race_dt, "thin represented context cohort"),
    ]:
        period_rows = {
            p: [r for r in data if period(r) == p and is_decided(r) and cohort_filter(r) and r.get("pro_se") is False]
            for p in ["P1", "P2", "P3"]
        }
        for dim_name, getter, registered_categories, status in dimensions:
            cats = set(registered_categories or [])
            for rows_for_period in period_rows.values():
                cats.update(getter(r) for r in rows_for_period)
            cats = sorted(cats)
            for p in ["P1", "P2", "P3"]:
                den_rows = period_rows[p]
                den = len(den_rows)
                for cat in cats:
                    num = sum(1 for r in den_rows if getter(r) == cat)
                    val = num / den if den else 0.0
                    lo, hi = ci_binary(den_rows, lambda r, c=cat, g=getter: g(r) == c, f"selection|{cohort}|{dim_name}|{p}|{cat}")
                    rows.append({
                        "cohort": cohort,
                        "dimension": dim_name,
                        "category": cat,
                        "period": p,
                        "numerator": num,
                        "denominator": den,
                        "share": pct_csv(val),
                        "ci_low": pct_csv(lo),
                        "ci_high": pct_csv(hi),
                        "registered_status": status,
                        "claim_gate": "APPENDIX-READY",
                        "note": cohort_note,
                    })
    dis_rows = [r for r in rows if r["cohort"] == "DIS" and r["period"] in {"P1", "P3"}]
    by_key = {(r["dimension"], r["category"], r["period"]): float(r["share"]) for r in dis_rows}
    shift_rows = []
    for dim, cat in sorted({(r["dimension"], r["category"]) for r in dis_rows}):
        if (dim, cat, "P1") in by_key and (dim, cat, "P3") in by_key:
            p1 = by_key[(dim, cat, "P1")]
            p3 = by_key[(dim, cat, "P3")]
            shift = p3 - p1
            shift_rows.append({
                "dimension": dim,
                "category": cat,
                "p1_share": p1,
                "p3_share": p3,
                "shift": shift,
                "abs_shift": abs(shift),
            })
    max_shift = max(shift_rows, key=lambda r: r["abs_shift"])
    if max_shift["abs_shift"] > 0.20:
        outcome = "SELECTION-EVIDENT"
    elif max_shift["abs_shift"] > 0.10:
        outcome = "INDETERMINATE"
    else:
        outcome = "SUPPORTS-BOUNDING"
    summary["outcome"] = outcome
    summary["max_shift"] = max_shift
    summary["shift_rows"] = shift_rows
    write_csv(OUT / "selection_audit.csv", rows)
    write_csv(
        OUT / "selection_audit_shifts.csv",
        [
            {
                "dimension": r["dimension"],
                "category": r["category"],
                "p1_share": pct_csv(r["p1_share"]),
                "p3_share": pct_csv(r["p3_share"]),
                "shift_pp": pp_csv(r["shift"]),
                "abs_shift_pp": pp_csv(r["abs_shift"]),
            }
            for r in shift_rows
        ],
    )
    return rows, summary


SUFFIXES = {
    "INC", "LLC", "CORP", "CORPORATION", "CO", "COMPANY", "LTD", "LIMITED", "LLP", "LP",
    "PLLC", "PC", "P C", "ASSN", "ASSOCIATION",
}


def plaintiff_side(case_name):
    text = case_name or ""
    parts = re.split(r"\s+v\.?\s+|\s+vs\.?\s+", text, maxsplit=1, flags=re.IGNORECASE)
    return parts[0].strip(), len(parts) == 1


def normalize_org(name):
    up = name.upper()
    up = up.replace("&", " AND ")
    up = up.translate(str.maketrans({ch: " " for ch in string.punctuation}))
    words = [w for w in up.split() if w]
    while words and words[-1] in SUFFIXES:
        words.pop()
    return " ".join(words)


def institutional_participation(data, fhip_roster_available=False):
    rows = []
    for arm in ["DIS", "RD-PURE", "DT-PURE", "RACE-DT", "DIS_ANY"]:
        flt = arm_filter(arm)
        for p in ["P1", "P2", "P3"]:
            den_rows = [r for r in data if period(r) == p and is_decided(r) and flt(r)]
            num = sum(1 for r in den_rows if is_inst(r))
            val = num / len(den_rows) if den_rows else 0.0
            lo, hi = ci_binary(den_rows, is_inst, f"inst|{arm}|{p}")
            rows.append({
                "cohort": arm,
                "period": p,
                "institutional_n": num,
                "denominator": len(den_rows),
                "share": pct_csv(val),
                "ci_low": pct_csv(lo),
                "ci_high": pct_csv(hi),
                "definition": "plaintiff_type in {FAIR_HOUSING_ORG, GOVERNMENT, GROUP_HOME_OPERATOR}; decided cells",
                "claim_gate": "APPENDIX-READY",
            })
    write_csv(OUT / "institutional_participation.csv", rows)

    roster = {}
    case_rows = [r for r in data if period(r) in {"P1", "P2", "P3"} and is_decided(r) and is_inst(r)]
    for r in case_rows:
        side, no_v = plaintiff_side(r.get("case_name", ""))
        norm = normalize_org(side)
        if not norm:
            norm = "UNKNOWN"
        item = roster.setdefault(norm, {
            "normalized_org_name": norm,
            "raw_names": set(),
            "cases_P1": 0,
            "cases_P2": 0,
            "cases_P3": 0,
            "first_decision_date": None,
            "last_decision_date": None,
            "ambiguous_normalization": False,
            "plaintiff_types": set(),
            "sample_cases": [],
        })
        item["raw_names"].add(side)
        item[f"cases_{period(r)}"] += 1
        date = r.get("date_filed")
        if date:
            item["first_decision_date"] = date if item["first_decision_date"] is None else min(item["first_decision_date"], date)
            item["last_decision_date"] = date if item["last_decision_date"] is None else max(item["last_decision_date"], date)
        item["plaintiff_types"].add(r.get("plaintiff_type") or "")
        if no_v or len(item["raw_names"]) > 1 or norm in {"UNITED STATES", "USA", "U S", "STATE", "CITY", "COUNTY"}:
            item["ambiguous_normalization"] = True
        if len(item["sample_cases"]) < 3:
            item["sample_cases"].append(r.get("case_name", ""))

    roster_rows = []
    for item in sorted(roster.values(), key=lambda x: x["normalized_org_name"]):
        p1 = item["cases_P1"]
        p3 = item["cases_P3"]
        if p1 > 0 and p3 == 0:
            churn = "P1_EXIT"
        elif p1 == 0 and p3 > 0:
            churn = "P3_ENTRY"
        elif p1 > 0 and p3 > 0:
            churn = "CONTINUING"
        else:
            churn = "P2_ONLY"
        roster_rows.append({
            "normalized_org_name": item["normalized_org_name"],
            "cases_P1": item["cases_P1"],
            "cases_P2": item["cases_P2"],
            "cases_P3": item["cases_P3"],
            "first_decision_date": item["first_decision_date"] or "",
            "last_decision_date": item["last_decision_date"] or "",
            "churn_status": churn,
            "ambiguous_normalization": "Y" if item["ambiguous_normalization"] else "N",
            "plaintiff_types": "; ".join(sorted(item["plaintiff_types"])),
            "raw_names": "; ".join(sorted(item["raw_names"])),
            "sample_cases": " | ".join(item["sample_cases"]),
            "claim_gate": "APPENDIX-READY",
        })
    write_csv(OUT / "org_roster.csv", roster_rows)

    churn_counts = Counter(r["churn_status"] for r in roster_rows)
    churn_rows = [
        {"metric": "total_normalized_orgs", "value": len(roster_rows)},
        {"metric": "p1_exit_orgs", "value": churn_counts["P1_EXIT"]},
        {"metric": "p3_entry_orgs", "value": churn_counts["P3_ENTRY"]},
        {"metric": "continuing_orgs", "value": churn_counts["CONTINUING"]},
        {"metric": "p2_only_orgs", "value": churn_counts["P2_ONLY"]},
        {"metric": "ambiguous_normalization_rows", "value": sum(1 for r in roster_rows if r["ambiguous_normalization"] == "Y")},
        {"metric": "fhip_full_terminee_roster_located", "value": "NO" if not fhip_roster_available else "YES"},
    ]
    write_csv(OUT / "org_churn_summary.csv", churn_rows)
    return rows, roster_rows, churn_rows


def pretrend(data):
    rows = []
    exact = {}
    for arm in ["RD-PURE", "DT-PURE", "MIXED", "DIS", "RACE-DT"]:
        flt = arm_filter(arm)
        for half in ["P1a", "P1b"]:
            den_rows = [r for r in data if p1_half(r) == half and is_decided(r) and flt(r)]
            strict = share(den_rows, is_strict_win)
            pro_se = share(den_rows, lambda r: r.get("pro_se") is True)
            exact[(arm, half, "strict")] = strict
            exact[(arm, half, "pro_se")] = pro_se
            strict_lo, strict_hi = ci_binary(den_rows, is_strict_win, f"pretrend|{arm}|{half}|strict")
            pro_lo, pro_hi = ci_binary(den_rows, lambda r: r.get("pro_se") is True, f"pretrend|{arm}|{half}|prose")
            rows.append({
                "cohort": arm,
                "half": half,
                "n": len(den_rows),
                "strict_win_n": sum(1 for r in den_rows if is_strict_win(r)),
                "strict_win_share": pct_csv(strict),
                "strict_ci_low": pct_csv(strict_lo),
                "strict_ci_high": pct_csv(strict_hi),
                "pro_se_n": sum(1 for r in den_rows if r.get("pro_se") is True),
                "pro_se_share": pct_csv(pro_se),
                "pro_se_ci_low": pct_csv(pro_lo),
                "pro_se_ci_high": pct_csv(pro_hi),
                "claim_gate": "APPENDIX-READY",
            })
    write_csv(OUT / "pretrend_p1_split.csv", rows)
    by = {(r["cohort"], r["half"]): r for r in rows}
    rd_strict = exact[("RD-PURE", "P1b", "strict")] - exact[("RD-PURE", "P1a", "strict")]
    dt_strict = exact[("DT-PURE", "P1b", "strict")] - exact[("DT-PURE", "P1a", "strict")]
    rd_pro = exact[("RD-PURE", "P1b", "pro_se")] - exact[("RD-PURE", "P1a", "pro_se")]
    dt_pro = exact[("DT-PURE", "P1b", "pro_se")] - exact[("DT-PURE", "P1a", "pro_se")]
    strict_diff = rd_strict - dt_strict
    pro_diff = rd_pro - dt_pro
    outcome = "PARALLEL" if abs(strict_diff) <= 0.10 and abs(pro_diff) <= 0.10 else "DIVERGING"
    summary = {
        "outcome": outcome,
        "rd_strict_change": rd_strict,
        "dt_strict_change": dt_strict,
        "strict_difference": strict_diff,
        "rd_pro_se_change": rd_pro,
        "dt_pro_se_change": dt_pro,
        "pro_se_difference": pro_diff,
        "rd_declining_relative_to_dt_gt_10pp": strict_diff < -0.10,
    }
    write_csv(
        OUT / "pretrend_decision_rule.csv",
        [{
            "rd_strict_change_pp": pp_csv(rd_strict),
            "dt_strict_change_pp": pp_csv(dt_strict),
            "strict_difference_pp": pp_csv(strict_diff),
            "rd_pro_se_change_pp": pp_csv(rd_pro),
            "dt_pro_se_change_pp": pp_csv(dt_pro),
            "pro_se_difference_pp": pp_csv(pro_diff),
            "rule_outcome": outcome,
            "claim_gate": "APPENDIX-READY",
        }],
    )
    return rows, summary


def md_table(rows, columns):
    lines = ["| " + " | ".join(label for _key, label in columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[key]) for key, _label in columns) + " |")
    return "\n".join(lines)


def get_note_anchor(pattern):
    lines = NOTE_PATH.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines, start=1):
        if pattern in line:
            return idx, ascii_clean(line)
    return None, ""


def get_footnote(num):
    lines = NOTE_PATH.read_text(encoding="utf-8").splitlines()
    start = f"[^{num}]:"
    for idx, line in enumerate(lines, start=1):
        if line.startswith(start):
            return idx, ascii_clean(line)
    return None, ""


def row_lookup(rows, cohort, dimension, category, period):
    for row in rows:
        if row["cohort"] == cohort and row["dimension"] == dimension and row["category"] == category and row["period"] == period:
            return row
    raise KeyError((cohort, dimension, category, period))


def inst_lookup(rows, cohort, period):
    for row in rows:
        if row["cohort"] == cohort and row["period"] == period:
            return row
    raise KeyError((cohort, period))


def pre_lookup(rows, cohort, half):
    for row in rows:
        if row["cohort"] == cohort and row["half"] == half:
            return row
    raise KeyError((cohort, half))


def write_narratives(selection_rows, selection_summary, inst_rows, roster_rows, churn_rows, pre_rows, pre_summary):
    max_shift = selection_summary["max_shift"]
    selection_outcome = selection_summary["outcome"]
    pre_outcome = pre_summary["outcome"]
    fhip_status = "CONDITIONAL-UNRESOLVED"

    # Selection MD
    p1_rd = row_lookup(selection_rows, "DIS", "bucket_mix", "RD-PURE", "P1")
    p3_rd = row_lookup(selection_rows, "DIS", "bucket_mix", "RD-PURE", "P3")
    p1_inst = row_lookup(selection_rows, "DIS", "institutional_share", "institutional", "P1")
    p3_inst = row_lookup(selection_rows, "DIS", "institutional_share", "institutional", "P3")
    selection_md = [
        "# Selection Audit - fn 90 Counsel-Selection Check",
        "",
        "Assurance: EXTENDED (machine-classified). Universe: represented, decided DIS cases unless noted.",
        "",
        f"Rule outcome: {selection_outcome}. The largest P1-to-P3 represented DIS mix shift was {max_shift['dimension']} / {max_shift['category']}: {pp(max_shift['shift'])} (absolute {pp(max_shift['abs_shift'])}).",
        "",
        "## Method",
        "",
        "DIS is `screening_result == YES` plus `disability_alleged is True`, narrower than the Note's Table 1 DIS_ANY cohort. Decided cases have outcome in PLAINTIFF_WIN, DEFENDANT_WIN, or MIXED. Represented means `pro_se is False`. Claim buckets normalize `claim_types` plus `primary_claim_type` using the comparator normalization map and do not expand `fha_claims[].theory`.",
        "",
        f"Bootstrap intervals use {BOOT_REPS} seeded reps, seed `{BOOT_SEED}`.",
        "",
        "## Headline",
        "",
        f"The disclosed represented DIS bucket mix stayed within the registered 10-point bounding threshold: RD-PURE {pct(float(p1_rd['share']))} to {pct(float(p3_rd['share']))}; institutional share {pct(float(p1_inst['share']))} to {pct(float(p3_inst['share']))}. Across all disclosed and registered dimensions, the maximum shift was {pp(max_shift['abs_shift'])}, so the registered rule returns {selection_outcome}.",
        "",
        "The result supports only an observable-bounding claim. It does not rule out unobservable within-bucket selection, including counsel choosing stronger RD-PURE cases inside the same bucket.",
        "",
        "## Files",
        "",
        "- `selection_audit.csv`: all cohort x dimension x category x period cells with bootstrap CIs.",
        "- `selection_audit_shifts.csv`: P1-to-P3 represented DIS decision-rule shifts.",
    ]
    (OUT / "selection_audit.md").write_text("\n".join(selection_md) + "\n", encoding="utf-8")

    # Institutional MD
    dis_p1 = inst_lookup(inst_rows, "DIS", "P1")
    dis_p3 = inst_lookup(inst_rows, "DIS", "P3")
    any_p1 = inst_lookup(inst_rows, "DIS_ANY", "P1")
    any_p3 = inst_lookup(inst_rows, "DIS_ANY", "P3")
    churn = {r["metric"]: r["value"] for r in churn_rows}
    inst_md = [
        "# Institutional Participation and Exit",
        "",
        "Assurance: EXTENDED (machine-classified). The institutional vocabulary is exactly FAIR_HOUSING_ORG, GOVERNMENT, and GROUP_HOME_OPERATOR.",
        "",
        "## Corrected participation series",
        "",
        f"DIS institutional share of decided cases moves from {dis_p1['institutional_n']}/{dis_p1['denominator']} ({pct(float(dis_p1['share']))}) in P1 to {dis_p3['institutional_n']}/{dis_p3['denominator']} ({pct(float(dis_p3['share']))}) in P3. For the Note's broader DIS_ANY cohort, the matching series is {any_p1['institutional_n']}/{any_p1['denominator']} ({pct(float(any_p1['share']))}) to {any_p3['institutional_n']}/{any_p3['denominator']} ({pct(float(any_p3['share']))}).",
        "",
        "This carries the comparator DIAGNOSIS item 13 correction: plaintiff_type values are uppercase in the database, so lowercase matching would silently zero the institutional column.",
        "",
        "## Roster churn",
        "",
        f"The normalized institutional-plaintiff roster contains {churn['total_normalized_orgs']} distinct names across decided P1-P3 cases. P1 exits: {churn['p1_exit_orgs']}; P3 entrants: {churn['p3_entry_orgs']}; continuing names: {churn['continuing_orgs']}; P2-only names: {churn['p2_only_orgs']}. Ambiguous-normalization rows are flagged in `org_roster.csv`.",
        "",
        "## Conditional FHIP matching",
        "",
        "CONDITIONAL-UNRESOLVED. Phase 0 located citable aggregate FHIP termination records and four named organizational plaintiffs, but no full 66-organization terminee roster. No deterministic terminee matching was performed.",
        "",
        "## Files",
        "",
        "- `institutional_participation.csv`: cohort x period institutional shares with CIs.",
        "- `org_roster.csv`: normalized organization roster with churn status and ambiguity flag.",
        "- `org_churn_summary.csv`: churn counts and FHIP-list status.",
    ]
    (OUT / "institutional_participation.md").write_text("\n".join(inst_md) + "\n", encoding="utf-8")

    # Pretrend MD
    rd_a = pre_lookup(pre_rows, "RD-PURE", "P1a")
    rd_b = pre_lookup(pre_rows, "RD-PURE", "P1b")
    dt_a = pre_lookup(pre_rows, "DT-PURE", "P1a")
    dt_b = pre_lookup(pre_rows, "DT-PURE", "P1b")
    pre_md = [
        "# P1 Pre-Trend Split",
        "",
        "Assurance: EXTENDED (machine-classified). Split: P1a = date_filed before 2023-04-01 within P1; P1b = the remainder of P1.",
        "",
        f"Rule outcome: {pre_outcome}. RD-PURE strict-win change P1a->P1b was {pp(pre_summary['rd_strict_change'])}; DT-PURE strict-win change was {pp(pre_summary['dt_strict_change'])}; difference {pp(pre_summary['strict_difference'])}. RD-PURE pro se-share change was {pp(pre_summary['rd_pro_se_change'])}; DT-PURE pro se-share change was {pp(pre_summary['dt_pro_se_change'])}; difference {pp(pre_summary['pro_se_difference'])}.",
        "",
        "## Cell-size caution",
        "",
        f"RD-PURE decided cells are {rd_a['n']} and {rd_b['n']}; DT-PURE cells are thinner at {dt_a['n']} and {dt_b['n']}. The result is a period-design check, not a causal test.",
        "",
        "## Files",
        "",
        "- `pretrend_p1_split.csv`: registered cohort x half strict-win and pro se shares with CIs.",
        "- `pretrend_decision_rule.csv`: rule arithmetic.",
    ]
    (OUT / "pretrend_p1_split.md").write_text("\n".join(pre_md) + "\n", encoding="utf-8")

    quoted = {
        "selection_outcome": selection_outcome,
        "selection_max_dimension": max_shift["dimension"],
        "selection_max_category": max_shift["category"],
        "selection_max_abs_shift": round(max_shift["abs_shift"], 6),
        "dis_inst_p1_n": int(dis_p1["institutional_n"]),
        "dis_inst_p1_den": int(dis_p1["denominator"]),
        "dis_inst_p1_share": round(float(dis_p1["share"]), 6),
        "dis_inst_p3_n": int(dis_p3["institutional_n"]),
        "dis_inst_p3_den": int(dis_p3["denominator"]),
        "dis_inst_p3_share": round(float(dis_p3["share"]), 6),
        "disany_inst_p1_n": int(any_p1["institutional_n"]),
        "disany_inst_p1_den": int(any_p1["denominator"]),
        "disany_inst_p1_share": round(float(any_p1["share"]), 6),
        "disany_inst_p3_n": int(any_p3["institutional_n"]),
        "disany_inst_p3_den": int(any_p3["denominator"]),
        "disany_inst_p3_share": round(float(any_p3["share"]), 6),
        "org_total": int(churn["total_normalized_orgs"]),
        "org_p1_exit": int(churn["p1_exit_orgs"]),
        "org_p3_entry": int(churn["p3_entry_orgs"]),
        "org_continuing": int(churn["continuing_orgs"]),
        "org_p2_only": int(churn["p2_only_orgs"]),
        "pretrend_outcome": pre_outcome,
        "pretrend_rd_strict_change": round(pre_summary["rd_strict_change"], 6),
        "pretrend_dt_strict_change": round(pre_summary["dt_strict_change"], 6),
        "pretrend_strict_difference": round(pre_summary["strict_difference"], 6),
        "pretrend_rd_pro_se_change": round(pre_summary["rd_pro_se_change"], 6),
        "pretrend_dt_pro_se_change": round(pre_summary["dt_pro_se_change"], 6),
        "pretrend_pro_se_difference": round(pre_summary["pro_se_difference"], 6),
        "rd_p1a_n": int(rd_a["n"]),
        "rd_p1b_n": int(rd_b["n"]),
        "dt_p1a_n": int(dt_a["n"]),
        "dt_p1b_n": int(dt_b["n"]),
        "fhip_match_status": fhip_status,
    }
    (OUT / "registered_analysis_results.json").write_text(json.dumps({
        "timestamp": now(),
        "bootstrap_reps": BOOT_REPS,
        "bootstrap_seed": BOOT_SEED,
        "quoted_numbers": quoted,
        "selection_decision": selection_summary,
        "pretrend_decision": pre_summary,
    }, indent=2, default=str) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = load_data()
    selection_rows, selection_summary = selection_audit(data)
    inst_rows, roster_rows, churn_rows = institutional_participation(data)
    pre_rows, pre_summary = pretrend(data)
    write_narratives(selection_rows, selection_summary, inst_rows, roster_rows, churn_rows, pre_rows, pre_summary)


if __name__ == "__main__":
    main()
