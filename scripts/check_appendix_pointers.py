#!/usr/bin/env python3
"""Appendix-pointer integrity guard.

Verifies, from scripts/appendix_pointer_assertions.json, that every registered
repository-pointing footnote in the manuscript mirror resolves end to end: the
raw footnote label exists in manuscript/Duty_Without_Data.md, the target file
exists, the target section heading exists, and every registered literal the
footnote states appears inside that section. This is the guard for the
footnote-in-hand reader: a pointer that resolves to a section that does not
carry the cited support fails the gate.

Assertion record shape (one per pointer; a footnote may register several):

  {
    "raw_footnote": "86",
    "target_file": "article/appendices/Appendix_E_Accommodation_Defendant_Analysis.md",
    "target_heading": "#### E.1.1 Claim-Specificity Validation",
    "required_literals": ["66.6%", "74.7%", "85%"],
    "note": "optional context for maintainers"
  }

"target_heading" null means the whole target file is the scope. Literal
matching is whitespace-normalized, so a value wrapped across lines still
counts. Deterministic, local, no network. Exit 0 only if every assertion
holds.

Usage: python scripts/check_appendix_pointers.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ASSERTIONS = Path(__file__).resolve().parent / "appendix_pointer_assertions.json"
MANUSCRIPT = REPO / "manuscript" / "Duty_Without_Data.md"


def section_text(lines: list[str], heading: str) -> str | None:
    """Text of the section under `heading` (exact stripped match), ending at the
    next heading of the same or higher level. None if the heading is absent."""
    target = heading.strip()
    level = len(target) - len(target.lstrip("#"))
    start = None
    for i, line in enumerate(lines):
        if line.strip() == target:
            start = i
            break
    if start is None:
        return None
    out: list[str] = []
    for line in lines[start + 1:]:
        s = line.strip()
        if s.startswith("#"):
            lvl = len(s) - len(s.lstrip("#"))
            if 1 <= lvl <= level:
                break
        out.append(line)
    return "\n".join(out)


def main() -> int:
    try:
        with open(ASSERTIONS, encoding="utf-8") as f:
            spec = json.load(f)
    except OSError as exc:
        print(f"check_appendix_pointers: cannot read assertions: {exc}", file=sys.stderr)
        return 2
    try:
        manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"check_appendix_pointers: cannot read manuscript: {exc}", file=sys.stderr)
        return 2

    failures: list[str] = []
    n_ok = 0
    for rec in spec["pointers"]:
        fn = rec["raw_footnote"]
        errs: list[str] = []
        if f"[^{fn}]:" not in manuscript:
            errs.append(f"footnote definition [^{fn}]: not found in the manuscript")
        target = REPO / rec["target_file"]
        if not target.exists():
            errs.append(f"target file missing: {rec['target_file']}")
        else:
            lines = target.read_text(encoding="utf-8").splitlines()
            heading = rec.get("target_heading")
            if heading:
                scope = section_text(lines, heading)
                if scope is None:
                    errs.append(f"heading not found: {heading!r}")
            else:
                scope = "\n".join(lines)
            if scope is not None:
                norm = re.sub(r"\s+", " ", scope)
                for lit in rec.get("required_literals", []):
                    if re.sub(r"\s+", " ", lit) not in norm:
                        errs.append(f"literal {lit!r} not found in the target section")
        if errs:
            for e in errs:
                failures.append(f"fn {fn} -> {rec['target_file']}: {e}")
        else:
            n_ok += 1

    print(f"appendix-pointer guard: {n_ok}/{len(spec['pointers'])} registered "
          "pointers resolve")
    if failures:
        for msg in failures:
            print("  FAIL:", msg)
        print(f"APPENDIX POINTER GUARD FAILED ({len(failures)} failure(s))")
        return 1
    print("APPENDIX POINTER GUARD PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
