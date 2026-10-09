title: GDPR Principles
summary: Article 5 of the GDPR establishes seven principles for personal data processing.
parent: gdpr
order: 100
labels: gdpr, regulation-concept
aliases: GDPR Principles | GDPR Article 5 | GDPR Seven Principles | GDPR Data Protection Principles
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/gdpr/GDPR Principles.md
reviewed: no
---
> Article 5 of the GDPR establishes seven principles for personal data processing. All processing must comply with all principles. Accountability principle (5(2)) places the burden of demonstrating compliance on the controller.

## The seven principles

### 1. Lawfulness, fairness, transparency (Article 5(1)(a))

Personal data shall be processed lawfully, fairly, and in a transparent manner in relation to the data subject.

- **Lawfulness**: processing must have a lawful basis (Article 6, plus Article 9 for special category data).
- **Fairness**: processing must be fair to data subjects — no deception, no detrimental processing without justification.
- **Transparency**: data subjects must be informed about processing per Articles 12-14.

Common failures:

- Processing without identifying lawful basis.
- Hidden processing (data sharing not disclosed).
- Opaque consent mechanisms.

### 2. Purpose limitation (Article 5(1)(b))

Personal data shall be collected for specified, explicit, legitimate purposes and not further processed in a manner incompatible with those purposes.

- Purpose must be specified at collection.
- Further processing for purposes compatible with original is allowed.
- Compatibility assessment factors in Article 6(4): link to original purpose, context, nature of data, consequences, safeguards.
- Public interest archiving, scientific/historical research, statistical purposes — special compatibility (Article 89).

Common failures:

- Collecting data for one purpose then using for unrelated purpose.
- Repurposing training data for new model versions without compatibility assessment.
- Customer data accessed by analytics or AI features without purpose alignment.

### 3. Data minimization (Article 5(1)(c))

Personal data shall be adequate, relevant, and limited to what is necessary in relation to the purposes for which they are processed.

- Collect only what is needed.
- Retain only as long as needed for the purpose (overlaps with storage limitation).
- Pseudonymize, anonymize, aggregate where the purpose allows.

Common failures:

- Collecting more fields than needed.
- Logging excessive personal data in audit logs.
- AI training data including more PII than the task requires.

### 4. Accuracy (Article 5(1)(d))

Personal data shall be accurate and, where necessary, kept up to date.

- Reasonable steps to ensure inaccurate data is erased or rectified without delay.
- Connects to right to rectification (Article 16).

Common failures:

- Stale customer records.
- AI models trained on outdated data producing wrong outputs about identifiable individuals.
- No mechanism for data subjects to correct errors.

### 5. Storage limitation (Article 5(1)(e))

Personal data shall be kept in a form which permits identification of data subjects for no longer than is necessary for the purposes.

- Retention schedules required.
- Longer retention permitted for archiving in public interest, scientific or historical research, statistical purposes (Article 89 safeguards).

Common failures:

- No retention schedule.
- Stale data accumulating in databases.
- Backup retention beyond justification.
- AI training data kept indefinitely after purpose served.

### 6. Integrity and confidentiality (Article 5(1)(f))

Personal data shall be processed in a manner that ensures appropriate security, including protection against unauthorized or unlawful processing and against accidental loss, destruction, or damage.

- Operationalized via Article 32 (security of processing).
- Bridges to information security management (ISO 27001 territory).
- Includes confidentiality, integrity, availability.

Common failures:

- Insufficient TOM (technical and organizational measures).
- Personal data breaches.
- Insufficient access controls.

### 7. Accountability (Article 5(2))

The controller shall be responsible for, and be able to demonstrate compliance with, the other principles.

- Burden of proof on controller.
- Documentation requirements throughout GDPR support accountability.
- Codes of conduct, certifications, DPIA records, processing records all serve accountability.

Common failures:

- No documentation of compliance work.
- Compliance claimed but not evidenced.
- Records of processing activities (Article 30) missing or incomplete.

## How the principles operate together

The principles are cumulative — all apply to all processing. Practical implications:

- Lawful basis (lawfulness) is necessary but not sufficient. Other principles must also be satisfied.
- Purpose limitation drives data minimization and storage limitation.
- Accuracy supports fairness (inaccurate processing is unfair).
- Security supports confidentiality and integrity, which feed back into lawfulness.
- Accountability requires demonstrating all the above.

## Connecting to other regulatory work

- **Lawfulness** — see [[GDPR Lawful Bases]].
- **Transparency** — see [[GDPR Data Subject Rights]] (Article 13-14 information).
- **Security** — overlaps with [[ISO 27001 Cluster|ISO 27001]] Annex A controls.
- **Accountability** — operationalized via records of processing, DPIAs, codes, certifications.

## Article 5 violations carry tier-2 fines

Article 83(5) — violations of basic principles (including Article 5) attract the higher penalty tier: up to €20M or 4% of global annual turnover (whichever higher). The principles are foundational; violations are taken seriously.

## SRE and AI-agent fit notes

### Lawfulness for AI processing

- Identify lawful basis for each AI feature processing personal data.
- Common choices: contract (for customer-facing features), legitimate interests (for security / fraud / analytics), consent (for marketing-style use), legal obligation (for compliance-driven processing).
- Special category data triggers Article 9 — explicit consent or specific exception required.

### Purpose limitation for AI

- AI training: training-data purpose must be clear, including whether training is part of the original purpose.
- AI inference: inference-time use must be within the purpose for which inference data was collected.
- Repurposing training data for new models requires compatibility assessment.

### Data minimization for AI

- Don't include personal data in prompts unnecessarily.
- Synthetic / anonymized data preferred where feasible.
- Filter PII from training data and RAG corpora where the task doesn't require it.

### Accuracy for AI

- AI outputs about identifiable individuals must support accuracy — there's no "AI exception" to GDPR accuracy.
- Hallucinations about real individuals can be inaccuracy violations.

### Storage limitation for AI

- Training data retention schedules.
- Model retention (do "deleted" data subjects' contributions persist in trained models? — open question, but increasingly relevant).
- Vendor-side retention (model providers retaining prompts and outputs).

### Integrity and confidentiality for AI

- Encryption in transit / at rest for personal data flowing through AI systems.
- Access controls on AI feature inputs and outputs.
- Vendor-side security (model providers' security posture).

### Accountability for AI

- Document the lawful basis decisions.
- Document the purpose specifications.
- Document the DPIA for AI features (typically required).
- Document the technical and organizational measures.

## Stefan-context implementation sketch

- Vault PII handling already follows minimization (whiteout-kb classification, no upload to public services).
- For AI work touching personal data:
  - Identify lawful basis per processing activity.
  - Document purpose narrowly.
  - Minimize PII in prompts / training data / RAG corpora.
  - Set retention schedules for personal data in AI infrastructure (logs, prompts, outputs).
  - Maintain accountability documentation.

## See also

- [[GDPR Cluster|cluster MOC]] · [[GDPR Lawful Bases]] · [[GDPR Data Subject Rights]] · [[GDPR Controller and Processor]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.34 Privacy and protection of PII)
