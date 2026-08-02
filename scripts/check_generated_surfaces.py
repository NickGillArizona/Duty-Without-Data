"""Gate check: generated surfaces stay in sync and dated status stays fresh.

Four assertions:

1. article/CLAIMS_INDEX.md matches article/CLAIMS_LEDGER.csv. The rendering is
   delegated to scripts/make_claims_index.py (imported, not duplicated); only
   the comparison lives here.
2. _data/series.yml matches results/series_2026-07.json. The rendering is
   delegated to scripts/make_site_data.py. If the site-data generator is not
   present, the assertion is skipped with a printed note.
3. Record-page dated status is fresh. In record/**/*.md, a dated STATUS line
   must carry a date no older than the newest dated event in
   record/hud-27061/CHRONOLOGY.md. A status line is (a) an "as of <date>"
   statement on a line that also carries status vocabulary ("current",
   "posted", "disposition", "pending", "status", "expiration", "lapse",
   "renewal"), or (b) a NOT YET PUBLISHED marker, which must be dated to be
   checkable and therefore fails when it carries no date at all. When a
   date directly follows "as of", that date governs; otherwise the newest
   date on the line does. Historical references without status vocabulary
   ("the regulation as of Sept. 27, 2022 (verbatim)") are records of a past
   state, cannot go stale, and are not checked; CHRONOLOGY.md itself is the
   reference and its dated event rows are exempt. A month-year date
   ("July 2026") resolves to the last day of its month. This assertion
   closes the gap that let a stale record README reach v1.0.0.
4. Appendix-count consistency: everywhere a reader surface states the number
   of appendices in words ("fifteen appendices"), the word equals the count
   of article/appendices/Appendix_*.md files actually present. Scanned: all
   tracked *.md except results/ (labeled historical and as-run artifacts),
   the manuscript mirror (content-locked), and the frozen verbatim
   instruments (as-run wording by design).
5. Footnote-index correspondence: every raw footnote registered in
   scripts/appendix_pointer_assertions.json has a row in
   article/FOOTNOTE_INDEX.md, and that row names the registered target
   file. (The index may carry additional rows for routes outside the
   registered set; those are guarded by the link check, not here.)

Usage:
  python scripts/check_generated_surfaces.py             # gate mode
  python scripts/check_generated_surfaces.py --selftest  # fixture tests
"""
from __future__ import annotations

import calendar
import datetime as dt
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CHRONOLOGY = os.path.join(REPO, "record", "hud-27061", "CHRONOLOGY.md")
RECORD_DIR = os.path.join(REPO, "record")
APPENDIX_DIR = os.path.join(REPO, "article", "appendices")

WORDS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
         "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
         "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
         "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
         "twenty": 20}

MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sept": 9, "sep": 9,
    "october": 10, "oct": 10, "november": 11, "nov": 11,
    "december": 12, "dec": 12,
}
MONTH_RX = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
# Full date: "July 6, 2026" / "Sept. 13, 1988" / "2026-08-01".
FULL_DATE_RE = re.compile(
    rf"(?:(?P<mon>{MONTH_RX})\.?\s+(?P<day>\d{{1,2}}),\s*(?P<year>\d{{4}}))"
    r"|(?:(?P<iso>\d{4}-\d{2}-\d{2}))"
)
# Month-year date with no day: "July 2026" (not followed by a day-comma form).
MONTH_YEAR_RE = re.compile(rf"(?P<mon>{MONTH_RX})\.?\s+(?P<year>\d{{4}})")

AS_OF_RE = re.compile(r"\bas of\b", re.IGNORECASE)
STATUS_VOCAB = ("current", "posted", "disposition", "pending", "status",
                "expiration", "lapse", "renewal")
NOT_YET_RE = re.compile(r"NOT YET PUBLISHED")

APPENDIX_COUNT_RE = re.compile(
    r"\b(" + "|".join(WORDS) + r")[\s-]+appendices\b", re.IGNORECASE)
# Assertion-4 exclusions (repository-relative POSIX prefixes or exact paths).
COUNT_SCAN_EXCLUDE = (
    "results/",                          # labeled historical / as-run artifacts
    "manuscript/Duty_Without_Data.md",   # content-locked manuscript mirror
    "method/preregistration/",           # frozen verbatim instruments
    "replication/comparator/PREDICTIONS.md",
)


