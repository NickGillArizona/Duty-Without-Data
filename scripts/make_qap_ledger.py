"""Generate results/qap_jurisdiction_ledger.csv — per-jurisdiction dispositions for the
2025-2026 QAP accessibility scan.

One row per jurisdiction (50 states + DC; Puerto Rico is NOT in scope), taken directly from
results/qap_accessibility_2025_2026.json. The ledger makes the scan's uncertainty explicit:
`record_status` separates classified rows (41) from manual-review rows (7) and
retrieval/extraction errors (3), so unresolved rows are never silently folded into a
substantive category.

Usage: python scripts/make_qap_ledger.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "results" / "qap_accessibility_2025_2026.json"
OUT = REPO / "results" / "qap_jurisdiction_ledger.csv"

FIELDS = [
    "state",
    "state_name",
    "record_status",
    "current_requested_label",
    "current_detailed_label",
    "baseline_kelsey_2023_detailed_label",
    "baseline_shift_detailed",
    "selected_document_url",
    "document_title_guess",
    "document_year_guess",
    "document_status_note",
    "auto_classification_reason",
    "manual_notes",
    "error",
    "scan_generated_at_utc",
]


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    generated = data.get("generated_at_utc", "")
    rows = []
    for r in sorted(data["records"], key=lambda x: x["state"]):
        row = {f: ("" if r.get(f) is None else str(r.get(f, ""))) for f in FIELDS[:-1]}
        row["scan_generated_at_utc"] = generated
        rows.append(row)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    from collections import Counter

    statuses = Counter(r["record_status"] for r in rows)
    print(f"wrote {OUT.relative_to(REPO)}: {len(rows)} rows; dispositions: {dict(statuses)}")


if __name__ == "__main__":
    main()
