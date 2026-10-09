title: OWASP LLM Top 10 Controversies
summary: Contested points and known limitations of the OWASP Top 10 for LLM Applications.
parent: owasp-llm-top-10
order: 100
labels: cross-cutting, owasp-llm-top-10
aliases: OWASP LLM Top 10 Controversies | OWASP LLM Critique | OWASP LLM Limitations
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/owasp-llm-top-10/OWASP LLM Top 10 Controversies.md
reviewed: no
---
> Contested points and known limitations of the OWASP Top 10 for LLM Applications. The list is widely-adopted and well-regarded; the critiques deserve attention.

## "Top 10" framing limits coverage

The 10-risk framing is operationally useful but enforces selection:

- Real AI security risk space is broader than ten categories.
- Boundary cases (some autonomous-agent risks, multimodal-specific risks, training-time supply-chain risks) get partial coverage.
- "Not in the Top 10" can be misread as "not important."

Counter: OWASP's Top 10 format is famous for accessibility. Sub-projects (OWASP AI Exchange, ASVS-equivalent) can cover more breadth.

Reality: practitioners using the Top 10 should be aware of what it doesn't cover and supplement from MITRE ATLAS, academic literature, vendor security advisories.

## Quantitative ranking is rough

The Top 10 ordering reflects working-group consensus, not measured prevalence or severity data:

- No public dataset on attack prevalence across LLM applications.
- Severity weighting is qualitative.
- The web Top 10 has data backing (CVE data, breach statistics); LLM Top 10 does not yet.

Implication: treating "LLM01 prompt injection is #1" as a hard ranking is overconfident. Treating it as "this is in the top of the list, deserves serious attention" is fine.

## Agent-system specifics under-covered

Several agent-system threats receive lighter coverage than their importance warrants:

- **Multi-step prompt injection** through tool-call chains.
- **Agent escalation** (agent gradually expanding its effective scope).
- **Multi-agent collusion** in systems with multiple agents.
- **Tool-call injection** at the tool API layer.
- **Memory poisoning** when agents have persistent memory.

LLM06 Excessive Agency provides umbrella coverage; specific agent-system threat patterns benefit from supplementary sources.

OWASP working group has discussed an Agent Top 10 as separate project; not committed as of 2026.

## Multimodal coverage is thin

Image, audio, video inputs and outputs receive light treatment:

- **Visual prompt injection** (instructions embedded in images): mentioned but not deeply addressed.
- **Audio prompt injection**: emerging threat; minimal coverage.
- **Multimodal model-specific vulnerabilities**: not categorized.
- **Cross-modal attacks** (text triggering image generation that triggers further behavior): underspecified.

As multimodal models become dominant, this gap will become more visible. Updates expected.

## Training-time risks underweighted

LLM04 Data and Model Poisoning covers training-time concerns at high level. Training-time risks are broader:

- **Data sourcing IP issues**: training-data IP infringement.
- **Data sourcing consent issues**: scraped data without consent.
- **Annotation worker exploitation**: training-data annotation supply chain.
- **Model architecture backdoors**: deliberate backdoors in published model architectures.
- **Pre-training data poisoning** at scale (subtle, large-scale corpus manipulation).

OWASP LLM Top 10 focuses on application-side concerns; training-time concerns are often outside the scope of organizations consuming hosted models. The asymmetry is real.

## "Defense in depth" is unsatisfying

The recurring mitigation advice across multiple risks is "defense in depth, no single control reliable." For practitioners wanting concrete answers, the framing is unsatisfying:

- What is the minimum viable defense set?
- How do I know if my defenses are sufficient?
- When do I stop adding layers?

The answer is genuinely "it depends on threat model, stakes, and risk tolerance" — but the OWASP LLM Top 10 doesn't make this dependency easier to navigate.

Counter: AI security is genuinely a new field with limited engineering certainty. Honesty about the uncertain state of practice is better than false confidence.

## Working group composition

OWASP working groups are open to participation. The LLM AI Cybersecurity & Governance Initiative working group includes practitioners, AI engineers, vendors, academics. Effects:

- **Vendor influence**: vendors (model providers, security tooling vendors) participate. Working group attempts vendor-neutrality; some critics argue vendor framing leaks into content.
- **English-language bias**: working group operates primarily in English; non-English-speaking practitioner voices underrepresented.
- **Western-organization concentration**: working group membership skews toward US / EU / UK organizations.

These are common open-community concerns; not specific to OWASP LLM Top 10. The working group is responsive to feedback; subsequent revisions reflect community input.

## Update cadence vs threat evolution

Annual revision cadence is faster than ISO / NIST cycles but still lags emerging threats:

- New jailbreak techniques emerge monthly.
- Tool-use attacks evolved rapidly through 2024-2025.
- Multi-agent systems are new attack surface; coverage lags maturation.
- Frontier-model-specific attacks may emerge faster than the Top 10 updates can absorb.

Practitioners track active threat sources (Anthropic / OpenAI / Google security advisories, MITRE ATLAS updates, academic preprints) alongside OWASP for current threat coverage.

## "We covered the Top 10" insufficiency

Same pattern as ISO 27001 compliance-vs-security:

- Covering the Top 10 doesn't mean the application is secure.
- Real-world breaches at "Top 10-covered" applications will happen.
- The Top 10 is starting point and minimum bar, not exhaustive assurance.

The lesson: the Top 10 is operational scaffolding. Treating coverage as security guarantee is the user error.

## Mitigation guidance varies in depth

Per-risk prevention guidance is uneven:

- LLM01 Prompt Injection: deep guidance, multiple defense layers.
- LLM06 Excessive Agency: clear principles, less specific implementation guidance.
- LLM09 Misinformation: high-level guidance; concrete factuality-checking techniques less developed.
- LLM10 Unbounded Consumption: standard rate-limiting guidance; less LLM-specific.

The unevenness reflects state-of-practice maturation. Some categories have more practitioner experience to draw from than others.

## Counterpoint: what OWASP LLM Top 10 still does well

The critique is calibrative. Structural benefits:

- **Practitioner-accessible threat taxonomy.** Operational, actionable, free.
- **De facto operational standard.** Practitioner literature, tooling, training, certification, vendor communications increasingly organize around the Top 10.
- **Faster update cadence than ISO / NIST.** Tracks threat-landscape evolution reasonably.
- **Vendor-neutral.** Open community process, not captured by single vendor.
- **Cross-references with adjacent frameworks** (NIST AI RMF, ISO 42001, MITRE ATLAS, OWASP web Top 10).
- **Tooling ecosystem.** PyRIT, Garak, Promptfoo, others organize testing around the categories.
- **Translation across languages.** OWASP volunteer translators produce non-English versions.

The critique is calibrative: OWASP LLM Top 10 is operational threat taxonomy + guidance. Treating it as complete AI security solution, or as substitute for adversarial testing, vendor management, defense-in-depth implementation, is the user error.

## See also

- [[OWASP LLM Top 10 Cluster|cluster MOC]] · [[OWASP LLM Top 10 2025]] · [[OWASP LLM Mitigations]] · [[OWASP LLM vs Top 10 Web]]
- [[ISO 42001 Controversies]] · [[NIST AI RMF Controversies]] (parallel framework critiques)
