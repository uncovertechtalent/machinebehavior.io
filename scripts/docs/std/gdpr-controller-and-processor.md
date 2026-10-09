title: GDPR Controller and Processor
summary: Articles 24-39 establish controller and processor obligations.
parent: gdpr
order: 100
labels: gdpr, regulation-concept
aliases: GDPR Controller and Processor | GDPR Article 28 | GDPR DPA | GDPR Article 32 | GDPR Breach Notification | GDPR DPIA | GDPR DPO
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/gdpr/GDPR Controller and Processor.md
reviewed: no
---
> Articles 24-39 establish controller and processor obligations. Controller determines purposes and means; processor processes on controller's behalf. Joint controllers share responsibility. Both have distinct GDPR obligations: technical and organizational measures, processing records, breach notification, DPIA, DPO. The processor agreement (Article 28 DPA) is the contractual instrument binding the two.

## Controller obligations (Article 24)

The controller shall implement appropriate technical and organizational measures (TOM) to ensure and demonstrate compliance, taking into account:

- Nature, scope, context, purposes of processing.
- Risks of varying likelihood and severity for rights and freedoms.

TOM include:

- Implementation of data protection policies.
- Adherence to approved codes of conduct (Article 40) or certification (Article 42).
- Data protection by design and by default (Article 25).

Controller can demonstrate compliance through documentation, codes, certifications.

## Data protection by design and by default (Article 25)

Controller must implement appropriate TOM at the time of determination of means of processing and at time of processing itself, to:

- Implement data protection principles effectively.
- Integrate necessary safeguards into the processing.
- Ensure that by default, only personal data necessary for each specific purpose are processed (data minimization by default).
- Apply to amount of data, extent of processing, period of storage, accessibility.

Privacy by design is a discipline: bake protections into the system, don't add them after the fact.

## Joint controllers (Article 26)

Two or more controllers jointly determining purposes and means of processing are joint controllers.

Joint controllers must:

- Determine respective responsibilities by transparent arrangement.
- Make essence of arrangement available to data subjects.
- Data subjects can exercise rights against either controller.

Common joint controller scenarios:

- Co-branded services.
- Platforms with shared data flows (case law: Fashion ID, Wirtschaftsakademie Schleswig-Holstein).
- Some advertising/marketing arrangements.

## Representatives of non-EU controllers/processors (Article 27)

Non-EU controllers/processors offering goods/services to EU data subjects or monitoring their behavior must designate an EU-established representative. Exceptions: occasional processing, low-risk processing, public authorities.

Representative acts as point of contact for data subjects and DPAs.

## Processor obligations (Article 28)

Processor processes personal data on behalf of controller. Processor obligations include:

- Process only on documented instructions from controller.
- Implement security measures (Article 32).
- Engage sub-processors only with prior controller authorization.
- Assist controller with data subject rights (Articles 12-22).
- Assist controller with Article 32-36 obligations.
- Delete or return personal data at end of services.
- Make available information necessary to demonstrate compliance.

### The Article 28 DPA (Data Processing Agreement)

Article 28(3) requires a contract (or other legal act) between controller and processor with specific contents:

- Subject matter, duration, nature, purpose of processing.
- Type of personal data, categories of data subjects.
- Obligations and rights of the controller.
- Specific processor obligations including:
  - Process only on documented controller instructions
  - Ensure confidentiality of processing staff
  - Take Article 32 security measures
  - Conditions for sub-processor engagement
  - Assist controller in responding to data subject requests
  - Assist controller with Articles 32-36 obligations
  - At controller's choice: delete or return data at end of services
  - Make available information to demonstrate compliance, allow audits

DPAs are the most common bilateral GDPR document. SCC-compliant DPA templates are widely available.

### Sub-processors

Processors engaging sub-processors require:

- Prior written controller authorization (specific or general).
- Flow-down obligations equivalent to those between controller and processor.
- Processor remains liable to controller for sub-processor compliance.

Model providers (Anthropic, OpenAI, Google) acting as processors typically have sub-processors (cloud infrastructure, evaluation contractors); their DPAs disclose and provide change-notification procedures.

## Records of processing activities (Article 30)

Both controllers and processors maintain records of processing activities.

Controller records (Article 30(1)) include:

- Name, contact of controller (and DPO).
- Purposes of processing.
- Description of categories of data subjects and personal data.
- Categories of recipients (including third countries).
- Cross-border transfers, including safeguards.
- Retention periods (envisaged where possible).
- General description of security measures.

Processor records (Article 30(2)) include:

- Name, contact of processor and each controller for which acting.
- Categories of processing carried out on behalf of each controller.
- Cross-border transfers.
- General description of security measures.

Exception: organizations with fewer than 250 employees exempted unless processing is likely to result in risk to rights/freedoms, processing not occasional, or includes special category / criminal data. Most organizations qualify in practice.

## Cooperation with supervisory authority (Article 31)

Controllers and processors shall cooperate with supervisory authority on request.

## Security of processing (Article 32)

Controller and processor shall implement appropriate TOM to ensure security appropriate to the risk, including (where appropriate):

- (a) Pseudonymization and encryption.
- (b) Confidentiality, integrity, availability, resilience of systems and services.
- (c) Ability to restore availability and access in event of incident.
- (d) Process for regularly testing, assessing, evaluating effectiveness of measures.

Risk assessment factors: accidental or unlawful destruction, loss, alteration, unauthorized disclosure or access.

Article 32 is the GDPR security pillar — overlaps heavily with ISO 27001 Annex A controls. ISO 27001 certification provides evidence of Article 32 compliance.

## Personal data breach notification (Articles 33-34)

### Notification to supervisory authority (Article 33)

