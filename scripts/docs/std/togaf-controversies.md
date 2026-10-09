title: TOGAF Controversies
summary: Contested points and known failure modes of TOGAF and the enterprise-architecture-function model it supports.
parent: togaf
order: 100
labels: cross-cutting, togaf
aliases: TOGAF Controversies | TOGAF Critique | TOGAF Failure Modes | Enterprise Architecture Critique | Shelfware Architecture
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/togaf/TOGAF Controversies.md
reviewed: no
---
> Contested points and known failure modes of TOGAF and the enterprise-architecture-function model it supports. TOGAF is dominant in enterprise EA because it is the most complete framework available, not because it is uncontested. Practitioners building or working alongside EA functions should know the soft spots.

## "Shelfware architecture" — the headline failure mode

The most-cited critique. EA functions produce target architectures, roadmaps, and reference architectures that delivery teams ignore. The documents become artefacts, not constraints. The pattern:

- The EA function spends months producing a target architecture and a roadmap.
- Delivery teams, under pressure to ship, build what is expedient.
- The architecture documents age; the gap between "the architecture" and "what was built" widens.
- The next strategic-planning cycle produces a new target architecture, equally ignored.

TOGAF's governance model (Architecture Board, Compliance reviews, Architecture Contracts) is meant to prevent this. In practice, EA functions often lack the organizational authority to enforce it — they can recommend, not require. The result is documentation that signals activity without changing outcomes.

Root cause is usually organizational, not framework: the EA function reports too low, lacks executive backing, or has no enforcement mechanism. But TOGAF's central-EA-function premise makes the function vulnerable to this — it concentrates architecture authority in a body that often does not have the power to use it.

## ADM-as-waterfall misuse

The ADM is drawn as a cycle, described as iterative, and explicitly tailorable. It is frequently implemented as a linear, multi-month, big-design-up-front exercise: complete Phase A, then B, then C, then D, producing full content-framework deliverables, before any building starts. This is the antithesis of Agile / DevOps delivery.

TOGAF's documentation says not to do this — the iteration patterns, the "minimum viable architecture" thinking in the 10th Edition, the agile-EA Series Guide all push against it. But the cultural inertia is strong: architects trained on the by-the-book ADM, governance processes that demand the full deliverable set, procurement contracts that specify TOGAF-conformant outputs — all pull toward the waterfall implementation.

## Documentation overhead

A full ADM cycle with complete content-framework deliverables (Architecture Vision, Architecture Definition Document spanning four domains, Architecture Requirements Specification, Architecture Roadmap, Implementation and Migration Plan, the recommended artifacts per phase) is a vast amount of documentation. Most of it ages quickly — the technology landscape changes, the business reorganizes, the roadmap is overtaken by events. Organizations that produce the full set generate maintenance burden without proportionate value, and the documents are read by few.

The framework permits lean adoption — produce only the deliverables and artefacts the engagement needs. The 10th Edition Series Guides encourage this. But "TOGAF says to produce X" is a common justification for over-documentation, and governance processes often demand the full set.

## Certification-mill problem

The TOGAF certification scheme generates significant revenue for The Open Group and accredited training partners. TOGAF Foundation in particular is widely regarded as a memorization exam — ADM phase names, content-framework structure, terminology — that validates exam-taking, not architecture capability.

Certificate-counting in CVs and procurement signals incentivizes credential acquisition over capability development. "We have N TOGAF-certified architects" is a weak signal of an organization's actual architecture capability. The experience-based Open CA program is the more credible signal, but it is much less commonly held because it requires substantial documented experience and a board review, not a multiple-choice exam.

## The central-EA-function model is contested

TOGAF is the standard tool of the central-EA-function model: a body that owns the enterprise architecture, sets technology standards, reviews designs for compliance, and dictates direction. This model is under pressure from:

- **Platform engineering** — the idea that a platform team provides paved roads and self-service capabilities, and product teams build on them autonomously, rather than a central function dictating architecture.
- **Product-team autonomy** — "you build it, you run it"; teams own their architecture decisions within guardrails.
- **DevOps culture** — fast feedback, small batches, decentralized decision-making; the antithesis of a central body reviewing designs.
- **Team Topologies** — the "enabling team" concept: EA repositioned as a team that helps other teams, not a team that controls them.

The evidence (Accelerate / DORA research, the success of platform-engineering at scale) favours decentralized models for delivery velocity. EA functions are increasingly repositioning as enabling / advisory rather than controlling — but the repositioning is incomplete, and many EA functions still operate the control model. TOGAF, with its Architecture Board and Compliance reviews, leans toward the control model; the framework can support enablement but does not naturally point there.

## Abstraction-heaviness and the practice gap

