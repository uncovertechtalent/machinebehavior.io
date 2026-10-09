title: TISAX vs ISO 27001
summary: Two information-security assurance mechanisms with overlapping controls but different mechanics, audiences, and audit dynamics.
parent: tisax
order: 100
labels: cross-cutting, iso-27001, tisax
aliases: TISAX vs ISO 27001 | ISO 27001 vs TISAX | TISAX ISO 27001 Comparison | TISAX ISO 27001 Mapping
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/tisax/TISAX vs ISO 27001.md
reviewed: no
---
> Two information-security assurance mechanisms with overlapping controls but different mechanics, audiences, and audit dynamics. Organizations serving both automotive and non-automotive customers typically implement both. This atom maps the overlap and the delta, the dual-implementation patterns, and the decision criteria for "which first?"

## Side-by-side mechanics

| Dimension | ISO/IEC 27001:2022 | TISAX |
|---|---|---|
| Standard owner | ISO / IEC (international body) | VDA (DE automotive industry) |
| Operating body | National accreditation bodies + certification bodies | ENX Association (Frankfurt) |
| Recognition type | Certificate | Label in shared registry |
| Audit output | Public-facing certificate | Private audit report + portal label |
| Visibility | Customer-requested; logo for marketing | OEM-portal query only; no public visibility |
| Validity | 3 years | 3 years |
| In-cycle audits | Annual surveillance audits | None |
| Scope mechanism | Organization-defined SoA | OEM-specified labels + assessment scope |
| Self-assessment role | Optional internal; feeds external | Mandatory first step of formal process |
| Assessment levels | Single (Stage 1 + Stage 2) | Three (AL1, AL2, AL3) |
| Control catalogue | Annex A (93 controls in 4 themes) | VDA-ISA (~40-50 controls + Prototype + Data Protection) |
| Maturity scoring | None (binary applicable / not) | SPICE-style 0-5 per control |
| Sector | Cross-sector, universal | German automotive supply chain |
| Geography | International recognition | DE-focused; some EU automotive reach |
| Cost (first time, small SaaS / supplier) | €15-40k+ certification | €5-15k audit + €1-5k ENX fees |
| Public-facing artefact | Yes (certificate) | No (registry-only) |
| Required by | Procurement RFPs across sectors | OEM contracts in automotive |
| Mandatory triggers | Customer / regulatory requirements | OEM contract flow-down |

## Control overlap

VDA-ISA 6.0 (late 2023) restructured to align with ISO 27001:2022 Annex A four-theme layout. Most VDA-ISA Info Sec controls map to one or more ISO 27001 Annex A controls.

Approximate overlap:

- **70-80%** of VDA-ISA Info Sec controls have a one-to-one or near-one-to-one ISO 27001 Annex A counterpart.
- **15-20%** of VDA-ISA Info Sec controls aggregate multiple ISO 27001 controls into a single VDA-ISA control with broader scope.
- **5-10%** of VDA-ISA Info Sec controls reflect automotive-specific tailoring not directly mirrored in Annex A (e.g., supplier-network-connection controls, automotive-specific incident handling).

The Prototype Protection and Data Protection modules have less ISO 27001 overlap. Prototype Protection is automotive-specific; Data Protection aligns more closely with ISO 27701 PIMS than core ISO 27001.

## What ISO 27001 covers that TISAX does not

- **Cross-sector applicability** — TISAX is automotive-scoped. ISO 27001 covers all sectors.
- **Management-system "shall" requirements (Cl 4-10)** — TISAX implicitly requires a management approach but does not have the explicit clause-level requirements of ISO 27001 Cl 4-10. The VDA-ISA catalogue is controls-focused.
- **Risk methodology breadth** — ISO 27001 (via Cl 6.1.2 + ISO 27005) accommodates multiple risk approaches. TISAX folds risk thinking into the controls themselves rather than as a standalone methodology.
- **Statement of Applicability** — no TISAX equivalent. OEMs specify labels; suppliers cannot unilaterally narrow scope through justified exclusions.
- **Public-facing recognition** — ISO 27001 certificates can be shared with any audience. TISAX labels are private.

## What TISAX covers that ISO 27001 does not

- **Prototype Protection** — automotive-specific. ISO 27001 has no native equivalent for pre-series component or prototype-vehicle protection.
- **Maturity scoring** — VDA-ISA SPICE-style 0-5 scoring is more granular than ISO 27001's binary "implemented / not."
- **Sector-coordinated assurance** — TISAX is designed for cross-OEM result-sharing; ISO 27001 has no equivalent registry mechanism.
- **AL-level flexibility** — TISAX offers three audit depths (AL1 / AL2 / AL3); ISO 27001 has a single audit depth (with risk-weighted scoping by the auditor).
- **Direct OEM-procurement integration** — TISAX is built into OEM procurement portals; ISO 27001 requires manual document exchange.

## Dual-implementation patterns

Suppliers serving both automotive and non-automotive customers typically run both. Two main patterns:

### Pattern 1: ISO 27001 first, TISAX added

Common for orgs that grew non-automotive and added automotive customers later. Implementation:

- Implement full ISO 27001 first (broader management-system scope, SoA, full Annex A consideration).
- Map VDA-ISA controls to ISO 27001 implementation; identify gaps (mostly Prototype Protection, some automotive-specific Info Sec items).
- Add gap-closing controls.
- Engage TISAX-accredited audit provider; many providers audit both standards in a combined engagement.

Time savings: 50-70% of TISAX implementation effort already done via ISO 27001.

### Pattern 2: TISAX first, ISO 27001 added

Common for German auto-supplier orgs expanding into non-automotive markets. Implementation:

