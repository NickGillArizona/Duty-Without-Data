"""Fail when the public comment-window presentation becomes stale."""
from __future__ import annotations

import argparse
import datetime as dt
import os
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
CONFIG = REPO / "_config.yml"
PUBLIC_PAGES = (REPO / "README.md", REPO / "index.md", REPO / "COMMENT.md")
DATE_KEY = "comment_window_deadline"
ACTIVE_KEY = "comment_window_active"

ACTIVE_TOKENS = (
    "the current Form HUD-27061 comment window closes",
    "The comment window closes Tuesday",
    "As of that date the comment window is open",
    "Until **August 11, 2026**",
)


def config_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\"'#\r\n]+)", text)
    return match.group(1).strip() if match else None


def display_date(value: dt.date) -> str:
    return f"{value:%B} {value.day}, {value.year}"


def validate(
    check_date: dt.date,
    deadline: dt.date,
    active: bool,
    pages: dict[str, str],
) -> list[str]:
    failures: list[str] = []
    if active and check_date > deadline:
        failures.append(
            f"{ACTIVE_KEY} is true on {check_date.isoformat()}, after "
            f"{deadline.isoformat()}"
        )
    if active:
        date_text = display_date(deadline)
        for path, text in pages.items():
            if date_text not in text:
                failures.append(f"{path} does not state the configured deadline {date_text}")
    else:
        for path, text in pages.items():
            for token in ACTIVE_TOKENS:
                if token in text:
                    failures.append(f"{path} still carries active-window text: {token}")
    return failures


def run_selftest() -> int:
    deadline = dt.date(2026, 8, 11)
    pages = {"README.md": "August 11, 2026"}
    assert validate(dt.date(2026, 8, 12), deadline, True, pages)
    assert validate(dt.date(2026, 8, 1), deadline, True, pages) == []
    assert validate(dt.date(2026, 8, 12), deadline, False, pages) == []
    print("OK: deadline-freshness guard self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()

    try:
        config_text = CONFIG.read_text(encoding="utf-8")
        raw_deadline = config_value(config_text, DATE_KEY)
        raw_active = config_value(config_text, ACTIVE_KEY)
        if raw_deadline is None or raw_active is None:
            raise ValueError(f"{DATE_KEY} and {ACTIVE_KEY} must be set in _config.yml")
        deadline = dt.date.fromisoformat(raw_deadline)
        if raw_active.casefold() not in {"true", "false"}:
            raise ValueError(f"{ACTIVE_KEY} must be true or false")
        active = raw_active.casefold() == "true"
        pages = {
            path.name: path.read_text(encoding="utf-8")
            for path in PUBLIC_PAGES
        }
        check_date = dt.date.fromisoformat(
            os.environ.get("DWD_CHECK_DATE", dt.date.today().isoformat())
        )
    except (OSError, ValueError) as exc:
        print(f"deadline-freshness guard could not prepare its inputs: {exc}", file=sys.stderr)
        return 2

    failures = validate(check_date, deadline, active, pages)
    if failures:
        print("Deadline presentation is stale or inconsistent:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    state = "active" if active else "inactive"
    print(
        f"OK: comment-window presentation is {state} and consistent as of "
        f"{check_date.isoformat()} (configured deadline {deadline.isoformat()})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
