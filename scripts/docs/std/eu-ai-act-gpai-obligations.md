title: EU AI Act GPAI Obligations
summary: Cross-cutting obligations for general-purpose AI (GPAI) models under the EU AI Act.
parent: eu-ai-act
order: 100
labels: eu-ai-act, regulation-concept
aliases: EU AI Act GPAI Obligations | AI Act GPAI | GPAI Obligations | General Purpose AI Obligations
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/eu-ai-act/EU AI Act GPAI Obligations.md
reviewed: no
---
> Cross-cutting obligations for general-purpose AI (GPAI) models under the EU AI Act. Two tiers: baseline GPAI (Articles 53-54) and GPAI with systemic risk (Article 55). Applicable from 2 August 2025 for newly-released models; pre-existing models have until 2 August 2027.

## What is a GPAI model

Article 3(63) definition: an AI model trained with a large amount of data using self-supervision at scale, displaying significant generality and capable of competently performing a wide range of distinct tasks, regardless of how the model is placed on the market, and that can be integrated into a variety of downstream systems or applications.

In practice: large language models (GPT-4 family, Claude, Gemini, Llama, Mistral, Cohere Command), large multimodal models, foundation models generally.

Excluded: smaller, narrow-purpose models even if technically large; research models not placed on market.

## Provider vs deployer distinction for GPAI

- **GPAI provider** — entity that develops the GPAI model and places it on the market.
- **GPAI deployer** — uses the GPAI model in their own system or product.

GPAI obligations primarily fall on the provider. Deployers consuming GPAI through APIs have separate (typically lighter) obligations under use-case-specific provisions, but inherit responsibilities for their own downstream applications.

## Baseline GPAI obligations (Articles 53-54)

Applicable to all GPAI models meeting the Article 3(63) definition.

### Technical documentation (Article 53(1)(a))

Provider must draw up and keep up to date technical documentation:

- General description of the model (intended tasks, types of AI systems it can be integrated into, acceptable use policies, release date, distribution methods)
- Detailed description (architectural design, design choices including rationale, design specifications, model parameters and details, training process)
- Information for the training, testing, validation data
- Computational resources used for training
- Energy consumption of the model
- Information on input and output modalities and formats
- Limitations of the model
- Other relevant information per Annex XI

Documentation must be made available to AI Office and national authorities upon request.

### Information for downstream providers (Article 53(1)(b))

Provider must make available to downstream providers (entities integrating the GPAI into their systems) information enabling them to understand model capabilities and limitations and to comply with AI Act obligations:

- General description of the model
- Description of the elements of the model and process for development
- Acceptable use information
- Other relevant information per Annex XII

Documentation must be sufficient for downstream provider compliance work.

### Copyright compliance (Article 53(1)(c))

Provider must put in place a policy to comply with EU copyright law, particularly:

- Identify and comply with reservations of rights expressed pursuant to Article 4(3) of Directive 2019/790 (text and data mining opt-outs)
- Address legal questions about training data sourcing

### Training content summary (Article 53(1)(d))

Provider must draw up and publish a sufficiently detailed summary of content used for training, according to template provided by AI Office.

The template is one of the more controversial implementation items. AI Office published template guidance through 2024-2025.

### Exemption for free and open source GPAI

Article 53(2): obligations (a) and (b) do not apply to GPAI providers that release the model under a free and open source license that allows access, use, modification, and distribution — provided the model is not GPAI with systemic risk.

Obligations (c) and (d) still apply (copyright and training-content summary).

## GPAI with systemic risk obligations (Article 55)

Applicable to GPAI models classified as having systemic risk per Article 51.

### Classification as systemic risk

Two paths (Article 51):

- **Article 51(1)(a)**: model has high impact capabilities evaluated based on technical tools / methodologies including indicators and benchmarks. Operationalized via Article 51(2) presumption.
- **Article 51(1)(b)**: model is designated by Commission decision following Annex XIII criteria.

**Article 51(2) presumption**: model is presumed to have high impact capabilities when training compute exceeds 10^25 FLOP.

The 10^25 FLOP threshold is provisional; expected to be revised as compute scaling continues. Commission may adjust by delegated act.

### Notification (Article 52)

GPAI provider must notify Commission when its model meets (or is likely to meet) Article 51 criteria.

Notification within two weeks of meeting or being likely to meet.

Provider can present arguments against systemic-risk designation; Commission considers but final designation rests with Commission.

### Obligations for GPAI with systemic risk (Article 55(1))

