#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Claims-ledger integrity gate.

Closes the gap the release gate had: no check read `article/CLAIMS_LEDGER.csv` at
all, so the ledger's evidence routes were unverified by any automated layer and
`validate_claims.py`'s 41 selected assertions were the only claim-side coverage.

What this check ESTABLISHES:

  1. the ledger parses as UTF-8 CSV with the expected header;
  2. every claim_id is present, well-formed, and unique;
  3. no required field is blank;
  4. EVERY path-like evidence route in `replication_artifact` resolves to a file
     or directory that exists in this tree.

Line endings are deliberately NOT checked. `.gitattributes` sets `* text=auto`, so
the object store is LF while a Windows checkout with `core.autocrlf=true` is CRLF.
Asserting on the working tree would fail for an environment reason that says
nothing about the ledger.

What it deliberately does NOT establish -- read `replication/GATES.md` before
citing a green run for more than the above:

  * that a route is the RIGHT route for its claim (route correctness is an
    editorial judgment, not a machine property);
  * that the cited primary source supports the claim (that is the Note's
    citation-verification program, not this gate);
  * that the ledger is complete with respect to every published number.

Coverage is REPORTED, never silently assumed: the summary prints how many rows
carry a public in-repository artifact route and how many rest on the cited
primary source plus privately retained material. A nonzero private-only count is
not a failure -- it is a disclosed property of the published ledger.

Usage:
    python scripts/check_claims_ledger.py            # gate mode
    python scripts/check_claims_ledger.py --report   # gate mode + per-row detail

Exit code 0 only if every hard check passes.
"""
from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "article" / "CLAIMS_LEDGER.csv"

EXPECTED_HEADER = [
    "claim_id",
    "note_location",
    "claim_text",
    "source_type",
    "primary_source_or_tier",
    "replication_artifact",
    "expected_value",
    "confidence_tier",
    "notes",
]

REQUIRED_NONBLANK = [
    "claim_id",
    "note_location",
    "claim_text",
    "source_type",
    "primary_source_or_tier",
    "replication_artifact",
    "expected_value",
    "confidence_tier",
]

CLAIM_ID = re.compile(r"^C\d{2,}[a-z]?$")

# A path-like token: at least one slash-separated segment. Trailing punctuation is
# stripped because routes are embedded in prose ("app. C SS C.1; record/hud-27061/").
PATHISH = re.compile(r"(?<![\w/])((?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]*)")

PRIVATE_MARKER = "retained privately"

# The generic private-material disclosure points at this file. It resolves, so it
# is a valid route, but it is NOT claim-specific public evidence -- excluding it is
# what makes the coverage split below mean anything.
GENERIC_DISCLOSURE_ROUTE = "replication/DATA_PROVENANCE.md"


def main() -> int:
    failures: list[str] = []
    report = "--report" in sys.argv

    if not LEDGER.exists():
        print("FAIL: %s does not exist" % LEDGER.relative_to(REPO))
        return 1

    raw = LEDGER.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print("FAIL: ledger is not valid UTF-8: %s" % exc)
        return 1
    rows = list(csv.DictReader(io.StringIO(text), strict=True))
    if not rows:
        print("FAIL: ledger has no rows")
        return 1

    header = list(rows[0].keys())
    if header != EXPECTED_HEADER:
        failures.append("header mismatch:\n  expected %s\n  found    %s"
                        % (EXPECTED_HEADER, header))

    seen: set[str] = set()
    routes_total = 0
    routes_bad: list[tuple[str, str]] = []
    public_rows = 0
    private_only_rows = 0

    for row in rows:
        cid = (row.get("claim_id") or "").strip()

        if not CLAIM_ID.match(cid):
            failures.append("malformed claim_id: %r" % cid)
        if cid in seen:
            failures.append("duplicate claim_id: %s" % cid)
        seen.add(cid)

        for field in REQUIRED_NONBLANK:
            if not (row.get(field) or "").strip():
                failures.append("%s: blank required field %r" % (cid or "?", field))

        artifact = row.get("replication_artifact") or ""
        row_routes = 0
        claim_specific = 0
        for match in PATHISH.finditer(artifact):
            token = match.group(1).rstrip(".,;)")
            if not token or token.startswith(("http://", "https://")):
                continue
            routes_total += 1
            row_routes += 1
            if token != GENERIC_DISCLOSURE_ROUTE:
                claim_specific += 1
            if not (REPO / token).exists():
                routes_bad.append((cid, token))

        if claim_specific:
            public_rows += 1
        elif PRIVATE_MARKER in artifact.lower():
            private_only_rows += 1

        if report:
            print("  %-6s routes=%-2d claim-specific=%-2d %s"
                  % (cid, row_routes, claim_specific, artifact[:70]))

    for cid, token in routes_bad:
        failures.append("%s: evidence route does not resolve: %s" % (cid, token))

    print("claims ledger: %d rows; %d path-like evidence routes; %d resolve"
          % (len(rows), routes_total, routes_total - len(routes_bad)))
    print("coverage (reported, not asserted): %d rows carry a claim-specific public "
          "route; %d rest on the cited primary source plus the generic private-material "
          "disclosure" % (public_rows, private_only_rows))

    if failures:
        print("\nFAILURES (%d):" % len(failures))
        for f in failures:
            print("  - %s" % f)
        return 1

    print("claims-ledger integrity: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
