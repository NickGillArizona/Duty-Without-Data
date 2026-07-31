# Counsel-Timing Audit

A docket-level audit of when plaintiff counsel first appears on the docket of each of the
eighteen qualifying plaintiff-side judgments. Cells are machine-coded at screening grade,
coded 2026-07-17 from locally archived docket records only (no live web retrieval, no
PACER pulls); they are not human-validated. Gaps are recorded UNKNOWN or
UNAVAILABLE_PACER_ONLY, never as absence.

The audit file is `FF_COUNSEL_TIMING.csv` (one row per case, canonical case-list order,
schema-validated, ASCII). The CSV carries 19 rows: the eighteen counted qualifying cases,
plus V-GONZALEZ, which is retained for the record but is not a qualifying judgment (the
judgment entered there runs on ADA Title III only). Every tally below is computed on the
counted eighteen.

## 1. Results

- `counsel_at_qualifying_disposition`: YES 18 of 18. Every counted case was represented at
  the qualifying disposition date. In four of them (McClendon, Osborne, CareOne,
  Millerborg) the attorney NAMES of record at that date are UNKNOWN in the archive (empty
  RECAP attorney tables or label-only dockets), but representation itself is directly
  evidenced - counsel-filed motions resolved in the qualifying order, fee awards or
  fee-entitlement findings, counsel-briefed summary-judgment recitals; for Millerborg, the
  database representation coding with a machine-verified dispositive quote and the archived
  ECF 62.
- `initial_prose`: FILED_BY_COUNSEL 15 of 18; UNKNOWN 3 (Watson - staff-docketed paper
  complaint, first counsel-signed filing ECF 5, 2020-10-20; McCready - filed in state
  court, removal attachments PACER-only; Millerborg - complaint PACER-only on a short-form
  docket carrying no filer tags and no attorney table). ZERO counted cases are coded
  FILED_PRO_SE.
- `post_dismissal_entry`: zero YES. No counted case shows plaintiff counsel FIRST appearing
  after a dismissal or adverse ruling (15 NA counsel-from-filing; 2 NO on the archived
  record; 1 UNKNOWN).
- Dated first counsel entry: 17 of 18 (Millerborg's is UNKNOWN on the archived short-form
  docket); none of the dated entries falls after an adverse ruling.
- `presuit_org_involvement`, three tiers:
  - DOCUMENTED (6): Dorchester (federal administrative-agency complaint preceded the DOJ
    3614(a) suit; doc299 p.1); FHJC-Pelican (fair-housing-org plaintiff + tester
    investigation); Gilead (Connecticut Fair Housing Center co-plaintiff, its counsel filed);
    Grossman (Florida Commission on Human Relations complaint, reasonable-cause finding,
    private-action election; complaint paras. 4-5); Harmony (ACLU of Indiana from filing;
    pre-suit variance request); SWFHC-Scottsdale (fair-housing-org plaintiff + pre-suit
    tester investigation per CA9 memo at 1-3).
  - NONE_IN_RECORD (8): Horizon, Huston, McClendon, McCready, Nitschke, Osborne, CareOne,
    Robins (each caveated where the complaint itself is unarchived).
  - UNKNOWN (4): Hill, Skochko, Watson, Millerborg (complaints not archived; no pre-suit
    facts in docket text).
- `coder_confidence`: HIGH 9 / MEDIUM 9.

Six of the eighteen carry documented pre-suit organizational or agency involvement; the
archived record shows none in eight and is silent in four. Any generalization from those
tiers carries the unarchived-complaint caveats recorded in the rows.

## 2. Discrepancy register (all recorded in-row in `unavailable_notes`)

1. V-HILL: the case notes say filer tags begin at ECF 3; `docket_entries.json` shows ECF 1
   itself tagged "(Stacey, Francyne)". Resolved in favor of the entry text; conclusion
   unchanged.
2. V-MCCLENDON: an earlier free-layer docket survey attributed a "Potter Handy ->
   Uzeta/DREDF" counsel succession. The local archive does not support the DREDF element:
   DREDF appears nowhere; the complaint is Uzeta-signed under a Center for Disability
   Access (Potter Handy) caption; the 2021-2022 withdrawal entries are label-only. That
   attribution is unverified on this record and is not carried into the coding.
3. V-ROBINS: complaint signature block dated 2024-10-10 against docket entry and page
   stamps showing 2024-10-01 docketing; coded from the docket; filer identity consistent in
   both sources.
4. V-WATSON: entry-1 filer ambiguity (court-staff docketing, no signature notation) left
   UNKNOWN rather than resolved by inference.
5. V-FHJC-PELICAN: the archived `counsel.json` flattening carries null attorney-name
   fields; names rest on docket filer tags plus the attorneys-API summary in the case notes.
6. V-MCCREADY: state-court (pre-removal) representation status is unarchived;
   `post_dismissal_entry` is coded NO on the federal record only.

## 3. Limitations

- The cells are machine-coded at screening grade against locally archived docket records
  and are not human-validated.
- The four name-unknown counsel cells and the three UNKNOWN initial-filer cells cannot be
  resolved on the archived record; the underlying documents are PACER-only.
- The one filing-posture ambiguity that touches representation, Watson's initial filing,
  concerns who filed the complaint, not representation at any merits stage: Watson was
  counsel-represented from at latest 2020-10-20, two years before the qualifying
  disposition.
- This audit codes counsel timing on the qualifying-judgment cases only. It includes no
  comparison sample of represented losses, so it supports no inference about how counsel
  timing differs between winning and losing represented cases.
- Some evidence-column locators reference docket records held in the underlying research
  archive and not included in this repository; the ECF numbers and dates they pin are
  quoted in the rows themselves.
