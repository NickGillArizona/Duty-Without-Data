#!/usr/bin/env python3
"""Assert the markdown pages stay usable by a reader who is not looking at them.

A page that reads well in a browser can be unusable through a screen reader,
and nothing else in the release gate would notice. This guard checks five
things a reader depending on assistive technology needs: every image carries
alt text substantial enough to convey what it shows; every diagram rendered as
a mermaid block is followed by a text equivalent, because the diagram itself is
markup a reader cannot hear; heading levels descend one at a time, so the
document outline used for navigation is not broken by a skipped level; every
table opens with a header row and its separator, so cells are announced with
their column; and no link is labelled "here" or "click here", which tells a
reader moving link-to-link nothing about where it goes.

Known limits, stated so a clean result is not over-read: reference-style images
and markup inside inline code spans are not inspected; HTML <img> tags are
inspected line-by-line, so a tag split across source lines is not seen; and
content inside fenced code blocks is skipped entirely.

Usage:
  python scripts/check_accessibility_contract.py             # scan; exit 1 on any hit
  python scripts/check_accessibility_contract.py --selftest  # fixture self-test only
  python scripts/check_accessibility_contract.py --repo PATH # scan a repo elsewhere

Exit codes: 0 clean, 1 violations (or self-test failure).
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

MIN_ALT_CHARS = 5
MERMAID_WINDOW = 10

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*(\S*)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+\S")
TABLE_ROW_RE = re.compile(r"^\s{0,3}\|")
# A separator row: pipes, dashes, optional alignment colons, at least one dash.
TABLE_SEP_RE = re.compile(r"^\s{0,3}\|[\s:|-]*-[\s:|-]*\|?\s*$")
TEXTEQ_RE = re.compile(r"(?i)text\s+equivalent")
BAD_LINKTEXT_RE = re.compile(r"\[\s*(?:click\s+)?here\s*\]\(", re.IGNORECASE)
HTML_IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
HTML_ALT_RE = re.compile(r"""alt\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)

RULE_DESC = {
    "X-ALT": "image alt text missing or shorter than "
             f"{MIN_ALT_CHARS} characters",
    "X-MERMAID": "diagram block with no text equivalent within "
                 f"{MERMAID_WINDOW} lines after it",
    "X-HEADING": "heading level skipped (the outline jumps more than one level)",
    "X-TABLE": "table does not open with a header row and its separator row",
    "X-LINKTEXT": "uninformative link text",
}

# Files permitted to break a specific rule, by repository-relative POSIX path
# -> list of rule ids. Ships EMPTY on purpose.
ALLOWLIST: dict[str, list[str]] = {
    # "results/figures/README.md": ["X-ALT"],
}

# Same reader-facing scope as the process-language guard. The two scopes are
# written out separately rather than shared, so each guard stays a standalone
# file that can be read and run on its own; if one scope changes, change both.
SCAN_DIRS = ("article", "method", "replication", "record", "action",
             "results", "manuscript", "data/dictionaries", "supplementary")
SKIP_DIRS = {".git", "__pycache__", "_local_archive", "case_texts",
             "prompts", "node_modules"}
SKIP_FILES = {"GITHUB_COMBINED.md", os.path.basename(__file__)}


def scan_targets() -> list[str]:
    """Top-level *.md plus every *.md under the scanned content trees."""
    targets = []
    for name in sorted(os.listdir(REPO)):
        path = os.path.join(REPO, name)
        if os.path.isfile(path) and name.lower().endswith(".md") \
                and name not in SKIP_FILES:
            targets.append(path)
    for sub in SCAN_DIRS:
        base = os.path.join(REPO, sub)
        if not os.path.isdir(base):
            continue
        for root, dirs, names in os.walk(base):
            dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
            for name in sorted(names):
                if name in SKIP_FILES:
                    continue
                if name.lower().endswith(".md"):
                    targets.append(os.path.join(root, name))
    seen, out = set(), []
    for t in targets:
        rel = os.path.relpath(t, REPO)
        if rel not in seen:
            seen.add(rel)
            out.append(t)
    return out


