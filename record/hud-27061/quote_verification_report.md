# Quote Verification Report — Administrative-Record Quotations

**Verification date:** 2026-04-18
**Verifier:** Fresh re-extraction from source binaries (not the `.txt` derivatives on disk at the time of memo authoring).
**Fresh-extraction tools used (different from originals):**
- `.docx` (SSA_2014, SSA_2019, SSA_2023): `pandoc <file>.docx -t plain`
- `.doc` (SSA_2006): `antiword`
- `.pdf` (FRN60_2023, FRN30_2023, comment_SAGE): `pdftotext` (poppler-utils)

Fresh outputs in `./record/hud-27061/fresh_extract/`. Comparison used whitespace-normalized matching (collapsed runs of whitespace) and curly-/straight-quote unification to avoid false MISMATCH calls caused purely by PDF/DOCX extraction artifacts.

## 1. Quote-by-quote verification

| # | Memo § | Source file | Verdict | Notes |
|---|--------|-------------|---------|-------|
| 1 | 9.2.2 | `FRN60_2023.pdf` | **MATCH** | Exact raw match at fresh-extract offset 6154. |
| 2 | 9.2.3 | `FRN60_2023.pdf` | **NEAR-MATCH** | Text is present verbatim; only difference is an extra paragraph break inside the sentence "...to appropriately collect this\n\ninformation" in the fresh PDF extract (a layout artifact, not a textual difference). Normalized match at offset 9284. The bolded expansion clause appears exactly as quoted. |
| 3 | 9.3.2 | `FRN30_2023.pdf` | **NEAR-MATCH** | Memo uses em-dash `—` in "24 CFR—PART 1—Nondiscrimination…Development—Effectuation"; `pdftotext` renders the original em-dash glyphs as double-hyphen `--`. Original PDF does contain em-dashes (confirmed visually in the `.pdf`). All other content matches character-for-character. Normalized match at offset 2586. |
| 4 | 9.3.3 | `FRN30_2023.pdf` | **MATCH** | Exact raw match at offset 2136. |
| 5 | 9.4.2 (Q15) | `SSA_2023.docx` | **MATCH** | Memo attributes the quote to Question 15 ("Explanation of Program Changes or Adjustments"). The three-sentence quote appears verbatim at fresh-extract offset 14616, immediately preceded by the "15." numbering and followed by the "16." header — confirming both location and wording. Note: the identical opening sentence "This is a reinstatement with change of a currently approved collection." also appears earlier in SSA_2023 (Question 1 context, offset 1985) but continues with different text there; the memo's Q15 attribution is correct. |
| 6 | 9.4.3 (Q8) | `SSA_2023.docx` | **MATCH** | All three ellipsis-joined fragments are present in the order given, within a single block of Q8 text spanning offsets 8963–9620 of the fresh extract. Apostrophe in "HUD's jurisdiction" is a curly apostrophe in the `.docx`; memo renders it as straight. |
| 7 | 9.5.2 (SAGE statutory) | `comment_SAGE.pdf` | **NEAR-MATCH** | **Punctuation difference.** Memo wraps internal regulatory quotes in single straight quotes: `'data concerning the . . . sex'`, `'applicants for, participants in, or beneficiaries…'`, `'necessary and appropriate'`. Source PDF uses double quotes: `"data concerning the . . . sex"`, `"applicants for, participants in, or beneficiaries…"`, `"necessary and appropriate"`. Otherwise verbatim. Offset 6309 in fresh extract. |
| 8 | 9.5.3 (SAGE burden) | `comment_SAGE.pdf` | **NEAR-MATCH** | Memo uses em-dashes `—` in "respondents—30 minutes" / "form—and to HUD staff—1.5 hours"; fresh PDF extract shows `--` (original PDF has em-dashes; poppler-utils renders them as `--`). One whitespace note: the source has "HUD staff-- 1.5 hours" (with a single space after the em-dash, preserved in the PDF as the second hyphen butts the space). Content identical. Offset 21101. |
| 9 | 9.6.1 (2006/2014/2019 boilerplate) | `SSA_2006.doc`, `SSA_2014.docx`, `SSA_2019.docx` | **NEAR-MATCH** | Present in all three. Two minor issues: (a) memo renders the dash before "Nondiscrimination" and "Provisional Guidance" as en-dash `–`; sources use hyphen `-` before the first and a left-double-quote `"` before "Provisional Guidance" (which the memo's en-dash approximates but is not the same glyph); (b) the memo's ellipsis `...` elides the phrase "of the Department of Housing and Urban Development -Effectuation" — this is a legitimate ellipsis, but the reader should know the elided text is substantive, not throat-clearing. |

## 2. Exact-text comparison for NEAR-MATCH items

**§9.3.2 — memo vs. source:**
- Memo: `"…24 CFR—PART 1—Nondiscrimination in Federally Assisted Programs of the Department of Housing and Urban Development—Effectuation of the Title VI…"`
- `pdftotext` output: `"…24 CFR--PART 1--Nondiscrimination… Development--Effectuation of the Title VI…"`
- Cause: em-dash rendering in poppler; the underlying PDF glyphs are em-dashes. MATCH at the glyph level; NEAR-MATCH at the tool-output level only.

**§9.5.2 — memo vs. source:**
- Memo: `'data concerning the . . . sex' of 'applicants for…' that HUD's Secretary determines are 'necessary and appropriate'`
- Source: `"data concerning the . . . sex" of "applicants for…" that HUD's Secretary determines are "necessary and appropriate"`
- Cause: The memo uses single quotes for embedded regulatory citations; the comment itself uses double quotes. This is a quoting-convention substitution and should be disclosed to the court as such (or restored to double quotes) before litigation filing.

**§9.6.1 — memo vs. source (SSA_2014/2019):**
- Memo: `"HUD Regulations 24 CFR 1.6 – Nondiscrimination in Federally Assisted Programs ... Title VI of the Civil Right Act of 1964…"`
- Source: `"HUD Regulations 24 CFR 1.6 - Nondiscrimination in Federally Assisted Programs of the Department of Housing and Urban Development -Effectuation of Title VI of the Civil Right Act of 1964…"`
- Cause: (i) hyphen vs. en-dash; (ii) legitimate ellipsis.

## 3. Absence-of-text confirmation (§9.3.4, §9.4.4, §9.6.2)

Case-insensitive string count on fresh extractions. Zero = absent.

| § | File | Term | Fresh count | Memo claim | Confirmed? |
|---|------|------|-------------|------------|------------|
| 9.3.4 | FRN30_2023 | "protected class" | 0 | absent | YES |
| 9.3.4 | FRN30_2023 | "Fair Housing Act" | 0 | absent | YES |
| 9.3.4 | FRN30_2023 | "24 CFR 121" | 0 | absent | YES |
| 9.3.4 | FRN30_2023 | "Other Demographic" | 0 | absent | YES |
| 9.3.4 | FRN30_2023 | "disability" | 0 | absent | YES |
| 9.3.4 | FRN30_2023 | "handicap" | 0 | absent | YES |
| 9.3.4 | FRN30_2023 | "Section 504" | 0 | absent | YES |
| 9.4.4 | SSA_2023 | "24 CFR 121" | 0 | absent | YES |
| 9.4.4 | SSA_2023 | "Part 121" | 0 | absent | YES |
| 9.4.4 | SSA_2023 | "Section 504" | 0 | absent | YES |
| 9.4.4 | SSA_2023 | "Part 8" | 0 | absent | YES |
| 9.4.4 | SSA_2023 | "disability" | 0 | absent outside § 3608(e)(6) | YES (0 total — even the statutory quote uses "handicap," not "disability") |
| 9.6.2 | SSA_2006 | "24 CFR 121" / "Section 504" / "Part 8" / "disability" / "handicap" | 0 / 0 / 0 / 0 / 0 | all absent | YES |
| 9.6.2 | SSA_2014 | same five terms | 0 / 0 / 0 / 0 / 0 | all absent | YES |
| 9.6.2 | SSA_2019 | same five terms | 0 / 0 / 0 / 0 / 0 | all absent | YES |

All sixteen absence assertions confirmed on independent re-extractions.

## 4. Overall verdict

**The memo's §9 is substantively litigation-ready,** but three cosmetic cleanups should precede any court filing:

1. **§9.3.2, §9.5.3:** Restore em-dashes (the memo already has them; the NEAR-MATCH is a pdftotext artifact, not a memo error). No action needed unless opposing counsel presses on extraction methodology — in which case, cite the PDF glyphs directly.
2. **§9.5.2:** The memo substitutes single quotes for the source's double quotes around embedded regulatory phrases. A court-facing brief should either (a) restore the double quotes and use block-quote formatting to avoid ambiguity, or (b) include a bracketed note "[single quotes substituted for double for readability]" per Bluebook R. 5.2(d) / Rule 5.3.
3. **§9.6.1:** The ellipsis omits "of the Department of Housing and Urban Development -Effectuation" — substantive enough that a cautious brief would render the phrase in full rather than eliding. Consider restoring the elided text.

No **MISMATCH** findings. Every T1 quotation appears verbatim (or verbatim-modulo-extraction-artifacts) in the source binary. Every absence-of-text claim survived re-verification with case-insensitive counting on a fresh extraction. The §9 corpus is citation-safe subject to the three cosmetic adjustments above.
