# Appendix K: Classification Prompts

**Cited by:** Appendix A § A.8 and Appendix A-4 § A-4.3 (pipeline instruments).
**Status of materials:** Instruments, not findings. K.1 is reproduced verbatim as run (re-confirmed byte-exact against the compiled screening class of 2026-04-11). K.2 and K.3 are republished from byte-exact constant-pool extractions out of the compiled pipeline classes of 2026-04-11 (SHA-256 digests in each section); version control does not cover 2026-03-28 to 2026-04-11, so prose edits inside that window cannot be excluded, but the field-level identification against the run-day output databases is exact (30/30 fields).
**Regeneration:** Not applicable; canonical prompt text is also preserved in `method/prompts/` and `method/pipeline/`.

The following prompts are the instruments used to generate all classification data in the two source corpora — the RA Database (2,366 downloaded documents) and the 2015 FHA Database (1,661) — that Appendix A § A.5 merges into the FHA Unified Database (3,198 from the two source corpora; T0 = 3,366 after the July 2026 endpoint refresh). They are reproduced or hosted in full to enable replication, together with the Stage 4 per-claim enrichment instruments (K.3).

## K.1 FHA Relevance Screening Prompt

Used by Gemini 3.1 Flash Lite at temperature 0.0 for binary FHA screening (Stage 1). Each of the 2,366 (RA Database) and 1,661 (2015 FHA Database) downloaded case texts was submitted with this prompt.

> You are a legal document classifier. Your only job is to determine whether the following document is a legal decision (e.g. court opinion, administrative ruling, or tribunal decision) that adjudicates a claim brought under the Fair Housing Act (FHA). Respond with ONLY the single word YES or NO. Do not include any explanation, punctuation, or other text.

## K.2 Case Classification Prompt

Used by all three OpenRouter models (MiniMax M2.7, DeepSeek V3.2, Kimi K2.5) at temperature 0.2 with model-specific reasoning budgets (see Section A.2.3) for independent classification (Stage 2). This is the identical prompt submitted to each model; each model received it as a system prompt alongside the full case text as the user message.

**Provenance.** The text below is the as-run system prompt recovered byte-exact from the compiled classification class of 2026-04-11; Java text-block processing happens at compile time, so the class constant is the literal runtime string. SHA-256 `CB9FC62B070797DE2E66FA5BE00C3A055E37857FCE8FFBEB2C41274ABB3FAD0A`; the identical text is hosted at [`prompts/case_classification_prompt.txt`](../../method/prompts/case_classification_prompt.txt). The run-day output databases match the recovered template 30/30 on per-model fields.