def parse_full_dates(text: str) -> list[dt.date]:
    """Every fully specified date (month-day-year or ISO) in text."""
    found: list[dt.date] = []
    for m in FULL_DATE_RE.finditer(text):
        try:
            if m.group("iso"):
                found.append(dt.date.fromisoformat(m.group("iso")))
            else:
                mon = MONTHS[m.group("mon").rstrip(".").casefold()]
                found.append(dt.date(int(m.group("year")), mon, int(m.group("day"))))
        except (KeyError, ValueError):
            continue
    return found


def _month_year_dates(text: str) -> list[dt.date]:
    """Month-year forms not already part of a full date, at month end."""
    dates: list[dt.date] = []
    stripped = FULL_DATE_RE.sub(" ", text)
    for m in MONTH_YEAR_RE.finditer(stripped):
        try:
            mon = MONTHS[m.group("mon").rstrip(".").casefold()]
            year = int(m.group("year"))
            dates.append(dt.date(year, mon, calendar.monthrange(year, mon)[1]))
        except (KeyError, ValueError):
            continue
    return dates


def parse_line_date(line: str) -> dt.date | None:
    """The governing date for a status line. A date directly following an
    "as of" governs (newest, if several "as of" occurrences); otherwise the
    newest date anywhere on the line. Month-year forms resolve to the last
    day of their month. Returns None when the line carries no parseable
    date."""
    as_of_dates: list[dt.date] = []
    for m in AS_OF_RE.finditer(line):
        window = line[m.end():m.end() + 24].lstrip()
        candidates = parse_full_dates(window) or _month_year_dates(window)
        for d in candidates:
            head = window[:20]
            # Only count a date that starts the window (directly follows).
            if FULL_DATE_RE.match(window) or MONTH_YEAR_RE.match(head):
                as_of_dates.append(d)
            break
    if as_of_dates:
        return max(as_of_dates)
    dates = parse_full_dates(line) + _month_year_dates(line)
    return max(dates) if dates else None


def newest_chronology_event(chronology_text: str) -> dt.date | None:
    """Newest fully dated event in the chronology's Date column."""
    newest: dt.date | None = None
    for line in chronology_text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or cells[0].startswith("---") or cells[0] == "Date":
            continue
        for d in parse_full_dates(cells[0]):
            if newest is None or d > newest:
                newest = d
    return newest


def check_record_freshness(reference: dt.date,
                           pages: dict[str, str]) -> list[str]:
    """Assertion 3 core. pages: repo-relative POSIX path -> text."""
    failures: list[str] = []
    for rel, text in pages.items():
        for lineno, line in enumerate(text.splitlines(), start=1):
            low = line.casefold()
            is_not_yet = bool(NOT_YET_RE.search(line))
            is_status_as_of = (AS_OF_RE.search(line)
                               and any(w in low for w in STATUS_VOCAB))
            if not (is_not_yet or is_status_as_of):
                continue
            line_date = parse_line_date(line)
            if line_date is None:
                if is_not_yet:
                    failures.append(
                        f"{rel}:{lineno}: NOT YET PUBLISHED marker carries no "
                        f"date and cannot be freshness-checked")
                continue
            if line_date < reference:
                failures.append(
                    f"{rel}:{lineno}: dated status ({line_date.isoformat()}) is "
                    f"older than the newest chronology event "
                    f"({reference.isoformat()})")
    return failures


def check_appendix_count(n_files: int, pages: dict[str, str]) -> list[str]:
    """Assertion 4 core. pages: repo-relative POSIX path -> text."""
    failures: list[str] = []
    for rel, text in pages.items():
        # Collapse hard wraps so "fifteen\nappendices" still matches.
        flat = re.sub(r"\s+", " ", text)
        for m in APPENDIX_COUNT_RE.finditer(flat):
            stated = WORDS[m.group(1).casefold()]
            if stated != n_files:
                failures.append(
                    f"{rel}: states {m.group(1)!r} appendices but "
                    f"{n_files} Appendix_*.md files are present")
    return failures


