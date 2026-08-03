# Duty Without Data

*Disability Fair Housing and the Record-Dependent Right* — research and replication archive

Nicholas Gill · Forthcoming, **Arizona Law Review** (2026)

**Web companion:** [five-minute version](https://nickgillarizona.github.io/Duty-Without-Data/).

> [!IMPORTANT]
> Federal disability fair-housing rights depend on records—requests, decisions, accessible units, occupancy—that HUD systems create only in fragments and no identified cross-program system reliably links, transmits, or makes accessible.

- **Understand the argument** — [Argument in brief](article/THE_ARGUMENT.md) · [full manuscript](manuscript/Duty_Without_Data.md) · [reader guide](article/READER_GUIDE.md)
- **Verify a printed claim** — [Claims index](article/CLAIMS_INDEX.md) · [ledger](article/CLAIMS_LEDGER.csv) · [worked verification](replication/VERIFY_ONE_CLAIM.md)
- **Review method and limits** — [Methodology](method/METHODOLOGY.md) · [validation](method/VALIDATION.md) · [reproduce](replication/REPRODUCE.md)
- **Find an appendix** — [Browse by question](article/appendices/README.md) · [exact crosswalk](article/APPENDIX_CROSSWALK.md)
- **Use the implementation materials** — [Time-ordered options](action/TAKE_ACTION.md) · [petition and comment materials](action/README.md)

**The problem, in one case.** In 2010 the Mobile Housing Board gave Donavette Ely a four-bedroom Section 8 voucher because her son’s asthma required a bedroom with separate temperature controls—the Board’s own written explanation cited his medical condition. When she could not find a qualifying unit in time, the Board granted one extension, refused more, and removed the family from the program. The Eleventh Circuit affirmed judgment for the Board: Ely “never explained” that her request was connected to her son’s disability. *Ely v. Mobile Hous. Bd.*, 605 F. App’x 846, 851–52 (11th Cir. 2015). The explanation sat in the Board’s own file; no record system carried it forward.

**The paper trail.** Congress gave HUD express fair-housing data authority in 1988; HUD’s own regulation has named disability-related data categories since 1989. One collection, three notices:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="action/figures/form_27061_timeline_dark.svg">
  <img src="action/figures/form_27061_timeline_light.svg" width="760" alt="Three panels comparing Form HUD-27061 across the 2022 proposal, the 2023 approved form, and the 2026 renewal. In 2022 HUD proposed adding protected-class categories, citing the Fair Housing Act and 24 CFR 121, whose categories include disability and family characteristics. The 2023 approved form collects race and ethnicity only, and the 2023 notice never uses the words disability, handicap, protected class, or Fair Housing Act. The 2026 renewal proposes the same form unchanged while still describing it as collecting other protected class data required by the Fair Housing Act. The burden estimate is identical in all three: 14,375 respondents and 8,625 annual hours.">
</picture>

*Proposed with disability categories (60-day notice, Sept. 27, 2022, 87 FR 58,524); approved without them (30-day notice, Jan. 27, 2023, 88 FR 5,370); renewal proposed unchanged (June 12, 2026, 91 FR 35,697) — [full chronology](record/hud-27061/CHRONOLOGY.md).*

The Note proposes a narrow response: petition HUD under 5 U.S.C. § 553(e), requiring the agency either to begin building the missing record architecture or explain on the record why it will not. A data category an agency invoked and then abandoned without explanation is what reasoned-explanation review exists to test.

## What the archive shows

<!-- claim-block: census-headline -->
From an original corpus of 1,900 screened federal opinion and order records, a one-case-one-unit census of the **606 decided cases** found **eighteen qualifying plaintiff-side judgments**—nine final contested judgments awarding relief, two final default judgments awarding relief, and seven liability determinations with the remedy still unresolved. About 3% of decided cases; across the per-period rates, **3.48% / 0.00% / 3.19%**, no decline or increase was detected (no equivalence is claimed). What moved is who fills the docket: the pro se share of decided cases rose from **59.6% to 76.1%**—and counsel had appeared in every one of the eighteen qualifying plaintiff-side judgments. **18 of 206 (8.7%)** represented cases ended in a qualifying judgment; **0 of 400** pro se cases did.
<!-- /claim-block -->

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="results/figures/fig1_composition_mobile_dark.svg">
  <source media="(max-width: 600px)" srcset="results/figures/fig1_composition_mobile_light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="results/figures/fig1_composition_dark.svg">
  <img src="results/figures/fig1_composition_light.svg" width="760" alt="Across three periods, the pro se share of decided cases rises from 59.6 percent to 76.1 percent while qualifying plaintiff-side judgments remain rare; none of the eighteen qualifying judgments was pro se.">
</picture>

*Figure 1. Case-level census from the registered July 2026 series, across periods P1–P3. P2 is a short window; all rates use one case as one unit.*

**Evidence boundary.** These are descriptive results, not a causal estimate. A separate machine-coded pleading-stage analysis supplies directional evidence about facts left untranslated into legal elements; it is not human-coded ground truth. Models are documented instruments, not legal authorities, and agreement does not establish accuracy.

**Source texts.** Full case texts are not distributed here; the validation and comparator texts are on file with the author, with CourtListener identifiers, URLs, and SHA-256 hashes preserved in [`opinion_sources.csv`](opinion_sources.csv).

## Check, do not just trust

[![Release checks](https://github.com/NickGillArizona/Duty-Without-Data/actions/workflows/release-checks.yml/badge.svg)](https://github.com/NickGillArizona/Duty-Without-Data/actions/workflows/release-checks.yml)

Every reported number should resolve to a registered claim, its analytical unit, and its generating artifact.

1. Find the statement in the [claims ledger](article/CLAIMS_LEDGER.csv).
2. Follow the complete [18-of-606 worked example](replication/VERIFY_ONE_CLAIM.md).
3. Check the [sample and denominator definitions](replication/SAMPLE_DEFINITIONS.md).
4. Re-run the documented route in the [reproduction guide](replication/REPRODUCE.md).

The release gate tests the registered series, figures, appendix pointers, links, manifest, and claim hygiene on every change. A green badge establishes internal consistency and reproducibility—not the truth of every legal or model-coded judgment.

## Implementation materials

> [!NOTE]
> Form HUD-27061 renewal comments are due August 11, 2026 — the [comment guide](COMMENT.md) explains how to file. The § 553(e) petition does not expire with the window — the [petition sequence](action/TAKE_ACTION.md) is drafted for adaptation at any time. Materials are illustrative templates requiring independent legal review, not legal advice.

The [implementation materials](action/README.md) are keyed to the archived record: the model § 553(e) petition templates, the 2026 comment template, the author's as-filed comment, and an adaptation checklist. **No litigation template is provided** — any complaint must be developed by counsel from an actual agency disposition, and none exists.

## Cite and reuse

Use GitHub’s **Cite this repository** control or the [citation guide](CITATION_GUIDE.md). Code is MIT licensed; data and documents are CC BY 4.0, subject to the [licensing guide](LICENSING.md).

## AI disclosure

Language models assisted classification, code development, analysis, and editing. The author reviewed the case-level census, made all legal and interpretive judgments, and is responsible for the manuscript and repository; no model output is cited as legal authority. Raw outputs are published for the headline validation ensemble, adjudication-tier metadata for the primary pipeline (boundary: [system map](method/SYSTEM_MAP.md)). Full roles, instruments, limitations: [AI_USE.md](AI_USE.md); attributions: [third-party notices](THIRD_PARTY_NOTICES.md).

## About the author

J.D. candidate, Class of 2027, University of Arizona James E. Rogers College of Law. Corrections: [nickgill@arizona.edu](mailto:nickgill@arizona.edu) or [open an issue](https://github.com/NickGillArizona/Duty-Without-Data/issues).

This archive is about disability rights, so its pages must stay usable with assistive technology; anything hard to use through a screen reader is a bug—report it.
