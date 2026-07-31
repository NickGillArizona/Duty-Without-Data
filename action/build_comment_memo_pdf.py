"""Build comment_memo_2026.pdf, the one-page forwarding memo for the Form HUD-27061
comment window (source text: comment_memo_2026.md).

Usage:  python build_comment_memo_pdf.py
Output: comment_memo_2026.pdf (letter size, one page; the script fails loudly if the
        content overflows onto a second page rather than silently shipping two).
"""

import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "comment_memo_2026.pdf")

BODY = [
    (
        "The situation.",
        'In September 2022, HUD proposed updating Form HUD-27061 — its one-page, '
        'cross-program demographic form — “to collect protected class data as required '
        'by the Fair Housing Act and HUD regulations at 24 CFR 121,” authorities whose '
        'categories include disability (“handicap”) and family characteristics. '
        '87 Fed. Reg. 58,524, 58,525. The form approved in 2023 collects race and ethnicity '
        'only; the 30-day notice contains no occurrence of “disability,” '
        '“handicap,” “protected class,” or “Fair Housing Act,” and '
        'the only change HUD’s Supporting Statement explained was a clerical field '
        'relabeling. 88 Fed. Reg. 5,370. On June 12, 2026, HUD proposed renewing the narrowed '
        'form unchanged — while still describing it as collecting “race, ethnicity, '
        'and other protected class data . . . as required by . . . the Fair Housing Act.” '
        '91 Fed. Reg. 35,697, 35,698. The burden estimate — 14,375 respondents, 8,625 '
        'annual hours — is identical across all three notices, which forecloses respondent '
        'burden as the disclosed reason for the narrowing. As of the archived record cutoff '
        'of July 8, 2026, HUD’s June 12, 2026 renewal notice remains pending and OMB has '
        'posted no disposition; the collection’s displayed expiration date of June 30, 2026 '
        'has passed. Check the official docket for anything later.',
    ),
    (
        "Why comment now.",
        'Comments are due August 11, 2026 (regulations.gov Docket No. HUD-2006-0214). HUD must '
        'evaluate the comments it receives, 44 U.S.C. 3506(c)(2)(A), and its submission to OMB '
        'is expected to summarize and respond to substantive issues raised, 5 C.F.R. '
        '1320.5(a)(1)(iv), 1320.8(d). The 2022 window drew exactly one substantive comment '
        '(SAGE, through Jones Day). On a docket this thin, a substantive organizational comment '
        'cannot be lost in a pile — and everything filed by August 11 becomes part of the '
        'administrative record that a planned rulemaking petition under 5 U.S.C. 553(e), and '
        'any court that later reviews HUD’s answer, will read.',
    ),
    (
        "The ask.",
        'File a comment before August 11. A drafted organizational template is published for '
        'adaptation, and counsel can adapt it in an afternoon. Its requests are record-facing '
        'and support a collection HUD itself proposed: address the 2022 proposal and the 2023 '
        'omission on the record; address 42 U.S.C. 3608(e)(6), 24 C.F.R. Part 121, and Section '
        '504 / 24 C.F.R. Part 8; address privacy-preserving design alternatives and the burden '
        'arithmetic. Then add one to three paragraphs only your organization can write — a '
        'matter where the paper trail failed, a data request you could not answer, a program '
        'decision made blind. Even a two-paragraph comment is evaluable.',
    ),
    (
        "What filing does not do.",
        'A PRA comment is routine administrative participation. It is not litigation, joins no '
        'lawsuit, and commits the organization to nothing after August 11. It supports a data '
        'collection HUD itself proposed in 2022 and asks the agency to engage its own '
        'authorities — or explain, on the record, why not.',
    ),
]

MATERIALS = [
    'How-to, record, and both comment tracks: '
    '<link href="https://nickgillarizona.github.io/Duty-Without-Data/comment/">'
    'nickgillarizona.github.io/Duty-Without-Data/comment/</link>',
    'Adaptable template: <link href="https://github.com/NickGillArizona/Duty-Without-Data/'
    'blob/main/action/2026_comment_template.md">github.com/NickGillArizona/Duty-Without-Data'
    '</link> (action/2026_comment_template.md)',
    'Comment form: <link href="https://www.regulations.gov/commenton/HUD-2006-0214-0010">'
    'www.regulations.gov/commenton/HUD-2006-0214-0010</link>',
    'Worked example (the author’s filed comment): '
    '<link href="https://www.regulations.gov/comment/HUD-2006-0214-0011">'
    'www.regulations.gov/comment/HUD-2006-0214-0011</link>',
]

FOOTER = (
    'Prepared by a J.D. candidate, not an attorney, for adaptation by an organization’s own '
    'counsel; drafted with LLM assistance and reviewed by the author; not legal advice. '
    'Questions, corrections, or a fifteen-minute walkthrough: nickgill@arizona.edu.'
)


def build(font_size, leading, space_after):
    styles = {
        "memo_title": ParagraphStyle(
            "memo_title", fontName="Times-Bold", fontSize=13, leading=16, spaceAfter=10,
        ),
        "head": ParagraphStyle(
            "head", fontName="Times-Roman", fontSize=font_size, leading=leading, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", fontName="Times-Roman", fontSize=font_size, leading=leading,
            spaceAfter=space_after, alignment=4,  # justified
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Times-Roman", fontSize=font_size, leading=leading,
            spaceAfter=2, leftIndent=16, bulletIndent=4,
        ),
        "footer": ParagraphStyle(
            "footer", fontName="Times-Italic", fontSize=font_size - 1.5,
            leading=leading - 1.5, textColor="#444444", spaceBefore=6,
        ),
    }

    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.7 * inch, bottomMargin=0.6 * inch,
        title="Comment window on HUD Form HUD-27061 closes August 11, 2026",
        author="Nicholas Gill",
        subject="Form HUD-27061 renewal (OMB Control No. 2535-0113) public-comment memo",
    )

    story = [Paragraph("MEMORANDUM", styles["memo_title"])]
    head = [
        ("TO:", "Housing and disability advocacy organizations and their counsel"),
        ("FROM:", "Nicholas Gill, J.D. candidate, University of Arizona James E. Rogers College "
                  "of Law; author, <i>Duty Without Data: Disability Fair Housing and the "
                  "Record-Dependent Right</i> (Arizona Law Review, forthcoming 2026)"),
        ("DATE:", "July 12, 2026"),
        ("RE:", "<b>Public-comment window on HUD Form HUD-27061 (OMB Control No. 2535-0113) "
                "closes Tuesday, August 11, 2026</b>"),
    ]
    for label, text in head:
        story.append(Paragraph(f"<b>{label}</b>&nbsp;&nbsp;{text}", styles["head"]))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.8, color="#333333", spaceAfter=8))

    for lead, text in BODY:
        story.append(Paragraph(f"<b>{lead}</b> {text}", styles["body"]))

    story.append(Paragraph("<b>Materials (all public).</b>", styles["body"]))
    for item in MATERIALS:
        story.append(Paragraph(item, styles["bullet"], bulletText="–"))
    story.append(Paragraph(FOOTER, styles["footer"]))

    doc.build(story)
    return doc.page


if __name__ == "__main__":
    pages = build(font_size=10, leading=12.6, space_after=7)
    if pages > 1:
        pages = build(font_size=9.5, leading=11.8, space_after=6)
    if pages > 1:
        sys.exit(f"ERROR: memo overflows to {pages} pages even at 9.5pt; trim the source text.")
    print(f"OK: wrote {OUT} ({pages} page)")
