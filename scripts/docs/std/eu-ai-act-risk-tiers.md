title: EU AI Act Risk Tiers
summary: The EU AI Act categorizes AI systems by risk level.
parent: eu-ai-act
order: 100
labels: eu-ai-act, regulation-concept
aliases: EU AI Act Risk Tiers | AI Act Risk Tiers | AI Act Categories | EU AI Act Unacceptable High Limited Minimal
type: regulation-concept
created: 2026-05-12
updated: 2026-10-09
origin: pillars/eu-ai-act/EU AI Act Risk Tiers.md
reviewed: no
---
> The EU AI Act categorizes AI systems by risk level. Unacceptable risk = prohibited. High risk = extensive obligations. Limited risk = transparency obligations. Minimal/no risk = voluntary. GPAI sits cross-cutting with its own tier (baseline + systemic risk subtier).

## Tier 1: Unacceptable risk (prohibited) — Article 5

Article 5 lists AI practices that are prohibited because they conflict with EU values and fundamental rights. Applicable since 2 February 2025.

### Prohibited practices

- **Subliminal techniques** beyond a person's consciousness, or manipulative / deceptive techniques causing or likely causing significant harm.
- **Exploitation of vulnerabilities** (age, disability, social/economic situation) causing or likely causing significant harm.
- **Social scoring** by public authorities or on their behalf evaluating natural persons based on social behavior or personality, leading to detrimental or unfavorable treatment in unrelated contexts or unjustified treatment.
- **Predictive policing based solely on profiling** of natural persons or assessing personality traits. Note: predictive policing based on objective and verifiable facts directly linked to criminal activity remains permissible.
- **Untargeted scraping of facial images** from the internet or CCTV to create or expand facial recognition databases.
- **Emotion recognition** in workplaces and educational institutions (with exceptions for medical or safety reasons).
- **Biometric categorization** of natural persons to deduce / infer race, political opinions, trade union membership, religious or philosophical beliefs, sex life, sexual orientation (exception: lawful filtering or labeling of biometric data in law enforcement).
- **Real-time remote biometric identification** in publicly accessible spaces for law enforcement, with narrow exceptions:
  - Targeted search for specific victims of crime (abduction, trafficking, sexual exploitation, missing persons)
  - Prevention of specific, substantial, and imminent threat to life or physical safety, or terrorist attack
  - Localization or identification of suspect of specific serious crimes listed in Annex II (punishable by min 4 years imprisonment)
- Authorization required for the exceptions; emergency exceptions with post-hoc judicial review.

### Penalties for prohibited practices

Article 99(3): up to €35M or 7% of global annual turnover (whichever higher) — the maximum penalty tier.

## Tier 2: High-risk — Article 6 and Annex III

Two paths to high-risk classification (Article 6):

### Path 1: Annex I products (Article 6(1))

AI systems used as a safety component of products covered by EU harmonization legislation listed in Annex I, where the product (or the AI as the product) is subject to third-party conformity assessment under that legislation.

Annex I includes:

- Machinery
- Toys
- Recreational craft
- Lifts
- Equipment in explosive atmospheres
- Radio equipment
- Pressure equipment
- Cableway installations
- Personal protective equipment
- Gas appliances
- Medical devices (including in vitro diagnostic)
- Civil aviation
- Two- and three-wheel vehicles
- Agricultural and forestry vehicles
- Marine equipment
- Rail systems (interoperability)
- Motor vehicles (UN R155 / R156 territory)

Applicability: 2 August 2028 for high-risk AI systems in Annex I products (Art 113(c)(ii) as amended by Reg. 2026/1744; originally 2 August 2027).

### Path 2: Annex III areas (Article 6(2))

AI systems used in 8 areas listed in Annex III, regardless of whether they are part of an Annex I product.

Annex III areas:

1. **Biometrics** — biometric identification, biometric categorization, emotion recognition. With exceptions for verification and narrowly-defined contexts (some are prohibited under Article 5, leaving residual high-risk uses).
2. **Critical infrastructure** — safety components for management/operation of critical digital infrastructure, road traffic, water/gas/heating/electricity.
3. **Education and vocational training** — admissions and assessment systems, evaluation of learning outcomes, detection of prohibited behavior during tests.
4. **Employment, workers' management, access to self-employment** — recruitment / selection / advertising, hiring decisions, work-related decisions affecting terms (promotion/termination), task allocation, performance / behavior monitoring.
5. **Access to essential private and public services** — eligibility for benefits, creditworthiness / credit scoring (with exceptions), emergency call dispatch and triage, life/health insurance risk assessment and pricing.
6. **Law enforcement** — assessing reliability of evidence, risk of natural person becoming victim or offender, profiling for individual risk assessment in investigation, polygraph-equivalent systems. Subject to additional restrictions; some uses prohibited under Article 5.
7. **Migration, asylum, border control** — polygraph-equivalent, security/health/migration risk assessment, processing applications, detection of irregularities.
8. **Administration of justice and democratic processes** — assisting judicial authorities in fact research, application of law to facts, alternative dispute resolution. Influencing election outcomes / voting behavior.

Applicability: 2 December 2027 for Annex III high-risk systems (Art 113(c)(i) as amended by Reg. 2026/1744; originally 2 August 2026).

### Exemption: Article 6(3)

