title: EU AI Act High-Risk Obligations
summary: Obligations applying to high-risk AI systems under the EU AI Act.
parent: eu-ai-act
order: 100
labels: eu-ai-act, regulation-concept
aliases: EU AI Act High-Risk Obligations | AI Act High-Risk | AI Act Annex III | High-Risk AI Compliance
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/eu-ai-act/EU AI Act High-Risk Obligations.md
reviewed: no
---
> Obligations applying to high-risk AI systems under the EU AI Act. High-risk classification triggers extensive compliance work: risk management, data governance, technical documentation, record-keeping, transparency, human oversight, accuracy/robustness/cybersecurity, conformity assessment, CE marking, post-market monitoring, serious incident reporting. Applicable from 2 August 2026 (Annex III) and 2 August 2027 (Annex I products).

## Who must comply

Three primary roles:

- **Provider** — natural or legal person developing or having developed an AI system, placing it on the market or putting it into service under own name or trademark.
- **Deployer** — natural or legal person using an AI system under its authority (other than personal non-professional activity). Was called "user" in earlier drafts.
- **Importer / Distributor** — for AI systems imported into or distributed within the EU.

Additional roles: **Authorized representative** (for non-EU providers), **Product manufacturer** (for Annex I product cases).

Each role has distinct obligations; provider obligations are the heaviest.

## Provider obligations (Articles 16, 8-21)

### Risk management system (Article 9)

Establish and maintain a risk management system throughout the AI system lifecycle. Iterative process including:

- Identification and analysis of risks the system may pose to health, safety, fundamental rights
- Estimation and evaluation of risks that may emerge when used as intended
- Evaluation of risks based on post-market monitoring data
- Adoption of risk management measures

### Data and data governance (Article 10)

For high-risk systems using training/validation/testing data:

- Data must be subject to appropriate data governance and management practices
- Data sets must be relevant, sufficiently representative, free of errors (to extent feasible), complete in view of intended purpose
- Special attention to bias in training data
- Special-category personal data processed only when strictly necessary for bias monitoring/correction, with appropriate safeguards

### Technical documentation (Article 11, Annex IV)

Comprehensive technical documentation including:

- General description of the system, intended purpose, lifecycle
- Detailed system description (elements, processes, computational logic, optimization)
- Detailed monitoring, functioning, control description
- Risk management system
- Changes through lifecycle
- Lists of harmonized standards applied or solutions adopted to meet requirements
- EU declaration of conformity
- Description of system in use

Annex IV provides the documentation template (extensive).

### Record-keeping (Article 12)

High-risk AI systems must enable automatic logging during operation. Logging:

- Must be appropriate to intended purpose
- Must support functioning monitoring
- Must support post-market monitoring

Logs must be kept by the provider when provider deploys the system, or by the deployer.

### Transparency and information for users (Article 13)

Systems designed and developed so deployers can:

- Understand and use the system appropriately
- Receive concise / complete / correct / clear information

Instructions for use must include: identity and contact of provider, characteristics, capabilities, limitations, intended purpose, accuracy / robustness / cybersecurity level, foreseeable circumstances of malfunction, expected useful life and maintenance.

### Human oversight (Article 14)

Systems designed and developed so they can be effectively overseen by natural persons. Human oversight measures include:

- Ability to fully understand the capacities and limitations
- Awareness of automation bias risks
- Ability to correctly interpret outputs
- Ability to disregard, override, or reverse outputs
- Ability to intervene or stop the system

Specific Article 14(5) provisions for certain biometric-identification high-risk systems requiring "two-eye" verification.

### Accuracy, robustness, cybersecurity (Article 15)

System must be designed and developed to achieve:

- Appropriate level of accuracy
- Robustness against errors, faults, inconsistencies
- Resilience against unauthorized third parties (cybersecurity)
- Mitigation against attacks attempting to manipulate training data or alter model behavior

Accuracy levels and metrics declared in instructions for use.

### Quality management system (Article 17)

Provider shall put in place a quality management system to ensure compliance. Documented in policies, procedures, instructions. Includes:

- Strategy for regulatory compliance
- Techniques for design / quality control / verification
- Procedures for conducting tests
- Procedures for post-market monitoring
- Procedures for serious incident reporting
- Procedures for cooperation with authorities

### Conformity assessment (Articles 19, 43)

Before placing on market or putting into service:

