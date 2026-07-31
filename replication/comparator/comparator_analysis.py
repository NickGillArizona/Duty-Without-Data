from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm


# Repo-relative paths: this module lives at <repo>/replication/comparator/, reads the committed
# canonical database, and writes outputs into the comparator module itself, so the
# analysis reruns from a clean clone with no parent-workspace dependency.
# The first-pass instrument (phase-0 provenance audit, prediction-
# registration machinery, and the deterministic rationale proxy superseded by
# the three-model consensus run under recoding_2026-07-07/) is preserved in
# git history and the project's private research records; this module regenerates the RETAINED
# analytic outputs only. The committed outputs are the as-run record: the seeded
# bootstrap tables reproduce byte-identically anywhere, while scipy/statsmodels
# cells (MODEL_RESULTS.json, MODELS.md model tables, chi-square p-values) match
# to full precision only under the locked environment recorded in
# requirements-lock.txt.
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "replication" / "comparator"
DATA_PATH = ROOT / "data" / "FHA_Unified_Database.json"
EXPECTED_SHA = "bcadb0ee59c8df54a201735eb5d09f58622d5402512c02d7bd9ac13e9671b178"
EXPECTED_N = 3366

PERIODS = {
    "P1": ("2022-01-01", "2024-06-28"),
    "P2": ("2024-06-28", "2025-02-05"),
    "P3": ("2025-02-05", "2026-07-02"),
}
PERIOD_ORDER = ["P1", "P2", "P3"]
DECISIVE_OUTCOMES = {"PLAINTIFF_WIN", "DEFENDANT_WIN", "MIXED"}
STRICT_WIN = {"PLAINTIFF_WIN"}
BROAD_WIN = {"PLAINTIFF_WIN", "MIXED"}

RD_TYPES = {
    "reasonable_accommodation_denial",
    "reasonable_modification_denial",
    "design_and_construction",
}
DT_TYPES = {"disparate_treatment"}

