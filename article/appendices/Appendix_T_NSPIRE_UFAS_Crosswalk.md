# Appendix T — NSPIRE / UFAS Accessibility Crosswalk

**Cited by:** Note footnotes 7 (UFAS/§ 504 crosswalk) and 47 (Part I.D)
**Source record:** the full methodology, sources used, and per-category coding rationale are retained in the project's private research records (see `../../replication/DATA_PROVENANCE.md`); the coding summary is § T.6
**Source dataset:** [`results/nspire_ufas_crosswalk.json`](../../results/nspire_ufas_crosswalk.json)
**Evidentiary status:** Appendix-level; supports the body's administrative-record NSPIRE claims (the preamble quotations are Tier 1, verified against the source binary).
**Regeneration:** Not script-generated; author-coded from the NSPIRE final standards and UFAS text (see § T.6).

---

## T.1 Bottom line

Of 17 core UFAS / Section 504 accessibility requirement categories applicable to federally assisted multifamily housing, NSPIRE inspections **fully cover 0 (0.0%)**, **partially cover 4 (23.5%)**, and **do not cover 13 (76.5%)**. No NSPIRE item verifies that the required number of accessible units exist in a property.

HUD itself acknowledged this gap in the May 2023 NSPIRE final rule preamble: "the NSPIRE Standards will include elements of accessibility within the standards, but these elements are not the same as the Federal accessibility standards as they relate to housing" and "[c]ompliance with these NSPIRE Standards does not mean the participant has complied with the Federal accessibility standards." 88 Fed. Reg. 30,442, 30,453 (May 11, 2023).

## T.2 Coding rule

| Code | Definition |
|---|---|
| **FULL** | NSPIRE verifies the core UFAS requirement, including existence where required and the governing dimensional/operability criteria. |
| **PARTIAL** | NSPIRE checks some accessibility-relevant aspect of the same feature, but incompletely. |
| **NOT** | NSPIRE has no inspectable item for the accessibility requirement, or only generic maintenance checks that do not test the accessibility standard itself. |

Conservative choice: when an NSPIRE item only checks generic function (for example, whether a sink works), I coded NOT rather than PARTIAL unless the standard actually tests an accessibility-relevant criterion.

## T.3 Summary statistics

| Coverage | Count | % |
|---|---|---|
| FULL | 0 | 0.0% |
| PARTIAL | 4 | 23.5% |
| NOT | 13 | 76.5% |
| **Total categories** | **17** | **100%** |

NSPIRE verifies Section 504 required accessible-unit counts? **No.**

## T.4 Crosswalk

| Requirement category | UFAS / Section 504 sections | Coverage |
|---|---|---|
| Required number of mobility-accessible and hearing/vision-accessible units | 24 C.F.R. § 8.22(b); UFAS § 4.34 | NOT |
| Accessible routes and ramps from site arrival points to entrances and common spaces | UFAS §§ 4.3, 4.8, 4.14.1; § 4.34.2(3), (7) | PARTIAL |
| Accessible parking spaces and passenger loading zones | UFAS § 4.6 | NOT |
| Doors and accessible entrances | UFAS §§ 4.13, 4.14; § 4.34.2(6)–(7) | NOT |
| Wheelchair turning space, clear floor space, route headroom/protrusion limits | UFAS §§ 4.2, 4.4; § 4.23.3 | NOT |
| Elevators | UFAS § 4.10 | PARTIAL |
| Water closets: transfer clearances, height, flush controls | UFAS § 4.16; § 4.34.5.2 | NOT |
| Bathroom grab bars and reinforcement | UFAS §§ 4.16.4, 4.20.4, 4.21.4, 4.26; § 4.34.5 | PARTIAL |
| Bathroom layout, door swing, accessible fixture arrangement | UFAS § 4.23; § 4.34.5.1 | NOT |
| Lavatories, mirrors, medicine cabinets | UFAS § 4.19; § 4.34.5.3 | NOT |
| Bathtubs and showers: seats, controls, spray units, transfer area, enclosure clearance | UFAS §§ 4.20, 4.21; § 4.34.5.4–.6 | NOT |
| Kitchens: clearances, work surfaces, sink/appliance approach, appliance controls | UFAS § 4.24; § 4.34.6 | NOT |
| Storage reach ranges and accessible hardware | UFAS § 4.25; § 4.34.2(8) | NOT |
| Controls and operating mechanisms | UFAS § 4.27; § 4.34.2(9) | NOT |
| Visual emergency alarms and alarm readiness in hearing/vision-accessible units | UFAS § 4.28; § 4.34.2(10); § 4.34.4(4) | PARTIAL |
| Accessible signage | UFAS § 4.30 | NOT |
| Telephones and communication features for hearing-impaired users | UFAS § 4.31 | NOT |

## T.5 Main conclusion

NSPIRE does not function as an accessibility-compliance audit. The verified overlap is narrow and limited to four buckets:

1. existing accessible-route safety / passability defects on paths and ramps;
2. elevator operability and leveling;
3. whether an already-installed bathroom grab bar is secure; and
4. whether certain alarms produce an audio or visual signal when tested.

Everything else that matters for UFAS / Section 504 compliance — required unit counts, doorway width, maneuvering clearance, turning radius, bathroom layout, kitchen work-surface geometry, accessible storage reach ranges, accessible controls, tactile signage, and communication features — is outside the NSPIRE inspection logic.

A property can do well on NSPIRE while still violating the core design-and-construction or Section 504 accessibility requirements that matter most to disabled tenants. The missing piece is not just a few more checklist items; it is the absence of a property-level accessibility module and output.

## T.6 Methodology and sources

Full source citations (including the specific UFAS subsections covered by each requirement category, the NSPIRE table references reviewed, and the inspection-item language coded) are retained with the project's private research records. The crosswalk was built from direct review of the NSPIRE final standards PDF (Tables 4, 5, 10, 12, 14, 17, 28–30, 40, 41, 49, 52, 56, 58) and the UFAS sections cited above. No LLM component is involved in the coding; each coding decision is the author's judgment against the inspection-item text and the UFAS requirement language.
