---
layout: default
title: "Methods and Replication"
permalink: /methods-and-replication/
description: "How the Duty Without Data case dataset was built, how it was validated, and how to reproduce every registered number."
---

# Methods and Replication

How the dataset was built and checked, and how to re-derive every registered number yourself.

The dataset behind the Note's Part II did not exist before this project. Court opinions were
retrieved, screened by a frozen prompt, and classified by several separately run AI models from
different providers, with disagreements resolved under prespecified adjudication rules; the
headline finding has its own separate ensemble, audited blind by a different vendor's models. The
models classify — answering fixed questions about each opinion; the author directed the project
and made all legal and interpretive judgments. Validation measures **reproducibility across
independent classifiers, not accuracy** against a human-coded benchmark, and every layer is
published with its instruments.

## The method, documented

- [Methodology](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/method/METHODOLOGY.md)
  — pipeline stages, model roster, prompts, and the publication boundary, with a guide to running
  the method on a different legal question.
- [System map](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/method/SYSTEM_MAP.md)
  — the one-page data-flow map, with a written text equivalent.
- [Validation](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/method/VALIDATION.md)
  — the published validation layers and what each does and does not establish.
- [Frozen prompts](https://github.com/NickGillArizona/Duty-Without-Data/tree/main/method/prompts)
  — the classification instruments as run.

## Reproduce it

One command runs the deterministic release gate — no network access, API keys, or spend — and
re-derives the registered series from the committed record:

    python scripts/run_release_checks.py

- [Reproduction guide](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/REPRODUCE.md)
  — what is deterministic, what needs model access, and the commands for each analysis.
- [The release gate](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/GATES.md)
  — every check, what a green run establishes, and what it deliberately does not.
- [Verify one claim, end to end](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/VERIFY_ONE_CLAIM.md)
  — a complete worked example from printed sentence to generating artifact.
- [Sample and denominator definitions](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/SAMPLE_DEFINITIONS.md)
  — executable predicates for every population the paper counts.

## The boundary

Full case texts are not redistributed; source identifiers and hashes are preserved so each text
can be re-obtained. End-to-end corpus reconstruction requires upstream working files retained
privately; the frozen canonical record published in the repository is the replication baseline.
The [evidence and limits page](https://nickgillarizona.github.io/Duty-Without-Data/evidence-and-limits/)
states what remains judgment rather than mechanics.
