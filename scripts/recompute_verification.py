import csv
import hashlib
import json
import re
import string
from collections import Counter
from pathlib import Path


# Repo-relative: this independent checker recomputes the registered-baseline outputs from the committed
# database and compares against the committed CSVs, so it runs from a clean clone.
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "supporting"
DATA_PATH = ROOT / "data" / "FHA_Unified_Database.json"
MAP_PATH = ROOT / "replication" / "comparator" / "CLAIM_TYPE_NORMALIZATION_MAP.json"
# The published database is the minimized projection of the registered research database:
# scripts/minimize_public_dataset.py drops five free-text / property-level fields that no
# published claim reads. REGISTERED_SOURCE_SHA_LF is the digest of the full registered
# object, retained privately; EXPECTED_SHA_LF is the digest of the published projection.
# The record count is unchanged because minimization removes fields, never records -- which
# is why every baseline below still recomputes to the committed CSVs.
REGISTERED_SOURCE_SHA_LF = "bc6c4b1091401d82216266b89152a7bb2c4aa72c70c0686f3cff01a0a0bff95a"
EXPECTED_SHA_LF = "3f150c39ff187eea002cfc51e7fd7b2c2e399bd27949606b40673a1a706055ed"
EXPECTED_COUNT = 3366
DECIDED = {"PLAINTIFF_WIN", "DEFENDANT_WIN", "MIXED"}
INST_TYPES = {"FAIR_HOUSING_ORG", "GOVERNMENT", "GROUP_HOME_OPERATOR"}
RD_TYPES = {"reasonable_accommodation_denial", "reasonable_modification_denial", "design_and_construction"}
DT_TYPES = {"disparate_treatment"}
SUFFIXES = {
    "INC", "LLC", "CORP", "CORPORATION", "CO", "COMPANY", "LTD", "LIMITED", "LLP", "LP",
    "PLLC", "PC", "P C", "ASSN", "ASSOCIATION",
}


def norm_key(value):
    if value is None:
        return None
    text = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    return text or None


RAW_MAP = json.loads(MAP_PATH.read_text(encoding="utf-8"))
CLAIM_MAP = {norm_key(k): v for k, v in RAW_MAP.items()}


def claim_type(value):
    key = norm_key(value)
    if not key:
        return None
    return CLAIM_MAP.get(key, key)


def claim_type_set(record):
    values = []
    if record.get("primary_claim_type") is not None:
        values.append(record.get("primary_claim_type"))
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
    return "P1a" if date < "2023-04-01" else "P1b"


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


def value_or_missing(value):
    if value is None:
        return "MISSING"
    text = str(value).strip()
    return text if text else "MISSING"


def share(rows, predicate):
    return 0.0 if not rows else sum(1 for r in rows if predicate(r)) / len(rows)


def plaintiff_side(case_name):
    parts = re.split(r"\s+v\.?\s+|\s+vs\.?\s+", case_name or "", maxsplit=1, flags=re.IGNORECASE)
    return parts[0].strip(), len(parts) == 1


def normalize_org(name):
    up = name.upper().replace("&", " AND ")
    up = up.translate(str.maketrans({ch: " " for ch in string.punctuation}))
    words = [w for w in up.split() if w]
    while words and words[-1] in SUFFIXES:
        words.pop()
    return " ".join(words) or "UNKNOWN"


def load_data():
    raw = DATA_PATH.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n")
    sha_lf = hashlib.sha256(normalized).hexdigest()
    data = json.loads(raw.decode("utf-8"))
    return data, sha_lf


def selection_result(data):
    period_rows = {
        p: [r for r in data if period(r) == p and is_decided(r) and is_dis(r) and r.get("pro_se") is False]
        for p in ["P1", "P3"]
    }
    dims = [
        ("bucket_mix", lambda r: bucket(r), ["RD-PURE", "MIXED", "DT-PURE", "OTHER"]),
        ("institutional_share", lambda r: "institutional" if is_inst(r) else "noninstitutional", ["institutional", "noninstitutional"]),
        ("court_circuit_mix", lambda r: value_or_missing(r.get("circuit")), None),
        ("defendant_type_mix", lambda r: value_or_missing(r.get("defendant_type")), None),
        ("procedural_posture_mix", lambda r: value_or_missing(r.get("procedural_posture")), None),
        ("section_504_ra_overlay_share", lambda r: "is_ra_case_true" if r.get("is_ra_case") is True else "is_ra_case_false", ["is_ra_case_true", "is_ra_case_false"]),
    ]
    shifts = []
    for dim, getter, base_cats in dims:
        cats = set(base_cats or [])
        for rows in period_rows.values():
            cats.update(getter(r) for r in rows)
        for cat in cats:
            p1 = share(period_rows["P1"], lambda r, c=cat, g=getter: g(r) == c)
            p3 = share(period_rows["P3"], lambda r, c=cat, g=getter: g(r) == c)
            shifts.append((dim, cat, p3 - p1, abs(p3 - p1)))
    dim, cat, shift, abs_shift = max(shifts, key=lambda x: x[3])
    if abs_shift > 0.20:
        outcome = "SELECTION-EVIDENT"
    elif abs_shift > 0.10:
        outcome = "INDETERMINATE"
    else:
        outcome = "SUPPORTS-BOUNDING"
    return {
        "selection_outcome": outcome,
        "selection_max_dimension": dim,
        "selection_max_category": cat,
        "selection_max_abs_shift": round(abs_shift, 6),
    }


