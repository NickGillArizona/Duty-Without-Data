#!/usr/bin/env python3
"""Denylist scanner for superseded outcome-series values.

Scans reader-facing markdown (and the rendered figure SVGs) for values that are
not part of the accepted archive: retired series values that must never be
served as current. The scan never modifies any file. It runs inside
run_release_checks.py in strict mode: any true-stale hit fails the gate. A
documented allowlist covers archival-labeled surfaces that disclose their basis
in place and verified numeric coincidences.

Context-aware: bare-number tokens (730, 728, 263, 467) and decimal tokens carry
word-boundary guards plus exclusion windows so that reporter citations
("602 U.S. 367", "263 F.3d"), section numbers, page pins ("at 730", "pp. 263-70"),
docket numbers ("No. 22-728"), dollar amounts, and digit-adjacent longer numbers
do not fire. Excluded raw matches are still recorded in report mode with verdict
"likely-false-positive" so a human can audit the exclusion logic.

Usage:
  python scripts/denylist_superseded_series.py --selftest
  python scripts/denylist_superseded_series.py --report [--out PATH]
  python scripts/denylist_superseded_series.py --report --strict   (exit 1 on any true-stale hit)
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Rules. Each: id, compiled pattern, description, and whether the surrounding-
# window exclusions apply (bare/ambiguous tokens) or the pattern is specific
# enough to stand alone.
# ---------------------------------------------------------------------------

RULES = [
    # -- superseded case-level N bases --------------------------------------
    ("D-730", r"(?<![\d.,])730(?![\d.])", True,
     "superseded case-level N (730 kept rows; universal collapse: 606)"),
    ("D-728", r"(?<![\d.,])728(?![\d.])", True,
     "superseded two-merge-only N (728; universal collapse: 606)"),
    ("D-263", r"(?<![\d.,])263(?![\d.])", True,
     "superseded represented pool (263; universal basis: 206)"),
    ("D-467", r"(?<![\d.,])467(?![\d.])", True,
     "superseded pro se pool (467; universal basis: 400)"),
    ("D-TRIPLE-N", r"\b367/86/277\b", False,
     "superseded per-window N (universal basis: 287/68/251)"),
    # -- superseded rates ----------------------------------------------------
    ("D-RATE-272", r"(?<![\d.])(?<!\$)2\.72%?(?![\d.])", False,
     "superseded 730-basis P1 strict rate (universal basis: 3.48%)"),
    ("D-RATE-289", r"(?<![\d.])(?<!\$)2\.89%?(?![\d.])", False,
     "superseded 730-basis P3 strict rate (universal basis: 3.19%)"),
    ("D-VPM", r"0\.33\s*(?:to|->|-->|/|and)\s*0\.47", False,
     "victories-per-month values withdrawn from citation on the superseded basis"),
    # -- superseded shares ---------------------------------------------------
    ("D-DOC-SHARES", r"(?<![\d.])(?:54\.2|63\.3|73\.7)%", False,
     "document-level share series on reader surfaces (case-level series: 59.6 -> 76.1)"),
    ("D-OLD-CASE-SHARES", r"(?<![\d.])(?:57\.5|55\.8|75\.1)%", False,
     "superseded 730-basis case-level shares (universal basis: 59.6/55.9/76.1)"),
    # -- superseded cells ----------------------------------------------------
    ("D-REPCELL-68", r"(?<![\d.])6\.8%(?![\d.])", False,
     "superseded represented cell pct (universal basis: 8.7%)"),
    ("D-REP-WINDOWS", r"\b156/38/69\b", False,
     "superseded per-window represented counts (universal basis: 116/30/60)"),
    ("D-QUAD", r"\b995/476/120/399\b", False,
     "document-level count series presented as case counts"),
    ("D-995-CASES", r"\b995\s+(?:dated-decided\s+)?cases\b", False,
     "995 is a document-level row count, not a case count ('995 rows' is legitimate)"),
    # -- superseded derived figures -----------------------------------------
    ("D-808PP", r"8\.08\s*(?:pp\b|percentage[- ]points?)", False,
     "superseded selection-audit gap figure (A-7 re-run owed on 606/206)"),
    ("D-269-188", r"26\.9%?\s*(?:->|-->|to)\s*18\.8%?", False,
     "superseded lag-window contrast"),
    ("D-748", r"(?<![\d.])74\.8%(?![\d.])", False,
     "stale fn 70 lag figure (A-4 re-run owed on collapsed units)"),
    ("D-ATLEAST57", r"(?i)\bat least 57(?:\.\d)?%", False,
     "identified LIVE FALSE printed figure (tier audit 2026-07-18)"),
    # -- fraction forms of the superseded series ----------------------------
    ("D-FRAC-OLD", r"\b(?:10/367|8/277|0/86|18/263|0/467|18/730|18/728)\b", False,
     "fraction forms of the superseded series (universal basis: 10/287, 8/251, 0/68, 18/206, 0/400, 18/606)"),
]

# Exclusion windows for bare-number rules (window_before = up to 28 chars ending
# at the match; window_after = up to 28 chars starting after the match).
EXCLUDE_BEFORE = [
    (r"U\.S\.C?\.?\s*$", "US-reports-or-USC-cite"),
    (r"(?:§|[Ss]ec(?:tion|s)?\.?)\s*[\d.\-]*$", "section-number"),
    (r"(?:No\.|Nos\.|Docket)\s*[\d:cvcr.\-]*$", "docket-number"),
    (r"(?i)(?:\bat|\bp\.|\bpp\.)\s+$", "page-pin"),
    (r"[-]\s?$", "hyphen-adjacent (docket/range)"),
    (r"\$\s*$", "dollar-amount"),
    (r"(?:F\.(?: Supp\.)?(?: [234]d| 2d| 3d| 4th)?|S\. ?Ct\.|L\. ?Ed\.(?: 2d)?|Fed\. ?Reg\.|F\.R\.D\.)\s+$", "reporter-page"),
    (r"(?:Form|OMB|Pub\. ?L\.)\s*(?:No\.)?\s*[\d\-]*$", "form-or-pubL-number"),
]
EXCLUDE_AFTER = [
    (r"^\s*(?:U\.S\.|F\.(?: Supp\.)?(?: [234]d| 2d| 3d| 4th)?|S\. ?Ct\.|L\. ?Ed\.|F\.R\.D\.)", "reporter-volume"),
    (r"^\s*C\.F\.R\.", "cfr-title"),
    (r"^\s*Fed\. ?Reg\.", "fedreg-volume"),
    (r"^-\d", "hyphen-adjacent (docket/range)"),
    (r"^\s*U\.S\.C\.", "usc-title"),
]

COMPILED = [(rid, re.compile(pat), excl, desc) for rid, pat, excl, desc in RULES]
EXC_B = [(re.compile(p), name) for p, name in EXCLUDE_BEFORE]
EXC_A = [(re.compile(p), name) for p, name in EXCLUDE_AFTER]

WINDOW = 28


def scan_line(line: str):
    """Return list of (rule_id, matched_text, col, verdict, reason).
    verdict: 'STALE' (non-excluded hit) or 'EXCLUDED' (raw match killed by an
    exclusion window)."""
    hits = []
    for rid, rx, apply_excl, desc in COMPILED:
        for m in rx.finditer(line):
            verdict, reason = "STALE", desc
            if apply_excl:
                before = line[max(0, m.start() - WINDOW):m.start()]
                after = line[m.end():m.end() + WINDOW]
                for erx, ename in EXC_B:
                    if erx.search(before):
                        verdict, reason = "EXCLUDED", ename
                        break
                if verdict == "STALE":
                    for erx, ename in EXC_A:
                        if erx.search(after):
                            verdict, reason = "EXCLUDED", ename
                            break
            hits.append((rid, m.group(0), m.start() + 1, verdict, reason))
    return hits


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

# (text, expected rule id that must fire as STALE)
POSITIVE_CASES = [
    ("Across the 730 identified decided-opinion cases", "D-730"),
    ("the two-merge basis gives 728 decided cases", "D-728"),
    ("18 of 263 represented cases (6.8%)", "D-263"),
    ("0 of 467 pro se decided cases", "D-467"),
    ("367/86/277 across the three windows", "D-TRIPLE-N"),
    ("a strict qualifying rate of 2.72%", "D-RATE-272"),
    ("P3 strict 2.89", "D-RATE-289"),
    ("rose from 0.33 to 0.47 victories per month", "D-VPM"),
    ("the share rose from 54.2% to 73.7%", "D-DOC-SHARES"),
    ("57.5% -> 75.1% on the case-level N", "D-OLD-CASE-SHARES"),
    ("the represented cell is 6.8%", "D-REPCELL-68"),
    ("represented 156/38/69 across the windows", "D-REP-WINDOWS"),
    ("the 995/476/120/399 series", "D-QUAD"),
    ("the corrected census covers 995 cases", "D-995-CASES"),
    ("an 8.08pp selection gap", "D-808PP"),
    ("falls 26.9 -> 18.8 under the lag test", "D-269-188"),
    ("74.8% after dropping the final six months", "D-748"),
    ("in at least 57% of the sampled cases", "D-ATLEAST57"),
    ("the strict cell prints 10/367 on the old basis", "D-FRAC-OLD"),
]

# (text, description) -- must produce ZERO STALE hits (either no raw match or
# every raw match EXCLUDED by a context window).
NEGATIVE_CASES = [
    ("Loper Bright Enterprises v. Raimondo, 602 U.S. 367 (2024)", "Loper Bright pin"),
    ("Chevron, 467 U.S. 837 (1984)", "Chevron pin (467 + U.S. after)"),
    ("see id. at 730.", "page pin 'at 730'"),
    ("Smith v. Jones, 263 F.3d 110 (9th Cir. 2001)", "reporter volume 263 F.3d"),
    ("F. Supp. 3d 263 (S.D.N.Y. 2020)", "reporter page 263"),
    ("No. 22-728 (7th Cir.)", "docket number containing 728"),
    ("$2.72 million in damages", "dollar amount 2.72"),
    ("version 2.89.1 of the pipeline", "version string 2.89.1"),
    ("pp. 263-70", "page range 263-70"),
    ("a correlation of 0.33 in the pilot data", "0.33 alone, no vpm pair"),
    ("the 995 recorded decided rows", "995 rows (document-level, legitimate)"),
    ("the 1,730 respondents", "digit-group 1,730"),
    ("16.8% of applications", "16.8% is not 6.8%"),
    ("a 174.8% increase", "174.8% is not 74.8%"),
    ("42 U.S.C. sec. 3604(f)(3)(B)", "section string, no token"),
    ("24 C.F.R. part 100.203", "regulation cite, no token"),
    ("the year 1728 saw no such filings", "1728 does not contain a bare 728"),
    ("3:21-cv-730 (W.D. Wash.)", "docket 3:21-cv-730 (hyphen-adjacent)"),
]


def selftest() -> int:
    print("denylist self-test:", len(POSITIVE_CASES), "positive /",
          len(NEGATIVE_CASES), "negative cases")
    failures = 0
    for text, want_rule in POSITIVE_CASES:
        stale = [h for h in scan_line(text) if h[3] == "STALE"]
        ok = any(h[0] == want_rule for h in stale)
        print(f"  {'PASS' if ok else 'FAIL'}  POS [{want_rule:<18}] {text!r}"
              + ("" if ok else f"  -> got {stale}"))
        failures += int(not ok)
    for text, why in NEGATIVE_CASES:
        stale = [h for h in scan_line(text) if h[3] == "STALE"]
        ok = not stale
        print(f"  {'PASS' if ok else 'FAIL'}  NEG [{why}] {text!r}"
              + ("" if ok else f"  -> spurious {stale}"))
        failures += int(not ok)
    total = len(POSITIVE_CASES) + len(NEGATIVE_CASES)
    print(f"self-test: {total - failures}/{total} passed")
    return 1 if failures else 0


# ---------------------------------------------------------------------------
# Report mode
# ---------------------------------------------------------------------------

def reader_facing_files():
    """Top-level *.md (minus the regenerable GITHUB_COMBINED.md dump),
    article/appendices/**/*.md, manuscript/*.md (the mirror of the canonical article
    text; hits there are flagged for author-side attention, never gated here),
    replication/**/*.md (the terminal comparator record, the frozen research
    instruments, and the reproduction protocol), results/*.md at the directory
    root (the generated statistical reports and the registry pages, which are
    read straight from the results listing), results/supporting/**/*.md
    (the supporting analyses), and the rendered figure SVGs in results/figures
    (their text nodes reach readers inline)."""
    files = []
    for name in sorted(os.listdir(REPO)):
        if name.lower().endswith(".md") and name != "GITHUB_COMBINED.md":
            p = os.path.join(REPO, name)
            if os.path.isfile(p):
                files.append(p)
    # results/ root only, non-recursive: the subdirectories holding reader-facing
    # markdown are enumerated separately (results/supporting, walked below) or are
    # scanned as SVG (results/figures), so walking the whole tree here would
    # double-count them.
    resdir = os.path.join(REPO, "results")
    if os.path.isdir(resdir):
        for name in sorted(os.listdir(resdir)):
            if name.lower().endswith(".md"):
                p = os.path.join(resdir, name)
                if os.path.isfile(p):
                    files.append(p)
    for sub in ("article", "manuscript", "method",
                "replication", "action", "record", "results/supporting",
                "data/dictionaries", "supplementary"):
        d = os.path.join(REPO, sub)
        if os.path.isdir(d):
            for root, _dirs, names in os.walk(d):
                for name in sorted(names):
                    if name.lower().endswith(".md"):
                        files.append(os.path.join(root, name))
    figdir = os.path.join(REPO, "results", "figures")
    if os.path.isdir(figdir):
        for name in sorted(os.listdir(figdir)):
            if name.lower().endswith(".svg"):
                files.append(os.path.join(figdir, name))
    return files


# Known numeric-coincidence trap: the repo's three-model ensemble
# mechanism-coding universe is "728 of 739" pleading-loss cases -- an unrelated
# 728 that collides with the superseded two-merge N. Recall is preserved (the
# rule still fires); the verdict guess downgrades hits whose line context is
# clearly the ensemble universe.
ENSEMBLE_CONTEXT = ("ensemble", "three-model", "739", "fleiss", "kappa",
                    "coder", "coded", "majority-vote", "majority vote",
                    "pleading-loss universe", "kimi", "glm", "deepseek")

# Hits that are legitimate by design, verified individually: archival-labeled
# cells disclose their interim basis in place, and several document-level
# appendix tables contain unrelated cells that happen to equal a retired
# token. Entries are (file, rule) -> reason;
# rule "*" covers every rule for that file. Allowlisted hits report as
# "allowlisted (...)" and do not fail --strict. Keep this list short and
# specific: a new entry requires the same per-hit verification these received.
ALLOWLIST = {
    ("LIMITATIONS_AND_NEGATIVE_RESULTS.md", "D-730"):
        "supersession-disclosure page: both 730 mentions state the document-level "
        "basis as superseded and mirror the fn 76 non-replication disclosure "
        "(verified 2026-07-31, curation pass)",
    ("article/appendices/Appendix_A4_Reproducibility_Audit.md", "D-730"):
        "archival-labeled exploratory run; interim basis disclosed in place",
    ("article/appendices/FN76_AGREEMENT.md", "D-730"):
        "archival reference to the interim-basis exploratory run, disclosed as such",
    ("article/appendices/Appendix_A5_Robustness_Checks.md", "D-808PP"):
        "document-level delta cell; the file states it is unrelated to the fn 90 audit",
    ("article/appendices/Appendix_A6_Comparator_Analysis.md", "D-OLD-CASE-SHARES"):
        "document-level composition-share cells; numeric coincidence",
    ("article/appendices/Appendix_A6_Comparator_Analysis.md", "D-DOC-SHARES"):
        "document-level comparator-family cells; numeric coincidence",
    ("article/appendices/Appendix_A7_Selection_and_Participation.md", "D-730"):
        "archival-labeled cells disclose their pre-consolidation basis in place",
    ("article/appendices/Appendix_A7_Selection_and_Participation.md", "D-TRIPLE-N"):
        "archival-labeled cells disclose their pre-consolidation basis in place",
    ("article/appendices/Appendix_B_Results_Tables.md", "D-728"):
        "document-level post-2024 row count; numeric coincidence",
    ("article/appendices/Appendix_H_Supplementary_Data.md", "D-DOC-SHARES"):
        "document-level stage-table cell; numeric coincidence",
    ("article/appendices/Appendix_E_Accommodation_Defendant_Analysis.md", "D-OLD-CASE-SHARES"):
        "document-level broad-rate cell; numeric coincidence",
    ("supplementary/empirical_extensions.md", "D-OLD-CASE-SHARES"):
        "document-level broad-rate cell; numeric coincidence",
    ("results/supporting/public_defendant_failure_stack.md", "D-730"):
        "heuristic specificity-bucket record count (mixed/other claim-type signals: "
        "730 records, 523 decided); a different quantity from the retired case-row basis",
    ("results/supporting/public_defendant_failure_stack.md", "D-REPCELL-68"):
        "pleading_failure_mechanism label distribution: MIXED count 90, share 6.8% of "
        "labeled records; not the retired represented-cell value",
    ("results/supporting/pums_state_and_invisible_populations.md", "D-OLD-CASE-SHARES"):
        "ACS PUMS cost-burden rate cell (White alone, 65+, disabled); demographic share "
        "unrelated to the case-share series",
    # results/ root and results/supporting memo surfaces brought into scope when the
    # authored analysis memos were nested under supporting/ and the scan was extended
    # to the results/ root. Each hit below was verified individually against its line
    # context: all are foreign-domain quantities (census, agency, program, and
    # coder-agreement cells) or disclosed document-level archive rows, not retired
    # series values served as current.
    ("results/appendix_report.md", "D-467"):
        "generated diagnostic report: race-category coder-agreement cell; an agreement "
        "denominator, not the retired pro se pool",
    ("results/appendix_report.md", "D-728"):
        "generated diagnostic report: document-level period-split row count for the "
        "post-2024 window; the table is labeled document-level and is not the retired "
        "merged-ensemble case denominator",
    ("results/hud_existing_disability_data_systems.md", "D-263"):
        "HUD PD&R PIC/TRACS extract: elderly-household count in the Section 202 "
        "universe, reported in thousands; a household count, not the retired "
        "represented pool",
    ("results/supporting/comparative_contextual_empirics.md", "D-263"):
        "MCAD fiscal-year housing-jurisdiction complaint count for Massachusetts, given "
        "once in a table and once restated in prose; a state-agency statistic",
    ("results/supporting/design_construction_bottleneck.md", "D-728"):
        "Providence-Warwick metro population cell in the census housing-stock table; "
        "digit-run coincidence with the retired two-merge N",
    ("results/supporting/design_construction_bottleneck.md", "D-OLD-CASE-SHARES"):
        "owner-occupied share cell in the ACS pre-1991 housing-stock table; a housing "
        "figure unrelated to the case-share series",
    ("results/supporting/doctrinal_case_audits.md", "D-OLD-CASE-SHARES"):
        "E.D. Pa. share-of-full-circuit-decline cells in the circuit deep-dive section "
        "(one table cell plus three prose restatements); district-concentration shares, "
        "numeric coincidence with the retired composition series",
    ("results/supporting/hmda_section_3614a_analogy.md", "D-730"):
        "Boston accessible-housing registry coverage count (affordable rental "
        "developments predating the 2016 threshold); a municipal program count",
    ("results/supporting/hud_administrative_record_deep_dives.md", "D-467"):
        "embedded copy of the appendix-report race-category agreement cell; the same "
        "agreement denominator, not the retired pro se pool",
    ("results/supporting/hud_administrative_record_deep_dives.md", "D-728"):
        "embedded copy of the document-level period-split table carried in the appendix "
        "report; document-level labeled context",
    ("results/supporting/methodological_audits_and_validation.md", "D-730"):
        "the file banner cites the printed fn 76 pre-consolidation disclosure, which "
        "itself contrasts the pre-consolidation series against the live one, and the "
        "section body is expressly labeled a document-level pre-collapse exploratory "
        "re-run; disclosed in place rather than served as current",
    ("results/supporting/program_specific_accessibility_gaps.md", "D-RATE-289"):
        "Utah accessible-unit share cell in the LIHTC QAP jurisdiction table; a program "
        "statistic unrelated to the retired qualifying-rate series",
    ("results/unified_stats_report.md", "D-728"):
        "generated statistics report: document-level period-split row count for the "
        "post-2024 window; document-level labeled context",
    ("replication/CASE_LEVEL_RULES.md", "D-730"):
        "published per-row census record; 730 is the kept opinion-row count, not a "
        "case-level N",
    ("replication/VERIFY_ONE_CLAIM.md", "D-730"):
        "published per-row census record; 730 is the kept opinion-row count, not a "
        "case-level N",
    ("replication/GATES.md", "D-730"):
        "published per-row census record; 730 is the kept opinion-row count, not a "
        "case-level N (the census-check section states what the gate asserts)",
    ("replication/comparator/MODELS.md", "D-OLD-CASE-SHARES"):
        "document-level Kitagawa composition-share cell (DIS 57.5); the file header "
        "labels every cell document-level archive output (ledger C49)",
    ("replication/comparator/TABLE1_COMPARATOR.md", "D-DOC-SHARES"):
        "document-level cohort-table cell (MIXED P3 pro se share); numeric coincidence "
        "with the retired token; the file header labels every cell document-level",
}


def guess_verdict(rel: str, rid: str, line: str, verdict: str, reason: str) -> str:
    if verdict == "EXCLUDED":
        return f"likely-false-positive ({reason})"
    rel_posix = rel.replace("\\", "/")
    allow = ALLOWLIST.get((rel_posix, rid)) or ALLOWLIST.get((rel_posix, "*"))
    if allow:
        return f"allowlisted ({allow})"
    low = line.lower()
    if rel_posix.startswith("manuscript/"):
        return ("review: canonical article text (mirror of the published Note; "
                "flagged for author-side attention, never gated here)")
    if rid == "D-728" and any(k in low for k in ENSEMBLE_CONTEXT):
        return "review: ensemble-universe 728 of 739 (numeric coincidence; likely legitimate)"
    if rid == "D-467" and "token" in low:
        return "review: token-count context (numeric coincidence; likely legitimate)"
    if rid in ("D-DOC-SHARES", "D-QUAD", "D-995-CASES") and "document" in low:
        return "review: document-level context (may be legitimate)"
    return "true-stale (guess)"


def report(out_path: str | None, strict: bool) -> int:
    rows = []
    files = reader_facing_files()
    for path in files:
        rel = os.path.relpath(path, REPO)
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except UnicodeDecodeError:
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        for i, line in enumerate(lines, 1):
            for rid, tok, col, verdict, reason in scan_line(line):
                rows.append({
                    "file": rel, "line": i, "rule": rid, "token": tok,
                    "verdict": guess_verdict(rel, rid, line, verdict, reason),
                    "context": line.strip()[:160],
                })
    n_stale = sum(1 for r in rows if r["verdict"].startswith("true-stale"))
    n_fp = sum(1 for r in rows if r["verdict"].startswith("likely-false-positive"))
    n_rev = sum(1 for r in rows if r["verdict"].startswith("review"))
    n_allow = sum(1 for r in rows if r["verdict"].startswith("allowlisted"))
    header = (f"denylist scan: {len(files)} files scanned, {len(rows)} raw hits "
              f"({n_stale} true-stale / {n_fp} likely-false-positive / "
              f"{n_rev} review / {n_allow} allowlisted)")
    print(header)
    if out_path:
        stamp = datetime.date.today().isoformat()
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("# DENYLIST SCAN -- " + stamp + "\n\n")
            f.write("Provenance: scripts/denylist_superseded_series.py --report. "
                    "The scan never modifies any file.\n\n")
            f.write(header + "\n\n")
            f.write("| file | line | rule | token | verdict | context |\n")
            f.write("|---|---|---|---|---|---|\n")
            for r in rows:
                ctx = r["context"].replace("|", "\\|")
                f.write(f"| {r['file']} | {r['line']} | {r['rule']} | "
                        f"{r['token']} | {r['verdict']} | {ctx} |\n")
            f.write("\nEND\n")
        print("report written:", out_path)
    else:
        for r in rows:
            print(f"  {r['file']}:{r['line']} [{r['rule']}] {r['token']!r} "
                  f"{r['verdict']} :: {r['context'][:100]}")
    return 1 if (strict and n_stale) else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.report:
        return report(args.out, args.strict)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
