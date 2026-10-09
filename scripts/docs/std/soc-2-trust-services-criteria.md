title: SOC 2 Trust Services Criteria
summary: Five TSC categories. Security is mandatory ("Common Criteria"); availability, processing integrity, confidentiality, privacy are optional based on service org choice.
parent: soc2
order: 100
labels: framework-concept, soc2
aliases: SOC 2 TSC | SOC 2 Trust Services Criteria | AICPA Trust Services Criteria | TSC Security Availability Processing Integrity Confidentiality Privacy
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/soc2/SOC 2 Trust Services Criteria.md
reviewed: no
---
> Five TSC categories. Security is mandatory ("Common Criteria"); availability, processing integrity, confidentiality, privacy are optional based on service org choice. Each TSC has criteria and points of focus drawn from COSO Internal Control — Integrated Framework.

## Security (Common Criteria, CC)

Mandatory. Nine CC sub-categories:

### CC1: Control Environment

- CC1.1: integrity and ethical values
- CC1.2: board oversight
- CC1.3: organizational structures
- CC1.4: commitment to competence
- CC1.5: accountability

### CC2: Communication and Information

- CC2.1: relevant information about objectives
- CC2.2: internal communication of information
- CC2.3: external communication of information

### CC3: Risk Assessment

- CC3.1: objectives specified
- CC3.2: risks identified
- CC3.3: fraud risk assessment
- CC3.4: significant change identification

### CC4: Monitoring Activities

- CC4.1: ongoing and separate evaluations
- CC4.2: evaluating and communicating deficiencies

### CC5: Control Activities

- CC5.1: control activities selected and developed
- CC5.2: technology controls
- CC5.3: policies and procedures

### CC6: Logical and Physical Access Controls

- CC6.1: logical access
- CC6.2: account management
- CC6.3: removal of access
- CC6.4: physical access
- CC6.5: physical access removal
- CC6.6: logical access protection
- CC6.7: data transmission
- CC6.8: protection against malicious software

### CC7: System Operations

- CC7.1: vulnerability detection
- CC7.2: anomaly monitoring
- CC7.3: incident response
- CC7.4: incident recovery
- CC7.5: recovery from outages

### CC8: Change Management

- CC8.1: change management process

### CC9: Risk Mitigation

- CC9.1: vendor / business partner risk
- CC9.2: vendor / business partner management

## Availability

Optional TSC. Criteria:

- A1.1: capacity / system performance
- A1.2: environmental protections
- A1.3: backup / restore

## Processing Integrity

Optional. System processing is complete, valid, accurate, timely, authorized.

- PI1.1: definitions and policies
- PI1.2: input controls
- PI1.3: processing controls
- PI1.4: output controls
- PI1.5: storage controls

## Confidentiality

Optional. Information designated confidential protected.

- C1.1: identification and protection of confidential information
- C1.2: destruction of confidential information

## Privacy

Optional. Personal information collected, used, retained, disclosed, disposed per commitments.

- P1.0: management policies for privacy
- P2.0: notice
- P3.0: choice and consent
- P4.0: collection
- P5.0: use, retention, disposal
- P6.0: access (data subject rights)
- P7.0: disclosure to third parties
- P8.0: security for privacy
- P9.0: quality
- P10.0: monitoring and enforcement

GDPR overlap substantial; Privacy TSC partially aligns with GDPR principles.

## Selecting TSC categories

Service org chooses which optional TSCs to include in scope:

- **Security only** — minimum scope.
- **Security + Availability** — common for SaaS.
- **Security + Availability + Confidentiality** — common for SaaS handling customer business data.
- **Security + Availability + Confidentiality + Privacy** — common when processing personal data.
- **All five** — comprehensive.

Customer-procurement preferences drive selection.

## Points of focus

Each TSC sub-category has "points of focus" — illustrative considerations to assess whether the criterion is met. Not mandatory controls; org designs controls addressing relevant points of focus.

## SOC 2 control activities

Service org designs control activities mapping to TSC criteria. Control activities are specific operational practices:

- Access reviews (CC6.2, CC6.3)
- Vulnerability scanning (CC7.1)
- Incident response (CC7.3, CC7.4)
- Change management (CC8.1)
- Vendor management (CC9.1, CC9.2)
- Encryption (CC6.7)
- Logging and monitoring (CC4.1, CC7.2)
- Training (CC2.2, CC4.2)

Auditor evaluates whether controls are suitably designed (Type 1) and operating effectively (Type 2).

## SRE and AI-agent fit notes

### AI features in SOC 2 scope

AI features part of the service org's system are in SOC 2 scope:

- CC6.7 data transmission: encryption of prompts, outputs, training data.
- CC6.1-CC6.6 logical access: control over AI feature access.
- CC7.2 anomaly monitoring: agent behavior monitoring.
- CC7.3 incident response: AI-incident response procedures.
- CC8.1 change management: system prompt / tool scope versioning.
- CC9.1-CC9.2 vendor risk: model provider due diligence.

### Privacy TSC for AI features processing personal data

When AI features process personal data, Privacy TSC adds:

- P3.0 consent (where applicable)
- P5.0 retention (training data, AI logs)
- P7.0 disclosure to third parties (model providers)
- P8.0 security

GDPR + SOC 2 Privacy TSC overlap substantial for orgs subject to both.

## Stefan-context implementation sketch

- For US-customer-facing AI / SaaS engagements: SOC 2 TSC categories per customer demand.
- Map AI feature controls to TSC criteria.
- For combined SOC 2 + ISO 27001 implementations: single control set with dual mapping.

## See also

- [[SOC 2 Cluster|cluster MOC]] · [[SOC 2 Type 1 vs Type 2]] · [[SOC 2 Assessment Process]] · [[SOC 2 vs ISO 27001]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
