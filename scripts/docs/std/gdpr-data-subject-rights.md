title: GDPR Data Subject Rights
summary: Articles 12-23 of the GDPR establish rights of data subjects.
parent: gdpr
order: 100
labels: gdpr, regulation-concept
aliases: GDPR Data Subject Rights | GDPR Rights | GDPR Articles 12-23 | DSR | GDPR Right to Erasure | GDPR Right of Access
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/gdpr/GDPR Data Subject Rights.md
reviewed: no
---
> Articles 12-23 of the GDPR establish rights of data subjects. Controllers must facilitate exercise of rights, respond within one month (extendable to three for complex cases), and not charge fees except in limited circumstances. Rights operationalize the dignity-based framing of GDPR's data protection.

## Procedural framework (Article 12)

Controllers must:

- Take appropriate measures to provide information in concise, transparent, intelligible, easily accessible form.
- Use clear and plain language (especially for children).
- Provide information in writing or by electronic means as appropriate.
- Facilitate exercise of rights (Articles 15-22).
- Respond within one month of receipt of request (extendable by two further months for complex cases, with notification).
- Reply free of charge unless requests are manifestly unfounded or excessive (in which case reasonable fee or refusal possible).
- Verify identity of data subject before responding (proportionate to request).

## Information rights (Articles 13-14)

When data is collected from the data subject (Article 13) or from elsewhere (Article 14), the controller must provide:

- Identity and contact details of controller (and DPO if applicable)
- Purposes of processing and lawful basis
- Legitimate interests pursued (if Article 6(1)(f))
- Recipients or categories of recipients
- Cross-border transfer information (countries, safeguards)
- Retention period
- Rights of the data subject (access, rectification, erasure, restriction, portability, object)
- Right to withdraw consent (if consent-based)
- Right to lodge complaint with supervisory authority
- Source of data (Article 14 only — when not from data subject)
- Existence of automated decision-making including profiling (Article 22) — and meaningful information about logic, significance, consequences

Timing:

- Article 13 (direct collection): at time of collection.
- Article 14 (indirect collection): reasonable period (max one month) after obtaining; at time of first communication if for communication; at time of disclosure if to be disclosed.

## Right of access (Article 15)

Data subject has right to obtain from the controller:

- Confirmation of whether personal data are being processed.
- Access to the personal data.
- Specific information: purposes, categories of data, recipients, retention period, rights, source, automated decision-making information.
- A copy of the personal data undergoing processing.

The right of access is foundational — many data subjects exercise this first; other rights cascade.

Implementation considerations:

- Identity verification.
- Personal data extraction across systems.
- Special category data handling (require additional verification).
- Format — typically electronic if requested electronically.
- Third-party data — copy provided to data subject must not adversely affect rights of others.

## Right to rectification (Article 16)

Data subject has right to obtain rectification of inaccurate personal data without undue delay. Also right to have incomplete personal data completed.

Implementation considerations:

- Notification to recipients (Article 19) if data has been disclosed.
- Update propagation across systems.

## Right to erasure / "right to be forgotten" (Article 17)

Data subject has right to obtain erasure of personal data without undue delay where:

- Data no longer necessary for the purposes for which collected/processed.
- Data subject withdraws consent (where consent was the basis) and no other legal ground.
- Data subject objects (Article 21) and no overriding legitimate grounds.
- Data have been unlawfully processed.
- Erasure required for compliance with legal obligation.
- Data collected in relation to information society services offered to a child.

Exceptions to erasure (Article 17(3)):

- Exercising right of freedom of expression and information.
- Compliance with legal obligation requiring processing.
- Public interest in public health.
- Archiving / research / statistics with Article 89 safeguards.
- Establishment / exercise / defence of legal claims.

The Google Spain (2014) decision established right to be forgotten foundationally pre-GDPR.

Implementation considerations:

- Erasure across systems including backups.
- Notification to recipients (Article 19).
- Search-engine de-indexing where applicable.
- AI training data — emerging question on whether trained models "remember" deleted data and what erasure obligation implies.

## Right to restriction (Article 18)

Data subject has right to obtain restriction of processing where:

- Accuracy contested (during verification).
- Processing unlawful but data subject opposes erasure (e.g., evidence preservation).
- Controller no longer needs data but data subject needs for legal claims.
- Data subject has objected pending verification of overriding legitimate grounds.

Restricted data may only be processed with consent, for legal claims, for protection of rights, for public interest reasons.

Implementation considerations:

- Restriction markers in data stores.
- Notification before lifting restriction.
- Notification to recipients (Article 19).

## Notification obligation (Article 19)

Controller must communicate any rectification, erasure, or restriction to each recipient to whom the data have been disclosed, unless this proves impossible or involves disproportionate effort. Controller informs the data subject about those recipients if data subject requests.

