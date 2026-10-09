title: NIST AI RMF
summary: Map of the NIST AI Risk Management Framework 1.0 (January 2023) and the Generative AI Profile (NIST AI 600-1, July 2024).
parent: index
order: 140
labels: ai-governance, moc, nist-ai-rmf, voluntary-frameworks
aliases: NIST AI RMF Cluster | NIST AI RMF | NIST Artificial Intelligence Risk Management Framework | AI RMF 1.0 | NIST AI 100-1
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nist-ai-rmf/NIST AI RMF Cluster.md
reviewed: no
---
> Map of the NIST AI Risk Management Framework 1.0 (January 2023) and the Generative AI Profile (NIST AI 600-1, July 2024). Voluntary, outcome-oriented US framework with four core functions (Govern, Map, Measure, Manage). Reference cluster for AI risk reasoning that complements ISO 42001 (management system) and bridges to OWASP LLM Top 10 (operational threats) and MITRE ATLAS (adversarial threats).

## Anchors

- [position](pillars/nist-ai-rmf/position.md): current view, dated, revisable
- [anchors](pillars/nist-ai-rmf/anchors.md): primary documents, NIST, AISI, named contributors

## Provenance

- **NIST** (National Institute of Standards and Technology) — US Department of Commerce. Long-standing publisher of voluntary frameworks influential globally (Cybersecurity Framework, SP 800-series, FIPS standards).
- **Executive Order 13859** (February 2019) — directed NIST to develop AI standards.
- **AI Risk Management Framework 1.0 (NIST AI 100-1)** — published January 2023. Four core functions, characteristics of trustworthy AI, sociotechnical framing.
- **AI RMF Playbook** — companion document. Actionable suggestions for each function and category. Updated multiple times since 2023.
- **AI RMF Roadmap** — published alongside 1.0. Charts NIST's planned future work.
- **AI RMF Crosswalks** — mappings to ISO 27001, ISO 42001, EU AI Act, NIST Privacy Framework, NIST CSF, OECD AI Principles. Published and updated through 2024-2025.
- **Generative AI Profile (NIST AI 600-1)** — published July 2024. 200+ suggested actions across 12 GenAI risk categories. The substantive GenAI extension of AI RMF 1.0.
- **NIST AI Safety Institute (AISI)** — established 2024 within NIST. Operationalizes AI safety work, particularly for frontier models. Survived Executive Order changes through 2025; structure ongoing.

## What NIST AI RMF is, in one paragraph

The NIST AI Risk Management Framework is a voluntary, US-origin framework for managing risks associated with AI systems. Outcome-oriented rather than control-prescriptive: it describes characteristics of trustworthy AI and four core functions for managing AI risk, with sub-categories per function and suggested actions per sub-category in the Playbook. Not certifiable. Applied across the AI lifecycle by any organization developing or using AI. Designed to bridge technical AI work, business decision-making, and broader stakeholder concerns. The Generative AI Profile (2024) extends the framework with substantive GenAI-specific risk content.

## The four core functions

The AI RMF organizes around four interdependent functions:

- **GOVERN** — culture, policies, processes, practices, and structures supporting AI risk management. The leadership and management spine.
- **MAP** — context establishment and risk identification. Understanding what AI systems are, where they operate, what risks they pose.
- **MEASURE** — analysis and tracking of identified risks using quantitative, qualitative, and mixed methods. Evaluation of trustworthy AI characteristics.
- **MANAGE** — risk treatment and ongoing management. Allocation of resources to mapped and measured risks, decisions about acceptable risk, monitoring.

The functions are cyclical and iterative, not sequential. GOVERN underlies all the others.

Detail in [[NIST AI RMF Core Functions]].

## Characteristics of trustworthy AI

The framework defines characteristics of trustworthy AI that ground the function-level work:

- **Valid and reliable** — performs as intended; predictable behavior.
- **Safe** — doesn't endanger life, health, property, environment.
- **Secure and resilient** — resists adversarial attacks; recovers from incidents.
- **Accountable and transparent** — clear responsibility chain; explainable decisions.
- **Explainable and interpretable** — humans can understand outputs.
- **Privacy-enhanced** — respects data subject rights, minimizes PII exposure.
- **Fair — with harmful bias managed** — equitable treatment across groups; bias identification and mitigation.

The characteristics are interdependent and sometimes in tension (e.g., explainability vs accuracy in deep models, fairness across multiple definitions). The framework expects practitioners to navigate the tensions explicitly.

## Generative AI Profile (NIST AI 600-1, July 2024)

GenAI-specific extension. 12 risk categories:

