# FHA Unified Database — Disability Cases — Three-Period Report

Generated: 2026-07-30 10:16

**Document-level pipeline diagnostic.** Counts and rates in this report are
computed on decided document rows, the pipeline layer above the one-case-one-unit
collapse. They are retained as labeled diagnostics and are not the Note's reported
series; the reported case-level series is `results/series_2026-07.json`.

**Database:** FHA Unified Database, filtered to disability cases (T2 canonical disjunctive)
- Filter expression: `screened-in AND (disability_alleged OR is_ra_case OR "disability" in protected_classes)`
- Total FHA screened-in: 2690
- Disability cases: 1900 (70.6%)
- Dated disability: 1347 — P1: 642, P2: 163, P3: 542
- Undated disability: 553

**Periods:**
- P1: Pre-Loper Bright (1/1/2022 through 6/27/2024)
- P2: Post-LB / Pre-HUD Secretary (6/28/2024 through 2/4/2025)
- P3: Post-HUD Secretary (2/5/2025 through 7/1/2026)

**Decided:** PLAINTIFF_WIN, DEFENDANT_WIN, MIXED

## A. Database Composition

Total screened-in FHA cases: 2690
Disability cases: 1900 (70.6%)
Dated disability cases: 1347
Undated disability cases: 553

| Period | Total | Decided |
|---|---|---|
| P1 | 642 | 476 |
| P2 | 163 | 120 |
| P3 | 542 | 399 |
| All dated | 1347 | 995 |

## B. Overall Win Rates

| Period | N decided | PW | DW | MIXED | Strict % | Broad % |
|---|---|---|---|---|---|---|
| P1 | 476 | 85 | 332 | 59 | 17.9 | 30.3 |
| P2 | 120 | 10 | 95 | 15 | 8.3 | 20.8 |
| P3 | 399 | 39 | 326 | 34 | 9.8 | 18.3 |
| P2+P3 | 519 | 49 | 421 | 49 | 9.4 | 18.9 |
| All | 995 | 134 | 753 | 108 | 13.5 | 24.3 |

Old binary split (validation):
| Era | N decided | PW | DW | MIXED | Strict % | Broad % |
|---|---|---|---|---|---|---|
| pre (<=2023) | 745 | 158 | 487 | 100 | 21.2 | 34.6 |
| post (>=2024) | 728 | 80 | 568 | 80 | 11.0 | 22.0 |

Chi-squared tests (strict):
  P1 vs P2: chi2=6.49, p=0.010862
  P1 vs P3: chi2=11.66, p=0.000639
  P2 vs P3: chi2=0.22, p=0.635943
  P1 vs P2+P3: chi2=15.09, p=0.000103

Chi-squared tests (broad):
  P1 vs P2: chi2=4.19, p=0.04078
  P1 vs P3: chi2=16.64, p=4.5e-05
  P2 vs P3: chi2=0.39, p=0.533435
  P1 vs P2+P3: chi2=17.44, p=3e-05

## C. Year-by-Year Win Rates

| Year | N decided | Strict % | Broad % |
|---|---|---|---|
| 2018 | 26 | 26.9 | 42.3 |
| 2019 | 55 | 25.5 | 54.5 |
| 2020 | 87 | 18.4 | 34.5 |
| 2021 | 155 | 14.2 | 27.7 |
| 2022 | 178 | 23.0 | 31.5 |
| 2023 | 170 | 20.0 | 30.6 |
| 2024 | 237 | 8.4 | 24.1 |
| 2025 | 352 | 11.4 | 19.9 |
| 2026 | 139 | 14.4 | 23.7 |

## D. Plaintiff Type Win Rates

**Overall (dated):**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 834 | 10.6 | 19.7 |
| GOVERNMENT | 11 | 54.5 | 81.8 |
| FAIR_HOUSING_ORG | 32 | 50.0 | 65.6 |
| GROUP_HOME_OPERATOR | 84 | 25.0 | 42.9 |
| OTHER | 33 | 9.1 | 33.3 |

**P1:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 378 | 15.1 | 26.2 |
| GOVERNMENT | 5 | 60.0 | 80.0 |
| FAIR_HOUSING_ORG | 22 | 45.5 | 59.1 |
| GROUP_HOME_OPERATOR | 50 | 24.0 | 40.0 |
| OTHER | 20 | 15.0 | 35.0 |