CLAIM_TYPE_MAP = {
    "reasonable_accommodation": "reasonable_accommodation_denial",
    "reasonable accommodation": "reasonable_accommodation_denial",
    "reasonable_accommodation_denial": "reasonable_accommodation_denial",
    "reasonable_modification": "reasonable_modification_denial",
    "reasonable modification": "reasonable_modification_denial",
    "reasonable_modification_denial": "reasonable_modification_denial",
    "design_construction": "design_and_construction",
    "design and construction": "design_and_construction",
    "design_and_construction": "design_and_construction",
    "disparate treatment": "disparate_treatment",
    "disparate_treatment": "disparate_treatment",
    "discriminatory_treatment": "disparate_treatment",
    "disparate impact": "disparate_impact",
    "disparate_impact": "disparate_impact",
    "retaliation": "retaliation",
    "interference coercion": "interference_coercion",
    "interference_coercion": "interference_coercion",
    "discriminatory_advertising": "discriminatory_advertising",
    "discriminatory lending": "discriminatory_lending",
    "discriminatory_lending": "discriminatory_lending",
    "not_fha": "not_fha",
    "n/a": "not_fha",
    "unclear": "unclear",
    "undetermined": "undetermined",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def load_data() -> list[dict[str, Any]]:
    actual = sha256_path(DATA_PATH)
    raw = DATA_PATH.read_bytes()
    data = json.loads(raw)
    if len(data) != EXPECTED_N or actual != EXPECTED_SHA:
        raise SystemExit(f"Baseline mismatch: n={len(data)} sha={actual}")
    return data


def period_for(date_filed: Any) -> str | None:
    if not date_filed:
        return None
    d = str(date_filed)
    for label, (start, end) in PERIODS.items():
        if start <= d < end:
            return label
    return None


def clean_str(x: Any) -> str:
    if x is None:
        return ""
    return str(x).strip()


def norm_token(x: Any) -> str:
    s = clean_str(x).lower()
    s = s.replace("-", "_").replace("/", "_").replace(" ", "_")
    return CLAIM_TYPE_MAP.get(s, s)


def norm_claim_types(record: dict[str, Any], include_fha_claims: bool = False) -> set[str]:
    vals: list[str] = []
    for x in record.get("claim_types") or []:
        vals.append(norm_token(x))
    pc = record.get("primary_claim_type")
    if pc:
        vals.append(norm_token(pc))
    if include_fha_claims:
        for claim in record.get("fha_claims") or []:
            th = claim.get("theory")
            if th:
                vals.append(norm_token(th))
    return {v for v in vals if v}


def protected_classes(record: dict[str, Any]) -> list[str]:
    return [clean_str(x).lower() for x in (record.get("protected_classes") or []) if clean_str(x)]


def is_screened(record: dict[str, Any]) -> bool:
    return record.get("screening_result") == "YES"


def dis_flag(record: dict[str, Any]) -> bool:
    return is_screened(record) and record.get("disability_alleged") is True


def dis_any(record: dict[str, Any]) -> bool:
    pcs = protected_classes(record)
    return is_screened(record) and (
        "disability" in pcs or record.get("disability_alleged") is True or record.get("is_ra_case") is True
    )


def nondis(record: dict[str, Any]) -> bool:
    return is_screened(record) and record.get("disability_alleged") is False


def primary_class(record: dict[str, Any]) -> str:
    return clean_str(record.get("primary_protected_class")).lower()


def has_di(record: dict[str, Any]) -> bool:
    return "disparate_impact" in norm_claim_types(record)


def race_all(record: dict[str, Any]) -> bool:
    return is_screened(record) and primary_class(record) == "race"


def race_dt(record: dict[str, Any]) -> bool:
    return race_all(record) and not has_di(record)


def fam(record: dict[str, Any]) -> bool:
    return is_screened(record) and primary_class(record) == "familial_status"


def bucket_for(record: dict[str, Any]) -> str | None:
    if not dis_flag(record):
        return None
    types = norm_claim_types(record, include_fha_claims=False)
    has_rd = bool(types & RD_TYPES)
    has_dt = bool(types & DT_TYPES)
    if has_rd and has_dt:
        return "MIXED"
    if has_rd and not has_dt:
        return "RD-PURE"
    if has_dt and not has_rd:
        return "DT-PURE"
    return None


COHORTS: dict[str, Callable[[dict[str, Any]], bool]] = {
    "DIS": dis_flag,
    "DIS_ANY_SENSITIVITY": dis_any,
    "RACE-DT": race_dt,
    "RACE-ALL": race_all,
    "NONDIS": nondis,
    "FAM": fam,
}


def cohort_rows(data: list[dict[str, Any]], cohort: str) -> list[dict[str, Any]]:
    if cohort in COHORTS:
        return [r for r in data if COHORTS[cohort](r)]
    if cohort in {"RD-PURE", "DT-PURE", "MIXED"}:
        return [r for r in data if bucket_for(r) == cohort]
    raise KeyError(cohort)


def is_decided(record: dict[str, Any]) -> bool:
    return record.get("outcome") in DECISIVE_OUTCOMES


def is_strict_win(record: dict[str, Any]) -> bool:
    return record.get("outcome") in STRICT_WIN


def is_broad_win(record: dict[str, Any]) -> bool:
    return record.get("outcome") in BROAD_WIN


def is_institutional(record: dict[str, Any]) -> bool:
    # Database stores plaintiff_type in UPPERCASE; the comparison set must use UPPERCASE
    # values. CLASS_ACTION is not a database vocabulary value.
    return record.get("plaintiff_type") in {"FAIR_HOUSING_ORG", "GOVERNMENT", "GROUP_HOME_OPERATOR"}


def is_mtd(record: dict[str, Any]) -> bool:
    return record.get("procedural_posture") == "MOTION_TO_DISMISS"


def rate_ci_boot(values: list[int | bool], reps: int = 2000, seed: int = 42) -> tuple[float | None, float | None, float | None]:
    arr = np.asarray([1 if v else 0 for v in values], dtype=float)
    if arr.size == 0:
        return None, None, None
    rng = np.random.default_rng(seed + arr.size + int(arr.sum() * 17))
    samples = rng.choice(arr, size=(reps, arr.size), replace=True).mean(axis=1)
    return float(arr.mean()), float(np.quantile(samples, 0.025)), float(np.quantile(samples, 0.975))


def fmt_pct(x: float | None) -> str:
    if x is None or pd.isna(x):
        return "NA"
    return f"{100*x:.1f}%"


def fmt_num(x: float | None, digits: int = 3) -> str:
    if x is None or pd.isna(x):
        return "NA"
    return f"{x:.{digits}f}"


def rows_to_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="\n")
        return
    fields: list[str] = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    out = []
    out.append("| " + " | ".join(fields) + " |")
    out.append("|" + "|".join(["---"] * len(fields)) + "|")
    for r in rows:
        out.append("| " + " | ".join(clean_str(r.get(f)) for f in fields) + " |")
    return "\n".join(out)


