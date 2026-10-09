title: TOGAF Architecture Capability
summary: The Architecture Capability Framework covers how to establish and operate an enterprise-architecture practice: the governing body (Architecture Board), the governance mechanisms (compliance reviews, contracts), the maturity models, and the skills framework.
parent: togaf
order: 100
labels: togaf, togaf-component
aliases: TOGAF Architecture Capability | TOGAF Architecture Governance | Architecture Board | TOGAF Architecture Compliance | Architecture Contract
type: togaf-component
created: 2026-05-12
updated: 2026-06-08
origin: pillars/togaf/TOGAF Architecture Capability.md
reviewed: no
---
> The Architecture Capability Framework covers how to establish and operate an enterprise-architecture practice: the governing body (Architecture Board), the governance mechanisms (compliance reviews, contracts), the maturity models, and the skills framework. This is the "how do you run an EA function" content, distinct from the ADM ("how do you do an architecture project").

## Establishing an architecture capability

TOGAF treats setting up an EA function as itself an ADM cycle (run in the Preliminary Phase). Decisions:

- **Scope** — what part of the enterprise does the EA function cover? Whole organization, a division, a domain?
- **Organizational model** — where does EA sit? Reporting to the CIO, the CTO, a Chief Architect, a transformation office? Centralized, federated, or hub-and-spoke?
- **Governance bodies** — establish the Architecture Board and define its remit.
- **Processes** — define the architecture-governance processes (compliance reviews, dispensations, contracts).
- **Roles and skills** — staff the function (see Skills Framework below).
- **Tools and repository** — select an EA tool; establish the Architecture Repository.
- **Principles** — define the architecture principles that constrain all architecture work.

## The Architecture Board

A cross-organizational body responsible for overseeing the implementation of the architecture governance strategy. Typical responsibilities:

- Provide architecture-governance oversight.
- Review and approve key architecture deliverables (Architecture Vision, Architecture Definition Documents, major roadmaps).
- Resolve architecture conflicts and ambiguities.
- Approve / reject dispensation requests (waivers from architecture standards).
- Ensure consistency between architecture work and the organization's strategy.
- Provide direction and authority for architecture decisions.
- Identify and mitigate architecture risks.

Composition: senior architects, often with representation from key business and IT stakeholders. Size: typically 4-8 members; too large becomes ineffective.

The Architecture Board is the EA function's "teeth." Without an effective board with real authority, architecture decisions get overridden and the EA function produces shelfware.

## Architecture Governance

The practice of managing and controlling enterprise architectures at an organization-wide level. Key mechanisms:

### Architecture Compliance reviews

A formal review of a project / solution's architecture against the enterprise architecture and standards. Conducted (per the ADM) in Phase G (Implementation Governance) but can happen at any point in a delivery lifecycle. Outcomes:

- **Compliant** — the solution conforms to the architecture and standards.
- **Compliant with observations** — minor deviations noted; no action blocking.
- **Non-compliant** — deviations that must be resolved (either the solution changes, or a dispensation is granted).

A compliance review checks: alignment with architecture principles, conformance to technology standards (the Standards Information Base), reuse of approved building blocks, fit with the target architecture, data-handling and security conformance.

### Architecture Contracts

Joint agreements between the architecture function (development partners) and sponsors / delivery teams on the deliverables, quality, and fitness-for-purpose of an architecture. Two main types:

- **Contract between architecture design / development partners** — agreement on what the architecture work will deliver.
- **Contract between architecture function and delivery teams** — agreement (issued in Phase G) on what the delivery will produce, to what architectural standard, with what compliance checkpoints.

The contract makes the architecture binding rather than advisory. "The delivery team agreed in the Architecture Contract to use the approved IAM building block; they didn't; that's a contract breach" is a stronger position than "the architects suggested IAM."

### Dispensations / waivers

When a project genuinely cannot or should not conform to a standard, it requests a dispensation. The Architecture Board reviews: is the deviation justified? For how long? What's the remediation plan? Approved dispensations go in the Governance Log with an expiry date. This is the controlled-exception mechanism — without it, either everything must conform (unworkable) or nothing is enforced (shelfware).

## Architecture Maturity Models

