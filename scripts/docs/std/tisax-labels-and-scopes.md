title: TISAX Labels and Scopes
summary: Labels are the unit of recognition in TISAX, what appears in the ENX portal, what OEMs query for, what suppliers earn from a successful assessment.
parent: tisax
order: 100
labels: tisax, tisax-mechanism
aliases: TISAX Labels | TISAX Scopes | TISAX Assessment Objectives | TISAX Protection Levels
type: tisax-mechanism
created: 2026-05-12
updated: 2026-06-08
origin: pillars/tisax/TISAX Labels and Scopes.md
reviewed: no
---
> Labels are the unit of recognition in TISAX — what appears in the ENX portal, what OEMs query for, what suppliers earn from a successful assessment. This atom maps the major label families, the per-label scoping rules, and how OEM contracts translate to label requirements.

## Label families

Five primary label families. A supplier typically obtains one or more in a single assessment cycle.

### 1. Information Security with High protection requirement

The baseline label. Required for the majority of OEM supplier relationships. Demonstrates that the supplier has implemented an information security management approach capable of protecting confidential business information.

Scope: the supplier's information processing in connection with the OEM relationship.

Typical AL: AL2 sufficient for most relationships; AL3 sometimes specified for tier-1 or strategic suppliers.

### 2. Information Security with Very High protection requirement

The top-tier information security label. Required for suppliers handling strategic or particularly sensitive business information.

Triggers: strategic-supplier-tier relationships, access to OEM intellectual property of high strategic value, access to commercial information whose disclosure would cause significant business harm.

Typical AL: AL3 standard.

### 3. Prototype Protection — Components

Required for suppliers handling pre-series components: physical parts, prototypes, samples, validation hardware.

Sub-labels exist for protection-requirement levels within Prototype Protection. The OEM specifies which sub-label is required based on the sensitivity of the prototype access.

Typical AL: AL3 (Prototype Protection almost always requires AL3 due to physical-control verification needs).

### 4. Prototype Protection — Vehicles

Required for suppliers handling prototype vehicles: test mules, validation vehicles, pre-production vehicles, autonomous-driving test platforms.

Additional controls beyond Components label: camouflage requirements for road testing, parking and storage restrictions, photo / video controls for any external exposure, transport rules.

Typical AL: AL3.

### 5. Prototype Protection — Test Vehicles in Use

Related to Vehicles label, with specific controls for prototype vehicles operating in public spaces. Covers operator training, route planning, media-protection during test runs, accident-handling procedures that protect prototype information.

### 6. Data Protection — Standard

Required for suppliers processing personal data on behalf of OEM that does not include special categories under GDPR Article 9.

Scope: data subject processing, technical and organizational measures, sub-processor management, breach notification.

Typical AL: AL2 sufficient; AL3 for very high-volume or sensitive processing.

### 7. Data Protection — Special Categories

Required when supplier processes Article 9 special-category personal data (health, biometric, ethnic origin, political opinion, religious belief, trade union membership, genetic data, sex life or sexual orientation).

Higher control bar than standard Data Protection. Reflects GDPR's elevated protection requirements for special categories.

Typical AL: AL3.

### 8. Connection to Third Parties

A specialized label for suppliers connecting to OEM networks (direct network connectivity, dedicated VPN, MPLS link, IT-to-IT integration). Controls cover the network-connection security and the segregation between the OEM-facing connection and other supplier infrastructure.

Often combined with other labels rather than standalone.

## How labels are scoped

Scope dimensions per label:

- **Sites** — which physical locations are covered. A supplier with multiple offices, plants, R&D centres may have site-specific labels. The ENX portal records per-site label status.
- **OEM relationships** — labels typically apply broadly to the supplier's information-processing capability, not specific OEM relationships. But Prototype Protection labels can be OEM-relationship-specific due to per-OEM physical-control requirements.
- **Technical scope** — which IT systems, networks, business processes are covered. Defined in the assessment.
- **Validity period** — 3 years from successful assessment completion.

## How OEMs specify label requirements

OEM supplier contracts contain TISAX flow-down clauses specifying:

- Which label(s) the supplier must obtain
- The required assessment level per label
- The required validity (typically "valid at time of contract and maintained throughout the term")
- The required scope (sites covered, business processes covered)
- Any OEM-specific addenda (some OEMs publish additional security requirements that suppliers must comply with on top of TISAX baseline)

