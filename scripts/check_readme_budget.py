"""Fail closed if the public README grows beyond its editorial budget."""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
README = REPO / "README.md"
# 900 accommodates the attorney-facing front door (case vignette, administrative-record
# timeline, census statement with finality classes, action-kit table) while still forcing
# a routing page rather than a second report.
CEILING = 900


def visible_words(markdown: str) -> list[str]:
    text = re.sub(r"<!--.*?-->", " ", markdown, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", " ", text)
    return re.findall(r"\b[\w§'-]+\b", text, flags=re.UNICODE)


def main() -> int:
    markdown = README.read_text(encoding="utf-8")
    words = visible_words(markdown)
    if len(words) > CEILING:
        print(f"FAIL: README has {len(words)} visible words; ceiling is {CEILING}.")
        return 1
    required = (
        "## What the archive shows",
        "## Check, do not just trust",
        "article/appendices/README.md",
        "replication/VERIFY_ONE_CLAIM.md",
    )
    missing = [marker for marker in required if marker not in markdown]
    if missing:
        print("FAIL: README is missing required route(s): " + ", ".join(missing))
        return 1
    print(f"PASS: README has {len(words)} visible words (ceiling {CEILING}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
