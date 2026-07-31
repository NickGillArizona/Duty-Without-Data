#!/usr/bin/env python3
"""Guard against retired reader-facing claims: the fn 87 magnitude band, the
retired Figure 2 chart, and independent-model-family validation framing.

The rest of the release gate checks paths, links, recomputed numbers, advocacy
figures, the superseded-series denylist, and the manifest -- nothing else would
notice a withdrawn qualitative claim sitting in reader-facing prose. This guard
closes that class.

Three rule families, all hard-failing:

  R-BAND    the withdrawn fn 87 "17-20 percentage point" translation-gap band.
            The magnitude did not survive verification and is withdrawn. The
            DIRECTIONAL finding survives and is NOT matched here -- only the
            magnitude band is retired.

  R-FIG2    the retired Figure 2 translation chart, no longer part of the
            accepted archive. Matches the figure stem so that a reintroduced
            <img>, srcset, markdown image, or re-registered builder is caught.
            Lines carrying a retirement marker (see RETIREMENT_MARKER) are
            exempt so the retirement record itself can be stated in prose and
            in code comments.

  R-FAMILY  claims of three-independent-model-family / independent-family
            validation. The "three independent model families" framing was
            found factually false (two of the seats belonged to one family);
            the standing rule is "No claim of three-family or
            independent-family validation, ever."

            SCOPE NOTE -- read before extending this rule. It deliberately does
            NOT match the phrase "three-model ensemble", which in this repo is
            the descriptive NAME of the Kimi K2.6 + GLM-5.1 + DeepSeek V3.2
            majority-vote stage. Those are three genuinely distinct models from
            three developers, and the phrase appears across ~39 files including
            raw data, JSON artifacts, and Java source. The retired framing
            concerned separate validation seats, not this ensemble. If that
            pipeline stage is ever renamed, add the pattern here then -- do not
            add it on inference.

            The rule also must not fire on "three-family dwelling" / "two- or
            three-family home", which is a housing type and appears throughout
            the corpus. The patterns require a model/coder/validation word.

Usage:
  python scripts/check_retired_claims.py            # scan; exit 1 on any hit
  python scripts/check_retired_claims.py --selftest  # pattern self-test
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

# A line stating that the figure is retired is not a reintroduction of it.
RETIREMENT_MARKER = re.compile(r"(?i)\bretired\b")

RULES = [
    (
        "R-BAND",
        re.compile(
            r"(?i)(?<![\d.])1[78]\s*(?:-|--|–|—|to)\s*20\s*"
            r"(?:pp\b|percentage[\s-]*points?|points?\b)"
        ),
        "withdrawn fn 87 17-20 pp translation-gap band (the directional "
        "finding survives, the magnitude does not)",
        False,
    ),
    (
        "R-FIG2",
        re.compile(r"(?i)fig2[_-]?translation"),
        "retired Figure 2 translation chart (not part of the accepted archive)",
        True,
    ),
    (
        "R-FAMILY",
        re.compile(
            r"(?i)"
            r"\b(?:three|3|two|multiple)[\s-]*(?:independent[\s-]*)?"
            r"(?:model|coder|llm)[\s-]*famil(?:y|ies)\b"
            r"|\bindependent[\s-]*(?:model[\s-]*)?famil(?:y|ies)\b"
            r"|\bthree[\s-]*famil(?:y|ies)[\s-]*"
            r"(?:validation|consensus|agreement|coding|panel)\b"
            r"|\bthree[\s-]*independent[\s-]*famil(?:y|ies)\b"
        ),
        "retired independent-model-family validation framing (standing rule: "
        "'No claim of three-family or independent-family validation, ever')",
        False,
    ),
]

# Reader-facing and build surfaces. Raw corpus (case_texts/, data/) and the
# machine-generated manifest are out of scope: they are evidence, not claims.
SCAN_DIRS = ("article", "manuscript", "results", "action",
             "method", "replication", "record", "data/dictionaries",
             "supplementary")
SCAN_GLOB_DIR_PREFIXES = ("validation_",)
SCAN_EXT = (".md", ".csv", ".py")
# "prompts" and "pipeline" stay here so that method/prompts and method/pipeline
# remain skipped now that they live under the scanned method/ root -- os.walk
# prunes on basename, so the pre-migration skip semantics are preserved exactly.
# "oira_harvest" is gone: that tree is now record/hud-27061 and IS scanned, as a
# reader-facing surface. The terminal comparator record and the frozen research
# instruments now live under replication/, which is scanned: neither may quote a
# retired claim.
SKIP_DIRS = {"case_texts", "data", "_local_archive", "prompts",
             "pipeline", ".git"}
# This guard's own source is excluded: its rule patterns and its POSITIVE_CASES
# fixtures ARE the retired strings, by construction. Excluding it is not a
# loosening of the check -- the fixtures are exercised by --selftest on every
# run, so the patterns stay proven. Any OTHER file that needs to quote a retired
# string must be handled by the RETIREMENT_MARKER exemption, not added here.
SKIP_FILES = {"GITHUB_COMBINED.md", "RELEASE_MANIFEST.json",
              os.path.basename(__file__)}


def scan_targets():
    """Top-level .md/.csv, scripts/*.py, and the reader-facing subtrees."""
    targets = []
    for name in sorted(os.listdir(REPO)):
        path = os.path.join(REPO, name)
        if os.path.isfile(path) and name not in SKIP_FILES:
            if name.lower().endswith((".md", ".csv")):
                targets.append(path)
    scripts_dir = os.path.join(REPO, "scripts")
    if os.path.isdir(scripts_dir):
        for name in sorted(os.listdir(scripts_dir)):
            if name in SKIP_FILES:
                continue
            if name.lower().endswith(".py"):
                targets.append(os.path.join(scripts_dir, name))
    roots = list(SCAN_DIRS) + [
        d for d in sorted(os.listdir(REPO))
        if os.path.isdir(os.path.join(REPO, d))
        and d.startswith(SCAN_GLOB_DIR_PREFIXES)
    ]
    for sub in roots:
        base = os.path.join(REPO, sub)
        if not os.path.isdir(base):
            continue
        for root, dirs, names in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in sorted(names):
                if name in SKIP_FILES:
                    continue
                if name.lower().endswith(SCAN_EXT):
                    targets.append(os.path.join(root, name))
    seen, out = set(), []
    for t in targets:
        rp = os.path.relpath(t, REPO)
        if rp not in seen:
            seen.add(rp)
            out.append(t)
    return out


def scan_line(line: str):
    """Return [(rule_id, matched_text, description)] for one line."""
    hits = []
    for rid, rx, desc, marker_exempt in RULES:
        if marker_exempt and RETIREMENT_MARKER.search(line):
            continue
        for m in rx.finditer(line):
            hits.append((rid, m.group(0), desc))
    return hits


POSITIVE_CASES = [
    ("places the gap at roughly 17 to 20 percentage points", "R-BAND"),
    ("audited band roughly 17-20 pp, below", "R-BAND"),
    ("a directional 17–20 pp band", "R-BAND"),
    ("the defensible gap is 18-20 percentage points", "R-BAND"),
    ("roughly 17 - 20 points on a bounded audit", "R-BAND"),
    ('<img src="results/figures/fig2_translation_light.svg">', "R-FIG2"),
    ("srcset=results/figures/fig2_translation_dark.svg", "R-FIG2"),
    ('"fig2_translation": lambda pal: fig2_translation(ensemble, pal),', "R-FIG2"),
    ("coded by three independent model families", "R-FAMILY"),
    ("three model families agreed on the label", "R-FAMILY"),
    ("validated across independent model families", "R-FAMILY"),
    ("a three-family validation design", "R-FAMILY"),
    ("two independent coder families", "R-FAMILY"),
]

NEGATIVE_CASES = [
    ("the finding is directional and machine-based", "surviving directional claim"),
    ("pro se / represented gap = 31.6 percentage points", "live ensemble gap"),
    ("Opus 4.7 full re-read (29.24 pp)", "validation-layer point estimate"),
    ("the 28-32 pp bracket is pipeline-internal", "pipeline-internal bracket"),
    ("a 17.5 percentage point shift", "unrelated single figure"),
    ("between 20 and 17 percentage points", "reversed order, not the band token"),
    ("# fig2_translation was RETIRED (no longer in the archive)", "retirement marker exempt"),
    ("Figure 2 retired; the builder was removed", "retirement prose"),
    ("three-model majority-vote ensemble", "pipeline stage name (NOT retired)"),
    ("Kimi K2.6 + GLM-5.1 + DeepSeek V3.2 majority vote", "coder roster"),
    ("a sober house in a three-family dwelling", "housing type, not a coder claim"),
    ("two- or three-family homeowners", "housing type, not a coder claim"),
    ("Fleiss' kappa across the three coders = 0.6297", "reliability across coders"),
    ("117 of 632 pro se strict failures", "unrelated counts"),
]


def selftest(quiet: bool = False) -> int:
    """Positive/negative pattern test.

    Run before every scan: a search tool that silently stops matching fails in
    the direction of 'nothing found', which is exactly the direction that turns
    into a false all-clear. Proving the patterns still fire on known-present
    strings is what makes the negative result trustworthy.
    """
    if not quiet:
        print(f"check_retired_claims self-test: {len(POSITIVE_CASES)} positive / "
              f"{len(NEGATIVE_CASES)} negative cases")
    failures = 0
    for text, want in POSITIVE_CASES:
        hits = scan_line(text)
        ok = any(h[0] == want for h in hits)
        if not quiet or not ok:
            print(f"  {'PASS' if ok else 'FAIL'}  POS [{want:<9}] {text!r}"
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    targets = scan_targets()
    findings = []
    for path in targets:
        rel = os.path.relpath(path, REPO).replace("\\", "/")
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except (UnicodeDecodeError, OSError):
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        for i, line in enumerate(lines, 1):
            for rid, tok, desc in scan_line(line):
                findings.append((rel, i, rid, tok, desc, line.strip()[:120]))

    if selftest(quiet=True) != 0:
        print("FAIL: pattern self-test failed; scan result not trustworthy")
        return 1

    for rel, i, rid, tok, desc, ctx in findings:
        print(f"RETIRED-CLAIM {rel}:{i} [{rid}] {tok!r} -- {desc}\n    {ctx}")
    if findings:
        print(f"FAIL: {len(findings)} retired-claim hit(s) across "
              f"{len({f[0] for f in findings})} file(s); {len(targets)} files scanned")
        return 1
    print(f"OK: no retired-claim hits ({len(targets)} files scanned, "
          f"{len(RULES)} rule families)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
