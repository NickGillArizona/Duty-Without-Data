# FHA Unified Database — Complete Appendix Data

Generated: 2026-07-30 10:16

**Document-level pipeline diagnostic.** Counts and rates in this report are
computed on decided document rows, the pipeline layer above the one-case-one-unit
collapse. They are retained as labeled diagnostics and are not the Note's reported
series; the reported case-level series is `results/series_2026-07.json`.

**Database:** FHA Unified Database, disability cases only
- Total FHA screened-in: 2690
- Disability cases: 1900 (70.6%)
- Dated disability: 1347 — P1: 642, P2: 163, P3: 542

**Periods:**
- P1: Pre-*Loper Bright* (1/1/2022 – 6/28/2024)
- P2: Post-LB / Pre-HUD Secretary (6/28/2024 – 2/5/2025)
- P3: Post-HUD Secretary (2/5/2025 – 7/1/2026)

## APPENDIX B: Results Tables

### B.1 Three-Period Win Rates

| Period | N decided | PW | DW | MIXED | Strict % | Broad % |
|---|---|---|---|---|---|---|
| P1 | 476 | 85 | 332 | 59 | 17.9 | 30.3 |
| P2 | 120 | 10 | 95 | 15 | 8.3 | 20.8 |
| P3 | 399 | 39 | 326 | 34 | 9.8 | 18.3 |
| P2+P3 | 519 | 49 | 421 | 49 | 9.4 | 18.9 |
| All dated | 995 | 134 | 753 | 108 | 13.5 | 24.3 |

### B.2 Binary Split Validation

| Era | N decided | Strict % | Broad % |
|---|---|---|---|
| pre (<=2023) | 745 | 21.2 | 34.6 |
| post (>=2024) | 728 | 11.0 | 22.0 |

### B.3 Year-by-Year (Table B.3)

| Year | N decided | Strict % | Broad % |
|---|---|---|---|
| 2015 | 25 | 32.0 | 40.0 |
| 2016 | 29 | 31.0 | 58.6 |
| 2017 | 20 | 35.0 | 45.0 |
| 2018 | 26 | 26.9 | 42.3 |
| 2019 | 55 | 25.5 | 54.5 |
| 2020 | 87 | 18.4 | 34.5 |
| 2021 | 155 | 14.2 | 27.7 |
| 2022 | 178 | 23.0 | 31.5 |
| 2023 | 170 | 20.0 | 30.6 |
| 2024 | 237 | 8.4 | 24.1 |
| 2025 | 352 | 11.4 | 19.9 |
| 2026 | 139 | 14.4 | 23.7 |

### B.4 Procedural Disposition

| Disposition | Count | % of decided |
|---|---|---|
| MOTION_TO_DISMISS | 837 | 56.8 |
| SUMMARY_JUDGMENT | 219 | 14.9 |
| APPEAL | 207 | 14.1 |
| PRELIMINARY_INJUNCTION | 103 | 7.0 |
| OTHER_PROCEDURAL | 57 | 3.9 |
| TRIAL | 19 | 1.3 |
| DEFAULT_JUDGMENT | 12 | 0.8 |
| OTHER | 8 | 0.5 |
| DISCOVERY | 6 | 0.4 |
| ADMINISTRATIVE_REVIEW | 3 | 0.2 |
| PROCEDURAL | 1 | 0.1 |
| SETTLEMENT_CONSENT | 1 | 0.1 |

### B.5 Statistical Tests

**Strict:**
  P1 vs P2: χ²=6.49, p=0.010862
  P1 vs P3: χ²=11.66, p=0.000639
  P2 vs P3: χ²=0.22, p=0.635943
  P1 vs P2+P3: χ²=15.09, p=0.000103

**Broad:**
  P1 vs P2: χ²=4.19, p=0.04078
  P1 vs P3: χ²=16.64, p=4.5e-05
  P2 vs P3: χ²=0.39, p=0.533435
  P1 vs P2+P3: χ²=17.44, p=3e-05

