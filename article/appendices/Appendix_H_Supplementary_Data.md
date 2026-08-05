# Appendix H: Supplementary Data

> [!NOTE]
> Outcome rates in this appendix are **document-level** pipeline output (T2 canonical
> population; document-row denominators), published as reproducibility targets for the
> archived scripts. The Note's reported Part II outcome series is the case-level census in
> [`results/series_2026-07.json`](../../results/series_2026-07.json) (qualifying-judgment
> rates 3.53 / 0.00 / 3.21 over the universal one-case-one-unit N 283/63/249, pooled
> N = 595; eighteen qualifying plaintiff-side judgments, none pro se); the Note's fn 66
> describes the case-level construction.
>
> In the procedural-posture tables, "PW Strict" records a plaintiff-favorable disposition at the
> document row for that stage; for Motion to Dismiss rows this is survival of the motion, not a
> qualifying judgment. The case-level census counts qualifying plaintiff-side judgments
> separately (eighteen, all with counsel appeared).

**Cited by:** Note footnote 140 (pleading-stage defense-win lower bounds).
**Evidentiary status:** Appendix-level stakes evidence (classification-dependent) plus sourced administrative statistics (§§ H.1–H.4).
**Regeneration:** litigation tables via `scripts/recompute_all_appendices.py`; administrative figures carry their own sources in-table.

*All data in this Appendix derive from the FHA Unified Database (T2 canonical disability population, n=1,900) unless otherwise noted. Period labels in this Appendix are the date-defined periods used elsewhere in this Note: P1 (2022-01-01 – 2024-06-27), P2 (2024-06-28 – 2025-02-04), P3 (2025-02-05 – 2026-07-01).*

## H.1 Modification Desert Data

- FY2021 reasonable modification complaints: 261 (3.1% of all HUD/FHAP complaints)
- Litigation win rate for structural-modification claims (Appendix E.1, n=83 decided): 19.3% strict / 36.1% broad
- Tenant-pays cost structure: Section 3604(f)(3)(A) requires tenants to bear modification costs, unlike Section 3604(f)(3)(B) accommodations
- Retrofit cost range: $9,000-$75,000 per unit to convert FHA-compliant Type B units to wheelchair-functional UFAS/Type A accessibility

## H.2 Design-and-Construction Noncompliance Ratio

- Noncompliance rate: 47% of covered multifamily communities (Housing Equality Center of Pennsylvania regional testing, 18/38 communities, 2005–2014); Equal Rights Center 2019 D.C. testing found 69.6% violation rate. The 2003 HUD/Steven Winter national study found composite conformance scores of 73–95%, indicating substantial but geographically uneven compliance.
- Complaint rate: 0.8% of all HUD/FHAP complaints (FY2021)
- **Comparison:** noncompliance far exceeds complaint-filing across all testing sources

## H.3 PUMS Disability Housing Data Summary

| Measure | Value | Source |
|---------|-------|--------|
| Disabled renter householders (all types) | 5.56 million | 2023 ACS 1-Year PUMS |
| Disabled renter householders (mobility/independent living) | 2.53 million cost-burdened + 0.98 million zero-income | 2023 ACS 1-Year PUMS |
| Disabled renters of color in non-entitlement communities | >=823,000 (28.3%) | 2022 ACS 5-Year, place-level analysis |
| Zero-income rate, Black disabled renter householders | 19.8% | 2023 ACS 1-Year PUMS |
| Median net worth, Black individuals with disabilities | $1,282 | NDI, 2020 (using SIPP 2014 Wave 4) |

## H.4 Enforcement Infrastructure Data