**P2:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 101 | 3.0 | 12.9 |
| GOVERNMENT | 2 | 0.0 | 100.0 |
| FAIR_HOUSING_ORG | 4 | 75.0 | 75.0 |
| GROUP_HOME_OPERATOR | 11 | 36.4 | 54.5 |
| OTHER | 2 | 0.0 | 50.0 |

**P3:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 355 | 7.9 | 14.6 |
| GOVERNMENT | 4 | 75.0 | 75.0 |
| FAIR_HOUSING_ORG | 6 | 50.0 | 83.3 |
| GROUP_HOME_OPERATOR | 23 | 21.7 | 43.5 |
| OTHER | 11 | 0.0 | 27.3 |

## E. Defendant Type Win Rates

**Overall (dated):**
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 7 | 28.6 | 57.1 |
| HOA_CONDO_ASSN | 86 | 24.4 | 39.5 |
| PRIVATE_LANDLORD | 266 | 17.3 | 28.6 |
| MUNICIPALITY | 153 | 16.3 | 32.0 |
| PROPERTY_MANAGEMENT | 176 | 13.1 | 22.7 |
| OTHER | 102 | 6.9 | 12.7 |
| HOUSING_AUTHORITY | 140 | 4.3 | 12.9 |
| GOVERNMENT | 40 | 0.0 | 2.5 |

Validation (full disability DB including undated):
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 17 | 41.2 | 64.7 |
| HOA_CONDO_ASSN | 142 | 26.1 | 40.8 |
| PRIVATE_LANDLORD | 408 | 19.9 | 32.1 |
| MUNICIPALITY | 228 | 16.7 | 32.9 |
| PROPERTY_MANAGEMENT | 241 | 16.2 | 28.2 |
| OTHER | 149 | 8.1 | 15.4 |
| HOUSING_AUTHORITY | 203 | 6.9 | 18.7 |
| GOVERNMENT | 56 | 8.9 | 10.7 |

**P1:**
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 4 | 25.0 | 50.0 |
| HOA_CONDO_ASSN | 43 | 32.6 | 46.5 |
| PRIVATE_LANDLORD | 128 | 20.3 | 36.7 |
| MUNICIPALITY | 78 | 19.2 | 33.3 |
| PROPERTY_MANAGEMENT | 83 | 18.1 | 27.7 |
| OTHER | 41 | 14.6 | 22.0 |
| HOUSING_AUTHORITY | 69 | 7.2 | 15.9 |
| GOVERNMENT | 18 | 0.0 | 0.0 |

**P2:**
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 1 | 0.0 | 0.0 |
| HOA_CONDO_ASSN | 15 | 6.7 | 40.0 |
| PRIVATE_LANDLORD | 34 | 2.9 | 11.8 |
| MUNICIPALITY | 22 | 27.3 | 50.0 |
| PROPERTY_MANAGEMENT | 13 | 15.4 | 23.1 |
| OTHER | 13 | 0.0 | 0.0 |
| HOUSING_AUTHORITY | 15 | 0.0 | 6.7 |
| GOVERNMENT | 4 | 0.0 | 0.0 |

**P3:**
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 2 | 50.0 | 100.0 |
| HOA_CONDO_ASSN | 28 | 21.4 | 28.6 |
| PRIVATE_LANDLORD | 104 | 18.3 | 24.0 |
| MUNICIPALITY | 53 | 7.5 | 22.6 |
| PROPERTY_MANAGEMENT | 80 | 7.5 | 17.5 |
| OTHER | 48 | 2.1 | 8.3 |
| HOUSING_AUTHORITY | 56 | 1.8 | 10.7 |
| GOVERNMENT | 18 | 0.0 | 5.6 |

## F. Pro Se Analysis

| Metric | Value |
|---|---|
| Known status (dated disability) | 1347 |
| Pro se count | 889 |
| Pro se % | 66.0 |
| Pro se strict % | 4.9 |
| Represented strict % | 31.6 |
| Pro se broad % | 11.1 |
| Represented broad % | 52.2 |

By period:
| Period | Pro Se % | N pro se | N rep | PS Strict % | Rep Strict % | PS Broad % | Rep Broad % |
|---|---|---|---|---|---|---|---|
| P1 | 58.9 | 378 | 264 | 7.0 | 34.2 | 14.7 | 53.7 |
| P2 | 57.7 | 94 | 69 | 2.6 | 19.0 | 9.0 | 42.9 |
| P3 | 76.9 | 417 | 125 | 3.5 | 31.8 | 8.4 | 53.4 |

