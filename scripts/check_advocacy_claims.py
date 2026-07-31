#!/usr/bin/env python3
"""Advocacy-surface claim guard.

The other release checks recompute statistics against the database
(validate_claims.py) but never read the reader-facing advocacy pages, so a
stale or invalidated figure can survive there silently (as happened when the
16-victory census was superseded). This check closes that gap: it asserts,
from scripts/advocacy_claim_assertions.json, that

  * no census-invalidated or superseded figure appears on any guarded page
    ("forbidden" patterns), and
  * the current corrected headline claims are actually present where they
    belong ("required" patterns),

so any future series change (e.g. a v131 sweep-merge adjustment) forces a
deliberate, simultaneous update of the pages and the assertion inventory.

Deterministic, local, no network. Exit 0 only if every assertion holds.
Usage: python scripts/check_advocacy_claims.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ASSERTIONS = Path(__file__).resolve().parent / "advocacy_claim_assertions.json"


def main() -> int:
    with open(ASSERTIONS, encoding="utf-8") as f:
        spec = json.load(f)

    failures: list[str] = []
    pages = spec["pages_all"]
    texts: dict[str, str] = {}
    for page in pages:
        p = REPO / page
        if not p.exists():
            failures.append(f"MISSING PAGE: {page}")
            continue
        texts[page] = p.read_text(encoding="utf-8")

    n_forbidden = 0
    for rule in spec["forbidden"]:
        rx = re.compile(rule["pattern"])
        for page, txt in texts.items():
            for i, line in enumerate(txt.splitlines(), 1):
                if rx.search(line):
                    n_forbidden += 1
                    failures.append(
                        f"FORBIDDEN {rule['id']} on {page}:{i} "
                        f"(pattern {rule['pattern']!r}: {rule['rationale']}) "
                        f"-> {line.strip()[:120]}")

    # Wrap-safe pass: forbidden patterns also run against whitespace-normalized
    # page text, so a phrase split across a line wrap cannot evade the guard.
    for rule in spec["forbidden"]:
        rx = re.compile(rule["pattern"])
        for page, txt in texts.items():
            if any(f.startswith(f"FORBIDDEN {rule['id']} on {page}:")
                   for f in failures):
                continue  # already reported with a line number
            normalized = re.sub(r"\s+", " ", txt)
            if rx.search(normalized):
                n_forbidden += 1
                failures.append(
                    f"FORBIDDEN {rule['id']} on {page} (wrap-normalized match; "
                    f"pattern {rule['pattern']!r}: {rule['rationale']})")

    n_required_ok = 0
    for rule in spec["required"]:
        page = rule["page"]
        if page not in texts:
            continue  # missing-page failure already recorded
        normalized = re.sub(r"\s+", " ", texts[page])
        if re.search(rule["pattern"], normalized):
            n_required_ok += 1
        else:
            failures.append(
                f"REQUIRED-MISSING {rule['id']} on {page} "
                f"(pattern {rule['pattern']!r}: {rule['rationale']})")

    print(f"advocacy claim guard: {len(pages)} pages, "
          f"{len(spec['forbidden'])} forbidden patterns "
          f"({n_forbidden} hits), "
          f"{n_required_ok}/{len(spec['required'])} required claims present")
    if failures:
        for msg in failures:
            print("  FAIL:", msg)
        print("ADVOCACY CLAIM GUARD FAILED "
              f"({len(failures)} failure(s))")
        return 1
    print("ADVOCACY CLAIM GUARD PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
