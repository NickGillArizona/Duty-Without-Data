#!/usr/bin/env python3
"""Guard the take-action kit against unfinished and time-bound text.

The templates in action/ are meant to be downloaded and used: a comment, a
petition, a complaint, a declaration. A reader cannot tell a finished template
from a draft one, so anything left half-written in them travels straight into a
filing -- an unfilled docket stub, a bracketed reminder to check something
before filing, an editorial aside, a sentence pinned to a date that has passed,
or a note that an attached figure was never rebuilt. This guard asserts that no
page in the kit carries that kind of text, that every template still tells the
reader it is not legal advice, and that any page describing the status of the
information-collection keeps both possibilities open rather than asserting an
outcome that has not been announced. A missing action/ directory is reported as
a clean pass with a note.

Usage:
  python scripts/check_action_canonicality.py             # scan; exit 1 on any hit
  python scripts/check_action_canonicality.py --selftest  # fixture self-test only
  python scripts/check_action_canonicality.py --repo PATH # scan a repo elsewhere

Exit codes: 0 clean (or directory absent), 1 violations (or self-test failure).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACTION_DIR = "action"

# ---------------------------------------------------------------------------
# Forbidden text. Each: id, compiled pattern, description. Line-level.
# ---------------------------------------------------------------------------

FORBIDDEN = [
    ("A-TOBEREMOVED", re.compile(r"(?i)\(to be removed"),
     "editorial aside left in a template a reader will file"),
    ("A-VERIFYATFILING", re.compile(r"(?i)\[VERIFY AT FILING"),
     "unresolved pre-filing reminder left in the template"),
    ("A-DOCKETSTUB", re.compile(r"(?i)HUD-2026-NNNN"),
     "unfilled docket-number stub"),
    ("A-ONCEPUBLISHES", re.compile(r"(?i)\bonce HUD publishes\b"),
     "text conditioned on a future publication the reader cannot check"),
    ("A-PLACEHOLDER", re.compile(r"(?i)\bplaceholders?\b"),
     "self-declared placeholder text"),
    ("A-NOTREGENERATED", re.compile(r"(?i)\bnot been regenerated\b"),
     "attached material disclosed as out of date"),
    ("A-STALEDATE", re.compile(r"(?i)\bAs of April 18\b"),
     "sentence pinned to a superseded date"),
]

# ---------------------------------------------------------------------------
# Required text. Whole-file, whitespace-normalized so a required phrase split
# across a line wrap still counts.
# ---------------------------------------------------------------------------

# A-HEDGE. The literal phrase "not legal advice" is the core, but the hedge is
# written several ways in practice: "This is not legal advice", "does not
# constitute legal advice", "is not intended as legal advice", "nothing here is
# legal advice". The pattern therefore anchors on a negation followed, within
# one clause (no sentence-ending period, at most 60 characters), by the phrase
# "legal advice". That is deliberately wider than a bare literal so a correctly
# hedged page is not failed for phrasing, and deliberately narrower than
# "legal advice" alone so a page that merely offers legal advice is not passed.
HEDGE_RE = re.compile(
    r"(?i)\b(?:not|no|none|nothing|neither|never)\b[^.\n]{0,60}\blegal advice\b")

# A-TWOBRANCH. Required only of a page that states the collection's status (see
# STATUS_TRIGGER below). The page must keep BOTH branches open -- renewed, or
# not yet disposed of -- rather than asserting a lapse or a renewal that has
# not been announced. One pattern, several accepted phrasings; all of them
# express the same thing: the outcome is not yet posted.
TWO_BRANCH_RE = re.compile(
    r"(?i)(?:"
    r"whether\s+HUD\s+(?:has\s+|had\s+|will\s+)?renew\w*"
    r"|whether\s+(?:the\s+)?(?:collection|form|clearance)\s+"
    r"(?:was\s+|is\s+|has\s+been\s+)?renew\w*"
    r"|renewal\s+remains\s+pending"
    r"|has\s+not\s+(?:yet\s+)?posted\s+a\s+disposition"
    r"|no\s+disposition\s+(?:has\s+been\s+)?(?:yet\s+)?(?:been\s+)?posted"
    r"|(?:either\s+)?renewed\s+or\s+(?:allowed\s+to\s+)?laps\w*"
    r"|renewed\s+nor\s+(?:formally\s+)?laps\w*"
    r")")

# A page "states the collection's status" when a line names the collection AND
# carries a status word. Line-level so the report can point at the sentence
# that created the obligation.
STATUS_SUBJECT = re.compile(r"(?i)(?:\b27061\b|\b2535-0113\b)")
STATUS_WORD = re.compile(
    r"(?i)\b(?:expir\w*|laps\w*|renew\w*|disposition|withdraw\w*|extension)\b")

REQUIRED_RULES = {
    "A-HEDGE": (HEDGE_RE, "a not-legal-advice hedge"),
    "A-TWOBRANCH": (TWO_BRANCH_RE,
                    "a both-branches-open statement of the collection's status"),
}

# Which requirements apply to which page, by filename. "*" is the default for
# any action/ page not listed. To exempt a page from a requirement, remove that
# rule id from its list -- do not weaken the pattern. A-TWOBRANCH is
# conditional: it is enforced only on pages that state the collection's status,
# so listing it on a page that never mentions the collection costs nothing.
REQUIRED = {
    "*": ["A-HEDGE", "A-TWOBRANCH"],
    "2026_comment_template.md": ["A-HEDGE", "A-TWOBRANCH"],
    "553e_petition_template.md": ["A-HEDGE", "A-TWOBRANCH"],
    "553e_petition_individual.md": ["A-HEDGE", "A-TWOBRANCH"],
    "comment_memo_2026.md": ["A-HEDGE", "A-TWOBRANCH"],
    "complaint_template.md": ["A-HEDGE", "A-TWOBRANCH"],
    "complaint_template_with_links.md": ["A-HEDGE", "A-TWOBRANCH"],
    "declaration_template.md": ["A-HEDGE", "A-TWOBRANCH"],
    "foia_standing_note.md": ["A-HEDGE", "A-TWOBRANCH"],
    "standing_brief.md": ["A-HEDGE", "A-TWOBRANCH"],
    "README.md": ["A-HEDGE", "A-TWOBRANCH"],
}

# Files a specific forbidden phrase is permitted on, by repository-relative
# POSIX path -> list of rule ids. Ships EMPTY: every entry is a standing
# exception to a kit that is meant to be filed as written.
ALLOWLIST: dict[str, list[str]] = {
    # "action/README.md": ["A-PLACEHOLDER"],
}

SKIP_FILES = {os.path.basename(__file__)}


def scan_document(name: str, text: str):
    """Return [(lineno_or_None, rule_id, detail)] for one action/ page.

    lineno is None for a whole-file requirement that has no single offending
    line (A-HEDGE); it is the line that created the obligation for
    A-TWOBRANCH; it is the offending line for every forbidden rule.
    """
    findings = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        for rid, rx, desc in FORBIDDEN:
            for m in rx.finditer(line):
                findings.append((i, rid, f"{m.group(0)!r} -- {desc}"))

    normalized = re.sub(r"\s+", " ", text)
    wanted = REQUIRED.get(name, REQUIRED.get("*", []))

    if "A-HEDGE" in wanted and not HEDGE_RE.search(normalized):
        findings.append((None, "A-HEDGE",
                         "required: " + REQUIRED_RULES["A-HEDGE"][1]
                         + " (no negated 'legal advice' clause found)"))

    if "A-TWOBRANCH" in wanted:
        trigger = None
        for i, line in enumerate(lines, 1):
            if STATUS_SUBJECT.search(line) and STATUS_WORD.search(line):
                trigger = i
                break
        if trigger is not None and not TWO_BRANCH_RE.search(normalized):
            findings.append((trigger, "A-TWOBRANCH",
                             "required: " + REQUIRED_RULES["A-TWOBRANCH"][1]
                             + " (this page states the collection's status but "
                               "does not keep both branches open)"))
    return findings


def scan_targets() -> list[str] | None:
    """Every *.md under action/, or None if the directory is absent."""
    base = os.path.join(REPO, ACTION_DIR)
    if not os.path.isdir(base):
        return None
    targets = []
    for root, dirs, names in os.walk(base):
        dirs[:] = [d for d in sorted(dirs) if d not in {".git", "__pycache__"}]
        for name in sorted(names):
            if name in SKIP_FILES:
                continue
            if name.lower().endswith(".md"):
                targets.append(os.path.join(root, name))
    return targets


HEDGE = "Nothing in this template is legal advice."
TWOBRANCH = ("The record does not show whether HUD renewed the collection; "
             "HUD has not yet posted a disposition.")
STATUS_LINE = "Form HUD-27061 (OMB 2535-0113) passed its displayed expiration."

POSITIVE_CASES = [
    ("complaint_template.md",
     f"# Complaint\n\n{HEDGE}\n\nName (to be removed before filing)\n",
     "A-TOBEREMOVED"),
    ("553e_petition_template.md",
     f"# Petition\n\n{HEDGE}\n\nCite [VERIFY AT FILING] the current rule.\n",
     "A-VERIFYATFILING"),
    ("2026_comment_template.md",
     f"# Comment\n\n{HEDGE}\n\nDocket HUD-2026-NNNN, submit via regulations.gov\n",
     "A-DOCKETSTUB"),
    ("standing_brief.md",
     f"# Brief\n\n{HEDGE}\n\nThis section applies once HUD publishes the notice.\n",
     "A-ONCEPUBLISHES"),
    ("declaration_template.md",
     f"# Declaration\n\n{HEDGE}\n\n[placeholder for the declarant's address]\n",
     "A-PLACEHOLDER"),
    ("comment_memo_2026.md",
     f"# Memo\n\n{HEDGE}\n\nThe attached figure has not been regenerated.\n",
     "A-NOTREGENERATED"),
    ("foia_standing_note.md",
     f"# Note\n\n{HEDGE}\n\nAs of April 18, no response had been received.\n",
     "A-STALEDATE"),
    ("complaint_template_with_links.md",
     "# Complaint\n\nFile this with the nearest FHEO office.\n",
     "A-HEDGE"),
    ("README.md",
     f"# Take action\n\n{HEDGE}\n\n{STATUS_LINE}\nThe collection has lapsed.\n",
     "A-TWOBRANCH"),
]

NEGATIVE_CASES = [
    ("complaint_template.md",
     f"# Complaint\n\n{HEDGE}\n\nDescribe the accommodation you requested.\n",
     "clean template with the hedge and no status claim"),
    ("README.md",
     f"# Take action\n\nThis kit is not legal advice.\n\n{STATUS_LINE}\n{TWOBRANCH}\n",
     "status stated and both branches kept open"),
    ("standing_brief.md",
     "# Brief\n\nThis material does not constitute legal advice.\n\n"
     "Standing is addressed in Part III.\n",
     "alternate hedge phrasing accepted"),
    ("declaration_template.md",
     "# Declaration\n\nNothing here is intended as legal advice.\n\n"
     "The place holder was removed.\n",
     "'place holder' spaced is not the label; hedge present"),
    ("comment_memo_2026.md",
     f"# Memo\n\n{HEDGE}\n\nThe agency published the notice on 2026-06-01.\n",
     "'publishes' in the past tense, not the conditional stub"),
    ("553e_petition_individual.md",
     f"# Petition\n\n{HEDGE}\n\nAs of April 2026 the rule remained in force.\n",
     "a date that is not the pinned stale date"),
    ("foia_standing_note.md",
     f"# Note\n\n{HEDGE}\n\nThe request was acknowledged; no records were withheld.\n",
     "no status claim, so no both-branches obligation"),
]


def selftest(quiet: bool = False) -> int:
    """Fixture self-test on synthetic pages; touches no repository file.

    Run before any scan is reported clean. The negative fixtures matter as much
    as the positive ones: they encode the phrasings a correctly finished page
    is allowed to use, so widening a pattern later fails here rather than
    quietly failing a good page.
    """
    if not quiet:
        print(f"check_action_canonicality self-test: {len(POSITIVE_CASES)} positive "
              f"/ {len(NEGATIVE_CASES)} negative fixtures")
    failures = 0
    for name, text, want in POSITIVE_CASES:
        hits = scan_document(name, text)
        ok = any(h[1] == want for h in hits)
        if not quiet or not ok:
            print(f"  {'PASS' if ok else 'FAIL'}  POS [{want:<16}] {name}"
                  + ("" if ok else f"  -> got {hits}"))
        failures += int(not ok)
    for name, text, why in NEGATIVE_CASES:
        hits = scan_document(name, text)
        ok = not hits
        if not quiet or not ok:
            print(f"  {'PASS' if ok else 'FAIL'}  NEG [{why}] {name}"
                  + ("" if ok else f"  -> spurious {hits}"))
        failures += int(not ok)
    total = len(POSITIVE_CASES) + len(NEGATIVE_CASES)
    if not quiet or failures:
        print(f"self-test: {total - failures}/{total} passed")
    return 1 if failures else 0


def read_text(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (UnicodeDecodeError, OSError):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                return f.read()
        except OSError:
            return ""


def main() -> int:
    global REPO
    ap = argparse.ArgumentParser(description="Take-action kit canonicality guard.")
    ap.add_argument("--selftest", "--self-test", dest="selftest",
                    action="store_true",
                    help="run the embedded fixtures only; touches no repo file")
    ap.add_argument("--repo", default=None,
                    help="repository root to scan (default: the parent of this "
                         "script's directory, as the other release checks resolve it)")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.repo:
        REPO = os.path.abspath(args.repo)

    if selftest(quiet=True) != 0:
        print("FAIL: fixture self-test failed; scan result not trustworthy")
        return 1

    targets = scan_targets()
    if targets is None:
        print(f"OK: no {ACTION_DIR}/ directory at {REPO}; "
              f"nothing to check (note: the kit may not be in place yet)")
        return 0

    findings = []
    allowed = 0
    for path in targets:
        rel = os.path.relpath(path, REPO).replace("\\", "/")
        name = os.path.basename(path)
        for lineno, rid, detail in scan_document(name, read_text(path)):
            if rid in ALLOWLIST.get(rel, []):
                allowed += 1
                continue
            findings.append((rel, lineno, rid, detail))

    for rel, lineno, rid, detail in findings:
        loc = f"{rel}:{lineno}" if lineno is not None else f"{rel} (whole file)"
        print(f"ACTION-CANON {loc} [{rid}] {detail}")
    if findings:
        print(f"FAIL: {len(findings)} take-action hit(s) across "
              f"{len({f[0] for f in findings})} file(s); "
              f"{len(targets)} pages checked, {allowed} allowlisted")
        return 1
    print(f"OK: take-action kit is canonical ({len(targets)} pages checked, "
          f"{len(FORBIDDEN)} forbidden rules, {len(REQUIRED_RULES)} required rules, "
          f"{allowed} allowlisted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
