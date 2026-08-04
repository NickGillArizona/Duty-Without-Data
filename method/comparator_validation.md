# Comparator Verification (fn 89) — Terminal Summary

This page summarizes how the comparator study's rationale coding was verified. The
closure memo of record is
[`../replication/comparator/provenance/VERIFICATION_CLOSURE.md`](../replication/comparator/provenance/VERIFICATION_CLOSURE.md);
the consolidated QA register is
[`../replication/comparator/METHODS_LIMITATIONS_AND_QA.md`](../replication/comparator/METHODS_LIMITATIONS_AND_QA.md).
For the pro se mechanism coding behind fn 87, see [`VALIDATION.md`](VALIDATION.md) — a
separate validation program.

## Underlying rationale coding (app. A-6)

The codes under verification came from a reuse of the Layer-2 ensemble architecture of
the core validation record ([`VALIDATION.md`](VALIDATION.md) § 3) — Kimi K2.6 + GLM-5.1 +
DeepSeek V3.2, majority vote, raw outputs preserved — run on class-masked
dismissal-rationale passages: Fleiss kappa 0.729 (n = 475), with a MiniMax M2.7
stratified re-read at kappa 0.608 (n = 143). Masking leakage was measured and reported,
not assumed (61.3% lexicon-level; 70.8% model class-guess; 96.6% in the record-dependent
arm).

## Protocol (pre-registered, AI-only, no human recode)

Triggers and thresholds were fixed and hash-registered before any verification call.
Two independent full-opinion-text runs replaced the originally planned human check:

- **R1 — decisive-row blind audit.** 96 rows (all 26 consensus Family-A rows, all
  no-consensus and misfilter rows, the B/C review-set rows, and a seeded 36-row B/C control)
  blindly recoded from full opinion text by three models from three labs (Claude
  Sonnet 5, GPT-5.5, Gemini 3.1 Pro), each required to return a verbatim evidence quote
  that was programmatically matched; panel disagreements adjudicated by a fourth model
  (Claude Opus 4.8) with the same quote requirement.
- **R2 — full-universe robustness.** All 476 rows recoded from full opinion text by an
  independent three-model trio, majority vote.

A 27-check completeness gate passed before any trigger was evaluated.

## Results

- 19 of 26 consensus Family-A rows sustained; the verified primary estimate is
  RD-PURE 13.6% [7.6, 20.3] vs DT-PURE 0.8% [0.0, 2.3] vs RACE-DT 0.6% [0.0, 1.9]
  (the RD-PURE estimate came down from 16.4% to 13.6% under verification, and the
  separation widened because the comparators' rates fell further).
- The raw-text run independently reproduces the concentration: 12.2% / 0.0% / 1.9%
  (Fleiss kappa 0.687 across the trio; cross-substrate row agreement 86%).
- Control stability: 1 of 36 B/C control rows flipped into A (2.8%).
- All three pre-committed triggers passed; the inversion guard did not fire.

## Standing limitations (never waived)

1. No human coded any row; model-correlated error across the seven models used cannot
   be excluded by adding more models.
2. The verified RD-PURE cell is thin (16 verified-A pro se rows of 118 classifiable);
   the interval states that honestly.
3. Quote-verbatim match rates are high but not total (87.2% / 80.5%).
4. The race arm's retrieval-capture differential (0.51-0.66) and the masked run's
   measured leakage (61.3% lexicon / 70.8% class-guess) remain standing disclosures.

## Evidence

Terminal decision table: [`../replication/comparator/FINAL_ROW_DECISIONS.csv`](../replication/comparator/FINAL_ROW_DECISIONS.csv).
Verified codes, raw panel outputs, statistics, completeness gate, and manifests:
`../replication/comparator/recoding_2026-07-07/raw_text_verification/`. The manuscript prints the
directional contrast at fn 89; the levels are appendix-tier (app. A-6).