def check_footnote_index(pointers: list[dict], index_text: str) -> list[str]:
    """Assertion 5 core. pointers: parsed registry records; index_text: the
    footnote index page."""
    failures: list[str] = []
    rows: dict[str, str] = {}
    for line in index_text.splitlines():
        m = re.match(r"\|\s*\[\^(\d+)\]\s*\|", line)
        if m:
            rows[m.group(1)] = rows.get(m.group(1), "") + line
    for p in pointers:
        fn = str(p["raw_footnote"])
        basename = p["target_file"].rsplit("/", 1)[-1]
        if fn not in rows:
            failures.append(
                f"article/FOOTNOTE_INDEX.md: registered footnote [^{fn}] has "
                f"no index row")
        elif basename not in rows[fn]:
            failures.append(
                f"article/FOOTNOTE_INDEX.md: row [^{fn}] does not name the "
                f"registered target {basename}")
    return failures


def iter_markdown(root: str) -> list[str]:
    out: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in {".git", "__pycache__", ".pytest_cache"}]
        for name in filenames:
            if name.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, name), root)
                out.append(rel.replace(os.sep, "/"))
    return sorted(out)


def run_gate() -> int:
    failures: list[str] = []

    # 1. Claims index drift (renderer delegated to make_claims_index).
    import make_claims_index
    try:
        with open(make_claims_index.OUT, encoding="utf-8", newline="") as f:
            committed = f.read()
        if committed.replace("\r\n", "\n") != make_claims_index.render():
            failures.append(
                "article/CLAIMS_INDEX.md does not match the ledger; regenerate "
                "with scripts/make_claims_index.py")
    except OSError:
        failures.append("article/CLAIMS_INDEX.md is missing; regenerate it")

    # 2. Site data drift (renderer delegated to make_site_data).
    if os.path.exists(os.path.join(REPO, "scripts", "make_site_data.py")):
        import make_site_data
        try:
            with open(make_site_data.OUT, encoding="utf-8", newline="") as f:
                committed = f.read()
            if committed.replace("\r\n", "\n") != make_site_data.render():
                failures.append(
                    "_data/series.yml does not match the series of record; "
                    "regenerate with scripts/make_site_data.py")
        except OSError:
            failures.append("_data/series.yml is missing; regenerate it")
    else:
        print("note: scripts/make_site_data.py not present; site-data "
              "assertion skipped")

    # 3. Record dated-status freshness.
    with open(CHRONOLOGY, encoding="utf-8") as f:
        reference = newest_chronology_event(f.read())
    if reference is None:
        failures.append("record/hud-27061/CHRONOLOGY.md has no dated event row")
    else:
        pages: dict[str, str] = {}
        for rel in iter_markdown(RECORD_DIR):
            if rel.endswith("CHRONOLOGY.md"):
                continue  # the reference itself; its event rows are history
            path = os.path.join(RECORD_DIR, rel)
            with open(path, encoding="utf-8") as f:
                pages["record/" + rel] = f.read()
        failures.extend(check_record_freshness(reference, pages))

    # 4. Appendix-count consistency.
    n_files = len([n for n in os.listdir(APPENDIX_DIR)
                   if n.startswith("Appendix_") and n.endswith(".md")])
    pages = {}
    for rel in iter_markdown(REPO):
        if any(rel == e or rel.startswith(e) for e in COUNT_SCAN_EXCLUDE):
            continue
        with open(os.path.join(REPO, rel), encoding="utf-8") as f:
            pages[rel] = f.read()
    failures.extend(check_appendix_count(n_files, pages))

    # 5. Footnote-index correspondence with the pointer registry.
    import json
    with open(os.path.join(REPO, "scripts", "appendix_pointer_assertions.json"),
              encoding="utf-8") as f:
        pointers = json.load(f)["pointers"]
    with open(os.path.join(REPO, "article", "FOOTNOTE_INDEX.md"),
              encoding="utf-8") as f:
        failures.extend(check_footnote_index(pointers, f.read()))

    if failures:
        print("Generated-surface failures:", file=sys.stderr)
        for f_ in failures:
            print(f"  {f_}", file=sys.stderr)
        return 1
    ref = reference.isoformat() if reference else "n/a"
    print(f"OK: claims index and site data match their sources; record dated "
          f"status is fresh against {ref}; appendix count word matches "
          f"{n_files} files on {len(pages)} scanned surfaces; footnote index "
          f"carries all {len(pointers)} registered routes.")
    return 0


