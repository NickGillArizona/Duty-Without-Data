# Data and Artifact Dictionaries

These dictionaries describe three distinct domains: the FHA Unified Database, external HUD administrative datasets, and the artifacts used for mechanism and per-claim classification. Each file defines its own units, fields, provenance, and limits. The dictionaries document the archive; they do not independently establish case facts or legal conclusions.

## Purpose

A reader who opens a committed data file needs four things: what one row is, what each field is permitted to contain, where the values came from, and what the field cannot be used to show. These pages carry that information for the three domains the archive publishes.

## The three domains

| Dictionary | Domain | Unit of observation |
|---|---|---|
| [`fha_unified_database.md`](fha_unified_database.md) | The FHA Unified Database assembled for this project | One federal FHA opinion record |
| [`hud_administrative_datasets.md`](hud_administrative_datasets.md) | External HUD administrative datasets used or evaluated by the archive | Stated per source |
| [`mechanism_coding_artifacts.md`](mechanism_coding_artifacts.md) | Schemas, controlled vocabularies, and artifacts for mechanism and per-claim classification | One coded pleading-loss case row |

## Authority

Each dictionary describes files as committed. Where a field is produced by model-assisted coding, the dictionary says so, and the field is a classification under a fixed question and a fixed set of permitted answers rather than an independent finding of fact. Sample and tier definitions are governed by [`../../replication/SAMPLE_DEFINITIONS.md`](../../replication/SAMPLE_DEFINITIONS.md); pipeline stage definitions are governed by [`../../method/METHODOLOGY.md`](../../method/METHODOLOGY.md). Where a dictionary and one of those governing files disagree, the governing file controls.

## Link map

- Machine-readable schema for the FHA Unified Database: [`../FHA_Unified_Database.schema.json`](../FHA_Unified_Database.schema.json)
- Per-claim extraction schema: [`../../method/pipeline/per_claim_extraction_schema.json`](../../method/pipeline/per_claim_extraction_schema.json)
- Reproduction protocol: [`../../replication/REPRODUCE.md`](../../replication/REPRODUCE.md)
- Provenance record: [`../../replication/DATA_PROVENANCE.md`](../../replication/DATA_PROVENANCE.md)
- Validation record: [`../../method/VALIDATION.md`](../../method/VALIDATION.md)

## Field-definition conventions

Field names appear exactly as they are stored. Types are the observed JSON types. A field described as an enum lists its permitted values in the form the file stores them; a field described as an array may carry more than one value in a single record. Where a field name in the prose differs from a term used in the Note, the dictionary entry states the correspondence.

## Missingness

Records in the FHA Unified Database are heterogeneous by design: screened-out records carry a small subset of keys and fully classified records carry the full schema, so presence is a property of the tier and not of the field alone. Presence and null rates by tier are tabulated in the FHA Unified Database dictionary. A blank cell is not a zero, and a value the archive could not establish is recorded as unavailable rather than as an established negative.

## Maintenance

The generated portion of the FHA Unified Database dictionary and the machine-readable JSON Schema are both produced by `python scripts/make_data_dictionary.py` and must be regenerated after any change to the committed database. The hand-maintained text should be updated in the same commit as any schema change it describes.
