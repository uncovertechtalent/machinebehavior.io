title: TISAX anchors
summary: Primary documents, operating bodies, audit providers, related standards, named voices, reference resources for the TISAX cluster.
parent: tisax
order: 6
labels: anchors, tisax
aliases: TISAX Anchors | TISAX Reading List | TISAX Sources
type: anchors
created: 2026-05-12
updated: 2026-05-12
origin: pillars/tisax/anchors.md
reviewed: no
---
> Primary documents, operating bodies, audit providers, related standards, named voices, reference resources for the TISAX cluster.

## Primary documents

- **VDA-ISA workbook** — the catalogue. Excel-format spreadsheet with controls, maturity-level criteria, scoring guidance. Current major version: 6.0 (late 2023), with maintenance updates through 2024-2025. Distributed by VDA via vda.de and via ENX participant portal.
- **TISAX Participant Handbook** — ENX-published operational document describing the assessment process, label types, registration steps, audit-provider engagement. Updated periodically; current ~2024-2025.
- **TISAX Assessment Provider Handbook** — operational guidance for audit providers. Less commonly read by suppliers but useful for understanding auditor expectations.
- **VDA-ISA criteria mapping** — VDA-published spreadsheet mapping VDA-ISA controls to ISO/IEC 27001:2022 Annex A and other reference frameworks. Useful for dual-implementation orgs.

## Operating bodies

- **ENX Association** — neutral operator. Frankfurt-based. enx.com. Maintains the registry, accredits audit providers, runs the portal. Annual participant fees fund operations.
- **VDA** (Verband der Automobilindustrie) — content owner. Authors and revises VDA-ISA. vda.de.

## Accredited audit providers

ENX-accredited audit providers as of 2026 (illustrative, not exhaustive; check enx.com for current list):

- **TÜV SÜD** (Munich)
- **TÜV Rheinland** (Cologne)
- **TÜV Nord** (Hannover)
- **TÜV Hessen**
- **DEKRA** (Stuttgart)
- **DQS** (Frankfurt)
- **KPMG**
- **Deloitte**
- **PwC**
- **EY**
- **BSI Group** (UK origin, German operations)
- **GRC partner firms** (specialist auditors with TISAX accreditation in addition to ISO 27001)

Auditor accreditation is checkable via the ENX portal participant view.

## Required and recommended companion standards

- **ISO/IEC 27001:2022** — the international ISMS standard. Most controls overlap; implementations typically converge.
- **ISO/IEC 27002:2022** — controls implementation guidance.
- **ISO/IEC 27005:2022** — risk management. Useful for risk-assessment methodology underlying VDA-ISA control selection.
- **ISO/IEC 27701:2019** — privacy information management. Complements VDA-ISA Data Protection module.
- **ISO/IEC 27017:2015** — cloud-specific controls. Useful when supplier uses cloud-hosted services for automotive customer data.
- **ISO/IEC 42001:2023** — AI management system. No formal TISAX integration yet, but practitioners are using it as an AI-specific overlay.
- **GDPR (EU 2016/679)** — privacy regulation. Data Protection module aligns explicitly.

## Adjacent automotive-sector standards

- **ISO/SAE 21434:2021** — Road vehicles — Cybersecurity engineering. Product-side cyber-security for vehicles. Different scope from TISAX (which is about supplier-org information security), but relevant for development partners working on connected / autonomous vehicle systems.
- **UN R155 / UN R156** — UN ECE regulations on vehicle cybersecurity (R155) and software update management (R156). Mandatory for vehicle type approval in UN member states from 2022.
- **ASPICE** (Automotive SPICE) — software process maturity model for automotive. Same SPICE roots as TISAX maturity levels. Common in development-partner relationships alongside TISAX.
- **VDA 6.x** — automotive quality management family (parallel to ISO 9001). Often required alongside TISAX in OEM contracts.

## Named practitioners and reference voices

TISAX is a smaller practitioner community than ISO 27001. Named voices include:

- **ENX Association staff** — public-facing communications, conference presentations, webinars. The most authoritative source on operational mechanics.
- **VDA Information Security Working Group** — authors the catalogue. Less individually-attributed than ENX side.
- **TÜV / DEKRA / KPMG senior auditors** — industry-conference presentations, particularly at VDA events and Hannover Messe. Surface common findings and emerging audit focus areas.
- **Mid-market German GRC consultancies** (KPMG GRC, Deloitte Risk Advisory, PwC, EY, plus specialist Mittelstand-focused firms) — practitioner content via industry publications.

For independent or critical voices, the field is thinner than for ISO 27001. Most TISAX writing is implementation-focused; critical analysis is rare in published form.

## Reference resources

- **enx.com** — official TISAX operating site. Participant portal, audit-provider list, handbook downloads.
- **vda.de** — VDA-ISA distribution. German-language primary.
- **VDA Information Security Conference** — annual industry event covering TISAX and adjacent automotive InfoSec.
- **Hannover Messe** — broader industrial event with VDA / ENX presence.
- **TISAX participant member webinars** — periodic ENX-hosted Q&A sessions, open to participants.

## Regulatory and procurement context

- **OEM contract clauses** — VW Group, BMW Group, Mercedes-Benz, Audi, Porsche, Bosch, Continental, ZF, Schaeffler, Hella, Mahle have TISAX flow-down clauses in supplier contracts. Wording varies but mechanism is consistent.
- **GDPR enforcement on automotive PII** — telematics, customer-relationship, employee, dealer-network data. Data Protection label increasingly required by OEMs handling EU resident data.
- **EU NIS2 Directive** — automotive critical-infrastructure operators in scope under member-state transposition. Overlap with TISAX coverage; non-equivalent.
- **EU AI Act** — high-risk classification for some automotive AI use cases (driver monitoring, ADAS) brings additional obligations. ISO 42001 + TISAX combined positioning emerging.

## See also

- [[TISAX Cluster|cluster MOC]] · [position](pillars/tisax/position.md)
- [[ISO 27001 Cluster|ISO 27001]] · [[ISO 27001 Family and Sector Variants]]
