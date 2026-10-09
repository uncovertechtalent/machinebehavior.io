title: ITIL 4 Service Value Chain
summary: The Service Value Chain (SVC) is the operating model at the heart of the Service Value System.
parent: itil
order: 100
labels: itil, itil-concept
aliases: ITIL 4 SVC | ITIL Service Value Chain | ITIL SVC | ITIL Value Chain
type: itil-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/itil/ITIL 4 Service Value Chain.md
reviewed: no
---
> The Service Value Chain (SVC) is the operating model at the heart of the Service Value System. Six interconnected activities that transform demand into value. Each activity converts inputs into outputs; the activities are linked but not in a fixed sequence.

## The six activities

### 1. Plan

Strategic, tactical, and operational planning. Ensures shared understanding of vision, status, and improvement direction across the four dimensions and across all products and services.

Inputs: governance direction, demand signal, improvement initiatives, market research, audit findings, performance data, supplier information.

Outputs: strategic, tactical, and operational plans; portfolio decisions; improvement plans; architectural decisions.

Practices most associated: Strategy Management, Portfolio Management, Architecture Management, Service Financial Management, Workforce and Talent Management, Risk Management, Information Security Management.

### 2. Improve

Continual improvement of products, services, and practices across the value chain. The activity where the continual-improvement component of the SVS manifests in operational form.

Inputs: performance information, lessons learned from incidents and problems, audit findings, stakeholder feedback, opportunity scans.

Outputs: improvement initiatives, prioritized backlog, status reports on improvements, value-realization information.

Practices: Continual Improvement (a practice in its own right), Measurement and Reporting. Touches all other practices indirectly.

### 3. Engage

Interaction with stakeholders to understand needs, communicate, and ensure transparency. Includes both internal stakeholders (users, business owners) and external stakeholders (consumers, partners, suppliers, regulators).

Inputs: stakeholder requests, complaints, feedback, market intelligence, opportunity signals, partner / supplier inputs.

Outputs: agreed requirements, agreed service-level targets, performance reports, change requests, partnership agreements, communications.

Practices: Relationship Management, Supplier Management, Service Desk, Service Level Management, Service Request Management, Business Analysis, parts of Service Catalogue Management.

### 4. Design & Transition

Build services that meet stakeholder needs in terms of quality, costs, and time-to-market. Transition them into operations.

Inputs: requirements from Engage, plans from Plan, improvement initiatives, contracts, knowledge from other activities.

Outputs: new and changed services, service requirements, performance information, change-evaluation reports.

Practices: Service Design, Service Validation and Testing, Release Management, Change Enablement, Project Management, Service Configuration Management.

### 5. Obtain / Build

Ensure that service components are available when and where they are needed, and meet agreed specifications. Includes building software, integrating systems, procuring hardware, sourcing services from suppliers.

Inputs: architectural decisions, design specifications, supplier inputs, infrastructure requirements.

Outputs: service components, contractual agreements, supplier-delivered services, infrastructure changes.

Practices: Software Development and Management, Deployment Management, Infrastructure and Platform Management, Supplier Management, IT Asset Management, Service Configuration Management.

### 6. Deliver & Support

Ensure that services are delivered and supported in line with agreed specifications and stakeholder expectations.

Inputs: service components from Obtain/Build, agreed levels from Engage, infrastructure, user requests, events, incidents.

Outputs: delivered services, resolved incidents, fulfilled requests, monitoring data, problem records.

Practices: Service Desk, Incident Management, Problem Management, Service Request Management, Monitoring and Event Management, Availability Management, Capacity and Performance Management, Service Continuity Management, IT Asset Management, Information Security Management.

## How activities connect

The activities are not a sequence. Different value streams use different sequences. The SVC is a connectivity model:

- A new service might flow: Engage (capture demand) → Plan (strategic fit) → Design & Transition (design) → Obtain/Build (build) → Deliver & Support (run) → Improve (refine).
- An incident might flow: Deliver & Support (detect, respond) → Engage (notify stakeholders) → Improve (post-incident learning).
- A vendor relationship might flow: Plan (strategic sourcing) → Engage (negotiate) → Obtain/Build (integrate) → Deliver & Support (ongoing relationship management) → Improve (performance review).

Activities can iterate, skip, parallelize. The same activity can be invoked multiple times in one value stream.