## APPENDIX C: Iqbal/Twombly Analysis

MTD Iqbal citation rate: 756/927 = 81.6%

**By period:**
  P1: 253/315 = 80.3%
  P2: 64/80 = 80.0%
  P3: 216/285 = 75.8%

**Iqbal effect on outcomes (all disability):**
| Period | Iqbal Strict % | Iqbal N | No-Iqbal Strict % | No-Iqbal N | Iqbal Broad % | No-Iqbal Broad % |
|---|---|---|---|---|---|---|
| All | 13.2 | 778 | 19.5 | 694 | 25.6 | 31.6 |
| P1 | 15.5 | 252 | 20.5 | 224 | 29.0 | 31.7 |
| P2 | 3.1 | 65 | 14.5 | 55 | 16.9 | 25.5 |
| P3 | 8.3 | 217 | 11.5 | 182 | 15.2 | 22.0 |

**MTD outcomes with/without Iqbal:**
| Metric | Iqbal Cited | Not Cited |
|---|---|---|
| N decided | 703 | 133 |
| DW % | 76.2 | 82.7 |
| PW % | 11.9 | 7.5 |
| Broad % | 23.8 | 17.3 |

**Cross-class Iqbal MTD citation rates:**
  disability: 735/902 = 81.5%
  race: 407/467 = 87.2%
  familial_status: 57/70 = 81.4%

## APPENDIX E: Accommodation & Defendant Analysis

### E.1 Win Rates by Accommodation Type (all disability decided)

| Accommodation Type | N decided | PW % | DW % | MIXED % | Strict % | Broad % |
|---|---|---|---|---|---|---|
| ASSISTANCE_ANIMAL | 106 | 34.0 | 45.3 | 20.8 | 34.0 | 54.7 |
| PARKING | 48 | 33.3 | 45.8 | 20.8 | 33.3 | 54.2 |
| SOBER_LIVING_GROUP_HOME_ZONING | 108 | 27.8 | 50.9 | 21.3 | 27.8 | 49.1 |
| LIVE_IN_AIDE | 24 | 25.0 | 62.5 | 12.5 | 25.0 | 37.5 |
| COMMUNICATION_ACCOMMODATION | 34 | 26.5 | 50.0 | 23.5 | 26.5 | 50.0 |
| EVICTION_DEFENSE | 63 | 14.3 | 82.5 | 3.2 | 14.3 | 17.5 |
| STRUCTURAL_MODIFICATION | 83 | 19.3 | 63.9 | 16.9 | 19.3 | 36.1 |
| OTHER | 159 | 14.5 | 76.1 | 9.4 | 14.5 | 23.9 |
| POLICY_EXCEPTION | 210 | 13.3 | 75.2 | 11.4 | 13.3 | 24.8 |
| DISCRIMINATION_PRIMARY | 340 | 13.5 | 77.6 | 8.8 | 13.5 | 22.4 |
| TRANSFER | 67 | 7.5 | 80.6 | 11.9 | 7.5 | 19.4 |
| RENT_PAYMENT | 19 | 15.8 | 63.2 | 21.1 | 15.8 | 36.8 |
| UNDETERMINED | 206 | 4.4 | 88.3 | 7.3 | 4.4 | 11.7 |

**P1:**
| Accommodation Type | N decided | Strict % | Broad % |
|---|---|---|---|
| ASSISTANCE_ANIMAL | 37 | 43.2 | 70.3 |
| PARKING | 13 | 30.8 | 69.2 |
| SOBER_LIVING_GROUP_HOME_ZONING | 35 | 25.7 | 45.7 |
| LIVE_IN_AIDE | 7 | 14.3 | 14.3 |
| COMMUNICATION_ACCOMMODATION | 17 | 41.2 | 52.9 |
| EVICTION_DEFENSE | 17 | 23.5 | 29.4 |
| STRUCTURAL_MODIFICATION | 22 | 27.3 | 36.4 |
| OTHER | 55 | 14.5 | 25.5 |
| POLICY_EXCEPTION | 58 | 19.0 | 29.3 |
| DISCRIMINATION_PRIMARY | 115 | 9.6 | 20.9 |
| TRANSFER | 23 | 17.4 | 21.7 |
| RENT_PAYMENT | 5 | 20.0 | 60.0 |
| UNDETERMINED | 71 | 4.2 | 8.5 |