| Measure | Value | Source |
|---------|-------|--------|
| HUD-direct reasonable-cause charges, Jan.-Aug. 2025 | 0 | NFHA 2025 Trends Report |
| HUD-direct reasonable-cause charges, 2014–2020 average | ≈ 30 / year | Appendix L.4 (FHEO Filed Cases data) |
| FHIP status | Defunded | NFHA 2025 Trends Report |
| FHEO funding (2024) | $86 million (of $153M needed) | NFHA 2025 Trends Report |
| FHEO funding (FY2026 proposal) | $68 million | Administration budget |
| Private nonprofit complaint share | 74.12% | NFHA 2025 Trends Report |
| FHEO 100-day investigation compliance | 29.8% (2020-2022) | HUD OIG Report 2024-BO-0005 |
| Triple enforcement deficit states | 5 (AL, ID, MS, ND, SD) -- 11.7M population | State-classification memorandum retained in the project's private research records |
| Section 811 PRA units | <35,000 | Priced Out 2024 |
| Working-age disabled SSI recipients | 4.1 million | Priced Out 2024 |
| SSI-to-FMR ratio (national average) | 142% | Priced Out 2024 |

## H.5 Procedural Posture Win Rates (FHA Unified Database, Disability Cases)

*Source: FHA Unified Database (T2 canonical disability population, n=1,900). PW Strict = plaintiff-win on all claims; Broad Rate = plaintiff-win on at least one claim or mixed outcome.*

### H.5.1 Overall Procedural Posture Win Rates

| Procedural Posture | Decided n | PW Strict | Broad Rate |
|--------------------|-----------|-----------|------------|
| Motion to Dismiss | 837 | 11.2% | 22.7% |
| Summary Judgment | 219 | 20.1% | 44.3% |
| Appeal | 207 | 19.8% | 31.4% |
| Preliminary Injunction | 103 | 19.4% | 21.4% |
| Trial | 19 | 68.4% | 73.7% |
| Default Judgment | 12 | 75.0% | 75.0% |

### H.5.2 Procedural Posture Win Rates by Period

**P1 (2022-01-01 – 2024-06-27):**

| Procedural Posture | Decided n | PW Strict | Broad Rate |
|--------------------|-----------|-----------|------------|
| Motion to Dismiss | 288 | 13.9% | 25.7% |
| Summary Judgment | 68 | 16.2% | 38.2% |
| Appeal | 45 | 22.2% | 37.8% |
| Preliminary Injunction | 33 | 27.3% | 30.3% |
| Trial | 11 | 63.6% | 72.7% |

**P2 (2024-06-28 – 2025-02-04):**

| Procedural Posture | Decided n | PW Strict | Broad Rate |
|--------------------|-----------|-----------|------------|
| Motion to Dismiss | 73 | 2.7% | 17.8% |
| Summary Judgment | 19 | 21.1% | 42.1% |
| Appeal | 17 | 17.6% | 17.6% |

**P3 (2025-02-05 – 2026-07-01):**

| Procedural Posture | Decided n | PW Strict | Broad Rate |
|--------------------|-----------|-----------|------------|
| Motion to Dismiss | 248 | 6.9% | 13.7% |
| Summary Judgment | 42 | 19.0% | 45.2% |
| Appeal | 35 | 11.4% | 20.0% |
| Preliminary Injunction | 40 | 2.5% | 5.0% |
| Default Judgment | 6 | 83.3% | 83.3% |

*Key finding (document-level series): MTD strict win rates dropped sharply between P1 (13.9%) and P2 (2.7%), and P3 recovered only part of the ground (6.9%). Over the same span summary judgment broad rates held steady and then climbed (38.2% → 42.1% → 45.2%), which fits a story in which the cases that clear MTD land on more favorable terrain. Appeals moved the other way: 37.8% broad in P1 down to 20.0% in P3, bottoming out at 17.6% in P2.*

### H.5.3 Pleading-Stage Defense-Win Lower Bounds (the Note's fn 140)

The pleading-stage defense-win floors on the final 595-case census are:

