# Comparator Verification Closure - 2026-07-07

## Disposition

The comparator study's rationale-coding is verified by an AI-only verification protocol,
executed 2026-07-07 under a pre-registered plan whose triggers and thresholds were fixed and
hash-registered before any verification call: registered plan SHA256
`c95b02dedb24bb1241c95cfafd6f6eb30c724f5b0d8c9601bd1fa8c188758ba3`; the author's decision
addendum electing machine-only verification SHA256
`50e7edf54a2d0ca30bc99cdce82e5c9a096389e21b6064730823517cd62c2992`. The registration
log carrying both entries is preserved in the project's private research records, and the registered prompt
hashes are pinned publicly in `verification_stage_manifest.json`. No human
hand-coding occurred; machine-only review supports the appendix-level claim. The verification is
a pre-registered machine protocol, not a human coding pass, which did not occur.

Claim status: the Family-A rationale contrast is machine-verified and supports the
appendix-level claim. Body use rests on Variant A (see section 5).

## 1. What replaced the human hand-check

Two independent raw-opinion-text runs, both stronger than the check they replaced:

- RUN R1 (decisive-row blind audit): all 26 consensus Family-A rows, all 6 no-consensus rows,
  all 4 misfilter flags, the 24 B/C review-set rows, and a seeded 36-row B/C control sample - 96 rows
  - were blindly recoded from FULL OPINION TEXT (not the masked summaries) by three strong
  models from three labs (anthropic/claude-sonnet-5, openai/gpt-5.5,
  google/gemini-3.1-pro-preview), each required to return a verbatim evidence quote that was
  programmatically matched against the opinion. Panel-vs-consensus disagreements (28 rows) were
  adjudicated by anthropic/claude-opus-4.8 with its own quote requirement. 288/288 panel reads
  succeeded; 87.2% of quotes verified verbatim; 0 adjudication failures.
- RUN R2 (full-universe robustness): all 476 rows recoded from full opinion text by the
  archive's Layer-2 trio (kimi-k2.6, glm-5.1, deepseek-v3.2), majority vote. 1,427/1,428 reads;
  Fleiss kappa 0.687; row-level agreement with the masked run 86%.

A completeness gate (27 hard checks: input composition, read coverage, schema, quote integrity,
adjudication closure, prompt-hash registration, artifact manifest) passed 27/27 BEFORE any
trigger was evaluated: `recoding_2026-07-07\raw_text_verification\COMPLETENESS_CHECK.json`.

## 2. What the verification found

- The load-bearing category survives with an honest haircut: 19 of 26 consensus Family-A rows
  sustained (73.1%); 6 overturned to B, 1 to UNCLEAR. Verified primary estimate: Family-A among
  pro se pleading losses = RD-PURE 13.6% [7.6, 20.3] (n=118) vs DT-PURE 0.8% [0.0, 2.3] (n=132)
  vs RACE-DT 0.6% [0.0, 1.9] (n=158). The comparators' rates FELL under verification, so the
  separation widened (roughly eighteenfold at the point estimates) while the RD-PURE estimate
  came down from 16.4% to 13.6%.
- The raw-text run independently reproduces the concentration: 12.2% vs 0.0% vs 1.9%. The
  summary-substrate caveat is thereby retired as a threat to the finding (it remains disclosed
  as a design fact of the primary run).
- Category stability: only 1 of 36 B/C control rows flipped into A (2.8%) - the panel is not
  generous with A codes; the asymmetry is in the cases, not the coder.
- Misfilter yield stayed low against full opinions (9 of 476), validating the pleading-loss
  filter a second time.

## 3. Pre-committed triggers (frozen in the registered plan) - outcomes

| Trigger | Threshold | Outcome |
|---|---|---|
| (i) Verified RD-PURE pro se Family-A | >= 8.0% AND CI lower bound above both comparators' CI upper bounds | PASS: 13.6%; 7.63% > 2.27% |
| (ii) Raw-text run ordering | RD-PURE >= 2x max(DT-PURE, RACE-DT) | PASS: 12.2% vs max 1.9% |
| (iii) Control stability | <= 20% of B/C controls flip into A | PASS: 1/36 (2.8%) |
| Inversion guard | RD <= either comparator in either run | NOT TRIGGERED |

RESULT: VARIANT A - the Part II.F body sentence plus expanded footnote 89, with the verified
numbers. Selected mechanically; no post-hoc discretion was exercised.

## 4. Residual limitations (carried into Appendix A-6, not waived)

1. No human coded any row, anywhere in this study. Model-correlated error across all seven
   models used (three masked-run coders, three panel coders, one adjudicator, spanning five
   labs) cannot be excluded by adding more models.
2. The verified RD-PURE estimate rests on 16 verified-A pro se rows out of 118 classifiable;
   the CI [7.6, 20.3] states that thinness honestly.
3. Quote-integrity is high but not total (87.2% / 80.5%); non-matching quotes are flagged in
   the raw artifacts and were retained only where the family code was otherwise valid.
4. The race arm's retrieval-capture differential (0.51-0.66) and the masked run's measured
   leakage (61.3% lexicon / 70.8% class-guess) remain standing disclosures.

## 5. Integration

Variant A - the Part II.F body sentence plus the expanded footnote 89 - carries the verified
numbers into the manuscript (footnotes 87/89/90) and the companion appendix
(article/appendices/Appendix_A6_Comparator_Analysis.md).

## 6. Artifact index (reproducibility)

All under `recoding_2026-07-07\raw_text_verification\`:
inputs (`verification_inputs_r1/r2.json`, `coverage_report.json`), registered prompts (hashes
pinned in `verification_stage_manifest.json`), raw model outputs (7 files, one per model per
run plus adjudication), verified codes
(`R1_VERIFIED_CODES.csv`), statistics and triggers (`VERIFICATION_RESULTS.json`), completeness
gate (`COMPLETENESS_CHECK.json`), and the SHA256 manifest (`VERIFICATION_MANIFEST.json`).
Scripts: `..\scripts\verification_{build_inputs,run_models,compute,completeness_check}.py`.
Every number in this memo recomputes from the canonical database plus these artifacts.


## 7. Selection outcome

Variant A is the selected result: the Part II.F body sentence and the expanded footnote 89
present the verified numbers, and the companion appendix carries the same figures in
article/appendices/Appendix_A6_Comparator_Analysis.md.
