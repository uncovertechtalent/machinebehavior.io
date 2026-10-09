title: OWASP LLM Top 10 anchors
summary: Primary documents, OWASP working group, related projects, named voices, reference resources for the OWASP LLM Top 10 cluster.
parent: owasp-llm-top-10
order: 6
labels: anchors, owasp-llm-top-10
aliases: OWASP LLM Top 10 Anchors | OWASP LLM Sources | OWASP LLM Reading List
type: anchors
created: 2026-05-12
updated: 2026-05-12
origin: pillars/owasp-llm-top-10/anchors.md
reviewed: no
---
> Primary documents, OWASP working group, related projects, named voices, reference resources for the OWASP LLM Top 10 cluster.

## Primary documents

- **OWASP Top 10 for LLM Applications v2.0 (2025 edition)** — published November 2024. Current version. Free PDF from owasp.org/www-project-top-10-for-large-language-model-applications/.
- **OWASP Top 10 for LLM Applications v1.1** — October 2023 revision of v1.0 (August 2023). Historical reference.
- **OWASP GenAI Red Teaming Guide** — companion document. Methodology for red-teaming LLM-integrated applications.
- **OWASP LLM Cybersecurity & Governance Checklist** — implementation-oriented companion checklist.
- **OWASP AI Exchange** — broader AI security knowledge base. Includes LLM Top 10 content + adjacent AI security guidance.

## Operating body

- **OWASP Foundation** — Open Worldwide Application Security Project. Long-standing community-driven application security organization. Foundation owns the IP; contributions are community-sourced.
- **OWASP LLM AI Cybersecurity & Governance Initiative** — working group established 2023. Multiple sub-working-groups producing the LLM Top 10, the GenAI Red Teaming Guide, the Cybersecurity Checklist, the AI Exchange.

## Related OWASP projects

- **OWASP Top 10 (Web)** — the original, dating to 2003. Now 2021 edition. Established the "Top 10" format.
- **OWASP API Security Top 10** — API-specific risks.
- **OWASP Mobile Top 10** — mobile-application risks.
- **OWASP ASVS** (Application Security Verification Standard) — comprehensive verification standard.
- **OWASP SAMM** (Software Assurance Maturity Model).
- **OWASP Cheat Sheet Series** — practical guidance per topic.
- **OWASP Dependency-Check / Dependency-Track** — supply-chain tooling.

## Related external taxonomies / frameworks

- **MITRE ATLAS** — Adversarial Threat Landscape for Artificial-Intelligence Systems. Adversary tactics, techniques, procedures specific to AI. Complementary to OWASP LLM Top 10.
- **MITRE ATT&CK** — adversary TTP framework for general cyber.
- **MITRE D3FEND** — defensive countermeasure framework.
- **NIST AI RMF GenAI Profile (NIST AI 600-1)** — Category 9 Information Security overlaps with OWASP LLM Top 10.
- **NIST SP 800-218A** — AI development security extension (in development).
- **AI Risk Atlas (IBM)** — AI risk taxonomy.
- **AVID (AI Vulnerability Database)** — community AI vulnerability tracking.

## Adversarial-AI research

Academic and industry research that informs the Top 10:

- **Carlini et al.** — adversarial ML, model extraction, membership inference.
- **Wallace et al.** — universal adversarial triggers, prompt-injection-adjacent.
- **Greshake et al.** — indirect prompt injection.
- **Various jailbreak research groups** — Anthropic safety team, OpenAI red team, academic labs.
- **Anthropic Constitutional AI papers** — defense-side perspectives.
- **OpenAI safety publications** — defense-side perspectives.

## Practitioner tooling (open source)

Tools that organize attacks by OWASP LLM Top 10 categories:

- **PyRIT** (Microsoft) — Python Risk Identification Toolkit for generative AI.
- **Garak** (NVIDIA) — LLM vulnerability scanner.
- **Promptfoo** — eval framework with red-teaming features.
- **DeepEval** — LLM evaluation framework with safety tests.
- **Buttercup** — RAG-specific evaluation framework.
- **HiddenLayer ModelScanner** — model file vulnerability scanner.

## Named contributors and voices

### OWASP LLM working group leads

- **Steve Wilson** — co-lead of OWASP LLM AI Cybersecurity & Governance Initiative.
- **Various working group co-leads** — published widely on LLM security.

### Independent AI security voices

- **Simon Willison** — practitioner; coined "prompt injection" term (September 2022). Active commentary on the threat landscape.
- **Andrej Karpathy** — practitioner perspective on LLM security and engineering.
- **Riley Goodside** — early prompt-injection practitioner; demo-driven public communication.
- **Pliny the Liberator** — jailbreak demonstrations; public-research role.
- **Various AI safety researchers** at Anthropic, OpenAI, Google DeepMind, Microsoft, academic labs.

### Critical voices

- **Various security researchers** arguing OWASP LLM Top 10 is incomplete (multimodal, agent-specific, training-time gaps).
- **AI safety researchers** distinguishing security (this Top 10) from safety (broader concerns).

## Reference resources

- **owasp.org/www-project-top-10-for-large-language-model-applications/** — official OWASP LLM Top 10 project page.
- **genai.owasp.org** — broader OWASP GenAI Security Project portal.
- **MITRE ATLAS** at atlas.mitre.org.
- **AI Vulnerability Database** at avidml.org.
- **HuggingFace AI Cookbook** — defensive patterns content.

## Regulatory and procurement context

- **EU AI Act** — high-risk and GPAI risk management obligations align with OWASP LLM Top 10 content.
- **NIST AI RMF GenAI Profile** — Category 9 maps closely to OWASP LLM Top 10.
- **ISO 42001 risk register inputs** — practitioners cite OWASP LLM Top 10 for AI-specific risk identification.
- **Vendor due diligence** — model provider security postures increasingly evaluated against OWASP LLM Top 10 categories.

## See also

- [[OWASP LLM Top 10 Cluster|cluster MOC]] · [position](pillars/owasp-llm-top-10/position.md)
- [[NIST AI RMF Cluster]] · [[ISO 42001 Cluster]] · [[EU AI Act Cluster]]
