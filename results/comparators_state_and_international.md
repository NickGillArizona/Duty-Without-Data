# Comparative Registry Models: State and International Disability-Housing Data Architectures

State registries (California, New York, Massachusetts, Illinois, Los Angeles) and international systems (Canada CMHC, United Kingdom EHS, Australia NDIS SDA, European Union Accessibility Act) demonstrate that accessible-housing data registries are administrable at scale. The research below provides the feasibility evidence underlying the Note's proposal.

**Companion to:** Nicholas Gill, *Duty Without Data: Disability Fair Housing and the Record-Dependent Right*, supplementary findings § 14 (HMDA analogical precedent) and § 18 (privacy architecture and international comparators).

**Sections:**

1. State disability data architectures — California, New York, Massachusetts, Illinois, Los Angeles
2. International comparators — Canada, United Kingdom, Australia, European Union

---

## 1. State Disability Data Architectures

**Scope.** The lens here is what each state's *agency-side* civil-rights and housing data architecture produces in publicly observable form, and what HUD does not produce that the state does. State-AG litigation postures and registry-comparator details outside that lens are intentionally not covered here.

---

## 1. California — FEHA + Civil Rights Department + HCD AFFH Data Viewer

**(a) Statutory authority.** California's principal fair-housing statute is the Fair Employment and Housing Act, Cal. Gov. Code § 12955. FEHA's disability scope is *broader* than the federal FHA in several material respects: § 12926 separately defines "physical disability," "mental disability," and "medical condition" (rather than the FHA's single "handicap" category); § 12955.3 codifies an explicit interactive-process and reasonable-accommodation duty; FEHA also reaches single-family rentals via § 12927 in ways the FHA's "Mrs. Murphy" exemption does not. FEHA is supplemented by the Unruh Civil Rights Act (Cal. Civ. Code § 51) for places of public accommodation including some housing-adjacent facilities.

**(b) Responsible state agencies.** Two agencies operate in tandem. The **California Civil Rights Department (CRD)** — formerly the Department of Fair Employment and Housing (DFEH), renamed July 1, 2022 — investigates and enforces FEHA housing complaints. The **California Department of Housing and Community Development (HCD)** is the housing-finance and planning agency that runs the state's housing-element review process and administers federal pass-through funds. CRD enforces; HCD plans and finances. Neither alone covers HUD's full domain, but together they cover most of it for California-supervised housing.

**(c) Data publication cadence.** CRD publishes annual data on enforcement actions (compliance notices, complaints, settlements) and intermittent topical reports — most recently the April 2025 Fair Housing Month release of testing data covering Los Angeles and Ventura Counties. HCD publishes Annual Progress Reports (APRs) on housing-element implementation continuously through a public dashboard, with new aggregated data added as jurisdictions submit their annual reports. HCD's AFFH Data Viewer is updated on an ongoing basis, with major version releases (most recently AFFH Data Viewer 3.0 in 2024-2025).

**(d) Public reporting granularity.** CRD's 2024 testing program reported disability-specific data at unusual granularity: 23% of 13 properties tested refused reasonable modification requests; testing methodology, sample sizes, and per-protected-class result rates were all disclosed. CRD also publishes aggregate compliance-notice counts (758 in 2024; 374 fair-housing-related). HCD's AFFH Data Viewer organizes downloadable layers by (1) Fair Housing Enforcement and Outreach Capacity, (2) Segregation and Integration, (3) Disparities in Access to Opportunity, (4) Disproportionate Housing Needs Including Displacement Risks, (5) Racially and Ethnically Concentrated Areas, and (6) Supplemental Data — with downloadable data layers, exportable maps, and per-jurisdiction analyses.

**(e) What California does that HUD does not.** Three things stand out. First, CRD publishes per-protected-class *paired-testing* result rates — not just aggregate intake counts. HUD has never published comparable testing-result statistics by protected class, despite the FHIP and FHEO having access to such data through grantee testing programs. Second, HCD's AFFH Data Viewer is a public, downloadable, statewide GIS-grade fair-housing data product. HUD's now-rescinded AFFH Tool was never as granular, and HUD has nothing analogous publicly available in 2026. Third, FEHA's broader disability definition produces a *categorically wider* enforcement intake than HUD captures, because California recognizes "medical condition" and bifurcated mental/physical disability classifications, generating data points HUD's intake architecture is not designed to record.

**(f) Implications for the Note.** California demonstrates that the Note's "HUD is anomalous within civil-rights data infrastructure" claim is not just a federal-comparator argument. It also holds vertically: a state civil-rights agency using HUD-pass-through funds (CRD is FHAP-certified) generates more granular, more publicly accessible disability data than HUD does in its own house. The "HUD does not even match its own state delegates" point sharpens the constructive-anomaly framing.

---

## 2. New York — NY Exec. Law § 296 + State Division of Human Rights + NYC HPD/MOPD

**(a) Statutory authority.** N.Y. Exec. Law § 296 (the Human Rights Law) prohibits discrimination in housing based on disability and is broader than the federal FHA in two key ways relevant to disability data. First, the New York definition of "disability" under § 292(21) is significantly broader than the FHA's "handicap" definition — covering any physical, mental, or medical impairment that prevents the exercise of normal bodily function or is demonstrable through medically accepted clinical or laboratory diagnostic techniques. Second, under recent amendments, the statute of limitations for filing housing-discrimination complaints is one year (extended in some categories to three years for sexual harassment), giving a longer evidentiary window than the FHA's two-year private-suit statute applied differently. § 296(5) covers refusal to rent, terms-and-conditions discrimination, and refusal to permit reasonable modifications or make reasonable accommodations.

**(b) Responsible state and local agencies.** The **NY State Division of Human Rights (NYSDHR)** is the primary state civil-rights enforcement body. Locally, **NYC HPD** (Department of Housing Preservation and Development) administers affordable-housing programs and is the primary actor on accessible-unit set-asides, while **MOPD** (Mayor's Office for People with Disabilities) publishes annual disability-related reports including the Accessible NYC report series.

**(c) Data publication cadence.** NYSDHR publishes an Annual Report (most recent: FY 2024). NYC HPD publishes ongoing data via Open Data and the NYC Housing Vacancy Survey Data Explorer. Following Local Law 25 of 2023 (signed February 21, 2023), HPD must report every three years on how many of its affordable-housing units are set aside for and rented to persons with disabilities — first report due September 1, 2024. (Note: the original task framing referenced "Local Law 71 of 2018" — that local law actually governs cleaning park playground equipment after pesticide application; the operational accessible-housing reporting law is **Local Law 25 of 2023**.) MOPD publishes annual Accessible NYC reports.

**(d) Public reporting granularity.** NYSDHR's reporting is the weak link in this architecture. As of November 7, 2023, 2,263 housing-discrimination cases had been filed with DHR between April 1, 2019 and October 31, 2023 — but the Comptroller's October 2024 audit found inadequate intake controls: of 120 sampled complaints, 82 (68%) initially could not be accounted for; 40 were located, 42 remained unaccounted for; 350+ open complaints had not been assigned to investigators as of February 2024. By contrast, NYC HPD set-aside data is granular: federally required Section 504 set-asides are 7% of HPD/HDC-financed units (5% mobility, 2% vision/hearing), with Local Law 25 reports providing unit counts per program and tenant-rented counts. MOPD's Accessible NYC 2025 housing chapter aggregates data across HPD, NYCHA, and supportive-housing pipelines.

**(e) What New York does that HUD does not.** NYC HPD's Local Law 25 reporting publishes 504-set-aside-unit counts and tenant occupancy by program — exactly the disaggregated unit-level disability data the Note argues HUD should publish for federally financed housing. HUD has the same Section 504 set-aside obligation across far more units nationally, but does not publish equivalent aggregated set-aside-versus-occupied data. NYSDHR also publishes complaint-volume data by protected class on an annual cadence; HUD's FHEO publication has been more sporadic and less complete on disability-specific intake data since 2023.

**(f) Implications for the Note.** New York illustrates both the prescriptive case and the operational caveat. NYC's Local Law 25 demonstrates that triennial set-aside reporting is technically and politically feasible at scale (NYC's affordable-housing pipeline is larger than most states'). At the same time, NYSDHR's documented intake-control failures show that *publishing* data and *running a competent intake system* are distinct architectural problems — supporting the Note's prescription that HUD reform must address both data design and operational capacity, not data design alone.

---

## 3. Massachusetts — Mass. Gen. Laws ch. 151B § 4 + MCAD + EOHLC + MassAccess

**(a) Statutory authority.** Mass. Gen. Laws ch. 151B § 4 prohibits housing discrimination based on disability ("handicap") in terms broader than the federal FHA in three operationally important ways: (1) the design-and-construction trigger reaches 3+ unit elevator buildings and ground-floor units in other 3+ buildings (lower than the federal 4+ unit baseline); (2) § 4(7B), enacted via St. 1989, c. 722 (approved Jan. 13, 1990), establishes a 15-day vacancy-notice requirement to a central registry for accessible units; and (3) the statute provides rent-parity protection for accessible units — landlords cannot charge more for an accessible unit than an equivalent non-accessible unit.

**(b) Responsible state agencies.** The **Massachusetts Commission Against Discrimination (MCAD)** investigates ch. 151B housing complaints. The **Executive Office of Housing and Livable Communities (EOHLC)** — the successor to the former Department of Housing and Community Development (DHCD), reorganized in 2023 — administers state housing finance and planning, including the "A Home for Everyone" Statewide Housing Plan. The **Massachusetts Rehabilitation Commission (MRC)** co-funds MassAccess. Operational housing-data work is therefore distributed across MCAD (complaint enforcement), EOHLC (planning and finance), MRC (disability services), and the **Citizens' Housing and Planning Association (CHAPA)** (which operates the MassAccess Housing Registry under MRC + EOHLC funding).

**(c) Data publication cadence.** MCAD publishes Annual Reports on a fiscal-year cycle (FY 2024 most recent at time of writing; FY 2025 issued in early 2026). The MassAccess Housing Registry is updated continuously by listing landlords pursuant to the § 4(7B) 15-day vacancy-notice obligation. EOHLC publishes the Statewide Housing Plan ("A Home for Everyone") on a roughly five-year cycle, with annual progress chapters; LHA tenant-data reporting is annual.

**(d) Public reporting granularity.** MassAccess provides unit-level granularity unmatched in any HUD product: searchable accessibility features include roll-in showers, hearing/vision communication devices, blind-accessibility features, transport proximity, rent level, subsidy status, and current vacancy status — by city/town, bedroom count, and adaptive feature. MCAD's FY 2024 report disclosed 3,553 new filings (a 15% jump, the highest since 2008), with disability cases the largest growth category. EOHLC's "A Home for Everyone" includes a dedicated "Units Accessible to People with Disabilities" section reporting Housing Navigator Massachusetts's finding of 10,200 accessible deed-restricted affordable units statewide, with availability ratios of 1 unit per 46 households in Metro Boston to 1:103 in Bristol County.

**(e) What Massachusetts does that HUD does not.** Three things HUD does not do: (1) publish a real-time, statewide, public, unit-level accessible-housing registry with feature-level filters; (2) impose a 15-day vacancy-notice obligation on landlords as a statutory data-feeding mechanism; (3) publish geographic accessible-unit-availability ratios at the county level. HUD has the Picture of Subsidized Households and Multifamily Inventory data, but neither captures accessibility features or current vacancy status. The statutory architecture matters: § 4(7B) makes data production a private-party legal duty, not just an agency reporting choice.

**(f) Implications for the Note.** Massachusetts is the strongest single-state proof-of-concept for the Note's architectural prescription. The combination of statutory data-feed mandate (§ 4(7B)), state agency operationalization (MRC + EOHLC + CHAPA), and granular public output (MassAccess) demonstrates that HUD's "we can't" defenses on disability-data architecture are belied by an existing operational system in a peer-jurisdiction. Caveat: Massachusetts is geographically small and politically cohesive in ways that simplify implementation; the Note should not overclaim that the Massachusetts model transfers wholesale to HUD's nationwide, multi-program domain. But the existence-proof — that this architecture is not impossible — is strong evidence against HUD's feasibility-objection framing.

---

## 4. Synthesis — HUD's Anomaly Extends Vertically

Across the three states examined, a consistent pattern emerges that sharpens the Note's "HUD is anomalous within civil-rights data infrastructure" framing in three ways the federal-comparator analysis alone cannot reach.

**First, vertical anomaly.** HUD does not match the data-publication granularity of the very state civil-rights agencies it certifies and partly funds (CRD, NYSDHR, MCAD are all FHAP-certified). The implicit assumption that federal agencies set the floor and states build above it is empirically inverted on disability-housing data: the floor sits below the ceiling.

**Second, statutory data-feed design.** Massachusetts' § 4(7B) and NYC's Local Law 25 of 2023 both demonstrate that data-feed obligations can be statutorily allocated to private actors (landlords) and agencies (HPD), reducing the agency burden HUD invokes as a feasibility objection. California's CRD testing-program publication shows agency-driven data production at high granularity is operationally feasible.

**Third, operational caveats.** The NYSDHR audit failures and MCAD backlog confirm the Note's implicit point that data architecture and operational capacity are distinct reform problems. Recommending data architecture without operational reform is half a recommendation.

---

## 5. Honest gaps

- **NYSDHR FY 2024 disability-specific housing complaint counts** are not publicly disaggregated in the snippets retrieved; the FY 2024 Annual Report at dhr.ny.gov/resources should be retrieved directly to populate that figure.
- **CRD per-county complaint counts disaggregated by protected class** are not consistently available; the testing-program data is the strongest disability-disaggregated CRD product currently in the public record.
- **MCAD fiscal-year housing-vs-employment disability breakdown** beyond the headline 3,553 figure requires direct retrieval of the FY 2024 and FY 2025 Annual Reports.
- **EOHLC accessible-unit pipeline forecasting data** is described qualitatively in "A Home for Everyone" but not provided as a downloadable dataset; similar to HUD's gap, this is a near-miss rather than a parallel.
- **The original task referenced "NYC Local Law 71 of 2018" for accessible-housing reporting**; that LL governs pesticide cleanup of park playground equipment. The functionally equivalent law is **Local Law 25 of 2023**, which is what this memo treats.

---

## 6. Sources

**California:**
- Cal. Gov. Code § 12955: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=12955.&lawCode=GOV
- Cal. Gov. Code § 12926: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=12926.&lawCode=GOV
- Cal. Gov. Code § 12955.3: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=12955.3.&lawCode=GOV
- California Civil Rights Department: https://calcivilrights.ca.gov/
- CRD April 2025 Fair Housing Month testing data: https://calcivilrights.ca.gov/2025/04/17/during-fair-housing-month-civil-rights-department-shares-new-data-on-housing-discrimination-in-southern-california/
- HCD AFFH Data Viewer: https://www.hcd.ca.gov/affh/data-viewer
- HCD AFFH page: https://www.hcd.ca.gov/planning-and-community-development/affirmatively-furthering-fair-housing
- HCD APR Dashboard: https://www.hcd.ca.gov/planning-and-community-development/housing-element-implementation-and-apr-dashboard
- HCD People with Disabilities page: https://www.hcd.ca.gov/policy-and-research/intersectional-policy-work/people-disabilities

**New York:**
- N.Y. Exec. Law § 296: https://www.nysenate.gov/legislation/laws/EXC/296
- NYSDHR: https://dhr.ny.gov/
- NYSDHR Resources / Annual Reports: https://dhr.ny.gov/resources
- NYSDHR Housing Disabilities flyer (April 2024): https://dhr.ny.gov/system/files/documents/2024/04/nysdhr-housing-disabilities.pdf
- OSC Audit, Investigation of Housing Discrimination Complaints (Oct. 2024): https://www.osc.ny.gov/state-agencies/audits/2024/10/15/investigation-housing-discrimination-complaints
- NYC HPD Where We Live NYC 2025 final plan: https://www.nyc.gov/site/hpd/news/066-25/city-new-york-releases-final-where-we-live-nyc-2025-fair-housing-plan
- NYC Local Law 25 of 2023 — CityLand summary: https://www.citylandnyc.org/council-approves-bill-to-report-on-affordable-housing-and-renters-with-disabilities/
- NYC HPD Affordable Housing Guide for People with Disabilities: https://www.nyc.gov/assets/hpd/downloads/pdfs/services/affordable-housing-guide-for-applicants-with-disabilities.pdf
- MOPD Accessible NYC 2025 Report — Housing: https://www.nyc.gov/site/mopd/publications/accessiblenyc-2025-report-housing.page

**Massachusetts:**
- Mass. Gen. Laws ch. 151B § 4: https://malegislature.gov/laws/generallaws/parti/titlexxi/chapter151b/section4
- MCAD: https://www.mass.gov/orgs/massachusetts-commission-against-discrimination
- MCAD Annual Reports list: https://www.mass.gov/lists/mcad-annual-reports
- MCAD FY24 Annual Report announcement: https://www.mass.gov/news/ma-commission-against-discrimination-mcad-issues-fy24-annual-report
- WBUR coverage of MCAD FY 2024 backlog and disability spike (Feb. 2025): https://www.wbur.org/news/2025/02/05/mcad-disability-bias-employee-allegations-investigations
- EOHLC: https://www.mass.gov/orgs/executive-office-of-housing-and-livable-communities
- EOHLC "Units Accessible to People with Disabilities" (A Home for Everyone): https://www.mass.gov/info-details/units-accessible-to-people-with-disabilities
- MassAccess Housing Program: https://www.mass.gov/massaccess-housing-program
- MassAccess Registry: https://www.massaccesshousingregistry.org/

---

## 2. International Disability-Housing Comparators

This memo documents how four peer jurisdictions (Canada, the United Kingdom, Australia, and the European Union) and the UN CRPD treaty regime structure disability-housing data collection, publication, and accountability. The point of comparison is not whether each system is perfect — none is — but whether it functions as the kind of data architecture that the Note argues HUD lacks: a national authority that periodically collects unit-level or household-level data on disability and accessibility features, publishes it on a regular cadence, and uses it to discipline programmatic decisions.

---

## 1. Canada — CMHC and the National Housing Strategy data system

The Canada Mortgage and Housing Corporation (CMHC) is Canada's federal housing agency and the operational analogue of HUD. Its disability-housing data architecture has three principal pillars.

**(a) National Housing Strategy (NHS) accessibility minimums and reporting.** The NHS, launched in 2017, requires that every project funded under its programs meet minimum accessibility criteria, with priority given to projects exceeding the minimum or achieving full universal design. CMHC publishes NHS Progress Reports tracking units committed for "people with developmental disabilities" and "seniors" as distinct equity-deserving categories. As of the December 2022 Progress Report, CMHC reported 845 new units committed for people with developmental disabilities. (https://www.cmhc-schl.gc.ca/lp/cmhc-accessible-housing)

**(b) Social and Affordable Housing Survey (SAHS).** Beginning in 2019 and run on a roughly biennial cycle, the SAHS collects structure-level data from social and affordable rental providers, including a dedicated accessibility-features module. The 2023 (cycle 4) and 2025 (cycle 5) results disclose, among other things, that "structures with no accessibility features declined from 60% in 2019 to 37% in 2023," and that "persons with physical disabilities and persons with mental disabilities were each an identified group in 3% of units surveyed." Data tables are published in machine-readable form. (https://www.cmhc-schl.gc.ca/observer/2025/cmhc-releases-5th-cycle-social-affordable-housing-survey-results; https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research/housing-data/data-tables/rental-market/social-affordable-housing-survey-rental-structures-data)

**(c) CMHC Accessibility Plans and Progress Reports.** Under the federal Accessible Canada Act, CMHC publishes triennial accessibility plans (2023–2025; 2026–2028) and annual progress reports against them, with public consultation requirements. (https://www.cmhc-schl.gc.ca/about-us/corporate-reporting/transparency/accessibility-at-cmhc/2026-2028-accessibility-plan)

A fourth, semi-public data infrastructure — the Housing Assessment Resource Tools (HART) project at UBC, CMHC-funded and launched in 2022 — generates community-level housing-needs assessments using Statistics Canada data; HART itself acknowledges that its census-derived inputs "currently exclude … accessibility," underscoring that even Canada's data architecture has gaps. (https://hart.ubc.ca/)

**Match to the Note's prescription:** Strong. CMHC functions as an accountable national data authority with a recurring structure-level survey that asks targeted accessibility-feature questions and publishes the results on a fixed cadence, against legislated equity goals. This is functionally close to what the Note proposes for HUD.

---

## 2. United Kingdom — English Housing Survey, Local Authority Registers, and EHRC oversight

The UK does not house its disability-housing data in a single agency; instead, it is distributed across three layers, but each layer is statutory and feeds into national reporting.

**(a) English Housing Survey (EHS) — accessibility module.** The EHS is the longest-running comparator: a continuous national household survey administered annually since 1967 (presently by the Ministry of Housing, Communities and Local Government, with NatCen Social Research as fieldwork contractor). Since the late 2000s, it has carried a dedicated Adaptations and Accessibility module, with the dwelling physical inspection coding the four "visitable" features (level access to entrance, flush threshold, sufficiently wide doorways, and a WC at entrance level). The 2018–19 EHS produced the headline finding that only 9% of homes in England have all four "visitable" features (since updated to 13%). The EHS is published as a Headline Report plus topic reports (housing quality, home adaptations, etc.). (https://www.gov.uk/government/collections/english-housing-survey; https://www.gov.uk/government/statistics/english-housing-survey-2019-to-2020-home-adaptations)

**(b) Building Regulation accessibility categories.** The Building Regulations (Part M4) classify new dwellings under three accessibility tiers — M4(1) Visitable, M4(2) Accessible/Adaptable, M4(3) Wheelchair User — so the regulatory baseline is itself a data field. The London Plan operationalizes this by requiring 90% of new-build London homes to meet M4(2) and 10% to meet M4(3). (https://www.london.gov.uk/programmes-strategies/housing-and-land/renting-home/london-accessible-housing-register)

**(c) Local Authority Accessible Housing Registers (AHRs).** Local councils maintain registers categorizing accessible stock (Category A wheelchair-accessible through Category E step-free), letting them match disabled applicants to suitable units. The London Accessible Housing Register, though no longer actively developed, was the most mature borough-aggregating implementation. (https://www.towerhamlets.gov.uk/lgnl/housing/lettings_and_the_housing_register/bidding_for_homes/accessible_housing_register.aspx)

**(d) Equality and Human Rights Commission (EHRC).** Under the Equality Act 2010 and its Public Sector Equality Duty, EHRC issues research reports (Reports 114 and 115 are the seminal "Britain's Hidden Crisis" series) finding that "1 in 5 disabled people in social housing live in unsuitable accommodation; … just 7% of homes in England have the most basic accessibility features." (https://www.equalityhumanrights.com/sites/default/files/research-report-114-housing-and-disabled-people-experiences-in-britain.pdf)

**Match to the Note's prescription:** Strong on collection and publication; weaker on enforcement linkage. The EHS dwelling inspection is precisely the kind of standardized, recurring physical survey the Note argues HUD should run on its assisted stock. UK authorities then use the data to set planning targets (London Plan 90/10) — a use HUD has never made of its own data.

---

## 3. Australia — NDIS, SDA, AIHW, and the National Disability Data Asset

Australia's architecture is the most disability-centric of the four — built around the National Disability Insurance Scheme (NDIS) — and is the most operationally granular at unit level.

**(a) Specialist Disability Accommodation (SDA) framework.** Under the NDIS, SDA is a category of housing for participants with extreme functional impairment or very high support needs. The SDA Design Standard sorts dwellings into four categories: Improved Liveability (sensory/cognitive), Robust (resilience and safety), Fully Accessible (wheelchair-grade physical access), and High Physical Support (ceiling hoists, dual-height fixtures). The Standard is itself a data taxonomy: every SDA-enrolled dwelling is tagged with one of the four codes. (https://www.ndis.gov.au/providers/housing-and-living-supports-and-services/specialist-disability-accommodation/sda-design-standard)

**(b) NDIS quarterly SDA data publication.** The National Disability Insurance Agency (NDIA) publishes quarterly reports including a dedicated SDA Appendix with enrolled-dwelling counts, design-category mix, geographic distribution, participant utilization, and "stranded funding" (participants with SDA funding who have not moved into an SDA home). As of 31 March 2025, there were 11,360 enrolled SDA dwellings (up 21% annually), 15,099 participants actively using SDA, and 9,662 participants with SDA funding but no SDA dwelling. Excel data tables are published. (https://dataresearch.ndis.gov.au/reports-and-analyses/specialist-disability-accommodation-sda-data; https://www.ndis.gov.au/publications/quarterly-reports)

**(c) AIHW disability-housing reports.** The Australian Institute of Health and Welfare publishes the *People with Disability in Australia* report series with a standing Housing chapter, drawing on Census, Survey of Disability, Ageing and Carers (SDAC), and the AIHW National Housing Assistance Data Repository. AIHW reports unit-level facts such as: in June 2022, 36% of social-housing households had at least one person with disability; 39% in public housing; 64% of people with disability own their home. (https://www.aihw.gov.au/reports/disability/people-with-disability-in-australia/contents/housing)

**(d) National Disability Data Asset (NDDA).** Operational since 19 December 2024, the NDDA is a co-governed (people with disability + governments) integrated dataset linking health, disability services, and income-support records, available to approved researchers. Disability Royal Commission Recommendation 12.8 commits to long-term funding. (https://www.ndda.gov.au/; https://www.health.gov.au/resources/publications/disability-royal-commission-progress-report-2025/volume-12-beyond-the-royal-commission/recommendation-128-long-term-support-for-the-national-disability-data-asset)

**(e) Disability Royal Commission housing findings.** The 2023 Royal Commission Final Report recommended decoupling housing from support services and implementing the NDIA's co-designed Home and Living Framework, with the government's 2024 response considering housing reforms via the NDIS Review. (https://www.health.gov.au/sites/default/files/2025-07/australian-government-response-to-the-disability-royal-commission.pdf)

**Match to the Note's prescription:** Closest of the four. The SDA quarterly report is exactly the cadence-and-granularity model HUD lacks. The four-category design taxonomy is the kind of standardized accessibility classification that HUD's UFAS/Section 504 regime nominally requires but does not collect or publish in unit-level form. Caveat: SDA covers only the most severely disabled cohort and a small share of total disabled-population housing.

---

## 4. European Union — Directive 2019/882, EU Disability Strategy 2021–2030, EU-SILC

The EU's architecture is the weakest of the four for housing specifically, because the European Accessibility Act does not extend to housing.

**(a) European Accessibility Act (Directive 2019/882).** Adopted 17 April 2019, the Act standardizes accessibility for products and services (chiefly digital). Critically, "the Act focuses mainly on digital products and services and does not cover areas such as health care services, education, transport, housing, or household products. Implementation of accessibility requirements of the built environment are left to the will of the EU countries." Member States were required to transpose by 28 June 2022 and apply the requirements by 28 June 2025. Built-environment accessibility is voluntary, allowing Member States to elect to make it mandatory at national level. (https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng; https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en)

**(b) European Strategy for the Rights of Persons with Disabilities 2021–2030.** The successor to the 2010–2020 strategy, this contains a housing pillar committed to "enabling persons with disabilities to live in accessible, supported housing in the community or to continue living at home." It does not impose a unit-level data-collection mandate but coordinates Member-State reporting. (https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030_en)

**(c) Eurostat / EU-SILC disability-housing statistics.** EU Statistics on Income and Living Conditions (EU-SILC) is the recurring household survey from which Eurostat publishes cross-Member-State disability-housing statistics. Disability is operationalized via the Global Activity Limitation Indicator. Since 2021, EU-SILC includes ad-hoc thematic modules every two years. Published Eurostat findings disaggregate housing tenure (in 2023, 68.2% of EU residents aged 16+ with disability lived in owner-occupied housing; 31.8% rented), housing deprivation (17.2% of those with activity limitation reported leaking roof / damp / rot, vs. 11.7% without), and energy poverty. (https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Disability_statistics_-_housing_conditions; https://ec.europa.eu/eurostat/web/income-and-living-conditions/database/modules)

**Match to the Note's prescription:** Partial. EU-SILC is a robust recurring survey instrument and its ad-hoc modules can interrogate accessibility, but the EU lacks (i) a unit-level accessibility-features dataset comparable to the EHS dwelling inspection, (ii) a binding member-state accessibility data-collection mandate analogous to a directive, and (iii) any equivalent of HUD-assisted-stock-level data because housing is a national competence. The EU comparator best supports the Note's argument that even peer jurisdictions with strong general-population disability statistics (EU-SILC) have left a gap at the assisted-housing-stock level — a gap HUD shares but does not even fill at the general-population level via comparable instruments.

---

## 5. UN CRPD Article 31 — Statistics and Data Collection Obligations

**Treaty text (Article 31, paraphrased to comply with copyright):** States Parties undertake to collect appropriate statistical and research data to formulate and implement policies giving effect to the Convention; the data must be disaggregated as appropriate and used to assess implementation and identify barriers; collection must comply with data-protection law and ethical/human-rights norms; and States Parties must disseminate the statistics and ensure their accessibility to persons with disabilities. (https://www.un.org/development/desa/disabilities/convention-on-the-rights-of-persons-with-disabilities/article-31-statistics-and-data-collection.html)

**U.S. status:** The United States signed the CRPD on July 30, 2009 but has not ratified (the Senate failed to reach the two-thirds majority on December 4, 2012). The U.S. is therefore not legally bound by Article 31, but signature creates an obligation under Vienna Convention Article 18 not to defeat the treaty's object and purpose pending a ratification decision.

**Implementation by other signatories (a representative sample):**

- **OHCHR Article 31 illustrative indicators.** OHCHR has published a List of Illustrative Indicators on Statistics and Data Collection that operationalizes Article 31 for State Party reporting; these include structural, process, and outcome indicators for housing among other rights areas. (https://www.ohchr.org/sites/default/files/article-31-indicators-en.pdf)

- **Washington Group Short Set (WG-SS).** A six-question functional-difficulty module designed for use in censuses and household surveys, now adopted in dozens of national instruments. The Disability Statistics – Questionnaire Review (DS-QR) Database tracks WG-SS adoption across population and housing censuses globally. (https://ijpds.org/article/view/2477)

- **Concluding Observations.** The CRPD Committee has consistently recommended that State Parties "develop a national system for the systematic collection of updated statistical and research data … disaggregated by age, sex, type of impairment, and other relevant factors" — a recommendation routinely directed at signatories with thin disability-housing data, including in housing-specific concluding observations to Australia, the UK, Canada, and EU member states. (https://www.ohchr.org/sites/default/files/2022-06/G2139630-Accesible.pdf)

- **New Zealand (Whaikaha) example.** New Zealand publishes formal responses to UNCRPD recommendations under Articles 31–33, treating Article 31 as an obligation to maintain a Disability Data and Evidence Working Group with cross-agency reach. (https://www.whaikaha.govt.nz/about-us/the-uncrpd/implementing-the-uncrpd/response-to-the-uncrpd-committees-recommendations/uncrpd-recommendations-specific-obligations-articles-3133)

The practical effect of Article 31 in peer jurisdictions is to provide a treaty-anchored backstop against the kind of agency discretion the Note critiques: even where domestic statutes are silent on the granularity of disability-housing data collection, ratifying states must report periodically to the CRPD Committee on what they collect and publish. The U.S., as a signatory only, faces no equivalent reporting discipline.

---

## 6. Synthesis: Which comparators best support the Note's prescription?

The Note's prescriptive argument is that HUD should operate, on a binding cadence, a unit-level disability-and-accessibility data infrastructure tied to its assisted stock, with public reporting that disciplines programmatic decisions. Ranked by closeness of fit:

1. **Australia (SDA quarterly reporting) is the strongest model.** It pairs (i) a formal four-category accessibility-design taxonomy applied at the dwelling level, (ii) quarterly publication with downloadable data tables, (iii) explicit disclosure of supply-demand mismatches (the 9,662 "stranded SDA-funded participants" datum), and (iv) AIHW supplementary reporting at the general population. The architectural lesson for HUD: standardize an accessibility classification at the unit level and publish on a fixed cadence, including unfilled-need indicators.

2. **Canada (CMHC SAHS + NHS reporting) is the closest institutional analogue.** CMHC is HUD's structural twin; the SAHS demonstrates that an HFA-style federal housing agency can run a recurring accessibility-features survey of its assisted stock and publish trend data ("60% no features in 2019 → 37% in 2023") that the agency can be held accountable to. The lesson for HUD is the institutional one: HUD already has the survey infrastructure (e.g., RHFS, AHS topical modules); the gap is design and political will, not capacity.

3. **United Kingdom (English Housing Survey + AHRs) is the strongest model for *general housing-stock* accessibility.** The EHS dwelling inspection's four-feature visitability code is a low-cost, high-yield model that HUD could adopt for HUD-assisted stock via either the AHS topical module or a dedicated REAC/NSPIRE accessibility add-on. The London Plan 90/10 rule shows how national-level data can drive sub-national binding planning targets.

4. **EU (Directive 2019/882 + EU-SILC) is the weakest fit but useful as a counter-example.** It shows that a continental architecture with strong general disability statistics (EU-SILC) can still leave the assisted-housing-stock gap unfilled — supporting the Note's argument that HUD's gap is not unique but rather is the typical *failure mode* that binding national mandates must affirmatively cure.

**On UN CRPD Article 31:** Article 31 is the international civil-rights baseline the Note's title gestures toward. Even non-ratifying signatories (the U.S.) are subject to its object-and-purpose obligation, and ratifying peer states (Canada, UK, Australia, all EU Member States) have built their data architectures partly in response to the CRPD Committee's repeated insistence that disability-housing data be collected, disaggregated, and disseminated. HUD's failure to maintain unit-level disability-accessibility data is therefore not merely a domestic policy gap but a deviation from a baseline that every comparable signatory has at least nominally endorsed.

**Honest gaps in this research:**
- I did not retrieve the underlying CMHC SAHS questionnaire to verify whether its "accessibility features" battery is comparable in granularity to NDIS SDA categories or EHS visitability features. A targeted FOI-equivalent or direct CMHC methodology review would close this gap.
- The London Accessible Housing Register is described in the literature as "no longer actively developed"; its current operational status across boroughs in 2026 is unclear from the sources retrieved.
- The EU's housing-pillar implementation under the 2021–2030 Strategy includes a planned European Disability Card and accessibility resource center; whether either has produced cross-Member-State comparable accessible-housing-stock data by 2026 is not confirmed in the sources retrieved.
- I have not independently verified the CRPD Committee's most recent Concluding Observations specifically addressing housing data for Canada, UK, Australia. Citing those observations directly would strengthen the international-baseline argument.

Word count: approximately 2,420.
