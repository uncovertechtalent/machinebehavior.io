title: NIS2 Security Measures
summary: Article 21 establishes the cybersecurity risk-management measures required of essential and important entities.
parent: nis2
order: 100
labels: nis2, regulation-concept
aliases: NIS2 Security Measures | NIS2 Article 21 | NIS2 Risk Management Measures
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nis2/NIS2 Security Measures.md
reviewed: no
---
> Article 21 establishes the cybersecurity risk-management measures required of essential and important entities. Ten minimum measures with all-hazards approach. Implementation must be appropriate and proportionate to risk.

## Article 21(1) general obligation

Essential and important entities shall take appropriate and proportionate technical, operational, and organisational measures to manage risks to security of their network and information systems and to prevent or minimise the impact of incidents on recipients and on other services.

Proportionality factors:

- State of the art
- Implementation costs
- Entity size
- Likelihood and severity of incidents
- Societal and economic impact

## Article 21(2) minimum measures

Ten measures the entity must implement:

### (a) Policies on risk analysis and information system security

Policies governing risk management and information security. ISO 27001 Cl 5.2 alignment.

### (b) Incident handling

Procedures for detecting, responding to, recovering from incidents. Connects to Article 23 reporting and ISO 27001 A.5.24-A.5.28.

### (c) Business continuity

Backup management, disaster recovery, crisis management. ISO 22301 + ISO 27001 A.5.29-A.5.30 alignment.

### (d) Supply chain security

Security aspects in relationships between entity and direct upstream suppliers and service providers. Includes:

- Supplier risk assessment
- Contractual security requirements
- Ongoing monitoring
- Specific consideration of vulnerabilities in suppliers and service providers
- Quality of cybersecurity practices including secure development

Cross-references ISO 27001 A.5.19-A.5.23.

For AI / SRE work: model vendors, cloud providers, SaaS providers all in scope.

### (e) Security in network and information systems acquisition, development, maintenance

Including vulnerability handling and disclosure. ISO 27001 A.8.25-A.8.30 alignment. Secure development lifecycle.

### (f) Policies and procedures to assess effectiveness of cybersecurity risk-management measures

Internal audit, metrics, continuous improvement. ISO 27001 Cl 9 + Cl 10 alignment.

### (g) Basic cyber hygiene practices and cybersecurity training

For staff. ISO 27001 A.6.3 + Cl 7.2 + Cl 7.3 alignment.

### (h) Policies and procedures regarding use of cryptography and encryption

ISO 27001 A.8.24 alignment.

### (i) Human resources security, access control policies, asset management

Combined people / access / asset controls. ISO 27001 A.5.9-A.5.18 + A.6 alignment.

### (j) Use of MFA / continuous authentication / secured communications

Multi-factor authentication, continuous authentication where applicable. Secured voice/video/text communications. Secured emergency communications. ISO 27001 A.5.17 + A.8.5 + A.8.21 alignment.

## Article 21(3) Member State enhancements

Member States may require essential and important entities to use particular ICT products, ICT services, or ICT processes that comply with European cybersecurity certification schemes per Regulation (EU) 2019/881.

## Article 21(5) Commission implementing acts

Commission empowered to adopt implementing acts laying down technical and methodological requirements. First implementing acts published 2024-2025 for specific sector technical requirements.

## DE-specific specifications

NIS2UmsuCG specifies implementation expectations. BSI guidance further details technical and organizational measures expected. KRITIS-Bausteine (BSI building blocks) provide sector-specific guidance.

## Implementation evidence

Auditor/authority expects:

- Documented policies covering each (a)-(j) area.
- Risk assessment with identified risks and treatments.
- Procedures with operational evidence (executed examples).
- Training records.
- Audit logs / monitoring evidence.
- Supplier security records.
- Incident response procedures (tested).
- Backup tested and recovery time evidence.
- Cryptography policy and operational evidence.
- MFA coverage evidence.
- Vulnerability management evidence.

## Implementing standards

- **ISO 27001:2022** — broadest fit; substantial Article 21 coverage via Annex A.
- **ISO 27002:2022** — controls implementation guidance.
- **ISO 22301:2019** — business continuity (Article 21(c)).
- **IEC 62443** — industrial control systems.
- **BSI IT-Grundschutz** — DE specific path.
- **Sector-specific standards** — depending on entity.

## Bridge to ISO 27001 implementation

For an entity already certified to ISO 27001:

- Article 21(a)-(c), (e)-(j) measures largely covered.
- Article 21(d) supply chain security may need depth additions.
- Risk-management framing (Cl 6 + Annex A.5.7 threat intel) aligns.
- Documentation discipline aligns.
- ISO 27001 cert + targeted NIS2 extensions = defensible NIS2 compliance position.

## SRE and AI-agent fit notes

### Article 21(d) supply chain for AI work

Direct upstream suppliers for AI features:

- Foundation model providers (Anthropic, OpenAI, Google, etc.)
- Vector DB SaaS providers
- Agent framework SaaS / open-source providers
- Cloud infrastructure providers
- ICT service providers

Each requires supplier risk assessment, contractual security requirements, ongoing monitoring.

### Article 21(b) incident handling for AI incidents

Incident response procedures must cover AI-related incidents: prompt injection, model behavior change incidents, vendor-side outages affecting AI features, data leakage via AI outputs.

### Article 21(e) secure development for AI features

System prompt design, tool scope definition, evaluation harness construction, deployment review all fall within secure-development scope.

### Article 21(h) cryptography for AI data flows

Encryption in transit / at rest for prompts, retrieved context, outputs, audit logs.

### Article 21(j) MFA for AI service access

Authentication of access to model APIs, AI feature admin interfaces, audit log systems.

## Stefan-context implementation sketch

- For NIS2-scope clients: map ISO 27001 implementation work to Article 21 categories.
- For supply chain: document own cybersecurity posture for client supplier-management workflows.
- For incident response: pre-built workflow with 24h early-warning capability.

## See also

- [[NIS2 Cluster|cluster MOC]] · [[NIS2 Scope and Entities]] · [[NIS2 Incident Reporting]] · [[NIS2 vs ISO 27001]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.6 People Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