A system listed in Annex III is NOT high-risk if it does not pose significant risk of harm to health, safety, fundamental rights. Specifically when the AI:

- Performs narrow procedural task
- Improves result of previously completed human activity
- Detects decision-making patterns or deviations without replacing/influencing the previously completed human assessment
- Performs preparatory task for an assessment

Providers self-assess this exemption; document the assessment. National competent authority can challenge.

This is the most operationally consequential provision and the most underspecified. Commission guidance expected.

## Tier 3: Limited-risk (transparency obligations) — Article 50

Limited-risk AI systems are not heavily regulated but have transparency obligations:

- **AI systems interacting with natural persons** (chatbots, voice agents) — must inform users they are interacting with AI, unless this is obvious from the circumstances.
- **AI systems generating synthetic audio/image/video/text content** — providers must ensure outputs are marked in machine-readable format as artificially generated or manipulated.
- **Deepfakes** — deployers must disclose that content has been artificially generated or manipulated.
- **AI-generated text for informing public on matters of public interest** — must be disclosed as artificially generated unless human-reviewed.
- **Emotion recognition and biometric categorization** (where permitted) — affected persons must be informed.

Transparency obligations apply broadly; many systems have one or more applicable.

Applicability: 2 August 2026. Generative systems placed on the market before that date must meet the Art 50(2) marking duty by 2 December 2026 (Art 111(4), added by Reg. 2026/1744).

## Tier 4: Minimal/no risk

All other AI systems. No mandatory obligations under the AI Act. Voluntary codes of conduct (Article 95) encouraged.

Most AI systems globally fall here. Examples: spam filters, video-game AI, basic recommenders, simple ML-based features without consequential individual impact.

## GPAI tier (Article 51-55)

Cross-cutting tier for general-purpose AI models. Two subtiers:

### Baseline GPAI

Applies to GPAI models meeting "general-purpose" definition (Article 3(63)).

Obligations (Article 53):

- Technical documentation (training process, evaluation results, intended/excluded uses)
- Documentation for downstream providers using the model
- Copyright compliance (especially with respect to the TDM exception's opt-out)
- Summary of training content (template provided by AI Office)
- Cooperation with AI Office and authorities

### GPAI with systemic risk (Article 55)

Applies to GPAI models with "high impact capabilities" (Article 51). Threshold defined as having computational training compute exceeding 10^25 FLOP (Article 51(2)). Commission can also designate models based on capability assessment (Article 51(1)(b)).

Additional obligations:

- Model evaluation including adversarial testing (Article 55(1)(a))
- Risk assessment and risk mitigation at Union level (Article 55(1)(b))
- Tracking, documenting, reporting serious incidents (Article 55(1)(c))
- Adequate cybersecurity protections (Article 55(1)(d))

Notification to Commission required when threshold met (Article 52).

Applicability: 2 August 2025 for GPAI obligations generally; pre-existing GPAI models placed on market before 2 August 2025 have until 2 August 2027.

Detail in [[EU AI Act GPAI Obligations]].

## Classifying an AI system

Practical classification flow:

1. Is it AI under Article 3 definition? If no, AI Act doesn't apply.
2. Is it a prohibited practice under Article 5? If yes, illegal.
3. Is it Annex I-product-related and triggering Path 1 high-risk? If yes, high-risk obligations.
4. Is it in an Annex III area? If yes, check Article 6(3) exemption. If exempted, document and treat as limited-risk or minimal. If not exempted, high-risk.
5. Is it a GPAI model? If yes, GPAI obligations apply (in addition to any high-risk obligations if also classified high-risk).
6. Does it interact with persons, generate synthetic content, do deepfakes, do emotion recognition, do biometric categorization? If yes, limited-risk transparency obligations.
7. None of the above? Minimal/no risk.

A single system can have multiple classifications (e.g., a GPAI model with systemic risk that is also placed in a high-risk system). Obligations cumulate.

## SRE and AI-agent fit notes

For typical agent systems built on model APIs:

- **Most do not fall in Annex III high-risk categories** by default. Use case matters: an agent helping HR with hiring is in Area 4 (Employment); an agent helping with credit decisions is in Area 5 (Essential services); an agent moderating user-generated content for a major platform may be in Area 8 (Democratic processes) edge.
- **Limited-risk transparency obligations apply broadly.** Chatbot disclosure, synthetic content marking, deepfake labeling: low-cost compliance, broad applicability.
- **GPAI obligations affect upstream model providers**, not typically the org consuming the model. But: vendor due diligence increasingly includes GPAI compliance posture.
- **Edge cases:** agent systems with significant autonomy / decision-making over individuals or groups face elevated classification risk. Document the classification analysis; don't assume.

## Stefan-context implementation sketch

For solo / small-team work on agent systems serving EU customers:

- Run the classification flow per significant agent / AI feature.
- Most agent systems will land at limited-risk or minimal-risk.
- For systems crossing into high-risk territory: substantial implementation work; coordinate with client.
- Transparency obligations for limited-risk: implement chatbot disclosure, AI-content labeling as defaults.
- For vendor due diligence: track model provider GPAI compliance posture.

## See also

- [[EU AI Act Cluster|cluster MOC]] · [[EU AI Act Timeline]] · [[EU AI Act High-Risk Obligations]] · [[EU AI Act GPAI Obligations]]
- [[ISO 42001 Cluster]] (likely harmonized standard for high-risk compliance)