The flow-down chain: OEM → tier-1 → tier-2 → tier-3, with each tier applying TISAX requirements to its own suppliers based on the originating OEM's requirements.

## Common label combinations

Patterns observed in practice:

- **Standard tier-2 IT services supplier:**
  - Info Sec High + AL2
- **Tier-2 prototype-component supplier:**
  - Info Sec High + AL3
  - Prototype Protection Components + AL3
- **Tier-1 development partner:**
  - Info Sec Very High + AL3
  - Prototype Protection Components + AL3
  - Prototype Protection Vehicles + AL3
  - Connection to Third Parties + AL3 (if direct network access)
- **HR / payroll / customer-service SaaS for OEM:**
  - Info Sec High + AL2
  - Data Protection Standard + AL2
- **Genetic / biometric / health data processor (e.g., driver-monitoring vendor):**
  - Info Sec High + AL3
  - Data Protection Special Categories + AL3

## Label visibility in the ENX portal

Once issued, labels appear in the ENX participant portal. Visibility rules:

- **Supplier owns its own label record** — the supplier can view its own labels and scope details.
- **Customer authorization required for cross-supplier visibility** — by default, only the supplier sees its labels. The supplier authorizes specific OEMs / customers to view labels. Authorization is typically standing (per ongoing business relationship) rather than per-query.
- **OEM-side view** — OEM procurement queries the portal for authorized supplier labels. Result includes label list, validity dates, assessment level, audit-provider identity, site coverage.
- **No public-facing view** — TISAX labels are not visible outside the ENX portal. There is no public registry, no logo for website use, no marketing-facing artefact (unlike ISO 27001 certificates which suppliers can publish).

## Labels vs ISO 27001 SoA

A TISAX label is closer to a "scoped ISO 27001 certificate" than a Statement of Applicability. The label says: this supplier has been assessed against the VDA-ISA criteria for this assessment objective, at this maturity level, with this scope, by this audit provider, valid until this date. There is no per-control "applicable yes / no" registry equivalent to the SoA; the audit-provider report carries the per-control scoring detail and is not published.

For a buyer (OEM), the label is shorthand: "this supplier passed this assessment at this rigor." For deeper visibility, the OEM can request the audit report from the supplier directly; supplier disclosure is bilateral and typically accompanies high-stakes engagements.

## Renewal and continuity

Labels expire after 3 years. Renewal mechanics:

- **Begin renewal 4-6 months before expiry** to ensure continuity.
- **Renewal assessment** runs against the then-current VDA-ISA catalogue version.
- **Catalogue revisions during the 3-year validity** do not invalidate the existing label; the label remains valid until expiry against the catalogue version it was issued under.
- **Scope changes during validity** (new site, new business process) require an in-cycle re-assessment for the extended scope.
- **Loss of label** — major contract breaches or significant security incidents may trigger OEM-side revocation requests; the ENX portal allows label removal in extreme cases.

## SRE and AI-agent fit notes

- **Cloud-services as label-bearing service-provider relationships.** Suppliers using model providers as cloud services should ensure the provider relationship is documented and reflected in supplier-control evidence under whichever label applies.
- **AI-tool-handled prototype data and label boundaries.** Default AI tooling configurations typically fail Prototype Protection criteria. Enterprise-tier configurations with strong DPAs and no-retention commitments are the path. Document the configuration as evidence for any label scoping prototype-data work.
- **Data Protection label and AI-processed PII.** If AI features process personal data on behalf of OEM, the AI handling falls under Data Protection label requirements: lawful basis, purpose limitation, retention, sub-processor management.
- **Tightening label scope around AI use.** Some OEMs have begun adding AI-specific contract addenda. Suppliers expecting to use AI tools in OEM-relationship work should review label scope vs intended AI use ahead of assessment.

## Stefan-context implementation sketch

- Engagement-by-engagement: confirm OEM-required labels + assessment levels via client contract.
- Most plausible engagement-driven labels:
  - **Info Sec High + AL2** for general consulting work
  - **Info Sec High + AL3 + Prototype Protection Components** for work touching pre-series data
  - **Data Protection Standard + AL2** for work touching OEM customer PII
- Self-prep against VDA-ISA workbook regardless of formal assessment, as discipline for handling automotive-customer engagements.

## See also

- [[TISAX Cluster|cluster MOC]] · [[TISAX VDA-ISA Catalogue]] · [[TISAX Assessment Levels]] · [[TISAX Assessment Process]]
