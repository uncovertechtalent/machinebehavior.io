title: DORA Incident Reporting
summary: Articles 17-23 establish DORA's second pillar: ICT-related incident management, classification, reporting.
parent: dora
order: 100
labels: dora, regulation-concept
aliases: DORA Incident Reporting | DORA Pillar 2 | DORA Articles 17-23
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/dora/DORA Incident Reporting.md
reviewed: no
---
> Articles 17-23 establish DORA's second pillar: ICT-related incident management, classification, reporting. Mandatory classification methodology; harmonized reporting timelines; voluntary cyber threat reporting.

## Incident management process (Article 17)

Financial entity establishes process for:

- Detection
- Logging
- Categorization
- Initial response
- Containment
- Investigation
- Resolution
- Recovery
- Post-incident analysis

Process is documented, tested, integrated with broader ICT risk management framework.

## Classification (Article 18 + RTS)

Major ICT-related incidents classified based on criteria:

- **Number of clients / financial counterparts affected**
- **Reputational impact**
- **Duration of the incident**
- **Geographical spread**
- **Data losses (confidentiality, integrity, availability of data)**
- **Criticality of services affected**
- **Economic impact**

Thresholds defined in RTS. Incident is "major" when criteria thresholds met.

Significant cyber threats (Art 18(2)) — separate classification for serious threats that did not materialize as incidents.

## Reporting timeline (Article 19)

Three-stage reporting for major ICT-related incidents:

- **Initial notification** — within 4 hours of incident classification as major (or sooner per RTS).
- **Intermediate report** — at specified intervals (per RTS).
- **Final report** — within 1 month of incident resolution.

DORA timelines are tighter than NIS2 (24h early warning vs DORA initial 4h).

Reporting flows to the competent authority of the financial entity.

## Templates and procedures (Article 20)

ESAs publish harmonized templates and procedures via RTS/ITS. Reporting format standardized across financial sector.

## Centralized reporting platform (Article 21)

ESAs may establish a single EU-wide reporting hub. Initial implementation through Member State competent authorities; centralized hub planned.

## Feedback to financial entity (Article 22)

Competent authority provides:

- Acknowledgement of receipt.
- Where appropriate, guidance on mitigation steps.
- Information on related incidents that may affect the entity.

Information-sharing two-way; entities get feedback as well as report.

## Information sharing on threats (Article 23 / Article 45)

Financial entities can voluntarily share cyber threat information with peers via information-sharing arrangements:

- **Threat intelligence**
- **Indicators of compromise**
- **Tactics, techniques, procedures (TTPs)**
- **Mitigation strategies**

Subject to data protection, competition law, confidentiality safeguards.

## Overlap with adjacent reporting regimes

Financial entity incidents may trigger reporting under multiple regimes:

- **DORA** (financial-services specific)
- **GDPR** (if personal data breach) — 72h to DPA
- **NIS2** — typically displaced by DORA for financial entities
- **Sector-specific** (e.g., banking secrecy, market abuse) — may apply
- **MiCA** (for crypto asset service providers)

DORA serves as the primary financial-sector reporting channel; integration with adjacent regimes via national competent authority coordination.

## Bridge to ISO 27001 and NIS2

ISO 27001 A.5.24-A.5.28 incident management provides operational foundation. DORA adds:

- Specific classification criteria (Art 18).
- Specific timeline (4h initial vs ISO's "without undue delay").
- Specific reporting templates.
- Mandatory regulatory destination.

NIS2 Art 23 reporting (24h/72h/1m) is parallel structure but generally displaced by DORA for financial entities.

## SRE and AI-agent fit notes

### AI-related incidents in financial services

Incidents involving AI features triggering DORA reporting:

- AI feature misclassification of financial transactions (e.g., fraud detection failure).
- Model behavior change causing service degradation.
- Vendor-side AI provider outage affecting financial service.
- Prompt injection causing data exfiltration.
- AI-feature unavailability affecting critical financial functions.

### Detection and reporting infrastructure

- Detection sources: monitoring, alerting, customer reports, vendor notifications.
- Classification: rapid assessment against Art 18 thresholds.
- Notification: pre-built templates aligned with RTS format.
- Channel: BaFin Meldewesen in DE; equivalent in other MS.

## Stefan-context implementation sketch

- For financial-services client engagements: ensure 4h notification capability (tighter than NIS2).
- Integration with GDPR breach response.
- AI-incident classification process documented.
- Vendor-side notification flow with model providers.

## See also

- [[DORA Cluster|cluster MOC]] · [[DORA ICT Risk Management]] · [[DORA Resilience Testing]] · [[DORA ICT Third-Party Risk]]
- [[NIS2 Incident Reporting]] (parallel structure) · [[GDPR Controller and Processor]] (breach reporting)
