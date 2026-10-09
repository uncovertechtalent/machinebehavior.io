title: TOGAF vs Other EA Frameworks
summary: How TOGAF relates to the other enterprise-architecture frameworks and notations: Zachman (taxonomy), FEAF / DoDAF (government / defence), ArchiMate / IT4IT (companion notations), Gartner EA (consulting approach), and the agile-EA contenders.
parent: togaf
order: 100
labels: cross-cutting, togaf
aliases: TOGAF vs Other EA Frameworks | TOGAF vs Zachman | TOGAF vs FEAF | TOGAF vs DoDAF | TOGAF vs ArchiMate | EA Framework Comparison
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/togaf/TOGAF vs Other EA Frameworks.md
reviewed: no
---
> How TOGAF relates to the other enterprise-architecture frameworks and notations: Zachman (taxonomy), FEAF / DoDAF (government / defence), ArchiMate / IT4IT (companion notations), Gartner EA (consulting approach), and the agile-EA contenders. Most of these are complementary to TOGAF rather than strictly competing; the ones that compete do so on "how do you do EA", not on "what is EA".

## Zachman Framework

- **Origin:** John Zachman, 1987 (IBM Systems Journal article), refined over decades.
- **Character:** a taxonomy / ontology, not a method. A 6×6 matrix: columns are interrogatives (What [data], How [function], Where [network], Who [people], When [time], Why [motivation]); rows are perspectives (Executive / Scope, Business Management / Business Concepts, Architect / System Logic, Engineer / Technology Physics, Technician / Component Configuration, Enterprise / Operations Instances). Each cell is a distinct, primitive model.
- **What it gives you:** a classification scheme — a way to know which artefacts you have, which you are missing, and which perspective and which interrogative each addresses.
- **What it does not give you:** a process for producing the artefacts. Zachman is "what" (the taxonomy), not "how" (the method).
- **Relationship to TOGAF:** complementary. Zachman classifies; TOGAF's ADM provides the method. Some organizations use Zachman as the artefact-classification scheme within a TOGAF-driven process. Treating them as competitors is a category error — one is a taxonomy, the other a method.

## FEAF / FEA (US Federal Enterprise Architecture)

- **Origin:** US federal government. FEAF (Federal Enterprise Architecture Framework) v1 1999; the FEA reference models early 2000s; the "Common Approach to Federal EA" 2012; the FEAF v2 2013.
- **Character:** a government EA framework with reference models — Performance Reference Model, Business Reference Model, Data Reference Model, Application Reference Model, Infrastructure Reference Model, Security Reference Model. Standardizes how US federal agencies describe and align their architectures.
- **Relationship to TOGAF:** bidirectional influence. FEAF borrowed from TOGAF (and from Zachman); TOGAF's Enterprise Continuum and reference-model thinking shaped and was shaped by FEA. US federal agencies often run TOGAF-aligned ADM processes producing FEAF-conformant artefacts.

## DoDAF / MODAF / NAF (Defence EA frameworks)

- **DoDAF** — US Department of Defense Architecture Framework. Current DoDAF 2.x. Defines "viewpoints" (All Viewpoint, Capability Viewpoint, Operational Viewpoint, Services Viewpoint, Systems Viewpoint, Data and Information Viewpoint, Standards Viewpoint, Project Viewpoint) and the "views" (specific products) within each.
- **MODAF** — UK Ministry of Defence Architecture Framework. Largely superseded by NAF.
- **NAF** — NATO Architecture Framework. Current NAF v4. Harmonizes the allied defence-EA approaches.
- **Character:** defence-specific, viewpoint-driven, oriented toward describing complex systems-of-systems for procurement and interoperability. Heavier on system / operational viewpoints than business architecture.
- **Relationship to TOGAF:** domain-specialized; TOGAF is more general. Defence organizations sometimes run TOGAF's ADM as the method while producing DoDAF / NAF-conformant views. The Unified Architecture Framework (UAF) is an effort to unify the defence frameworks; it can sit within a TOGAF process.

## ArchiMate

- **Origin:** Dutch research project (Telematica Instituut), early 2000s; adopted by The Open Group in 2008. Current ArchiMate 3.2.
- **Character:** a modeling notation — a visual language for describing enterprise architectures. Layers: Business, Application, Technology, plus Physical, and cross-cutting Motivation, Strategy, and Implementation & Migration aspects. Defines element types and relationship types and their visual representation.
- **What it gives you:** a standard way to *draw* architecture models — so a "business process" looks the same in every diagram, relationships are precise, and tools can interoperate.
- **What it does not give you:** a method (that is TOGAF's ADM) or a classification taxonomy (that is Zachman's matrix).
- **Relationship to TOGAF:** companion. Same owner (The Open Group). The ArchiMate metamodel maps onto the TOGAF content metamodel. TOGAF's content framework describes *what* artefacts to produce; ArchiMate provides *how to draw* many of them. The combination — TOGAF method + ArchiMate notation + an ArchiMate-capable tool — is a common enterprise EA stack.

## IT4IT

