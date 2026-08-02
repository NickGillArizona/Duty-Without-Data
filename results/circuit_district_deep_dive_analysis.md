# Circuit District Deep-Dive Analysis

Generated: 2026-07-06T11:19:51

## Method and assumptions

- Reused the screened-in disability universe and the period definitions used across the document-level analyses: P1 = 2013-2020, P2 = 2021-2022, P3 = 2023-2026.
- Kept the original broad-win definition: outcome in {PLAINTIFF_WIN, MIXED}.
- Ranked circuits by the full-universe P1 -> P3 broad-win decline, then did the district/judge attribution on district-court cases inside those circuits.
- The unified database has no native district or judge fields. Districts were derived from the structured court field; judges were parsed from opinion headers/signatures in the raw-text opinion files from the case-text corpus (not distributed with this repository).
- Judge-level attribution was computed on parsed judge identities, but this public memo reports judge-level results anonymized to the court level. Per-judge identities are withheld by editorial decision: the diagnostic locates where the P3 shortfall concentrates, and publishing named-judge shortfall attributions would invite reading a docket-composition artifact as individual-judge behavior. The distributed results JSON is likewise anonymized.
- Singleton surnames and obvious OCR fragments are now only counted as identified judges when they can be canonically matched to a fuller identity; otherwise they are pushed into the unresolved bucket so they do not overstate identification coverage or depress the unknown-inclusive HHI.
- District and judge 'decline' shares are expressed as a P3 shortfall count: expected P3 broad wins at the circuit's district-court P1 baseline minus actual P3 broad wins. They locate where the P3 shortfall is concentrated, not whose own P1 -> P3 rate changed the most.
- Share-of-full-decline ratios are diagnostic, non-additive shares rather than partition totals. They can exceed 100% because a district-court shortfall is being compared with a full-circuit denominator while offsetting negative contributions and non-district components remain outside the numerator.
- The district-side >50% test is complete because every P3 district-court case is district-assigned. The judge-side >50% test now reports conservative bounds: observed top identified judge share, unknown-judge share, and the max possible single-judge share if all unresolved judge shortfall belonged to one judge.
- MTD survival is coded as 1 - defendant-win rate among P3 district-court motion-to-dismiss cases.
- Post-Jan.-2025 appointee checks use office-relevant appointment dates when a single federal office can be tied to the judge's case district; same-district multi-office biographies are left unresolved rather than forced into a negative.
- A circuit-level post-Jan.-2025 result is only definitive when both judge identification and appointment lookups are complete; otherwise the result is reported as indeterminate rather than as a clean negative.
- Appointment dates come from manual seeds first, then any prior district-keyed lookup results cached from earlier runs, and only then from live public-biography lookups. That makes reruns reproducible within the original environment, but a fresh machine or later biography edits can still change the unresolved/resolved mix at the margins. (The distributed results/circuit_district_deep_dive_results.json omits the per-judge identity fields; a full re-run requires the undistributed case-text corpus.)

## Table: top-5 declining circuits with district-level decomposition

| Circuit | Full P1→P3 decline | P3 district-court cases | Leading district (identified P3 judges) | District share of full decline | Top identified judge (anonymized; court) | Judge share of full decline | HHI (identified / +unknown) | Post-Jan-2025 appointee check |
| --- | ---: | ---: | --- | ---: | --- | ---: | ---: | --- |
| 2nd Circuit | 45.65% → 9.09% (-36.56 pp) | 168 | S.D.N.Y. (34) | 59.4% | S.D.N.Y. judge | 23.1% | 685.33 / 661.14 | 0 resolved; indeterminate |
| 4th Circuit | 42.86% → 10.19% (-32.67 pp) | 96 | D. Md. (13) | 53.8% | D. Md. judge | 7.1% | 500.46 / 1213.11 | 0 resolved; indeterminate |
| 10th Circuit | 43.75% → 11.39% (-32.36 pp) | 75 | D. Kan. (5) | 25.3% | E.D. Okla. judge | 10.9% | 534.41 / 1271.11 | 0 resolved; indeterminate |
| 3rd Circuit | 48.15% → 20.35% (-27.79 pp) | 102 | E.D. Pa. (11) | 58.2% | D.N.J. judge | 13.5% | 621.30 / 2564.40 | 0 resolved; indeterminate |
| 5th Circuit | 42.86% → 16.13% (-26.73 pp) | 85 | N.D. Tex. (6) | 33.0% | W.D. Tex. judge | 12.1% | 448.89 / 2556.40 | 0 resolved; indeterminate |

