"""Derive the published, minimized analytical datasets from the full research databases.

WHY THIS EXISTS
---------------
The research databases carry per-case free-text fields that the published analyses do
not use: model-written case summaries and holdings, free-text accommodation narratives,
free-text race detail, and property-level city. Aggregating disability-related narrative
across hundreds of cases raises a data-minimization question that is separate from the
fact that court records are public. This archive answers it the way the Note asks HUD to
answer it: publish the fields the published claims need, and no more.

WHAT IT DOES
------------
Removes the fields listed in ``DROP_FIELDS`` from every record of each database. Nothing
else changes: record order, record count, all remaining field values, JSON indentation,
and CRLF line endings are preserved byte-for-byte. The transformation is therefore a pure
projection -- every published number recomputes from the minimized file exactly as it did
from the full file, which ``scripts/recompute_verification.py`` re-checks on every gate run.

The full databases are retained in the project's private research records. Their
registered digests are recorded below so that a reader holding the full data can confirm
that the published file is the stated projection of the registered object rather than a
separately assembled dataset.

RUNNING IT
----------
    python scripts/minimize_public_dataset.py --check    # verify the tree is minimized
    python scripts/minimize_public_dataset.py            # apply (needs the full sources)

``--check`` is what the release gate runs: it confirms no dropped field survives in any
published database, and it does not need the private sources.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Free-text / unnecessary-granularity fields removed from every published database.
# Each entry: field -> why it is not needed to reproduce a published claim.
DROP_FIELDS = {
    "key_holding": "model-written holding summary; no published claim reads it",
    "brief_summary": "model-written case summary; no published claim reads it",
    "accommodation_description": "free-text disability/accommodation narrative",
    "race_if_mentioned": "free-text race detail; the published analysis uses no race field",
    "property_city": "property-level location below the state granularity any claim uses",
}

# Databases published in minimized form, with the indentation each file uses.
TARGETS = {
    "FHA_Unified_Database.json": 1,
    "FHA_3604_Database_unified_20260328_104352.json": 2,
    "FHA_RA_Database_unified_20260328_090852.json": 2,
}

# sha256 over LF-normalized bytes of the FULL databases, as registered on 2026-07-08 and
# retained privately. These are provenance anchors, not files in this repository.
REGISTERED_SOURCE_SHA_LF = {
    "FHA_Unified_Database.json":
        "bc6c4b1091401d82216266b89152a7bb2c4aa72c70c0686f3cff01a0a0bff95a",
}


def sha_lf(raw: bytes) -> str:
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def serialize(records, indent: int) -> bytes:
    """Reproduce the source formatting exactly: given indent, ensure_ascii, CRLF."""
    text = json.dumps(records, indent=indent, ensure_ascii=False)
    return text.replace("\n", "\r\n").encode("utf-8")


def project(records):
    """Drop the minimized-away fields. Pure projection; order and count preserved."""
    out = []
    removed = 0
    for rec in records:
        if not isinstance(rec, dict):
            out.append(rec)
            continue
        new = {k: v for k, v in rec.items() if k not in DROP_FIELDS}
        removed += len(rec) - len(new)
        out.append(new)
    return out, removed


def check() -> int:
    failures = []
    for name in TARGETS:
        path = DATA / name
        if not path.exists():
            failures.append("%s: MISSING" % name)
            continue
        records = json.loads(path.read_text(encoding="utf-8"))
        present = sorted({f for rec in records if isinstance(rec, dict)
                          for f in DROP_FIELDS if f in rec})
        if present:
            failures.append("%s: still carries %s" % (name, ", ".join(present)))
        else:
            print("  OK   %-46s %d records, 0 minimized-away fields"
                  % (name, len(records)))
    if failures:
        print("\nFAIL: public dataset is not minimized")
        for f in failures:
            print("  " + f)
        return 1
    print("\nPASS: no minimized-away field survives in any published database")
    return 0


def apply_() -> int:
    for name, indent in TARGETS.items():
        path = DATA / name
        raw = path.read_bytes()
        records = json.loads(raw.decode("utf-8"))

        # Faithfulness gate: the serializer must reproduce the source bytes exactly
        # before it is trusted to write a projection of them.
        if serialize(records, indent) != raw:
            print("ABORT: serializer is not byte-faithful for %s; nothing written" % name)
            return 1

        source_sha = sha_lf(raw)
        registered = REGISTERED_SOURCE_SHA_LF.get(name)
        if registered and source_sha != registered:
            print("ABORT: %s is not the registered source (sha_lf %s != %s)"
                  % (name, source_sha[:16], registered[:16]))
            return 1

        projected, removed = project(records)
        out = serialize(projected, indent)
        path.write_bytes(out)
        print("  %-46s %d records, %d field values removed" % (name, len(records), removed))
        print("      source sha256_lf  %s" % source_sha)
        print("      published sha256_lf %s" % sha_lf(out))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="verify the published databases are minimized (no sources needed)")
    args = ap.parse_args()
    print("Minimized-away fields: %s" % ", ".join(sorted(DROP_FIELDS)))
    return check() if args.check else apply_()


if __name__ == "__main__":
    sys.exit(main())
