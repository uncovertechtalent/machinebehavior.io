title: TOGAF position
summary: Current view on what TOGAF (Standard 10th Edition) is good for, what it is not good for, and where it sits as an enterprise-architecture framework.
parent: togaf
order: 5
labels: position, togaf
aliases: TOGAF Position | TOGAF Current View
type: position
created: 2026-05-12
updated: 2026-05-12
origin: pillars/togaf/position.md
reviewed: no
---
> Current view on what TOGAF (Standard 10th Edition) is good for, what it is not good for, and where it sits as an enterprise-architecture framework. Dated, revisable, diff-tracked.

## State of the view as of 2026-05-12

### What TOGAF does well

- **Provides a common EA vocabulary.** "Baseline architecture", "target architecture", "gap analysis", "transition architecture", "building block", "architecture principle" — these have TOGAF-derived meanings in most large-organization EA functions. Adoption reduces translation cost.
- **The ADM is a usable checklist.** Even practitioners who do not run the full ADM cycle use it as a reminder of what to consider: stakeholder concerns, business architecture before technology, gap analysis, roadmap, governance during delivery. The phases are a defence against skipping analysis.
- **Separates "what" from "how" via building blocks.** The ABB / SBB distinction (architecture building block = required functionality; solution building block = chosen implementation) is a clean way to keep architecture decisions separate from procurement decisions.
- **Governance model is substantive.** The Architecture Board, Architecture Compliance reviews, and Architecture Contracts give the EA function teeth — a way to ensure delivery actually follows the architecture, not just a way to produce documents.
- **10th Edition restructure is sensible.** Splitting stable Fundamental Content from updatable Series Guides addresses the "the framework is frozen for years while the world moves" problem. Agile-EA, digital-EA, security-architecture guidance can evolve without a full standard revision.
- **Vendor-neutral.** The Open Group is a consortium, not a single vendor. TOGAF does not push a particular tool or technology stack (unlike, say, a vendor's reference architecture).
- **Complements other frameworks cleanly.** TOGAF + Zachman (Zachman classifies, TOGAF provides method). TOGAF + ArchiMate (ArchiMate models, TOGAF provides method). TOGAF + ITIL (TOGAF designs the structure, ITIL runs the services in it). TOGAF + COBIT (COBIT governs, TOGAF architects).

### What TOGAF does poorly

- **Heavyweight by default.** A full ADM cycle with complete content-framework deliverables is a large undertaking. Organizations that implement TOGAF "by the book" produce vast documentation that ages quickly and is read by few. The framework permits tailoring; practitioner culture often does not.
- **"Shelfware architecture" failure mode.** EA functions produce target architectures and roadmaps that delivery teams ignore. The architecture document becomes an artefact, not a constraint. TOGAF's governance model is meant to prevent this; in practice, EA functions often lack the organizational authority to enforce it.
- **ADM-as-waterfall misuse.** The ADM is drawn as a cycle and described as iterative, but it is frequently implemented as a linear, multi-month, big-design-up-front exercise — the antithesis of Agile delivery. The 10th Edition agile-EA Series Guide acknowledges this; the cultural inertia is real.
- **Certification-mill problem.** TOGAF Foundation in particular is widely regarded as a memorization exam — terminology, ADM phase names, content-framework structure — that validates exam-taking more than architecture capability. The certification generates revenue for The Open Group and accredited training partners; certificate-counting in CVs and procurement signals incentivizes credential acquisition over capability.
- **EA-function-vs-delivery tension.** TOGAF is the standard tool of the central-EA-function model. That model is in tension with autonomous-product-team / platform-engineering models. TOGAF does not resolve the tension; it tends to reinforce the central-function approach.
- **AI-system architecture gaps.** The 10th Edition Series Guides are catching up (digital-EA guidance, some AI references), but the deep questions — how do you architect for inherently-non-deterministic components, how do you do gap analysis when the "target" includes capabilities that emerge rather than being designed, how do you govern an architecture that includes autonomous agents — are not addressed in depth.
- **Slow at the core.** Even with the Series Guide restructure, the Fundamental Content (ADM, content framework) moves slowly. The ADM has been substantially stable since TOGAF 9 (2009).
- **Abstraction-heavy.** TOGAF documentation is dense and abstract. The barrier to productive use is high; many "TOGAF-trained" people never apply it because the path from certification to practice is unclear.

### Where the evidence currently sits

- **TOGAF dominates enterprise EA.** Most large-organization EA functions use TOGAF or a TOGAF-derived approach. Penetration is highest in regulated industries (finance, insurance, government, telecoms, utilities, defence) and lowest in tech-native organizations.
- **Certification volume is high.** The Open Group reports hundreds of thousands of TOGAF certifications cumulatively. Foundation-level certificates particularly common in enterprise-architect and solution-architect roles.
- **The central-EA-function model is under pressure.** Platform engineering, product-team autonomy, and "you build it, you run it" thinking challenge the premise of a central EA function dictating architecture. EA functions are increasingly repositioning as enabling / advisory rather than controlling — "enabling team" in Team Topologies terms. Whether this repositioning succeeds varies by organization.
- **Agile EA is the active reconciliation front.** "How do we do enterprise architecture in an agile organization" is the live question. TOGAF's agile-EA Series Guide, the "minimum viable architecture" concept, lightweight-ADM approaches, and architecture-as-enablement framings are all attempts. No settled answer.
- **AI is reshaping EA practice.** AI-assisted architecture analysis, AI-generated impact assessments, and the need to architect AI capabilities into the enterprise are all entering EA work. The 10th Edition acknowledges; it does not formally integrate.
- **TOGAF 10 → TOGAF 11?** No public roadmap. The Open Group's pattern with the 10th Edition is incremental Series Guide updates rather than major version increments. The Fundamental Content is likely stable for years.

## Personal calibration

- **Working assumption for enterprise engagements:** TOGAF vocabulary will be load-bearing if the client has an EA function. Speak it accurately. Avoid both evangelism and dismissal.
- **Working assumption for AI-system architecture work:** frame it as an enterprise-architecture change, not just an engineering project. Use the ADM phases as a checklist (business architecture impact, application landscape fit, technology architecture, roadmap, governance). Do not produce the full content-framework deliverable set unless the client requires it.
- **Working assumption for the EA-vs-delivery tension:** be explicit about which model the organization runs (central EA function vs platform-enabled product teams) and adapt. Bridge the vocabularies; do not pretend the tension does not exist.
- **Working assumption for own credentialing:** TOGAF Foundation is procurement-recognized and a reasonable bar; Practitioner has more signal value than Foundation; Open CA (experience-based, board-reviewed) is the more credible architecture-capability signal but requires substantial documented experience. Worth holding Foundation+Practitioner if doing EA-adjacent enterprise work; Open CA if architecture is a primary identity.
- **Working assumption for small / solo operations:** TOGAF as conceptual scaffolding, not as process. Use the ADM phases as a thinking checklist; use the building-block concept; skip the governance machinery that assumes enterprise scale and a standing EA function.

## What would shift this view

- **A major TOGAF 11 release** with substantively rebuilt agile-EA and AI-system-architecture content would shift the framework's relevance for modern delivery contexts.
- **A widely-adopted lightweight EA approach** displacing TOGAF in the enterprise. Nothing currently matches TOGAF's reach; the "minimum viable architecture" and "EA as enablement" movements are tendencies, not frameworks.
- **The Open Group governance changes** affecting framework quality or content openness. The Open Group is a consortium with broad membership; framework capture risk is lower than PeopleCert / ITIL but not zero.
- **AI-assisted EA tooling maturing** to the point where the ADM's analysis steps are substantially automated. Possible within 3-5 years; would change what "doing TOGAF" means in practice.

## See also

- [[TOGAF Cluster|cluster MOC]] · [[TOGAF Controversies]]
- [anchors](pillars/togaf/anchors.md)