Tools to assess the maturity of the architecture capability itself. TOGAF references several, notably:

- **ACMM (Architecture Capability Maturity Model)** — originally from the US Department of Commerce. Levels 0-5 (None / Initial / Under Development / Defined / Managed / Measured) across elements like architecture process, architecture development, business linkage, senior management involvement, operating unit participation, architecture communication, IT security, architecture governance, IT investment and acquisition strategy.
- Organizations also use CMMI-derived models, the Gartner EA maturity assessment, or custom models.

Maturity assessment is a periodic activity (referenced in the Governance Log). It surfaces gaps in the EA function's own capability — weak governance, poor business linkage, thin senior-management support — and feeds an improvement plan.

## Architecture Skills Framework

Defines the roles in an architecture practice and the skills each requires. TOGAF identifies roles such as:

- **Enterprise Architect** — the broadest role; oversees the whole architecture across business, data, application, technology; connects architecture to strategy.
- **Business Architect** — focuses on business architecture: capabilities, value streams, processes, organizational structure.
- **Data / Information Architect** — focuses on data architecture: data entities, data governance, data lifecycle, master data.
- **Application Architect** — focuses on application architecture: application portfolio, application services, integration.
- **Technology / Infrastructure Architect** — focuses on technology architecture: platforms, infrastructure, networks, technology standards.
- **Solution Architect** — focuses on a specific solution within the enterprise architecture (sometimes considered distinct from EA roles).

The framework lists skill categories (generic skills, business skills, enterprise-architecture skills, programme-management skills, IT general knowledge, technical IT skills, legal-environment knowledge) and indicative proficiency levels per role. It is a competence-mapping tool, not a rigid prescription.

## SRE and AI-system fit notes

- **Architecture Board as the AI-governance body.** When an organization operates AI systems at scale, the Architecture Board (or a sub-board) is a natural place for AI-system architecture governance: reviewing AI-system designs against principles, approving / rejecting AI-tool dispensations, resolving conflicts (which team owns the shared RAG infrastructure?).
- **Architecture Compliance reviews for AI systems.** Add an AI-system review category: does the design have human accountability for autonomous-agent actions? Is there a kill-switch / reversibility for irreversible actions? Is the model provider on the approved list with an appropriate DPA? Are PII-handling constraints respected? Is there audit logging of agent decisions? Is there monitoring for anomalous agent behavior?
- **Architecture Contracts for AI delivery.** When a delivery team builds an AI feature, the Architecture Contract should bind: which model provider / tier, which data classifications may be sent to it, which audit-logging standard, which monitoring requirements. "The team agreed in the contract to use the zero-retention enterprise tier; they used the default consumer tier; that's a breach" is enforceable.
- **AI dispensations in the Governance Log.** "Team X wants to use a non-approved model provider for capability Y because the approved provider lacks feature Z; approved for 6 months pending the approved provider adding the feature; remediation owner: ..." — this is the record of controlled AI exceptions.
- **EA function repositioning vs AI sprawl.** The "EA as enabling team, not controlling function" repositioning (Team Topologies framing) is the right move for most organizations — but AI adoption without *any* coordination produces duplicate RAG implementations, inconsistent vendor relationships, and no shared monitoring. The EA function's value here is enablement (shared patterns, shared infrastructure, shared vendor relationships) plus light-touch governance (the AI principles, the approved-provider list, the compliance review for high-stakes systems). Heavy control fails; zero coordination fails; enablement-plus-light-governance is the workable middle.
- **AI maturity assessment.** Adapt a maturity model for the AI-system capability: how mature is the organization's AI governance, AI security practice, AI vendor management, AI monitoring, AI incident response? Surfaces gaps; feeds an improvement plan.

## See also

- [[TOGAF Cluster|cluster MOC]] · [[TOGAF ADM]] · [[TOGAF Content Framework]] · [[TOGAF Enterprise Continuum]]
- [[ITIL 4 Service Value System]] (ITIL's governance component — TOGAF governs the architecture, ITIL governs the services)
- [[ISO 27001 Clause 9 Performance Evaluation]] (ISO 27001's internal audit and management review — adjacent governance mechanisms)
