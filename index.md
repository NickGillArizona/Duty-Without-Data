---
layout: default
title: Duty Without Data
---

# Duty Without Data

Disability fair-housing rights are enforceable on paper. Administering and proving them often
depends on transaction and asset records that existing systems create only in fragments — pieces
no cross-program system reliably links, transmits, or makes accessible. This page is the short
version of a law-review Note about that gap — and the narrow, already-drafted administrative fix
it proposes.

Nicholas Gill, *Duty Without Data: Disability Fair Housing and the Record-Dependent Right*,
forthcoming, Arizona Law Review (2026).
[Full repository on GitHub](https://github.com/NickGillArizona/Duty-Without-Data).

<!-- claim-block: census-headline -->
**The finding, in three numbers.** Of **606 decided cases** in an original corpus of 1,900
screened federal disability fair-housing opinion and order records, **eighteen** ended in a
qualifying plaintiff-side judgment — and none of the 400 pro se cases did. These are
descriptive results, not causal estimates. The Note's response is a narrow rulemaking
petition under 5 U.S.C. § 553(e).
<!-- /claim-block -->

[Read the argument](#the-argument) ·
[Verify a claim](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/VERIFY_ONE_CLAIM.md) ·
[Reproduce the analysis](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/REPRODUCE.md) ·
[Cite](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/CITATION_GUIDE.md) ·
[Contact](mailto:nickgill@arizona.edu)

## The story

In 2010, the housing authority in Mobile, Alabama issued Donavette Ely a larger Section 8 voucher
because her son's asthma was severe enough that his physician recommended a bedroom with its own
temperature controls. The authority's own written explanation tied the voucher to his medical
condition. When Ely could not find an affordable four-bedroom unit in time and asked for more time
to search, the authority refused — and later removed the family from the program. The Eleventh
Circuit held the authority could not be liable, because Ely "never explained" that her extension
request was connected to her son's disability. *Ely v. Mobile Housing Board*, 605 F. App'x 846,
851–52 (11th Cir. 2015).

The explanation was sitting in the authority's own file. No record system carried it forward to the
moment of decision. The right was not absent; the record architecture was.

## The argument

Disability fair-housing rights are *record-dependent*: proving them turns on records of what
landlords and housing agencies did — who requested what and when, what the answer was, which
accessible units exist and who lives in them. HUD's own instruments create pieces of those
records, but no identified coordinated federal system reliably collects, links, or makes them
accessible.

The gap is not a missing statute. Congress gave HUD express data-collection rulemaking authority in
1988 (42 U.S.C. § 3614a; § 3608(e)(6)), and HUD's own regulation, 24 C.F.R. Part 121, has named
handicap and family characteristics as data categories since 1989. In 2022, HUD proposed collecting
protected-class data, citing the Fair Housing Act and Part 121. In 2023, the approved version
collected race and ethnicity only, with no explanation of where the disability categories went. In
June 2026, HUD proposed renewing the narrowed form unchanged, as the approval ran to its June 30,
2026 expiration.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/NickGillArizona/Duty-Without-Data/main/action/figures/form_27061_timeline_dark.svg">
  <img src="https://raw.githubusercontent.com/NickGillArizona/Duty-Without-Data/main/action/figures/form_27061_timeline_light.svg" width="760" alt="Timeline of Form HUD-27061: 2022 proposal including disability, 2023 approval without it, 2026 renewal of the narrowed form.">
</picture>

The stakes are measurable. In an original dataset of 1,900 screened federal disability
fair-housing opinion and order records, a case-level census of every decided case found that qualifying plaintiff-side
judgments — final contested judgments, final defaults, and liability determinations with the remedy
unresolved — issued eighteen times in four
and a half years, roughly 3% of the 606 decided cases overall, with none in the short middle window. In every one,
counsel had appeared for the plaintiff; none arose in a pro se case. And the share of the decided docket brought without a lawyer rose from
59.6% to 76.1%.

The chart below puts those two series in one frame, across the census's three periods — P1
(January 1, 2022 – June 27, 2024), P2 (June 28, 2024 – February 4, 2025), and P3 (February 5,
2025 – July 1, 2026). The top line is who files: the share of decided cases brought without a
lawyer, a majority in every period and 76.1% by the end. The bottom line is how often plaintiffs
win: the qualifying-judgment rate, under 4% in every period and zero in P2. The gap between the
two lines is the figure's point — the docket is increasingly pro se, and every one of the
eighteen qualifying judgments sits on the counseled side of it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/NickGillArizona/Duty-Without-Data/main/results/figures/fig1_composition_dark.svg">
  <img src="https://raw.githubusercontent.com/NickGillArizona/Duty-Without-Data/main/results/figures/fig1_composition_light.svg" width="760" alt="Line chart across three periods: the pro se share of the decided docket rises from 59.6% to 76.1%, while the qualifying-judgment rate runs at 3.48% and 3.19% in P1 and P3 and zero in the short P2 window; eighteen qualifying plaintiff-side judgments in all, none pro se.">
</picture>

And the way unrepresented plaintiffs lose points straight back at missing records: among
pleading-stage losses, factual narratives that never get translated into the legal elements courts
screen for are markedly more common in pro se losses than in represented ones; the coding is
machine-based, so the finding is directional. Private lawsuits do not
substitute for administrative records; they depend on them.

The full compression for lawyers — the case, the authorities, the administrative record, the
remedy, the objections and answers — is
[THE_ARGUMENT.md](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/article/THE_ARGUMENT.md).

## The method

The dataset behind those numbers did not exist before this project; the archive documents the
model-assisted classification method used to build it. Several separately run AI models — from
different providers — each read every court opinion and answer the same fixed questions about it;
when all three models disagree, the split escalates to a designated adjudication model under prespecified adjudication rules; the headline finding gets its
own separate model ensemble, which is then audited blind by a different vendor's models. Nine models
across five validation layers, with the frozen prompts, adjudication rules, and the headline
ensemble's disagreement record published (the primary pipeline publishes tier metadata in place of
per-model raw outputs), a claims ledger tying every number in the paper to the script that produced
it, and a primary three-classifier run that cost $85.59 inside a roughly $160 pipeline. The project
was conceived, directed, and adjudicated by the author; the models classify — coding answers to
fixed questions about each opinion — and the agreement
rates are reported rather than asserted. The full design — and a step-by-step guide to running the
method on your own research question — is in
[METHODOLOGY.md](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/method/METHODOLOGY.md).

Behind the article is a public research and replication archive: frozen prompts, documented
classification rules, independent re-reads, claim-to-artifact mappings, and an automated release
gate. Editors checking a citation should start with the
[footnote index](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/article/FOOTNOTE_INDEX.md);
researchers rerunning the work should start with
[REPRODUCE.md](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/REPRODUCE.md).

## The remedy

The Note does not ask a court to order HUD to build a database. It proposes a petition under
5 U.S.C. § 553(e) — the APA provision letting any interested person petition an agency for a rule —
asking HUD for a companion disability-data rule grounded in authority Congress granted in 1988.
Filing it obligates HUD to respond within a reasonable time and to state the grounds for any denial
(5 U.S.C. § 555(b), (e)), and a denial gets ordinary reasoned-explanation review under
*Massachusetts v. EPA*, 549 U.S. 497, 527–28 (2007). The remedy for an unreasoned denial is a
remand for explanation — not judicial database design. The limiting principle: make duties Congress
already enacted verifiable; derive no new ones.

Drafted, adaptation-ready templates — the petition (organizational and individual variants), the
2026 comment, the contingent judicial-review layer, and a standing brief — are in
[action/](https://github.com/NickGillArizona/Duty-Without-Data/tree/main/action), each drafted
by a J.D. candidate, not an attorney, for adaptation by counsel. Nothing on this site is legal
advice, no attorney-client relationship is created by using it, and the site was drafted with LLM
assistance and reviewed and approved by the author.

## The comment window closes Tuesday, August 11, 2026

HUD's notice proposing to renew Form HUD-27061 unchanged published June 12, 2026 (91 Fed. Reg.
35,697), and comments are due August 11, 2026, on
[regulations.gov Docket No. HUD-2006-0214](https://www.regulations.gov/docket/HUD-2006-0214).
The shareable how-to — the record in four dates, filing tracks for organizations and for
individuals, and a one-page memo formatted for forwarding to counsel — is the
[comment page](https://nickgillarizona.github.io/Duty-Without-Data/comment/).
Comments filed now become part of the administrative record HUD must evaluate — and that any later
court can read. An adaptable comment template is in the
[advocacy kit](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/action/2026_comment_template.md),
and the author's own filed comment
([Comment No. HUD-2006-0214-0011](https://www.regulations.gov/comment/HUD-2006-0214-0011)) serves
as a worked example.

After the window closes, the petition materials remain the live path.

The time-ordered playbook — now, next, and only-if-HUD-denies — is
[TAKE_ACTION.md](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/TAKE_ACTION.md).

## The archive

Every number in the Note has a paper trail:
[CLAIMS_LEDGER.csv](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/article/CLAIMS_LEDGER.csv)
maps each empirical sentence to its source, script, output, and footnote, and the analysis re-runs
with the commands in
[REPRODUCE.md](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/REPRODUCE.md). The
manuscript, eighteen appendices, the multi-model methodology, and the validation materials are all
in the [repository](https://github.com/NickGillArizona/Duty-Without-Data). Start with the
[README](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/README.md).

Questions, corrections, or a walkthrough for your organization:
[open an issue](https://github.com/NickGillArizona/Duty-Without-Data/issues) or email
[nickgill@arizona.edu](mailto:nickgill@arizona.edu).