| Window | Pleading-stage defense wins / decided cases | Lower-bound rate |
|--------|---------------------------------------------|------------------|
| P1 | 142/283 | 50.2% |
| P2 | 48/63 | 76.2% |
| P3 | 144/249 | 57.8% |

These floors apply the registered A08 any-member pleading-loss rule to the final
D-QV5-2 case spine (594 = 282/63/249; see `../../ERRATA.md`). The reconstruction
reproduces the historical 606-case result before yielding the final counts above.
Their lower-bound status and the no-cross-period-trend disclaimer below are unchanged.


These are **lower bounds**, not point estimates: not every validation lane exposes a complete
pleading-stage flag, so a decided case whose lanes do not surface the flag is excluded from the
numerator even when its disposition was in fact a pleading-stage defense win. Because the degree
of flag under-coverage may itself differ across windows, no cross-period trend is asserted on
this series.

## H.6 Housing Type Win Rates

| Housing Type | Decided n | PW Strict | Broad Rate |
|--------------|-----------|-----------|------------|
| Private Market | 588 | 19.4% | 33.0% |
| Public Housing | 107 | 4.7% | 18.7% |
| Other Subsidized | 60 | 16.7% | 30.0% |

*Public housing plaintiffs win at roughly one-quarter the strict rate and just over half the broad rate of private market plaintiffs; the housing-authority rows of § H.10 show the same pattern by defendant type.*

## H.7 Delay-as-Denial Analysis

**Prevalence:** 72 cases invoke delay-as-denial (3.8% of all disability cases in the FHA Unified Database).

| DaD Invoked | Decided n | PW Strict | Broad Rate |
|-------------|-----------|-----------|------------|
| Yes | 66 | 37.9% | 65.2% |
| No | 1,405 | 15.1% | 26.6% |

*When courts treat unreasonable delay as a constructive denial of accommodation, plaintiffs do far better: strict win rates run 2.5x higher, broad rates 2.4x higher.*

## H.8 Interactive Process and Delay-as-Denial Co-Occurrence

Of 200 cases in which courts discuss the interactive process, delay-as-denial is also invoked in 59 (29.5%). Combined IP+DaD strict win: 43.4% (n=53); combined broad win: 69.8%. A court already working through the interactive-process framework tends to look at the timing of the accommodation request, and that is where delay-as-denial gets recognized.

## H.9 *Loper Bright* Citation Analysis

Total cases citing *Loper Bright Enterprises v. Raimondo*: **6** in the T2 disability population (all in P3); the full unified corpus contains 9. The low count is unsurprising for a decision this recent, and the Note's argument does not depend on citation uptake: the dataset uses June 28, 2024 only as a period boundary (Note fn 67), and the Note's administrative-law argument (Parts III.A and IV.A) is built for independent-judgment review rather than resting on deference.

## H.10 Pro Se Outcomes by Defendant Type (All Disability Decided)

| Defendant Type | Pro Se PW Strict (n) | Represented PW Strict (n) |
|----------------|----------------------|---------------------------|
| Property Management | 5.6% (10/178) | 46.0% (29/63) |
| HOA / Condo | 6.7% (4/60) | 40.2% (33/82) |
| Private Landlord | 9.9% (28/282) | 42.4% (53/125) |
| Housing Authority | 4.5% (7/157) | 15.2% (7/46) |
| Municipality | 3.0% (2/67) | 22.4% (36/161) |
| Government | 0.0% (0/37) | 26.3% (5/19) |

*Every defendant type shows the representation gap. Pro se plaintiffs do worst against municipalities (3.0%) and housing authorities (4.5%), which are also the institutional defendants most likely to have experienced counsel on the other side. Private landlords are the smallest-scale defendants, yet even there pro se win rates (9.9%) come to roughly one-quarter of the represented rate (42.4%). The HOA numbers (6.7% vs. 40.2%) are harder to explain away, since HOA disputes often turn on well-documented accommodation requests where the factual record ought to favor plaintiffs.*

---