In addition to baseline GPAI obligations:

- **Model evaluation including adversarial testing (Article 55(1)(a))**: state-of-the-art evaluation including documented adversarial testing aimed at identifying and mitigating systemic risks.
- **Risk assessment and mitigation at Union level (Article 55(1)(b))**: assess and mitigate systemic risks that may stem from development, market placement, use of the model.
- **Serious incident tracking and reporting (Article 55(1)(c))**: track, document, report serious incidents and possible corrective measures to AI Office and national authorities.
- **Cybersecurity protections (Article 55(1)(d))**: ensure adequate level of cybersecurity for the model and physical infrastructure.

Additional documentation requirements per Annex XII.

## Codes of Practice (Article 56)

Mechanism for GPAI providers to demonstrate compliance via voluntary Codes of Practice:

- AI Office facilitates development by GPAI providers, downstream providers, civil society, academia, other stakeholders.
- Codes describe how providers will meet Article 53 / 55 obligations.
- Compliance with adherence to a Code provides demonstrable evidence of compliance with the relevant articles.

The **GPAI Code of Practice** developed through 2024-2025 stakeholder process. Published mid-2025 (final version after multiple drafts). Major GPAI providers signed; signing helps demonstrate compliance.

## Obligations on downstream providers consuming GPAI

Downstream providers using GPAI in their own AI systems have obligations under the use-case-specific provisions (not the GPAI articles directly). If their system is high-risk, they comply with Articles 8-21 etc. with the support of the GPAI provider's downstream-provider documentation.

The GPAI provider is responsible for GPAI model obligations; the downstream provider is responsible for the AI system obligations of the system they place on market.

Information flow from GPAI provider to downstream provider (Article 53(1)(b)) is the bridge.

## Open-source GPAI considerations

Article 53(2) exemption for free and open-source GPAI (when not systemic-risk):

- Open-source models exempt from technical documentation (Article 53(1)(a)) and information-for-downstream (Article 53(1)(b)).
- Still subject to copyright (Article 53(1)(c)) and training-content summary (Article 53(1)(d)).
- Systemic-risk open-source GPAI is subject to all obligations.

This was contested through drafting; final text reflects compromise. Practical impact: Llama, Mistral open-weight models, others released under open licenses face lighter baseline obligations (but Llama 3.1 405B has been considered for systemic-risk classification given its capabilities).

## SRE and AI-agent fit notes

### Implications for orgs consuming GPAI

Most orgs are GPAI deployers (consuming Anthropic / OpenAI / Google / etc. models through APIs), not GPAI providers. Implications:

- GPAI provider compliance posture is a vendor due-diligence axis.
- Provider's downstream-provider documentation enables your AI Act compliance for downstream system.
- Track provider Code of Practice signature status.
- Provider systemic-risk classification matters: systemic-risk models may have different commercial terms, capabilities, restrictions.

### Implications for orgs developing GPAI

For orgs training and releasing their own GPAI:

- Substantial compliance work. Baseline obligations are non-trivial.
- Systemic-risk path requires substantial additional infrastructure (evaluation, adversarial testing, serious incident reporting, cybersecurity).
- Cost-benefit analysis often pushes toward consuming hosted GPAI rather than self-development for non-AI-product organizations.
- Open-source path provides exemption from some baseline obligations but not from systemic-risk obligations if applicable.

### Vendor due diligence checklist for GPAI providers

- Article 53 compliance documentation available?
- Training-content summary published?
- Copyright compliance policy documented?
- GPAI Code of Practice signed?
- Article 55 systemic-risk classification (if applicable)?
- Serious incident reporting commitment?
- Cybersecurity posture documentation?

## Stefan-context implementation sketch

- Stefan's work mostly involves consuming hosted GPAI (Anthropic Claude primarily). Stefan is a deployer, not a provider.
- Vendor due diligence: track Anthropic's GPAI compliance posture, Code of Practice signature status, systemic-risk classification.
- For client engagements involving GPAI consumption: document the upstream GPAI provider's compliance evidence in supplier-management records.
- For agent systems built on GPAI: deployer obligations from the AI Act flow through; classification analysis per the broader system, not just the GPAI model.

## See also

- [[EU AI Act Cluster|cluster MOC]] · [[EU AI Act Risk Tiers]] · [[EU AI Act Timeline]] · [[EU AI Act High-Risk Obligations]] · [[EU AI Act Governance]]
- [[ISO 42001 Annex A Controls]] (A.10 third-party relationships overlap)