**P2:**
| Accommodation Type | N decided | Strict % | Broad % |
|---|---|---|---|
| ASSISTANCE_ANIMAL | 6 | 0.0 | 33.3 |
| SOBER_LIVING_GROUP_HOME_ZONING | 11 | 45.5 | 54.5 |
| COMMUNICATION_ACCOMMODATION | 3 | 0.0 | 0.0 |
| STRUCTURAL_MODIFICATION | 11 | 18.2 | 27.3 |
| OTHER | 8 | 12.5 | 25.0 |
| POLICY_EXCEPTION | 16 | 0.0 | 18.8 |
| DISCRIMINATION_PRIMARY | 37 | 5.4 | 18.9 |
| TRANSFER | 6 | 0.0 | 16.7 |
| UNDETERMINED | 18 | 0.0 | 5.6 |

**P3:**
| Accommodation Type | N decided | Strict % | Broad % |
|---|---|---|---|
| ASSISTANCE_ANIMAL | 23 | 21.7 | 30.4 |
| PARKING | 14 | 35.7 | 50.0 |
| SOBER_LIVING_GROUP_HOME_ZONING | 25 | 16.0 | 48.0 |
| LIVE_IN_AIDE | 5 | 0.0 | 0.0 |
| COMMUNICATION_ACCOMMODATION | 6 | 0.0 | 33.3 |
| EVICTION_DEFENSE | 34 | 2.9 | 2.9 |
| STRUCTURAL_MODIFICATION | 21 | 14.3 | 28.6 |
| OTHER | 40 | 12.5 | 17.5 |
| POLICY_EXCEPTION | 54 | 9.3 | 16.7 |
| DISCRIMINATION_PRIMARY | 75 | 12.0 | 16.0 |
| TRANSFER | 14 | 0.0 | 7.1 |
| RENT_PAYMENT | 11 | 0.0 | 9.1 |
| UNDETERMINED | 76 | 2.6 | 10.5 |

### E.2 Win Rates by Defendant Type (all disability decided)

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
| HOA_CONDO_ASSN | 28 | 21.4 | 28.6 |
| PRIVATE_LANDLORD | 104 | 18.3 | 24.0 |
| MUNICIPALITY | 53 | 7.5 | 22.6 |
| PROPERTY_MANAGEMENT | 80 | 7.5 | 17.5 |
| OTHER | 48 | 2.1 | 8.3 |
| HOUSING_AUTHORITY | 56 | 1.8 | 10.7 |
| GOVERNMENT | 18 | 0.0 | 5.6 |

### E.3 Win Rates by Disability Category

| Disability Category | N decided | Strict % | Broad % |
|---|---|---|---|
| SENSORY | 40 | 32.5 | 57.5 |
| INTELLECTUAL_DEVELOPMENTAL | 55 | 29.1 | 41.8 |
| MOBILITY | 220 | 25.9 | 45.0 |
| SUBSTANCE_USE | 92 | 23.9 | 40.2 |
| MENTAL_HEALTH | 218 | 17.0 | 29.4 |
| MULTIPLE_UNSPECIFIED | 411 | 15.1 | 26.3 |
| OTHER | 83 | 15.7 | 27.7 |
| UNDETERMINED | 343 | 5.0 | 11.4 |

**P1:**
| Disability Category | N decided | Strict % | Broad % |
|---|---|---|---|
| SENSORY | 18 | 38.9 | 55.6 |
| INTELLECTUAL_DEVELOPMENTAL | 18 | 22.2 | 44.4 |
| MOBILITY | 59 | 20.3 | 42.4 |
| SUBSTANCE_USE | 36 | 22.2 | 33.3 |
| MENTAL_HEALTH | 80 | 21.2 | 36.2 |
| MULTIPLE_UNSPECIFIED | 127 | 17.3 | 28.3 |
| OTHER | 17 | 35.3 | 47.1 |
| UNDETERMINED | 117 | 7.7 | 13.7 |

