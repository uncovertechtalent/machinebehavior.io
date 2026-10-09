title: ITIL Controversies
summary: Contested points and known failure modes of ITIL and the certification ecosystem.
parent: itil
order: 100
labels: cross-cutting, itil
aliases: ITIL Controversies | ITIL Critique | ITIL Failure Modes | ITIL Bureaucracy | ITIL vs DevOps
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/itil/ITIL Controversies.md
reviewed: no
---
> Contested points and known failure modes of ITIL and the certification ecosystem. ITIL is widely used and widely criticized; both deserve attention. The critique is not that ITIL should be abandoned but that practitioner reality often falls short of framework intent.

## Process-heaviness and bureaucratization

The most-cited critique. Recurring patterns:

- **Change Advisory Boards (CABs)** that meet weekly to approve every change, including low-risk routine ones. Multi-week approval cycles for changes that should take hours.
- **Incident-management process layers** that route a simple ticket through tier 1, tier 2, tier 3 escalation when direct routing to subject-matter expert would resolve faster.
- **Configuration Management Database (CMDB)** projects that consume years and produce data of dubious accuracy by completion.
- **Documentation requirements** that grow to fill available capacity, with stale documents that nobody reads.

ITIL v3 (2007) was particularly prone to over-implementation. ITIL 4 (2019) explicitly criticizes these patterns — the Change Enablement practice description directly addresses CAB pathologies, and the "keep it simple and practical" guiding principle is a counter to documentation creep.

Counter-argument: the failure modes are not framework requirements. ITIL recommendations are adapt-as-needed; orgs that implement bureaucracy chose it. The framework itself is process-light if read carefully.

Reality: practitioner culture, tooling defaults, and procurement signals all push toward heavier implementation than the framework requires. The over-implementation is institutional, not personal.

## ITIL vs DevOps / SRE tension

A persistent narrative since 2010:

- **ITIL emphasizes stability through control**; DevOps / SRE emphasize stability through engineering discipline and continuous delivery.
- **ITIL Change Management (v3) emphasizes approval gates**; DevOps continuous-delivery emphasizes automated testing and gradual rollout.
- **ITIL Service Management roles** are often distinct from engineering roles; DevOps blurs the boundary.
- **ITIL's enterprise IT lineage** vs DevOps' tech-native lineage created cultural mismatch.

Resolution attempts:

- **ITIL Practitioner (2016)** introduced the seven guiding principles, many compatible with DevOps thinking.
- **ITIL 4 (2019)** added High-Velocity IT (HVIT) module explicitly addressing DevOps integration.
- **DevOps Institute** (acquired by PeopleCert 2022) provides DevOps-specific certifications complementary to ITIL.

Current state: tension reduced but not eliminated. Tech-native organizations still tend toward DevOps / SRE vocabulary without explicit ITIL framing. Enterprise IT organizations have begun adopting DevOps practices within ITIL framing. Hybrid practitioner identities are increasingly common.

## Certification mill critique

ITIL has generated significant certification revenue over multiple decades. The Foundation exam in particular is widely regarded as memorization-driven rather than capability-validating.

Patterns:

- **Foundation as box-checking.** Practitioners pass Foundation without applying the framework. Procurement signal works; capability development does not.
- **Boot-camp culture.** Three-day Foundation courses optimized for exam pass-rate rather than understanding.
- **Continuing demand for credentials.** Each version bump (v2 → v3 → ITIL 4) creates re-certification demand. PeopleCert's 2023 introduction of CPD-renewal mandates further extends this.
- **CV credential-counting.** Hiring practices that count certifications can incentivize credential acquisition over capability.

PeopleCert's position: certifications signal vocabulary fluency and framework knowledge; practitioner capability is built through application. Critique: the marketing positions certifications more strongly than this honest characterization.

Reality: the Foundation certificate is a reasonable vocabulary signal at low cost. Treating it as more than that is the user error.

## PeopleCert ownership concentration

In 2021 PeopleCert acquired AXELOS, consolidating ITIL, PRINCE2, MSP, P3O, RESILIA, and adjacent IP under single ownership. Acquired DevOps Institute in 2022.

Concerns raised:

- **Framework openness.** ITIL was previously co-owned by UK government (Cabinet Office); now wholly private. Long-term governance trajectory unclear.
- **Pricing pressure.** Single ownership creates pricing power; exam and training fees have risen.
- **CPD renewal scheme** introduced 2023 — replacing lifetime certifications with cycle-renewal requirements is revenue-favorable for PeopleCert and adds ongoing cost for practitioners.
- **IP concentration.** Multiple best-practice frameworks under single private ownership concentrates governance risk.

Counter-argument: PeopleCert has invested in content currency (2023 refresh) and digital infrastructure (PeopleCert Wallet). Single ownership reduces fragmentation that complicated multi-stakeholder governance under AXELOS.

Reality: the concentration is real; the long-term implications depend on PeopleCert governance choices.

## Tooling capture

ServiceNow's dominance in enterprise ITSM tooling (60-70% market share) means that "doing ITIL" in practice often means "configuring ServiceNow per its ITIL implementation":

