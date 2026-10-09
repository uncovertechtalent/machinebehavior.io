title: ITIL
summary: Map of ITIL 4 (2019, with 2023 refresh) as the dominant IT service management framework.
parent: index
order: 240
labels: itil, itsm-frameworks, moc, service-management
aliases: ITIL Cluster | ITIL | ITIL 4 | IT Infrastructure Library
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/itil/ITIL Cluster.md
reviewed: no
---
> Map of ITIL 4 (2019, with 2023 refresh) as the dominant IT service management framework. Service Value System, Service Value Chain, four dimensions, seven guiding principles, 34 practices, certification scheme. Reference cluster for service-management decisions in SRE / platform / AI-ops work and for procurement contexts that mandate ITIL alignment.

## Anchors

- [position](pillars/itil/position.md): current view, dated, revisable
- [anchors](pillars/itil/anchors.md): primary documents, PeopleCert, training providers, named practitioners

## Provenance

- **ITIL v1** (1989-1996) — UK Central Computer and Telecommunications Agency (CCTA). Origin: standardize IT operations across UK government. ~40 books, function-oriented.
- **ITIL v2** (2000-2004) — consolidated into ~10 books grouped around Service Support and Service Delivery. First version to gain meaningful international adoption.
- **ITIL v3** (2007, refreshed 2011) — Office of Government Commerce (OGC) owner. Five core books along the **service lifecycle** (Service Strategy, Design, Transition, Operation, Continual Service Improvement). 26 processes + 4 functions. Dominant in 2010s enterprise IT.
- **ITIL 4** (2019) — paradigm shift. AXELOS owner (joint venture Cabinet Office + Capita, formed 2013). Replaced the lifecycle / process model with the **Service Value System (SVS)** built around the **Service Value Chain (SVC)**, four dimensions, seven guiding principles, and 34 practices.
- **PeopleCert acquisition** (2021) — AXELOS acquired by PeopleCert; PeopleCert now owns ITIL, PRINCE2, MSP, and adjacent best-practice IP. Material published via peoplecert.org.
- **ITIL 4 2023 refresh** — Practice Manager modules and Master capstone refreshed; some practice content updated to reflect cloud / DevOps / AI / agile maturation since 2019.

## What ITIL is, in one paragraph

ITIL is a framework for IT service management. Not a standard, not a methodology — a body of practice with terminology, models, and recommended approaches. The framework describes how IT organizations plan, build, deliver, and continually improve services that create value for stakeholders. ITIL 4 reframed the 30-year tradition around the Service Value System, treating service management as a holistic value-creation activity rather than a sequence of process steps. Organizations adopt and tailor ITIL; there is no certifiable management system in the ISO sense (ISO/IEC 20000 fills that role for organizations seeking certification).

## What changed structurally from v3 to ITIL 4

- **Lifecycle dropped.** v3's Service Strategy → Design → Transition → Operation → CSI sequence replaced by the Service Value Chain (a network of activities, not a linear flow).
- **Processes renamed practices.** 26 v3 processes + 4 functions consolidated into 34 ITIL 4 practices. Some processes merged (e.g., capacity and availability into Service Level Management adjacents), some renamed.
- **Service Value System (SVS) introduced.** Holistic operating model containing: guiding principles, governance, Service Value Chain, practices, continual improvement.
- **Four Dimensions added.** Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes — meant to be applied to every aspect of service management.
- **Seven Guiding Principles** lifted from ITIL Practitioner (2016) and made central to the framework.
- **Stronger Agile / Lean / DevOps integration** in terminology and recommendations.
- **Customer-centric value framing** — services exist to co-create value with consumers; value definition is consumer-led.

## The Service Value System (SVS) — high level

The SVS describes how all the components and activities work together to facilitate value creation. Inputs: opportunity / demand. Outputs: value. Five components:

- **Guiding principles** — seven recommendations to guide decisions and actions.
- **Governance** — direction-setting and oversight by the governing body.
- **Service Value Chain** — six activities that respond to demand and create value.
- **Practices** — 34 capabilities used in the value chain.
- **Continual improvement** — recurring activity at all levels.

Detail in [[ITIL 4 Service Value System]].

## The Service Value Chain (SVC) — six activities

The SVC is the operating model at the heart of the SVS. Six activities:

- **Plan** — strategic, tactical, operational planning.
- **Improve** — ongoing improvement across all components.
- **Engage** — interaction with stakeholders, understanding needs.
- **Design & Transition** — build services that meet stakeholder needs and transition them to operations.
- **Obtain / Build** — acquire or build components needed for services.
- **Deliver & Support** — provide services to consumers and resolve issues.

The activities are interconnected; value streams use them in different sequences depending on the work type.

Detail in [[ITIL 4 Service Value Chain]].

## The Four Dimensions of service management

Applied to every aspect of SVS:

- **Organizations & People** — structures, roles, skills, culture, communication.
- **Information & Technology** — service data, tooling, automation, AI / ML.
- **Partners & Suppliers** — vendor relationships, contracts, sourcing models.
- **Value Streams & Processes** — how activities are organized and executed.

External factors (PESTLE — political, economic, social, technological, legal, environmental) shape all four dimensions.

Detail in [[ITIL 4 Four Dimensions]].

## The Seven Guiding Principles

Universal recommendations that guide adoption and adaptation:

1. **Focus on value** — every action contributes to value for stakeholders.
2. **Start where you are** — don't discard everything; assess and build on existing capability.
3. **Progress iteratively with feedback** — small steps, frequent feedback.
4. **Collaborate and promote visibility** — work together, share information.
5. **Think and work holistically** — service is a system; address it as such.
6. **Keep it simple and practical** — minimum viable process; cut what doesn't add value.
7. **Optimize and automate** — humans on judgment, machines on repetition.