def institutional_result(data):
    result = {}
    for label, flt in [("dis", is_dis), ("disany", is_dis_any)]:
        for p in ["P1", "P3"]:
            rows = [r for r in data if period(r) == p and is_decided(r) and flt(r)]
            n = sum(1 for r in rows if is_inst(r))
            result[f"{label}_inst_{p.lower()}_n"] = n
            result[f"{label}_inst_{p.lower()}_den"] = len(rows)
            result[f"{label}_inst_{p.lower()}_share"] = round(n / len(rows), 6)
    return result


def roster_result(data):
    roster = {}
    for r in data:
        if period(r) not in {"P1", "P2", "P3"} or not is_decided(r) or not is_inst(r):
            continue
        side, _no_v = plaintiff_side(r.get("case_name", ""))
        norm = normalize_org(side)
        item = roster.setdefault(norm, {"P1": 0, "P2": 0, "P3": 0})
        item[period(r)] += 1
    churn = Counter()
    for counts in roster.values():
        if counts["P1"] > 0 and counts["P3"] == 0:
            churn["P1_EXIT"] += 1
        elif counts["P1"] == 0 and counts["P3"] > 0:
            churn["P3_ENTRY"] += 1
        elif counts["P1"] > 0 and counts["P3"] > 0:
            churn["CONTINUING"] += 1
        else:
            churn["P2_ONLY"] += 1
    return {
        "org_total": len(roster),
        "org_p1_exit": churn["P1_EXIT"],
        "org_p3_entry": churn["P3_ENTRY"],
        "org_continuing": churn["CONTINUING"],
        "org_p2_only": churn["P2_ONLY"],
    }


def pretrend_result(data):
    shares = {}
    ns = {}
    for arm in ["RD-PURE", "DT-PURE"]:
        flt = arm_filter(arm)
        for half in ["P1a", "P1b"]:
            rows = [r for r in data if p1_half(r) == half and is_decided(r) and flt(r)]
            ns[(arm, half)] = len(rows)
            shares[(arm, half, "strict")] = share(rows, is_strict_win)
            shares[(arm, half, "pro_se")] = share(rows, lambda r: r.get("pro_se") is True)
    rd_strict = shares[("RD-PURE", "P1b", "strict")] - shares[("RD-PURE", "P1a", "strict")]
    dt_strict = shares[("DT-PURE", "P1b", "strict")] - shares[("DT-PURE", "P1a", "strict")]
    rd_pro = shares[("RD-PURE", "P1b", "pro_se")] - shares[("RD-PURE", "P1a", "pro_se")]
    dt_pro = shares[("DT-PURE", "P1b", "pro_se")] - shares[("DT-PURE", "P1a", "pro_se")]
    strict_diff = rd_strict - dt_strict
    pro_diff = rd_pro - dt_pro
    outcome = "PARALLEL" if abs(strict_diff) <= 0.10 and abs(pro_diff) <= 0.10 else "DIVERGING"
    return {
        "pretrend_outcome": outcome,
        "pretrend_rd_strict_change": round(rd_strict, 6),
        "pretrend_dt_strict_change": round(dt_strict, 6),
        "pretrend_strict_difference": round(strict_diff, 6),
        "pretrend_rd_pro_se_change": round(rd_pro, 6),
        "pretrend_dt_pro_se_change": round(dt_pro, 6),
        "pretrend_pro_se_difference": round(pro_diff, 6),
        "rd_p1a_n": ns[("RD-PURE", "P1a")],
        "rd_p1b_n": ns[("RD-PURE", "P1b")],
        "dt_p1a_n": ns[("DT-PURE", "P1a")],
        "dt_p1b_n": ns[("DT-PURE", "P1b")],
    }


def check(name, observed, expected, failures):
    ok = observed == expected
    print(f"{'PASS' if ok else 'FAIL'} {name}: observed={observed!r} expected={expected!r}")
    if not ok:
        failures.append(name)


def main():
    data, sha = load_data()
    failures = []
    expected = json.loads((OUT / "registered_analysis_results.json").read_text(encoding="utf-8"))["quoted_numbers"]

    check("canonical sha256_lf", sha, EXPECTED_SHA_LF, failures)
    check("canonical record count", len(data), EXPECTED_COUNT, failures)

    observed = {}
    observed.update(selection_result(data))
    observed.update(institutional_result(data))
    observed.update(roster_result(data))
    observed.update(pretrend_result(data))
    observed["fhip_match_status"] = "CONDITIONAL-UNRESOLVED"

    for key in sorted(observed):
        check(key, observed[key], expected[key], failures)

    # Spot-check output shape for the de-duplicated shift table.
    with (OUT / "selection_audit_shifts.csv").open(newline="", encoding="utf-8") as f:
        shift_rows = list(csv.DictReader(f))
    unique_pairs = {(r["dimension"], r["category"]) for r in shift_rows}
    check("selection shift table has no duplicate dimension/category rows", len(shift_rows), len(unique_pairs), failures)

    if failures:
        print(f"RESULT: FAIL ({len(failures)} checks failed)")
        raise SystemExit(1)
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