Validation (full disability DB):
  Pro se: 1161/1899 = 61.1%
  Pro se strict: 6.1% (n=911)
  Represented strict: 32.4% (n=561)

Pro se x defendant type (disability, decided):
| Defendant Type | PS Strict % | PS N | Rep Strict % | Rep N |
|---|---|---|---|---|
| PROPERTY_MANAGEMENT | 5.6% (10/178) | 178 | 46.0% (29/63) | 63 |
| HOA_CONDO_ASSN | 6.7% (4/60) | 60 | 40.2% (33/82) | 82 |
| PRIVATE_LANDLORD | 9.9% (28/282) | 282 | 42.4% (53/125) | 125 |
| HOUSING_AUTHORITY | 4.5% (7/157) | 157 | 15.2% (7/46) | 46 |
| MUNICIPALITY | 3.0% (2/67) | 67 | 22.4% (36/161) | 161 |

## G. MTD Gatekeeping

**MTD share and survival:**
| Period | Decided | MTD Decided | MTD Share % | MTD Strict % | MTD Broad % |
|---|---|---|---|---|---|
| All | 995 | 609 | 61.2 | 9.7 | 19.9 |
| P1 | 476 | 288 | 60.5 | 13.9 | 25.7 |
| P2 | 120 | 73 | 60.8 | 2.7 | 17.8 |
| P3 | 399 | 248 | 62.2 | 6.9 | 13.7 |

Old split validation:
| Era | MTD N | MTD Strict % | MTD Broad % |
|---|---|---|---|
| pre | 390 | 16.4 | 30.0 |
| post | 447 | 6.7 | 16.3 |

**MTD by accommodation type (all disability):**
| Accommodation Type | N | Broad % |
|---|---|---|
| PARKING | 25 | 60.0 |
| ASSISTANCE_ANIMAL | 45 | 42.2 |
| SOBER_LIVING_GROUP_HOME_ZONING | 30 | 50.0 |
| COMMUNICATION_ACCOMMODATION | 15 | 33.3 |
| EVICTION_DEFENSE | 30 | 13.3 |
| POLICY_EXCEPTION | 111 | 26.1 |
| STRUCTURAL_MODIFICATION | 49 | 30.6 |
| DISCRIMINATION_PRIMARY | 223 | 16.1 |
| TRANSFER | 47 | 19.1 |

**MTD by circuit (all disability, n>=20):**
| Circuit | N | Broad % |
|---|---|---|
| 1st Circuit | 26 | 42.3 |
| 2nd Circuit | 140 | 14.3 |
| 3rd Circuit | 107 | 19.6 |
| 4th Circuit | 73 | 17.8 |
| 5th Circuit | 54 | 31.5 |
| 6th Circuit | 63 | 27.0 |
| 7th Circuit | 64 | 34.4 |
| 8th Circuit | 35 | 14.3 |
| 9th Circuit | 162 | 21.0 |
| 10th Circuit | 45 | 31.1 |
| 11th Circuit | 46 | 21.7 |
| D.C. Circuit | 20 | 25.0 |

**Circuit MTD P1 vs P2+P3 (n>=10 both):**
| Circuit | P1 N | P1 Broad % | P2+P3 N | P2+P3 Broad % | Delta pp |
|---|---|---|---|---|---|
| 2nd Circuit | 49 | 16.3 | 51 | 5.9 | -10.4 |
| 3rd Circuit | 36 | 19.4 | 44 | 15.9 | -3.5 |
| 4th Circuit | 23 | 13.0 | 31 | 9.7 | -3.3 |
| 5th Circuit | 20 | 45.0 | 23 | 21.7 | -23.3 |
| 6th Circuit | 22 | 27.3 | 22 | 13.6 | -13.7 |
| 7th Circuit | 27 | 37.0 | 22 | 18.2 | -18.8 |
| 8th Circuit | 11 | 27.3 | 13 | 7.7 | -19.6 |
| 9th Circuit | 52 | 25.0 | 65 | 16.9 | -8.1 |
| 10th Circuit | 12 | 25.0 | 24 | 29.2 | 4.2 |
| 11th Circuit | 22 | 36.4 | 15 | 0.0 | -36.4 |

## H. Interactive Process