Detail in [[ITIL 4 Guiding Principles]].

## The 34 Practices

ITIL 4 organizes capabilities into 34 practices grouped in three categories:

- **General management practices (14)** — adopted from broader business management: Strategy Management, Portfolio Management, Architecture Management, Service Financial Management, Workforce and Talent Management, Continual Improvement, Measurement and Reporting, Risk Management, Information Security Management, Knowledge Management, Organizational Change Management, Project Management, Relationship Management, Supplier Management.
- **Service management practices (17)** — core service work: Availability Management, Business Analysis, Capacity and Performance Management, Change Enablement, Incident Management, IT Asset Management, Monitoring and Event Management, Problem Management, Release Management, Service Catalogue Management, Service Configuration Management, Service Continuity Management, Service Design, Service Desk, Service Level Management, Service Request Management, Service Validation and Testing.
- **Technical management practices (3)** — technology-specific: Deployment Management, Infrastructure and Platform Management, Software Development and Management.

Detail in [[ITIL 4 Practices]].

## Certification scheme

ITIL 4 certifications (administered by PeopleCert):

- **Foundation** — entry. SVS, SVC, four dimensions, guiding principles, basic practices.
- **Managing Professional (MP)** stream — for technically-focused practitioners. Four modules:
  - Create, Deliver and Support (CDS)
  - Drive Stakeholder Value (DSV)
  - High-Velocity IT (HVIT)
  - Direct, Plan and Improve (DPI) (shared with SL)
- **Strategic Leader (SL)** stream — for business / strategic leaders. Two modules:
  - Direct, Plan and Improve (DPI) (shared with MP)
  - Digital and IT Strategy (DITS)
- **Practice Manager (PM)** stream — for practice-area specialists. Six modules grouped by practice cluster:
  - Monitor, Support, and Fulfil
  - Plan, Implement, and Control
  - Collaborate, Assure, and Improve
  - Create, Deliver, and Support
  - Drive Stakeholder Value
  - High-Velocity IT
- **Master** — capstone, requires MP + SL completion and practitioner experience.
- **Specialist** modules for specific practices and topic areas.

Detail in [[ITIL 4 Certification Scheme]].

## ITIL vs ISO/IEC 20000

| Aspect | ITIL 4 | ISO/IEC 20000-1 |
|---|---|---|
| Type | Framework, best practice | Certifiable standard |
| Owner | PeopleCert | ISO / IEC |
| Recognition | Body of practice | Certification |
| Mandatory content | None (recommended) | "Shall" requirements |
| Certifiable scope | Individuals, not orgs | Orgs (and individuals via training) |
| Mechanics | Adopt and adapt | Certify against shall-list |

Detail in [[ITIL vs ISO 20000]].

## Why this matters for SRE and AI-agent work

- **ITIL is the lingua franca of enterprise IT operations.** SRE work in enterprise contexts often interacts with ITIL practices: change enablement, incident management, problem management, service level management. Understanding the vocabulary reduces friction.
- **ITIL vs SRE tension is real.** ITIL's lineage is process-heavy enterprise IT. SRE's lineage is Google-origin software-engineering-applied-to-operations. The two communities have sometimes treated each other as rivals; the reality is that mature operations use both — ITIL for structure, SRE for engineering discipline. ITIL 4's High-Velocity IT module is an explicit reach toward DevOps / SRE practice.
- **AI-ops adoption shapes practice evolution.** Monitoring and Event Management practice, Incident Management practice, and Problem Management practice are all evolving as AIOps tooling matures. ITIL 4 acknowledges this; practitioner work increasingly bridges ITIL terminology with modern observability and AI-assisted operations.
- **Service Level Management × AI features.** AI features have novel reliability characteristics (vendor-side model drift, response-time variability, hallucination as a failure mode). ITIL Service Level Management practice provides a structure for SLO definition; the underlying SLOs need rethinking for AI-system characteristics.
- **Supplier Management × model providers.** ITIL Supplier Management practice maps naturally to model-provider relationships (Anthropic, OpenAI, etc.). Reuse the framework for due diligence, contract management, performance review.

## Stefan-context relevance

Stefan does SRE / staff-engineer-track work touching:

- Enterprise IT contexts where ITIL is in active use
- Customer engagements where service-management vocabulary is procurement-load-bearing
- AI-system operations that are reshaping classic ITIL practices

Cluster atoms should:

- Stay practitioner-grounded (named practices, real-world adoption patterns)
- Bridge ITIL vocabulary with SRE / DevOps / Agile vocabulary
- Surface AI-operations fit points and gaps
- Avoid both ITIL-evangelist tone and ITIL-dismissive tone — the framework has structural value and structural failure modes

## Related clusters and atoms

- [[ISO 27001 Cluster|ISO 27001]] — Information Security Management practice in ITIL maps to ISO 27001 territory
- [[TISAX Cluster|TISAX]] — automotive supplier service relationships often invoke ITIL-style mechanics
- [[SRE/pillars/index|SRE pillars]] — sibling framework with different intellectual lineage; intentional cross-link

## Conventions for this cluster

- Atoms named `ITIL <Topic>.md` with consistent structure
- ITIL 4 is the default version reference; v3 noted only for historical contrast
- Cross-link to SRE and ISO clusters where practices overlap
- Mark 2023 refresh items explicitly where they shift practitioner expectation
- Use ITIL terminology accurately but always provide a non-ITIL gloss

## See also

[[ITIL Cluster]] (pillars MOC) · [position](pillars/itil/position.md) · [anchors](pillars/itil/anchors.md) · [[ISO 27001 Cluster]] · [[TISAX Cluster]]
