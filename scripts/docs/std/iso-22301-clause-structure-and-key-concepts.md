title: ISO 22301 Clause Structure and Key Concepts
summary: Same structural pattern as ISO 27001 / ISO.
parent: iso-22301
order: 100
labels: framework-concept, iso-22301
aliases: ISO 22301 Clause Structure | ISO 22301 BIA | ISO 22301 RTO MBCO | ISO 22301 Key Concepts
type: framework-concept
created: 2026-05-12
updated: 2026-10-04
origin: pillars/iso-22301/ISO 22301 Clause Structure and Key Concepts.md
reviewed: no
---
## Clauses 4-10 (Annex SL aligned)

Same structural pattern as ISO 27001 / ISO 42001:

- **Cl 4 Context** — interested parties, scope of BCMS.
- **Cl 5 Leadership** — top management commitment, policy, roles.
- **Cl 6 Planning** — risks/opportunities, BCM objectives.
- **Cl 7 Support** — resources, competence, awareness, communication, documented information.
- **Cl 8 Operation** — the BCMS-specific clause:
  - 8.1 Operational planning and control
  - 8.2 Business impact analysis and risk assessment
  - 8.3 Business continuity strategies and solutions
  - 8.4 Business continuity plans and procedures
  - 8.5 Exercise programme
  - 8.6 Evaluation of business continuity documentation and capabilities
  - (Corrected 2026-10-03 against the ISO 22301:2019 table of contents, official iTeh sample PDF. The earlier list had 8.6 as exercise programme and 8.7 as evaluation; 8.7 does not exist in the 2019 edition.)
- **Cl 9 Performance Evaluation** — monitoring, internal audit, management review.
- **Cl 10 Improvement** — nonconformity and corrective action; continual improvement.

## Key concepts

### Business Impact Analysis (BIA)

Process to identify time-critical activities and quantify continuity requirements. Outputs:

- **Maximum Tolerable Period of Disruption (MTPD)** — longest disruption tolerable before consequences become unacceptable.
- **Recovery Time Objective (RTO)** — target time to restore activity. RTO < MTPD.
- **Recovery Point Objective (RPO)** — maximum tolerable data loss in time.
- **Minimum Business Continuity Objective (MBCO)** — minimum service level during disruption.
- **Recovery Capacity Objective** — capacity needed to meet MBCO.

### Risk Assessment

Identify risks of disruption to time-critical activities. Inputs to BC strategy.

### BC Strategy

Choices about how to ensure continuity:

- Alternative sites (cold, warm, hot).
- Alternative suppliers.
- Manual workarounds.
- Reduced-service operations.
- Insurance.

### BC Plans

Documented plans:

- **Incident Response Plan** — initial response.
- **Business Continuity Plan** — sustained alternative-mode operations.
- **Disaster Recovery Plan** — ICT-specific recovery (overlaps with ISO 27031).

### Exercises and Testing

Regular tested plans:

- Tabletop exercises.
- Walkthrough exercises.
- Simulation exercises.
- Live exercises.
- IT-specific failover tests.

Annual minimum; more frequent for high-criticality activities.

### Evaluation

- Internal audit (Cl 9.2).
- Management review (Cl 9.3).
- Post-incident review.
- Exercise debriefs.

## Implementation patterns

### Combined ISO 27001 + ISO 22301

- Single management system with shared Cl 4-10 implementation.
- Distinct ISO 27001 ISMS scope + ISO 22301 BCMS scope.
- Combined internal audit programme.
- Combined management review with both topics.
- Combined certification audit (capable certification bodies).

### DORA-aligned BC

DORA Article 11 ICT business continuity requirements align with ISO 22301 substantially. Financial entities subject to both can use ISO 22301 implementation as DORA evidence.

### NIS2-aligned BC

NIS2 Article 21(c) business continuity requirement aligns with ISO 22301 substantially.

## SRE and AI-agent fit notes

### BC for AI features

AI-feature business continuity considerations:

- **Vendor outage scenarios**: model provider unavailability; fallback to alternative provider or non-AI processing.
- **Vendor exit strategy**: ability to switch providers; data portability.
- **AI-feature criticality**: BIA includes AI features per their business impact.
- **AI-incident recovery**: post-AI-incident recovery procedures.

### DR for AI infrastructure

- RPO / RTO for AI feature databases, vector stores, model state.
- Backup of system prompts, tool scopes, configurations.
- Recovery procedures tested.

## Stefan-context implementation sketch

- For client engagements: ISO 22301 vocabulary supplements ISO 27001.
- For SRE work: BC discipline integrated with reliability engineering.
- For AI features: vendor-outage scenarios in BIA.

## See also

- [[ISO 22301 Cluster|cluster MOC]] · [[ISO 22301 Controversies]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.29-A.5.30) · [[DORA ICT Risk Management]]
