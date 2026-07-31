#!/usr/bin/env python3
"""Guard reader-facing pages against production vocabulary.

Every markdown page in this repository is written for someone who did not
build it: a reader, a reviewer, a tenant, an advocate. Words that describe how
the material was produced -- schedules, sign-offs, file-naming series, internal
statuses, drafting stages -- carry no meaning for that reader and, worse, imply
a process they cannot inspect. This guard asserts that the reader-facing
markdown surfaces are free of that vocabulary. It is deliberately narrow: the
ordinary legal senses of "ruling", "lane", "harvest", "sitting", and "gate" are
NOT matched, and the three patterns most likely to collide with ordinary legal
English carry documented context exemptions. Verbatim instruments that must
reproduce a source document exactly are exempt by path.

Usage:
  python scripts/check_process_language.py             # scan; exit 1 on any hit
  python scripts/check_process_language.py --selftest  # pattern self-test only
  python scripts/check_process_language.py --repo PATH # scan a repo elsewhere

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

# ---------------------------------------------------------------------------
# Rules. Each: id, compiled pattern, description, context-exemption tuple.
#
# The context tuple, when non-empty, suppresses the hit if any of its
# lowercased substrings appears on the same line. This is the same mechanism
# the superseded-series denylist uses for its known numeric-coincidence traps:
# it preserves the pattern (recall is unchanged) and downgrades only the
# specific collision that was verified to be legitimate legal English.
#
# SCOPE NOTES -- read before extending or loosening.
#
#   P-WORKORDER   A maintenance work order is a real and common object in
#                 housing prose (a repair request, a vendor ticket). Those
#                 lines are exempt by context. The production sense -- a
#                 document that schedules the project's own tasks -- is not.
#
#   P-RATIFIED    "ratified by the States", "ratified by the Senate", and the
#                 agency-law doctrine of ratification by a principal are all
#                 ordinary legal English and are exempt by context. The
#                 production sense -- a person signing off on a draft -- is not.
#
#   P-EXECUTOR    An executor of an estate is ordinary legal English and is
#                 exempt by context. The production sense -- a role that runs
#                 tasks -- is not.
#
#   P-REVIEWQUEUE Only the internal work-routing compounds are matched
#                 ("high-review queue", "working queue", "exported queue",
#                 "adjudication queue", "queue files"). A bare "queue", and an
#                 agency's own "processing queue" (the FOIA filing guide
#                 describes HUD's FOIA processing queue), are ordinary English
#                 and are NOT matched.
#
#   P-SANITIZED   Matched as a production verb. The two legitimate uses in this
#                 repository are allowlisted by path: a disclosure sentence
#                 stating that nothing was sanitized, and the SANITIZATION_NOTE
#                 whose title names the disclosure itself.
#
#   P-APPENDIXREADY / P-SCREENINGONLY
#                 The hyphenated labels are matched. Where they are DATA -- the
#                 claim_gate column emitted into the generated comparator tables
#                 and JSON payloads -- they are allowlisted by path, because the
#                 column and its values are machine-read and editing them would
#                 change an artifact rather than a page.
#
# The following words are DELIBERATELY NOT matched anywhere in this file, in
# any rule: "ruling", "lane", "harvest", "sitting", "gate", "pending", "wave",
# standing alone. Each is ordinary legal or ordinary English, and each was
# measured against this repository before being excluded:
#   "pending"  3,079 occurrences, essentially all the ordinary legal sense
#              ("the renewal notice remains pending", "any pending matter").
#   "wave"     the internal sense is "disability-wave", a live identifier in
#              three committed scripts (unified_overnight_openrouter.py,
#              public_defendant_analysis.py, pro_se_mechanism_analysis.py);
#              renaming the prose would desync it from the code. The ordinary
#              sense ("a wave of litigation") is also common here.
#   "lane"     the corpus uses it metaphorically throughout ("doctrinal lane",
#              "accessibility lane"), and the appendix sentence "not every
#              validation lane exposes a complete pleading-stage flag" is
#              mirrored verbatim from the article's own footnote 140.
# Only the multi-word production phrases built on these are matched. Do not add
# the bare words.
# ---------------------------------------------------------------------------

WORKORDER_OK = ("maintenance", "repair", "vendor", "contractor", "ticket",
                "work orders were", "landlord", "property manager", "janitor",
                "habitability", "service request")

RATIFIED_OK = ("senate", "congress", "legislature", "legislative", "states",
               "state legislature", "convention", "amendment", "treaty",
               "voters", "electorate", "parliament", "council", "principal",
               "agency law", "referendum", "charter")

EXECUTOR_OK = ("estate", "will", "probate", "decedent", "deceased", "testator",
               "testatrix", "heir", "intestate", "personal representative")

RULES = [
    ("P-WORKORDER",
     re.compile(r"(?i)\bwork[\s-]orders?\b"),
     "production scheduling vocabulary", WORKORDER_OK),
    ("P-AUTHORRULING",
     # \u2019 is the typographic apostrophe, escaped so this file stays
     # ASCII; re expands \uXXXX inside a pattern even in a raw string.
     re.compile(r"(?i)\bauthor(?:'s|\u2019s|s')?[\s-]+rulings?\b"),
     "internal decision vocabulary", ()),
    ("P-RATIFIED",
     re.compile(r"(?i)\bratified\s+by\b"),
     "internal sign-off vocabulary", RATIFIED_OK),
    ("P-CONTROLPLANE",
     re.compile(r"(?i)\bcontrol[_/\\-]plane\b"),
     "internal directory name", ()),
    ("P-DRAFTSERIES",
     re.compile(r"(?i)\bnote_v1[0-9]{2}\b"),
     "internal draft-file series name", ()),
    ("P-EDITCYCLE",
     re.compile(r"(?i)\bedit[\s-]cycles?\b"),
     "drafting-stage vocabulary", ()),
    ("P-EXECUTOR",
     re.compile(r"(?i)\bexecutors?\b"),
     "production role vocabulary", EXECUTOR_OK),
    ("P-COMPLETIONLOG",
     re.compile(r"(?i)\bcompletion[\s-]logs?\b"),
     "internal progress-record name", ()),
    ("P-CLAIMGATE",
     re.compile(r"(?i)\bclaim[\s-]gat(?:e|es|ed|ing)\b"),
     "internal claim-status vocabulary", ()),
    # The next two rules mix case sensitivity ON PURPOSE (inline scoped flags).
    # The HYPHENATED spelling is a label and is matched in any case; the SPACED
    # spelling is matched only in full caps, because "screening only" and "do
    # not cite" are grammatical lowercase English sentences ("tenant screening
    # only became routine after 1996"; "courts do not cite the 1988 Report").
    ("P-SCREENINGONLY",
     re.compile(r"(?:(?i:screening-only)|SCREENING[\s-]ONLY)"),
     "internal claim-status label", ()),
    ("P-DONOTCITE",
     re.compile(r"(?:(?i:do-not-cite)|DO[\s-]NOT[\s-]CITE)"),
     "internal citation-status label", ()),
    ("P-CONTENTLOCK",
     re.compile(r"(?i)\bcontent[\s-]lock(?:s|ed|ing)?\b"),
     "internal freeze vocabulary", ()),
    ("P-RESYNC",
     re.compile(r"(?i)\bre[\s-]?sync(?:s|ed|ing|hroniz\w*)?\b"),
     "internal file-copy vocabulary", ()),
    ("P-STAGINGPLAN",
     re.compile(r"(?i)\bstaging[\s-]plans?\b"),
     "internal plan-document name", ()),
    ("P-SITTINGRECORD",
     re.compile(r"(?i)\bsitting[\s-]records?\b"),
     "internal decision-record name", ()),
    ("P-LANEREPORT",
     re.compile(r"(?i)\blane[\s-]reports?\b"),
     "internal work-stream report name", ()),
    ("P-DECOUNTED",
     re.compile(r"(?i)\bde[\s-]?counted\b"),
     "internal coding-status vocabulary", ()),
    # -- residue families added by the 2026-07-30 vocabulary sweep -----------
    # Same case-mixing rationale as P-SCREENINGONLY: the hyphenated form is a
    # label in any case; there is no lowercase spaced form to collide with.
    ("P-APPENDIXREADY",
     re.compile(r"(?:(?i:appendix-ready)|APPENDIX[\s-]READY)"),
     "internal claim-status label", ()),
    # Case-mixed for the same reason: "the tenant needs human assistance" is a
    # grammatical lowercase sentence, so only the hyphenated label (any case)
    # and the full-caps spaced label are matched.
    ("P-NEEDSHUMAN",
     re.compile(r"(?:(?i:needs-human)|NEEDS[\s-]HUMAN)"),
     "internal workflow-status label", ()),
    ("P-REVIEWQUEUE",
     re.compile(r"(?i)(?:\b(?:high[\s-]review|low[\s-]confidence|review|working"
                r"|adjudication|export(?:ed)?)[\s-]queues?\b"
                r"|\bqueue[\s-]files?\b)"),
     "internal work-routing vocabulary", ()),
    ("P-REMEDIATIONPASS",
     re.compile(r"(?i)\bremediation[\s-](?:lane|pass|run|batch|stage)\b"),
     "internal correction-stage vocabulary", ()),
    ("P-SPRINT",
     re.compile(r"(?i)\bsprints?\b"),
     "internal work-period vocabulary", ()),
    ("P-SANITIZED",
     re.compile(r"(?i)\bsanitiz(?:e|es|ed|ing|ation)\b"),
     "internal output-scrubbing vocabulary", ()),
]

# Verbatim instruments: files that reproduce a filed or frozen source document
# exactly. Their wording is fixed by what was filed, so they are exempt from
# every rule in this guard by design -- changing their text to satisfy a style
# rule would make them no longer verbatim. Exact repository-relative POSIX
# paths. Ships with one commented example.
FROZEN_INSTRUMENT_PATHS: list[str] = [
    # Wrapped verbatim instrument. Its own banner states that everything below
    # it is the pre-registered instrument as run on 2026-07-08, byte-exact, and
    # that the internal file references, model assignments, and workflow
    # vocabulary in the body are part of the fixed registered object rather than
    # a description of this repository. Rewording it would destroy the verbatim
    # property the registration depends on.
    "method/preregistration/PREREGISTERED_PROMPT_2026-07-08.md",
    # Registered prediction set, wrapped the same way: the body below its banner is
    # the object the logged SHA-256 bcd5598e... covers, so its wording is fixed by
    # what was registered before any outcome analytics ran.
    "replication/comparator/PREDICTIONS.md",
]

# Narrower exemption: a specific file may carry specific phrases. Exact
# repository-relative POSIX path -> list of permitted phrases, compared
# case-insensitively against the literal matched text. Keep short and specific;
# each entry is a standing exception.
ALLOWLIST: dict[str, list[str]] = {
    # manuscript/Duty_Without_Data.md is a byte-synced copy of the article of
    # record, not an independently authored page: its wording is fixed by the
    # accepted manuscript. Two phrases in it are article prose, not repository
    # process residue, and both sit inside the Note's own footnotes:
    #   fn 1  (:225) "... targeted author rulings -- the qualifying-judgment-
    #                 boundary and finality-class sittings of July 17, 2026 ..."
    #                 -- the Note's own disclosure of how the outcome
    #                 adjudication was ratified; the phrase names the thing the
    #                 footnote is disclosing.
    #   fn 176 (:350) "... dated to July 21, 2026, and to be re-verified at
    #                 content lock." -- "content lock" is the law-review
    #                 production milestone the footnote is dated against.
    # Rewriting either would edit published article text and desync the mirror.
    # The same carve-out already exists in the superseded-series denylist, which
    # routes manuscript/ hits to author-side review rather than gating on them.
    # Scope is two phrases, not the whole file: the rest stays under the guard.
    "manuscript/Duty_Without_Data.md": ["author rulings", "content lock"],

    # -- claim_gate DATA, not prose (added 2026-07-30) ----------------------
    # The comparator pipeline emits a claim_gate column whose values are
    # "APPENDIX-READY" / "SCREENING-ONLY". The column name and its values are
    # machine-read: the generated tables below are that column rendered to
    # markdown, and the .py entries are the emitters that write it. Editing
    # either would change a generated artifact rather than a page, so the label
    # is allowlisted in exactly those files and nowhere else.
    "replication/comparator/TABLE1_COMPARATOR.md": ["APPENDIX-READY"],
    "replication/comparator/MODELS.md": ["APPENDIX-READY"],
    "replication/comparator/comparator_analysis.py": ["APPENDIX-READY",
                                                      "SCREENING-ONLY"],
    "replication/comparator/recoding_2026-07-07/scripts/compute_consensus.py":
        ["APPENDIX-READY"],
    # Emits "# SCREENING-ONLY (2026-07-16)" into THREELAYER_SUMMARY.md. The
    # committed summary already reads "Assurance: RESEARCH LEAD", so the
    # emitter and the artifact have drifted; reconciling them is an author
    # decision about the generated file, not a page edit.
    "results/specificity_threelayer/run_threelayer_comparison.py":
        ["SCREENING-ONLY"],

    # -- the label naming that same claim_gate tier in adjacent prose -------
    # Both sentences describe what the claim_gate column above them contains,
    # so the label is the referent, not residue. Whether the public tier
    # vocabulary should change at all is an author decision; until it does,
    # the prose must keep matching the data.
    # The same register's opening disclosure ("Nothing here is sanitized") is
    # the ordinary English sense and is allowlisted alongside it.
    "replication/comparator/METHODS_LIMITATIONS_AND_QA.md": ["APPENDIX-READY",
                                                             "sanitized"],
    "article/appendices/Appendix_A6_Comparator_Analysis.md": ["APPENDIX-READY"],

    # -- P-SANITIZED legitimate uses (added 2026-07-30) ---------------------
    # A disclosure that nothing was sanitized is the opposite of the thing the
    # rule guards against.
    "replication/comparator/recoding_2026-07-07/raw_text_verification/SANITIZATION_NOTE.md":
        ["Sanitization"],
}

# Post-migration reader-facing markdown: the top-level pages plus the scanned
# content trees. Raw corpus and machine artifacts are out of scope -- they are
# evidence, not prose a reader is asked to read.
SCAN_DIRS = ("article", "method", "replication", "record",
             "action", "results", "manuscript", "data/dictionaries",
             "supplementary")
SKIP_DIRS = {".git", "__pycache__", "_local_archive", "case_texts",
             "prompts", "node_modules"}
SKIP_FILES = {"GITHUB_COMBINED.md", os.path.basename(__file__)}

# Suffixes scanned inside SCAN_DIRS. Markdown is the reader-facing page; .py and
# .txt were added 2026-07-30 because the scripts and text outputs shipped inside
# those trees are read by anyone reproducing the work, and their docstrings,
# comments, and emitted strings are prose in every sense that matters. The
# top-level sweep stays markdown-only: the loose files at the repository root
# are pages, and the root .txt files are dependency locks.
SCAN_SUFFIXES = (".md", ".py", ".txt")


def scan_targets() -> list[str]:
    """Top-level *.md plus every scanned suffix under the content trees."""
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
                if name.lower().endswith(SCAN_SUFFIXES):
                    targets.append(os.path.join(root, name))
    seen, out = set(), []
    for t in targets:
        rel = os.path.relpath(t, REPO)
        if rel not in seen:
            seen.add(rel)
            out.append(t)
    return out


def scan_line(line: str):
    """Return [(rule_id, matched_phrase, description)] for one line."""
    low = line.lower()
    hits = []
    for rid, rx, desc, exempt in RULES:
        if exempt and any(tok in low for tok in exempt):
            continue
        for m in rx.finditer(line):
            hits.append((rid, m.group(0), desc))
    return hits


def is_exempt(rel_posix: str, phrase: str) -> str | None:
    """Return the reason this file may carry this phrase, else None."""
    if rel_posix in FROZEN_INSTRUMENT_PATHS:
        return "verbatim instrument (exempt by design)"
    for permitted in ALLOWLIST.get(rel_posix, []):
        if permitted.lower() == phrase.lower():
            return "allowlisted phrase"
    return None


POSITIVE_CASES = [
    ("see the work order for the schedule", "P-WORKORDER"),
    ("Per the work-order dated 2026-07-18", "P-WORKORDER"),
    ("resolved by author ruling D-12", "P-AUTHORRULING"),
    ("the author's ruling is recorded", "P-AUTHORRULING"),
    ("this text was ratified by the reviewer", "P-RATIFIED"),
    ("stored under control_plane/", "P-CONTROLPLANE"),
    ("copied from note_v136 on 2026-07-22", "P-DRAFTSERIES"),
    ("during the current edit cycle", "P-EDITCYCLE"),
    ("the edit-cycle is closed", "P-EDITCYCLE"),
    ("assigned to the executor for the run", "P-EXECUTOR"),
    ("appended to the COMPLETION LOG", "P-COMPLETIONLOG"),
    ("tagged claim-gate: appendix-ready", "P-CLAIMGATE"),
    ("this material is claim gated", "P-CLAIMGATE"),
    ("marked SCREENING-ONLY, not for print", "P-SCREENINGONLY"),
    ("the figure is DO-NOT-CITE", "P-DONOTCITE"),
    ("DO NOT CITE these cells", "P-DONOTCITE"),
    ("the page is under content-lock", "P-CONTENTLOCK"),
    ("resync the mirror before release", "P-RESYNC"),
    ("we re-sync the manuscript copy", "P-RESYNC"),
    ("logged in the staging plan", "P-STAGINGPLAN"),
    ("per the sitting record of 2026-07-18", "P-SITTINGRECORD"),
    ("summarized in the lane report", "P-LANEREPORT"),
    ("the case was DE-COUNTED after review", "P-DECOUNTED"),
    ("this cell is APPENDIX-READY at most", "P-APPENDIXREADY"),
    ("tagged appendix-ready, not body text", "P-APPENDIXREADY"),
    ("the row is marked NEEDS-HUMAN", "P-NEEDSHUMAN"),
    ("routed to the needs-human tier", "P-NEEDSHUMAN"),
    ("flagged NEEDS HUMAN before scoring", "P-NEEDSHUMAN"),
    ("the 132-case high-review queue", "P-REVIEWQUEUE"),
    ("exported into the working queue", "P-REVIEWQUEUE"),
    ("the adjudication queue by role", "P-REVIEWQUEUE"),
    ("the queue files sharpen that impression", "P-REVIEWQUEUE"),
    ("run 2026-07-07 in the remediation lane", "P-REMEDIATIONPASS"),
    ("counts recomputed in the remediation pass", "P-REMEDIATIONPASS"),
    ("Comparative Sprint C5.A3", "P-SPRINT"),
    ("scheduled for the next sprint", "P-SPRINT"),
    ("outputs were sanitized before release", "P-SANITIZED"),
    ("the sanitization step ran last", "P-SANITIZED"),
]

NEGATIVE_CASES = [
    ("the court's ruling in Olmstead", "bare 'ruling' is ordinary legal English"),
    ("a ruling on the motion to dismiss", "bare 'ruling'"),
    ("the bike lane and the sidewalk curb cut", "bare 'lane'"),
    ("harvest of public comments", "bare 'harvest'"),
    ("the panel sitting en banc", "bare 'sitting'"),
    ("a gate at the property entrance", "bare 'gate'"),
    ("the gatekeeping function of Rule 12(b)(6)", "'gate' inside another word"),
    ("the landlord ignored the maintenance work order for six weeks",
     "maintenance work order is ordinary housing prose"),
    ("submitted a repair work order to the property manager",
     "repair work order is ordinary housing prose"),
    ("the Fourteenth Amendment was ratified by the States in 1868",
     "constitutional ratification"),
    ("the treaty was ratified by the Senate", "treaty ratification"),
    ("the executor of the decedent's estate filed the complaint",
     "executor of an estate is ordinary legal English"),
    ("the will named an executor and two heirs", "probate sense"),
    ("courts do not cite the 1988 Report for this proposition",
     "'do not cite' as ordinary prose, lowercase and spaced"),
    ("tenant screening only became routine after 1996",
     "'screening only' as ordinary prose, lowercase and spaced"),
    ("the note at footnote 136 explains the gap", "no draft-series token"),
    ("Note v. Housing Authority, 136 F.3d 1", "citation, not the file series"),
    ("the editing of the brief took two weeks", "'edit' without 'cycle'"),
    ("a plan for staging the exhibits at trial", "'staging' without 'plan'"),
    ("the record of the sitting judge", "'sitting' without 'record'"),
    ("the report describes each lane of traffic", "'lane' and 'report' separated"),
    ("counted and de-emphasized in the appendix", "'de-' without 'counted'"),
    ("synchronized clocks are irrelevant here", "'sync' without the 're-' prefix"),
    ("the appendix ready for filing was served that day",
     "'appendix ready' as ordinary prose, lowercase and spaced"),
    ("HUD's FOIA processing queue is months long",
     "an agency's own processing queue is ordinary English"),
    ("plaintiffs wait in the queue for a hearing date", "bare 'queue'"),
    ("the tenant needs human assistance to file",
     "'needs human' followed by an ordinary object"),
    ("remediation of the lead paint was ordered",
     "'remediation' in its ordinary housing sense"),
    ("the consent decree required remediation and monitoring",
     "'remediation' as a remedy, not a production stage"),
    ("the renewal notice remains pending before OMB", "bare 'pending'"),
    ("a wave of disability filings followed the 1988 amendments", "bare 'wave'"),
    ("the report describes each lane of traffic", "bare 'lane'"),
]


def selftest(quiet: bool = False) -> int:
    """Positive/negative pattern test; touches no repository file.

    Run before any scan is reported clean. A pattern that silently stops
    matching fails in the direction of 'nothing found' -- the direction that
    turns into a false all-clear. The negative cases are load-bearing here:
    they are the ordinary-legal-English collisions this guard must never fire
    on, and they fail loudly if a rule is later widened.
    """
    if not quiet:
        print(f"check_process_language self-test: {len(POSITIVE_CASES)} positive / "
              f"{len(NEGATIVE_CASES)} negative cases")
    failures = 0
    for text, want in POSITIVE_CASES:
        hits = scan_line(text)
        ok = any(h[0] == want for h in hits)
        if not quiet or not ok:
            print(f"  {'PASS' if ok else 'FAIL'}  POS [{want:<16}] {text!r}"
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
    ap = argparse.ArgumentParser(description="Reader-facing process-language guard.")
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

    targets = scan_targets()
    findings = []
    exempted = 0
    for path in targets:
        rel = os.path.relpath(path, REPO).replace("\\", "/")
        for i, line in enumerate(read_lines(path), 1):
            for rid, phrase, desc in scan_line(line):
                if is_exempt(rel, phrase):
                    exempted += 1
                    continue
                findings.append((rel, i, rid, phrase, desc, line.strip()[:120]))

    if selftest(quiet=True) != 0:
        print("FAIL: pattern self-test failed; scan result not trustworthy")
        return 1

    for rel, i, rid, phrase, desc, ctx in findings:
        print(f"PROCESS-LANGUAGE {rel}:{i}:{phrase!r} [{rid}] -- {desc}\n    {ctx}")
    if findings:
        print(f"FAIL: {len(findings)} process-language hit(s) across "
              f"{len({f[0] for f in findings})} file(s); "
              f"{len(targets)} files scanned, {exempted} exempted")
        return 1
    print(f"OK: no process language on reader-facing pages "
          f"({len(targets)} files scanned, {len(RULES)} rule families, "
          f"{exempted} exempted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
