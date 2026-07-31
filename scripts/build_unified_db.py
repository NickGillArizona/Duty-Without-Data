"""
Build the unified single-source-of-truth FHA case classification database.

This is the Layer 1 production script that produced data/FHA_Unified_Database.json.
It reads the resolved DB (with per-model suffixed fields + canonical fields produced
by the three-base-classifier pipeline: MiniMax M2.7 + DeepSeek V3.2 + Kimi K2.5,
with Haiku 4.5 / Sonnet 4.6 tiered consensus adjudication; see
method/pipeline/model_configuration.md and method/pipeline/model_metadata.json) and produces:

1. A clean unified DB with ONLY canonical fields — the single source of truth
   used by the analysis scripts in this directory.
2. An audit DB preserving the per-model fields (suffixed `_minmax`, `_deepseek`,
   `_kimi`) alongside canonical values for downstream validation work.

Also patches any remaining gaps in canonical fields by falling back to whichever
base classifier provided a value.

Path resolution: paths are resolved through `scripts/config.py` (FHA_DATA_DIR,
FHA_RESULTS_DIR). The input resolved DB is not baked in; set the environment
variable `FHA_RESOLVED_DB_PATH` to point INPUT_PATH at a local copy of the
resolved DB. The default OUTPUT_DIR is the repo's `data/` directory.
"""

import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path

# Resolve paths through scripts/config.py if available; otherwise fall back to
# repo-relative defaults rooted at this file's parent's parent (i.e., the
# repository root).
SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[1]
DATA_DIR = Path(os.environ.get('FHA_DATA_DIR', REPO_ROOT / 'data'))

# The resolved DB is produced by the upstream three-model classification pipeline
# (Java implementation: see consensus_resolution.md in method/pipeline/). It is not
# committed to this repository because of size; readers can either point this
# script at a local copy via FHA_RESOLVED_DB_PATH or skip directly to the
# already-built data/FHA_Unified_Database.json.
_RESOLVED_DB_ENV = os.environ.get('FHA_RESOLVED_DB_PATH')
INPUT_PATH = Path(_RESOLVED_DB_ENV) if _RESOLVED_DB_ENV else None
OUTPUT_DIR = Path(os.environ.get('FHA_BUILD_OUTPUT_DIR', DATA_DIR))

SUFFIXES = ['_minmax', '_deepseek', '_kimi']

# Identity fields (always present, never suffixed)
IDENTITY_FIELDS = ['source_file', 'screening_result', 'case_name', 'citation']

# Canonical categorical fields
CATEGORICAL_FIELDS = [
    'court', 'year', 'procedural_posture', 'fha_section_cited',
    'accommodation_type', 'secondary_accommodation_type',
    'plaintiff_type', 'defendant_type', 'disability_category',
    'outcome', 'primary_claim_type', 'claim_types',
    'loper_bright_cited', 'race_mentioned', 'dual_basis_claim',
    'race_if_mentioned', 'interactive_process_discussed',
    'delay_as_denial', 'property_city', 'property_state',
    'housing_type', 'subsidy_program', 'primary_protected_class',
    'protected_classes',
]

# Free-text canonical fields
FREE_TEXT_FIELDS = [
    'accommodation_description', 'key_holding', 'brief_summary', 'key_cases_cited',
]

ALL_CANONICAL_FIELDS = CATEGORICAL_FIELDS + FREE_TEXT_FIELDS

# Resolution metadata fields to preserve
META_FIELDS = ['_resolution_method', '_adjudicated_fields', '_adjudication_reasoning']


