"""Generate RELEASE_MANIFEST.json — one authoritative hash manifest for the release tree.

Covers every git-tracked file (per `git ls-files`) except the manifest itself. For each file it
records size, SHA-256 of the raw bytes, and — for text files — SHA-256 of the LF-normalized bytes
so that a checkout under core.autocrlf can be distinguished from a genuine content change.

Execution-era hash manifests inside replication/comparator/ and method/preregistration/ are
historical provenance records, not verification instruments.

Usage:  python scripts/make_release_manifest.py
Verify: python scripts/check_release_manifest.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "RELEASE_MANIFEST.json"


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO, capture_output=True, check=True
    ).stdout.decode("utf-8")
    return sorted(p for p in out.split("\0") if p and p != MANIFEST.name)


def is_text(data: bytes) -> bool:
    return b"\0" not in data[:8192]


def entry(relpath: str) -> dict:
    data = (REPO / relpath).read_bytes()
    e = {
        "size": len(data),
        "sha256_bytes": hashlib.sha256(data).hexdigest(),
    }
    if is_text(data):
        e["sha256_lf"] = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
    return e


def main() -> None:
    files = tracked_files()
    manifest = {
        "_note": (
            "Authoritative release manifest: every git-tracked file except this manifest. "
            "sha256_bytes is the raw-byte hash; sha256_lf (text files) is the LF-normalized "
            "hash. Verify with scripts/check_release_manifest.py. Execution-era hash manifests "
            "in replication/comparator/ and method/preregistration/ are historical provenance "
            "only."
        ),
        "generated_date": datetime.date.today().isoformat(),
        "file_count": len(files),
        "files": {p: entry(p) for p in files},
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {MANIFEST.name}: {len(files)} files")


if __name__ == "__main__":
    main()