## Inputs and outputs (broader view)

The SVC has external interfaces:

- **External inputs:** opportunity signals from the market, demand signals from consumers, governance direction, regulatory and contractual requirements, supplier information, financial constraints.
- **External outputs:** value to consumers (in the form of services delivered, requests fulfilled, incidents resolved), value to the organization (revenue, market position, capability development), value to other stakeholders (regulators, partners, society).

The SVC is value-creating; the inputs are not just inside-organization signals but include opportunity-side and demand-side market reality.

## Implementation patterns

Organizations adopt the SVC in different ways:

- **As vocabulary only.** Use the six activity names in operating-model conversations without restructuring.
- **As lens for value-stream mapping.** Model existing work as flows through the activities. Identify gaps and inefficiencies.
- **As organizational structure.** Some organizations align teams or capabilities to the activities (a Plan team, an Improve team). Generally discouraged by ITIL guidance because it creates silos along activity lines that should be cross-cutting.
- **As input to operating-model design.** Use the SVC + four dimensions + guiding principles as inputs to designing a target operating model.

## Common implementation gaps

- **Confusing SVC with v3 lifecycle.** Practitioners trained in v3 sometimes map SVC activities to v3 lifecycle stages incorrectly (Design & Transition ≠ Service Transition; Plan ≠ Service Strategy). The conceptual reset is real.
- **Treating activities as departments.** Building a "Plan team" or "Engage team" creates silos. Activities should be cross-cutting capabilities, not organizational units.
- **Skipping Improve.** Improve is often the least-resourced activity because it competes with operational priorities. Continual improvement degrades when it has no protected capacity.
- **Engage limited to customer-facing.** Engage covers all stakeholder interaction, including with internal customers, partners, suppliers, and regulators. Limiting it to consumer-facing work misses much of its scope.

## SRE and AI-agent fit notes

### SVC × SRE practice

- **Plan** maps to SRE capacity planning, error budget setting, reliability target planning.
- **Improve** maps to SRE postmortem follow-ups, toil reduction projects, reliability investments.
- **Engage** maps to SRE communication with developer teams, business stakeholders, customer-success teams; covers SLO negotiation.
- **Design & Transition** maps to SRE pre-production review, production-readiness review, launch coordination.
- **Obtain/Build** maps to platform engineering, infrastructure provisioning, tooling acquisition.
- **Deliver & Support** maps to incident response, on-call rotation, day-to-day operations.

The mappings are imperfect but usable as bridge vocabulary in mixed-discipline teams.

### SVC × AI-system operations

AI-system operations workflows use the SVC differently than classical IT services:

- **Plan** must include model-version planning, AI risk planning, capacity for both compute and model API quotas.
- **Engage** includes stakeholder education on AI capability limits and failure modes — a substantially larger engagement load than classical IT.
- **Design & Transition** includes prompt engineering, tool-scope design, output validation, evaluation harness creation.
- **Obtain/Build** includes vendor selection (model providers), training infrastructure (where applicable), evaluation infrastructure.
- **Deliver & Support** includes agent action audit logging, behavioral monitoring, vendor-side anomaly response.
- **Improve** includes systematic prompt-injection testing, vendor-relationship review, model-behavior-drift management.

The SVC scaffolds these but does not prescribe the AI-specific content; practitioner work fills in.

### Value-stream mapping for AI features

A practical pattern: pick a specific AI feature (e.g., "agent that drafts incident summaries"). Map its value stream through the SVC. Identify which practices are involved at each activity. Identify gaps (e.g., Monitoring and Event Management practice as applied to the agent vs as applied to traditional infrastructure). Build remediation plan.

## Stefan-context implementation sketch

- Vault as service: value streams for vault content development (Plan → Engage → Design & Transition → Obtain/Build → Deliver & Support → Improve), with bd issues capturing improvement initiatives.
- Agent system as service: value streams for new agent deployment (Plan capacity / scope → Engage stakeholders → Design system prompt and tool scope → Build integration → Deliver supported usage → Improve via observation and incident learning).
- Client engagement delivery: value-stream-mapped per engagement type if helpful; lighter scaffolding otherwise.

## See also

- [[ITIL Cluster|cluster MOC]] · [[ITIL 4 Service Value System]] · [[ITIL 4 Four Dimensions]] · [[ITIL 4 Practices]]