**P2:**
| Disability Category | N decided | Strict % | Broad % |
|---|---|---|---|
| INTELLECTUAL_DEVELOPMENTAL | 4 | 75.0 | 75.0 |
| MOBILITY | 13 | 7.7 | 15.4 |
| MENTAL_HEALTH | 23 | 4.3 | 26.1 |
| MULTIPLE_UNSPECIFIED | 36 | 13.9 | 30.6 |
| OTHER | 12 | 0.0 | 16.7 |
| UNDETERMINED | 28 | 0.0 | 3.6 |

**P3:**
| Disability Category | N decided | Strict % | Broad % |
|---|---|---|---|
| SENSORY | 8 | 12.5 | 50.0 |
| INTELLECTUAL_DEVELOPMENTAL | 16 | 6.2 | 18.8 |
| MOBILITY | 47 | 27.7 | 38.3 |
| SUBSTANCE_USE | 18 | 22.2 | 50.0 |
| MENTAL_HEALTH | 45 | 11.1 | 17.8 |
| MULTIPLE_UNSPECIFIED | 115 | 7.0 | 13.0 |
| OTHER | 22 | 13.6 | 18.2 |
| UNDETERMINED | 125 | 3.2 | 9.6 |

### E.4 Win Rates by Legal Theory (primary_claim_type)

| Claim Type | N decided | Strict % | Broad % |
|---|---|---|---|
| reasonable_accommodation_denial | 791 | 18.7 | 32.1 |
| disparate_treatment | 387 | 13.4 | 22.7 |
| disparate_impact | 33 | 21.2 | 45.5 |
| interference_coercion | 29 | 6.9 | 17.2 |
| retaliation | 87 | 3.4 | 17.2 |
| design_and_construction | 31 | 48.4 | 71.0 |
| reasonable_modification_denial | 24 | 8.3 | 29.2 |
| other | 55 | 5.5 | 10.9 |

### E.5 FHA Section Cited Effect

| Section | N decided | Strict % | Broad % |
|---|---|---|---|
| 3604(f)(3)(B) | 498 | 24.1 | 41.0 |
| 3604(f)(3)(A) | 7 | 0.0 | 0.0 |
| 3604(f)(3)(C) | 28 | 42.9 | 67.9 |
| NONE_SPECIFIC | 854 | 10.9 | 18.9 |

## APPENDIX F: Galanter Plaintiff-Type Analysis

### F.1 Plaintiff Type Win Rates

**All disability (full DB):**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 1217 | 13.4 | 24.0 |
| GROUP_HOME_OPERATOR | 135 | 26.7 | 44.4 |
| FAIR_HOUSING_ORG | 51 | 43.1 | 60.8 |
| GOVERNMENT | 23 | 52.2 | 82.6 |
| OTHER | 45 | 11.1 | 33.3 |

**P1:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 378 | 15.1 | 26.2 |
| GROUP_HOME_OPERATOR | 50 | 24.0 | 40.0 |
| FAIR_HOUSING_ORG | 22 | 45.5 | 59.1 |
| GOVERNMENT | 5 | 60.0 | 80.0 |
| OTHER | 20 | 15.0 | 35.0 |

**P2:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 101 | 3.0 | 12.9 |
| GROUP_HOME_OPERATOR | 11 | 36.4 | 54.5 |
| FAIR_HOUSING_ORG | 4 | 75.0 | 75.0 |
| GOVERNMENT | 2 | 0.0 | 100.0 |
| OTHER | 2 | 0.0 | 50.0 |

