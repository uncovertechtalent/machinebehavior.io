title: NIST AI RMF GenAI Profile
summary: NIST AI 600-1, published July 2024.
parent: nist-ai-rmf
order: 100
labels: framework-profile, nist-ai-rmf
aliases: NIST AI RMF GenAI Profile | NIST AI 600-1 | GenAI Profile | NIST AI RMF Generative AI Profile
type: framework-profile
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nist-ai-rmf/NIST AI RMF GenAI Profile.md
reviewed: no
---
> NIST AI 600-1, published July 2024. The Generative AI Profile extending the NIST AI Risk Management Framework 1.0 with substantive content for generative AI systems. 200+ suggested actions across the four core functions and 12 GenAI-specific risk categories.

## What the GenAI Profile adds

AI RMF 1.0 (January 2023) was general-AI-focused. The GenAI Profile (NIST AI 600-1, July 2024) extends it with:

- **12 GenAI-specific risk categories** — identifying risks particular to generative AI.
- **200+ suggested actions** — concrete steps mapped to AI RMF functions (Govern, Map, Measure, Manage) and the 12 risk categories.
- **Context-specific guidance** — recognizes generative AI as distinct from predictive ML in risk characteristics.
- **Reference to operational practices** — implicit alignment with OWASP LLM Top 10, MITRE ATLAS, sector guidance.

The Profile is positioned as living guidance; updates expected as GenAI practice evolves.

## The 12 risk categories

### 1. CBRN information or capabilities

GenAI providing chemical, biological, radiological, nuclear weapons information or capabilities to non-experts.

Concerns:

- Lowering the expertise barrier to weapon design or production
- Aggregating dual-use information in dangerous combinations
- Bypassing established safeguards (chemical-precursor controls, biosecurity oversight)

Example MANAGE actions: refusal training for CBRN topics, output filtering for dual-use content, red-team testing for CBRN scenarios.

### 2. Confabulation

GenAI fabricating content that appears authoritative but is false. Hallucinations.

Concerns:

- Factually incorrect outputs presented confidently
- Citation fabrication
- User over-reliance leading to downstream errors

Example MEASURE actions: factuality evaluation, citation verification testing, distribution shift monitoring.

### 3. Dangerous, violent, or hateful content

GenAI generating content that causes physical harm, glorifies violence, or expresses hatred toward groups.

Concerns:

- Harassment generation
- Self-harm encouragement
- Violence glorification
- Hate-speech amplification

Example GOVERN actions: content policy with red lines, governance review of policy enforcement effectiveness.

### 4. Data privacy

Privacy violations through GenAI: training-data PII leakage, inference-time PII handling, retention concerns.

Concerns:

- Memorized training data including PII surfacing in outputs
- User PII in prompts being retained by vendor
- Cross-user data leakage in shared-model scenarios
- Data subject rights challenges (right to erasure for model-encoded data)

Example MAP actions: privacy impact assessment for GenAI deployments, training-data privacy review.

### 5. Environmental impacts

Compute energy and water consumption of GenAI training and inference.

Concerns:

- Training-compute carbon footprint
- Inference-compute scaling impact
- Water consumption for cooling
- Hardware lifecycle environmental impact

Example MAP actions: environmental impact assessment for significant GenAI deployments.

### 6. Harmful bias or homogenization

Biased outputs and bias amplification across users.

Concerns:

- Outputs reflecting training-data biases (race, gender, geography, language)
- Bias amplification when GenAI outputs feed back into training data
- Homogenization of perspectives via uniform model use
- Cultural bias toward dominant-language / dominant-culture training data

Example MEASURE actions: bias evaluation across demographic dimensions, output diversity measurement.

### 7. Human-AI configuration

Risks from how humans interact with AI: over-reliance, complacency, role confusion.

Concerns:

- Over-trust in AI outputs leading to errors
- Skill atrophy when AI handles routine work
- Role confusion between human and AI responsibilities
- AI replacing human judgment where human judgment is appropriate

Example GOVERN actions: human-AI role policies, complacency mitigation procedures.

### 8. Information integrity

GenAI-generated content polluting information ecosystem.

Concerns:

- Synthetic media (deepfakes) including non-consensual intimate imagery and impersonation
- Mass-generated misinformation
- Information landscape degradation through low-quality AI content
- Provenance/authenticity erosion

Example MANAGE actions: provenance metadata, content authenticity (C2PA standards), output watermarking.

### 9. Information security

GenAI as attack tool and as attack surface.

Concerns:

- GenAI as offensive cyber capability (phishing, code generation, vulnerability discovery)
- GenAI applications vulnerable to prompt injection
- Model supply chain compromise
- Training-data poisoning
- Adversarial inputs causing model misbehavior

Example MEASURE actions: prompt-injection testing, adversarial robustness evaluation. Maps to OWASP LLM Top 10.

### 10. Intellectual property

IP infringement through GenAI.

Concerns:

