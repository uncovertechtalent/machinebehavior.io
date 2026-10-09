title: TOGAF ADM
summary: The Architecture Development Method is the core of TOGAF, a step-by-step method for developing and managing the lifecycle of an enterprise architecture.
parent: togaf
order: 100
labels: togaf, togaf-component
aliases: TOGAF ADM | Architecture Development Method | TOGAF Architecture Development Method
type: togaf-component
created: 2026-05-12
updated: 2026-06-08
origin: pillars/togaf/TOGAF ADM.md
reviewed: no
---
> The Architecture Development Method is the core of TOGAF — a step-by-step method for developing and managing the lifecycle of an enterprise architecture. Nine phases in a cycle, with Requirements Management at the centre. The ADM is iterative (cycle, phase, and activity levels) and tailorable to context.

## The phases

### Preliminary Phase

Prepare and initiate the architecture capability.

- Define the enterprise scope for architecture work.
- Identify and establish the architecture governance bodies.
- Define and establish the architecture principles.
- Tailor the TOGAF framework and any other frameworks to the organization's context.
- Select and implement architecture tools.
- Establish the Architecture Repository.

Output: Organizational Model for Enterprise Architecture, tailored architecture framework, initial Architecture Repository, Request for Architecture Work (the trigger for the ADM cycle).

### Phase A: Architecture Vision

Set scope, constraints, and expectations for the cycle. Produce the high-level vision and secure approval to proceed.

- Confirm the Request for Architecture Work.
- Identify stakeholders, their concerns, and business requirements.
- Define the scope and constraints.
- Develop the Architecture Vision (a high-level, aspirational view of the target).
- Define the business value and the business case.
- Assess business transformation readiness.
- Develop the Statement of Architecture Work; secure sponsor approval.

Output: Approved Statement of Architecture Work, refined architecture principles, Architecture Vision, draft Architecture Definition Document, communications plan.

### Phase B: Business Architecture

Develop the target business architecture and analyze the gap from the baseline.

- Develop the baseline business architecture (current state).
- Develop the target business architecture (future state): organization structure, business functions, business processes, business capabilities, business services, value streams, products, governance.
- Perform gap analysis (baseline vs target).
- Define candidate roadmap components.
- Resolve impacts across the architecture landscape.
- Conduct formal stakeholder review.
- Finalize the business architecture; create the Architecture Definition Document (business sections).

Output: Refined Statement of Architecture Work, validated business principles / goals / drivers, baseline and target business architectures, gap analysis, business architecture components of the roadmap.

### Phase C: Information Systems Architectures

Develop the target data architecture and application architecture. Often done as two sub-phases; can be done in either order or in parallel.

**Data Architecture:**
- Baseline and target data architecture: data entities, data components, relationships, data lifecycle, data management, data governance.
- Gap analysis; roadmap components.

**Application Architecture:**
- Baseline and target application architecture: application components, application services, application interactions, application portfolio.
- Gap analysis; roadmap components.

Output: Baseline and target data and application architectures, gap analyses, information-systems components of the roadmap, updated Architecture Definition Document.

### Phase D: Technology Architecture

Develop the target technology architecture.

- Baseline and target technology architecture: platform services, technology components, hardware, networks, software infrastructure, technology standards.
- Gap analysis; roadmap components.
- Resolve impacts; stakeholder review.

Output: Baseline and target technology architectures, gap analysis, technology components of the roadmap, updated Architecture Definition Document.

### Phase E: Opportunities and Solutions

Consolidate the gap analyses from B-D; identify how to deliver the target.

- Consolidate gaps, dependencies, and roadmap components from phases B, C, D.
- Determine whether an incremental approach is needed (and define Transition Architectures if so).
- Identify major work packages and projects.
- Identify delivery vehicles (new projects, existing programmes, change requests).
- Conduct a high-level implementation and migration strategy.

Output: Architecture Roadmap, Transition Architectures (if needed), Implementation and Migration Plan (initial), work package definitions.

### Phase F: Migration Planning

Finalize the detailed Implementation and Migration Plan.

- Confirm interactions with the organization's project / portfolio management.
- Prioritize the migration projects (cost-benefit, risk).
- Confirm the Architecture Roadmap and Transition Architectures.
- Complete the Implementation and Migration Plan.
- Complete the architecture development cycle and document lessons learned.

Output: Finalized Architecture Definition Document, Architecture Roadmap, Implementation and Migration Plan, Implementation Governance Model, change requests for the architecture capability.

### Phase G: Implementation Governance

Provide architecture oversight during the delivery (project / programme execution).

- Confirm scope and priorities with development teams.
- Identify deployment resources and skills.
- Guide development of solutions deployment.
- Perform Architecture Compliance reviews.
- Implement business and IT operations.
- Issue Architecture Contracts (agreements between architecture function and delivery teams on what will be delivered and to what standard).

