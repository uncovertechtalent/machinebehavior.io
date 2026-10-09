title: NIS2
summary: Map of Directive (EU) 2022/2555, the NIS2 Directive.
parent: index
order: 50
labels: cybersecurity-regulation, eu-regulation, moc, nis2
aliases: NIS2 Cluster | NIS2 | NIS2 Directive | Directive 2022/2555 | EU NIS2
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nis2/NIS2 Cluster.md
reviewed: no
---
> Map of Directive (EU) 2022/2555 — the NIS2 Directive. Successor to the original NIS Directive (2016/1148). Cybersecurity for essential and important entities across the EU. Member state transposition deadline 17 October 2024; enforcement ramping through 2025-2026. Reference cluster for EU cybersecurity compliance work, broadened sector scope (energy, transport, banking, healthcare, drinking water, waste water, digital infrastructure, ICT service management, public administration, space, postal/courier, waste management, chemicals, food, manufacturing, digital providers, research).

## Anchors

- [position](pillars/nis2/position.md): current view, dated, revisable
- [anchors](pillars/nis2/anchors.md): primary text, ENISA, national authorities, Member State transposition

## Provenance

- **NIS Directive (2016/1148)** — original Network and Information Systems Directive. In force 2018-2024.
- **Commission review** — 2020. Identified gaps: inconsistent scope across Member States, low maturity for essential service operators, weak enforcement.
- **NIS2 proposal** — December 2020.
- **Trilogue negotiations** — 2021-2022.
- **NIS2 adopted** — 14 December 2022.
- **OJEU publication** — 27 December 2022.
- **In force** — 16 January 2023.
- **Transposition deadline** — 17 October 2024 (Member States transpose into national law).
- **Replaces NIS Directive** — from 18 October 2024.
- **Enforcement** — ramping through 2025-2026 as national laws operationalize.

## What NIS2 is, in one paragraph

NIS2 is the EU's cybersecurity directive establishing a high common level of cybersecurity across the Union. Applies to essential entities (high-criticality sectors) and important entities (other critical sectors). Imposes cybersecurity risk management measures (Art 21), incident reporting obligations (Art 23), management body accountability (Art 20), supervision and enforcement by national competent authorities, penalties up to €10M or 2% of global annual turnover (essential entities) / €7M or 1.4% (important entities). Significantly broadens scope vs original NIS Directive: more sectors, lower size threshold, harder requirements.

## Scope: essential vs important entities

NIS2 distinguishes two tiers based on sector and size.

### Essential entities (Annex I — high-criticality sectors)

- Energy (electricity, district heating/cooling, oil, gas, hydrogen)
- Transport (air, rail, water, road)
- Banking
- Financial market infrastructure
- Health (healthcare providers, EU reference laboratories, medical research, pharmaceuticals, medical device manufacturers)
- Drinking water
- Waste water
- Digital infrastructure (IXPs, DNS service providers, TLD name registries, cloud service providers, data center service providers, content delivery network providers, trust service providers, public electronic communications networks/services)
- ICT service management (managed service providers, managed security service providers)
- Public administration (central, regional)
- Space

### Important entities (Annex II — other critical sectors)

- Postal and courier services
- Waste management
- Manufacture / production / distribution of chemicals
- Production / processing / distribution of food
- Manufacturing (medical devices, computer/electronic/optical products, electrical equipment, machinery, motor vehicles, other transport equipment)
- Digital providers (online marketplaces, online search engines, social networking services platforms)
- Research organisations

### Size thresholds

Default: medium and large entities in Annex I/II sectors.

- **Medium**: 50+ staff or annual turnover/balance sheet >€10M.
- **Large**: 250+ staff or annual turnover >€50M or balance sheet >€43M.

Exceptions where smaller entities included regardless of size: trust service providers, DNS service providers, TLD registries, providers of public electronic communications networks/services, others critical to the entity's sector.

Member States can extend scope nationally.

Detail in [[NIS2 Scope and Entities]].

## Cybersecurity risk-management measures (Article 21)

Essential and important entities must take "appropriate and proportionate technical, operational and organisational measures" to manage cybersecurity risks. Article 21(2) lists minimum measures:

- (a) Policies on risk analysis and information system security
- (b) Incident handling
- (c) Business continuity (backup management, disaster recovery, crisis management)
- (d) Supply chain security (security in supplier relationships and direct upstream providers)
- (e) Security in network and information systems acquisition, development, maintenance (vulnerability handling, disclosure)
- (f) Policies and procedures to assess effectiveness of risk-management measures
- (g) Basic cyber hygiene practices and cybersecurity training
- (h) Policies and procedures on use of cryptography (and encryption)
- (i) Human resources security, access control, asset management
- (j) Use of MFA, secured voice/video/text communications, secured emergency communications

Detail in [[NIS2 Security Measures]].

## Incident reporting (Article 23)

Significant incidents must be reported via three-stage timeline:

