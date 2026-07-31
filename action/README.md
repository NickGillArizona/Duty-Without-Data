# Administrative Action Materials

This directory contains research templates for counsel's independent review and
adaptation. Each canonical template identifies its filing posture, the facts the filer
must supply, and the authorities to verify; [`ADAPTATION_CHECKLIST.md`](./ADAPTATION_CHECKLIST.md)
is the adaptation procedure. No document is legal advice, and no template is ready for
filing without counsel's case-specific review.

The materials implement the next steps proposed by the Note *Duty Without Data:
Disability Fair Housing and the Record-Dependent Right* (Arizona Law Review, forthcoming
2026). They were drafted by a J.D. candidate, not an attorney, with LLM assistance and
author review. They are research materials, not legal advice; nothing here creates an
attorney-client relationship; and the decision whether and what to file belongs to the
filer and the filer's counsel.

**Current posture.** As of the archived record cutoff of July 8, 2026, HUD's June 12,
2026 renewal notice remains pending and OMB has posted no disposition; the collection's
displayed expiration date of June 30, 2026 has passed. Every template is written to
survive either outcome -- whether the collection is renewed or allowed to lapse -- and none
asserts that either has occurred.
Check the official record before filing; the archived status pulls are at
[`../article/appendices/admin_record_c/pra_comment_2026/oira_status_pulls.md`](../article/appendices/admin_record_c/pra_comment_2026/oira_status_pulls.md).

## Canonical router

| Task | Canonical document | Filing posture | Required reviewer |
|---|---|---|---|
| Build the renewal record now | [`2026_comment_template.md`](./2026_comment_template.md) | PRA public comment, Docket ID HUD-2006-0214 (Document ID HUD-2006-0214-0010); comments close Tuesday, August 11, 2026 | Organization's own counsel or authorized signatory |
| Brief a board or counsel in one page | [`comment_memo_2026.md`](./comment_memo_2026.md) ([PDF](./comment_memo_2026.pdf)) | Internal forwarding memo; not filed | Whoever forwards it |
| Ask HUD to act, on a clock that does not expire with the comment window (organization) | [`553e_petition_template.md`](./553e_petition_template.md) | Petition for rulemaking, 5 U.S.C. 553(e); no dedicated HUD portal (certified mail primary) | Counsel with administrative-law experience |
| Same, filed by an individual with a disability | [`553e_petition_individual.md`](./553e_petition_individual.md) | Petition for rulemaking, 5 U.S.C. 553(e); "interested person" standard | Counsel with administrative-law or disability-rights experience |
| Adapt any of the above | [`ADAPTATION_CHECKLIST.md`](./ADAPTATION_CHECKLIST.md) | Procedure, not a filing | Everyone using this kit |

**No litigation template is provided.** Any complaint would need to respond to an actual
agency disposition, an identified plaintiff, the governing venue, and the resulting
administrative record — none of which presently exists. Judicial-review materials, if the
contingency ever arises, must be developed by counsel from the actual agency disposition;
the Note's Part IV and [`../article/appendices/Appendix_D_Standing_Reviewability_Annex.md`](../article/appendices/Appendix_D_Standing_Reviewability_Annex.md)
state the governing framework.

## How the pieces fit together

The pieces are sequenced, and each does distinct work. The **2026 public comment**
builds the renewal record now: HUD's 60-day notice proposing to renew Form HUD-27061
unchanged published June 12, 2026 (91 Fed. Reg. 35,697), and **comments are due Tuesday,
August 11, 2026**. Under 44 U.S.C. 3506(c)(2)(A), HUD must evaluate the comments it
receives, and everything filed becomes part of the public record that any later reviewer
-- agency or court -- can read. The **section 553(e) petition** is the durable vehicle,
and it does not expire with the comment window: filing it triggers HUD's duty under
5 U.S.C. 555(b) to conclude the matter within a reasonable time and, under 555(e), to
give a statement of grounds for any denial, and a denial of a rulemaking petition is
judicially reviewable under *Massachusetts v. EPA*, 549 U.S. 497, 527-28 (2007). The
organizational and individual variants are complementary; the individual variant explains
why section 553(e)'s "interested person" standard is broader than Article III standing and
is therefore the lower-risk vehicle for an individual. Judicial review is the contingent layer,
not the plan, and no complaint or plaintiff-selection material is published here: those
turn on an actual agency disposition and an actual filer, and belong to counsel. The
governing framework -- including who can bring an eventual review case after *FDA v.
Alliance for Hippocratic Medicine*, 602 U.S. 367 (2024) -- is the Note's Part IV and
[`../article/appendices/Appendix_D_Standing_Reviewability_Annex.md`](../article/appendices/Appendix_D_Standing_Reviewability_Annex.md).

None of these templates has been filed. The author's own comment in the 2026 docket --
filed July 6, 2026 in his individual capacity and posted July 7, 2026 as Comment No.
HUD-2006-0214-0011 -- is archived separately at
[`../article/appendices/admin_record_c/pra_comment_2026/`](../article/appendices/admin_record_c/pra_comment_2026/)
and serves as a worked example.

## Supporting files

| File | What it is |
|---|---|
| `comment_memo_2026.pdf` | One-page forwarding memo, generated from `comment_memo_2026.md`. |
| [`build_comment_memo_pdf.py`](./build_comment_memo_pdf.py) | Builds `comment_memo_2026.pdf`. |
| `figures/` | Timeline figures for the 2022-2023-2026 Form HUD-27061 sequence, in light and dark variants. |

The Markdown sources are authoritative. The Word and PDF builds are generated from them
by the scripts above; run the builders after editing a source.

## Where to go next

- [`../article/THE_ARGUMENT.md`](../article/THE_ARGUMENT.md) -- the Note's legal argument, compressed for lawyers who have not read it.
- [`../TAKE_ACTION.md`](../TAKE_ACTION.md) -- the time-ordered version of this kit: what to do now, next, and only if HUD denies.
- [`../article/appendices/admin_record_c/pra_comment_2026/`](../article/appendices/admin_record_c/pra_comment_2026/) -- the author's 2026 comment as filed and posted (Comment No. HUD-2006-0214-0011), with a crosswalk to the Note.
- [`../article/appendices/Appendix_C_HUD_Administrative_Record.md`](../article/appendices/Appendix_C_HUD_Administrative_Record.md) -- the HUD-27061 / Part 121 administrative record, including the petition's twelve-exhibit evidentiary map (section C.5).
- [`../article/appendices/Appendix_D_Standing_Reviewability_Annex.md`](../article/appendices/Appendix_D_Standing_Reviewability_Annex.md) -- extended standing and reviewability analysis.
- [`../record/hud-27061/CHRONOLOGY.md`](../record/hud-27061/CHRONOLOGY.md) and [`../record/hud-27061/RECORD_METHOD.md`](../record/hud-27061/RECORD_METHOD.md) -- the dated administrative-record chronology and the record-assembly method behind the templates.
