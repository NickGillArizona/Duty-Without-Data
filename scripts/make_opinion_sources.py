"""Generate opinion_sources.csv — per-row source provenance for all database records.

One row per record in data/FHA_Unified_Database.json:

- source_file            repository row identifier (the database's stable per-case label);
- case_name, court, year descriptive fields from the database;
- courtlistener_cluster_id  numeric CourtListener cluster id parsed from the source_file
                          prefix (present for API-harvested rows; blank for legacy rows
                          harvested before the labeled-prefix convention);
- courtlistener_url      stable API URL for the cluster (blank when no id);
- database_sources       the database's own source flags for the row;
- source_text_status     "on file with author" for the 853 opinion texts used by the
                          validation/comparator modules; blank for other rows;
- sha256_lf              SHA-256 of the on-file text after CRLF->LF normalization. When a text
                          is not present in a local case_texts/ directory, regeneration CARRIES
                          FORWARD the row's existing sha256_lf rather than recomputing it --
                          running this script without the on-file texts preserves, and does not
                          re-verify, the registered hashes.

Texts not on file can be retrieved with scripts/fetch_opinion_texts.py. Corpus-level
retrieval windows and licensing are documented in replication/DATA_PROVENANCE.md.

Usage: python scripts/make_opinion_sources.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DB = REPO / "data" / "FHA_Unified_Database.json"
CASE_TEXTS = REPO / "case_texts"
OUT = REPO / "opinion_sources.csv"

CLUSTER_RE = re.compile(r"^(\d{6,9})_")

# Verified-cluster overrides (ERRATA 2026-08-04, third entry). Four rows carry a
# numeric filename prefix that is NOT the row's CourtListener cluster id (the
# prefix resolves to an unrelated case). Each override below was re-resolved by
# caption/party search against the live API with a passing positive control and
# an exact decision-date or court corroboration; the sweep record is the
# project's w1b_identity_sweep_2026-08-04 lane.
CLUSTER_OVERRIDES = {
    "025 - MATTER OF HART v New York City Hous Auth 2": "9884278",
    "025 - MATTER OF HART v New York City Housing Authority": "9884278",
    "10000566_2024_Robinson v. District of Columbia_dcd": "9533953",
    "10464414_2024_Sandpiper Residents Association v. HUD_cadc": "9997813",
    "9363862_2023_Socal Recovery, LLC v. City of Costa Mesa_ca9": "9368386",
}


def sha256_lf(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    records = json.loads(DB.read_text(encoding="utf-8"))
    prior = {}
    if OUT.exists():
        with OUT.open(newline="", encoding="utf-8-sig") as f:
            prior = {row["source_file"]: row for row in csv.DictReader(f)}
    rows = []
    on_file = 0
    for r in records:
        sf = r.get("source_file") or ""
        m = CLUSTER_RE.match(sf)
        cid = CLUSTER_OVERRIDES.get(sf, m.group(1) if m else "")
        text_path = CASE_TEXTS / f"{sf}.txt"
        in_repo = text_path.exists()
        prior_hash = prior.get(sf, {}).get("sha256_lf", "")
        text_hash = sha256_lf(text_path) if in_repo else prior_hash
        has_on_file_text = bool(text_hash)
        on_file += int(has_on_file_text)
        srcs = r.get("database_sources")
        if isinstance(srcs, list):
            srcs = "; ".join(str(s) for s in srcs)
        rows.append(
            {
                "source_file": sf,
                "case_name": r.get("case_name") or "",
                "court": r.get("court") or "",
                "year": r.get("year") or "",
                "courtlistener_cluster_id": cid,
                "courtlistener_url": (
                    f"https://www.courtlistener.com/api/rest/v4/clusters/{cid}/" if cid else ""
                ),
                "database_sources": srcs or "",
                "source_text_status": "on file with author" if has_on_file_text else "",
                "sha256_lf": text_hash,
            }
        )
    rows.sort(key=lambda x: x["source_file"])
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with_id = sum(1 for x in rows if x["courtlistener_cluster_id"])
    print(
        f"wrote {OUT.name}: {len(rows)} rows; {with_id} with CourtListener cluster ids; "
        f"{on_file} with source text on file"
    )


if __name__ == "__main__":
    main()
