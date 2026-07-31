"""Fetch opinion texts from CourtListener for rows listed in opinion_sources.csv.

Deterministic fetch-normalize-hash route into a LOCAL case_texts/ working directory (opinion
texts are not distributed in this repository; the directory is created on first run): for each
requested row with a CourtListener cluster id, this script retrieves the cluster's
sub-opinions from the REST v4 API, extracts plain text (preferring `plain_text`, falling back
to HTML fields with tags stripped), normalizes line endings to LF, writes
case_texts/<source_file>.txt, and prints the SHA-256 of the normalized bytes.

Honesty notes:

- The as-run instruments for the validation and comparator lanes are the author-held on-file
  texts whose normalized SHA-256 values are registered in opinion_sources.csv; a fetched text
  is authoritative for reproducing those runs only when its hash matches the registered value.
- A fresh fetch can differ from the original harvest if CourtListener re-OCRs or corrects an
  opinion. When opinion_sources.csv records a sha256_lf for a row, this script compares and
  reports DRIFT rather than overwriting (use --overwrite to replace).
- Legacy rows without a CourtListener cluster id (pre-convention labels such as
  "025 - Arrington v MZ 2640 OWNER LLP") cannot be fetched by id; locate them by case name
  via CourtListener search. They are reported as SKIPPED-NO-ID.

Anonymous API access is rate-limited; pass --token for a CourtListener API token.

Usage:
  python scripts/fetch_opinion_texts.py --only-missing          # fetch texts absent locally
  python scripts/fetch_opinion_texts.py --verify                # re-fetch local store, report drift
  python scripts/fetch_opinion_texts.py --limit 10 --token XYZ
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCES = REPO / "opinion_sources.csv"
CASE_TEXTS = REPO / "case_texts"
API = "https://www.courtlistener.com/api/rest/v4"

TAG_RE = re.compile(r"<[^>]+>")


def get_json(url: str, token: str | None) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "duty-without-data-replication"})
    if token:
        req.add_header("Authorization", f"Token {token}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def opinion_text(op: dict) -> str:
    for field in ("plain_text", "html_with_citations", "html", "html_lawbox", "xml_harvard"):
        val = op.get(field)
        if val and val.strip():
            if field == "plain_text":
                return val
            return html.unescape(TAG_RE.sub(" ", val))
    return ""


def fetch_cluster_text(cluster_id: str, token: str | None) -> str:
    cluster = get_json(f"{API}/clusters/{cluster_id}/", token)
    texts = []
    for op_url in cluster.get("sub_opinions", []):
        op = get_json(op_url, token)
        t = opinion_text(op)
        if t.strip():
            texts.append(t)
    return "\n\n".join(texts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default=None, help="CourtListener API token")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only-missing", action="store_true", default=True)
    ap.add_argument("--verify", action="store_true", help="re-fetch committed texts and report drift")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    CASE_TEXTS.mkdir(exist_ok=True)
    rows = list(csv.DictReader(SOURCES.open(encoding="utf-8")))
    done = 0
    for row in rows:
        sf, cid = row["source_file"], row["courtlistener_cluster_id"]
        dest = CASE_TEXTS / f"{sf}.txt"
        if not cid:
            if not dest.exists():
                print(f"SKIPPED-NO-ID: {sf}")
            continue
        if dest.exists() and not args.verify and not args.overwrite:
            continue
        if args.limit is not None and done >= args.limit:
            break
        try:
            text = fetch_cluster_text(cid, args.token)
        except Exception as e:  # noqa: BLE001 — report and continue
            print(f"FETCH-ERROR: {sf}: {e}")
            continue
        if not text.strip():
            print(f"EMPTY: {sf}")
            continue
        norm = text.replace("\r\n", "\n").encode("utf-8")
        digest = hashlib.sha256(norm).hexdigest()
        recorded = row.get("sha256_lf") or ""
        if recorded and digest != recorded:
            print(f"DRIFT: {sf}: fetched {digest[:12]} != recorded {recorded[:12]}")
            if not args.overwrite:
                done += 1
                time.sleep(1)
                continue
        if not dest.exists() or args.overwrite:
            dest.write_bytes(norm)
            print(f"WROTE: {sf} ({digest[:12]})")
        else:
            print(f"OK: {sf} ({digest[:12]})")
        done += 1
        time.sleep(1)  # be polite to the API


if __name__ == "__main__":
    main()
