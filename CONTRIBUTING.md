# Contributing

This repository is a replication package for a law review note. Contributions are welcome in the following forms:

## Bug Reports

If you encounter errors running the replication scripts, please open an issue with:
- The script name and command you ran
- The full error traceback
- Your Python version and operating system

## Data Corrections

If you identify a classification error in the FHA Unified Database, please open an issue with:
- The `case_name` and `citation` of the affected record
- The field(s) you believe are incorrect
- The correct value(s) with supporting reasoning

## Replication Extensions

If you extend this pipeline to a new legal domain, I'd welcome a link to your work. Open an issue or PR to add it to a "Related Projects" section.

## Style: Model-Behavior Vocabulary

Use *classify*, *classification*, or *code* for model behavior. The exact defined term
*per-claim structured extraction* may be used only as the name of Stage 4 or in an existing
artifact filename. Use *extract* or *extraction* outside that defined term only for
deterministic software operations on files, fields, or strings. Do not describe a model as
extracting facts.

## Pre-Release Checks

`scripts/run_release_checks.py` is this repository's regression suite. Run it before
publishing any snapshot; every check must pass. What each check establishes — and what a
green run does not establish — is documented in [replication/GATES.md](replication/GATES.md).

The suite also blocks registered opinion-source text from entering the release and verifies
that the public comment-window language remains synchronized with its configured deadline.

## Accessibility

Figures must carry substantive alt text stating the series they render, diagrams get an
adjacent prose text equivalent, and tables keep header rows. Accessibility gaps are bugs;
report them like any other error.

## Corrections After Release

Material corrections follow a versioned, terminal-state rule:

1. Report the issue through the claim-correction issue template, or email the author.
2. A confirmed material correction updates the governing authority (the manuscript
   statement or the registered series), the claims ledger, every dependent
   presentation, and the regression checks in one change set.
3. The corrected state ships as a new immutable release; existing tags are never
   moved or rewritten.
4. The release notes state the corrected terminal fact and the affected claim IDs.
5. The underlying investigation is preserved privately. Development queues, run logs,
   and other internal execution records do not enter the public tree; the public
   record stays terminal-state.

## Surface Contracts

Every repeated fact has exactly one governing home; every other appearance is a
derived presentation kept in line by the release checks. When editing, change the
authority and its checks together -- never a derived surface alone.

| Surface | Job | Authority status |
|---|---|---|
| `manuscript/Duty_Without_Data.md` | The Note's text | Governing human authority; never edited here |
| `results/series_2026-07.json` | Final case-level series | Sole machine authority for empirical claims |
| `article/CLAIMS_LEDGER.csv` | Claim-to-evidence registry | Registry; every citable claim has a row |
| `README.md`, `index.md` | Front doors | Derived; claim blocks validated against the series |
| `article/` appendices + crosswalks | Cited support | Derived; letter-keyed, print-fixed |
| `method/` | Terminal method + validation | Governing method statements |
| `replication/` | Reproduction contract | Executable; commands must run from a clean clone |
| `results/` root | Canonical outputs and registries | Generated; regenerate, do not hand-edit |
| `results/supporting/`, `supplementary/` | Research context | Not authority; see each directory README |
| `record/hud-27061/` | Administrative record | Source layer; content frozen |
| `action/` | Advocacy templates | Derived from the record; counsel adapts |
| `scripts/`, CI | Enforcement | The checks themselves |

## Code of Conduct

Be respectful and constructive. This is an academic research project.
