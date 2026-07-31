# Comparator Study (Appendix A-6)

Terminal record of the cross-class comparator study reported in
article/appendices/Appendix_A6_Comparator_Analysis.md and cited by the manuscript at
footnotes 87, 89, and 90.

**Start with [`METHODS_LIMITATIONS_AND_QA.md`](METHODS_LIMITATIONS_AND_QA.md)** — the
consolidated methods, limitations, and QA register — and
[`provenance/VERIFICATION_CLOSURE.md`](provenance/VERIFICATION_CLOSURE.md), the
verification closure memo.

## The study in one paragraph

Within disability, record-dependent claims (RD-PURE: accommodation, modification, and
design-and-construction) are compared with open-textured disparate-treatment claims
(DT-PURE) and a race disparate-treatment arm (RACE-DT), over the same three periods, on
the same machine-classified corpus. The claim families and predictions were registered
before analytics ([`PREDICTIONS.md`](PREDICTIONS.md), a frozen instrument;
registered outcomes in `REGISTERED_PREDICTION_RESULTS.json`).

## Verified headline result

Institutionally-held-fact (Family-A) pleading deficits among pro se pleading losses:
RD-PURE 13.6% [7.6, 20.3] vs DT-PURE 0.8% [0.0, 2.3] vs RACE-DT 0.6% [0.0, 1.9] —
machine-verified under a pre-registered AI-only protocol; no human coded any row
(closure memo, sections 1-4). The full raw-text recode independently reproduces the
concentration: 12.2% vs 0.0% vs 1.9%.

## Adverse results (part of the record by design)

- DIVERGING P1 pre-trend on the rate series (../../results/supporting/ and app. A-6 sec. A-6.9).
- Race-arm retrieval-capture differential, 0.51-0.66
  (recoding_2026-07-07/courtlistener_recall/).
- Measured masking leakage: 61.3% lexicon-level, 70.8% by model class-guess — "masking
  attempted," never "blind."
- The first-pass keyword proxy for rationale coding was superseded by the three-model
  consensus (row-level agreement with the consensus: 38.2%; nothing from the proxy
  carries weight). The as-run first-pass record is preserved in git history and the
  project's private research records.

## Evidence map

- Frozen instruments: `PREDICTIONS.md`, `RATIONALE_RUBRIC.md`, and the registered
  prompts under `recoding_2026-07-07/`, hash-pinned in
  `provenance/verification_stage_manifest.json` and
  `provenance/remediation_hash_manifest.json`.
- Final structured outputs: `RATIONALE_CODED_ROWS_CONSENSUS.csv` (476 rows),
  `FINAL_ROW_DECISIONS.csv` (the 60-row terminal decision table: consensus, verified
  family, verification route), `RATIONALE_SUMMARY_CONSENSUS.csv`, and the raw per-model
  outputs and statistics under `recoding_2026-07-07/consensus_stage/`.
- Verification evidence: `recoding_2026-07-07/raw_text_verification/` (inputs, raw
  panel outputs, `R1_VERIFIED_CODES.csv`, `VERIFICATION_RESULTS.json`,
  `COMPLETENESS_CHECK.json` — 27/27 — and the SHA-256 manifests); independent
  reproduction audit: `recoding_2026-07-07/audit/AUDIT_RECOMPUTE.json`.
- Document-level analytic tables (labeled pipeline output; the reported Part II series
  is the case-level census in `results/series_2026-07.json`): `TABLE1_COMPARATOR.csv`
  and `.md`, `KITAGAWA_DECOMPOSITION.csv`, `MODEL_RESULTS.json`, `MODELS.md`,
  `SAMPLE_TABLE.csv`, `EXCLUSIVE_BASIS_SENSITIVITY.csv`, and the
  `missingness_*.csv` robustness pair.

## Regeneration

```bash
python replication/comparator/comparator_analysis.py
python replication/comparator/regenerate_table1.py
python replication/comparator/recoding_2026-07-07/scripts/compute_consensus.py
```

The consensus computation is byte-deterministic from the committed inputs. The seeded
bootstrap tables reproduce byte-identically anywhere; scipy/statsmodels cells match to
full precision under the locked environment in `requirements-lock.txt`. Fresh model API
reruns are optional deep validation — the frozen structured outputs above are the
primary reproduction evidence.