1. **CBRN information or capabilities** — AI helping non-experts produce chemical/biological/radiological/nuclear weapons.
2. **Confabulation** — fabricated content; hallucinations.
3. **Dangerous, violent, or hateful content** — generation of harmful content.
4. **Data privacy** — privacy violations through GenAI.
5. **Environmental impacts** — compute energy and water use.
6. **Harmful bias or homogenization** — biased outputs; bias amplification across users.
7. **Human-AI configuration** — over-reliance, complacency, role confusion.
8. **Information integrity** — generated content polluting information ecosystem.
9. **Information security** — GenAI as attack tool and as attack surface.
10. **Intellectual property** — IP infringement, training-data IP issues.
11. **Obscene, degrading, or abusive content** — CSAM and similar.
12. **Value chain and component integration** — supply-chain risks specific to GenAI stack.

200+ suggested actions across the four functions and 12 categories. The Profile is the operational depth that AI RMF 1.0 lacked for GenAI.

Detail in [[NIST AI RMF GenAI Profile]].

## NIST AI RMF vs ISO 42001

| Aspect | NIST AI RMF | ISO 42001 |
|---|---|---|
| Type | Voluntary framework | Certifiable standard |
| Owner | NIST (US) | ISO / IEC |
| Approach | Outcome-oriented | Management-system requirements |
| Functions / clauses | Govern / Map / Measure / Manage | Cl 4-10 (Annex SL) |
| Controls / actions | ~70 sub-categories, 200+ GenAI Profile actions | ~38 Annex A controls |
| Certifiable | No | Yes |
| Cost (org) | Adoption only | Cert costs |
| Update cycle | Frequent | 5-10 years |
| US procurement | Strong (federal AI EO references) | Limited |
| EU procurement | Limited | Strong (with AI Act harmonization) |

Complementary, not competing. Detail in [[NIST AI RMF vs ISO 42001]].

## Adoption patterns

- **US federal contractors** — NIST AI RMF is the preferred reference for AI work via Executive Orders (EO 14110 October 2023; rescinded January 2025 but NIST work continues).
- **US AI-feature SaaS** — many citing NIST AI RMF alignment in public communications.
- **Cross-border AI companies** — often implement both NIST AI RMF and ISO 42001.
- **Outside US** — voluntary adoption growing, particularly in jurisdictions without strong domestic AI governance frameworks.

## Why this matters for SRE and AI-agent work

- **Outcome-oriented framing helps prioritize.** The four functions and characteristics-of-trustworthy-AI bring focus to "what are we actually trying to achieve" rather than "what controls do we have."
- **GenAI Profile is operationally substantive.** The 200+ actions provide concrete suggestions for generative-AI work. Closes the gap that ISO 42001's generality leaves open.
- **Crosswalk to ISO 42001** simplifies dual implementation. Function-to-clause mapping reduces re-work.
- **US procurement signal.** US federal AI work and US-customer-facing AI work increasingly reference NIST AI RMF; alignment statement carries weight.
- **AISI engagement.** Frontier model evaluations, safety testing collaborations, voluntary commitments — NIST AISI's work shapes broader practice.

## Stefan-context relevance

Stefan does AI-agent and SRE work touching:

- Agent systems with non-determinism, autonomous-action concerns, vendor-model dependencies
- Generative AI risk categories directly applicable
- Cross-jurisdictional positioning (NIST for US, ISO 42001 for EU)
- Client engagements where AI governance evidence is procurement-load-bearing

Cluster atoms should:

- Translate framework outcomes to operational practice
- Bridge AI RMF, ISO 42001, OWASP LLM Top 10, MITRE ATLAS
- Surface GenAI Profile actions relevant to agent systems
- Stay implementation-grounded

## Related clusters and atoms

- [[ISO 42001 Cluster|ISO 42001]] — sibling AI governance standard, certifiable
- [[OWASP LLM Top 10 Cluster]] — operational threat taxonomy; complementary to NIST AI RMF
- [[EU AI Act Cluster]] — regulatory driver; NIST AI RMF informs but does not satisfy AI Act
- [[ISO 27001 Cluster|ISO 27001]] — InfoSec management; supports AI risk management on the security dimension

## Conventions for this cluster

- Atoms named `NIST AI RMF <Topic>.md` with consistent structure
- AI RMF 1.0 + GenAI Profile July 2024 are default version references
- Cross-link to ISO 42001 cluster atoms where content overlaps
- Cite NIST AI RMF function-and-subcategory references explicitly (e.g., GOVERN 1.1, MAP 2.3)
- Carry GenAI Profile action references where directly applicable

## See also

[[NIST AI RMF Cluster]] (pillars MOC) · [position](pillars/nist-ai-rmf/position.md) · [anchors](pillars/nist-ai-rmf/anchors.md) · [[ISO 42001 Cluster]] · [[OWASP LLM Top 10 Cluster]] · [[EU AI Act Cluster]]