## Right to portability (Article 20)

Where processing is based on consent (6(1)(a) or 9(2)(a)) or contract (6(1)(b)), AND processing is carried out by automated means, data subject has right to:

- Receive personal data concerning them in structured, commonly used, machine-readable format.
- Transmit those data to another controller.
- Where technically feasible, direct transmission from one controller to another.

Not applicable to processing necessary for public interest task or official authority.

Implementation considerations:

- Format choice (JSON, CSV, etc.).
- Identity verification.
- Scope: data "provided by" the data subject — interpretation varies.

## Right to object (Article 21)

Data subject has right to object to processing based on:

- (1) Legitimate interests (Article 6(1)(f)) or public interest (Article 6(1)(e)): processing must stop unless controller demonstrates compelling legitimate grounds overriding interests, rights, freedoms, or for legal claims.
- (2) Direct marketing: absolute right to object; processing for direct marketing must stop immediately. Includes profiling related to direct marketing.
- (6) Scientific/historical research or statistics processing for public interest: right to object on grounds relating to particular situation, unless processing necessary for public interest task.

The Article 21(2) absolute right to object to direct marketing is one of the more practically consequential rights — opt-out must be honored.

## Automated individual decision-making rights (Article 22)

Data subject has right not to be subject to a decision based solely on automated processing (including profiling) which:

- Produces legal effects concerning him or her, or
- Similarly significantly affects him or her.

Exceptions (Article 22(2)):

- (a) Necessary for entering into / performing a contract.
- (b) Authorized by Union or member state law with safeguards.
- (c) Based on explicit consent.

Even when exception applies, controller must implement suitable measures including:

- Right to obtain human intervention.
- Right to express point of view.
- Right to contest the decision.

For special category data, additional restrictions (Article 22(4)).

The "solely automated" and "similarly significant effects" criteria are the operational fulcrum:

- AI-assisted decisions with human review typically fall outside the strict scope.
- "Significant" — credit decisions, employment decisions, automated denials of service typically qualify; recommendations and rankings often debated.

Recent CJEU jurisprudence (SCHUFA Holding C-634/21, 2023) has tightened application — broad reading of "solely" in some contexts.

## Right to lodge complaint (Article 77)

Every data subject has right to lodge complaint with supervisory authority. Member state DPA must investigate complaints, inform complainant of progress and outcome.

## Right to judicial remedy (Articles 78-79)

Data subjects can pursue judicial remedy against supervisory authority decisions and against controllers/processors directly.

## Compensation rights (Article 82)

Data subjects have right to compensation for material or non-material damage from infringement.

## Restrictions (Article 23)

Member state law can restrict rights/obligations where necessary and proportionate to safeguard:

- National security, defence, public security.
- Crime prevention/investigation.
- Other important EU or member state public interests.
- Judicial independence.
- Breaches of professional ethics.
- Monitoring/inspection/regulatory functions.
- Protection of data subject or rights of others.
- Enforcement of civil claims.

Restrictions must respect essence of fundamental rights and be necessary and proportionate.

## SRE and AI-agent fit notes

### Right of access for AI features

- Personal data in prompts, retrieved context, agent outputs, audit logs all in scope of access requests.
- Implement extraction across the AI feature data flow.
- Consider including AI-system-generated inferences about the data subject (e.g., classifications, risk scores) as personal data subject to access.

### Right to erasure for AI

- Deletion across systems including AI infrastructure.
- Open question on model-encoded data — current practice does not require model retraining for individual data subject requests, but the position may evolve.
- RAG corpora must support erasure.

### Right to rectification for AI

- AI-generated inferences about real individuals subject to rectification if inaccurate.
- Hallucinations about real individuals — emerging case law on whether these are GDPR violations and what the rectification path looks like.

### Article 22 for AI

- Most AI-assisted human decisions fall outside strict Article 22 scope.
- Fully automated significant decisions (credit, hiring, denial of service) trigger Article 22 obligations.
- Provide human intervention path, explanation, contestability.

### Right to portability for AI training

- Data provided by data subject is portable.
- AI-inferred data about the data subject — debated; trending toward including in portability scope.

## Stefan-context implementation sketch

- For client engagements: build data subject rights response capability before requests arrive.
- For AI features touching personal data: implement extraction across the data flow; document the AI-system-generated inferences as personal data; provide human-intervention paths for Article 22-relevant decisions.
- For vault personal data (whiteout-kb): own data; rights theoretical but apply.

## See also

- [[GDPR Cluster|cluster MOC]] · [[GDPR Principles]] · [[GDPR Lawful Bases]] · [[GDPR Controller and Processor]]
- [[EU AI Act Cluster]] (Article 22 overlap with AI Act Article 86 right to explanation)
