# `method/` — Index

The governing method layer. One page per role; evidence lives with the modules it
documents.

## Governing layer

| Page | Role |
|---|---|
| [`METHODOLOGY.md`](METHODOLOGY.md) | Technical companion: pipeline stages, model roster, prompts, and the publication boundary for model outputs |
| [`SYSTEM_MAP.md`](SYSTEM_MAP.md) | One-page map of the data flow, the twenty-check release gate, and what is and is not published at each stage |
| [`METHOD_SPECIFICATION.md`](METHOD_SPECIFICATION.md) | The method specification: the model-assisted classification workflow and its limits |

## Validation records — one record per validated program

| Page | Program | Backs |
|---|---|---|
| [`VALIDATION.md`](VALIDATION.md) | Core database validation: the five-layer record for the primary classification pipeline and the mechanism-family coding (primary ensemble, blind fourth-coder re-read, resolver sensitivity, sample replay, independent pipeline audit) | fns 1, 68, 87 |
| [`comparator_validation.md`](comparator_validation.md) | Terminal summary of the comparator rationale-coding verification (pre-registered AI-only protocol) | fn 89 / app. A-6 |
| [`selection_and_pretrend.md`](selection_and_pretrend.md) | Terminal summary of the counsel-selection audit and the adverse P1 pre-trend check | fn 90 / app. A-6.9 |

Subdirectories: [`prompts/`](prompts/) (frozen classification instruments, indexed by
[`prompts/MANIFEST.md`](prompts/MANIFEST.md)),
[`pipeline/`](pipeline/) (pipeline configuration and schemas),
`validation_three_model/`, `validation_kimi_k2_6/`, `validation_four_coder_full/`
(validation-layer inputs, raw outputs, and reports — the raw per-model outputs of the
headline validation ensemble are published here).