- Training data IP issues (copyrighted material used without license)
- Output IP issues (verbatim reproduction of training data, infringing derivative works)
- Trademark issues in generated content
- Patent considerations for AI-generated inventions

Example MAP actions: IP risk assessment per GenAI deployment.

### 11. Obscene, degrading, abusive content

CSAM and similar harmful content.

Concerns:

- CSAM (child sexual abuse material) generation
- Non-consensual intimate imagery
- Degrading content of identifiable individuals

Example GOVERN actions: zero-tolerance policy, mandatory abuse reporting protocols (NCMEC referral for CSAM in US, equivalent in other jurisdictions).

### 12. Value chain and component integration

Supply-chain risks specific to the GenAI stack.

Concerns:

- Foundation-model provider concentration
- Component integration risks (RAG retrievers, vector DBs, agent frameworks, tooling)
- Training-data supply chain (data curation, annotation, sourcing)
- Plugin / tool / extension supply chain for agent systems

Example MANAGE actions: vendor due diligence per supply-chain component, component change monitoring.

## Function-by-function action density

The 200+ actions distribute across the four AI RMF functions:

- **GOVERN**: ~50 actions. Policy, accountability, third-party management, culture.
- **MAP**: ~50 actions. Context, capabilities, risk identification per category.
- **MEASURE**: ~70 actions. Evaluation, testing, monitoring per category.
- **MANAGE**: ~30 actions. Risk treatment, response, recovery.

(Approximate distribution; actual document provides exact mapping.)

## How to use the Profile

### As risk register input

The 12 categories provide a usable taxonomy for AI risks. Each risk in the org's register can be tagged with the relevant categories. Treatment selection draws on suggested actions.

### As evaluation harness scope

The MEASURE actions describe what to evaluate. For an agent system, evaluation harness should cover:

- Confabulation (factuality, hallucination rate)
- Information security (prompt-injection, adversarial robustness)
- Data privacy (PII leakage)
- Harmful bias (across user demographics)
- Information integrity (output veracity)

### As vendor due diligence checklist

The GOVERN and MANAGE actions on third-party / value-chain integration provide a checklist for evaluating model providers and other GenAI stack vendors.

### As gap analysis tool

Map current practice against the actions. Identify gaps. Prioritize closure based on org-specific risk profile.

## Common implementation patterns

- **Subset adoption**: not all 200+ actions apply to every org. Risk-driven subset selection is the practical approach.
- **Category prioritization**: pick the 3-5 highest-priority categories for the org's context, build coverage there, expand over time.
- **Layered with OWASP / MITRE**: GenAI Profile categories 1, 6, 8, 9 overlap with OWASP LLM Top 10. Implementation uses OWASP/MITRE for technical depth, GenAI Profile for management-system framing.

## Common implementation gaps

- **Treating the Profile as exhaustive checklist.** Not all actions apply; risk-driven selection required.
- **Category 12 (value chain) under-implemented.** Foundation-model provider relationships often treated lightly; the Profile expects more rigorous due diligence and monitoring.
- **Category 5 (environmental) not addressed.** Energy and water impact rarely on AI governance radar; the Profile expects assessment.
- **Category 7 (human-AI configuration) handled informally.** Over-reliance and complacency rarely have explicit governance treatment.

## SRE and AI-agent fit notes

For agent systems serving enterprise customers, the most load-bearing categories are typically:

1. **Category 9 (Information security)** — prompt injection, tool misuse, adversarial inputs. Heavy operational work.
2. **Category 4 (Data privacy)** — customer PII handling through agents and model APIs. Heavy contractual + technical work.
3. **Category 2 (Confabulation)** — factuality and hallucination management. Heavy evaluation harness work.
4. **Category 12 (Value chain)** — model provider relationships, RAG architecture, agent framework dependencies. Heavy vendor management work.
5. **Category 7 (Human-AI configuration)** — autonomy levels, kill-switches, human-in-the-loop. Design-time decisions.

Categories 1 (CBRN), 11 (CSAM-style), 3 (violent/hateful) typically handled by model provider safety training; org-side concerns are usage policy and reporting protocols.

Categories 5 (environmental), 6 (bias), 8 (information integrity), 10 (IP) require attention but typically less operational depth for agent systems specifically.

## Stefan-context implementation sketch

For solo / small-team agent system work:

- **Risk register categorization**: tag each AI risk with relevant GenAI Profile category.
- **Highest-priority categories**: 9 (Information security), 4 (Data privacy), 12 (Value chain) for typical engagement work.
- **Lightweight implementation**: pick 5-10 specific actions per top category; implement them; document.
- **Bridge to OWASP LLM Top 10** for technical depth on Category 9.
- **Bridge to GDPR / ISO 27701** for technical depth on Category 4.

## See also

- [[NIST AI RMF Cluster|cluster MOC]] · [[NIST AI RMF Core Functions]] · [[NIST AI RMF vs ISO 42001]]
- [[OWASP LLM Top 10 Cluster]] (operational threat depth)
- [[EU AI Act Cluster]] (regulatory overlap on synthetic content, transparency)
