import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


# Repo-relative: resolves against the repository so the baseline rebuild runs from a clean clone.
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "supporting"
PREREG = ROOT / "method" / "preregistration"
DATA_PATH = ROOT / "data" / "FHA_Unified_Database.json"
MAP_PATH = ROOT / "replication" / "comparator" / "CLAIM_TYPE_NORMALIZATION_MAP.json"

EXPECTED_DATA_SHA_LF = "bc6c4b1091401d82216266b89152a7bb2c4aa72c70c0686f3cff01a0a0bff95a"
EXPECTED_DATA_COUNT = 3366
INST_TYPES = {"FAIR_HOUSING_ORG", "GOVERNMENT", "GROUP_HOME_OPERATOR"}
DECIDED = {"PLAINTIFF_WIN", "DEFENDANT_WIN", "MIXED"}
RD_TYPES = {"reasonable_accommodation_denial", "reasonable_modification_denial", "design_and_construction"}
DT_TYPES = {"disparate_treatment"}


def now():
    return datetime.now(timezone.utc).astimezone().isoformat()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_data():
    raw = DATA_PATH.read_bytes()
    got_sha = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
    data = json.loads(raw.decode("utf-8"))
    return data, got_sha


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
    primary = record.get("primary_claim_type")
    if primary is not None:
        values.append(primary)
    for item in record.get("claim_types") or []:
        values.append(item)
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
    classes = record.get("protected_classes") or []
    classes_l = {str(c).lower() for c in classes}
    return screened(record) and (
        record.get("disability_alleged") is True
        or record.get("is_ra_case") is True
        or "disability" in classes_l
    )


def is_race_dt(record):
    return (
        screened(record)
        and str(record.get("primary_protected_class", "")).lower() == "race"
        and "disparate_impact" not in claim_type_set(record)
    )


def pct(n, d):
    return None if d == 0 else round(n / d, 6)


