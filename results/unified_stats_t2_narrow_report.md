# FHA Unified Database — Disability Cases — Three-Period Report

Generated: 2026-07-26 10:44

**Database:** FHA Unified Database, filtered to disability cases (T2-narrow robustness)
- Filter expression: `screened-in AND "disability" in protected_classes`
- Total FHA screened-in: 2690
- Disability cases: 1849 (68.7%)
- Dated disability: 1320 — P1: 630, P2: 159, P3: 531
- Undated disability: 529

**Periods:**
- P1: Pre-Loper Bright (1/1/2022 through 6/27/2024)
- P2: Post-LB / Pre-HUD Secretary (6/28/2024 through 2/4/2025)
- P3: Post-HUD Secretary (2/5/2025 through 7/1/2026)

**Decided:** PLAINTIFF_WIN, DEFENDANT_WIN, MIXED

## A. Database Composition

Total screened-in FHA cases: 2690
Disability cases: 1849 (68.7%)
Dated disability cases: 1320
Undated disability cases: 529

| Period | Total | Decided |
|---|---|---|
| P1 | 630 | 465 |
| P2 | 159 | 116 |
| P3 | 531 | 391 |
| All dated | 1320 | 972 |

## B. Overall Win Rates

| Period | N decided | PW | DW | MIXED | Strict % | Broad % |
|---|---|---|---|---|---|---|
| P1 | 465 | 83 | 326 | 56 | 17.8 | 29.9 |
| P2 | 116 | 9 | 92 | 15 | 7.8 | 20.7 |
| P3 | 391 | 36 | 323 | 32 | 9.2 | 17.4 |
| P2+P3 | 507 | 45 | 415 | 47 | 8.9 | 18.1 |
| All | 972 | 128 | 741 | 103 | 13.2 | 23.8 |

Old binary split (validation):
| Era | N decided | PW | DW | MIXED | Strict % | Broad % |
|---|---|---|---|---|---|---|
| pre (<=2023) | 714 | 150 | 470 | 94 | 21.0 | 34.2 |
| post (>=2024) | 715 | 76 | 561 | 78 | 10.6 | 21.5 |

Chi-squared tests (strict):
  P1 vs P2: chi2=7.09, p=0.007737
  P1 vs P3: chi2=13.25, p=0.000272
  P2 vs P3: chi2=0.23, p=0.629981
  P1 vs P2+P3: chi2=17.08, p=3.6e-05

Chi-squared tests (broad):
  P1 vs P2: chi2=3.9, p=0.048415
  P1 vs P3: chi2=18.1, p=2.1e-05
  P2 vs P3: chi2=0.66, p=0.418245
  P1 vs P2+P3: chi2=18.47, p=1.7e-05

## C. Year-by-Year Win Rates

| Year | N decided | Strict % | Broad % |
|---|---|---|---|
| 2018 | 22 | 22.7 | 31.8 |
| 2019 | 51 | 23.5 | 54.9 |
| 2020 | 80 | 20.0 | 37.5 |
| 2021 | 149 | 13.4 | 26.8 |
| 2022 | 172 | 23.3 | 30.2 |
| 2023 | 166 | 19.9 | 30.7 |
| 2024 | 232 | 8.2 | 24.1 |
| 2025 | 345 | 10.7 | 18.8 |
| 2026 | 138 | 14.5 | 23.9 |

## D. Plaintiff Type Win Rates

**Overall (dated):**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 815 | 10.2 | 19.0 |
| GOVERNMENT | 11 | 54.5 | 81.8 |
| FAIR_HOUSING_ORG | 31 | 51.6 | 67.7 |
| GROUP_HOME_OPERATOR | 84 | 25.0 | 42.9 |
| OTHER | 30 | 6.7 | 30.0 |