def main():
    if INPUT_PATH is None or not INPUT_PATH.exists():
        raise SystemExit(
            f"Resolved DB not found (FHA_RESOLVED_DB_PATH={INPUT_PATH}). "
            f"Either set FHA_RESOLVED_DB_PATH to point at a local copy, or use "
            f"the already-built data/FHA_Unified_Database.json directly. "
            f"This script is preserved for documentation of the Layer 1 pipeline; "
            f"the upstream classification orchestrator (Java) is published at "
            f"method/pipeline/java/mfh/gfo/ in this repository."
        )

    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f'Loaded: {len(data)} records')

    unified = []
    audit = []
    patched_count = 0
    field_patch_counts = Counter()

    for rec in data:
        is_fha = rec.get('screening_result', '').upper() != 'NO'

        # ----- Build unified (clean) record -----
        clean = {}
        for field in IDENTITY_FIELDS:
            if field in rec:
                clean[field] = rec[field]

        if is_fha:
            # Copy canonical fields, patching gaps from model outputs
            for field in ALL_CANONICAL_FIELDS:
                val = rec.get(field)

                # Patch: if canonical is missing, try model suffixes
                if val is None or val == '' or (isinstance(val, str) and val.strip() == ''):
                    for suffix in SUFFIXES:
                        fallback = rec.get(field + suffix)
                        if fallback is not None and fallback != '':
                            val = fallback
                            field_patch_counts[field] += 1
                            patched_count += 1
                            break

                if val is not None:
                    clean[field] = val

            # Resolution metadata
            clean['_resolution_method'] = rec.get('_resolution_method', 'unknown')
            adjudicated = rec.get('_adjudicated_fields')
            if adjudicated:
                clean['_adjudicated_fields'] = adjudicated

        unified.append(clean)

        # ----- Build audit record (everything) -----
        audit.append(rec)

    # Stats
    fha_records = [r for r in unified if r.get('screening_result', '').upper() != 'NO']
    print(f'\nFHA-relevant records: {len(fha_records)}')
    print(f'Screened out: {len(unified) - len(fha_records)}')
    print(f'Patched {patched_count} field gaps from model fallbacks')
    if field_patch_counts:
        print('  Patches by field:')
        for f, c in field_patch_counts.most_common():
            print(f'    {f}: {c}')

    # Field coverage
    print(f'\nCanonical field coverage (FHA records):')
    for field in ALL_CANONICAL_FIELDS:
        has = sum(1 for r in fha_records if r.get(field) is not None and r.get(field) != '')
        pct = 100 * has / len(fha_records) if fha_records else 0
        marker = '' if pct == 100.0 else f'  <-- {len(fha_records) - has} missing'
        print(f'  {field:40s} {has:>5}/{len(fha_records)} ({pct:5.1f}%){marker}')

    # Resolution method breakdown
    print(f'\nResolution methods:')
    methods = Counter(r.get('_resolution_method', 'none') for r in fha_records)
    for m, c in methods.most_common():
        print(f'  {m:35s} {c:>5} ({100*c/len(fha_records):.1f}%)')

    # Field count comparison
    unified_fields = sum(len(r.keys()) for r in unified) / len(unified)
    audit_fields = sum(len(r.keys()) for r in audit) / len(audit)
    print(f'\nAvg fields per record:')
    print(f'  Unified (clean): {unified_fields:.0f}')
    print(f'  Audit (full):    {audit_fields:.0f}')
    print(f'  Reduction:       {audit_fields - unified_fields:.0f} fields removed per record')

    # Write unified DB
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    unified_path = OUTPUT_DIR / f'FHA_RA_Database_unified_{ts}.json'
    with open(unified_path, 'w', encoding='utf-8') as f:
        json.dump(unified, f, indent=2, ensure_ascii=False)
    print(f'\nUnified DB written: {unified_path}')
    print(f'  Records: {len(unified)} | FHA: {len(fha_records)}')

    # Write audit DB (the full resolved version is already the audit trail)
    audit_path = OUTPUT_DIR / f'FHA_RA_Database_audit_{ts}.json'
    with open(audit_path, 'w', encoding='utf-8') as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
    print(f'Audit DB written: {audit_path}')

    # Also produce a summary stats file for the appendix
    stats = {
        'generated': ts,
        'source_file': INPUT_PATH.name,
        'total_records': len(data),
        'fha_relevant': len(fha_records),
        'screened_out': len(data) - len(fha_records),
        'patched_fields': patched_count,
        'resolution_methods': {m: c for m, c in methods.most_common()},
        'field_coverage': {},
    }
    for field in ALL_CANONICAL_FIELDS:
        has = sum(1 for r in fha_records if r.get(field) is not None and r.get(field) != '')
        stats['field_coverage'][field] = {
            'count': has,
            'total': len(fha_records),
            'pct': round(100 * has / len(fha_records), 1) if fha_records else 0,
        }
    stats_path = OUTPUT_DIR / f'FHA_RA_Database_stats_{ts}.json'
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f'Stats written: {stats_path}')


if __name__ == '__main__':
    main()