def assert_equal(name, got, expected, errors):
    if got != expected:
        errors.append({"check": name, "expected": expected, "got": got})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data, data_sha = load_data()
    errors = []
    assert_equal("canonical database SHA256-LF", data_sha, EXPECTED_DATA_SHA_LF, errors)
    assert_equal("canonical database record count", len(data), EXPECTED_DATA_COUNT, errors)

    baseline = {
        "timestamp": now(),
        "canonical_database": str(DATA_PATH.relative_to(ROOT)),
        "canonical_database_sha256_lf": data_sha,
        "canonical_database_records": len(data),
        "expected_database_sha256_lf": EXPECTED_DATA_SHA_LF,
        "expected_database_records": EXPECTED_DATA_COUNT,
    }
    (PREREG / "session_baseline.json").write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")

    periods = ["P1", "P2", "P3"]
    arms = ["DIS", "RD-PURE", "DT-PURE", "RACE-DT"]

    def arm_filter(arm):
        if arm == "DIS":
            return lambda r: is_dis(r)
        if arm == "RD-PURE":
            return lambda r: is_dis(r) and bucket(r) == "RD-PURE"
        if arm == "DT-PURE":
            return lambda r: is_dis(r) and bucket(r) == "DT-PURE"
        if arm == "RACE-DT":
            return lambda r: is_race_dt(r)
        raise ValueError(arm)

    institutional_rows = []
    for arm in arms:
        flt = arm_filter(arm)
        for p in periods:
            rows = [r for r in data if period(r) == p and is_decided(r) and flt(r)]
            inst_n = sum(1 for r in rows if is_inst(r))
            institutional_rows.append({
                "arm": arm,
                "period": p,
                "inst_n": inst_n,
                "n": len(rows),
                "share": pct(inst_n, len(rows)),
                "definition": "plaintiff_type in {FAIR_HOUSING_ORG, GOVERNMENT, GROUP_HOME_OPERATOR}; decided cells",
                "claim_gate": "APPENDIX-READY",
            })

    expected_inst = {
        ("DIS", "P1"): (74, 383),
        ("DIS", "P3"): (30, 314),
        ("RD-PURE", "P1"): (32, 170),
        ("RD-PURE", "P3"): (11, 141),
        ("DT-PURE", "P1"): (9, 78),
        ("DT-PURE", "P3"): (2, 53),
        ("RACE-DT", "P1"): (6, 138),
        ("RACE-DT", "P3"): (1, 71),
    }
    for row in institutional_rows:
        key = (row["arm"], row["period"])
        if key in expected_inst:
            assert_equal(f"institutional {key} inst_n/n", (row["inst_n"], row["n"]), expected_inst[key], errors)

    with (OUT / "baseline_institutional.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(institutional_rows[0].keys()))
        writer.writeheader()
        writer.writerows(institutional_rows)

    represented_rows = []
    for p in ["P1", "P3"]:
        rows = [r for r in data if period(r) == p and is_decided(r) and is_dis(r) and r.get("pro_se") is False]
        mix = Counter(bucket(r) for r in rows)
        represented_rows.append({
            "period": p,
            "n": len(rows),
            "rd_pure": mix["RD-PURE"],
            "mixed": mix["MIXED"],
            "dt_pure": mix["DT-PURE"],
            "other": mix["OTHER"],
            "institutional": sum(1 for r in rows if is_inst(r)),
            "definition": "represented (pro_se is False), decided, DIS cohort",
            "claim_gate": "APPENDIX-READY",
        })
    expected_rep = {
        "P1": {"n": 176, "rd_pure": 94, "mixed": 53, "dt_pure": 18, "other": 11, "institutional": 73},
        "P3": {"n": 81, "rd_pure": 38, "mixed": 26, "dt_pure": 14, "other": 3, "institutional": 30},
    }
    for row in represented_rows:
        got = {k: row[k] for k in ["n", "rd_pure", "mixed", "dt_pure", "other", "institutional"]}
        assert_equal(f"represented decided DIS {row['period']}", got, expected_rep[row["period"]], errors)

    with (OUT / "baseline_represented.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(represented_rows[0].keys()))
        writer.writeheader()
        writer.writerows(represented_rows)

    comparator_rows = []
    expected_comp = {
        "RD-PURE": {"P1": 170, "P2": 33, "P3": 141},
        "DT-PURE": {"P1": 78, "P2": 23, "P3": 53},
    }
    for arm in ["RD-PURE", "DT-PURE"]:
        row = {"arm": arm}
        for p in periods:
            n = sum(1 for r in data if period(r) == p and is_decided(r) and is_dis(r) and bucket(r) == arm)
            row[p] = n
        comparator_rows.append(row)
        assert_equal(f"comparator anchor {arm}", {p: row[p] for p in periods}, expected_comp[arm], errors)
    with (OUT / "baseline_comparator_anchors.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["arm", "P1", "P2", "P3"])
        writer.writeheader()
        writer.writerows(comparator_rows)

    # Author-held source-archive records: only the manuscript entry ships with this repository.
    fhip_sources = [
        {
            "path": "manuscript/Duty_Without_Data.md",
            "status": "manuscript anchor",
            "use": "Footnotes 60 and 77 route the FHIP termination claim to NFHA 2025, Massachusetts Fair Housing Center v. HUD, and app. C.",
        },
        {
            "path": "sources/v122_acquisitions/agency/03_NFHA_2025_Fair_Housing_Trends_Report.pdf",
            "status": "citable PDF exists",
            "use": "NFHA report states that 78 FHIP grants were terminated, rescinding $30 million, and names four organizational plaintiffs; it does not provide a full 66-organization terminee roster.",
        },
        {
            "path": "sources/FINAL_ARCHIVE/t6_courtlistener_fhip_dmass_3_25_cv_30041.json",
            "status": "machine-readable docket record exists",
            "use": "CourtListener docket metadata for Massachusetts Fair Housing Center v. HUD; useful for docket chronology, not a terminee-name roster.",
        },
        {
            "path": "Displacing-Deference-Data-and-Doctrine-for-a-Disability-Centered-AFFH/appendices/Appendix_C_HUD_Administrative_Record.md",
            "status": "companion appendix exists",
            "use": "Appendix C records the FHIP chronology and partial reinstatement; no full terminee-name roster located in this file.",
        },
        {
            "path": "research_outputs/J_fhip_coverage.md",
            "status": "derivative memo exists",
            "use": "Aggregates FHIP capacity facts and a few named examples; treated as routing/provenance, not a primary terminee roster.",
        },
        {
            "path": "sources/v122_acquisitions/agency/22_NLIHC_Whistleblowers_HUD_2025.html",
            "status": "citable public-source capture exists",
            "use": "Documents enforcement-capacity claims and FHIP funding limbo; not a terminee-name roster.",
        },
    ]
    for src in fhip_sources:
        src_path = ROOT / src["path"]
        src["exists"] = src_path.exists()
        src["sha256"] = sha256(src_path) if src_path.exists() and src_path.is_file() else None

    fhip_md = [
        "# FHIP Provenance - Phase 0",
        "",
        "Claim-gate: APPENDIX-READY for repository provenance facts only; no publication claim is upgraded here.",
        "",
        "## Note route",
        "",
        "- The manuscript fn 60 cites NFHA 2025 for FHIP terminations, FHEO charge contraction, and staffing reductions.",
        "- The manuscript fn 77 cites `Massachusetts Fair Housing Center v. HUD`, No. 3:25-cv-30041, and points to app. C for the full docket chronology.",
        "",
        "## Located local records",
        "",
        "| Path | Status | Use | SHA256 |",
        "|---|---|---|---|",
    ]
    for src in fhip_sources:
        fhip_md.append(f"| `{src['path']}` | {src['status']} | {src['use']} | `{src['sha256'] or 'n/a'}` |")
    fhip_md.extend([
        "",
        "## Terminee-list status",
        "",
        "No full machine-readable or citable 66-organization terminee roster was located in the searched local materials.",
        "The NFHA report provides a citable aggregate and names four organizational plaintiffs: Massachusetts Fair Housing Center, Intermountain Fair Housing Council, Fair Housing Council of South Texas, and Housing Research & Advocacy Center. Those names do not constitute the full terminee list. The Phase 3 matching condition is therefore unresolved unless a full roster is later supplied.",
        "",
        "Search scope recorded from Phase 0: `sources`, `research_outputs`, `oira_harvest`, and `results`.",
    ])
    (PREREG / "PROVENANCE_FHIP.md").write_text("\n".join(fhip_md) + "\n", encoding="utf-8")

    summary = {
        "timestamp": now(),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "institutional_baseline_rows": institutional_rows,
        "represented_baseline_rows": represented_rows,
        "comparator_anchor_rows": comparator_rows,
        "fhip_full_terminee_roster_located": False,
        "fhip_named_plaintiff_examples": [
            "Massachusetts Fair Housing Center",
            "Intermountain Fair Housing Council",
            "Fair Housing Council of South Texas",
            "Housing Research & Advocacy Center",
        ],
    }
    (OUT / "baseline_verification.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Phase 0 Baseline Verification",
        "",
        f"Status: {'PASS' if not errors else 'FAIL'}",
        "",
        "No registered Phase 2-4 quantities were computed in this phase.",
        "",
        "## Canonical database",
        "",
        f"- Path: `{DATA_PATH.relative_to(ROOT)}`",
        f"- Records: {len(data)}",
        f"- SHA256: `{data_sha}`",
        "",
        "## Required baselines",
        "",
        "- Corrected institutional shares: reproduced against `INSTITUTIONAL_SHARE_CORRECTED.csv` expected P1/P3 cells.",
        "- Represented decided DIS cells: reproduced P1 n=176 and P3 n=81 with registered peeked bucket mix.",
        "- Comparator anchor cells: reproduced RD-PURE 170/33/141 and DT-PURE 78/23/53.",
        "",
        "## FHIP provenance",
        "",
        "- Full terminee roster located: NO.",
        "- Citable aggregate and four named organizational plaintiffs located in the archived NFHA report.",
        "- Conditional FHIP matching remains unresolved absent a full terminee roster.",
    ]
    if errors:
        md.extend(["", "## Errors", ""])
        for err in errors:
            md.append(f"- {err['check']}: expected `{err['expected']}`, got `{err['got']}`")
    (OUT / "baseline_verification.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    if errors:
        raise SystemExit("Phase 0 baseline verification failed; see results/supporting/baseline_verification.json")


if __name__ == "__main__":
    main()