In case of personal data breach, controller shall:

- Notify supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware.
- If notification later than 72 hours, give reasons for delay.
- Include in notification: nature of breach, categories and approximate numbers of data subjects, categories and approximate numbers of records, contact details for DPO, likely consequences, measures taken or proposed.

Exception: notification not required if breach unlikely to result in risk to rights/freedoms.

Processor must notify controller without undue delay after becoming aware.

### Notification to data subjects (Article 34)

When breach likely to result in high risk to rights/freedoms, controller communicates breach to data subjects without undue delay.

Communication includes: nature, contact details, likely consequences, measures taken.

Exception: not required if measures applied render data unintelligible (e.g., strong encryption), subsequent measures applied that ensure high risk no longer materializing, or disproportionate effort (in which case public communication or similar).

The 72-hour clock starts at controller awareness. Operationally tight; pre-built notification workflow essential.

## Data Protection Impact Assessment (Article 35)

DPIA required where processing likely to result in high risk to rights and freedoms, in particular:

- Systematic and extensive automated evaluation (including profiling) producing legal/similarly significant effects.
- Large-scale processing of special category or criminal conviction data.
- Systematic monitoring of publicly accessible area on large scale.

DPIA contents:

- Systematic description of processing operations and purposes.
- Assessment of necessity and proportionality.
- Assessment of risks to rights and freedoms.
- Measures envisaged to address risks.

DPAs publish lists of operations requiring DPIA (Article 35(4)) and operations not requiring (Article 35(5)).

## Prior consultation (Article 36)

Where DPIA indicates high residual risk in absence of measures, controller shall consult supervisory authority prior to processing.

## Data Protection Officer (Articles 37-39)

### Appointment criteria (Article 37)

DPO mandatory where:

- (a) Processing carried out by public authority/body (except courts in judicial capacity).
- (b) Core activities consist of regular and systematic monitoring of data subjects on large scale.
- (c) Core activities consist of large-scale processing of special category or criminal data.

Voluntary appointment for other controllers/processors.

### Position (Article 38)

DPO:

- Properly and timely involved in all data protection issues.
- Provided with necessary resources.
- Cannot be dismissed/penalized for performing tasks.
- Reports to highest management level.
- Can be employee or external on service contract.
- Contact published and communicated to DPA.

### Tasks (Article 39)

DPO tasks include:

- Inform and advise controller, processor, employees on GDPR obligations.
- Monitor compliance.
- Provide advice regarding DPIA.
- Cooperate with supervisory authority.
- Act as contact point for supervisory authority.

DPO has high independence requirements; cannot be given conflicting tasks.

## Codes of conduct and certification (Articles 40-43)

Mechanisms for demonstrating compliance:

- **Codes of conduct** drawn up by representative associations, approved by DPAs (national codes) or EDPB (cross-border).
- **Certification** issued by accredited certification bodies. Mechanism for demonstrating compliance with specific aspects (e.g., transfer safeguards, security).

Adherence to approved codes / certifications provides evidence of compliance. Doesn't substitute for accountability obligation but provides defensible position.

## SRE and AI-agent fit notes

### Controller vs processor for AI work

- **Org as controller, model provider as processor**: typical for API consumption. Org determines purposes; model provider processes on instructions.
- **Org as controller, fine-tuning provider as processor**: similar.
- **Org as joint controller with provider**: rare but possible for deeply-integrated arrangements where both determine purposes.
- **Org as processor**: when org provides AI features to other organizations as customers, org is processor to those customers as controllers.

### DPA for model providers

Standard model provider DPAs (Anthropic, OpenAI, Google, others) cover:

- Processing only on customer instructions (system prompt + API calls).
- No training on customer data (in enterprise tiers).
- Retention windows (zero-retention available in some enterprise tiers).
- Sub-processor lists (cloud infrastructure typically).
- Security measures (ISO 27001 + ISO 27017 + SOC 2 usually cited).
- Audit rights (typically via providing audit reports).
- Cross-border transfer mechanisms (typically EU-US Data Privacy Framework + SCCs as backup).

### TOM for AI processing

- Article 32 security measures apply to AI feature data flows.
- Encryption in transit / at rest.
- Access controls on prompts, retrieved context, outputs.
- Audit logging.
- Backup and restore.
- Vendor-side security posture.

### DPIA for AI features

- Often required given high-risk processing patterns.
- Build DPIA into the AI feature development lifecycle (parallels ISO 42001 impact assessment).
- AI-specific risk categories (prompt injection, hallucination about real individuals, automated decision-making) included in DPIA.

### Breach notification for AI

- Breach categories include unauthorized access to prompts, outputs, training data.
- Model-vendor breaches notified to org (as controller); org notifies DPA and data subjects per Articles 33-34.
- Cross-vendor incident coordination essential — incident at model provider, vector DB provider, cloud provider all flow.

## Stefan-context implementation sketch

- For client engagements: clarify controller/processor roles per processing activity.
- DPAs in place with model providers (Anthropic enterprise tier covers most of this).
- Records of processing for client-related processing (lightweight; aligned with Article 30 requirements).
- DPIA performed and documented for AI features in client deployments where high-risk processing.
- Breach notification workflow documented (channels to client, channels from model providers).

## See also

- [[GDPR Cluster|cluster MOC]] · [[GDPR Principles]] · [[GDPR Lawful Bases]] · [[GDPR Data Subject Rights]] · [[GDPR Cross-Border Transfers]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.19-A.5.23 supplier relationships, A.5.34 PII)
- [[ISO 27001 Annex A.8 Technological Controls]] (A.8.24 cryptography, A.8.10 deletion, A.8.11 masking, A.8.12 DLP)