> You are classifying federal Fair Housing Act reasonable accommodation cases under 42 U.S.C. § 3604(f)(3)(B). For each case, extract the following fields. If a field cannot be determined from the available text, enter "UNDETERMINED." Do not guess — only classify based on what the opinion or order states.
>
> CRITICAL: You MUST output a single JSON object using EXACTLY the flat key structure shown in the template below. Do not nest fields inside sub-objects. Do not use variant key names. Every field listed in the template must appear in your output. If you cannot determine a value, use "UNDETERMINED" — never omit the field entirely.
>
> Fields to Extract
>
> 1. Case Identification
> - case_name: Full case name as styled
> - citation: Reporter citation (F.4th, F.Supp.3d, F.App'x, or WL number)
> - court: Court (e.g., "S.D.N.Y.", "7th Cir.", "D. Or.")
> - year: Year of the opinion or order being reviewed (integer)
> - procedural_posture: Select ONE from: MOTION_TO_DISMISS, SUMMARY_JUDGMENT, PRELIMINARY_INJUNCTION, TRIAL, DEFAULT_JUDGMENT, APPEAL, SETTLEMENT_CONSENT, ADMINISTRATIVE_REVIEW, DISCOVERY, OTHER_PROCEDURAL. If the opinion addresses multiple motions, select the one producing the most significant ruling on the RA claim.
> - fha_section_cited: Which subsection(s) of § 3604(f)(3) does the court substantively analyze? Select all that apply, comma-separated: "3604(f)(3)(A)" = reasonable modifications (physical changes at tenant's expense), "3604(f)(3)(B)" = reasonable accommodations (rules, policies, practices, services), "3604(f)(3)(C)" = design and construction (accessibility in new multifamily housing), "NONE_SPECIFIC" = court discusses § 3604(f) generally without specifying subsection.
>
> 2. Accommodation Type (Primary Classification)
>
> Classify the accommodation at issue into ONE primary category. If multiple accommodation types are alleged, classify by the PRIMARY accommodation driving the court's analysis.
>
> - ASSISTANCE_ANIMAL: Request to keep an animal (dog, cat, other) as an emotional support animal, service animal, or therapy animal, including breed/weight/species restriction waiver requests. In accommodation_description, specify whether ESA, service animal, or therapy animal if the opinion states the distinction.
> - STRUCTURAL_MODIFICATION: Request for physical changes to the dwelling or common areas (ramps, grab bars, widened doorways, roll-in showers, lowered counters, reserved parking space construction, automatic door openers)
> - POLICY_EXCEPTION: Request to waive or modify a rule, policy, or practice that does not fit any other specific category. Examples: occupancy limits, breed-neutral pet restrictions unrelated to assistance animals, no-smoking waivers, quiet hours exceptions, storage restrictions, move-in/move-out scheduling, criminal background screening waivers. This is the RESIDUAL policy category — use a more specific category (PARKING, TRANSFER, LIVE_IN_AIDE, EVICTION_DEFENSE, RENT_PAYMENT, COMMUNICATION_ACCOMMODATION, VISITOR_CAREGIVER_ACCESS) whenever one fits.
> - PARKING: Request for reserved, closer, accessible, or additional parking (without physical construction — if construction of a new space is required, classify as STRUCTURAL_MODIFICATION)
> - TRANSFER: Request to transfer to a different unit (ground floor, larger, quieter, accessible) within the same property or housing authority
> - SOBER_LIVING_GROUP_HOME_ZONING: Municipal zoning or land-use challenge by a group home, sober living facility, recovery residence, or supportive housing provider seeking to operate in a residentially zoned area
> - LIVE_IN_AIDE: Request to have a live-in aide, caregiver, or additional occupant for disability-related assistance as a permanent resident
> - COMMUNICATION_ACCOMMODATION: Request for alternative communication format or method (email delivery of notices, large print documents, sign language interpreter, TTY/TDD, audio recordings of meetings, translated documents for disability-related comprehension needs). Do NOT include requests to communicate with a specific person or general customer service complaints.
> - EVICTION_DEFENSE: Request that a landlord not proceed with eviction, or grant a second chance after a lease violation, as a reasonable accommodation for disability. Includes direct-threat defenses where the landlord claims the tenant poses a threat and the tenant argues accommodation would mitigate the threat. Includes requests to vacate a default judgment or extend cure period.
> - RENT_PAYMENT: Request to modify rent payment terms — payment plans for arrears, waiver of late fees, rent reduction, or modification of payment schedule — as a disability accommodation. Do NOT include requests for rent subsidy or voucher (classify those as POLICY_EXCEPTION).
> - VISITOR_CAREGIVER_ACCESS: Request to modify guest, visitor, or access policies to allow caregivers, aides, or family members to visit or access the property for disability-related support. Distinct from LIVE_IN_AIDE (which involves a permanent resident). Includes requests for key access, gate codes, or building entry for non-resident caregivers.
> - DISCRIMINATION_PRIMARY: The court's analysis focuses on intentional discrimination under § 3604(f)(1) or (f)(2) — refusal to rent, harassment, retaliation for requesting accommodation — rather than on the accommodation analysis under § 3604(f)(3)(B). Describe the accommodation request, if any, in accommodation_description.
> - OTHER: Does not fit any above category. Briefly describe in accommodation_description.
>
> - accommodation_type: [Select one from above]
> - accommodation_description: Brief (one sentence) description of the specific accommodation requested
>
> 3. Secondary Accommodation Type
> - secondary_accommodation_type: If the case involves a SECOND distinct accommodation request that receives substantial analysis, classify it here using the same categories. Otherwise enter "NONE."
>
> 4. Parties
>
> - plaintiff_type: Classify the plaintiff:
>   - INDIVIDUAL_TENANT: Individual person(s) seeking or residing in housing
>   - FAIR_HOUSING_ORG: Fair housing organization, testing organization, or advocacy group   (e.g., NFHA, local fair housing center)
>   - GROUP_HOME_OPERATOR: Operator of a group home, sober living facility, recovery   residence, or supportive housing
>   - GOVERNMENT: United States, state, or local government as plaintiff/complainant
>   - OTHER: Describe briefly
>
> - defendant_type: Classify the defendant:
>   - PRIVATE_LANDLORD: Individual landlord or private property owner
>   - PROPERTY_MANAGEMENT: Property management company
>   - HOA_CONDO_ASSN: Homeowners association or condominium association
>   - HOUSING_AUTHORITY: Public housing authority or government housing agency
>   - DEVELOPER: Housing developer or construction company
>   - MUNICIPALITY: City, county, town, or zoning board (zoning/land-use challenges)
>   - OTHER: Describe briefly
>
> 5. Disability Type
> - disability_category: Classify the disability at issue. Select ONE primary category:
>   - MENTAL_HEALTH: Depression, anxiety, PTSD, bipolar disorder, schizophrenia, or other   psychiatric disability
>   - SUBSTANCE_USE: Substance use disorder, alcoholism, recovery from addiction
>   - MOBILITY: Wheelchair use, ambulatory difficulty, musculoskeletal conditions
>   - SENSORY: Deaf/hard of hearing, blind/low vision
>   - INTELLECTUAL_DEVELOPMENTAL: Intellectual disability, autism, developmental disability
>   - MULTIPLE_UNSPECIFIED: Multiple disabilities alleged or disability not specified beyond   "disabled"
>   - OTHER: Describe briefly
>
> 6. Outcome
> - outcome: What happened at the procedural stage identified above:
>   - PLAINTIFF_WIN: Court ruled for plaintiff on the RA claim (granted PI, denied MTD,   granted SJ for plaintiff, jury verdict for plaintiff)
>   - DEFENDANT_WIN: Court ruled for defendant on the RA claim (granted MTD, granted SJ   for defendant, jury verdict for defendant)
>   - MIXED: Split outcome (some claims survived, some dismissed; partial summary judgment)
>   - SETTLEMENT: Case resolved by settlement or consent decree
>   - PROCEDURAL: Ruling on procedural matter only (remand, discovery dispute, class   certification) — no merits determination
>
> - key_holding: One sentence summarizing the court's core reasoning on the RA claim
>
> - loper_bright_cited: Does the opinion cite, discuss, or reference Loper Bright Enterprises v. Raimondo, 144 S. Ct. 2244 (2024)? (YES/NO)
>
> 7. Race-Disability Intersection
> - race_mentioned: Does the opinion mention the plaintiff's race or ethnicity? (YES/NO)
> - dual_basis_claim: Does the complaint allege BOTH race and disability discrimination? (YES/NO)
> - race_if_mentioned: If YES to either above, what race/ethnicity? Otherwise "N/A"
>
> 8. Interactive Process
> - interactive_process_discussed: Does the court discuss whether the defendant engaged in an interactive process with the plaintiff? (YES/NO)
> - delay_as_denial: Does the court address whether delay in responding to the accommodation request constituted a constructive denial? (YES/NO)
>
> 9. Property Location
> - property_city: The city or municipality where the housing at issue is located, as stated in the opinion. If the opinion identifies only the county or region, enter that. If no location is identifiable, enter "UNDETERMINED."
> - property_state: The two-letter state abbreviation (e.g., "CA", "NY", "TX"). If the court is a federal district court, the state can usually be inferred from the court name even if the opinion does not state it explicitly. Enter "UNDETERMINED" only if neither the opinion text nor the court name provides the state.
>
> 10. Housing Program Context
> - housing_type: Classify the housing at issue:
>   - PRIVATE_MARKET: Unsubsidized private rental or ownership housing
>   - PUBLIC_HOUSING: Public housing authority-owned units
>   - SECTION_8_VOUCHER: Housing Choice Voucher (tenant-based)
>   - SECTION_8_PBV: Project-Based Voucher or project-based Section 8
>   - LIHTC: Low-Income Housing Tax Credit property
>   - SECTION_811: Section 811 supportive housing
>   - SECTION_202: Section 202 elderly housing
>   - SUPPORTIVE_HOUSING: Supportive housing not otherwise categorized   (permanent supportive housing, transitional housing)
>   - OTHER_SUBSIDIZED: Other federal, state, or local subsidy
>   - HOA_CONDO: Owner-occupied condominium or HOA-governed community
>   - MANUFACTURED_HOUSING: Mobile home park or manufactured housing
>   - UNDETERMINED: Cannot determine from the opinion
> - subsidy_program: If the opinion mentions a specific federal, state, or local housing program by name (e.g., "LIHTC," "Section 8," "HOME," "CDBG," "Housing Trust Fund," "state housing finance agency"), list it here. Otherwise "NONE_MENTIONED."
>
> Classification Rules
>
> 1. When accommodation type is ambiguous: Classify based on what the COURT analyzes, not what the complaint alleges. If the court's analysis focuses on the ESA request even though structural modifications were also requested, classify as ASSISTANCE_ANIMAL.
>
> 2. Zoning cases: If the core dispute is whether a municipality must permit a group home or sober living facility to operate, classify as SOBER_LIVING_GROUP_HOME_ZONING regardless of the specific zoning provision at issue. These cases often frame the issue as "reasonable accommodation from zoning requirements."
>
> 3. Parking: Use the PARKING category only when the request is for designation or reservation of an existing space. If the request requires constructing a new parking area or physically modifying a space (adding signage alone does not count), classify as STRUCTURAL_MODIFICATION.
>
> 4. Multiple opinions in the same case: If you encounter multiple opinions from the same case (e.g., MTD ruling and later SJ ruling), classify each opinion separately. They will share a case_name but differ in procedural_posture, year, and potentially outcome.
>
> 5. Unpublished/summary orders: Classify these the same as published opinions. Note in citation if unpublished.
>
> 6. Cases where RA is not the primary claim: If the case primarily involves a different FHA theory (disparate impact, design-and-construction, direct discrimination) and RA is only a secondary or minor claim, still classify the RA component but note in key_holding that RA was not the primary theory.
>
> 7. Eviction-related accommodations: If the tenant requests that the landlord not evict them (or reverse an eviction) as a reasonable accommodation for disability — even if the underlying lease violation is noise, property damage, or behavioral — classify as EVICTION_DEFENSE. Do not classify as POLICY_EXCEPTION merely because the eviction follows a "policy" violation.
>
> 8. Communication format requests: If the accommodation is about HOW information is delivered (format, language, medium) rather than WHAT policy is being changed, classify as COMMUNICATION_ACCOMMODATION. Example: requesting email notices instead of paper is COMMUNICATION_ACCOMMODATION; requesting more notice time before an inspection is POLICY_EXCEPTION.
>
> 9. Discrimination-primary cases: Some cases allege discriminatory intent (e.g., refusing to rent to a disabled person, harassment, retaliation for requesting accommodation). If the court's analysis focuses on intentional discrimination under § 3604(f)(1) or (f)(2) rather than on the accommodation analysis under § 3604(f)(3)(B), classify accommodation_type as DISCRIMINATION_PRIMARY and describe the accommodation request, if any, in accommodation_description.
>
> 10. Tenant screening / criminal background: If the accommodation request is to waive or modify a criminal background screening policy, classify as POLICY_EXCEPTION. If the case primarily challenges the screening practice as disparate impact rather than requesting an individual accommodation, note in key_holding that RA was not the primary theory.
>
> 11. Emotional support animal vs. service animal: Both are ASSISTANCE_ANIMAL. Do not create separate subcategories. But in accommodation_description, specify whether the animal is an ESA, service animal, or therapy animal if the opinion states the distinction.
>
> 12. Default: when in doubt between POLICY_EXCEPTION and a specific category, prefer the specific category. POLICY_EXCEPTION is the residual.
>
> 11. Protected Class Analysis
>
> - primary_protected_class: The single protected class MOST CENTRAL to the court's analysis. This is the class whose discrimination claim receives the most substantive legal discussion. Use ONLY one of: "race", "color", "national_origin", "religion", "sex", "familial_status", "disability" Use "" if the case does not involve the Fair Housing Act.
>
> Guidance:
> - If the case analyzes a reasonable accommodation or reasonable modification claim under § 3604(f)(3), the primary class is "disability".
> - If the case analyzes refusal to rent based on race under § 3604(a), the primary class is "race".
> - If the case involves multiple protected classes, choose the one the court spends the most analysis on.
> - If the case is a group home / sober living zoning challenge, the primary class is "disability" even if the opinion discusses neighborhood racial composition.
>
> - protected_classes: ALL protected classes at issue in the case, not just the primary one. A case can involve multiple classes (e.g., a Black wheelchair user alleging both race and disability discrimination). Use ONLY these values: "race", "color", "national_origin", "religion", "sex", "familial_status", "disability" Return [] if the case does not involve the Fair Housing Act.
>
> 12. Claim Type Analysis
>
> - claim_types: ALL Fair Housing Act claim types alleged or analyzed in the opinion. Use ONLY these values:
> - "disparate_treatment" — Intentional discrimination under § 3604(a)-(b)
> - "disparate_impact" — Facially neutral policy with discriminatory effect under § 3604(a)
> - "reasonable_accommodation_denial" — Failure to accommodate under § 3604(f)(3)(B)
> - "reasonable_modification_denial" — Failure to permit modification under § 3604(f)(3)(A)
> - "design_and_construction" — Inaccessible multifamily housing under § 3604(f)(3)(C)
> - "retaliation" — Retaliation for exercising FHA rights under § 3617
> - "interference_coercion" — Interference, coercion, or intimidation under § 3617
> - "discriminatory_advertising" — Discriminatory notices or advertising under § 3604(c)
> - "discriminatory_lending" — Discrimination in residential real estate transactions under § 3605
> - "steering" — Directing people based on protected class
> - "other" — Any FHA claim not captured above
> Return [] if not an FHA case.
>
> - primary_claim_type: The single claim type that receives the most substantive analysis. Use the same values as claim_types. Use "" if not an FHA case.
>
> 13. Key Cases Cited
>
> - key_cases_cited: Up to 5 cases the court relies on MOST HEAVILY. Use standard citation format. Always include if cited: Ashcroft v. Iqbal, Bell Atlantic v. Twombly, Texas Dept. of Housing v. Inclusive Communities Project, City of Cleburne v. Cleburne Living Center, Olmstead v. L.C., Loper Bright v. Raimondo. Return [] if no significant cases cited or not an FHA case.
>
> 14. Brief Summary
>
> - brief_summary: Two sentences maximum. First sentence: who sued whom over what. Second sentence: what the court decided and why.
>
> Output Format
>
> Respond with ONLY the JSON object using exactly these keys. No explanation, no markdown formatting, no code fences.
>
> {
>   "case_name": "",
>   "citation": "",
>   "court": "",
>   "year": 0,
>   "procedural_posture": "",
>   "fha_section_cited": "",
>   "accommodation_type": "",
>   "accommodation_description": "",
>   "secondary_accommodation_type": "",
>   "plaintiff_type": "",
>   "defendant_type": "",
>   "disability_category": "",
>   "outcome": "",
>   "key_holding": "",
>   "loper_bright_cited": "",
>   "race_mentioned": "",
>   "dual_basis_claim": "",
>   "race_if_mentioned": "",
>   "interactive_process_discussed": "",
>   "delay_as_denial": "",
>   "property_city": "",
>   "property_state": "",
>   "housing_type": "",
>   "subsidy_program": "",
>   "primary_protected_class": "",
>   "protected_classes": [],
>   "key_cases_cited": [],
>   "claim_types": [],
>   "primary_claim_type": "",
>   "brief_summary": ""
> }

## K.3 Per-Claim Structured Extraction Prompts (Stage 4)

Used by Haiku 4.5 via the Batch API for the per-claim structured extraction (the defined Stage 4 term; see [`METHODOLOGY.md`](../../method/METHODOLOGY.md)) that decomposed the 3,193-case per-claim sub-corpus into 6,718 claim records. Both instruments were extracted byte-exact from the compiled extraction class of 2026-04-11 by the same constant-pool method as K.2 and are hosted in full:

- System prompt: [`prompts/per_claim_extraction_system_prompt.txt`](../../method/prompts/per_claim_extraction_system_prompt.txt) — SHA-256 `CC54B1E7C00A96ADAF71B1FBB6BB9156488D314D5D5F02F5A64895B773F28F0E`
- Per-case user-message template: [`prompts/per_claim_extraction_user_template.txt`](../../method/prompts/per_claim_extraction_user_template.txt) — SHA-256 `8C28EA76CD4870F2E2C187A6FC719A18B22F76576D6E78E0C5B1F2788CE245FF`

The permitted output structure is fixed by [`pipeline/per_claim_extraction_schema.json`](../../method/pipeline/per_claim_extraction_schema.json). The outputs are classifications under fixed questions; they do not establish the facts of any case.

---

*Supplementary materials for the Note (Arizona Law Review). The unified dataset (`data/FHA_Unified_Database.json`; T0 = 3,366 case-level records; the per-claim sub-corpus is 3,193 cases / 6,718 claims — see Appendix A § A.5 for the reconciliation) and all replication materials are in this repository.*
