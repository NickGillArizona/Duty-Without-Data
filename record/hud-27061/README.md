# `record/hud-27061/` — Record Map

**Contents current as of July 2026.**
**Research subject:** HUD Form 27061 (OMB Control No. 2535-0113) — 2022–2023 PRA reversion
**Research output:** forthcoming law review note + APA viability record

This README is the canonical map of files in `./record/hud-27061/`. The directory contains three layers:

1. **Primary-record files** — federal-government-issued documents harvested from the public record.
2. **Research-product files** — the methodology memorandum and analytical artifacts.
3. **FOIA-preparation files** — the FOIA package that operationalizes the research. (Litigation and petition templates live in the repository-root [`action/`](../../action/) kit.)

---

## Quick pointers

- **Start here:** [`CHRONOLOGY.md`](./CHRONOLOGY.md) (the dated record, with primary-source citations) and [`RECORD_METHOD.md`](./RECORD_METHOD.md) (how the record was assembled, and its limits). Quotation checks: [`quote_verification_report.md`](./quote_verification_report.md).
- **Integrity manifest:** [`file_inventory.csv`](./file_inventory.csv) (SHA256 hashes of every primary-record file).
- **Longitudinal data:** [`longitudinal_tables.csv`](./longitudinal_tables.csv) (15 Federal Register notices, 10 ICR cycles, 2022-vs-2023 reconciliation).
- **FOIA package:** [`foia/FOIA_filing_guide.md`](./foia/FOIA_filing_guide.md) + three request letters.
- **Litigation and petition templates:** [`action/`](../../action/) at the repository root.

---

## File index

### Methodology and analysis