## Finding: is the decline concentrated in a few judges or genuinely diffuse?

- Districts clearing the >50% full-circuit-decline threshold appear in 3 circuits; there are 3 qualifying district entries: 2nd Circuit — S.D.N.Y. (59.4% of full-circuit shortfall); 4th Circuit — D. Md. (53.8% of full-circuit shortfall); 3rd Circuit — E.D. Pa. (58.2% of full-circuit shortfall).
- No circuit has a definitive observed >50% single-judge concentration.
- The judge-side >50% full-circuit test resolves to no in: 2nd Circuit (max possible single-judge share 33.5%); 4th Circuit (max possible single-judge share 43.9%); 10th Circuit (max possible single-judge share 43.0%).
- The judge-side >50% full-circuit test remains indeterminate where unresolved judge assignments are too large to rule out a single-judge concentration: 3rd Circuit (observed top identified=13.5%, unknown bucket=68.4%, max possible=81.8%); 5th Circuit (observed top identified=12.1%, unknown bucket=65.2%, max possible=77.2%).
- Judge-concentration HHI ranges from 448.89 to 685.33 on identified judges only, and from 661.14 to 2564.40 when the unknown-judge bucket is treated as one extra chamber.
- Overall, the P3 shortfall is more district-concentrated than judge-concentrated: 3 district entries across 3 circuits clear the >50% full-circuit threshold, while the single-judge test resolves to no in 2nd Circuit, 4th Circuit, and 10th Circuit and remains indeterminate in 3rd Circuit and 5th Circuit.

## Finding: does any post-2025 appointee drive meaningful share of P3 outcomes?

- No resolved judge biography shows a post-Jan.-2025 appointee in the P3 set, but the overall check is indeterminate rather than definitively negative.
- Remaining gaps that prevent a definitive negative: 2nd Circuit (50 unresolved appointment lookups; 18 P3 cases with unidentified judges); 4th Circuit (25 unresolved appointment lookups; 30 P3 cases with unidentified judges); 10th Circuit (26 unresolved appointment lookups; 24 P3 cases with unidentified judges); 3rd Circuit (4 unresolved appointment lookups; 50 P3 cases with unidentified judges); 5th Circuit (23 unresolved appointment lookups; 42 P3 cases with unidentified judges).
- Unresolved appointment lookups alone still total 128 across the five circuits.

## Conclusion: effect on the 'institutional, not ideological' claim

- This deep dive still points most strongly to a district-level pleading gate: the steepest declines are heavily concentrated in a few districts, and those districts tend to pair high P3 pro se shares with very low P3 MTD survival.
- But the no-single-judge and no-post-2025-appointee claims are not fully global. The no-single-judge claim is definitive only in 2nd Circuit, 4th Circuit, and 10th Circuit and remains unresolved in 3rd Circuit and 5th Circuit. The post-2025-appointee check remains indeterminate because some P3 judges still lack office-relevant appointment dates or judge identification.

## Circuit-by-circuit findings

### 2nd Circuit