**P3:**
| Plaintiff Type | N decided | Strict % | Broad % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 355 | 7.9 | 14.6 |
| GROUP_HOME_OPERATOR | 23 | 21.7 | 43.5 |
| FAIR_HOUSING_ORG | 6 | 50.0 | 83.3 |
| GOVERNMENT | 4 | 75.0 | 75.0 |
| OTHER | 11 | 0.0 | 27.3 |

### F.2 Plaintiff Type × Pro Se

| Plaintiff Type | Pro Se % | PS Strict % | Rep Strict % |
|---|---|---|---|
| INDIVIDUAL_TENANT | 72.9 | 6.1 | 33.6 |
| GROUP_HOME_OPERATOR | 1.3 | 0.0 | 27.1 |
| FAIR_HOUSING_ORG | 2.7 | 100.0 | 42.0 |
| GOVERNMENT | 0.0 | None | 52.2 |
| OTHER | 30.2 | 0.0 | 15.2 |

## APPENDIX G: Circuit-Level Analysis

### G.1 Overall Win Rates by Circuit (all disability decided)

| Circuit | N decided | Strict % | Broad % |
|---|---|---|---|
| 1st Circuit | 44 | 25.0 | 29.5 |
| 2nd Circuit | 197 | 13.7 | 22.8 |
| 3rd Circuit | 163 | 12.3 | 24.5 |
| 4th Circuit | 109 | 6.4 | 18.3 |
| 5th Circuit | 105 | 20.0 | 32.4 |
| 6th Circuit | 117 | 16.2 | 25.6 |
| 7th Circuit | 112 | 26.8 | 38.4 |
| 8th Circuit | 64 | 14.1 | 26.6 |
| 9th Circuit | 311 | 16.7 | 30.9 |
| 10th Circuit | 83 | 12.0 | 27.7 |
| 11th Circuit | 110 | 16.4 | 29.1 |
| D.C. Circuit | 36 | 25.0 | 41.7 |

### G.2 MTD Broad Win Rates by Circuit

| Circuit | MTD N | MTD Broad % |
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

### G.3 Binary Pre/Post by Circuit

| Circuit | Pre N | Pre Broad % | Post N | Post Broad % | Delta pp |
|---|---|---|---|---|---|
| 1st Circuit | 29 | 31.0 | 15 | 26.7 | -4.3 |
| 2nd Circuit | 104 | 31.7 | 93 | 12.9 | -18.8 |
| 3rd Circuit | 83 | 25.3 | 80 | 23.8 | -1.5 |
| 4th Circuit | 38 | 26.3 | 71 | 14.1 | -12.2 |
| 5th Circuit | 53 | 41.5 | 52 | 23.1 | -18.4 |
| 6th Circuit | 63 | 28.6 | 54 | 22.2 | -6.4 |
| 7th Circuit | 70 | 41.4 | 42 | 33.3 | -8.1 |
| 8th Circuit | 32 | 31.2 | 32 | 21.9 | -9.3 |
| 9th Circuit | 161 | 37.9 | 150 | 23.3 | -14.6 |
| 10th Circuit | 34 | 41.2 | 49 | 18.4 | -22.8 |
| 11th Circuit | 55 | 32.7 | 55 | 25.5 | -7.2 |
| D.C. Circuit | 23 | 56.5 | 13 | 15.4 | -41.1 |

### G.4 Three-Period MTD by Circuit (P1 vs P2+P3, n≥10 both)

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

### G.5 Interactive Process Discussion Rate by Circuit

| Circuit | Total | IP Discussed | IP % |
|---|---|---|---|
| 1st Circuit | 53 | 15 | 28.3 |
| 2nd Circuit | 282 | 14 | 5.0 |
| 3rd Circuit | 181 | 6 | 3.3 |
| 4th Circuit | 146 | 12 | 8.2 |
| 5th Circuit | 148 | 15 | 10.1 |
| 6th Circuit | 146 | 20 | 13.7 |
| 7th Circuit | 138 | 17 | 12.3 |
| 8th Circuit | 95 | 6 | 6.3 |
| 9th Circuit | 386 | 47 | 12.2 |
| 10th Circuit | 123 | 14 | 11.4 |
| 11th Circuit | 142 | 19 | 13.4 |
| D.C. Circuit | 38 | 5 | 13.2 |

