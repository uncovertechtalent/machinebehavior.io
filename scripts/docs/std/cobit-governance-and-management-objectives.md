title: COBIT Governance and Management Objectives
summary: Board-level. Evaluate stakeholder needs / conditions / options, Direct via policies, Monitor performance.
parent: cobit
order: 100
labels: cobit, framework-concept
aliases: COBIT Governance and Management Objectives | COBIT 40 Objectives | COBIT Five Domains | COBIT EDM APO BAI DSS MEA
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/cobit/COBIT Governance and Management Objectives.md
reviewed: no
---
## Governance domain — EDM (5 objectives)

Board-level. Evaluate stakeholder needs / conditions / options, Direct via policies, Monitor performance.

- **EDM01** Ensured Governance Framework Setting and Maintenance
- **EDM02** Ensured Benefits Delivery
- **EDM03** Ensured Risk Optimisation
- **EDM04** Ensured Resource Optimisation
- **EDM05** Ensured Stakeholder Engagement

## Management domain — APO (14 objectives)

Plan, organize:

- **APO01** Managed I&T Management Framework
- **APO02** Managed Strategy
- **APO03** Managed Enterprise Architecture
- **APO04** Managed Innovation
- **APO05** Managed Portfolio
- **APO06** Managed Budget and Costs
- **APO07** Managed Human Resources
- **APO08** Managed Relationships
- **APO09** Managed Service Agreements
- **APO10** Managed Vendors
- **APO11** Managed Quality
- **APO12** Managed Risk
- **APO13** Managed Security
- **APO14** Managed Data

## Management domain — BAI (11 objectives)

Build, acquire, implement:

- **BAI01** Managed Programs
- **BAI02** Managed Requirements Definition
- **BAI03** Managed Solutions Identification and Build
- **BAI04** Managed Availability and Capacity
- **BAI05** Managed Organisational Change
- **BAI06** Managed IT Changes
- **BAI07** Managed IT Change Acceptance and Transitioning
- **BAI08** Managed Knowledge
- **BAI09** Managed Assets
- **BAI10** Managed Configuration
- **BAI11** Managed Projects

## Management domain — DSS (6 objectives)

Deliver, service, support:

- **DSS01** Managed Operations
- **DSS02** Managed Service Requests and Incidents
- **DSS03** Managed Problems
- **DSS04** Managed Continuity
- **DSS05** Managed Security Services
- **DSS06** Managed Business Process Controls

## Management domain — MEA (4 objectives)

Monitor, evaluate, assess:

- **MEA01** Managed Performance and Conformance Monitoring
- **MEA02** Managed System of Internal Control
- **MEA03** Managed Compliance with External Requirements
- **MEA04** Managed Assurance

## Per objective

Each of the 40 has:

- **Purpose statement**
- **Description**
- **Mapping to enterprise goals**
- **Mapping to alignment goals**
- **Governance/management practices** — typically 4-7 per objective
- **Activities** per practice
- **Inputs and outputs** (work products)
- **Capability levels** 0-5

## Capability levels

Per objective:

- **0 Incomplete** — practice not implemented.
- **1 Initial** — basic implementation.
- **2 Managed** — performance managed.
- **3 Defined** — standardized process.
- **4 Quantitatively Managed** — metrics-driven.
- **5 Optimising** — continuous improvement.

Similar to SPICE / CMMI scales.

## Design factors application

Eleven design factors tailor governance system:

- Risk profile → emphasis on EDM03, APO12.
- I&T-related issues → specific BAI / DSS focus.
- Compliance requirements → MEA03 emphasis.
- Etc.

Tailoring produces priority order across the 40 objectives.

## Focus areas

ISACA publishes focus-area guides extending COBIT for specific contexts:

- **Information Security** — emphasizes APO13, DSS05.
- **DevOps** — emphasizes BAI06, BAI07, DSS02.
- **SMB** — proportional tailoring.
- **Risk** — emphasizes EDM03, APO12.
- **Digital Transformation**.

## Cross-framework mapping

COBIT 2019 maps practices to:

- ISO 27001 controls.
- NIST CSF subcategories.
- ITIL practices.
- Other frameworks.

Cross-references support multi-framework implementations.

## Bridge to ITIL

- COBIT BAI04 ↔ ITIL Availability + Capacity Management.
- COBIT BAI06 ↔ ITIL Change Enablement.
- COBIT BAI09-10 ↔ ITIL IT Asset Management + Service Configuration Management.
- COBIT DSS02 ↔ ITIL Incident + Service Request Management.
- COBIT DSS03 ↔ ITIL Problem Management.
- COBIT DSS04 ↔ ITIL Service Continuity Management.
- COBIT DSS05 ↔ ITIL Information Security Management.

ITIL implements operationally; COBIT governs.

## Bridge to ISO 27001

- COBIT APO13 + DSS05 align with ISO 27001 ISMS substantively.
- COBIT MEA03 supports ISO 27001 Cl 9.1 + A.5.31.
- COBIT EDM emphasizes board-level oversight; ISO 27001 Cl 5.

## SRE and AI-agent fit notes

For governance-strategy work:

- COBIT vocabulary aligns with board-level conversations.
- APO12 (Managed Risk) + APO13 (Managed Security) for cybersecurity governance.
- APO04 (Managed Innovation) for AI-adoption governance.
- BAI03 (Managed Solutions Identification and Build) for AI feature development.

## Stefan-context implementation sketch

- For governance-tier client work: COBIT vocabulary useful.
- For implementation-tier: ITIL primary, COBIT-aware.

## See also

- [[COBIT Cluster|cluster MOC]] · [[COBIT Controversies]]
- [[ITIL 4 Service Value System]] · [[ITIL 4 Practices]] · [[ISO 27001 Cluster]]