def scan_text(text: str):
    """Return [(lineno, rule_id, detail)] for one markdown document.

    Single pass. Fenced code blocks are skipped for every rule: a table or a
    heading inside a code sample is sample text, not document structure. The
    first heading in a document is not measured against anything, so a file
    that legitimately opens at level 2 is not failed for its own first line.
    """
    findings = []
    lines = text.splitlines()

    in_fence = False
    fence_char = ""
    mermaid_open: int | None = None
    prev_level: int | None = None
    run_start: int | None = None
    run: list[str] = []

    def flush_table():
        nonlocal run_start, run
        if run_start is not None:
            if len(run) < 2 or not TABLE_SEP_RE.match(run[1]):
                findings.append((run_start, "X-TABLE", RULE_DESC["X-TABLE"]))
        run_start, run = None, []

    for i, line in enumerate(lines, 1):
        fence = FENCE_RE.match(line)
        if fence:
            flush_table()
            token = fence.group(1)[0]
            info = fence.group(2).strip().lower()
            if not in_fence:
                in_fence, fence_char = True, token
                if info.startswith("mermaid"):
                    mermaid_open = i
            elif token == fence_char:
                in_fence, fence_char = False, ""
                if mermaid_open is not None:
                    window = lines[i:i + MERMAID_WINDOW]
                    if not any(TEXTEQ_RE.search(w) for w in window):
                        findings.append(
                            (mermaid_open, "X-MERMAID", RULE_DESC["X-MERMAID"]))
                    mermaid_open = None
            continue
        if in_fence:
            continue

        if TABLE_ROW_RE.match(line):
            if run_start is None:
                run_start = i
            run.append(line)
        else:
            flush_table()

        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            if prev_level is not None and level > prev_level + 1:
                findings.append(
                    (i, "X-HEADING",
                     f"{RULE_DESC['X-HEADING']}: level {prev_level} -> {level}"))
            prev_level = level

        for m in IMAGE_RE.finditer(line):
            alt = m.group(1).strip()
            if len(alt) < MIN_ALT_CHARS:
                findings.append(
                    (i, "X-ALT",
                     f"{RULE_DESC['X-ALT']} (alt={alt!r}, src={m.group(2)!r})"))

        for m in HTML_IMG_RE.finditer(line):
            alt_m = HTML_ALT_RE.search(m.group(0))
            alt = ""
            if alt_m:
                alt = alt_m.group(1) if alt_m.group(1) is not None \
                    else (alt_m.group(2) or "")
            if len(alt.strip()) < MIN_ALT_CHARS:
                findings.append(
                    (i, "X-ALT",
                     f"{RULE_DESC['X-ALT']} (HTML img, alt={alt.strip()!r})"))

        for m in BAD_LINKTEXT_RE.finditer(line):
            findings.append(
                (i, "X-LINKTEXT", f"{RULE_DESC['X-LINKTEXT']}: {m.group(0)!r}"))

    flush_table()
    # An unterminated diagram fence never gets a text equivalent.
    if mermaid_open is not None:
        findings.append((mermaid_open, "X-MERMAID",
                         RULE_DESC["X-MERMAID"] + " (block never closed)"))
    return sorted(findings, key=lambda f: (f[0], f[1]))


POSITIVE_CASES = [
    ("![](figures/timeline.svg)", "X-ALT"),
    ("![map](figures/map.svg)", "X-ALT"),
    ("Text before ![ ](x.png) and after", "X-ALT"),
    ("```mermaid\ngraph TD;\nA-->B;\n```\n\nThe diagram shows the sequence.\n",
     "X-MERMAID"),
    ("```mermaid\ngraph TD;\nA-->B;\n", "X-MERMAID"),
    ("# Title\n\n#### Deep\n", "X-HEADING"),
    ("## Section\n\n##### Detail\n", "X-HEADING"),
    ("| Year | Count |\n| 2022 | 14 |\n", "X-TABLE"),
    ("| single row |\n", "X-TABLE"),
    ("See [here](https://example.org/petition) for the text.", "X-LINKTEXT"),
    ("See [Click Here](https://example.org) to file.", "X-LINKTEXT"),
    ('<img src="figures/timeline.svg" width="760">', "X-ALT"),
    ("<img src='figures/map.svg' alt='map'>", "X-ALT"),
]

