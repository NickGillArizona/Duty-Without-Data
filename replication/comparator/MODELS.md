# Models

All estimates are machine-classified and APPENDIX-READY only. Thin P2 cells are descriptive; do not significance-chase. All cells are document-level archive output; the current manuscript prints no decline or composition-share components from this module (the reported Part II series is the case-level census in `results/series_2026-07.json`, on which no aggregate trend is asserted).

## Kitagawa Decomposition
| arm | n_p1 | n_p3 | strict_p1 | strict_p3 | decline | comp_share_avg | tag |
|---|---|---|---|---|---|---|---|
| DIS | 383 | 314 | 21.1% | 11.8% | 9.4% | 57.5% | APPENDIX-READY |
| RD-PURE | 170 | 141 | 28.8% | 10.6% | 18.2% | 42.6% | APPENDIX-READY |
| DT-PURE | 78 | 53 | 10.3% | 15.1% | -4.8% | NA | APPENDIX-READY |
| RACE-DT | 138 | 71 | 8.7% | 5.6% | 3.1% | 17.2% | APPENDIX-READY |
| NONDIS | 325 | 219 | 10.5% | 5.0% | 5.4% | 44.1% | APPENDIX-READY |

## within_disability_rd_vs_dt

Formula: `strict_win ~ C(period, Treatment(reference="P1")) * C(bucket2, Treatment(reference="DT-PURE")) * pro_se_int`

Warning: Quasi-separation or thin-cell instability likely; interpret interaction coefficients as directional diagnostics only.

| term | OR | OR_CI | p |
|---|---|---|---|
| Intercept | 0.500 | [0.188, 1.332] | 0.166 |
| C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 1.357 | [0.469, 3.929] | 0.573 |
| C(period, Treatment(reference="P1"))[T.P2]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 0.421 | [0.024, 7.285] | 0.552 |
| C(period, Treatment(reference="P1"))[T.P3]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 0.340 | [0.066, 1.756] | 0.198 |
| pro_se_int | 0.069 | [0.012, 0.384] | 0.002 |
| C(period, Treatment(reference="P1"))[T.P2]:pro_se_int | 3.412 | [0.110, 106.140] | 0.484 |
| C(period, Treatment(reference="P1"))[T.P3]:pro_se_int | 0.382 | [0.023, 6.442] | 0.504 |
| C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 3.616 | [0.553, 23.642] | 0.180 |
| C(period, Treatment(reference="P1"))[T.P2]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 0.000 | [0.000, 0.000] | 0.000 |
| C(period, Treatment(reference="P1"))[T.P3]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 0.683 | [0.027, 17.052] | 0.816 |

## cross_class_dis_vs_race_dt

Formula: `strict_win ~ C(period, Treatment(reference="P1")) * C(cohort2, Treatment(reference="RACE-DT")) * pro_se_int`

Warning: Quasi-separation or thin-cell instability likely; interpret interaction coefficients as directional diagnostics only.

| term | OR | OR_CI | p |
|---|---|---|---|
| Intercept | 0.182 | [0.076, 0.434] | 0.000 |
| C(cohort2, Treatment(reference="RACE-DT"))[T.DIS] | 2.920 | [1.159, 7.361] | 0.023 |
| C(period, Treatment(reference="P1"))[T.P2]:C(cohort2, Treatment(reference="RACE-DT"))[T.DIS] | 0.707 | [0.064, 7.826] | 0.777 |
| C(period, Treatment(reference="P1"))[T.P3]:C(cohort2, Treatment(reference="RACE-DT"))[T.DIS] | 2550515354.426 | [0.000, 0.000] | NA |
| pro_se_int | 0.214 | [0.051, 0.909] | 0.037 |
| C(period, Treatment(reference="P1"))[T.P2]:pro_se_int | 0.000 | [0.000, 0.000] | 0.000 |
| C(period, Treatment(reference="P1"))[T.P3]:pro_se_int | 1907080225.254 | [0.000, 0.000] | NA |
| C(cohort2, Treatment(reference="RACE-DT"))[T.DIS]:pro_se_int | 0.914 | [0.193, 4.334] | 0.910 |
| C(period, Treatment(reference="P1"))[T.P2]:C(cohort2, Treatment(reference="RACE-DT"))[T.DIS]:pro_se_int | 168360772.914 | [5874763.707, 4824934460.546] | 0.000 |
| C(period, Treatment(reference="P1"))[T.P3]:C(cohort2, Treatment(reference="RACE-DT"))[T.DIS]:pro_se_int | 0.000 | [0.000, 0.000] | NA |

