title: TOGAF
summary: Map of TOGAF (The Open Group Architecture Framework), Standard 10th Edition (2022), as the dominant enterprise architecture framework.
parent: index
order: 250
labels: ea-frameworks, enterprise-architecture, moc, togaf
aliases: TOGAF Cluster | TOGAF | The Open Group Architecture Framework | TOGAF Standard
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/togaf/TOGAF Cluster.md
reviewed: no
---
> Map of TOGAF (The Open Group Architecture Framework), Standard 10th Edition (2022), as the dominant enterprise architecture framework. The Architecture Development Method (ADM), the Architecture Content Framework, the Enterprise Continuum, the Architecture Capability Framework, and the certification scheme. Reference cluster for enterprise-architecture decisions in SRE / platform / AI-system architecture work and for procurement contexts that mandate TOGAF alignment.

## Anchors

- [position](pillars/togaf/position.md): current view, dated, revisable
- [anchors](pillars/togaf/anchors.md): primary documents, The Open Group, training providers, named practitioners

## Provenance

- **TAFIM** (Technical Architecture Framework for Information Management) — US Department of Defense, early 1990s. The direct ancestor. DoD granted The Open Group permission to build a public framework from TAFIM.
- **TOGAF 1** (1995) — first public version, essentially TAFIM-derived, technology-architecture-focused.
- **TOGAF 7** (2001) — "Technical Edition." Still narrow.
- **TOGAF 8** (2002-2003) — "Enterprise Edition." Broadened from technology architecture to enterprise architecture (business, data, application, technology). The version where TOGAF became "EA framework" rather than "IT architecture framework."
- **TOGAF 9** (2009) — major restructure. Modular: ADM, ADM Guidelines and Techniques, Architecture Content Framework, Enterprise Continuum and Tools, TOGAF Reference Models, Architecture Capability Framework.
- **TOGAF 9.1** (2011) — maintenance update; corrections and clarifications.
- **TOGAF 9.2** (2018) — update; improved business architecture content, content metamodel simplification, alignment with the ArchiMate modeling language.
- **TOGAF Standard, 10th Edition** (2022) — current. Restructured into **TOGAF Fundamental Content** (the stable core: ADM, content framework, enterprise continuum, capability framework) plus **TOGAF Series Guides** (modular, updatable guidance on specific topics — agile, digital, business architecture, security architecture, etc.). The restructure aims to keep the core stable while letting topic guidance evolve faster.

Owner: **The Open Group** — a vendor-neutral technology consortium (members include major IT vendors, enterprises, government bodies, consultancies). The Open Group also owns the ArchiMate modeling language, the IT4IT reference architecture, the Open CA / Open CITS certification programs, and FACE / SOSA defence standards.

## What TOGAF is, in one paragraph

TOGAF is a framework for enterprise architecture — the practice of analyzing, designing, planning, and governing the structure of an organization's business processes, information systems, and technology infrastructure so they align with the organization's strategy. TOGAF is not a methodology in the prescriptive sense, not a modeling notation (ArchiMate fills that role), and not a maturity model. It is a body of practice with a method (the ADM), a content structure, a classification scheme (the Enterprise Continuum), and a governance model (the Architecture Capability Framework). Organizations adopt and tailor TOGAF; there is no certifiable management system. Individuals certify (Foundation, Practitioner); organizations do not.

## The Architecture Development Method (ADM) — the core

The ADM is the heart of TOGAF: a step-by-step method for developing and managing the lifecycle of an enterprise architecture. Nine phases arranged in a cycle, with Requirements Management at the center:

