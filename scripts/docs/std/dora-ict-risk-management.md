title: DORA ICT Risk Management
summary: Articles 5-15 establish DORA's first pillar: the ICT risk management framework.
parent: dora
order: 100
labels: dora, regulation-concept
aliases: DORA ICT Risk Management | DORA Pillar 1 | DORA Articles 5-15
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/dora/DORA ICT Risk Management.md
reviewed: no
---
> Articles 5-15 establish DORA's first pillar: the ICT risk management framework. Comprehensive, integrated framework covering governance, identification, protection, detection, response, recovery, learning, communication. The management body is fully accountable.

## Governance (Article 5)

Management body of the financial entity:

- Has full responsibility for the ICT risk management framework.
- Approves the strategy, policies, procedures.
- Defines roles and responsibilities for ICT functions.
- Sets risk tolerance levels.
- Ensures appropriate budget.
- Ensures continuous training for management body members.
- Reviews framework periodically.

Cannot be delegated as a whole to operational level. Strong parallel to NIS2 Article 20 and ISO 27001 Cl 5.

## ICT risk management framework (Article 6)

Financial entity establishes ICT risk management framework that is:

- Documented.
- Reviewed at least once per year (more frequently for major changes).
- Subject to internal audit at least once every three years.
- Aligned with the entity's overall risk management framework.
- Integrated with business strategy and operations.

The framework includes strategies, policies, procedures, ICT protocols, tools.

## Identification (Article 8)

Entity identifies and documents:

- All ICT-supported business functions, roles, responsibilities, owners.
- Information assets.
- ICT assets.
- ICT third-party providers.
- Interconnections and interdependencies.

Updated continuously and at least annually. Map underpins all other risk management activities.

## Protection and prevention (Article 9)

Appropriate ICT security measures including:

- ICT security strategies, policies, procedures.
- Strong authentication mechanisms (MFA equivalent).
- Robust authorization.
- Cryptography for data confidentiality, integrity, authenticity.
- Network security.
- Endpoint security.
- Physical security of ICT systems.
- Patch management.
- Configuration management.

Risk-based and proportional. Cross-references ISO 27001 Annex A controls heavily.

## Detection (Article 10)

Continuous monitoring and detection mechanisms:

- Detect anomalous activities.
- Detect ICT-related incidents.
- Detect performance issues affecting business continuity.
- Identify single points of failure.
- Identify ICT-related risks.

Logging, monitoring, alerting capabilities required.

## Response and recovery (Article 11)

ICT business continuity policy with:

- ICT business continuity plans.
- ICT response and recovery plans.
- Adequate recovery time objectives (RTOs) and recovery point objectives (RPOs).
- Communication protocols for incidents.
- Tested annually at minimum.

Severe disruption scenarios — including pandemic, geopolitical, supply chain — must be considered.

## Backup policies and procedures (Article 12)

- Backup policies and procedures.
- Restoration tested regularly.
- Logical and physical separation of backups.
- Backup integrity protections.

## Learning and evolving (Article 13)

Post-incident reviews after every major ICT-related incident:

- Causes identified.
- Improvements identified.
- Action items tracked.
- Awareness programmes updated.

Continuous improvement embedded.

## Communication (Article 14)

Communication protocols for:

- Internal stakeholders during incidents.
- External stakeholders including customers, counterparties, regulators.
- Crisis communication.

Pre-defined communication plans with templates.

## Simplified framework for certain entities (Article 16)

Smaller entities (e.g., small institutions) can apply simplified ICT risk management framework:

- Lighter governance requirements.
- Proportional security measures.
- Risk-based scope adjustments.

Specifics in RTS.

## Bridge to ISO 27001

Article 6 framework ≈ ISO 27001 ISMS.
Article 8 identification ≈ ISO 27001 A.5.9 asset inventory.
Article 9 protection ≈ ISO 27001 Annex A.5-A.8.
Article 10 detection ≈ ISO 27001 A.8.15-A.8.16.
Article 11 response/recovery ≈ ISO 27001 A.5.24-A.5.30 + ISO 22301.
Article 12 backup ≈ ISO 27001 A.8.13.
Article 13 learning ≈ ISO 27001 A.5.27 + Cl 10.

ISO 27001 + ISO 22301 implementation provides ~75-85% of DORA Pillar 1 substantive coverage.

## SRE and AI-agent fit notes

### AI features in financial-entity ICT systems

AI features in financial entities are part of ICT-supported business functions. Subject to Article 6 framework. Specific considerations:

- **Identification (Art 8)**: AI features in asset register; dependencies on model providers identified.
- **Protection (Art 9)**: input validation, output validation, secure prompting, tool-scope discipline.
- **Detection (Art 10)**: anomalous AI behavior monitoring; vendor-side change detection.
- **Response/recovery (Art 11)**: AI-incident response plans; fallback to non-AI processing if needed.
- **Learning (Art 13)**: post-incident reviews of AI-related events.

### Vendor (model provider) ICT TPP status

Model providers are ICT third-party providers under DORA. Subject to:

- Pillar 4 third-party risk management (Art 28-44).
- Contractual requirements (Art 30 mandatory clauses).
- Register of information entry.

## Stefan-context implementation sketch

- For financial-services client work: leverage client's existing ICT risk management framework; document AI-specific extensions per Art 8-15.
- For vendor positioning: document own cybersecurity posture for client's register-of-information.

## See also

- [[DORA Cluster|cluster MOC]] · [[DORA Incident Reporting]] · [[DORA Resilience Testing]] · [[DORA ICT Third-Party Risk]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
