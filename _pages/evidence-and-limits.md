---
layout: default
title: "Evidence and Limits"
permalink: /evidence-and-limits/
description: "What the Duty Without Data archive establishes, what requires judgment, the adverse preregistered findings, and the structural limits of the evidence."
---

# Evidence and Limits

What the archive establishes, what it does not, and where every number comes from.

The archive earns trust by what it discloses against itself. The canonical statement is the
repository's
[Evidence and Limits page](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/article/EVIDENCE_AND_LIMITS.md);
this page is the short version.

## The series of record

The reported outcome series is a one-case-one-unit census: {{ site.data.series.n_pooled }} decided
cases ({{ site.data.series.n_by_period }} across three periods), with
{{ site.data.series.qualifying_phrase }} ({{ site.data.series.qualifying_by_period }} by period;
per-period rates {{ site.data.series.rates_prose }}). Counsel had appeared in every qualifying
judgment: {{ site.data.series.represented_cell }} represented cases ended in one, and
{{ site.data.series.pro_se_cell }} pro se cases did. The pro se share of decided cases rose from
{{ site.data.series.share_span }}. **No aggregate trend is asserted in either direction.** An
earlier document-level analysis supported decline framings that the case-level census does not;
it is superseded for outcome reporting and retained only as labeled pipeline output.

## Reproducible versus judgment

Counts, rates, intervals, file integrity, and the release gate's checks are mechanically
reproducible from released materials. Whether the corpus is complete, whether each legal
classification is correct, whether machine-coded labels are substantively accurate, and whether
any observed pattern is causal all require independent judgment — no green badge establishes them.

## Adverse findings, reported

Four preregistered results cut against the convenient reading, and each is reported where it
occurred: a pre-trend adverse to sharp shock-attribution; an inconclusive case-mix selection
audit; a subset non-replication disclosed rather than smoothed; and a coding field that failed
blind validation and therefore supports no reported analysis. The specifics — with their numbers,
which live in the ledgered sources rather than on this page — are in
[Evidence and Limits](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/article/EVIDENCE_AND_LIMITS.md)
and the appendices it cites.

## Structural limits

- The corpus measures the decisional pipeline, not violations; nothing here is a claim-success
  rate.
- No causal estimates: the design does not identify the effect of representation, records, or
  case selection.
- Machine-coded layers are labeled as such; the archive measures reproducibility, not accuracy
  against a human-coded benchmark.
- Negative existence claims are statements about the located record after documented searches —
  never proof of absence.

## Verify a claim yourself

Every registered claim has a route: start at the
[claims index](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/article/CLAIMS_INDEX.md),
then follow the
[worked verification example](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/VERIFY_ONE_CLAIM.md).
The [methods and replication page](https://nickgillarizona.github.io/Duty-Without-Data/methods-and-replication/)
routes to the full reproduction path.