## APPENDIX H: Supplementary Data

### H.1 Win Rates by Procedural Posture

| Posture | N decided | Strict % | Broad % |
|---|---|---|---|
| MOTION_TO_DISMISS | 837 | 11.2 | 22.7 |
| SUMMARY_JUDGMENT | 219 | 20.1 | 44.3 |
| APPEAL | 207 | 19.8 | 31.4 |
| PRELIMINARY_INJUNCTION | 103 | 19.4 | 21.4 |
| TRIAL | 19 | 68.4 | 73.7 |
| DEFAULT_JUDGMENT | 12 | 75.0 | 75.0 |
| DISCOVERY | 6 | 0.0 | 0.0 |
| OTHER_PROCEDURAL | 57 | 17.5 | 24.6 |

**P1:**
| Posture | N decided | Strict % | Broad % |
|---|---|---|---|
| MOTION_TO_DISMISS | 288 | 13.9 | 25.7 |
| SUMMARY_JUDGMENT | 68 | 16.2 | 38.2 |
| APPEAL | 45 | 22.2 | 37.8 |
| PRELIMINARY_INJUNCTION | 33 | 27.3 | 30.3 |
| TRIAL | 11 | 63.6 | 72.7 |
| DISCOVERY | 4 | 0.0 | 0.0 |
| OTHER_PROCEDURAL | 18 | 22.2 | 27.8 |

**P2:**
| Posture | N decided | Strict % | Broad % |
|---|---|---|---|
| MOTION_TO_DISMISS | 73 | 2.7 | 17.8 |
| SUMMARY_JUDGMENT | 19 | 21.1 | 42.1 |
| APPEAL | 17 | 17.6 | 17.6 |
| PRELIMINARY_INJUNCTION | 6 | 0.0 | 0.0 |
| OTHER_PROCEDURAL | 4 | 25.0 | 25.0 |

**P3:**
| Posture | N decided | Strict % | Broad % |
|---|---|---|---|
| MOTION_TO_DISMISS | 248 | 6.9 | 13.7 |
| SUMMARY_JUDGMENT | 42 | 19.0 | 45.2 |
| APPEAL | 35 | 11.4 | 20.0 |
| PRELIMINARY_INJUNCTION | 40 | 2.5 | 5.0 |
| DEFAULT_JUDGMENT | 6 | 83.3 | 83.3 |
| OTHER_PROCEDURAL | 22 | 9.1 | 18.2 |

### H.2 Win Rates by Housing Type

| Housing Type | N decided | Strict % | Broad % |
|---|---|---|---|
| PRIVATE_MARKET | 588 | 19.4 | 33.0 |
| PUBLIC_HOUSING | 107 | 4.7 | 18.7 |
| OTHER_SUBSIDIZED | 60 | 16.7 | 30.0 |
| UNDETERMINED | 152 | 6.6 | 13.2 |

### H.3 Loper Bright Citation

  All disability: 6 cases cite Loper Bright
  P1: 0 cases cite Loper Bright
  P2: 0 cases cite Loper Bright
  P3: 6 cases cite Loper Bright

### H.4 Delay-as-Denial

Delay-as-denial invoked: 72 cases (3.8%)
  DaD strict win: 37.9% (n=66)
  No DaD strict win: 15.1% (n=1405)
  DaD broad win: 65.2% (n=66)
  No DaD broad win: 26.6% (n=1405)

### H.5 Interactive Process + Delay-as-Denial

IP discussed: 200, of which DaD also invoked: 59 (29.5%)
  Combined IP+DaD strict: 43.4% (n=53)
  Combined IP+DaD broad: 69.8% (n=53)

### H.6 Pro Se × Defendant Type Cross-Tab