NEGATIVE_CASES = [
    ("![Timeline of the 2022 form revision](figures/timeline.svg)",
     "alt text of sufficient length"),
    ("![Bar chart of outcomes by representation status](figures/fig1.svg)",
     "descriptive alt text"),
    ("```mermaid\ngraph TD;\nA-->B;\n```\n\nText equivalent: A precedes B.\n",
     "diagram followed by a text equivalent"),
    ("```mermaid\ngraph TD;\nA-->B;\n```\n\n\n\nA text equivalent follows.\n"
     "Text equivalent -- A precedes B.\n",
     "text equivalent inside the ten-line window"),
    ("# Title\n\n## Section\n\n### Detail\n\n## Next section\n",
     "one level at a time, and returning up is fine"),
    ("## Fragment\n\n### Detail\n", "first heading is not measured"),
    ("| Year | Count |\n|------|-------|\n| 2022 | 14 |\n",
     "header row plus separator"),
    ("| Year | Count |\n| :--- | ----: |\n| 2022 | 14 |\n",
     "aligned separator row"),
    ("See [the petition text](https://example.org/petition).",
     "informative link text"),
    ("Start [here is the full record](https://example.org) instead.",
     "'here' is not the whole link text"),
    ("```\n| a | b |\n| 1 | 2 |\n```\n", "table inside a code fence is sample text"),
    ("```text\n# Title\n#### Deep\n```\n", "headings inside a code fence"),
    ("```\n![](x.png)\n```\n", "image markup inside a code fence"),
    ("A sentence about what happens here.", "the word 'here' outside a link"),
    ('<img src="figures/fig1.svg" alt="Bar chart of outcomes across the three periods">',
     "HTML image with descriptive alt text"),
    ('```\n<img src="x.svg">\n```\n', "HTML image inside a code fence is sample text"),
    ("| pipe in prose is not a table row? no -- it is |\n|---|\n",
     "single-column table with a separator"),
]


def selftest(quiet: bool = False) -> int:
    """Fixture self-test on synthetic documents; touches no repository file.

    Run before any scan is reported clean. The negative fixtures encode the
    shapes a correctly written page is allowed to use -- code fences, aligned
    separators, an opening level-2 heading -- so a later tightening of a rule
    fails here rather than on a good page.
    """
    if not quiet:
        print(f"check_accessibility_contract self-test: {len(POSITIVE_CASES)} "
              f"positive / {len(NEGATIVE_CASES)} negative fixtures")
    failures = 0
    for text, want in POSITIVE_CASES:
        hits = scan_text(text)
        ok = any(h[1] == want for h in hits)
        if not quiet or not ok:
            print(f"  {'PASS' if ok else 'FAIL'}  POS [{want:<11}] "
                  f"{text.splitlines()[0][:56]!r}"
                  + ("" if ok else f"  -> got {hits}"))
        failures += int(not ok)
    for text, why in NEGATIVE_CASES:
        hits = scan_text(text)
        ok = not hits
        if not quiet or not ok:
            print(f"  {'PASS' if ok else 'FAIL'}  NEG [{why}] "
                  f"{text.splitlines()[0][:56]!r}"
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
    ap = argparse.ArgumentParser(description="Markdown accessibility contract guard.")
    ap.add_argument("--selftest", "--self-test", dest="selftest",
                    action="store_true",
                    help="run the embedded fixtures only; touches no repo file")
    ap.add_argument("--repo", default=None,
                    help="repository root to scan (default: the parent of this "
                         "script's directory, as the other release checks resolve it)")
    ap.add_argument("--max-report", type=int, default=0,
                    help="print at most N findings (0 = all); the counts are "
                         "always complete")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.repo:
        REPO = os.path.abspath(args.repo)

    if selftest(quiet=True) != 0:
        print("FAIL: fixture self-test failed; scan result not trustworthy")
        return 1

    targets = scan_targets()
    findings = []
    allowed = 0
    for path in targets:
        rel = os.path.relpath(path, REPO).replace("\\", "/")
        for lineno, rid, detail in scan_text(read_text(path)):
            if rid in ALLOWLIST.get(rel, []):
                allowed += 1
                continue
            findings.append((rel, lineno, rid, detail))

    shown = findings if args.max_report <= 0 else findings[:args.max_report]
    for rel, lineno, rid, detail in shown:
        print(f"A11Y {rel}:{lineno}:{rid} -- {detail}")
    if len(shown) < len(findings):
        print(f"    ... and {len(findings) - len(shown)} more")
    if findings:
        by_rule = {}
        for _, _, rid, _ in findings:
            by_rule[rid] = by_rule.get(rid, 0) + 1
        breakdown = ", ".join(f"{k} {v}" for k, v in sorted(by_rule.items()))
        print(f"FAIL: {len(findings)} accessibility hit(s) across "
              f"{len({f[0] for f in findings})} file(s) "
              f"[{breakdown}]; {len(targets)} files scanned, {allowed} allowlisted")
        return 1
    print(f"OK: accessibility contract holds ({len(targets)} files scanned, "
          f"{len(RULE_DESC)} rules, {allowed} allowlisted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