- **Origin:** The Open Group, 2015. Current IT4IT 3.x.
- **Character:** a reference architecture for managing the business of IT — the "IT value chain" with four value streams: Strategy to Portfolio (S2P), Requirement to Deploy (R2D), Request to Fulfil (R2F), Detect to Correct (D2C). Defines the functional components and data objects that flow through the IT value chain.
- **Relationship to TOGAF:** companion. Same owner. IT4IT is itself an example of a reference architecture (an Enterprise Continuum asset at the Common Systems level — a reference architecture for "running IT"). TOGAF's ADM could produce an IT4IT-aligned target architecture for an IT organization. IT4IT also complements ITIL (IT4IT is the architecture of the IT-management capability; ITIL is the practice).

## Gartner EA (formerly Meta Group EA)

- **Origin:** Meta Group (acquired by Gartner 2005); evolved into Gartner's EA practice and methodology.
- **Character:** a consulting-driven approach emphasizing business outcomes, "future-state architecture", and EA-as-strategic-enabler. Less prescriptive on method than TOGAF; more emphasis on the EA function's positioning and value contribution. Gartner publishes EA maturity models, EA team-structure guidance, and "EA reference architecture" material as analyst products.
- **Relationship to TOGAF:** a competing answer to "how do you do EA" — but at a different level. Gartner EA is light on method detail (no ADM equivalent) and heavy on positioning / outcomes; TOGAF is heavy on method and light on the "how do you make EA matter politically" question. Many organizations run a TOGAF-derived method while using Gartner's positioning / maturity guidance. They are not mutually exclusive.

## PEAF, IAF, and other proprietary / niche frameworks

- **PEAF** (Pragmatic Enterprise Architecture Framework) — Kevin Smith. Positioned as a leaner, more pragmatic alternative to TOGAF. Modest adoption.
- **IAF** (Integrated Architecture Framework) — Capgemini-proprietary. TOGAF-influenced; used within Capgemini engagements.
- **Various consultancy-internal frameworks** — most large IT consultancies have a proprietary EA method, usually TOGAF-derived or TOGAF-compatible.

## SAFe and agile-architecture approaches

- **SAFe (Scaled Agile Framework)** — includes architecture roles (Enterprise Architect, System Architect, Solution Architect) and concepts (architectural runway, intentional architecture vs emergent design, the "architect as enabler" framing).
- **Open Agile Architecture (O-AA)** — The Open Group's own agile-architecture standard, separate from TOGAF.
- **"Minimum Viable Architecture", "Just Enough Architecture", "Evolutionary Architecture"** (Ford / Parsons / Kua) — lighter-weight thinking that pushes back on heavyweight EA.
- **Relationship to TOGAF:** tension and partial reconciliation. The classic central-EA-function model TOGAF supports is in tension with autonomous-product-team / platform-engineering models. TOGAF's 10th Edition agile-EA Series Guide, the O-AA standard, and the "EA as enabling team" repositioning are attempts to bridge. No settled answer; this is the live front in EA practice.

## Quick decision guide

- **You need a classification scheme for architecture artefacts** → Zachman (use it within a TOGAF process).
- **You need a method for developing enterprise architecture** → TOGAF's ADM (the default; few alternatives at this level of method detail).
- **You need a notation for drawing architecture models** → ArchiMate (companion to TOGAF).
- **You are a US federal agency** → FEAF-conformant, likely with a TOGAF-derived method.
- **You are a defence / aerospace organization** → DoDAF / NAF / UAF, possibly with TOGAF as the method.
- **You want guidance on the EA function's positioning and value** → Gartner EA material (alongside, not instead of, TOGAF).
- **You are an agile / product-team-centric organization** → TOGAF's agile-EA Series Guide, O-AA, "minimum viable architecture" thinking; expect to tailor TOGAF heavily or use it as a thinking checklist rather than a process.
- **You want the architecture of "running IT"** → IT4IT (complements TOGAF and ITIL).

## SRE and AI-system fit notes

- **For AI-system architecture, TOGAF's ADM is the most complete method available** — there is no "AI EA framework" with comparable method detail. Use the ADM as the structure (business architecture impact, application landscape fit, technology architecture, roadmap, governance) and tailor heavily for short iterations.
- **ArchiMate can model AI-system architectures** — application-layer elements for AI services, technology-layer elements for model-serving infrastructure, motivation-layer elements for the drivers / constraints (regulatory, vendor, risk). An organization-specific ArchiMate extension can capture AI-specific entities (model, prompt template, agent, tool definition, vendor relationship).
- **For agile / platform-team contexts, lean on the agile-EA thinking, not the heavyweight ADM** — minimum viable architecture, just-enough analysis, iterating in short cycles. The "EA as enabling team" framing (shared AI patterns, shared AI infrastructure, shared vendor relationships, light-touch governance) is the right shape for most modern organizations adopting AI.
- **No single framework solves AI governance** — TOGAF for the architecture method, ISO/IEC 42001 for the AI management system, ISO 27001 for security controls, the OWASP LLM Top 10 for the technical threat taxonomy, NIST AI RMF for outcome-oriented framing. Combine.

## See also

- [[TOGAF Cluster|cluster MOC]] · [[TOGAF ADM]] · [[TOGAF Enterprise Continuum]] · [[TOGAF Controversies]]
- [[ITIL Cluster|ITIL]] (service management — complements TOGAF; IT4IT bridges the two)
- [[ISO 27001 Cluster|ISO 27001]] (security controls — inputs to architecture design)