**P1:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 371 | 15.1 | 25.9 |
| GOVERNMENT | 5 | 60.0 | 80.0 |
| FAIR_HOUSING_ORG | 21 | 47.6 | 61.9 |
| GROUP_HOME_OPERATOR | 50 | 24.0 | 40.0 |
| OTHER | 17 | 11.8 | 29.4 |

**P2:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 97 | 2.1 | 12.4 |
| GOVERNMENT | 2 | 0.0 | 100.0 |
| FAIR_HOUSING_ORG | 4 | 75.0 | 75.0 |
| GROUP_HOME_OPERATOR | 11 | 36.4 | 54.5 |
| OTHER | 2 | 0.0 | 50.0 |

**P3:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 347 | 7.2 | 13.5 |
| GOVERNMENT | 4 | 75.0 | 75.0 |
| FAIR_HOUSING_ORG | 6 | 50.0 | 83.3 |
| GROUP_HOME_OPERATOR | 23 | 21.7 | 43.5 |
| OTHER | 11 | 0.0 | 27.3 |

## E. Defendant Type Win Rates

**Overall (dated):**
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 7 | 28.6 | 57.1 |
| HOA_CONDO_ASSN | 83 | 22.9 | 37.3 |
| PRIVATE_LANDLORD | 259 | 16.6 | 27.4 |
| MUNICIPALITY | 150 | 16.0 | 31.3 |
| PROPERTY_MANAGEMENT | 174 | 13.2 | 23.0 |
| OTHER | 98 | 7.1 | 13.3 |
| HOUSING_AUTHORITY | 138 | 4.3 | 12.3 |
| GOVERNMENT | 39 | 0.0 | 2.6 |

Validation (full disability DB including undated):
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 17 | 41.2 | 64.7 |
| HOA_CONDO_ASSN | 137 | 24.8 | 39.4 |
| PRIVATE_LANDLORD | 394 | 19.3 | 31.0 |
| MUNICIPALITY | 225 | 16.4 | 32.4 |
| PROPERTY_MANAGEMENT | 235 | 16.2 | 28.1 |
| OTHER | 139 | 7.2 | 15.1 |
| HOUSING_AUTHORITY | 199 | 7.0 | 18.6 |
| GOVERNMENT | 55 | 9.1 | 10.9 |

**P1:**
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 4 | 25.0 | 50.0 |
| HOA_CONDO_ASSN | 43 | 32.6 | 46.5 |
| PRIVATE_LANDLORD | 124 | 20.2 | 36.3 |
| MUNICIPALITY | 76 | 18.4 | 31.6 |
| PROPERTY_MANAGEMENT | 82 | 18.3 | 28.0 |
| OTHER | 39 | 15.4 | 23.1 |
| HOUSING_AUTHORITY | 67 | 7.5 | 14.9 |
| GOVERNMENT | 18 | 0.0 | 0.0 |

**P2:**
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 1 | 0.0 | 0.0 |
| HOA_CONDO_ASSN | 15 | 6.7 | 40.0 |
| PRIVATE_LANDLORD | 33 | 0.0 | 9.1 |
| MUNICIPALITY | 21 | 28.6 | 52.4 |
| PROPERTY_MANAGEMENT | 13 | 15.4 | 23.1 |
| OTHER | 11 | 0.0 | 0.0 |
| HOUSING_AUTHORITY | 15 | 0.0 | 6.7 |
| GOVERNMENT | 4 | 0.0 | 0.0 |

**P3:**
| Defendant Type | N decided | Strict % | Broad % |
|---|---|---|---|
| DEVELOPER | 2 | 50.0 | 100.0 |
| HOA_CONDO_ASSN | 25 | 16.0 | 20.0 |
| PRIVATE_LANDLORD | 102 | 17.6 | 22.5 |
| MUNICIPALITY | 53 | 7.5 | 22.6 |
| PROPERTY_MANAGEMENT | 79 | 7.6 | 17.7 |
| OTHER | 48 | 2.1 | 8.3 |
| HOUSING_AUTHORITY | 56 | 1.8 | 10.7 |
| GOVERNMENT | 17 | 0.0 | 5.9 |

