# Counsel-Timing Audit for the Eighteen Qualifying Cases

This directory hosts the docket-level counsel-timing audit the Note's footnote cites as
the "Audit file in the repository": a RECAP/PACER review of when plaintiff counsel first
appears on each qualifying case's docket, coded from locally archived docket records.

Contents:

- `FF_COUNSEL_TIMING.csv` -- the per-case audit file (one row per case; ECF-pinned
  evidence columns; UNKNOWN / UNAVAILABLE_PACER_ONLY recorded where the archive does not
  support a value, never inferred).
- `FF_COUNSEL_TIMING_REPORT.md` -- the audit report accompanying the CSV (methodology,
  headline tallies, per-case notes).

## Frame note (read before using the tallies)

The CSV carries 19 rows. The COUNTED eighteen qualifying cases are the 19 rows minus
V-GONZALEZ (not a qualifying judgment under the final finality classification) and
including V-MILLERBORG. The report's tallies are computed on that counted-eighteen frame;
the CSV is the record matching the Note's footnote.

On the counted-eighteen frame the footnote's figures reproduce from the CSV directly:

- `initial_prose` = FILED_BY_COUNSEL for 15 of 18 (source-verified by CM/ECF filer tag,
  signature block, or fee-award recital, per the evidence columns); the remaining 3
  (V-MCCREADY, V-WATSON, V-MILLERBORG) are recorded UNKNOWN, none coded pro se at filing.
- A dated first counsel entry exists for 17 of 18 (V-MILLERBORG's is UNKNOWN on the
  archived short-form docket).
- `post_dismissal_entry`: no counted case shows plaintiff counsel first appearing after a
  dismissal or adverse ruling.

## Caveats carried from the audit of record

The cells are machine-coded at screening grade against the locally archived docket
records; gaps are UNKNOWN or UNAVAILABLE_PACER_ONLY, never treated as absence. Some
evidence-column locators reference docket records that are not published in this
repository; the ECF numbers and dates they pin are quoted in the rows themselves.
