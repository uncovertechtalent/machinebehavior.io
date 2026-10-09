title: DORA ICT Third-Party Risk
summary: Articles 28-44 establish DORA's fourth pillar: management of ICT third-party risk.
parent: dora
order: 100
labels: dora, regulation-concept
aliases: DORA ICT Third-Party Risk | DORA Pillar 4 | DORA Articles 28-44 | DORA CTPP | DORA Critical ICT Third-Party Providers
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/dora/DORA ICT Third-Party Risk.md
reviewed: no
---
> Articles 28-44 establish DORA's fourth pillar: management of ICT third-party risk. Comprehensive obligations on financial entities for managing TPP relationships, plus Union-level oversight of critical ICT third-party providers (CTPPs).

## General principles (Articles 28-29)

Financial entity remains fully responsible for compliance with regulatory obligations regardless of outsourcing to ICT third-party providers. Cannot delegate ultimate accountability.

### ICT third-party risk strategy (Article 28(2))

Strategy on the use of ICT services covering:

- Concentration risk
- Substitutability assessment
- Exit strategies
- Multi-vendor approach where appropriate

### Register of information (Article 28(3))

Financial entity maintains register of all ICT TPP contractual arrangements:

- Contractor identity
- Service nature
- Service criticality (supports critical or important functions vs not)
- Location of data processing
- Sub-processors
- Risk assessment
- Contract terms summary
- Performance metrics

Register submitted to competent authority periodically. ITS standardizes the format.

### Pre-contractual analysis (Article 28(7))

Before entering ICT service contracts:

- Risk assessment
- Due diligence on the TPP
- Assessment of TPP's compliance with applicable regulation
- Assessment of TPP's ability to meet entity's requirements

### Concentration risk (Article 29)

Entity assesses and manages concentration risk:

- Single-TPP dependencies
- Multiple-TPP arrangements with same underlying provider
- Geographical concentration
- Substitutability constraints

## Contractual provisions (Article 30)

Mandatory contract clauses with ICT TPPs supporting critical or important functions:

### Article 30(2) general clauses

For all ICT TPP contracts:

- Clear and complete description of services
- Locations of service provision and data processing
- Personal data handling provisions
- Data accessibility, recovery, return in case of contract termination
- Service level agreements with performance targets
- Notification obligations
- Cooperation with competent authorities
- Termination rights
- Service quality monitoring rights

### Article 30(3) additional clauses for critical/important function support

Additional clauses:

- Right to monitor TPP performance continuously
- Right to inspect and audit (or accept third-party audits)
- Right to access TPP premises
- Cooperation with competent authority access
- Exit strategy provisions
- Service continuity during transition
- Subcontracting restrictions and approval
- Insurance coverage

### Article 30(7) mandatory inclusion

Member States ensure contracts have these clauses. National competent authorities can require contract modifications.

## Sub-outsourcing / subcontracting (Articles 30, 33)

TPP can sub-outsource only with controller authorization. Sub-processors:

- Subject to flow-down requirements equivalent to original contract.
- Identified in register of information.
- Subject to entity's monitoring rights.

RTS specifies subcontracting conditions for critical / important functions.

## Critical ICT third-party providers (Articles 31-44)

Subset of ICT TPPs designated as CTPP — subject to Union-level oversight.

### CTPP designation criteria (Article 31)

ESAs designate based on:

- **Systemic impact**: impact of CTPP failure on financial sector stability.
- **Substitutability**: difficulty replacing CTPP.
- **Reliance**: extent of financial entity reliance.
- **Number of financial entities** using the CTPP.
- **Total value of services**.

Likely CTPP designations: major cloud providers (AWS, Microsoft Azure, Google Cloud, IBM Cloud), major SaaS providers serving financial sector, specialized financial-services TPPs.

### Joint Oversight Mechanism (Article 32)

For each CTPP:

- **Lead Overseer** designated (one of ESAs).
- **Joint Oversight Network**: ESAs cooperate on CTPP oversight.

### Lead Overseer powers (Articles 35-39)

- Information requests
- General investigations
- On-site inspections at CTPP premises
- Requesting CTPP cooperation with financial entity audits
- Issuing recommendations to CTPPs
- Imposing periodic penalty payments

### CTPP cooperation obligations

CTPPs must:

- Cooperate with Lead Overseer.
- Provide information.
- Allow inspections.
- Implement recommendations (or justify non-implementation).

### Where CTPP non-cooperative

Lead Overseer can recommend financial entities terminate CTPP relationships or modify them. Significant business impact for non-cooperative CTPP.

### Penalty payments

Lead Overseer can impose periodic penalty payments on non-cooperative CTPPs — daily fines up to 1% of average daily worldwide turnover.

## Concentration risk at Union level (Article 44)

ESAs assess Union-level concentration risk in ICT third-party services. Can:

- Issue guidelines.
- Identify systemic concentration.
- Recommend remediation.

## Bridge to ISO 27001

ISO 27001 A.5.19-A.5.23 supplier relationships provide foundational discipline. DORA adds:

- More prescriptive contract clauses.
- Register of information format.
- Substitutability and exit planning emphasis.
- Union-level CTPP oversight (no ISO 27001 equivalent).

ISO 27001-implementing financial entities still need DORA-specific extensions.

## SRE and AI-agent fit notes

### Model providers as ICT TPPs

Anthropic, OpenAI, Google, Cohere, Mistral, others providing model APIs to financial entities are ICT third-party providers. Subject to:

- Contract clauses (Art 30).
- Register inclusion.
- Risk assessment.
- Potential CTPP designation (largest providers serving multiple financial entities).

### Cloud providers as likely CTPPs

AWS, Azure, Google Cloud, IBM Cloud likely candidates for CTPP designation given:

- Financial-sector penetration.
- Substitutability challenges.
- Systemic impact potential.

CTPP designation brings Lead Overseer oversight to vendor; affects vendor commercial terms with financial customers.

### Contract negotiation for AI vendors

Financial-services AI vendor contracts must include Article 30(3) clauses for critical-function support:

- Audit rights
- Inspection rights
- Exit provisions
- Subcontracting controls

Standard model-vendor enterprise terms typically need DORA-specific addenda.

## Stefan-context implementation sketch

- For financial-services client engagements: support vendor due diligence on AI / cloud providers.
- For consultancy positioning serving financial customers: ICT TPP status — expect contract clauses, register inclusion, audit cooperation.
- Document own cybersecurity posture for financial entity register-of-information.

## See also

- [[DORA Cluster|cluster MOC]] · [[DORA ICT Risk Management]] · [[DORA Governance and Penalties]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.19-A.5.23 supplier relationships)