def run_selftest() -> int:
    chron = (
        "| Date | Event | Source |\n"
        "|---|---|---|\n"
        "| Sept. 13, 1988 | Enactment. | Pub. L. |\n"
        "| June 12, 2026 | Notice; comments due August 11, 2026. | 91 FR |\n"
        "| July 6, 2026 | Comment filed (posted July 7, 2026). | docket |\n"
    )
    ref = newest_chronology_event(chron)
    fresh_pages = {
        "record/x/README.md": (
            "Contents current as of July 2026.\n"
            "| 2026-06-30 | no OMB disposition posted as of 2026-08-01 |\n"
        ),
        "record/x/analysis.md": (
            "## Part 121 as of Sept. 27, 2022 (verbatim)\n"
            "records in its control as of the date of this request\n"
        ),
    }
    stale_pages = {"record/x/README.md": "Contents current as of May 2026.\n"}
    undated_pages = {"record/x/status.md": "The disposition is NOT YET PUBLISHED.\n"}
    dated_marker = {"record/x/status.md":
                    "NOT YET PUBLISHED as of August 1, 2026.\n"}
    cases = [
        ("chronology max is the Date column, not a due date",
         ref == dt.date(2026, 7, 6), True),
        ("month-year resolves to month end",
         parse_line_date("current as of July 2026") == dt.date(2026, 7, 31), True),
        ("fresh status passes",
         check_record_freshness(dt.date(2026, 7, 6), fresh_pages) == [], True),
        ("historical as-of without status vocabulary is skipped",
         check_record_freshness(dt.date(2026, 7, 6),
                                {"record/x/analysis.md":
                                 fresh_pages["record/x/analysis.md"]}) == [],
         True),
        ("stale status fails (negative control)",
         bool(check_record_freshness(dt.date(2026, 7, 6), stale_pages)), True),
        ("undated NOT YET PUBLISHED fails (negative control)",
         bool(check_record_freshness(dt.date(2026, 7, 6), undated_pages)), True),
        ("dated NOT YET PUBLISHED marker passes when fresh",
         check_record_freshness(dt.date(2026, 7, 6), dated_marker) == [], True),
        ("as-of date governs over a fresher date elsewhere on the line "
         "(negative control)",
         bool(check_record_freshness(
             dt.date(2026, 7, 6),
             {"record/x/s.md": "On August 1, 2026 the office noted no "
              "disposition posted as of June 1, 2026.\n"})), True),
        ("event date does not mask a fresh as-of date",
         check_record_freshness(
             dt.date(2026, 7, 6),
             {"record/x/s.md": "| 2026-06-30 | no OMB disposition posted "
              "as of 2026-08-01 |\n"}) == [], True),
        ("matching appendix count passes",
         check_appendix_count(15, {"a.md": "the fifteen appendices support"}) == [],
         True),
        ("wrapped count word still matches",
         bool(check_appendix_count(14, {"a.md": "the fifteen\nappendices"})), True),
        ("count mismatch fails (negative control)",
         bool(check_appendix_count(14, {"a.md": "fifteen appendices"})), True),
        ("footnote row naming registered target passes",
         check_footnote_index(
             [{"raw_footnote": "86", "target_file": "article/appendices/App_E.md"}],
             "| [^86] | II | claim | [`App_E.md`](appendices/App_E.md) |\n") == [],
         True),
        ("missing footnote row fails (negative control)",
         bool(check_footnote_index(
             [{"raw_footnote": "87", "target_file": "a/App_M.md"}],
             "| [^86] | II | claim | route |\n")), True),
        ("row missing the registered target fails (negative control)",
         bool(check_footnote_index(
             [{"raw_footnote": "86", "target_file": "a/App_E.md"}],
             "| [^86] | II | claim | [`Other.md`](Other.md) |\n")), True),
        ("generated-file drift comparison fails on difference "
         "(negative control)",
         "a\nb\n".replace("\r\n", "\n") != "a\nc\n", True),
    ]
    passed = 0
    for name, got, want in cases:
        ok = got == want
        passed += int(ok)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"self-test: {passed}/{len(cases)} passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(run_selftest() if "--selftest" in sys.argv[1:] else run_gate())