| Defendant | PS N dec | PS Strict | PS Broad | Rep N dec | Rep Strict | Rep Broad |
|---|---|---|---|---|---|---|
| DEVELOPER | 3 | 0.0 | 0.0 | 14 | 50.0 | 78.6 |
| HOA_CONDO_ASSN | 60 | 6.7 | 21.7 | 82 | 40.2 | 54.9 |
| PRIVATE_LANDLORD | 282 | 9.9 | 18.1 | 125 | 42.4 | 64.0 |
| MUNICIPALITY | 67 | 3.0 | 4.5 | 161 | 22.4 | 44.7 |
| PROPERTY_MANAGEMENT | 178 | 5.6 | 12.9 | 63 | 46.0 | 71.4 |
| OTHER | 109 | 4.6 | 9.2 | 40 | 17.5 | 32.5 |
| HOUSING_AUTHORITY | 157 | 4.5 | 12.7 | 46 | 15.2 | 39.1 |
| GOVERNMENT | 37 | 0.0 | 0.0 | 19 | 26.3 | 31.6 |
| LENDER | 3 | 0.0 | 0.0 | 1 | 100.0 | 100.0 |

## APPENDIX A-3: Extended Empirical Analysis (Key Cross-Tabs)

### A3.1 Procedural Posture × Period


**MOTION_TO_DISMISS:**
| Period | N decided | Strict % | Broad % |
|---|---|---|---|
| P1 | 288 | 13.9 | 25.7 |
| P2 | 73 | 2.7 | 17.8 |
| P3 | 248 | 6.9 | 13.7 |

**SUMMARY_JUDGMENT:**
| Period | N decided | Strict % | Broad % |
|---|---|---|---|
| P1 | 68 | 16.2 | 38.2 |
| P2 | 19 | 21.1 | 42.1 |
| P3 | 42 | 19.0 | 45.2 |

**APPEAL:**
| Period | N decided | Strict % | Broad % |
|---|---|---|---|
| P1 | 45 | 22.2 | 37.8 |
| P2 | 17 | 17.6 | 17.6 |
| P3 | 35 | 11.4 | 20.0 |

### A3.2 Interactive Process × Defendant Type

| Defendant Type | IP Cases | Total | IP % | IP Broad % | No-IP Broad % |
|---|---|---|---|---|---|
| HOA_CONDO_ASSN | 43 | 180 | 23.9 | 65.8 | 31.7 |
| PRIVATE_LANDLORD | 54 | 537 | 10.1 | 54.9 | 28.7 |
| MUNICIPALITY | 28 | 273 | 10.3 | 40.7 | 31.8 |
| PROPERTY_MANAGEMENT | 24 | 319 | 7.5 | 54.5 | 25.7 |
| HOUSING_AUTHORITY | 37 | 253 | 14.6 | 32.4 | 16.0 |

### A3.3 State-Level Win Rates (n≥20 decided)

| State | N decided | Strict % | Broad % |
|---|---|---|---|
| DC | 25 | 36.0 | 56.0 |
| TN | 26 | 34.6 | 50.0 |
| IL | 53 | 34.0 | 45.3 |
| LA | 30 | 33.3 | 46.7 |
| IN | 40 | 30.0 | 42.5 |
| WA | 25 | 28.0 | 36.0 |
| FL | 69 | 23.2 | 37.7 |
| OK | 29 | 20.7 | 31.0 |
| MA | 25 | 20.0 | 24.0 |
| AZ | 39 | 17.9 | 33.3 |
| MI | 29 | 17.2 | 20.7 |
| OR | 53 | 17.0 | 35.8 |
| CA | 139 | 15.8 | 29.5 |
| TX | 69 | 14.5 | 24.6 |
| NV | 21 | 14.3 | 19.0 |
| NJ | 58 | 13.8 | 32.8 |
| NY | 186 | 12.9 | 21.0 |
| PA | 98 | 11.2 | 22.4 |
| OH | 52 | 7.7 | 17.3 |
| AL | 28 | 7.1 | 17.9 |
| MD | 60 | 6.7 | 23.3 |
| VA | 21 | 4.8 | 14.3 |