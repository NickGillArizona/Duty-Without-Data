"""Fail closed if a budgeted editorial surface grows beyond its ceiling."""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
README = REPO / "README.md"
# 900 accommodates the attorney-facing front door (case vignette, administrative-record
# timeline, census statement with finality classes, action-kit table) while still forcing
# a routing page rather than a second report.
CEILING = 900
ARGUMENT = REPO / "article" / "THE_ARGUMENT.md"
# Anchored to the 2026-08-02 strengthened build (measured 2,926 visible words; the
# author-ratified working hold is ~2,900 by plain word count). The page is the
# fifteen-minute compression; this guard blocks silent regrowth into a second
# manuscript rather than enforcing a design target.
ARGUMENT_CEILING = 2950


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
    argument_words = visible_words(ARGUMENT.read_text(encoding="utf-8"))
    if len(argument_words) > ARGUMENT_CEILING:
        print(f"FAIL: THE_ARGUMENT has {len(argument_words)} visible words; "
              f"ceiling is {ARGUMENT_CEILING}.")
        return 1
    print(f"PASS: README has {len(words)} visible words (ceiling {CEILING}); "
          f"THE_ARGUMENT has {len(argument_words)} (ceiling {ARGUMENT_CEILING}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
