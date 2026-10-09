title: ITIL 4 Practices
summary: Thirty-four organizational capabilities used in the Service Value Chain.
parent: itil
order: 100
labels: itil, itil-concept
aliases: ITIL 4 Practices | ITIL 34 Practices | ITIL Practices | ITIL 4 General Management Practices | ITIL 4 Service Management Practices | ITIL 4 Technical Management Practices
type: itil-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/itil/ITIL 4 Practices.md
reviewed: no
---
> Thirty-four organizational capabilities used in the Service Value Chain. ITIL 4 replaced v3's "processes + functions" model with "practices" — each practice includes process content, but also the people, tools, suppliers, and data needed to perform the capability. Three categories: General Management (14), Service Management (17), Technical Management (3).

## How practices differ from v3 processes

v3 distinguished processes (sequences of activities) from functions (organizational groups). ITIL 4 collapsed both into practices.

A practice in ITIL 4 has:

- One or more processes
- Roles and responsibilities
- Information needs
- Technology / tooling needs
- Supplier dependencies (if applicable)
- Value-stream integration patterns

A v3 process map to an ITIL 4 practice often involved renaming, occasional merging, and adding the broader "capability" framing.

## General management practices (14)

Adopted from broader business management. Not IT-specific but applied within service management.

### Strategy Management

Formulate goals, define means to achieve them, allocate resources, set direction. Strategic management for the IT organization or service-provider entity.

### Portfolio Management

Strategic decisions about portfolios of products, services, programmes, projects, and other investments. Aligns investment with strategy. Includes service portfolio, project portfolio, application portfolio, customer portfolio.

### Architecture Management

Provides understanding of all the different elements that make up an organization. Establishes blueprint for service development, supports decision-making across the four dimensions.

### Service Financial Management

Supports the org's strategies and plans for service management by ensuring financial resources and investments are used effectively. Budgeting, accounting, charging, financial planning.

### Workforce and Talent Management

Ensures the right people are available, with the right skills, in the right roles. Recruitment, learning, development, succession planning.

### Continual Improvement

The practice. Mirrors the SVS continual-improvement component. Establishes a continual-improvement register, prioritizes improvement initiatives, embeds improvement thinking across the org.

### Measurement and Reporting

Supports good decision-making and continual improvement by quantifying and evaluating service performance, organizational performance, market position, customer perception.

### Risk Management

Ensures the org understands and effectively manages risks. Risk identification, assessment, treatment, monitoring. Maps to ISO 27005 / 31000 family.

### Information Security Management

Protects information, including confidentiality, integrity, and availability. Closely aligned with ISO 27001 territory. ITIL practice covers the management aspects; deep technical controls live elsewhere.

### Knowledge Management

Maintains and improves the effective, efficient, and convenient use of information and knowledge across the organization. Explicit + tacit knowledge handling.

### Organizational Change Management

Ensures changes in an organization are smoothly and successfully implemented. People-side of change (distinct from Change Enablement, which is the technical-change practice).

### Project Management

Ensures all projects in the organization are successfully delivered. Includes traditional waterfall, Agile, and hybrid project approaches.

### Relationship Management

Establishes and nurtures relationships between the org and its stakeholders at strategic and tactical levels. Customer relationship, partner relationship, internal-stakeholder relationship.

### Supplier Management

Ensures the org's suppliers and their performance are managed appropriately to support consistent service quality. Vendor management, contract management, performance review.

## Service management practices (17)

Core IT-service-management capabilities.

### Availability Management

Ensures services deliver agreed levels of availability. Availability targets, measurement, improvement.

### Business Analysis

Analyses a business or some element of it, defines its associated needs, and recommends solutions.

### Capacity and Performance Management

Ensures services achieve agreed performance levels and have adequate capacity. Capacity planning, performance monitoring, demand management.

### Change Enablement

Maximizes the number of successful service and product changes. Risk-based change classification (standard, normal, emergency), change approval, change records.

Replaces v3's Change Management. Renamed to emphasize enabling change rather than gatekeeping. ITIL 4 explicitly criticizes traditional CAB-heavy implementations.

### Incident Management

Minimizes the negative impact of incidents by restoring normal service operation as quickly as possible. Incident detection, classification, response, resolution, closure.

The most widely-implemented practice. Often the entry point for ITIL adoption.

### IT Asset Management

Plans and manages the full lifecycle of all IT assets. Hardware, software licenses, cloud subscriptions, contracts.

### Monitoring and Event Management

Systematically observes services and components, records and reports selected changes of state. Events, alerts, monitoring infrastructure, alert correlation, AIOps integration.

### Problem Management

Reduces the likelihood and impact of incidents by identifying actual and potential causes. Problem identification, problem control (analysis, workarounds), error control (resolution of known errors).

### Release Management

Makes new and changed services available for use. Coordinates with Change Enablement (changes get approved; releases get deployed).

### Service Catalogue Management

Provides a single source of consistent information on services and service offerings, ensuring it is available to the relevant audience. Service catalog, request catalog.

### Service Configuration Management

Ensures accurate and reliable information about service configuration is available when and where it is needed. Configuration items, configuration management database (CMDB), configuration management system (CMS).

### Service Continuity Management

Ensures availability and performance of a service is maintained at sufficient level in case of a disaster. Disaster recovery, business continuity, crisis management. Maps to ISO 22301 territory.

