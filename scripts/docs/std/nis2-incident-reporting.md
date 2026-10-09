title: NIS2 Incident Reporting
summary: Article 23 establishes the incident reporting regime.
parent: nis2
order: 100
labels: nis2, regulation-concept
aliases: NIS2 Incident Reporting | NIS2 Article 23 | NIS2 24h 72h | NIS2 Significant Incident
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nis2/NIS2 Incident Reporting.md
reviewed: no
---
> Article 23 establishes the incident reporting regime. Significant incidents must be notified via three-stage timeline: 24h early warning, 72h incident notification, 1-month final report. Plus intermediate progress reports. Tight timelines force pre-built response infrastructure.

## What triggers reporting

A "significant incident" is one that:

- Causes or is capable of causing severe operational disruption of services or financial loss for the entity concerned, OR
- Has affected or is capable of affecting other natural or legal persons by causing considerable material or non-material damage

The qualitative definition creates classification uncertainty in marginal cases. Implementing acts provide sector-specific specifications.

## Three-stage timeline

### Stage 1: Early warning (within 24 hours)

Within 24 hours of becoming aware of the significant incident.

Content:

- Indication of whether the incident is suspected to be caused by unlawful or malicious action.
- Indication of whether the incident is suspected to have cross-border impact.

Brief notification — minimum content. Aims to alert authorities and trigger coordination if needed.

### Stage 2: Incident notification (within 72 hours)

Within 72 hours of becoming aware.

Content:

- Update on the early warning.
- Initial assessment including severity, impact, indicators of compromise where available.

### Stage 3: Final report (within 1 month)

Within one month of submission of the incident notification.

Content:

- Detailed description of the incident, including severity and impact.
- Type of threat or root cause likely triggering the incident.
- Applied and ongoing mitigation measures.
- Cross-border impact where applicable.

### Intermediate progress reports

Where applicable, upon CSIRT or competent authority request, status updates between Stage 2 and Stage 3.

## "Awareness" of incident

The clock starts at awareness. Awareness is when the entity has reasonable grounds to believe an incident has occurred (not full forensic confirmation). Operational implication: early-warning notification often precedes complete understanding.

## Notification to recipients

Where appropriate, entities notify their service recipients of:

- Significant incidents likely to adversely affect the recipients
- Significant cyber threats and any measures or remedies that recipients can take

For severe cyber threats, entities also notify recipients of mitigation steps.

## To whom: competent authority or CSIRT

Member State designates whether reporting flows to competent authority, CSIRT, or both. DE: BSI as primary recipient. Other Member States vary.

## Voluntary reporting of cyber threats and near-misses

Article 30 allows voluntary reporting of:

- Cyber threats that could potentially affect the entity or others
- Near-miss incidents (would have qualified as significant if not for protective measures)

Voluntary reports do not result in penalty. Used for situational awareness.

## Cross-border coordination

Where incident affects multiple Member States:

- Competent authorities of affected Member States informed.
- ENISA may be informed for situational awareness.
- EU-CyCLONe coordination for large-scale incidents.

## Overlap with other regimes

Many incidents trigger reporting under multiple regulations:

- **NIS2 + GDPR**: personal data breach typically triggers both. GDPR Art 33 (72h) + NIS2 Art 23 (24h/72h/1m).
- **NIS2 + DORA**: financial services ICT incidents — DORA lex specialis but NIS2 reporting may still apply.
- **NIS2 + sector regulators**: financial, telecoms, energy may have sector-specific reporting.
- **NIS2 + AI Act**: serious incidents in AI systems may overlap.

Coordination mechanisms in development to reduce duplicate reporting; current state is parallel reporting for many incidents.

## Implementation evidence

Authority expects:

- Documented incident response procedure with NIS2 timelines incorporated.
- Pre-built notification templates (24h, 72h, 1m).
- Defined points of contact (entity-side + authority-side).
- Detection capability sufficient to identify incidents promptly.
- Communication channels tested.
- Recent incident response records (where applicable) demonstrating timeline adherence.

## Common gaps

- **24h capability missing.** Out-of-hours incident detection and decision-to-notify infrastructure absent.
- **Significant incident classification unclear.** No documented decision criteria; entity over- or under-reports.
- **Templates not pre-built.** Notification drafted under pressure during incident.
- **No connection to GDPR breach response.** Parallel obligations not integrated; duplicate work or missed obligations.
- **Recipient notification overlooked.** Article 23(2)(b) recipient notification obligation forgotten.

## SRE and AI-agent fit notes

### AI-related incidents to consider

- Model behavior shift affecting service quality (significant if severe operational impact)
- Vendor-side outage at model provider
- Prompt injection causing data exfiltration (also GDPR breach)
- Tool-misuse leading to service disruption
- RAG corpus compromise affecting outputs
- Agent action with adverse downstream effects

### Detection-to-notification pipeline

For 24h early warning:

- Detection sources (monitoring, alerting, user reports, vendor notifications)
- Triage process (is this a significant incident?)
- Authorization (who decides to notify)
- Notification channel (BSI Meldeplattform in DE, equivalent in other MS)
- Pre-built templates

### Vendor-side incident reporting

Model provider incidents:

- Vendor notifies customer (per DPA terms)
- Customer assesses NIS2 / GDPR / AI Act reporting obligations
- Customer reports to authorities as applicable
- Coordination with vendor on subsequent reporting

## Stefan-context implementation sketch

- For NIS2-scope client engagements: ensure 24h notification capability is built into client's incident response infrastructure.
- Pre-built notification templates aligned with DE BSI Meldeplattform.
- Integration with GDPR breach response workflow.
- Vendor-side incident notification flow documented.

## See also

- [[NIS2 Cluster|cluster MOC]] · [[NIS2 Security Measures]] · [[NIS2 Governance and Penalties]]
- [[GDPR Controller and Processor]] (Article 33 breach notification parallel)