- **Preliminary Phase** — establish the architecture capability; tailor TOGAF; define architecture principles.
- **Phase A: Architecture Vision** — scope, stakeholders, business case, high-level vision; secure approval to proceed.
- **Phase B: Business Architecture** — target business architecture; gap analysis vs baseline.
- **Phase C: Information Systems Architectures** — data architecture and application architecture; target states; gap analysis.
- **Phase D: Technology Architecture** — target technology architecture; gap analysis.
- **Phase E: Opportunities and Solutions** — consolidate gaps; identify delivery vehicles (projects, programmes); transition architectures.
- **Phase F: Migration Planning** — detailed implementation and migration plan; prioritize; cost-benefit.
- **Phase G: Implementation Governance** — architecture oversight during delivery; architecture contracts; compliance reviews.
- **Phase H: Architecture Change Management** — manage changes to the architecture; assess whether changes warrant a new ADM cycle.
- **Requirements Management** (central) — manage architecture requirements throughout all phases.

Detail in [[TOGAF ADM]].

## The Architecture Content Framework

A structured model of the work products produced by architecture work:

- **Deliverables** — formal, contractual outputs (e.g., Architecture Definition Document, Architecture Roadmap, Architecture Contract). Reviewed and signed off.
- **Artifacts** — granular architectural work products (catalogs, matrices, diagrams) describing aspects of the architecture from a viewpoint.
- **Building blocks** — reusable components of capability:
  - **Architecture Building Blocks (ABBs)** — define what functionality is required; specification-level.
  - **Solution Building Blocks (SBBs)** — implement the ABBs; product / component-level.

The content metamodel defines the entities (actors, functions, data entities, applications, technology components, etc.) and their relationships.

Detail in [[TOGAF Content Framework]].

## The Enterprise Continuum

A classification scheme for architecture assets, from generic to specific:

- **Architecture Continuum** — Foundation Architectures → Common Systems Architectures → Industry Architectures → Organization-Specific Architectures. Each level more specialized.
- **Solutions Continuum** — the corresponding implementation assets at each level: Foundation Solutions → Common Systems Solutions → Industry Solutions → Organization-Specific Solutions.
- **Architecture Repository** — where the assets live: the Architecture Metamodel, the Architecture Capability, the Architecture Landscape (current architectures), the Standards Information Base, the Reference Library, the Governance Log.

Detail in [[TOGAF Enterprise Continuum]].

## The Architecture Capability Framework

How to establish and operate an architecture practice:

- **Architecture Board** — cross-organizational body overseeing architecture governance.
- **Architecture Governance** — the practice of managing and controlling architectures at an enterprise level. Architecture Compliance reviews. Architecture Contracts.
- **Architecture Maturity Models** — assess the maturity of the architecture capability (TOGAF references the US ACMM — Architecture Capability Maturity Model — among others).
- **Architecture Skills Framework** — roles (Enterprise Architect, Business Architect, Data Architect, Application Architect, Technology Architect) and the skills each requires.

Detail in [[TOGAF Architecture Capability]].

## Certification scheme

TOGAF certifications (administered by The Open Group):

- **TOGAF Standard, 10th Edition — Foundation** (Part 1) — knowledge of TOGAF terminology, structure, ADM phases, core concepts.
- **TOGAF Standard, 10th Edition — Practitioner** (Part 2) — ability to apply TOGAF; scenario-based exam.
- **TOGAF Enterprise Architecture Practitioner** — combined Part 1 + Part 2.
- **TOGAF Business Architecture, Digital Enterprise Architecture, and other Series Guide-aligned badges** — newer modular credentials introduced with the 10th Edition restructure.
- **Open CA (Open Certified Architect)** — experience-based certification (board-reviewed, not exam-based) at Certified / Master / Distinguished levels. Broader than TOGAF; recognizes architecture practitioner experience generally.

Detail in [[TOGAF Certification Scheme]].

## TOGAF vs other EA frameworks