## within_disability_sensitivity_mixed_as_rd

Formula: `strict_win ~ C(period, Treatment(reference="P1")) * C(bucket2, Treatment(reference="DT-PURE")) * pro_se_int`

| term | OR | OR_CI | p |
|---|---|---|---|
| Intercept | 0.500 | [0.188, 1.332] | 0.166 |
| C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 1.161 | [0.412, 3.272] | 0.777 |
| C(period, Treatment(reference="P1"))[T.P2]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 0.765 | [0.058, 10.103] | 0.839 |
| C(period, Treatment(reference="P1"))[T.P3]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 0.311 | [0.065, 1.503] | 0.146 |
| pro_se_int | 0.069 | [0.012, 0.384] | 0.002 |
| C(period, Treatment(reference="P1"))[T.P2]:pro_se_int | 3.412 | [0.110, 106.140] | 0.484 |
| C(period, Treatment(reference="P1"))[T.P3]:pro_se_int | 0.382 | [0.023, 6.442] | 0.504 |
| C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 3.257 | [0.522, 20.307] | 0.206 |
| C(period, Treatment(reference="P1"))[T.P2]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 0.168 | [0.003, 10.299] | 0.395 |
| C(period, Treatment(reference="P1"))[T.P3]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 1.943 | [0.095, 39.709] | 0.666 |

## within_disability_sensitivity_mixed_as_dt

Formula: `strict_win ~ C(period, Treatment(reference="P1")) * C(bucket2, Treatment(reference="DT-PURE")) * pro_se_int`

Warning: Quasi-separation or thin-cell instability likely; interpret interaction coefficients as directional diagnostics only.

| term | OR | OR_CI | p |
|---|---|---|---|
| Intercept | 0.449 | [0.272, 0.742] | 0.002 |
| C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 1.511 | [0.789, 2.896] | 0.213 |
| C(period, Treatment(reference="P1"))[T.P2]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 0.321 | [0.048, 2.150] | 0.242 |
| C(period, Treatment(reference="P1"))[T.P3]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE] | 0.713 | [0.223, 2.275] | 0.567 |
| pro_se_int | 0.124 | [0.047, 0.324] | 0.000 |
| C(period, Treatment(reference="P1"))[T.P2]:pro_se_int | 1.570 | [0.215, 11.468] | 0.657 |
| C(period, Treatment(reference="P1"))[T.P3]:pro_se_int | 1.451 | [0.365, 5.763] | 0.597 |
| C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 2.016 | [0.591, 6.878] | 0.263 |
| C(period, Treatment(reference="P1"))[T.P2]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 0.000 | [0.000, 0.000] | 0.000 |
| C(period, Treatment(reference="P1"))[T.P3]:C(bucket2, Treatment(reference="DT-PURE"))[T.RD-PURE]:pro_se_int | 0.180 | [0.023, 1.418] | 0.103 |

## Power / Thin-Cell Notes

| cell | n | rough_mde_two_group_pp_at_p15 | note |
|---|---|---|---|
| DT-PURE P2 decided | 23 | 0.29482492962847423 | Normal-approximation rough MDE for context only; do not significance-chase thin cells. |
| RACE-DT P2 decided | 37 | 0.23244877378130524 | Normal-approximation rough MDE for context only; do not significance-chase thin cells. |
| RACE-DT P2 dated | 42 | 0.2181742422927143 | Normal-approximation rough MDE for context only; do not significance-chase thin cells. |