| Period | Total | IP Discussed | IP % | IP Strict % | No-IP Strict % | IP Broad % | No-IP Broad % |
|---|---|---|---|---|---|---|---|
| All | 1900 | 200 | 10.5 | 28.1 | 14.4 | 49.2 | 25.3 |
| P1 | 642 | 57 | 8.9 | 27.3 | 16.7 | 41.8 | 28.8 |
| P2 | 163 | 11 | 6.7 | 33.3 | 6.3 | 77.8 | 16.2 |
| P3 | 542 | 41 | 7.6 | 12.5 | 9.5 | 40.6 | 16.3 |

## I. Design-and-Construction

| Period | D&C Cases | D&C Decided | Strict % | Share % |
|---|---|---|---|---|
| All | 59 | 36 | 41.7 | 3.1 |
| P1 | 23 | 13 | 30.8 | 3.6 |
| P2 | 3 | 1 | 100.0 | 1.8 |
| P3 | 9 | 7 | 57.1 | 1.7 |

**FHA Section Citation Effect:**
§ 3604(f)(3)(B) cited: 24.1% strict (n=498)
No specific section: 10.9% strict (n=854)

§ 3604(f)(3)(B) by period:
| Period | N decided | Strict % |
|---|---|---|
| P1 | 160 | 28.8 |
| P2 | 33 | 9.1 |
| P3 | 95 | 18.9 |

## J. Iqbal/Twombly

MTD Iqbal citation rate: 756/927 = 81.6%
| Period | Iqbal Strict % | Iqbal N | No-Iqbal Strict % | No-Iqbal N |
|---|---|---|---|---|
| All | 13.2 | 778 | 19.5 | 694 |
| P1 | 15.5 | 252 | 20.5 | 224 |
| P2 | 3.1 | 65 | 14.5 | 55 |
| P3 | 8.3 | 217 | 11.5 | 182 |

MTD Iqbal citation rate by period:
  P1: 253/315 = 80.3%
  P2: 64/80 = 80.0%
  P3: 216/285 = 75.8%

## K. Loper Bright Citation

All: 6 cases cite Loper Bright
P1: 0 cases cite Loper Bright
P2: 0 cases cite Loper Bright
P3: 6 cases cite Loper Bright

## L. Accommodation Type Win Rates by Period


**P1:**
| Accommodation Type | N decided | Strict % | Broad % |
|---|---|---|---|
| PARKING | 13 | 30.8 | 69.2 |
| ASSISTANCE_ANIMAL | 37 | 43.2 | 70.3 |
| SOBER_LIVING_GROUP_HOME_ZONING | 35 | 25.7 | 45.7 |
| COMMUNICATION_ACCOMMODATION | 17 | 41.2 | 52.9 |
| EVICTION_DEFENSE | 17 | 23.5 | 29.4 |
| POLICY_EXCEPTION | 58 | 19.0 | 29.3 |
| STRUCTURAL_MODIFICATION | 22 | 27.3 | 36.4 |
| DISCRIMINATION_PRIMARY | 115 | 9.6 | 20.9 |
| TRANSFER | 23 | 17.4 | 21.7 |

**P2:**
| Accommodation Type | N decided | Strict % | Broad % |
|---|---|---|---|
| ASSISTANCE_ANIMAL | 6 | 0.0 | 33.3 |
| SOBER_LIVING_GROUP_HOME_ZONING | 11 | 45.5 | 54.5 |
| POLICY_EXCEPTION | 16 | 0.0 | 18.8 |
| STRUCTURAL_MODIFICATION | 11 | 18.2 | 27.3 |
| DISCRIMINATION_PRIMARY | 37 | 5.4 | 18.9 |
| TRANSFER | 6 | 0.0 | 16.7 |

**P3:**
| Accommodation Type | N decided | Strict % | Broad % |
|---|---|---|---|
| PARKING | 14 | 35.7 | 50.0 |
| ASSISTANCE_ANIMAL | 23 | 21.7 | 30.4 |
| SOBER_LIVING_GROUP_HOME_ZONING | 25 | 16.0 | 48.0 |
| COMMUNICATION_ACCOMMODATION | 6 | 0.0 | 33.3 |
| EVICTION_DEFENSE | 34 | 2.9 | 2.9 |
| POLICY_EXCEPTION | 54 | 9.3 | 16.7 |
| STRUCTURAL_MODIFICATION | 21 | 14.3 | 28.6 |
| DISCRIMINATION_PRIMARY | 75 | 12.0 | 16.0 |
| TRANSFER | 14 | 0.0 | 7.1 |