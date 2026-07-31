"""Top-level deterministic release gate — one command, no network, no API keys, no cost.

Runs, in order:

1. scripts/check_no_user_paths.py      — path-leak guard;
2. scripts/check_internal_links.py     — internal file links and section anchors;
3. scripts/validate_claims.py          — recomputes the manuscript's headline numbers from the
                                         frozen canonical database;
4. scripts/check_appendix_pointers.py  — registered repository-pointing footnotes resolve to
                                         the exact section and literals they cite;
5. scripts/check_release_manifest.py   — verifies every tracked file against RELEASE_MANIFEST.json;
6. scripts/check_action_canonicality.py — the take-action kit is finished text a reader can
                                         file as written;
7. scripts/check_accessibility_contract.py — the markdown pages stay usable through assistive
                                         technology;
8. scripts/build_case_level_series.py --check — the registered case-level series reproduces
                                         from the published per-row census record;
9. scripts/check_readme_budget.py    — keeps the repository front door within its editorial
                                         budget and required routes;
10. scripts/recompute_verification.py — independent recomputation of the
                                         registered-baseline outputs against the committed CSVs;
11. scripts/check_advocacy_claims.py   — the registered headline claims are present on the
                                         guarded reader-facing pages, and no superseded figure is;
12. scripts/denylist_superseded_series.py --report --strict — no retired outcome-series value
                                         is served as current on any reader-facing surface;
13. scripts/check_retired_claims.py    — no withdrawn qualitative claim (the fn 87 magnitude
                                         band, the retired Figure 2, withdrawn validation
                                         framing) reappears in reader-facing prose;
14. scripts/check_stale_banners.py     — no pre-publication banner survives on a committed file;
15. scripts/check_process_language.py  — reader-facing pages stay free of production vocabulary;
16. scripts/check_claim_authority.py   — the front-door claim blocks carry the literals derived
                                         at runtime from the series of record
                                         (results/series_2026-07.json);
17. scripts/check_source_text_leakage.py — no non-distributed opinion text enters the release;
18. scripts/check_deadline_freshness.py — the time-sensitive comment-window presentation is current.

Everything here is a deterministic local check. Model reruns (OpenRouter/Anthropic lanes) and
corpus reconstruction are intentionally NOT part of this gate; see replication/REPRODUCE.md ("What is
deterministic and what is not") and replication/GATES.md (what a green run does and does not establish).

Usage: python scripts/run_release_checks.py
Exit code 0 only if every check passes.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

CHECKS = [
    ("path-leak guard", ["scripts/check_no_user_paths.py"]),
    ("internal-link guard", ["scripts/check_internal_links.py"]),
    ("claim validation", ["scripts/validate_claims.py"]),
    ("appendix-pointer guard", ["scripts/check_appendix_pointers.py"]),
    ("release manifest", ["scripts/check_release_manifest.py"]),
    ("take-action kit canonicality", ["scripts/check_action_canonicality.py"]),
    ("accessibility contract", ["scripts/check_accessibility_contract.py"]),
    ("case-level census", ["scripts/build_case_level_series.py", "--check"]),
    ("README editorial budget", ["scripts/check_readme_budget.py"]),
    ("strengthening recompute", ["scripts/recompute_verification.py"]),
    ("advocacy-surface claims", ["scripts/check_advocacy_claims.py"]),
    ("superseded-series denylist", ["scripts/denylist_superseded_series.py", "--report", "--strict"]),
    ("retired-claim guard", ["scripts/check_retired_claims.py"]),
    ("stale-banner guard", ["scripts/check_stale_banners.py"]),
    ("process-language guard", ["scripts/check_process_language.py"]),
    ("claim-authority blocks", ["scripts/check_claim_authority.py"]),
    ("source-text leakage guard", ["scripts/check_source_text_leakage.py"]),
    ("deadline freshness", ["scripts/check_deadline_freshness.py"]),
]


def main() -> int:
    failures = []
    for label, cmd in CHECKS:
        print(f"=== {label}: python {cmd[0]} ===")
        result = subprocess.run([sys.executable, *cmd], cwd=REPO)
        if result.returncode != 0:
            failures.append(label)
        print()
    if failures:
        print("RELEASE CHECKS FAILED:", "; ".join(failures))
        return 1
    print(f"RELEASE CHECKS PASSED ({len(CHECKS)}/{len(CHECKS)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
