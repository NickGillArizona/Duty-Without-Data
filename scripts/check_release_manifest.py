"""Verify the release tree against RELEASE_MANIFEST.json.

Recomputes hashes for every git-tracked file and compares against the manifest:

- MISSING  — file in the manifest but not tracked in this clone;
- EXTRA    — tracked file absent from the manifest;
- MISMATCH — raw-byte hash differs AND the LF-normalized hash differs (content change);
- LINE-ENDINGS — raw-byte hash differs but the LF-normalized hash matches (checkout
  translation under core.autocrlf; reported as a warning, not a failure).

Exit code 0 only when there are no MISSING, EXTRA, or MISMATCH entries.

Usage: python scripts/check_release_manifest.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "RELEASE_MANIFEST.json"


def tracked_files() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO, capture_output=True, check=True
    ).stdout.decode("utf-8")
    return {p for p in out.split("\0") if p and p != MANIFEST.name}


def main() -> int:
    if not MANIFEST.exists():
        print("FAIL: RELEASE_MANIFEST.json not found")
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = manifest["files"]
    actual = tracked_files()

    missing = sorted(set(expected) - actual)
    extra = sorted(actual - set(expected))
    mismatched: list[str] = []
    line_endings_only: list[str] = []

    for relpath in sorted(set(expected) & actual):
        data = (REPO / relpath).read_bytes()
        want = expected[relpath]
        if hashlib.sha256(data).hexdigest() == want["sha256_bytes"]:
            continue
        lf = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
        if want.get("sha256_lf") and lf == want["sha256_lf"]:
            line_endings_only.append(relpath)
        else:
            mismatched.append(relpath)

    for label, items in [("MISSING", missing), ("EXTRA", extra), ("MISMATCH", mismatched)]:
        for p in items:
            print(f"{label}: {p}")
    for p in line_endings_only:
        print(f"LINE-ENDINGS (warning only): {p}")

    if missing or extra or mismatched:
        print(
            f"FAIL: {len(missing)} missing, {len(extra)} extra, {len(mismatched)} mismatched "
            f"({len(line_endings_only)} line-ending-only warnings)"
        )
        return 1
    print(
        f"OK: {len(expected)} manifest entries verified "
        f"({len(line_endings_only)} line-ending-only warnings)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
