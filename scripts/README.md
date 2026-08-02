# Scripts

What runs what, and which scripts belong to the release gate. The single entry
point for verification is:

```bash
python scripts/run_release_checks.py
```

Deterministic, local, no network, no keys; [`replication/GATES.md`](../replication/GATES.md)
documents every check.

## Families

- **Release-gate checks** — `run_release_checks.py` and everything it invokes:
  the `check_*` scripts, `validate_claims.py`, `denylist_superseded_series.py`,
  `build_case_level_series.py --check`, and `recompute_verification.py`. These
  run on every change and are the basis of the release badge.
- **Generators of committed artifacts** — the `make_*` scripts
  (`make_fig1.py` with the shared SVG primitives in `make_figures.py`,
  `make_claims_index.py`, `make_site_data.py`, `make_social_preview.py`,
  `make_release_manifest.py`, `make_data_dictionary.py`,
  `make_opinion_sources.py`, `make_qap_ledger.py`) and
  `minimize_public_dataset.py`. Every output is committed; regenerating with
  unchanged inputs diffs clean.
- **Analysis recomputation** — `recompute_stats_unified.py`,
  `recompute_all_appendices.py`, the hypothesis scripts (`h1_h2_analysis.py`
  through `h8_analysis.py`), `decomposition.py`, `robustness_bootstrap.py`,
  `robustness_checks.py`, `regression_analysis.py`,
  `regression_analysis_full.py`, the `pums_*` census scripts, the program-data
  scripts (`cdbg_*`, `posh_analysis.py`, `reac_analysis.py`,
  `ahs_2023_accessibility_analysis.py`, `lihtc_accessibility_audit.py`,
  `pums_housing_stock_analysis.py`), `circuit_district_deep_dive.py`,
  `pro_se_mechanism_analysis.py`, `strengthening_analysis.py`,
  `state_complaint_panel.py`, `supplemental_batch.py`, and
  `rationale_dedup_sensitivity.py`. These re-derive the committed `results/`
  artifacts from the committed data;
  [`replication/REPRODUCE.md`](../replication/REPRODUCE.md) maps script to
  output to claim.
- **Network- or key-dependent** — `fetch_opinion_texts.py`,
  `census_pums_replication.py`, `qap_accessibility_2025_2026_scan.py`,
  `unified_overnight_merge.py`, `unified_overnight_openrouter.py`, and the
  orchestration wrapper `run_all.py` where it drives them. Not part of the
  gate; model reruns and corpus reconstruction are documented as
  nondeterministic in [`replication/REPRODUCE.md`](../replication/REPRODUCE.md).
- **Shared modules** — `config.py`, `analysis_filters.py`.
- **Archived one-time fixes** — the leading-underscore scripts are preserved
  for provenance and are not meant to be run again.