### Service Design

Designs products and services that are fit for purpose, fit for use, can be delivered by the org and its ecosystem.

### Service Desk

Captures demand for incident resolution and service requests. Single point of contact for users.

### Service Level Management

Sets clear business-based targets for service performance and ensures delivery is properly assessed, monitored, and managed. SLAs, SLOs (per ITIL 4 — borrowing SRE terminology), service-level monitoring and reporting.

### Service Request Management

Supports the agreed quality of a service by handling all pre-defined, user-initiated service requests in an effective and user-friendly manner.

### Service Validation and Testing

Ensures new or changed products and services meet defined requirements. Testing across functional, performance, security, usability dimensions.

## Technical management practices (3)

Technology-specific capabilities.

### Deployment Management

Moves new or changed hardware, software, documentation, processes, or any other component to live environments. May include deployment to pre-production environments.

### Infrastructure and Platform Management

Oversees the infrastructure and platforms used by the org. Servers, networks, cloud platforms, container platforms.

### Software Development and Management

Ensures the org's applications meet stakeholder needs in terms of functionality, reliability, maintainability, compliance, and auditability.

## Practice maturity considerations

Each practice has a maturity dimension. Common maturity scales:

- **Initial / Performed / Established / Predictable / Optimizing** — borrowing from CMMI / SPICE.
- **Practice capability levels** — ITIL 4 publishes capability-level criteria per practice in the Practice Guides.

Organizations typically target different maturity levels per practice based on strategic importance. Not every practice needs to be at the highest level.

## Practice-to-value-chain mapping

Practices are used across SVC activities, not aligned to single activities. Examples:

- **Incident Management** primarily used in Deliver & Support; contributes to Improve (post-incident reviews) and Engage (stakeholder communication).
- **Service Level Management** used in Plan (target setting), Engage (negotiation, reporting), Deliver & Support (monitoring), Improve (target adjustment).
- **Change Enablement** used in Design & Transition (planning), Obtain/Build (component changes), Deliver & Support (operational changes).
- **Supplier Management** used in Plan (sourcing strategy), Engage (relationship management), Obtain/Build (procurement, integration), Deliver & Support (performance management).

## Common practice-adoption patterns

- **Starter set**: Incident Management, Change Enablement, Service Request Management, Service Desk, Knowledge Management. Common entry point for IT-service-management adoption.
- **Maturity expansion**: Problem Management, Service Level Management, Monitoring and Event Management. Second wave once incident response stabilizes.
- **Strategic expansion**: Portfolio Management, Architecture Management, Service Financial Management. For organizations growing service-management maturity beyond operations.
- **Specialist depth**: practice-specific deep capability (e.g., advanced Capacity and Performance Management for high-scale operations).

## SRE and AI-agent fit notes

### Practices closely-related to SRE

- **Incident Management** — SRE incident response, on-call rotation, war rooms.
- **Problem Management** — SRE postmortems, root cause analysis, action items.
- **Service Level Management** — SRE SLO definition, error budget management.
- **Monitoring and Event Management** — SRE observability stack.
- **Availability Management** — SRE reliability target setting and tracking.
- **Capacity and Performance Management** — SRE capacity planning.
- **Change Enablement** — SRE production-readiness, gradual rollout, canary deployment.
- **Continual Improvement** — SRE error-budget-driven investment in reliability.

The mappings are real; vocabulary differs.

### Practices for AI-system operations

Practices that need substantial AI-specific tailoring:

- **Service Level Management** — SLO definition for non-deterministic systems. Latency distribution, output quality metrics, vendor-side dependency.
- **Monitoring and Event Management** — agent action logging, anomalous behavior detection, vendor-side anomaly correlation.
- **Incident Management** — incident classification when AI is involved; coordinating with model-vendor support; communicating non-deterministic failures to users.
- **Problem Management** — root-cause analysis when the failure is model behavior; coordinating with vendor on model-side issues; tracking known model behaviors as known errors.
- **Change Enablement** — change-impact analysis for system prompt changes, tool scope changes, model version changes.
- **Service Configuration Management** — system prompts, tool scopes, model versions, retrieval corpora as configuration items.
- **Information Security Management** — AI-specific security concerns (prompt injection, tool misuse, output leakage).
- **Supplier Management** — model-provider relationships, DPA management, vendor-side performance.
- **Service Continuity Management** — vendor outage scenarios, fallback model strategies.
- **Knowledge Management** — system prompts and prompt-engineering knowledge as institutional knowledge.

## Stefan-context implementation sketch

- For solo / small-team operations: Incident Management (lightweight, bd-tracked), Knowledge Management (vault as knowledge base), Supplier Management (vendor relationship tracking).
- For client work: practice vocabulary as bridge language; specific practice depth per client maturity.
- For AI-system operations: tailor Monitoring and Event Management, Incident Management, Change Enablement, Service Configuration Management to agent-system characteristics. Documented as additions to standard practice rather than parallel processes.

## See also

- [[ITIL Cluster|cluster MOC]] · [[ITIL 4 Service Value System]] · [[ITIL 4 Service Value Chain]] · [[ITIL 4 Four Dimensions]]
- [[ISO 27001 Cluster|ISO 27001]] (Information Security Management practice maps directly)