| File | What it is |
|---|---|
| `CHRONOLOGY.md` | The dated administrative-record chronology, with primary-source citations. |
| `RECORD_METHOD.md` | How the record was assembled: scope, sources, method, and limitations. (The full working memorandum behind both is retained in the project's private research records.) |
| `file_inventory.csv` | SHA256 integrity manifest for primary-record files. |
| `longitudinal_tables.csv` | Three-table longitudinal dataset (FR notices, ICR cycles, 2022/2023 reconciliation). |
| `quote_verification_report.md` | pandoc/pdftotext/antiword verification pass for all Tier 1 quotations in § 9. |
| `cfr_part121_analysis.md` | Historical-snapshot verification of 24 CFR Part 121 as "Collection of Data" (not Faith-Based Organizations). Confirms HUD's 2022 citation was accurate. |

A Regulations.gov re-run on 2026-04-18 confirmed record stability (1 comment; 8 documents);
that capture is author-held and not distributed with this archive.

### Primary-record files (2003–2023 PRA record)

Federal Register notices:

| File | Source URL |
|---|---|
| `FRN60_2023.pdf` / `.txt` | FR Doc. 2022-20868, 87 FR 58524 (Sept. 27, 2022) — the 60-day expansion proposal |
| `FRN30_2023.pdf` / `.txt` | FR Doc. 2023-01699, 88 FR 5370 (Jan. 27, 2023) — the 30-day reversion |

Supporting Statements (RegInfo.gov / OIRA):

| File | OIRA cycle | Concluded |
|---|---|---|
| `SSA_2023.docx` / `.txt` | 202301-2535-001 | 2023-06-13 |
| `SSA_2019.docx` / `.txt` | 201904-2535-001 | 2019-07-01 |
| `SSA_2014.docx` / `.txt` | 201306-2535-001 | 2014-01-02 |
| `SSA_2006.doc` / `.txt` | 200609-2535-001 | 2006-11-21 |

Public comments:

| File | Source |
|---|---|
| `comment_SAGE.pdf` / `.txt` | Jones Day on behalf of Services & Advocacy for LGBT Elders, 2022-11-23, Regulations.gov ID HUD-2006-0214-0008 (12 pp.) |
| `comment_Williams1.pdf` / `.txt` | Williams Institute email, 2022-10-10 |
| `comment_Williams2.pdf` | BYTE-IDENTICAL DUPLICATE of `comment_Williams1.pdf` (OIRA cataloging artifact — count as one submission) |

RegInfo.gov landing pages:

| File | What it is |
|---|---|
| `icr_*.html` (N=10) | ICR summary page for each of the 10 OIRA cycles associated with OMB 2535-0113 |
| `doc_*.html` (N=10) | Document-listing page for each of the 10 cycles |

### FOIA package

| File | Agency | Target |
|---|---|---|
| [`foia/FOIA_filing_guide.md`](./foia/FOIA_filing_guide.md) | — | Filing procedures, timelines, response handling, staggered strategy |
| [`foia/FOIA_1_HUD_pre2006_records.md`](./foia/FOIA_1_HUD_pre2006_records.md) | HUD | 2003-cycle Supporting Statements (OIRA refs 200302-2535-001 and 200308-2535-001) |
| `foia/FOIA_2_HUD_internal_communications.md` | HUD | Planned request; template not committed in this public archive. |
| `foia/FOIA_3_OMB_OIRA_passback.md` | OMB/OIRA | Planned request; template not committed in this public archive. |
| [`foia/foia_tracking.csv`](./foia/foia_tracking.csv) | — | Tracking template with filing priorities |

**Filing sequence (recommended):** FOIA 2 (week 1) → FOIA 3 (week 2) → FOIA 1 (week 4). See filing guide §6.

### Litigation-preparation templates (in `action/`)

These are drafted by a JD candidate, not an attorney. They are templates meant to accelerate counsel's work, not filed documents. The kit lives in the repository-root [`action/`](../../action/) directory; the index below points at those locations.

| File | What it is |
|---|---|
| [`../../action/2026_comment_template.md`](../../action/2026_comment_template.md) | Detailed public-comment template for the 2026 60-day window, asking HUD to address on the record the 2022 protected-class proposal, § 3608(e)(6), Part 121. |
| [`../../action/553e_petition_template.md`](../../action/553e_petition_template.md) | 5 U.S.C. § 553(e) petition for rulemaking / modification of the approved ICR; alternative vehicle to the 2026 comment. Drafted for an *organizational* petitioner. |
| [`../../action/553e_petition_individual.md`](../../action/553e_petition_individual.md) | 5 U.S.C. § 553(e) petition adapted for an *individual* petitioner with a disability, relying on Part 8 accessibility hooks and the broader "interested person" standard. Complements rather than duplicates the organizational petition. |

---

## Key dates

| Date | Event |
|---|---|
| 2022-09-27 | 60-day notice published (87 FR 58524) — proposed protected-class expansion |
| 2022-11-23 | SAGE/Jones Day comment filed |
| 2022-11-28 | 60-day comment period closed (only 1 substantive comment received) |
| 2023-01-27 | 30-day notice published (88 FR 5370) — silent reversion to race/ethnicity only |
| 2023-02-27 | 30-day comment period closed |
| 2023-06-13 | OIRA approved 2023 cycle (ref 202301-2535-001) |
| 2026-04-18 | Research harvest; methodology memo and FOIA package drafted (citations and Alliance-standing content post-verified) |
| 2026-06-30 | Current approval expires |
| **Expected 2025/2026** | **60-day notice for the triennial renewal — NOT YET PUBLISHED as of 2026-04-18.** Absence is itself a publishable finding. See §12.11 and §24. |

---

## Reliability framework

The underlying methodology memorandum (retained in the project's private research records) tagged every factual assertion `[T1]`, `[T2]`, or `[T3]`; the same tiers govern the documents here:

- **T1** — verbatim from primary source, verified against source binary (SHA256 hashes in Appendix B; verification log in `quote_verification_report.md`).
- **T2** — LLM-extracted, spot-checked.
- **T3** — analytical / synthesized.

Every Tier 1 quotation was re-verified on 2026-04-18 using pandoc, pdftotext, and antiword against the source binaries. No material mismatches were found.

---

## What's not here (intentionally)

- **No internal HUD records.** The public-record harvest does not reach the internal decisional record. The FOIA package targets that gap.
- **No plaintiff identified.** Plaintiff selection belongs to counsel; no plaintiff-development analysis is published in this archive (litigation-development materials are retained in the project's private research records).
- **No filed pleadings.** The `action/` templates are drafted for counsel's review, not filing.
- **No legal advice.** The author is a JD candidate, not an attorney. Nothing here creates an attorney-client relationship.

## Byte-identical filename aliases (intentional)

Four document pairs in this directory are byte-identical copies under two filenames. Both names
are retained deliberately: each name is cited by as-run research records (the claims ledger and
crosswalks cite one convention; the methodology memorandum, quote-verification report, and file
inventory cite the other), and renaming either side would break the as-run citations. Git stores
identical content once, so the duplication costs nothing; treat the pairs as aliases.

| Copy A | Copy B | SHA-256 (first 12) |
|---|---|---|
| `88FR5370_30day_notice.pdf` | `FRN30_2023.pdf` | `c55c5750b57b` |
| `87FR58524_proposal.pdf` | `FRN60_2023.pdf` | `9f42ca6f24da` |
| `2535-0113_supporting_statement_A.docx` | `SSA_2023.docx` | `46bba4c8585e` |
| `SSA_2023.txt` | (formerly `fresh_extract/SSA_2023_fresh.txt`; duplicate removed 2026-07-10) | `4c7ccdbf7325` |

`comment_Williams1.pdf` and `comment_Williams2.pdf` are also byte-identical (`763ab1f6fc40`):
the same attachment was posted under two regulations.gov docket entries, so both entries are
preserved as they appear on the docket. The unreferenced duplicate text extracts
`fresh_extract/SSA_{2014,2019,2023}_fresh.txt` were removed 2026-07-10; the canonical extracts
remain at `SSA_2014.txt`, `SSA_2019.txt`, and `SSA_2023.txt`.
