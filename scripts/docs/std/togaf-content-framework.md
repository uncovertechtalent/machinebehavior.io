title: TOGAF Content Framework
summary: The Architecture Content Framework defines the work products of architecture activity: deliverables, artifacts, and building blocks.
parent: togaf
order: 100
labels: togaf, togaf-component
aliases: TOGAF Content Framework | TOGAF Architecture Content | TOGAF Building Blocks | ABB SBB | TOGAF Deliverables Artifacts
type: togaf-component
created: 2026-05-12
updated: 2026-06-08
origin: pillars/togaf/TOGAF Content Framework.md
reviewed: no
---
> The Architecture Content Framework defines the work products of architecture activity: deliverables, artifacts, and building blocks. It gives a structured model so architecture outputs are consistent and reusable. The content metamodel defines the entities and relationships these work products describe.

## Three categories of work product

### Deliverables

Formal, contractual outputs of the architecture work — the things that get reviewed, signed off, and form part of project / engagement contracts. Examples (mapped to ADM phases that produce them):

- **Request for Architecture Work** (Preliminary / triggers a cycle)
- **Statement of Architecture Work** (Phase A)
- **Architecture Vision** (Phase A)
- **Architecture Principles** (Preliminary / Phase A)
- **Architecture Definition Document** (built across B-D, finalized in F) — the central deliverable; describes baseline and target architectures across business, data, application, technology.
- **Architecture Requirements Specification** (built across phases)
- **Architecture Roadmap** (Phase E-F)
- **Implementation and Migration Plan** (Phase F)
- **Transition Architecture(s)** (Phase E)
- **Architecture Contract** (Phase G) — agreement between the architecture function and delivery teams.
- **Compliance Assessment** (Phase G)
- **Architecture Building Blocks** and **Solution Building Blocks** (used across phases)
- **Change Request** (Phase H)
- **Organizational Model for Enterprise Architecture** (Preliminary)
- **Tailored Architecture Framework** (Preliminary)

Deliverables are typically composed of artifacts.

### Artifacts

Granular architectural work products that describe an aspect of the architecture from a particular viewpoint. Three artifact types:

- **Catalogs** — lists of things of a particular type (e.g., Application Portfolio Catalog, Technology Standards Catalog, Business Service / Function Catalog, Data Entity / Data Component Catalog, Principles Catalog). The "what exists" inventory.
- **Matrices** — show relationships between things of two types (e.g., Business Interaction Matrix, Application / Data Matrix, Application / Function Matrix, Actor / Role Matrix, System / Technology Matrix). The "how things relate" view.
- **Diagrams** — pictorial representations from a viewpoint (e.g., Business Footprint Diagram, Application Communication Diagram, Data Lifecycle Diagram, Environments and Locations Diagram, Platform Decomposition Diagram). The "show me" view.

TOGAF provides a recommended set of artifacts per ADM phase. Practitioners select the subset relevant to their engagement; lean engagements produce few artifacts.

ArchiMate is the recommended notation for many of these artifacts (ArchiMate and TOGAF share an owner — The Open Group — and the ArchiMate metamodel maps onto the TOGAF content metamodel).

### Building Blocks

Reusable components of capability. The key distinction:

- **Architecture Building Block (ABB)** — defines *what* functionality / capability is required, without specifying *how* it is implemented. Specification-level. Example: "an identity-and-access-management capability supporting SSO, MFA, and lifecycle provisioning." ABBs are stable; they describe requirements.
- **Solution Building Block (SBB)** — implements one or more ABBs. Product / component-level. Example: "Okta" or "Microsoft Entra ID" or "Keycloak deployed on Kubernetes." SBBs change as technology and procurement decisions change.

The ABB / SBB split keeps architecture decisions (what capability is needed) separate from procurement / engineering decisions (which product). When a vendor is swapped, the ABB stays; the SBB changes. This is one of TOGAF's cleaner contributions.

