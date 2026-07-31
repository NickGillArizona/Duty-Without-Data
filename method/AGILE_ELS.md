# Agile Empirical Legal Studies

Agile Empirical Legal Studies (Agile ELS), developed and documented by Nicholas
Gill, is a workflow for classifying legal corpora with independently run language
models under controlled vocabularies, defined adjudication rules, reported agreement
measures, published instruments, and claim-level release checks. This archive is its
worked implementation: 3,366 federal fair-housing litigation records screened to
2,690 opinions and 1,900 disability cases, classified under a frozen 30-output-key
schema,
with a case-level outcome series built on a documented one-case-one-unit rule.

Agile ELS does not treat model agreement as legal truth or as accuracy against human
coding. It treats models as documented classification instruments and makes the
resulting claims auditable through published inputs, outputs, disagreement records,
validation layers, and deterministic checks.

## 1. When to use it

Agile ELS fits research questions with three properties:

1. The answer lives in a large corpus of legal documents that no one researcher can
   read, but each document can be coded by answering fixed questions with bounded
   answers.
2. The claims the research will print are counts, rates, and directional patterns
   over those codes -- not legal conclusions about individual documents.
3. The budget is a researcher's, not an institution's. The worked implementation's
   primary three-classifier run cost $85.59 in model fees; the full pipeline --
   screening, per-claim extraction, the audits, and one candidate-model run that was
   abandoned and never used -- came to roughly $160, with the Haiku and Sonnet
   adjudication calls billed separately and not itemized in that total.

It does not fit questions that turn on the legal correctness of individual
classifications, or corpora too small for disagreement statistics to be meaningful.

## 2. Design invariants

Every Agile ELS implementation keeps five invariants:

1. **Models classify; they do not judge.** Every instrument asks fixed questions
   with controlled vocabularies. No legal conclusion in the published work rests on
   a model's judgment.
2. **Instruments are frozen and published.** The exact prompts, vocabularies, and
   resolution rules ship with the archive, byte-for-byte as run.
3. **Disagreement is data.** Every inter-model disagreement is resolved by a
   predefined rule, and agreement statistics are reported, never assumed. What is
   published varies by stage and is stated where it binds: for the headline
   mechanism ensemble the raw per-model outputs and the disagreement log ship with
   the archive; for the primary pipeline the resolution is published as
   machine-readable tier metadata rather than as a per-case disagreement log.
4. **Verification is separate from production.** No classification is validated by
   the model or pipeline that produced it. The archive states where this separation
   is partial rather than restating the invariant as satisfied: in the 2015 FHA
   Database component, ties are broken by a MiniMax tiebreaker, and MiniMax M2.7 is
   also one of the three base classifiers (section 5).
5. **Claims trace end to end.** Each printed statistic maps through a claims ledger
   to a source population, a transformation rule, an executable script, and a
   generated artifact, and a deterministic release gate re-checks the chain.

## 3. Corpus construction

The corpus is built from a documented retrieval specification (court coverage, date
window, query terms), unified into a single database with one record per opinion
document and a stable source identifier. Screening to the analysis population is
itself a classification stage with a published instrument, so the population
definition is auditable rather than assumed. Tier definitions (total corpus,
screened-in, subject-screened) are stated as executable predicates, and the same
predicate code generates the published counts.

## 4. Primary classification

Three independently run models from different providers classify the screened corpus
across the database's controlled fields under identical frozen prompts. In
the worked implementation the primary classifiers are MiniMax M2.7, DeepSeek V3.2,
and Kimi K2.5. "Independently run" means separate providers and separate runs -- it
is not a claim about training independence, and Agile ELS never infers error
independence from provider diversity.

## 5. Adjudication

Disagreements route by a predefined, published rule keyed to disagreement shape and
field criticality. Unanimous answers and 2-of-3 majorities are adopted directly, with
no adjudicator call. Only a three-way split escalates: in the worked implementation,
three-way splits on non-critical fields route to a designated adjudicator (Haiku 4.5),
and three-way splits on the critical fields -- outcome, primary claim type, and claim
types -- route to a second designated adjudicator (Sonnet 4.6). The full tier table is
published in `pipeline/consensus_resolution.md` and in machine-readable form in
`pipeline/adjudication_metadata.json`.

Who broke ties differs by run, and the tier metadata records both. In the RA Database
component (n = 1,857) the adjudicators were Haiku 4.5 (697 records) and Sonnet 4.6
(302 records). In the 2015 FHA Database component (n = 1,496) -- which is merged into
the same published unified database, not a discarded precursor -- three-way splits
were instead broken by a MiniMax tiebreaker (171 non-critical, 571 critical: 742
records, 49.6% of that component). MiniMax M2.7 is also one of the three base
classifiers, so for those records the tiebreaker was not independent of the panel it
was resolving. The metadata's own note reads: "earlier-pipeline tier-4 used MiniMax
tiebreaker; later switched to Sonnet 4.6 for the unified RA database."

