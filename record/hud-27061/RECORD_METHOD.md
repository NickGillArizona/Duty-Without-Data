# Administrative-Record Assembly: Method and Limitations

How the Form HUD-27061 / OMB 2535-0113 record in this directory was assembled, what was
searched, what was included, and what the method cannot establish. The dated results are
in [`CHRONOLOGY.md`](./CHRONOLOGY.md); quotation checks are in
[`quote_verification_report.md`](./quote_verification_report.md); the integrity manifest
(SHA-256 per file) is [`file_inventory.csv`](./file_inventory.csv).

## Scope and sources

The record covers the collection's public administrative trail from its earliest archived
ICR cycle (2003) through the 2026 renewal notice, across four source systems:

1. **Federal Register** — every located notice bearing OMB Control No. 2535-0113, plus
   the Part 121 promulgation and the related rulemaking documents the Note cites.
2. **Reginfo.gov** — the ICR history for 2535-0113: per-cycle landing pages, document
   lists, and supporting statements for each located cycle, 2003–2023.
3. **Regulations.gov** — the public-comment record for the 2022 60-day docket and the
   2026 renewal docket.
4. **Oversight records** — the GAO and HUD OIG reports the Note cites, retrieved from
   the issuing agencies.

Retrieval dates, query terms, and per-document URLs are recorded in
[`../../replication/DATA_PROVENANCE.md`](../../replication/DATA_PROVENANCE.md) §§ 1.1–1.4
and in `file_inventory.csv`.

## Method

Collection combined scripted harvests of the Federal Register and reginfo.gov records
with manual retrieval and verification of individual documents. Language-model assistance
was used to organize searches and draft working summaries; every document relied on was
retrieved and archived as a primary source, every quotation used from the record was
checked against the archived original (see `quote_verification_report.md`), and the
tabulated cycle data in `longitudinal_tables.csv` derive from the archived reginfo.gov
pages themselves. The working research memoranda produced during assembly are retained in
the project's private research records (see `DATA_PROVENANCE.md`); this directory's
documents are the terminal public record.

## Inclusion rules

- A document is included if it is part of the collection's public administrative trail
  (notice, supporting statement, ICR record, public comment) or an oversight record the
  Note cites.
- Text extractions (`.txt`) accompany binary documents where extraction was reliable;
  the binary is always the source of record.
- Duplicate copies preserved under distinct source object IDs are retained and labeled.

## Limitations

- **Located-record discipline.** Negative statements ("no contemporaneous explanation in
  the located record," "no successor ICR on record") are claims about the located public
  record after the documented searches, not assertions about internal agency files. The
  FOIA package in [`foia/`](./foia/) targets the internal decisional record the public
  trail cannot reach.
- **Status statements are dated.** Statements about the renewal's posture speak as of
  the archived status pulls; readers should check the live docket and ICR record for
  later developments.
- **No litigation posture.** This directory documents an administrative record. It
  contains no complaint, no plaintiff analysis, and no litigation strategy; the Note's
  Part IV states the legal framework, and any judicial-review materials would have to be
  developed from an actual agency disposition.