Building blocks have characteristics: they are reusable, they have defined boundaries and interfaces, they may be assembled from other building blocks, they should be loosely coupled.

## The content metamodel

A model of the entities that architecture work products describe and their relationships. Core entity groups:

- **Architecture Principles, Vision, and Requirements** — principles, constraints, assumptions, requirements, gaps.
- **Business Architecture** — organization unit, actor, role, business function, business service, business process, business capability, value stream, product, contract, measure, driver, goal, objective.
- **Information Systems Architecture** — data entity, logical data component, physical data component, application component (logical and physical), information system service.
- **Technology Architecture** — platform service, logical technology component, physical technology component.
- **Architecture Realization** — work package, capability increment, deliverable, transition architecture, architecture contract, standard, guideline, specification.

Relationships connect these (e.g., "actor performs role", "role accesses application", "application realizes business service", "application component is deployed on technology component", "data entity is created by business process").

TOGAF defines a "core" metamodel plus optional extensions (governance extension, services extension, process modeling extension, data extension, infrastructure consolidation extension, motivation extension). Organizations adopt the extensions relevant to their needs.

## How deliverables, artifacts, and building blocks fit together

- **Building blocks** are the reusable parts of the architecture (ABBs = required capabilities; SBBs = implementing components).
- **Artifacts** describe the architecture (catalogs of building blocks, matrices of their relationships, diagrams of their arrangement).
- **Deliverables** package artifacts into formal, reviewable outputs (the Architecture Definition Document contains many artifacts).

The Architecture Repository (see [[TOGAF Enterprise Continuum]]) stores all of these so they are reusable across engagements.

## Tailoring the content framework

The full content framework is large. Tailoring:

- **Deliverable selection** — produce only the deliverables the engagement / governance requires. A focused capability-architecture engagement might produce a Statement of Architecture Work, a slim Architecture Definition Document, a Roadmap, and a few artifacts.
- **Artifact selection** — pick the catalogs / matrices / diagrams that answer the stakeholders' actual questions. Producing the full recommended artifact set per phase is rarely warranted.
- **Metamodel extension selection** — adopt only relevant extensions.
- **Notation choice** — ArchiMate, UML, BPMN, or informal sketches depending on context and audience.

The common failure: producing the full deliverable and artifact set "because TOGAF says so", generating documentation that ages quickly and is read by few. The framework permits — and the 10th Edition Series Guides encourage — leaner adoption.

## SRE and AI-system fit notes

- **ABB / SBB for AI capabilities.** ABB: "an LLM-based text-generation capability supporting RAG over enterprise documents, with PII redaction, audit logging, and human-in-the-loop on high-stakes outputs." SBB: "Claude API (enterprise tier, zero-retention DPA) + a Postgres+pgvector store + a redaction service + an audit-log pipeline." Swapping model providers changes the SBB; the ABB persists. This keeps the architecture decision (what AI capability is needed) separate from the vendor decision.
- **Artifacts for AI-system architecture.** Useful additions: a Model Inventory Catalog (which models, which versions, which vendors, which tiers), an AI Capability / Data Matrix (which AI capabilities touch which data entities), an Agent Tool-Scope Catalog (which agents, which tools, which scopes), a Vendor Dependency Diagram (AI capabilities → model providers → contractual commitments).
- **Metamodel extension for AI.** Consider an organization-specific metamodel extension capturing AI-system entities: model, model version, prompt template, tool definition, agent, vendor relationship, and their relationships to the standard entities (application component, data entity, business service).
- **Don't over-document AI architecture.** AI-system designs change fast (vendor model updates, prompt iterations, tool-scope adjustments). Heavy content-framework deliverables age out quickly. Keep AI-architecture artefacts lean and treat them as living documents.

## See also

- [[TOGAF Cluster|cluster MOC]] · [[TOGAF ADM]] · [[TOGAF Enterprise Continuum]] · [[TOGAF Architecture Capability]]