- ServiceNow's data model is opinionated. CMDB structure, incident classification, change types, service catalog all reflect ServiceNow design choices.
- Customizations are technically possible but rarely fully exercised due to upgrade-cost concerns.
- New ITSM practitioners are often more familiar with "the ServiceNow way" than with ITIL framework content.

Result: framework intent and tool implementation diverge. ITIL 4's guidance to "start where you are" can in practice mean "start with what ServiceNow does."

Similar dynamics with Jira Service Management (Atlassian), BMC Helix, Ivanti, others — at lower market share but same pattern.

## AI / autonomous-operations gaps

ITIL 4 (2019) acknowledged AI in passing; 2023 refresh expanded slightly. Substantive gaps remain:

- **AIOps integration.** Monitoring and Event Management practice description does not deeply integrate AIOps adoption patterns. Practitioner work fills the gap.
- **Autonomous agent operations.** No specific practice content for agent-system operations.
- **Prompt-engineering as discipline.** Knowledge Management practice could plausibly cover this; current content does not.
- **SLO definition for non-deterministic systems.** Service Level Management practice content assumes deterministic services.
- **Vendor-side model behavior.** Supplier Management practice content does not address the specific dynamics of model-provider relationships.
- **AI-incident classification and response.** Incident Management practice does not address AI-related failure modes (hallucination, prompt-injection-induced behavior, tool-misuse).

ISO/IEC 42001 (AI management system, 2023) is the parallel ISO development addressing AI governance. ITIL has not yet produced equivalent depth.

## Practice-list inconsistency

The 34 ITIL 4 practices vary substantially in depth and quality of description:

- **Well-developed practices**: Incident Management, Change Enablement, Problem Management, Service Level Management. Decades of v2 / v3 evolution behind them.
- **Thin practices**: Knowledge Management, IT Asset Management, Service Catalogue Management. Practice guides exist but are shallower.
- **Borrowed practices**: General Management practices like Strategy Management, Portfolio Management, Risk Management. Adapted from broader management thinking; depth varies.

The asymmetry reflects historical development paths. New adopters expecting consistent depth across all 34 practices are typically disappointed.

## "We have ITIL but our IT operations are bad"

Mirror of the ISO 27001 / TISAX compliance-vs-substance pattern:

- ITIL-trained workforces with mature ITSM tooling and well-attended ceremony, producing IT operations that nonetheless fail their customers.
- Common failure modes: change-approval cycles that block urgent work, incident-management that prioritizes ticket-handling over resolution, problem-management that produces reports nobody reads, configuration-management with stale data.

The lesson: ITIL adoption is procedure adoption, not capability development. Capability is built by doing the work well, with the framework as scaffolding. Substituting framework adoption for capability development is a common antipattern.

## Geographic and language bias

ITIL originated in UK government. Original language: English. Cultural assumptions: UK / Anglosphere enterprise.

Implications:

- Translation friction in non-English-language contexts.
- Cultural assumptions about hierarchy, decision-making, communication may not transfer cleanly.
- Adoption patterns vary by region: UK / North America / Australia heaviest, continental Europe variable, Asia-Pacific increasing, regional adaptation common.

PeopleCert has translated framework content into multiple languages; cultural translation lags linguistic translation.

## Cost gating for small organizations

Implementation costs (training, tooling, time) gate smaller organizations:

- **Tool licensing**: ServiceNow per-user pricing scales with org size; SMB-tier tooling (Freshservice, Jira SM) cheaper but with capability gaps.
- **Training and certification**: per-person Foundation cost €1-2k with training; multi-person workforce coverage scales.
- **Implementation effort**: 6-12 months to mature even a subset of practices requires significant capacity.

For organizations under 50 staff, "doing ITIL" formally is often disproportionate. Practice-level adoption (selected practices at modest maturity) without tooling-heavy implementation is the realistic path.

## Counterpoint: what ITIL still does well

The critique is not that ITIL should be replaced. Structural benefits:

- **Vocabulary as bridge.** Cross-team, cross-vendor, cross-organization conversations benefit from shared terminology.
- **Framework as enumeration.** The 34 practices provide a complete-enough enumeration of service-management capabilities. New leaders use it as a gap analysis aid.
- **Guiding principles as durable guidance.** The seven guiding principles survive translation outside ITIL and serve as general operating-model recommendations.
- **Service Value System as conceptual reset.** ITIL 4's SVS / value-chain model is a meaningful improvement over v3's lifecycle. The reframe accommodates Agile, Lean, DevOps, customer-centricity.
- **Procurement signal.** ITIL Foundation certificates and ITIL-aligned operations satisfy a recurring procurement question with minimal effort.

The critique is calibrative: ITIL is a framework that scaffolds service-management capability. Treating it as a capability substitute, a security-of-process guarantee, or a complete solution for modern operations is the user error.

## See also

- [[ITIL Cluster|cluster MOC]] · [[ITIL Version History]] · [[ITIL vs ISO 20000]]
- [[ISO 27001 Controversies]] · [[TISAX Controversies]] (parallel critiques of adjacent frameworks)