Output: Architecture Contracts, compliance assessments, deployed solutions aligned with the architecture, change requests.

### Phase H: Architecture Change Management

Manage changes to the architecture in a controlled way once it is established.

- Establish a change-management process for the architecture.
- Monitor technology and business changes.
- Assess change requests: do they fit within the current architecture (incremental change) or do they require a new ADM cycle (major change)?
- Manage governance and the architecture's ongoing fitness.

Output: Architecture updates, change to the architecture framework / principles, new Request for Architecture Work (if a new cycle is triggered).

### Requirements Management (central)

Not a phase but a continuous activity running through all phases. Manage architecture requirements: identify, store, prioritize, and feed them to the relevant ADM phases. The "Requirements Repository" holds requirements; phases pull from it and push new requirements into it.

The ADM diagram places Requirements Management at the centre with arrows to all phases, signalling that requirements flow continuously rather than being captured once.

## Iteration in the ADM

The ADM is explicitly iterative at three levels:

- **Cycle iteration** — running the full ADM repeatedly as the architecture evolves.
- **Phase iteration** — iterating between phases (e.g., B → C → B again as application-architecture findings change the business architecture).
- **Activity iteration** — iterating within a phase.

TOGAF defines iteration "patterns" — e.g., "Baseline First" vs "Target First", "Architecture Definition iterations" vs "Transition Planning iterations" — to structure how teams move through the phases. Practitioners choose the pattern that fits the engagement.

## Tailoring the ADM

The Preliminary Phase explicitly includes tailoring. Common tailoring:

- **Scope tailoring** — full enterprise vs a segment vs a single capability.
- **Depth tailoring** — strategic (high-level, broad) vs segment (focused) vs capability (detailed) architecture levels.
- **Deliverable tailoring** — which content-framework deliverables to produce; lean engagements produce fewer.
- **Integration with other frameworks** — Scrum / SAFe for delivery, ITIL for operations, COBIT for governance, PRINCE2 / PMI for project management.
- **Agile-EA tailoring** — minimum-viable-architecture approaches, just-in-time architecture, iterating in short cycles. The 10th Edition's agile-EA Series Guide covers this.

## ADM vs delivery methods

The ADM is an architecture method, not a delivery method. It produces architectures and roadmaps; delivery (building the actual systems) happens in projects / programmes / product teams using their own methods (Scrum, SAFe, Kanban, waterfall). Phase G (Implementation Governance) is the interface: the architecture function oversees delivery without doing delivery.

The common failure: treating the ADM as a delivery method, producing a multi-month big-design-up-front exercise before any building starts. The fix: tailor the ADM to produce just-enough architecture, iterate, and let delivery proceed in parallel under Phase G governance.

## SRE and AI-system fit notes

- **Introducing AI capabilities is an ADM cycle.** Request for Architecture Work ("we want to add AI-assisted X to the enterprise"). Phase A: vision, stakeholders (legal, security, the business unit, IT), business case. Phase B: which business capabilities does AI enable / change? Phase C: how do AI services fit the application landscape; what data do they consume; data governance implications. Phase D: model serving infrastructure, GPU / inference capacity, vector stores, vendor API dependencies. Phase E-F: roadmap, build-vs-buy, vendor selection, migration. Phase G: governance during delivery — does the AI-system design meet enterprise standards (security, data handling, reversibility)? Phase H: ongoing change management — vendor model updates, scope expansion.
- **Gap analysis for AI is awkward.** Classic gap analysis assumes a designed target state. AI capabilities partly emerge (you discover what the model can do as you use it). Tailor: treat the target as a direction with explicit uncertainty, iterate in short cycles, revisit the gap analysis frequently.
- **Architecture principles for AI.** The Preliminary Phase / Phase A should establish AI-specific principles: human accountability for autonomous-agent actions, reversibility for irreversible actions, vendor due diligence for model providers, data-handling constraints (no PII to non-DPA-covered model APIs), monitoring requirements.
- **Phase G Architecture Compliance reviews are the AI-governance point.** Use the compliance review to check AI-system designs against principles and standards before delivery proceeds.
- **The ADM-as-waterfall risk is acute for AI work.** AI-system work needs short iterations and frequent re-evaluation. A by-the-book multi-month ADM cycle before any building is the wrong shape. Tailor aggressively.

## See also

- [[TOGAF Cluster|cluster MOC]] · [[TOGAF Content Framework]] · [[TOGAF Enterprise Continuum]] · [[TOGAF Architecture Capability]]
- [[ITIL 4 Service Value Chain]] (the ITIL operating model — TOGAF designs the structure, ITIL runs services in it)