## F. Pro Se Analysis

| Metric | Value |
|---|---|
| Known status (dated disability) | 1320 |
| Pro se count | 874 |
| Pro se % | 66.2 |
| Pro se strict % | 4.8 |
| Represented strict % | 31.2 |
| Pro se broad % | 11.0 |
| Represented broad % | 51.3 |

By period:
| Period | Pro Se % | N pro se | N rep | PS Strict % | Rep Strict % | PS Broad % | Rep Broad % |
|---|---|---|---|---|---|---|---|
| P1 | 59.2 | 373 | 257 | 7.1 | 34.4 | 14.5 | 53.6 |
| P2 | 56.6 | 90 | 69 | 1.4 | 19.0 | 8.1 | 42.9 |
| P3 | 77.4 | 411 | 120 | 3.6 | 30.1 | 8.4 | 50.6 |

Validation (full disability DB):
  Pro se: 1134/1848 = 61.4%
  Pro se strict: 6.0% (n=889)
  Represented strict: 32.1% (n=539)

Pro se x defendant type (disability, decided):
| Defendant Type | PS Strict % | PS N | Rep Strict % | Rep N |
|---|---|---|---|---|
| PROPERTY_MANAGEMENT | 5.8% (10/173) | 173 | 45.2% (28/62) | 62 |
| HOA_CONDO_ASSN | 6.7% (4/60) | 60 | 39.0% (30/77) | 77 |
| PRIVATE_LANDLORD | 9.8% (27/276) | 276 | 41.9% (49/117) | 117 |
| HOUSING_AUTHORITY | 4.5% (7/156) | 156 | 16.3% (7/43) | 43 |
| MUNICIPALITY | 3.0% (2/66) | 66 | 22.0% (35/159) | 159 |

## G. MTD Gatekeeping

**MTD share and survival:**
| Period | Decided | MTD Decided | MTD Share % | MTD Strict % | MTD Broad % |
|---|---|---|---|---|---|
| All | 972 | 594 | 61.1 | 9.6 | 19.5 |
| P1 | 465 | 281 | 60.4 | 13.9 | 25.3 |
| P2 | 116 | 70 | 60.3 | 2.9 | 18.6 |
| P3 | 391 | 243 | 62.1 | 6.6 | 13.2 |

Old split validation:
| Era | MTD N | MTD Strict % | MTD Broad % |
|---|---|---|---|
| pre | 374 | 16.6 | 29.4 |
| post | 438 | 6.6 | 16.2 |

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
| DISCRIMINATION_PRIMARY | 209 | 14.4 |
| TRANSFER | 47 | 19.1 |

**MTD by circuit (all disability, n>=20):**
| Circuit | N | Broad % |
|---|---|---|
| 1st Circuit | 26 | 42.3 |
| 2nd Circuit | 135 | 14.8 |
| 3rd Circuit | 104 | 19.2 |
| 4th Circuit | 71 | 15.5 |
| 5th Circuit | 53 | 30.2 |
| 6th Circuit | 63 | 27.0 |
| 7th Circuit | 63 | 33.3 |
| 8th Circuit | 33 | 15.2 |
| 9th Circuit | 155 | 21.3 |
| 10th Circuit | 43 | 30.2 |
| 11th Circuit | 45 | 20.0 |

