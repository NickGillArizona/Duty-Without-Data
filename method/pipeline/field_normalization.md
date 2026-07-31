# Field Normalization

Free-text fields were normalized to controlled vocabulary using a mapping pipeline.

## Normalization Rules

| Raw Value | Canonical Value |
|-----------|----------------|
| "African American" | "Black" |
| "African-American" | "Black" |
| "Section 8" | "SECTION_8_HCV" |
| "Housing Choice Voucher" | "SECTION_8_HCV" |
| "HCV" | "SECTION_8_HCV" |

## Normalized Fields

- `race_if_mentioned` — normalized racial/ethnic identifiers
- `subsidy_program` — normalized housing subsidy program names
- `defendant_type` — normalized institutional categories
- `disability_category` — normalized disability type labels

## Implementation

The normalization rules this document describes are the authoritative specification. The harvest and
classification Java layer is retained in the project's private research records; this
specification, not the code, governs.