1. **Early warning** — within 24 hours of awareness. Indication of whether suspected to be caused by unlawful or malicious action or to have cross-border impact.
2. **Incident notification** — within 72 hours of awareness. Update including initial assessment of severity / impact / indicators of compromise.
3. **Final report** — within one month of notification. Detailed description of incident, severity, impact, threat type, mitigation measures, cross-border impact.

Intermediate progress reports also required.

A "significant incident" is one that causes (or is capable of causing) severe operational disruption or financial loss, or affects natural or legal persons with considerable material or non-material damage.

Detail in [[NIS2 Incident Reporting]].

## Management body accountability (Article 20)

Management bodies of essential/important entities must:

- Approve cybersecurity risk-management measures.
- Oversee implementation.
- Be held liable for non-compliance.
- Follow training to gain sufficient knowledge to identify risks and assess management practices.

Management body accountability is one of NIS2's most consequential changes vs NIS1.

## Governance and enforcement

### National competent authorities

Each Member State designates competent authorities for NIS2.

### National cybersecurity strategies

Member States adopt national cybersecurity strategies.

### CSIRT network

National CSIRTs cooperate via the CSIRTs network.

### EU-CyCLONe

Cyber Crisis Liaison Organisation Network — operational cooperation for large-scale incidents.

### ENISA

Coordinates implementation support. Issues guidelines. Threat-landscape reporting.

### Cooperation Group

EU-level cooperation among Member States, Commission, ENISA.

### Penalties (Article 34)

- **Essential entities**: administrative fines up to maximum of €10M or 2% of total worldwide annual turnover (whichever higher).
- **Important entities**: administrative fines up to maximum of €7M or 1.4% of total worldwide annual turnover (whichever higher).

Plus management body liability and other corrective measures.

Detail in [[NIS2 Governance and Penalties]].

## NIS2 vs original NIS Directive

| Aspect | NIS Directive (2016/1148) | NIS2 (2022/2555) |
|---|---|---|
| Entity classification | OES (operators of essential services) + DSP (digital service providers) | Essential entities + Important entities |
| Scope (sectors) | 7 essential sectors | 18 sectors |
| Size threshold | Member State discretion | Harmonized medium+/large default |
| Identification | Member State identifies OES | Self-identification, harmonized |
| Security measures | General requirement | Article 21 minimum measures list |
| Reporting timeline | "Without undue delay" | 24h early warning + 72h notification + 1m final |
| Management liability | Limited | Explicit (Art 20) |
| Penalties | Member State discretion | Harmonized up to €10M / 2% |
| Supervision | Reactive primarily | Proactive (essential) + reactive (important) |

NIS2 is materially heavier than NIS1.

## NIS2 vs ISO 27001

NIS2 is regulation; ISO 27001 is voluntary standard. Many NIS2 Article 21 measures map directly to ISO 27001 Annex A controls. ISO 27001 certification helps demonstrate NIS2 compliance but does not substitute. Detail in [[NIS2 vs ISO 27001]].

## Why this matters for SRE and AI-agent work

- **Many client orgs in scope.** Mittelstand manufacturers, healthcare providers, digital infrastructure, ICT service providers, cloud customers — large swathes of typical SRE client base.
- **Supply chain security (Art 21(d))** requires due diligence on direct upstream providers. Model vendors, cloud providers, SaaS providers all in scope.
- **Incident reporting timelines are tight.** 24h early warning requires response infrastructure.
- **Management body liability.** Cybersecurity at board level by mandate.
- **Cross-cutting with DORA (financial), CRA (digital products), AI Act, GDPR.** Integrated compliance work.

## Stefan-context relevance

Stefan does SRE / staff-engineer-track work touching:

- Mittelstand clients increasingly in NIS2 scope (manufacturing, healthcare, ICT services)
- Cloud and managed-service vendor relationships (supply chain considerations)
- Incident-response engagement work
- DE transposition — NIS2UmsuCG passed late 2024 / early 2025

Cluster atoms should:

- Stay regulation-grounded with article references
- Bridge NIS2 obligations to ISO 27001 / 27002 implementation work
- Surface DE-specific transposition specifics where load-bearing
- Track sector-specific implementation patterns

## Related clusters and atoms

- [[ISO 27001 Cluster|ISO 27001]] — close control overlap with NIS2 Art 21
- [[DORA Cluster|DORA]] — financial services ICT resilience (overlaps with NIS2)
- [[Cyber Resilience Act Cluster|Cyber Resilience Act]] — product cybersecurity (overlaps)
- [[GDPR Cluster|GDPR]] — incident reporting overlap; both regimes co-apply
- [[ITIL Cluster|ITIL]] — service management ties

## Conventions for this cluster

- Atoms named `NIS2 <Topic>.md` with consistent structure
- Article references cited explicitly
- DE transposition (NIS2UmsuCG) noted where divergent
- Cross-link to ISO 27001 / DORA / CRA / GDPR

## See also

[[NIS2 Cluster]] (pillars MOC) · [position](pillars/nis2/position.md) · [anchors](pillars/nis2/anchors.md) · [[ISO 27001 Cluster]] · [[DORA Cluster]] · [[GDPR Cluster]]