| Framework | Origin | Character | Relationship to TOGAF |
|---|---|---|---|
| Zachman Framework | John Zachman, 1987 | Taxonomy / ontology (6×6 matrix) | Complementary; Zachman classifies, TOGAF provides method |
| FEAF / FEA | US federal government | Government EA reference model | Influenced by and influencing TOGAF |
| DoDAF / MODAF / NAF | US / UK / NATO defence | Defence-specific viewpoints | Domain-specific; TOGAF more general |
| Gartner EA (formerly Meta) | Gartner | Consulting-driven, business-outcome-focused | Competing approach; less prescriptive method |
| ArchiMate | The Open Group | Modeling notation | Companion to TOGAF (same owner) |
| IT4IT | The Open Group | Reference architecture for IT management | Companion to TOGAF (same owner) |
| SAFe (architecture parts) | Scaled Agile | Agile-scaling framework with architecture roles | Tension and reconciliation efforts |

Detail in [[TOGAF vs Other EA Frameworks]].

## Why this matters for SRE and AI-system work

- **TOGAF is the enterprise-architecture lingua franca.** Large organizations (banks, insurers, government, telcos, manufacturers) often run TOGAF-aligned EA practices. SRE / platform work in these contexts interacts with the EA function — architecture review boards, technology standards, reference architectures.
- **The ADM provides a structure for AI-system architecture work.** Introducing AI capabilities into an enterprise is an architecture change: Phase B (business architecture — what business capabilities does AI enable / change?), Phase C (application architecture — how do AI services fit the application landscape?), Phase D (technology architecture — model serving, vector stores, GPU infrastructure, vendor APIs), Phase E-F (roadmap and migration). The ADM gives a checklist for not skipping the analysis.
- **Architecture governance is where AI-system risk surfaces at the enterprise level.** Architecture Compliance reviews are a natural place to assess whether an AI-system design meets enterprise standards (security, data handling, vendor management, reversibility). The Architecture Board should treat AI-system designs as a review category.
- **Reference architectures for AI.** The Enterprise Continuum concept (Foundation → Common → Industry → Organization-Specific) maps onto how AI reference architectures are evolving: generic patterns (RAG, agent loops, tool-use) → industry-specific patterns → organization-specific implementations.
- **TOGAF vs Agile tension is the same shape as ITIL vs DevOps.** Heavyweight EA processes can stifle delivery velocity. TOGAF's 10th Edition Series Guides include agile-EA guidance; the reconciliation is partial. SRE / platform practitioners caught between an EA function and a delivery mandate should know both vocabularies.

## Stefan-context relevance

Stefan does SRE / staff-engineer-track work touching:

- Enterprise contexts where TOGAF-aligned EA functions operate ([employer]-class buyers, large manufacturers, regulated industries)
- AI-system architecture work that should be framed as enterprise-architecture change, not just engineering
- Procurement / consulting engagements where EA vocabulary is load-bearing

Cluster atoms should:

- Stay practitioner-grounded (named ADM phases, real adoption patterns)
- Bridge TOGAF vocabulary with SRE / platform-engineering / DevOps / Agile vocabulary
- Surface AI-system-architecture fit points and gaps
- Avoid both EA-evangelist tone and EA-dismissive tone — the framework has structural value and well-documented failure modes

## Related clusters and atoms

- [[ITIL Cluster|ITIL]] — service management; ITIL and TOGAF are complementary (ITIL runs services, TOGAF designs the structure they fit into); some practitioners hold both
- [[ISO 27001 Cluster|ISO 27001]] — security architecture is a TOGAF concern (Series Guide); ISO 27001 controls are inputs to architecture design
- [[SRE/pillars/index|SRE pillars]] — platform and reliability practice; intentional cross-link

## Conventions for this cluster

- Atoms named `TOGAF <Topic>.md` with consistent structure
- TOGAF Standard 10th Edition is the default version reference; 9.x noted only for historical contrast
- Cross-link to ITIL, ISO, and SRE clusters where concerns overlap
- Mark 10th-Edition restructure items explicitly where they shift practitioner expectation
- Use TOGAF terminology accurately but always provide a non-TOGAF gloss

## See also

[[TOGAF Cluster]] (pillars MOC) · [position](pillars/togaf/position.md) · [anchors](pillars/togaf/anchors.md) · [[ITIL Cluster]] · [[ISO 27001 Cluster]]
