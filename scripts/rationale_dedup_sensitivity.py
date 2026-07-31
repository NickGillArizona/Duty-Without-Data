"""Case-level dedup sensitivity for the Appendix A-6.4 pleading-deficit core.

The rationale-coding universe is document-level and contains a small number of
cases contributing more than one pleading-loss document. This script rebuilds
the verified Family-A estimator (blind full-opinion audit codes where audited,
masked-consensus codes otherwise), reproduces the printed row-level cells
exactly, and then collapses to distinct case names (a case counts as Family-A
if any of its classifiable pro se rows is verified A).

Inputs (both committed in this repository):
  replication/comparator/RATIONALE_CODED_ROWS_CONSENSUS.csv
  replication/comparator/recoding_2026-07-07/raw_text_verification/R1_VERIFIED_CODES.csv

Expected output:
  row-level  RD-PURE 16/118 (13.6%)  DT-PURE 1/132 (0.8%)  RACE-DT 1/158 (0.6%)
  case-level RD-PURE 14/110 (12.7%)  DT-PURE 1/128 (0.8%)  RACE-DT 1/145 (0.7%)
"""

from __future__ import annotations

import collections
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P_CONSENSUS = ROOT / "replication" / "comparator" / "RATIONALE_CODED_ROWS_CONSENSUS.csv"
P_VERIFIED = (
    ROOT
    / "replication"
    / "comparator"
    / "recoding_2026-07-07"
    / "raw_text_verification"
    / "R1_VERIFIED_CODES.csv"
)

ARMS = ("RD-PURE", "DT-PURE", "RACE-DT")
EXPECTED_ROW_LEVEL = {"RD-PURE": (16, 118), "DT-PURE": (1, 132), "RACE-DT": (1, 158)}


def truthy(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes")


def main() -> None:
    with P_VERIFIED.open(newline="", encoding="utf-8") as handle:
        verified = {row["row_id"]: row for row in csv.DictReader(handle)}
    with P_CONSENSUS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(verified) == 96 and len(rows) == 476

    matched = 0
    for row in rows:
        audit = verified.get(row["arm"] + "|" + row["source_file"])
        if audit:
            matched += 1
        row["final_family"] = audit["verified_family"] if audit else row["consensus_family"]
    assert matched == 96, "every audited row must join back to the universe"

    for arm in ARMS:
        classifiable = [
            r
            for r in rows
            if r["arm"] == arm and truthy(r["pro_se"]) and r["final_family"] in ("A", "B", "C")
        ]
        a_rows = sum(r["final_family"] == "A" for r in classifiable)
        assert (a_rows, len(classifiable)) == EXPECTED_ROW_LEVEL[arm], arm

        by_case: dict[str, list[str]] = collections.defaultdict(list)
        for r in classifiable:
            by_case[r["case_name"].strip().lower()].append(r["final_family"])
        a_cases = sum("A" in families for families in by_case.values())

        print(
            f"{arm:8s} row-level A {a_rows}/{len(classifiable)} "
            f"({100 * a_rows / len(classifiable):.1f}%); "
            f"case-level A {a_cases}/{len(by_case)} "
            f"({100 * a_cases / len(by_case):.1f}%)"
        )


if __name__ == "__main__":
    main()
