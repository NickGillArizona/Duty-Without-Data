# Data Dictionary: HUD Administrative Datasets

This dictionary describes the external HUD administrative datasets used or evaluated by the archive. For each source, it identifies the unit of observation, relevant fields, transformations, access conditions, and known limits. Dated agency-status information must be checked against the cited public record before reuse.

Assurance and field conventions for all three dictionaries are in [`README.md`](README.md).

The repository also includes three HUD administrative datasets used for the institutional-infrastructure analysis in Parts I, III, and IV. Detailed methodology and findings are documented in [Appendix L](../../article/appendices/Appendix_L_HUD_Administrative_Data.md). Analysis scripts are in `scripts/`.

## CDBG National Accomplishment Reports

**File:** `data/CDBG_Accomp_Natl.xlsx` | **Script:** `scripts/cdbg_analysis.py` | **Output:** `results/cdbg_results.json`

CDBG grantee accomplishment data (FY2005–FY2024), reporting persons/households served by activity code. Key fields in output: `disability_analysis_by_year` (yearly 05B/03B beneficiary counts), `summary_statistics` (20-year totals, shares, trends), `activity_categories` (full code inventory).

## Picture of Subsidized Households (POSH)

**Files:** `data/US_2024_2020census.xlsx`, `data/STATE_2024_2020census.xlsx`, `data/dictionary_2024.pdf` | **Script:** `scripts/posh_analysis.py` | **Output:** `results/posh_results.json`

HUD's annual census of ~5.1 million subsidized housing units. Key fields in output: `national_summary` (total units, disability rates, estimated disabled households), `by_program` (program-level breakdowns for HCV, Project-Based Section 8, Public Housing, Section 811, Section 202, Mod Rehab).

## REAC/NSPIRE Physical Inspection Scores

**Files:** `data/public_housing_physical_inspection_scores.xlsx`, `data/multifamily_physical_inspection_scores.xlsx` | **Script:** `scripts/reac_analysis.py` | **Output:** `results/reac_results.json`

HUD REAC inspection scores for 34,649 properties (6,190 public housing, 28,459 multifamily). Key fields in output: `inspection_overview` (property counts, score distributions, failure rates), `nspire_transition_insight` (UPCS vs. NSPIRE failure rate comparison), `accessibility_keyword_search` (verification that no accessibility fields exist in published schema).
