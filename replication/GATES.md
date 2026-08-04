# Release Gate

This page explains what the release badge does and does not establish. The gate is a
regression suite for the repository's registered claims and reader-facing safeguards. It
checks the committed repository state; it does not establish the truth of legal
propositions, the facts of any case, or the accuracy of a model classification.

## How to run it

```bash
python scripts/run_release_checks.py
```

One command, deterministic, local: no network, no API keys, no cost. Exit code 0 only if
every check passes. The CI badge in the [README](../README.md) runs exactly this command in
two environments (see [Environments](#environments)).

## The twenty checks

| # | Check | Script | What it examines | A failure means |
|---|---|---|---|---|
| 1 | Path-leak guard | `scripts/check_no_user_paths.py` | Every release file | A local filesystem path leaked into a public file |
| 2 | Internal links and anchors | `scripts/check_internal_links.py` | Markdown links in release files | A link points to a missing file or a missing section anchor |
| 3 | Claim validation | `scripts/validate_claims.py` | 41 registered statistics | A published number no longer recomputes from the frozen database and committed series |
| 4 | Appendix-pointer guard | `scripts/check_appendix_pointers.py` | Registered repository-pointing footnotes | A footnote's target section or its cited literals no longer resolve |
| 5 | Release manifest | `scripts/check_release_manifest.py` | Every git-tracked file | The committed tree drifted from `RELEASE_MANIFEST.json` (line-ending-only differences warn, not fail) |
| 6 | Take-action kit canonicality | `scripts/check_action_canonicality.py` | The pages in `action/` | A template is half-written, out of date, unhedged, or announces an outcome the agency has not posted |
| 7 | Accessibility contract | `scripts/check_accessibility_contract.py` | Reader-facing markdown | A page is unusable through assistive technology |
| 8 | Case-level census | `scripts/build_case_level_series.py --check` | `replication/case_level_census.csv` | The registered case-level series no longer reproduces from the published per-row record |
| 9 | README editorial budget | `scripts/check_readme_budget.py` | `README.md` | The front door grew past its editorial word budget or lost a required route |
| 10 | Strengthening recompute | `scripts/recompute_verification.py` | The strengthening module outputs | A registered strengthening output no longer recomputes from its committed inputs |
| 11 | Advocacy-surface claims | `scripts/check_advocacy_claims.py` | The guarded reader-facing pages | A registered headline claim is missing where it belongs, or a superseded figure appears |
| 12 | Superseded-series denylist | `scripts/denylist_superseded_series.py --report --strict` | Reader-facing markdown and rendered figure SVGs | A retired outcome-series value is being served as current |
| 13 | Retired-claim guard | `scripts/check_retired_claims.py` | Reader-facing prose | A withdrawn qualitative claim (the fn 87 magnitude band, the retired Figure 2, the withdrawn validation framing) reappeared |
| 14 | Stale-banner guard | `scripts/check_stale_banners.py` | Every tracked text file | A pre-publication banner survived into a shipped file |
| 15 | Process-language guard | `scripts/check_process_language.py` | Reader-facing markdown, plus the `.py` and `.txt` files shipped inside the scanned content trees | Production vocabulary that means nothing to a reader leaked into a public page |
| 16 | Claim-authority blocks | `scripts/check_claim_authority.py` | The marker-delimited claim blocks on README, index, and THE_ARGUMENT | A front-door census statement no longer matches the literals derived at runtime from `results/series_2026-07.json` |
| 17 | Source-text leakage guard | `scripts/check_source_text_leakage.py` | Tracked and untracked, nonignored release files | A registered source opinion, or a file placed in a source-text directory, would enter the public repository |
| 18 | Deadline freshness guard | `scripts/check_deadline_freshness.py` | `_config.yml`, README, index, and COMMENT | Comment-window status or deadline language drifted from the configured publication state |
| 19 | Claims-ledger integrity | `scripts/check_claims_ledger.py` | `article/CLAIMS_LEDGER.csv` | The ledger fails to parse, a claim row is malformed, a required field is blank, or a path-like evidence route no longer resolves in the tree |
| 20 | Generated-surface sync | `scripts/check_generated_surfaces.py` | The generated pages, the record pages' dated status lines, and the appendix count | A generated surface drifted from its source, a dated status line is older than the newest chronology event, or a stated appendix count no longer matches the files present |

### What each check asserts

**6 — Take-action kit canonicality.** The templates in [`../action/`](../action/) are meant
to be downloaded and used, so anything left half-written in them travels into a real filing.
The kit's bracketed ADAPTATION fields (`[PETITIONER ORGANIZATION]`, `[VENUE]`, and the like)
are its design — counsel fills them — and are not violations. What the check fails on is a
registered set of editorial-stub phrases: unfilled docket stubs, verify-at-filing reminders,
figures disclosed as out of date, and stale as-of dates; it also requires that each template
still says it is not legal advice and that any page describing the status of the form keeps
both possibilities open rather than announcing an outcome the agency has not posted. A new
editorial-reminder phrase must be added to the check's registered list to be caught — the
check does not infer stub-ness from brackets alone. If the `action/` directory is absent,
the check reports a clean pass and says so.

**7 — Accessibility contract.** A page that reads well in a browser can be unusable through
a screen reader, and no other check would notice. This one requires alt text long enough to
convey what an image shows, a written text equivalent after every diagram, heading levels
that descend one at a time so the document outline can be navigated, tables that open with a
header row and its separator so cells are announced with their column, and link text that
says where the link goes. Content inside code blocks is skipped. HTML image tags are
inspected line-by-line for substantive alt text; a tag whose attributes are split across
source lines is not seen.

**8 — Case-level census.** The article's headline outcome claim is stated over case units,
not opinion documents, and the record behind that collapse is published as a per-row CSV.
This check reads [`case_level_census.csv`](case_level_census.csv), re-derives each case
unit's outcome, period, and representation from its member rows under the rules in
[`CASE_LEVEL_RULES.md`](CASE_LEVEL_RULES.md), and compares the result against the registered
series in [`../results/series_2026-07.json`](../results/series_2026-07.json). It asserts the
structural invariants of the record — 730 kept opinion rows resolving to 598 decided case
units — and the eleven registered cells: 598 decided units pooled; 283 / 65 / 250 across the
three windows; 206 represented and 400 pro se; eighteen qualifying judgments, 10 / 0 / 8 by
window; and zero qualifying judgments in pro se cases. A failure means the published series
and the published record no longer agree.

**11–15 — Claim hygiene.** The last five checks hold the reader-facing surfaces to the
registered series of record: they require the registered headline claims to remain present
on the pages that carry them (11), and they fail on any figure outside the series of record
served as current (12), any claim family outside the registered set appearing in prose (13),
any pre-release banner on a committed file (14), and any internal production vocabulary on a
public page (15). Each prints the file, line, and rule for every hit.

Check 15 reads the docstrings, comments, and emitted strings of the scripts and text outputs
shipped inside the scanned trees as well as the markdown, because anyone reproducing the work
reads them. It is deliberately narrow: bare "ruling", "lane", "harvest", "sitting", "gate",
"pending", "wave", and "queue" are ordinary legal or ordinary English and are never matched;
only the multi-word production compounds built on them are. Where a matched label is data
rather than prose (the `claim_gate` column the comparator pipeline emits), it is allowlisted
by path, and the two verbatim registered instruments are exempt in full. The rule list, the
reasoning behind every deliberate exclusion, and every allowlist entry are documented in the
script itself; `--selftest` runs the fixtures without touching a repository file.

**16 — Claim-authority blocks.** The series of record, `results/series_2026-07.json`, is the
sole machine authority for the case-level census. The three front-door pages (README,
`index.md`, `article/THE_ARGUMENT.md`) each carry one marker-delimited claim block, and this
check derives the required census literals from the series JSON at run time — nothing in the
check restates a number — then requires each literal to appear inside its page's block. If
the series of record changes, the derived literals change with it, and any page still
carrying the old prose fails with the file, block, and missing literal printed.

**17 — Source-text leakage guard.** The release publishes citations, source registries, and
derived classifications, not redistributed opinion text. This check examines tracked files
and untracked files that are not excluded by `.gitignore`. It fails on source-text directory
names, a filename matching a registered `source_file`, or file content whose SHA-256 digest
matches a registered source opinion. It cannot identify an altered excerpt or an
unregistered source, so human review and secret scanning remain necessary.

**18 — Deadline freshness guard.** The comment window is time-sensitive publication text.
This check treats `_config.yml` as the authority for whether the window is active and for
its deadline. While active, README, index, and COMMENT must state the configured date; after
the date passes, an active window fails automatically. When the window is marked inactive,
registered invitations to submit comments fail so an expired call does not remain public.

**19 — Claims-ledger integrity.** The first check that reads
[`../article/CLAIMS_LEDGER.csv`](../article/CLAIMS_LEDGER.csv) directly. It asserts that the
ledger parses with the expected header, that every claim ID is well-formed and unique, that
no required field is blank, and that every path-like evidence route resolves to a file or
directory in this tree; it reports, without asserting, the split between claim-specific
public routes and primary-source-plus-private routes. It does not establish that a route is
the right route for its claim, that the cited primary source supports the claim, or that the
ledger covers every published number.

**20 — Generated-surface sync.** Some pages are renderings of machine sources:
[`../article/CLAIMS_INDEX.md`](../article/CLAIMS_INDEX.md) is generated from the claims
ledger, and `_data/series.yml` (the Pages site's census data) is generated from the series
of record. This check re-renders each from its source and fails on any drift, so neither
can be hand-edited into disagreement. It also holds the administrative-record pages to
their own chronology — a dated status line ("current as of ...", "no disposition posted as
of ...", a NOT YET PUBLISHED marker) must carry a date no older than the newest dated event
in [`../record/hud-27061/CHRONOLOGY.md`](../record/hud-27061/CHRONOLOGY.md), the gap that
once let a stale record README ship — and requires that everywhere a reader surface states
the number of appendices in words, the word matches the appendix files actually present. It
also cross-checks [`../article/FOOTNOTE_INDEX.md`](../article/FOOTNOTE_INDEX.md) against the
registered pointer inventory: every registered footnote must have an index row naming its
registered target.

## What a green run establishes

- Every registered statistic on a reader-facing surface reproduces from the committed
  artifacts.
- Registered footnote pointers resolve to the exact section and literals they cite.
- Internal navigation works, no local path leaked, and the committed tree matches the
  registered manifest.
- No superseded figure, withdrawn claim, stale banner, or production vocabulary appears on
  a reader-facing page, and the registered headline claims are present where they belong.
- No registered source-opinion file is present, and the comment-window language agrees with
  the configured publication deadline and active/inactive state.

## What a green run does not establish

- The legal correctness of any argument, the facts of any case, or the accuracy of any
  model classification. Validation layers measure **reproducibility** across independent
  classifiers, not accuracy against a human-coded gold standard (none exists at this
  corpus scale); see [`../method/VALIDATION.md`](../method/VALIDATION.md).
- The completeness of the underlying corpus. The per-row case-level record is now
  published, so the gate verifies the transformation: check 8 re-derives every registered
  case-level cell from [`case_level_census.csv`](case_level_census.csv) under the published
  rules. What stays outside the gate is the legal correctness of the classifications those
  rows carry — whether a given disposition is properly coded as a qualifying judgment, or a
  party properly coded as represented, is a legal judgment no script tests. The reproduction
  boundary for the case-level census is stated in [`REPRODUCE.md`](REPRODUCE.md).

## Relationship to the claims ledger

[`../article/CLAIMS_LEDGER.csv`](../article/CLAIMS_LEDGER.csv) is the registry of claims, and
`validate_claims.py` asserts the registered values against recomputation. Changing a claim
requires changing the page and the ledger in the same change set — that is the design, so no
series can drift silently.

## Environments

CI runs the gate twice: on Ubuntu with Python 3.11 and `requirements.txt` (the supported
dependency floor) and on Windows with Python 3.13 and `requirements-lock.txt` (the
environment recorded for the published outputs; see the lock file's header).

## Adding a claim

Add the claim to `CLAIMS_LEDGER.csv`, register its value, and update the page — in one
change set.

## Interpreting a failure

Each check prints the file, line, and rule for every failure. A failure is not always an
error in the flagged file: it can mean the ledger is out of step with a deliberate change.
Resolve by making the page, the ledger, and the checks consistent — never by weakening a
check to make a failure disappear.