- **Internal control conformity assessment** for most Annex III high-risk systems (provider self-assesses).
- **Notified Body assessment** for some categories (notably biometric remote identification subject to specific procedures, and Annex I product cases following the underlying product regulation's conformity assessment).

Conformity assessment results in EU declaration of conformity (Annex V) and CE marking.

### Registration in EU database (Article 49)

High-risk AI systems must be registered in an EU database before being placed on market or put into service.

### Post-market monitoring (Article 72)

Provider must establish and document post-market monitoring system to actively collect, document, analyze data on performance throughout the lifetime. Outputs feed back into risk management.

### Reporting of serious incidents (Article 73)

Providers must report serious incidents to market surveillance authority. Timelines:

- Within 15 days of becoming aware of serious incident or malfunction
- Shorter timeline (immediately, no later than 2 days) for incidents involving breach of fundamental rights obligations
- Even shorter (immediately, no later than 10 days) for incidents involving widespread infringement / serious malfunction

### CE marking (Article 48)

CE marking affixed to the high-risk AI system (or accompanying documentation where physical attachment not feasible).

### Cooperation with authorities (Article 21)

Providers cooperate with national competent authorities and market surveillance authorities.

## Deployer obligations (Article 26)

For deployers of high-risk AI systems:

- Use system according to instructions for use
- Assign human oversight to natural persons with necessary competence
- Monitor operation per instructions
- Suspend use if reasonable grounds to consider use makes the system present risk
- Inform provider, distributor, market surveillance authority of risks identified
- Keep logs automatically generated by the system (for at least 6 months unless other rules apply)
- For workplace deployment: inform affected workers and their representatives prior to use
- Conduct fundamental rights impact assessment in certain cases (Article 27, deployer use of high-risk by public authorities and private entities providing public services)

## Specific deployer obligations: Fundamental rights impact assessment (Article 27)

For deployers of high-risk Annex III systems (some public/quasi-public uses), additional obligation: conduct FRIA before deploying:

- Process description
- Period of use
- Categories of natural persons / groups likely affected
- Specific risks of harm
- Implementation of human oversight measures
- Measures if risks materialize, including governance / complaint mechanisms

Result registered with market surveillance authority in some cases.

## Importer / distributor obligations (Articles 23-25)

- **Importer (Article 23)**: verify provider compliance, ensure documentation accompanies the system, indicate own contact information, monitor for compliance signals, cooperate with authorities.
- **Distributor (Article 24)**: verify CE marking and required documentation, ensure storage / transport conditions don't compromise compliance, cooperate with authorities.

## Authorized representative (Article 22)

Non-EU providers must designate an EU-established authorized representative who:

- Verifies that conformity assessment and technical documentation are completed
- Keeps documentation available for authorities
- Cooperates with authorities
- Acts as point of contact

## Notified Body involvement

For high-risk AI systems requiring third-party conformity assessment:

- Notified Body designated by Member State for the specific category
- Performs conformity assessment per Annex VI or Annex VII procedure
- Issues conformity certificate
- Subsequent surveillance during validity

Notified Body capacity is a current bottleneck (as of 2026); designations are ongoing through 2025-2027.

## Compliance evidence per obligation

| Obligation | Evidence artefact |
|---|---|
| Risk management | Risk management documentation, iterative review records |
| Data governance | Data governance procedures, data set documentation, bias assessment records |
| Technical documentation | Annex IV documentation set |
| Record-keeping | Logging system in operation, retention records |
| Transparency | Instructions for use document |
| Human oversight | Oversight design documentation, training records for human overseers |
| Accuracy / robustness / cybersecurity | Performance metrics, robustness test results, cybersecurity assessment |
| Quality management | QMS documentation, internal audit records |
| Conformity assessment | Conformity assessment records, declaration of conformity |
| Registration | EU database entry |
| Post-market monitoring | PMM system documentation, data analysis records |
| Serious incident reporting | Reporting procedure, reports filed (with timestamps) |

## SRE and AI-agent fit notes

### Agent systems and high-risk classification

Most agent systems built on model APIs are not in Annex III by default. Use case matters:

- Agent helping HR with hiring → Area 4 (Employment) → likely high-risk
- Agent making credit decisions → Area 5 (Essential services) → likely high-risk
- Agent moderating content for major platforms → potentially Area 8 edge
- Internal-productivity agent without consequential decisions → likely not high-risk

Article 6(3) exemption applies if the system performs narrow procedural tasks or doesn't pose significant risk. Document the assessment.

### Mapping high-risk obligations to existing implementation work

For systems crossing into high-risk territory, obligations map heavily to existing AI governance work:

| AI Act obligation | Existing work it draws on |
|---|---|
| Risk management (Art 9) | ISO 42001 Cl 6.1.2 / 8.2 risk processes; NIST AI RMF MAP / MEASURE / MANAGE |
| Data governance (Art 10) | ISO 42001 Annex A.7; NIST AI RMF GenAI Profile Category 4 |
| Technical documentation (Art 11) | ISO 42001 Cl 7.5 documented information |
| Record-keeping / logging (Art 12) | ISO 27001 A.8.15; ISO 42001 A.6.2.8 |
| Transparency (Art 13) | ISO 42001 A.8 information for interested parties |
| Human oversight (Art 14) | NIST AI RMF GenAI Profile Category 7 |
| Accuracy / robustness / cybersecurity (Art 15) | OWASP LLM Top 10 (security); ISO 42001 Annex A.6.2.4 V&V |
| Quality management (Art 17) | ISO 9001 + ISO 42001 management system |
| Conformity assessment (Art 19, 43) | Audit infrastructure; ISO 42001 cert-adjacent |
| Post-market monitoring (Art 72) | ISO 42001 A.6.2.6; NIST AI RMF MANAGE |
| Serious incident reporting (Art 73) | ISO 42001 A.8.4; ISO 27001 incident management |

ISO 42001 harmonization (when complete) will provide presumption of conformity for many of these obligations.

## Stefan-context implementation sketch

For solo / small-team agent system work potentially touching high-risk categories:

- Run classification analysis per significant agent.
- Most likely outcome: limited-risk or minimal-risk; document the Article 6(3) exemption rationale where applicable.
- For systems crossing into high-risk: coordinate with client; substantial implementation work; consider ISO 42001 alignment path.
- Document classification assessments in vault as evidence artefacts.

## See also

- [[EU AI Act Cluster|cluster MOC]] · [[EU AI Act Risk Tiers]] · [[EU AI Act Timeline]] · [[EU AI Act GPAI Obligations]] · [[EU AI Act Governance]]
- [[ISO 42001 Clause Structure]] · [[ISO 42001 Annex A Controls]] · [[NIST AI RMF Core Functions]] · [[OWASP LLM Top 10 2025]]