- TISAX already in place (often Info Sec High + AL2 minimum).
- Expand controls to cover ISO 27001 Annex A gaps (controls not in VDA-ISA or shaped differently).
- Build out management-system "shall" requirements (Cl 4-10), particularly more formal risk methodology, internal audit, management review.
- Produce Statement of Applicability.
- Engage ISO 27001 certification body.

Time savings: 60-80% of ISO 27001 implementation effort already done via TISAX.

### Pattern 3: Combined audit by single provider

Several audit providers (large TÜV / DEKRA / DQS firms, Big Four) hold both ISO 27001 certification-body status and TISAX audit-provider accreditation. A combined audit covers both standards in a single engagement.

Cost savings: 20-40% on audit fees vs separate audits.

Implementation timing: typically one of the standards is the "lead" (driving the audit conduct) with the other as overlay; auditor produces both deliverables from a shared evidence base.

## Decision criteria: which first?

### Choose ISO 27001 first if:

- Org serves multiple sectors with non-automotive customers a significant share.
- Procurement RFPs cite ISO 27001 explicitly.
- US-market customer presence is significant (US procurement more familiar with ISO 27001 than TISAX).
- The org wants public-facing security recognition (website logo, marketing material).

### Choose TISAX first if:

- Org serves automotive primarily or exclusively.
- OEM contract clauses specify TISAX with no equivalent ISO 27001 acceptance.
- The first major customer engagement requiring assurance is automotive.
- The supplier-tier is mid-market German Mittelstand with no international expansion immediate.

### Implement both if:

- Mixed customer portfolio (auto + non-auto).
- Strategic positioning for procurement-readiness across sectors.
- Large enough scale to amortize dual-audit cost (typically 100+ employees or significant revenue with assurance-dependent customers).

## OEM acceptance of ISO 27001 in lieu of TISAX

Generally, German OEMs do not accept ISO 27001 in lieu of TISAX. Reasons:

- TISAX has automotive-specific control content (Prototype Protection) that ISO 27001 does not cover.
- TISAX uses the ENX-portal mechanism for cross-OEM result-sharing.
- TISAX assessment levels (especially AL3) include physical-control verification that ISO 27001 surveillance audits do not.

Some non-German OEMs (Stellantis, Renault, some Japanese / Korean OEMs in EU operations) accept ISO 27001 or have their own equivalent. Volvo / Polestar accept TISAX. Tesla and other US-origin OEMs use SOC 2 / ISO 27001 patterns more than TISAX.

## OEM acceptance of TISAX in lieu of ISO 27001

Outside automotive, TISAX has limited recognition. Non-automotive procurement organizations typically:

- Are unfamiliar with TISAX
- Cannot verify TISAX labels (no ENX portal access)
- Default to recognized international standards (ISO 27001, SOC 2)

A TISAX-only supplier serving non-automotive customers typically cannot use the TISAX label as the primary procurement-readiness signal. Either provide audit report directly, or pursue additional ISO 27001 / SOC 2 certification.

## Audit-provider and auditor overlap

The same audit-provider firms handle both ISO 27001 certification and TISAX assessment:

- TÜV SÜD, TÜV Rheinland, TÜV Nord — both
- DEKRA, DQS — both
- KPMG, Deloitte, PwC, EY — both
- BSI Group — both (particularly UK / EMEA)
- Schellman, A-LIGN — primarily ISO 27001 / SOC 2; some TISAX presence
- Coalfire — primarily ISO 27001 / SOC 2 / FedRAMP

Within firms, the same lead auditor sometimes handles both audits (combined engagement); sometimes different auditors per standard (depth specialization). Discuss with the audit provider during selection.

## Common implementation gotchas

- **Scope mismatch.** ISO 27001 SoA scope and TISAX label scope are not identical. Suppliers sometimes discover that the ISO 27001 scope excludes a site that is in scope for a TISAX label, or vice versa.
- **Control implementation mapped but not aligned.** Generic ISO 27001 implementations sometimes fail TISAX automotive-specific scoring. Example: a generic asset inventory may pass ISO 27001 but fail TISAX Prototype Protection asset-tracking requirements.
- **Audit-provider experience mismatch.** A provider strong in ISO 27001 may have weaker TISAX automotive-context capability, or vice versa. Combined audits work better when the provider has equivalent strength in both.
- **Catalogue version drift.** VDA-ISA revisions (e.g., 5.1 → 6.0) move faster than ISO 27001 revisions (8-year cycle). Combined implementations need to track both update cycles.
- **Documentation overhead.** Maintaining two sets of evidence packages, two sets of policy mappings, two sets of audit responses doubles maintenance unless the org consolidates documentation around a single source of truth with output formats per audit.

## SRE and AI-agent fit notes

- **Control alignment for AI/cloud.** ISO 27001:2022 Annex A.5.7 (threat intel), A.5.23 (cloud), A.8.9 (configuration), A.8.16 (monitoring), A.8.28 (secure coding) closely map to VDA-ISA 6.0 equivalents. Implementation work satisfies both with appropriate evidence documentation.
- **Prototype Protection × AI.** This is the standout TISAX-specific item. ISO 27001 implementations targeting automotive customers need explicit Prototype Protection control build-out — no native ISO equivalent.
- **Vendor and supplier management.** ISO 27001 A.5.19-A.5.23 + VDA-ISA supplier-security controls overlap substantially. AI-tool vendor (model provider) management can be documented once and referenced for both.

## See also

- [[TISAX Cluster|cluster MOC]] · [[ISO 27001 Cluster|ISO 27001]] 
- [[TISAX VDA-ISA Catalogue]] · [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
- [[TISAX Assessment Process]] · [[ISO 27001 Certification Process]]
