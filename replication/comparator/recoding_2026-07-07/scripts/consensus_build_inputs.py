"""Build the Phase 5 consensus input set.

Takes the EXACT 476-row universe from the first pass (RATIONALE_CODED_ROWS.csv arm +
source_file), pulls the full rationale text from the canonical DB, applies the SAME masking
patterns as the first pass (unchanged, so the substrate is identical), and writes
consensus_inputs.json. Also runs the extended-lexicon leakage scan (DIAGNOSIS item 4).

Additionally builds undetermined_inputs.json: the 152 UNDETERMINED-primary-class + 70
empty-protected_classes screened-in rows, unmasked, for the Phase 2.2 sensitivity
classification (primary protected class).
"""
# As-run execution record from the author's research environment; the input paths
# below do not resolve in this archive. The recorded outputs are committed in this
# study directory.
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
STUDY = ROOT / "results" / "comparator_analysis_2026-07"
OUT = STUDY / "recoding_2026-07-07" / "consensus_stage"
# As-run source: the full research database (the masked rationale text it assembles
# reads narrative fields the published minimized database omits -- see
# scripts/minimize_public_dataset.py). The private study inputs it verifies against
# are retained in the project's research records.
DATA_PATH = ROOT / "data" / "FHA_Unified_Database.json"

MASK_REPLACEMENTS = [
    (r"\b(disab\w*|handicap\w*|impair\w*|wheelchair|ptsd|autis\w*|mental health|mobility|blind|deaf)\b", "[CLASS]"),
    (r"\b(race|racial|black|white|african[- ]american|hispanic|latino|asian|native american)\b", "[CLASS]"),
    (r"\b(familial status|children|child|minor)\b", "[CLASS]"),
    (r"\b(reasonable accommodation|accommodation|reasonable modification|modification|design and construction|disparate treatment|disparate impact)\b", "[CLAIM]"),
]

# Extended lexicon for the REAL leakage scan: terms that identify class after the
# first-pass mask has run. Grouped by the class they give away.
LEAK_LEXICON = {
    "disability": [
        "service animal", "emotional support", "esa", "assistance animal", "support animal",
        "grab bar", "ramp", "ada", "americans with disabilities", "section 504",
        "rehabilitation act", "interactive process", "3604(f)", "ssdi", "ssi",
        "caregiver", "medical documentation", "physician", "therapist", "diagnosis",
        "parking space", "service dog", "companion animal",
    ],
    "race": [
        "section 1981", "1981", "1982", "title vii", "national origin", "color",
        "ethnicity", "racial slur", "n-word", "redlining", "steering",
    ],
    "familial": ["familial", "occupancy standard", "adults only", "family with"],
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rationale_text(r) -> str:
    parts = [str(r.get("key_holding") or ""), str(r.get("brief_summary") or "")]
    for c in r.get("fha_claims") or []:
        parts.append(str(c.get("reasoning") or ""))
        parts.append(str(c.get("disposition") or ""))
    return " ".join(p.strip() for p in parts if p.strip())


def mask(text: str) -> str:
    for pat, repl in MASK_REPLACEMENTS:
        text = re.sub(pat, repl, text, flags=re.I)
    return text


def leak_hits(masked: str) -> dict:
    t = masked.lower()
    hits = {}
    for cls, kws in LEAK_LEXICON.items():
        found = sorted({k for k in kws if re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", t)})
        if found:
            hits[cls] = found
    return hits


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    by_sf = {}
    for r in data:
        sf = str(r.get("source_file") or "")
        if sf:
            by_sf.setdefault(sf, r)

    coded = list(csv.DictReader((STUDY / "RATIONALE_CODED_ROWS.csv").open(encoding="utf-8")))
    inputs, missing = [], []
    lex_leak_rows = 0
    for row in coded:
        r = by_sf.get(row["source_file"])
        if r is None:
            missing.append(row["source_file"])
            continue
        raw = rationale_text(r)
        masked = mask(raw)
        hits = leak_hits(masked)
        if hits:
            lex_leak_rows += 1
        inputs.append({
            "row_id": f"{row['arm']}|{row['source_file']}",
            "arm": row["arm"],
            "source_file": row["source_file"],
            "case_name": row["case_name"],
            "period": row["period"],
            "pro_se": row["pro_se"],
            "true_class": "race" if row["arm"] == "RACE-DT" else "disability",
            "proxy_family_first_pass": row["family"],
            "masked_text": masked,
            "text_chars": len(raw),
            "lexicon_leak_hits": hits,
        })
    assert not missing, f"source_files not found in canonical DB: {missing[:5]}"
    assert len(inputs) == 476, f"expected 476 rows, got {len(inputs)}"

    payload = json.dumps(inputs, indent=1, ensure_ascii=False)
    (OUT / "consensus_inputs.json").write_text(payload, encoding="utf-8", newline="\n")

    # Phase 2.2 sensitivity inputs: UNDETERMINED + empty-protected_classes screened-in rows.
    und = []
    for r in data:
        if r.get("screening_result") != "YES":
            continue
        is_und = r.get("primary_protected_class") == "UNDETERMINED"
        is_empty = r.get("protected_classes") == []
        if not (is_und or is_empty):
            continue
        und.append({
            "source_file": r.get("source_file"),
            "case_name": r.get("case_name"),
            "group": "UNDETERMINED" if is_und else "EMPTY_PCS",
            "date_filed": r.get("date_filed"),
            "outcome": r.get("outcome"),
            "pro_se": r.get("pro_se"),
            "claim_types": r.get("claim_types"),
            "text": rationale_text(r),  # unmasked by design: the task IS class identification
        })
    (OUT / "undetermined_inputs.json").write_text(json.dumps(und, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")

    prompt_sha = sha256_bytes((OUT / "phase5_rationale_prompt.txt").read_bytes())
    summary = {
        "n_rows": len(inputs),
        "by_arm": {a: sum(1 for i in inputs if i["arm"] == a) for a in ["RD-PURE", "DT-PURE", "RACE-DT"]},
        "inputs_sha256": sha256_bytes(payload.encode("utf-8")),
        "prompt_sha256": prompt_sha,
        "lexicon_leak_rows": lex_leak_rows,
        "lexicon_leak_rate": round(lex_leak_rows / len(inputs), 4),
        "undetermined_sensitivity_rows": len(und),
    }
    (OUT / "consensus_inputs_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
