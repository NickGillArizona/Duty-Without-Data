#!/usr/bin/env python3
"""Guard against pre-publication banners surviving into committed files.

A file that still carries a banner reserved for unfinished material -- a
do-not-commit marker, a pending-signature notice, a not-for-release stamp, a
staged-work label, a hold-until-approval line, or a bare hold identifier --
contradicts the fact that the file is committed and shipped. Readers cannot
tell whether the page in front of them is the released one or a draft that
escaped. Nothing else in the release gate reads for this: the path, link,
number, and manifest checks all pass on a file whose only defect is that it
announces it should not have been published. This guard asserts that no
tracked text file in the repository carries such a banner, with a narrow,
per-file allowlist for surfaces that must quote one verbatim.

Usage:
  python scripts/check_stale_banners.py             # scan; exit 1 on any hit
  python scripts/check_stale_banners.py --selftest  # pattern self-test only
  python scripts/check_stale_banners.py --repo PATH # scan a repo elsewhere

Exit codes: 0 clean, 1 violations (or self-test failure), 2 could not enumerate
the repository's files.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Rules. Each: id, compiled pattern, description.
#
# Spelling variants are folded into one rule where they are the same banner
# written two ways ("DO NOT COMMIT" / "DO-NOT-COMMIT"); the reported phrase is
# the literal matched text, so the two remain distinguishable in the output.
#
# SCOPE NOTE -- case sensitivity is mixed ON PURPOSE in the first three rules
# (inline scoped flags). Each of those banners has two spellings: a HYPHENATED
# label, which is matched in any case because it is never anything but a label,
# and a SPACED form, which is matched only in full caps because the lowercase
# spaced version is a grammatical English sentence fragment that occurs in
# ordinary prose -- "the parties do not commit to a schedule", "a pending
# freeze on rent increases", "the comment period is not for release of new
# data". Lowercasing those patterns would fail good pages; dropping them would
# miss the banner. The split is the only form that does both.
#
# SCOPE NOTE -- B-UNTIL-RATIFY. "until ratification" is grammatical legal
# English about treaties and constitutional amendments ("no effect until
# ratification by the States"). It is included here because in this repository
# it is a hold marker, not a description of ratification by a legislature. If a
# reader-facing page ever needs the constitutional sense, allowlist that file
# by exact path rather than loosening the pattern -- the phrase is short enough
# that a looser pattern would stop catching the hold marker entirely.
# ---------------------------------------------------------------------------

RULES = [
    (
        "B-NOCOMMIT",
        re.compile(r"(?:(?i:\bdo-not-commit\b)|\bDO[\s-]+NOT[\s-]+COMMIT\b)"),
        "do-not-commit banner on a committed file",
    ),
    (
        "B-PENDING-FREEZE",
        re.compile(r"(?:(?i:\bpending-freeze\b)|\bPENDING[\s-]+FREEZE\b)"),
        "pending-signature banner on a published file",
    ),
    (
        "B-NOT-FOR-RELEASE",
        re.compile(r"(?:(?i:\bnot-for-release\b)|\bNOT[\s-]+FOR[\s-]+RELEASE\b)"),
        "not-for-release banner on a released file",
    ),
    (
        "B-STAGED",
        re.compile(r"(?i)\bSTAGED\s*(?:--|\u2013|\u2014)"),
        "staged-work banner (the 'STAGED --' label) on a shipped file",
    ),
    (
        "B-UNTIL-RATIFY",
        re.compile(r"(?i)\buntil\s+ratification\b"),
        "hold-until-approval banner on a published file",
    ),
    (
        "B-RG001",
        re.compile(r"(?i)\bR-G001\b"),
        "bare internal hold identifier on a reader-facing surface",
    ),
]

# Files that are permitted to carry specific banner phrases, by exact
# repository-relative POSIX path -> list of permitted phrases (compared
# case-insensitively against the literal matched text). Ships EMPTY on purpose:
# every entry is a standing exception and needs the same per-file verification
# the rest of the gate's allowlists received. Use the exact matched phrase, not
# a pattern.
ALLOWLIST: dict[str, list[str]] = {
    # "record/correction_record.md": ["NOT FOR RELEASE"],
}

# Extensions scanned. Fixed by specification: markdown, python, json, csv,
# plain text, yml. NOTE: ".yaml" is deliberately NOT in this list -- the scope
# given to this guard names ".yml" only. Add it when the scope is widened, not
# on inference.
SCAN_EXT = (".md", ".py", ".json", ".csv", ".txt", ".yml")

# This guard's own source is excluded: its rule patterns and its POSITIVE_CASES
# fixtures ARE the banner strings, by construction. That is not a loosening --
# --selftest exercises the fixtures on every run, so the patterns stay proven.
# RELEASE_MANIFEST.json is machine-generated inventory, not prose; it can carry
# a banner phrase only as part of a filename or hash listing.
SKIP_FILES = {"RELEASE_MANIFEST.json", "GITHUB_COMBINED.md",
              os.path.basename(__file__)}


def scan_targets() -> list[str]:
    """Every tracked (and untracked, non-ignored) text file in the repository.

    Uses the same enumeration as the path-leak guard: a release commit picks up
    tracked files plus untracked files git does not ignore, so both are in
    scope. Raises RuntimeError if git cannot enumerate the tree -- a silent
    empty list would read as a clean pass.
    """
    try:
        tracked = subprocess.run(
            ["git", "ls-files"], cwd=REPO,
            capture_output=True, text=True, check=True)
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"], cwd=REPO,
            capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError(str(exc)) from exc

    out = []
    seen = set()
    for rel in (tracked.stdout + untracked.stdout).splitlines():
        rel = rel.strip()
        if not rel or rel in seen:
            continue
        seen.add(rel)
        if not rel.lower().endswith(SCAN_EXT):
            continue
        if os.path.basename(rel) in SKIP_FILES:
            continue
        path = os.path.join(REPO, rel)
        if os.path.isfile(path):
            out.append(path)
    return sorted(out)


def scan_line(line: str):
    """Return [(rule_id, matched_phrase, description)] for one line."""
    hits = []
    for rid, rx, desc in RULES:
        for m in rx.finditer(line):
            hits.append((rid, m.group(0), desc))
    return hits


def is_allowlisted(rel_posix: str, phrase: str) -> str | None:
    """Return the permitted phrase if this file may carry it, else None."""
    for permitted in ALLOWLIST.get(rel_posix, []):
        if permitted.lower() == phrase.lower():
            return permitted
    return None


POSITIVE_CASES = [
    ("<!-- DO NOT COMMIT -- working copy -->", "B-NOCOMMIT"),
    ("STATUS: DO-NOT-COMMIT", "B-NOCOMMIT"),
    ("# status: Do-Not-Commit until review", "B-NOCOMMIT"),
    ("Banner: PENDING FREEZE SIGNATURE", "B-PENDING-FREEZE"),
    ("status = pending-freeze", "B-PENDING-FREEZE"),
    ("NOT FOR RELEASE -- internal circulation", "B-NOT-FOR-RELEASE"),
    ("marked not-for-release pending review", "B-NOT-FOR-RELEASE"),
    ("STAGED -- awaiting sign-off", "B-STAGED"),
    ("STAGED \u2014 not merged", "B-STAGED"),
    ("Held until ratification of the amendment set", "B-UNTIL-RATIFY"),
    ("see R-G001 for the hold", "B-RG001"),
    ('  "note": "R-G001",', "B-RG001"),
]

NEGATIVE_CASES = [
    ("The frozen instrument was committed on 2026-07-18.", "plain commit prose"),
    ("git commit -m 'release'", "ordinary command line"),
    ("The freeze is recorded in the manifest.", "freeze without the banner"),
    ("Release notes for v1.2 are in CHANGELOG.md", "release without the banner"),
    ("regenerate_series_606_STAGED.py rebuilds the table",
     "STAGED inside a filename, no banner dash"),
    ("The rule was ratified in 1868.", "ratification prose, not the hold banner"),
    ("Ratification debates are summarized in Part I.", "ratification noun alone"),
    ("Rule R-G002 governs the appendix pointers", "adjacent identifier, not R-G001"),
    ("RG001 is a serial number", "no hyphen, not the identifier"),
    ("committed to publishing the underlying data", "commit as a verb of intent"),
    ("Do not cite the superseded table.", "different instruction entirely"),
    ("The comment period is not for release of new data.",
     "lowercase spaced 'not for release' is ordinary prose, not the banner"),
    ("The parties do not commit to a schedule.",
     "lowercase spaced 'do not commit' is ordinary prose, not the banner"),
    ("The ordinance imposed a pending freeze on rent increases.",
     "lowercase spaced 'pending freeze' is ordinary prose, not the banner"),
]


def selftest(quiet: bool = False) -> int:
    """Positive/negative pattern test.

    Run before every scan is reported clean: a search that silently stops
    matching fails in the direction of 'nothing found', which is exactly the
    direction that turns into a false all-clear. Proving the patterns still
    fire on known-present strings is what makes the negative result
    trustworthy. Touches no repository file.
    """
    if not quiet:
        print(f"check_stale_banners self-test: {len(POSITIVE_CASES)} positive / "
              f"{len(NEGATIVE_CASES)} negative cases")
    failures = 0
    for text, want in POSITIVE_CASES:
        hits = scan_line(text)
        ok = any(h[0] == want for h in hits)
        if not quiet or not ok:
            print(f"  {'PASS' if ok else 'FAIL'}  POS [{want:<17}] {text!r}"
                  + ("" if ok else f"  -> got {hits}"))
        failures += int(not ok)
    for text, why in NEGATIVE_CASES:
        hits = scan_line(text)
        ok = not hits
        if not quiet or not ok:
            print(f"  {'PASS' if ok else 'FAIL'}  NEG [{why}] {text!r}"
                  + ("" if ok else f"  -> spurious {hits}"))
        failures += int(not ok)
    total = len(POSITIVE_CASES) + len(NEGATIVE_CASES)
    if not quiet or failures:
        print(f"self-test: {total - failures}/{total} passed")
    return 1 if failures else 0


def read_lines(path: str) -> list[str]:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().splitlines()
    except (UnicodeDecodeError, OSError):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                return f.read().splitlines()
        except OSError:
            return []


def main() -> int:
    global REPO
    ap = argparse.ArgumentParser(description="Stale pre-publication banner guard.")
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

    try:
        targets = scan_targets()
    except RuntimeError as exc:
        print(f"check_stale_banners: could not list git files: {exc}",
              file=sys.stderr)
        return 2

    findings = []
    allowed = 0
    for path in targets:
        rel = os.path.relpath(path, REPO).replace("\\", "/")
        for i, line in enumerate(read_lines(path), 1):
            for rid, phrase, desc in scan_line(line):
                if is_allowlisted(rel, phrase):
                    allowed += 1
                    continue
                findings.append((rel, i, rid, phrase, desc, line.strip()[:120]))

    if selftest(quiet=True) != 0:
        print("FAIL: pattern self-test failed; scan result not trustworthy")
        return 1

    for rel, i, rid, phrase, desc, ctx in findings:
        print(f"STALE-BANNER {rel}:{i}:{phrase!r} [{rid}] -- {desc}\n    {ctx}")
    if findings:
        print(f"FAIL: {len(findings)} stale-banner hit(s) across "
              f"{len({f[0] for f in findings})} file(s); "
              f"{len(targets)} files scanned, {allowed} allowlisted")
        return 1
    print(f"OK: no stale banners ({len(targets)} files scanned, "
          f"{len(RULES)} rule families, {allowed} allowlisted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