TOGAF documentation is dense and abstract. The path from "TOGAF certified" to "doing TOGAF productively" is unclear — many certified practitioners never apply the framework because the gap between the abstract content and concrete practice is large. Critics (Svyatoslav Kotusev's empirical research is the sharpest example) document a significant difference between TOGAF-as-described and EA-as-practiced: organizations claim TOGAF adoption but actually do something much lighter and more pragmatic, with the TOGAF label as a flag of legitimacy rather than a description of practice.

## EA-as-IT vs EA-as-business

TOGAF's lineage is IT (TAFIM was a DoD IT-infrastructure framework; TOGAF 1-7 were IT-architecture-focused). Despite the TOGAF 8 broadening to "enterprise architecture", TOGAF in practice is often IT-centric — owned by IT, focused on the application and technology landscape, with business architecture as a thin upstream phase. Critics (Tom Graves is the most prominent) argue that real enterprise architecture is about the whole enterprise, not just IT, and that TOGAF's IT roots limit it. The 9.2 business-architecture improvements and the 10th Edition's business-focused Series Guides are responses; the IT-centricity is sticky.

## AI-system architecture gaps

The 10th Edition's Series Guides (digital-EA, agile-EA) touch adjacent ground, but the deep questions of architecting AI capabilities into the enterprise are not addressed:

- **Gap analysis for partly-emergent capabilities.** Classic gap analysis assumes a designed target. AI capabilities partly emerge — you discover what the model can do as you use it. TOGAF has no native treatment of "the target is a direction with explicit uncertainty."
- **Governing autonomous components.** The ADM and the governance model assume designed, deterministic systems. Autonomous agents that make decisions are a different shape. How does an Architecture Compliance review assess an agent's behavior?
- **Vendor-as-implicit-data-processor.** Model providers are a new kind of supplier dependency. TOGAF's treatment of supplier / partner relationships is generic; AI-vendor relationships have specific data-handling, model-version-drift, and contractual characteristics that need explicit treatment.
- **AI reference architectures.** The Enterprise Continuum concept maps onto how AI reference architectures should be organized (Foundation → Common → Industry → Organization-Specific), but TOGAF provides no AI reference content.

ISO/IEC 42001 (AI management system) is the partial answer for AI governance; the integration story with TOGAF is undeveloped. A TOGAF Series Guide on AI-system architecture is a plausible future addition — the Series Guide structure is built for exactly this kind of fast-moving topic.

## The Open Group governance question

The Open Group is a vendor-neutral consortium with broad membership (IT vendors, enterprises, government, consultancies, academia). Framework-capture risk is lower than for a single-owner framework — but it is not zero, and a consortium's incentives (membership fees, certification revenue, member-vendor interests) are not perfectly aligned with "produce the best possible framework." The certification revenue stream in particular creates an incentive to keep the framework complex enough to require training.

## Counterpoint: what TOGAF still does well

The critique is not that TOGAF should be abandoned — there is no better-developed EA framework. The structural benefits are real:

- **Common vocabulary.** Baseline architecture, target architecture, gap analysis, transition architecture, building block, architecture principle — these have shared meanings in most enterprise EA contexts.
- **The ADM as a checklist.** Even practitioners who do not run the full cycle use the phases to avoid skipping analysis: stakeholder concerns, business before technology, gap analysis, roadmap, governance during delivery.
- **The ABB / SBB split.** Separating "what capability is required" from "which product implements it" is a genuinely useful discipline.
- **The governance model.** Architecture Boards, Compliance reviews, and Architecture Contracts give the EA function teeth — when the organization backs them.
- **The Series Guide restructure.** Decoupling the stable core from fast-moving topic guidance is the right move; it directly addresses the "frozen for years" critique.
- **Vendor neutrality.** TOGAF does not push a particular vendor's stack.
- **Complementarity.** TOGAF + Zachman + ArchiMate + ITIL + COBIT compose cleanly; each addresses a different facet.

The critique is calibrative: TOGAF is the most complete EA framework, with well-documented failure modes that are mostly about how organizations implement it (heavyweight, waterfall, shelfware, control-model) rather than about the framework's content. Tailor aggressively, position the EA function as enablement not control, keep documentation lean, and treat the ADM as a thinking checklist rather than a mandatory process — and the framework's value shows. Implement it by the book in a control-model EA function and the failure modes show.

## See also

- [[TOGAF Cluster|cluster MOC]] · [[TOGAF ADM]] · [[TOGAF vs Other EA Frameworks]] · [[TOGAF Certification Scheme]]
- [position](pillars/togaf/position.md) (cluster-level position derived from these contested points)
- [[ITIL Controversies]] (parallel critique of ITIL — many shared themes: process-heaviness, cert-mill, agile tension)