Adjudicators are not blind: each adjudication request carries the original case text
together with each model's answer for the disputed fields, and the adjudicator applies
the same fixed question under a published adjudication instrument. The routing rule is
part of the frozen instrument set; changing it mid-run is a protocol violation, not a
tuning step.

## 6. Headline-specific coding

Findings that carry the published argument get their own instrument and their own
ensemble, separate from the database build. The worked implementation's directional
translation finding is coded by a three-model ensemble (Kimi K2.6, GLM-5.1, DeepSeek
V3.2) under majority vote, with inter-rater agreement reported (Fleiss kappa =
0.63) and every disagreement logged. Headline findings are labeled model-coded and
directional wherever they are stated.

## 7. Validation and agreement reporting

Validation layers measure reproducibility under the stated instruments -- whether
independent re-reads reproduce the classifications -- not accuracy against a
human-coded gold standard, and the archive says so explicitly. The worked
implementation publishes five layers: (1) the primary pipeline's own inter-model
agreement; (2) the three-model mechanism ensemble (Kimi K2.6 + GLM-5.1 + DeepSeek
V3.2), which also carries the backward-compatibility comparison against an earlier
coding as a sub-item; (3) a stratified single-model re-read by Kimi K2.6; (4) a blind
full-universe fourth-coder re-read by Opus 4.7; and (5) an end-to-end reclassification
audit by a model that played no role in the primary pipeline (Opus 4.6; outcome
kappa = 0.561 on a stratified 50-opinion sample). Raw per-model outputs and the
disagreement log are published for the mechanism ensemble
(`validation_three_model/`); the primary pipeline's per-model raw outputs are not
part of this release, and its resolution is published as tier metadata instead.

Two reporting rules are mandatory. First, agreement is reported as reproducibility;
it does not determine which disputed label is correct. Second, no attenuation or
conservatism claim is made from agreement statistics alone: random nondifferential
error can attenuate an estimated difference only under assumptions this design does
not itself establish.

## 8. Deterministic and nondeterministic boundaries

Everything downstream of the classified database is deterministic: population
filters, collapse rules, counts, rates, and figures regenerate from committed code
and committed inputs. The nondeterministic stages -- model classification runs --
are bounded by frozen instruments, published resolution rules, and -- for the
mechanism ensemble -- committed raw outputs and logged disagreements, so the archive
distinguishes what re-runs exactly from what is reproducible only as
a fresh classification under the same instruments. Human decisions that shape a
denominator (screening rules, one-case-one-unit collapse, keep/exclude
adjudication) are recorded in bounded codes and published so the transformation is
reconstructable, not narrated.

## 9. Failure handling

Failures are handled by rule, not by rerun-until-clean: retrieval misses and
unreadable documents are recorded as unavailable, never silently dropped;
classification runs that fail mid-batch resume from logged state; and discovered
defects are corrected at the source with the affected artifacts regenerated, not
patched in place. A gap in the record is reported as a gap.

## 10. Release controls

The archive ships with a deterministic release gate that re-checks the repository on
every change, including path hygiene, internal links and section anchors, registered
claim values, case-level census reproduction, and a hash manifest of every tracked
file. The
complete list, and what a green run does and does not establish, is in
`../replication/GATES.md`. A green gate asserts that the repository's registered
properties hold; it does not validate legal conclusions or model truth.

## 11. Limitations

Agile ELS inherits the limits of its instruments. Classifications are model
outputs; agreement does not establish accuracy; provider diversity does not
establish error independence; and validation without a human-coded sample bounds
reproducibility, not truth. Findings coded under this method should be labeled
model-coded, and directional findings should stay directional.

## 12. Reuse checklist

To run Agile ELS on a different legal question:

1. Write the retrieval specification and tier predicates first; freeze them.
2. Draft controlled vocabularies and fixed questions for every field; pilot on a
   small sample; freeze the instruments before the production run.
3. Choose three independently run classifiers from different providers and one or
   two designated adjudicators; publish the routing rule before running.
4. Log every disagreement; publish raw outputs alongside resolved labels.
5. Give each headline finding its own instrument and ensemble; report agreement.
6. Build the claims ledger as you write, not after.
7. Wire a release gate that fails on any drift between printed values and generated
   artifacts.
8. State the human-decision boundary (screening, collapse, keep/exclude) in bounded
   codes and publish it.

Adapt the method, not the pipeline: the worked implementation's fields, prompts, and
source constraints are domain-specific.

## 13. Citation

Cite the method as:

Nicholas Gill, *Agile Empirical Legal Studies: Method Specification and Worked
Implementation*, in *Duty Without Data: Research and Replication Archive* (2026).

Pin citations to a commit or archived release as described in the repository's
citation guide. Cite the Arizona Law Review article for the legal argument and
printed findings; cite this specification when relying on or adapting the method's
classification, adjudication, validation, or release-control design.
