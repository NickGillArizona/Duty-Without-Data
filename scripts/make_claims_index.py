"""Generate article/CLAIMS_INDEX.md — the reader-facing view of the claims ledger.

Reads article/CLAIMS_LEDGER.csv and writes a deterministic Markdown index: one
entry per registered claim, with its Note location, claim text, source type,
primary source or tier, evidence route, and confidence tier. The CSV remains
the machine surface; this page is its human-readable rendering. Regenerate
after any ledger change; the release gate fails if the two drift.

Usage:
  python scripts/make_claims_index.py           # write the index
  python scripts/make_claims_index.py --check   # exit 1 if the committed index drifts
"""
import csv
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "article", "CLAIMS_LEDGER.csv")
OUT = os.path.join(REPO, "article", "CLAIMS_INDEX.md")

HEADER = """# Claims Index

Generated from [`CLAIMS_LEDGER.csv`](CLAIMS_LEDGER.csv) by
`scripts/make_claims_index.py`; do not edit this page by hand. Each entry
states where the claim appears in the Note, the claim text as registered, the
source type, the primary source or tier, the evidence route, and the ledger's
confidence tier. The release gate verifies the ledger row-by-row and verifies
that this page matches the ledger. Rows whose evidence route rests on the
cited primary source plus privately retained material should be verified at
the primary source itself (see
[`EVIDENCE_AND_LIMITS.md`](EVIDENCE_AND_LIMITS.md)).

## Registered claims
"""


def one_line(text: str) -> str:
    return " ".join(text.split())


def render() -> str:
    with open(LEDGER, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    parts = [HEADER]
    for r in rows:
        parts.append(f"\n### {r['claim_id']} — {one_line(r['note_location'])}\n\n")
        parts.append(f"> {one_line(r['claim_text'])}\n\n")
        parts.append(f"- **Source type:** {one_line(r['source_type'])}\n")
        parts.append(
            f"- **Primary source / tier:** {one_line(r['primary_source_or_tier'])}\n"
        )
        parts.append(f"- **Evidence route:** `{one_line(r['replication_artifact'])}`\n")
        parts.append(f"- **Confidence tier:** {one_line(r['confidence_tier'])}\n")
    return "".join(parts)


def main() -> int:
    rendered = render()
    if "--check" in sys.argv[1:]:
        try:
            with open(OUT, encoding="utf-8", newline="") as f:
                committed = f.read()
        except OSError:
            print("FAIL: article/CLAIMS_INDEX.md is missing; regenerate it.")
            return 1
        if committed.replace("\r\n", "\n") != rendered:
            print(
                "FAIL: article/CLAIMS_INDEX.md does not match the ledger; "
                "regenerate with scripts/make_claims_index.py."
            )
            return 1
        print(f"OK: CLAIMS_INDEX.md matches the ledger ({rendered.count(chr(10))} lines).")
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(rendered)
    print("wrote article/CLAIMS_INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
