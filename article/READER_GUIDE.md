# Reader Guide

If a search result or a direct link dropped you on an interior file, this page tells you
what kind of surface you landed on and where the authoritative version of each thing
lives. It is a router, not a summary; the front door is the [repository
README](../README.md).

## What is canonical

These surfaces are the versions of record. Where any other page appears to disagree with
one of them, the surface below governs.

| Surface | Authoritative for |
|---|---|
| [The manuscript](../manuscript/Duty_Without_Data.md) | The article's full text and footnotes as mirrored in this archive |
| [The series of record](../results/series_2026-07.json) | Every case-level census figure (counts, rates, intervals) |
| [The claims ledger](CLAIMS_LEDGER.csv) | The registered printed claims and their evidence routes; browsable as the generated [claims index](CLAIMS_INDEX.md) |
| [The HUD-27061 chronology](../record/hud-27061/CHRONOLOGY.md) | The dated administrative record of the form at the center of the argument |
| [The appendix crosswalk](APPENDIX_CROSSWALK.md) | Which appendix each manuscript footnote cites, and the lettering |

## What is supplementary

Cited support and extended analysis, subordinate to the canonical surfaces above: the
letter-keyed appendices (start from the [appendix index](appendices/README.md), which
maps them by question), the analysis memos under [`results/`](../results/README.md), and
the method documentation under [`method/`](../method/README.md). Each appendix states its
own evidence posture in its header.

## What is historical

Retained for the record, not current findings: the superseded document-level outcome
series (labeled where they appear; the case-level census replaced them for outcome
reporting), the as-run validation and comparator artifacts (frozen at their run dates by
design), and the 2026 comment-window record ([COMMENT.md](../COMMENT.md)). What was
superseded and why is stated in [Evidence and Limits](EVIDENCE_AND_LIMITS.md).

## Which surface answers which question

| Your question | Go to |
|---|---|
| What does the article argue? | [The argument in brief](THE_ARGUMENT.md), or the [full manuscript](../manuscript/Duty_Without_Data.md) |
| Is a printed number supported? | [Claims index](CLAIMS_INDEX.md), then the [worked verification example](../replication/VERIFY_ONE_CLAIM.md) |
| What are the limits of the evidence? | [Evidence and Limits](EVIDENCE_AND_LIMITS.md) and [AI use](../AI_USE.md) |
| What does HUD's own record show? | [The administrative record](../record/hud-27061/CHRONOLOGY.md) and [Appendix C](appendices/Appendix_C_HUD_Administrative_Record.md) |
| How was the analysis built and checked? | [Methodology](../method/METHODOLOGY.md), [validation](../method/VALIDATION.md), and the [system map](../method/SYSTEM_MAP.md) |
| Can I reproduce it myself? | [Reproduction guide](../replication/REPRODUCE.md) and the [release gate](../replication/GATES.md) |
| What can be done about the problem? | [Implementation materials](../action/README.md) |

## Where the evidence boundary lives

[Evidence and Limits](EVIDENCE_AND_LIMITS.md) is the canonical statement of what the
archive establishes and what it does not: what is mechanically reproducible versus what
rests on judgment, the adverse preregistered findings, and the structural limitations.
Nothing in this repository asserts a claim-success rate, a causal estimate, or the legal
correctness of any classification, and no census figure should be quoted from memory of
this guide — take numbers from the pages that carry them, which the release gate binds to
the series of record.