**Circuit MTD P1 vs P2+P3 (n>=10 both):**
| Circuit | P1 N | P1 Broad % | P2+P3 N | P2+P3 Broad % | Delta pp |
|---|---|---|---|---|---|
| 2nd Circuit | 48 | 16.7 | 49 | 6.1 | -10.6 |
| 3rd Circuit | 35 | 20.0 | 44 | 15.9 | -4.1 |
| 4th Circuit | 21 | 4.8 | 31 | 9.7 | 4.9 |
| 5th Circuit | 20 | 45.0 | 22 | 18.2 | -26.8 |
| 6th Circuit | 22 | 27.3 | 22 | 13.6 | -13.7 |
| 7th Circuit | 26 | 34.6 | 22 | 18.2 | -16.4 |
| 8th Circuit | 10 | 30.0 | 13 | 7.7 | -22.3 |
| 9th Circuit | 51 | 25.5 | 62 | 17.7 | -7.8 |
| 10th Circuit | 12 | 25.0 | 22 | 27.3 | 2.3 |
| 11th Circuit | 22 | 36.4 | 15 | 0.0 | -36.4 |

## H. Interactive Process

| Period | Total | IP Discussed | IP % | IP Strict % | No-IP Strict % | IP Broad % | No-IP Broad % |
|---|---|---|---|---|---|---|---|
| All | 1849 | 200 | 10.8 | 28.1 | 13.9 | 49.2 | 24.6 |
| P1 | 630 | 57 | 9.0 | 27.3 | 16.6 | 41.8 | 28.4 |
| P2 | 159 | 11 | 6.9 | 33.3 | 5.6 | 77.8 | 15.9 |
| P3 | 531 | 41 | 7.7 | 12.5 | 8.9 | 40.6 | 15.3 |

## I. Design-and-Construction

| Period | D&C Cases | D&C Decided | Strict % | Share % |
|---|---|---|---|---|
| All | 59 | 36 | 41.7 | 3.2 |
| P1 | 23 | 13 | 30.8 | 3.7 |
| P2 | 3 | 1 | 100.0 | 1.9 |
| P3 | 9 | 7 | 57.1 | 1.7 |

**FHA Section Citation Effect:**
§ 3604(f)(3)(B) cited: 24.1% strict (n=498)
No specific section: 10.3% strict (n=815)

§ 3604(f)(3)(B) by period:
| Period | N decided | Strict % |
|---|---|---|
| P1 | 160 | 28.8 |
| P2 | 33 | 9.1 |
| P3 | 95 | 18.9 |

## J. Iqbal/Twombly

MTD Iqbal citation rate: 735/902 = 81.5%
| Period | Iqbal Strict % | Iqbal N | No-Iqbal Strict % | No-Iqbal N |
|---|---|---|---|---|
| All | 12.9 | 751 | 19.1 | 677 |
| P1 | 15.4 | 246 | 20.5 | 219 |
| P2 | 3.2 | 63 | 13.2 | 53 |
| P3 | 7.6 | 210 | 11.0 | 181 |

MTD Iqbal citation rate by period:
  P1: 247/308 = 80.2%
  P2: 62/77 = 80.5%
  P3: 212/280 = 75.7%

## K. Loper Bright Citation

All: 3 cases cite Loper Bright
P1: 0 cases cite Loper Bright
P2: 0 cases cite Loper Bright
P3: 3 cases cite Loper Bright

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
| STRUCTURAL_MODIFICATION | 21 | 23.8 | 33.3 |
| DISCRIMINATION_PRIMARY | 111 | 9.9 | 18.9 |
| TRANSFER | 23 | 17.4 | 21.7 |

**P2:**
| Accommodation Type | N decided | Strict % | Broad % |
|---|---|---|---|
| ASSISTANCE_ANIMAL | 6 | 0.0 | 33.3 |
| SOBER_LIVING_GROUP_HOME_ZONING | 11 | 45.5 | 54.5 |
| POLICY_EXCEPTION | 16 | 0.0 | 18.8 |
| STRUCTURAL_MODIFICATION | 11 | 18.2 | 27.3 |
| DISCRIMINATION_PRIMARY | 34 | 2.9 | 17.6 |
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
| DISCRIMINATION_PRIMARY | 69 | 10.1 | 11.6 |
| TRANSFER | 14 | 0.0 | 7.1 |