- Full circuit decline: 45.65% -> 9.09% (-36.56 pp), producing a P3 shortfall of 64.35 broad-win-equivalent cases.
- District-court component: 42.50% -> 7.14% (-35.36 pp), with 59.40 shortfall cases across 168 P3 district-court cases (95.5% of the circuit's P3 docket).
- Largest district shortfall concentrations: S.D.N.Y. (38.20 shortfall cases; 59.4% of full-circuit decline; identified P3 judges=34; P3 pro se=80.77%; P3 MTD survival=15.09%); E.D.N.Y. (9.78 shortfall cases; 15.2% of full-circuit decline; identified P3 judges=11; P3 pro se=69.57%; P3 MTD survival=0.00%); N.D.N.Y. (6.05 shortfall cases; 9.4% of full-circuit decline; identified P3 judges=10; P3 pro se=57.69%; P3 MTD survival=33.33%).
- Largest identified judge shortfall concentrations (anonymized to court): an S.D.N.Y. judge (14.88 shortfall cases; 23.1% of full-circuit decline); an E.D.N.Y. judge (2.12 shortfall cases; 3.3% of full-circuit decline); a second S.D.N.Y. judge (2.12 shortfall cases; 3.3% of full-circuit decline).
- Judge identification coverage: 150 / 168 P3 district-court cases (89.3%).
- Concentration: HHI identified-only=685.33; HHI with unknown bucket=661.14.
- >50% test for full-circuit decline: top district S.D.N.Y. = 59.4%; judge-side result = definitive no; observed top identified judge share = 23.1%, unknown-judge bucket = 10.3%, conservative max possible single-judge share = 33.5%.
- Post-Jan. 2025 appointee check: indeterminate; 0 resolved post-Jan. 2025 appointees found, but 50 identified judges still lack appointment dates and 18 P3 cases still lack judge identification.

### 4th Circuit

- Full circuit decline: 42.86% -> 10.19% (-32.67 pp), producing a P3 shortfall of 35.29 broad-win-equivalent cases.
- District-court component: 50.00% -> 9.38% (-40.62 pp), with 39.00 shortfall cases across 96 P3 district-court cases (88.9% of the circuit's P3 docket).
- Largest district shortfall concentrations: D. Md. (19.00 shortfall cases; 53.8% of full-circuit decline; identified P3 judges=13; P3 pro se=63.46%; P3 MTD survival=25.00%); E.D.N.C. (5.50 shortfall cases; 15.6% of full-circuit decline; identified P3 judges=2; P3 pro se=100.00%; P3 MTD survival=12.50%); D.S.C. (4.50 shortfall cases; 12.8% of full-circuit decline; identified P3 judges=3; P3 pro se=90.91%; P3 MTD survival=20.00%).
- Largest identified judge shortfall concentrations (anonymized to court): a D. Md. judge (2.50 shortfall cases; 7.1% of full-circuit decline); a second D. Md. judge (2.50 shortfall cases; 7.1% of full-circuit decline); a third D. Md. judge (2.00 shortfall cases; 5.7% of full-circuit decline).
- Judge identification coverage: 66 / 96 P3 district-court cases (68.8%).
- Concentration: HHI identified-only=500.46; HHI with unknown bucket=1213.11.
- >50% test for full-circuit decline: top district D. Md. = 53.8%; judge-side result = definitive no; observed top identified judge share = 7.1%, unknown-judge bucket = 36.8%, conservative max possible single-judge share = 43.9%.
- Post-Jan. 2025 appointee check: indeterminate; 0 resolved post-Jan. 2025 appointees found, but 25 identified judges still lack appointment dates and 30 P3 cases still lack judge identification.

### 10th Circuit

- Full circuit decline: 43.75% -> 11.39% (-32.36 pp), producing a P3 shortfall of 25.56 broad-win-equivalent cases.
- District-court component: 46.67% -> 12.00% (-34.67 pp), with 26.00 shortfall cases across 75 P3 district-court cases (94.9% of the circuit's P3 docket).
- Largest district shortfall concentrations: D. Kan. (6.47 shortfall cases; 25.3% of full-circuit decline; identified P3 judges=5; P3 pro se=43.75%; P3 MTD survival=16.67%); E.D. Okla. (4.67 shortfall cases; 18.3% of full-circuit decline; identified P3 judges=3; P3 pro se=10.00%; P3 MTD survival=NA); D. Utah (4.53 shortfall cases; 17.7% of full-circuit decline; identified P3 judges=5; P3 pro se=57.14%; P3 MTD survival=42.86%).
- Largest identified judge shortfall concentrations (anonymized to court): an E.D. Okla. judge (2.80 shortfall cases; 10.9% of full-circuit decline); a D. Kan. judge (1.87 shortfall cases; 7.3% of full-circuit decline); a second D. Kan. judge (1.87 shortfall cases; 7.3% of full-circuit decline).
- Judge identification coverage: 51 / 75 P3 district-court cases (68.0%).
- Concentration: HHI identified-only=534.41; HHI with unknown bucket=1271.11.
- >50% test for full-circuit decline: top district D. Kan. = 25.3%; judge-side result = definitive no; observed top identified judge share = 10.9%, unknown-judge bucket = 32.1%, conservative max possible single-judge share = 43.0%.
- Post-Jan. 2025 appointee check: indeterminate; 0 resolved post-Jan. 2025 appointees found, but 26 identified judges still lack appointment dates and 24 P3 cases still lack judge identification.

### 3rd Circuit

- Full circuit decline: 48.15% -> 20.35% (-27.79 pp), producing a P3 shortfall of 31.41 broad-win-equivalent cases.
- District-court component: 52.94% -> 18.63% (-34.31 pp), with 35.00 shortfall cases across 102 P3 district-court cases (90.3% of the circuit's P3 docket).
- Largest district shortfall concentrations: E.D. Pa. (18.29 shortfall cases; 58.2% of full-circuit decline; identified P3 judges=11; P3 pro se=86.36%; P3 MTD survival=13.16%); D.N.J. (14.65 shortfall cases; 46.6% of full-circuit decline; identified P3 judges=11; P3 pro se=66.67%; P3 MTD survival=30.43%); M.D. Pa. (1.18 shortfall cases; 3.8% of full-circuit decline; identified P3 judges=3; P3 pro se=50.00%; P3 MTD survival=33.33%).
- Largest identified judge shortfall concentrations (anonymized to court): a D.N.J. judge (4.24 shortfall cases; 13.5% of full-circuit decline); an E.D. Pa. judge (2.18 shortfall cases; 6.9% of full-circuit decline); a second D.N.J. judge (2.12 shortfall cases; 6.7% of full-circuit decline).
- Judge identification coverage: 52 / 102 P3 district-court cases (51.0%).
- Concentration: HHI identified-only=621.3; HHI with unknown bucket=2564.4.
- >50% test for full-circuit decline: top district E.D. Pa. = 58.2%; judge-side result = indeterminate; observed top identified judge share = 13.5%, unknown-judge bucket = 68.4%, conservative max possible single-judge share = 81.8%.
- Post-Jan. 2025 appointee check: indeterminate; 0 resolved post-Jan. 2025 appointees found, but 4 identified judges still lack appointment dates and 50 P3 cases still lack judge identification.

### 5th Circuit

- Full circuit decline: 42.86% -> 16.13% (-26.73 pp), producing a P3 shortfall of 24.86 broad-win-equivalent cases.
- District-court component: 60.00% -> 16.47% (-43.53 pp), with 37.00 shortfall cases across 85 P3 district-court cases (91.4% of the circuit's P3 docket).
- Largest district shortfall concentrations: N.D. Tex. (8.20 shortfall cases; 33.0% of full-circuit decline; identified P3 judges=6; P3 pro se=70.59%; P3 MTD survival=14.29%); S.D. Tex. (7.80 shortfall cases; 31.4% of full-circuit decline; identified P3 judges=6; P3 pro se=84.62%; P3 MTD survival=33.33%); W.D. Tex. (5.20 shortfall cases; 20.9% of full-circuit decline; identified P3 judges=6; P3 pro se=91.67%; P3 MTD survival=37.50%).
- Largest identified judge shortfall concentrations (anonymized to court): a W.D. Tex. judge (3.00 shortfall cases; 12.1% of full-circuit decline); an S.D. Tex. judge (1.80 shortfall cases; 7.2% of full-circuit decline); an N.D. Tex. judge (1.80 shortfall cases; 7.2% of full-circuit decline).
- Judge identification coverage: 43 / 85 P3 district-court cases (50.6%).
- Concentration: HHI identified-only=448.89; HHI with unknown bucket=2556.4.
- >50% test for full-circuit decline: top district N.D. Tex. = 33.0%; judge-side result = indeterminate; observed top identified judge share = 12.1%, unknown-judge bucket = 65.2%, conservative max possible single-judge share = 77.2%.
- Post-Jan. 2025 appointee check: indeterminate; 0 resolved post-Jan. 2025 appointees found, but 23 identified judges still lack appointment dates and 42 P3 cases still lack judge identification.

## Limitations

- Judge parsing depends on OCR quality in the raw opinion texts; district totals are more reliable than judge-name totals where signatures were badly scanned or where orders only exposed docket initials/section numbers.
- The conservative max-possible single-judge share assumes all unresolved judge shortfall could collapse onto one judge; that is the correct bound for the >50% test, but it is intentionally worst-case rather than a point estimate.
- Appointment-date coverage is now strongest for the judges occupying the largest identified shortfall shares; lower-impact magistrate names and judges without stable public biography pages still leave the all-judges census incomplete, and same-district multi-office biographies are treated conservatively as unresolved when the office-relevant appointment date cannot be isolated.
- Because share-of-full-decline uses a full-circuit denominator, district and judge rows should not be added together and should not be read as exhausting the full decline even when an individual row exceeds 100%.
- The appointment-lookup layer is partly path-dependent: if a prior deep-dive JSON exists in this environment, the script reuses those resolved biographies before hitting live Wikipedia. That improves stability inside this repository but should be disclosed in replication notes.
- Because the unified database has no district/judge variables, this output should be treated as a reproducible derived layer built on top of the structured database, not as native database fields.