def make_dataframe(data: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for idx, r in enumerate(data):
        per = period_for(r.get("date_filed"))
        types = norm_claim_types(r, include_fha_claims=False)
        rows.append(
            {
                "idx": idx,
                "case_name": r.get("case_name"),
                "source_file": r.get("source_file"),
                "date_filed": r.get("date_filed"),
                "period": per,
                "screened": is_screened(r),
                "outcome": r.get("outcome"),
                "decided": is_decided(r),
                "strict_win": 1 if is_strict_win(r) else 0,
                "broad_win": 1 if is_broad_win(r) else 0,
                "pro_se": bool(r.get("pro_se")),
                "pro_se_int": 1 if r.get("pro_se") is True else 0,
                "represented": 1 if r.get("pro_se") is False else 0,
                "institutional": 1 if is_institutional(r) else 0,
                "mtd": 1 if is_mtd(r) else 0,
                "primary_class": primary_class(r) or "missing",
                "protected_classes": ";".join(protected_classes(r)),
                "dis_flag": dis_flag(r),
                "dis_any": dis_any(r),
                "nondis": nondis(r),
                "race_all": race_all(r),
                "race_dt": race_dt(r),
                "fam": fam(r),
                "bucket": bucket_for(r),
                "claim_types_norm": ";".join(sorted(types)),
                "has_di": "disparate_impact" in types,
                "has_rd": bool(types & RD_TYPES),
                "has_dt": bool(types & DT_TYPES),
                "procedural_posture": r.get("procedural_posture"),
                "plaintiff_type": r.get("plaintiff_type"),
                "court": r.get("court"),
                "circuit": r.get("circuit"),
                "database_sources": ";".join(r.get("database_sources") or []),
                "dual_basis_claim": r.get("dual_basis_claim"),
            }
        )
    return pd.DataFrame(rows)


def phase2_outputs(data: list[dict[str, Any]], df: pd.DataFrame) -> None:
    write_json(OUT / "CLAIM_TYPE_NORMALIZATION_MAP.json", CLAIM_TYPE_MAP)

    miss_rows = []
    for cohort in ["DIS", "DIS_ANY_SENSITIVITY", "RACE-DT", "RACE-ALL", "NONDIS", "FAM", "RD-PURE", "DT-PURE", "MIXED"]:
        rows = cohort_rows(data, cohort)
        total = len(rows)
        missing_date = sum(1 for r in rows if not r.get("date_filed"))
        miss_rows.append(
            {
                "cohort": cohort,
                "n": total,
                "date_filed_missing_n": missing_date,
                "date_filed_missing_share": missing_date / total if total else None,
                "claim_gate": "APPENDIX-READY",
            }
        )
    rows_to_csv(OUT / "missingness_by_cohort.csv", miss_rows)

    proxy_rows = []
    for proxy in ["circuit", "database_sources", "court"]:
        for cohort in ["DIS", "RACE-ALL", "NONDIS"]:
            rows = cohort_rows(data, cohort)
            if proxy == "database_sources":
                keys = [";".join(r.get("database_sources") or []) for r in rows]
            else:
                keys = [clean_str(r.get(proxy)) or "missing" for r in rows]
            miss = [0 if r.get("date_filed") else 1 for r in rows]
            tab: dict[str, list[int]] = defaultdict(lambda: [0, 0])
            for k, m in zip(keys, miss):
                tab[k][m] += 1
            try:
                arr = np.asarray(list(tab.values()))
                p = stats.chi2_contingency(arr)[1] if arr.shape[0] > 1 else None
            except Exception:
                p = None
            proxy_rows.append(
                {
                    "cohort": cohort,
                    "proxy": proxy,
                    "levels": len(tab),
                    "chi_square_p": p,
                    "claim_gate": "APPENDIX-READY",
                }
            )
    rows_to_csv(OUT / "missingness_proxy_tests.csv", proxy_rows)

    sample_rows = []
    for cohort in ["DIS", "DIS_ANY_SENSITIVITY", "RACE-DT", "RACE-ALL", "NONDIS", "FAM", "RD-PURE", "DT-PURE", "MIXED"]:
        rows = cohort_rows(data, cohort)
        for per in PERIOD_ORDER:
            per_rows = [r for r in rows if period_for(r.get("date_filed")) == per and is_decided(r)]
            for rep in ["pro_se", "represented", "all"]:
                if rep == "pro_se":
                    cell = [r for r in per_rows if r.get("pro_se") is True]
                elif rep == "represented":
                    cell = [r for r in per_rows if r.get("pro_se") is False]
                else:
                    cell = per_rows
                sample_rows.append(
                    {
                        "cohort": cohort,
                        "period": per,
                        "representation": rep,
                        "n_decided": len(cell),
                        "claim_gate": "APPENDIX-READY",
                    }
                )
    rows_to_csv(OUT / "SAMPLE_TABLE.csv", sample_rows)

    sens_rows = []
    for cohort, pred in [("DIS", dis_flag), ("RACE-DT", race_dt), ("RACE-ALL", race_all), ("NONDIS", nondis)]:
        rows = [r for r in data if pred(r)]
        exclusive = [
            r
            for r in rows
            if r.get("dual_basis_claim") in {False, None}
            and len(set(protected_classes(r))) <= 1
        ]
        sens_rows.append(
            {
                "cohort": cohort,
                "n_primary": len(rows),
                "n_exclusive_basis_sensitivity": len(exclusive),
                "excluded_mixed_or_dual": len(rows) - len(exclusive),
                "claim_gate": "APPENDIX-READY",
            }
        )
    rows_to_csv(OUT / "EXCLUSIVE_BASIS_SENSITIVITY.csv", sens_rows)


def table1(data: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for cohort in ["DIS", "DIS_ANY_SENSITIVITY", "RACE-DT", "RACE-ALL", "NONDIS", "FAM", "RD-PURE", "DT-PURE", "MIXED"]:
        all_rows = cohort_rows(data, cohort)
        for per in PERIOD_ORDER:
            cell = [r for r in all_rows if period_for(r.get("date_filed")) == per and is_decided(r)]
            strict, strict_lo, strict_hi = rate_ci_boot([is_strict_win(r) for r in cell])
            broad, broad_lo, broad_hi = rate_ci_boot([is_broad_win(r) for r in cell])
            represented = [r for r in cell if r.get("pro_se") is False]
            prose = [r for r in cell if r.get("pro_se") is True]
            rep_rate, rep_lo, rep_hi = rate_ci_boot([is_strict_win(r) for r in represented])
            pro_rate, pro_lo, pro_hi = rate_ci_boot([is_strict_win(r) for r in prose])
            pro_share, ps_lo, ps_hi = rate_ci_boot([r.get("pro_se") is True for r in cell])
            inst_share, inst_lo, inst_hi = rate_ci_boot([is_institutional(r) for r in cell])
            mtd = [r for r in cell if is_mtd(r)]
            mtd_surv, mtd_lo, mtd_hi = rate_ci_boot([is_broad_win(r) for r in mtd])
            rows.append(
                {
                    "cohort": cohort,
                    "period": per,
                    "n_decided": len(cell),
                    "strict_win_rate": strict,
                    "strict_win_ci_low": strict_lo,
                    "strict_win_ci_high": strict_hi,
                    "broad_win_rate": broad,
                    "broad_win_ci_low": broad_lo,
                    "broad_win_ci_high": broad_hi,
                    "represented_strict_win": rep_rate,
                    "represented_strict_win_ci_low": rep_lo,
                    "represented_strict_win_ci_high": rep_hi,
                    "pro_se_strict_win": pro_rate,
                    "pro_se_strict_win_ci_low": pro_lo,
                    "pro_se_strict_win_ci_high": pro_hi,
                    "pro_se_share": pro_share,
                    "pro_se_share_ci_low": ps_lo,
                    "pro_se_share_ci_high": ps_hi,
                    "institutional_plaintiff_share": inst_share,
                    "institutional_plaintiff_share_ci_low": inst_lo,
                    "institutional_plaintiff_share_ci_high": inst_hi,
                    "mtd_n_decided": len(mtd),
                    "mtd_broad_survival_rate": mtd_surv,
                    "mtd_broad_survival_ci_low": mtd_lo,
                    "mtd_broad_survival_ci_high": mtd_hi,
                    "p2_descriptive_only": per == "P2" and len(cell) < 60,
                    "claim_gate": "APPENDIX-READY",
                }
            )
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "TABLE1_COMPARATOR.csv", index=False)
    md_rows = []
    for _, r in df.iterrows():
        md_rows.append(
            {
                "cohort": r["cohort"],
                "period": r["period"],
                "N": int(r["n_decided"]),
                "strict": fmt_pct(r["strict_win_rate"]),
                "broad": fmt_pct(r["broad_win_rate"]),
                "rep_strict": fmt_pct(r["represented_strict_win"]),
                "pro_se_strict": fmt_pct(r["pro_se_strict_win"]),
                "pro_se_share": fmt_pct(r["pro_se_share"]),
                "inst_share": fmt_pct(r["institutional_plaintiff_share"]),
                "tag": r["claim_gate"],
            }
        )
    write_text(
        OUT / "TABLE1_COMPARATOR.md",
        "# Table 1 Comparator Analog\n\n"
        "All rows are machine-classified and APPENDIX-READY only. P2 rows with n < 60 are descriptive-only. All cells are document-level pipeline output; the reported Part II series is the case-level census (results/series_2026-07.json), and case-level comparator arm cells are in article/appendices/Appendix_A6_Comparator_Analysis.md.\n\n"
        + markdown_table(md_rows, ["cohort", "period", "N", "strict", "broad", "rep_strict", "pro_se_strict", "pro_se_share", "inst_share", "tag"]),
    )
    return df


def kitagawa_for(rows: list[dict[str, Any]], label: str) -> dict[str, Any]:
    p1 = [r for r in rows if period_for(r.get("date_filed")) == "P1" and is_decided(r)]
    p3 = [r for r in rows if period_for(r.get("date_filed")) == "P3" and is_decided(r)]
    strata = [False, True]  # represented, pro se

    def w_rate(cell: list[dict[str, Any]], pro: bool) -> tuple[float, float, int]:
        sub = [r for r in cell if (r.get("pro_se") is True) == pro]
        w = len(sub) / len(cell) if cell else math.nan
        rate = sum(1 for r in sub if is_strict_win(r)) / len(sub) if sub else math.nan
        return w, rate, len(sub)

    vals = {}
    for pro in strata:
        vals[pro] = {"p1": w_rate(p1, pro), "p3": w_rate(p3, pro)}
    r1 = sum(vals[pro]["p1"][0] * vals[pro]["p1"][1] for pro in strata if not math.isnan(vals[pro]["p1"][1]))
    r3 = sum(vals[pro]["p3"][0] * vals[pro]["p3"][1] for pro in strata if not math.isnan(vals[pro]["p3"][1]))
    comp_at_p1 = sum((vals[pro]["p3"][0] - vals[pro]["p1"][0]) * vals[pro]["p1"][1] for pro in strata if not math.isnan(vals[pro]["p1"][1]))
    comp_at_p3 = sum((vals[pro]["p3"][0] - vals[pro]["p1"][0]) * vals[pro]["p3"][1] for pro in strata if not math.isnan(vals[pro]["p3"][1]))
    avg_comp = (comp_at_p1 + comp_at_p3) / 2
    change = r3 - r1
    decline = r1 - r3
    share1 = (-comp_at_p1 / decline) if decline and decline > 0 else math.nan
    share2 = (-comp_at_p3 / decline) if decline and decline > 0 else math.nan
    share_avg = (-avg_comp / decline) if decline and decline > 0 else math.nan
    return {
        "arm": label,
        "n_p1": len(p1),
        "n_p3": len(p3),
        "strict_p1": r1,
        "strict_p3": r3,
        "change_p3_minus_p1": change,
        "decline_p1_minus_p3": decline,
        "composition_effect_comp_first": -comp_at_p1,
        "composition_share_comp_first": share1,
        "composition_effect_rate_first": -comp_at_p3,
        "composition_share_rate_first": share2,
        "composition_effect_path_symmetric": -avg_comp,
        "composition_share_path_symmetric": share_avg,
        "represented_n_p1": vals[False]["p1"][2],
        "represented_n_p3": vals[False]["p3"][2],
        "pro_se_n_p1": vals[True]["p1"][2],
        "pro_se_n_p3": vals[True]["p3"][2],
        "claim_gate": "APPENDIX-READY",
    }


def model_results(df: pd.DataFrame, data: list[dict[str, Any]]) -> dict[str, Any]:
    decomp = []
    for arm in ["DIS", "RD-PURE", "DT-PURE", "RACE-DT", "NONDIS"]:
        decomp.append(kitagawa_for(cohort_rows(data, arm), arm))
    rows_to_csv(OUT / "KITAGAWA_DECOMPOSITION.csv", decomp)

    model_payload: dict[str, Any] = {"decomposition": decomp, "models": {}, "power_notes": []}

    def fit_model(name: str, mdf: pd.DataFrame, formula: str) -> None:
        try:
            mdf = mdf.copy()
            mdf["strict_win"] = mdf["strict_win"].astype(int)
            fit = smf.glm(formula=formula, data=mdf, family=sm.families.Binomial()).fit(cov_type="HC1")
            rows = []
            ci = fit.conf_int()
            for term in fit.params.index:
                coef = float(fit.params[term])
                ci_low = float(ci.loc[term, 0])
                ci_high = float(ci.loc[term, 1])
                rows.append(
                    {
                        "term": term,
                        "coef": coef,
                        "or": float(math.exp(coef)) if abs(coef) < 700 else (math.inf if coef > 0 else 0.0),
                        "ci_low": ci_low,
                        "ci_high": ci_high,
                        "or_ci_low": float(math.exp(ci_low)) if abs(ci_low) < 700 else (math.inf if ci_low > 0 else 0.0),
                        "or_ci_high": float(math.exp(ci_high)) if abs(ci_high) < 700 else (math.inf if ci_high > 0 else 0.0),
                        "p": float(fit.pvalues[term]),
                    }
                )
            separation_warning = any(
                (not np.isfinite(t["or"]))
                or t["or"] > 1e6
                or t["or"] < 1e-6
                or (not np.isfinite(t["p"]))
                for t in rows
            )
            model_payload["models"][name] = {
                "formula": formula,
                "n": int(len(mdf)),
                "terms": rows,
                "warning": "Quasi-separation or thin-cell instability likely; interpret interaction coefficients as directional diagnostics only." if separation_warning else "",
                "claim_gate": "APPENDIX-READY",
            }
        except Exception as exc:
            model_payload["models"][name] = {"formula": formula, "error": str(exc), "claim_gate": "SCREENING-ONLY"}

    within = df[df["decided"] & df["period"].isin(PERIOD_ORDER) & df["bucket"].isin(["RD-PURE", "DT-PURE"])].copy()
    within["bucket2"] = within["bucket"]
    fit_model(
        "within_disability_rd_vs_dt",
        within,
        'strict_win ~ C(period, Treatment(reference="P1")) * C(bucket2, Treatment(reference="DT-PURE")) * pro_se_int',
    )

    cross = df[df["decided"] & df["period"].isin(PERIOD_ORDER) & (df["dis_flag"] | df["race_dt"])].copy()
    cross = cross[(cross["dis_flag"] ^ cross["race_dt"])].copy()
    cross["cohort2"] = np.where(cross["dis_flag"], "DIS", "RACE-DT")
    fit_model(
        "cross_class_dis_vs_race_dt",
        cross,
        'strict_win ~ C(period, Treatment(reference="P1")) * C(cohort2, Treatment(reference="RACE-DT")) * pro_se_int',
    )

    for assignment in ["MIXED_AS_RD", "MIXED_AS_DT"]:
        sens = df[df["decided"] & df["period"].isin(PERIOD_ORDER) & df["bucket"].isin(["RD-PURE", "DT-PURE", "MIXED"])].copy()
        if assignment == "MIXED_AS_RD":
            sens["bucket2"] = sens["bucket"].replace({"MIXED": "RD-PURE"})
        else:
            sens["bucket2"] = sens["bucket"].replace({"MIXED": "DT-PURE"})
        fit_model(
            f"within_disability_sensitivity_{assignment.lower()}",
            sens,
            'strict_win ~ C(period, Treatment(reference="P1")) * C(bucket2, Treatment(reference="DT-PURE")) * pro_se_int',
        )

    for label, filt in [
        ("DT-PURE P2 decided", (df["bucket"] == "DT-PURE") & (df["period"] == "P2") & df["decided"]),
        ("RACE-DT P2 decided", (df["race_dt"]) & (df["period"] == "P2") & df["decided"]),
        ("RACE-DT P2 dated", (df["race_dt"]) & (df["period"] == "P2")),
    ]:
        n = int(filt.sum())
        p = 0.15
        mde = (1.96 + 0.84) * math.sqrt(2 * p * (1 - p) / n) if n > 0 else None
        model_payload["power_notes"].append(
            {
                "cell": label,
                "n": n,
                "rough_mde_two_group_pp_at_p15": mde,
                "note": "Normal-approximation rough MDE for context only; do not significance-chase thin cells.",
            }
        )

    write_json(OUT / "MODEL_RESULTS.json", model_payload)
    write_text(OUT / "MODELS.md", render_models_md(model_payload))
    return model_payload


def render_models_md(payload: dict[str, Any]) -> str:
    lines = ["# Models", "", "All estimates are machine-classified and APPENDIX-READY only. Thin P2 cells are descriptive; do not significance-chase. All cells are document-level archive output; the current manuscript prints no decline or composition-share components from this module (the reported Part II series is the case-level census in `results/series_2026-07.json`, on which no aggregate trend is asserted).", ""]
    lines.append("## Kitagawa Decomposition")
    rows = []
    for r in payload["decomposition"]:
        rows.append(
            {
                "arm": r["arm"],
                "n_p1": r["n_p1"],
                "n_p3": r["n_p3"],
                "strict_p1": fmt_pct(r["strict_p1"]),
                "strict_p3": fmt_pct(r["strict_p3"]),
                "decline": fmt_pct(r["decline_p1_minus_p3"]),
                "comp_share_avg": fmt_pct(r["composition_share_path_symmetric"]),
                "tag": r["claim_gate"],
            }
        )
    lines.append(markdown_table(rows, ["arm", "n_p1", "n_p3", "strict_p1", "strict_p3", "decline", "comp_share_avg", "tag"]))
    for name, model in payload["models"].items():
        lines += ["", f"## {name}", "", f"Formula: `{model.get('formula')}`", ""]
        if "error" in model:
            lines.append(f"Model did not fit: {model['error']}")
            continue
        if model.get("warning"):
            lines.append(f"Warning: {model['warning']}")
            lines.append("")
        term_rows = []
        for t in model["terms"]:
            keep = ("period" in t["term"] and ":" in t["term"]) or t["term"] == "Intercept" or "bucket2" in t["term"] or "cohort2" in t["term"] or "pro_se" in t["term"]
            if keep:
                term_rows.append(
                    {
                        "term": t["term"],
                        "OR": fmt_num(t["or"], 3),
                        "OR_CI": f"[{fmt_num(t['or_ci_low'], 3)}, {fmt_num(t['or_ci_high'], 3)}]",
                        "p": fmt_num(t["p"], 3),
                    }
                )
        lines.append(markdown_table(term_rows, ["term", "OR", "OR_CI", "p"]))
    lines += ["", "## Power / Thin-Cell Notes", ""]
    lines.append(markdown_table(payload["power_notes"], ["cell", "n", "rough_mde_two_group_pp_at_p15", "note"]))
    return "\n".join(lines)


def generated_file_names() -> list[str]:
    """Public comparator-root files pinned by HASH_MANIFEST.json: the retained
    analytic outputs, the frozen instruments and registered records, and the
    terminal consensus tables produced by the correction run."""
    return [
        "CLAIM_TYPE_NORMALIZATION_MAP.json",
        "EXCLUSIVE_BASIS_SENSITIVITY.csv",
        "FINAL_ROW_DECISIONS.csv",
        "KITAGAWA_DECOMPOSITION.csv",
        "METHODS_LIMITATIONS_AND_QA.md",
        "MODEL_RESULTS.json",
        "MODELS.md",
        "missingness_by_cohort.csv",
        "missingness_proxy_tests.csv",
        "PREDICTIONS.md",
        "RATIONALE_CODED_ROWS_CONSENSUS.csv",
        "RATIONALE_RUBRIC.md",
        "RATIONALE_SUMMARY_CONSENSUS.csv",
        "README.md",
        "REGISTERED_PREDICTION_RESULTS.json",
        "SAMPLE_TABLE.csv",
        "TABLE1_COMPARATOR.csv",
        "TABLE1_COMPARATOR.md",
        "comparator_analysis.py",
        "regenerate_table1.py",
    ]


def finalize_manifest() -> None:
    manifest = []
    for name in generated_file_names():
        path = OUT / name
        if path.exists() and path.is_file():
            manifest.append({"file": name, "sha256": sha256_path(path), "bytes": path.stat().st_size})
    write_json(OUT / "HASH_MANIFEST.json", manifest)


def analytics() -> None:
    data = load_data()
    df = make_dataframe(data)
    phase2_outputs(data, df)
    table1(data)
    model_results(df, data)
    finalize_manifest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate the retained comparator analytic outputs from the committed database."
    )
    parser.add_argument("stage", nargs="?", default="analytics", choices=["analytics"])
    parser.parse_args()
    analytics()


if __name__ == "__main__":
    main()
