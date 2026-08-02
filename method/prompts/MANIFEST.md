# Prompt Manifest

The classification instruments in this directory, as run. Each file is frozen: its wording
is fixed by the runs it governed, and rewording one would falsify the as-run record. Model
attribution below states what the instrument itself records; where an instrument does not
name its models, the model roster in [`../METHODOLOGY.md`](../METHODOLOGY.md) is the
authoritative source. None of these instruments is superseded; all four are the current
as-run versions.

| File | Task | Model(s) | Dated/version marker | Status |
|---|---|---|---|---|
| `fha_screening_prompt.txt` | Stage-1 binary FHA relevance screening of the retrieved corpus | Google Gemini 3.1 Flash Lite, temperature 0.0 (stated in the instrument) | Stage header in the instrument | As run; frozen |
| `case_classification_prompt.txt` | 30-key structured classification of FHA reasonable-accommodation opinions | Primary-pipeline roster per `../METHODOLOGY.md` (three independently run base models with tiered adjudication) | None in-file; frozen as committed | As run; frozen |
| `per_claim_extraction_system_prompt.txt` | System instrument for per-claim structured extraction from opinions | Not named in-file; see `../METHODOLOGY.md` | None in-file; frozen as committed | As run; frozen |
| `per_claim_extraction_user_template.txt` | Per-opinion user template paired with the system instrument above | Not named in-file; see `../METHODOLOGY.md` | None in-file; frozen as committed | As run; frozen |

The preregistered headline-mechanism instrument is separate and lives in
[`../preregistration/`](../preregistration/README.md) (wrapped verbatim, hash-logged in
`HASH_MANIFEST.json`). File integrity for everything here is covered by the release
manifest (`RELEASE_MANIFEST.json`, gate check 5).
