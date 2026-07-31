# Three-Layer Claim-Specificity Comparison (2026-07-16)

**Assurance: RESEARCH LEAD.** Deterministic comparison; no model coding.

Three-layer claim_specificity comparison.
Generated: 2026-07-16T09:45:23Z.

## Inputs

Layer inputs are held outside this repository; the comparison below is reproduced from the
committed CSVs in this directory.

- Layer 1 recorded key : secondary-field audit key (col db_claim_specificity)
- Layer 2 re-read      : secondary-field audit recodes (col my_claim_specificity)
- Layer 3 third read   : independent specificity re-read (col my_claim_specificity)
- Join column          : record ordinal

## Disagreement universe (recomputed from Layer 1 vs Layer 2)

- Joined rows                : 408
- Determinate (both coded)   : 407
- Baseline agreement (key=SOL1): 271/407 = 66.6%
- Indeterminate (one blank)  : 1
- Disagreement rows          : 136
    - CODE_VS_CODE           : 82
    - SOL1_UNCLEAR           : 54
- Cross-check vs expected 271/407/136: OK

## Third-read coverage

- Present in third read      : 136/136 (100.0%)
- Absent                     : 0
- Absent & persistent no-text: 0
- Absent & not-yet-coded     : 0
- Tolerance rule (final mode): pass when present == 136, OR every absent ordinal is a persistent no-text opinion (SOL-1 text_status in ['UNRESOLVED_TEXT']), i.e. present == 136.

## Adjudication counts -- overall

| adjudication | n |
|---|---|
| KEY_CORROBORATED | 33 |
| SOL1_CORROBORATED | 42 |
| NEITHER | 24 |
| THIRD_UNCLEAR | 36 |
| NO_TEXT | 1 |
| TOTAL | 136 |

## Adjudication counts -- by disagreement_type

### CODE_VS_CODE (n=82)

| adjudication | n |
|---|---|
| KEY_CORROBORATED | 29 |
| SOL1_CORROBORATED | 42 |
| NEITHER | 3 |
| THIRD_UNCLEAR | 7 |
| NO_TEXT | 1 |

### SOL1_UNCLEAR (n=54)

| adjudication | n |
|---|---|
| KEY_CORROBORATED | 4 |
| NEITHER | 21 |
| THIRD_UNCLEAR | 29 |

## Adjudication counts -- by specificity class (recorded key code)

| key_code | KEY_CORR | SOL1_CORR | NEITHER | THIRD_UNCLEAR | NO_TEXT | NOT_YET | total |
|---|---|---|---|---|---|---|---|
| MISSING | 0 | 0 | 13 | 4 | 0 | 0 | 17 |
| MIXED | 0 | 34 | 3 | 4 | 0 | 0 | 41 |
| OPEN_TEXTURED | 0 | 8 | 8 | 23 | 0 | 0 | 39 |
| SPECIFIC_DUTY | 33 | 0 | 0 | 5 | 1 | 0 | 39 |

## Third-read observability distribution (coded rows only)

| observability | n |
|---|---|
| BORDERLINE | 10 |
| CLEAR | 90 |
| NOT_OBSERVABLE | 35 |

## Two-branch adjudicated field agreement

Majority vote = 2 of 3 layers (recorded key, SOL-1, third read). A disagreement row is scored KEY_CORROBORATED when the independent third read matches the recorded key (key + third = majority), which *confirms* the recorded key value for that row. SOL1_CORROBORATED overturns the key. NEITHER / THIRD_UNCLEAR / NO_TEXT leave the row unresolved.

### (a) Full universe -- recorded-key agreement under majority-vote adjudication

Start from the baseline recorded-key vs SOL-1 agreement, then add the disagreement rows the third read resolves in the key's favor:

- Baseline agreement                : 271 / 407 = 66.6%
- + KEY_CORROBORATED (all types)    : + 33
- Adjudicated key-agreement (num)   : 271 + 33 = 304
- Over full determinate universe    : 304 / 407 = 74.7%
  (unresolved rows -- SOL1_CORROBORATED=42, NEITHER=24, THIRD_UNCLEAR=36, NO_TEXT=1 -- counted as non-agreement)
- Resolved-rows-only rate           : 304 / 346 = 87.9%
  (denominator = agreements + KEY_CORROBORATED + SOL1_CORROBORATED)

### (b) Code-vs-code disputes only (SOL1_UNCLEAR rows excluded)

- Baseline agreement (excl. SOL1_UNCLEAR): 271 / 353 = 76.8%
- + KEY_CORROBORATED (code-vs-code)  : + 29
- Adjudicated key-agreement (num)   : 271 + 29 = 300
- Over code-vs-code universe        : 300 / 353 = 85.0%
- Resolved-rows-only rate           : 300 / 342 = 87.7%
  (SOL1_CORROBORATED code-vs-code = 42, NEITHER=3, THIRD_UNCLEAR=7)

---

G2 (keep / caveat / cut) is an AUTHOR decision; this memo is evidence only.
