title: TOGAF Enterprise Continuum
summary: A classification scheme for architecture and solution assets, ordered from generic to organization-specific.
parent: togaf
order: 100
labels: togaf, togaf-component
aliases: TOGAF Enterprise Continuum | Architecture Continuum | Solutions Continuum | TOGAF Architecture Repository
type: togaf-component
created: 2026-05-12
updated: 2026-06-08
origin: pillars/togaf/TOGAF Enterprise Continuum.md
reviewed: no
---
> A classification scheme for architecture and solution assets, ordered from generic to organization-specific. It gives a way to talk about reuse: where does a given asset sit on the spectrum from "universal pattern" to "our specific implementation"? Paired with the Architecture Repository, which stores the assets.

## The two continua

The Enterprise Continuum has two parallel parts:

### Architecture Continuum

Architecture assets (the "what / specification" side), ordered generic → specific:

1. **Foundation Architectures** — the most generic. Universal building blocks and standards applicable to any organization. TOGAF's Technical Reference Model (TRM) is an example of a Foundation Architecture asset.
2. **Common Systems Architectures** — patterns common across many organizations but not universal. Examples: a generic security architecture, a generic management-and-monitoring architecture, a generic network-infrastructure architecture. The Integrated Information Infrastructure Reference Model (III-RM) is a Common Systems Architecture asset in TOGAF.
3. **Industry Architectures** — patterns specific to an industry. Examples: a banking reference architecture (BIAN), a telecoms reference architecture (TM Forum's Frameworx / SID / eTOM), a retail reference architecture (ARTS), an insurance reference architecture (ACORD). Industry bodies maintain these.
4. **Organization-Specific Architectures** — the architecture for a particular organization. The most specific. This is what an ADM cycle in a given company produces.

Each level inherits from and specializes the level above. Organization-Specific Architectures draw on Industry Architectures, which draw on Common Systems Architectures, which draw on Foundation Architectures.

### Solutions Continuum

The corresponding implementation assets (the "how / realization" side), ordered generic → specific:

1. **Foundation Solutions** — generic, off-the-shelf building blocks: programming languages, operating systems, generic services.
2. **Common Systems Solutions** — products implementing common-systems patterns: a commercial security product, a commercial monitoring suite, a database management system.
3. **Industry Solutions** — products / packages for an industry: a core banking platform, a telecom billing system, an insurance policy-administration system.
4. **Organization-Specific Solutions** — the actual deployed solution for a particular organization, configured and integrated for that organization's needs.

The two continua relate: an Architecture Building Block at a given continuum level is realized by a Solution Building Block at the corresponding level. An Industry Architecture's "core banking capability" ABB is realized by an Industry Solution's "Temenos / Finastra / Mambu" SBB.

## Why the continuum matters

- **Reuse discipline.** Before designing something new, check whether a Foundation, Common Systems, or Industry asset already covers it. Only build Organization-Specific assets where the organization genuinely differs.
- **Vendor / standards leverage.** Industry reference architectures (BIAN, TM Forum, ACORD) and standards bodies' work are Architecture Continuum assets you can adopt rather than reinventing.
- **Procurement clarity.** Knowing whether you need a Common Systems Solution (commodity product) or an Organization-Specific Solution (heavily customized / built) shapes the buy-vs-build decision.
- **Avoiding over-specialization.** Organizations that build everything Organization-Specific end up with high maintenance cost and low vendor leverage. The continuum is a prompt to ask "could a more generic asset serve here?"

## The Architecture Repository

Where the continuum's assets — and the organization's own architecture work products — are stored. TOGAF defines the repository as having several parts:

- **Architecture Metamodel** — the tailored content metamodel the organization uses (entities, relationships, extensions).
- **Architecture Capability** — definition of the parameters, structures, and processes supporting the architecture function (links to the Architecture Capability Framework).
- **Architecture Landscape** — the architectural representation of assets in use (or planned) in the organization, at three levels: Strategic Architectures (broad, long-term), Segment Architectures (focused on a business segment), Capability Architectures (detailed, specific capability).
- **Standards Information Base (SIB)** — the standards the organization mandates / recommends (technology standards, data standards, security standards, regulatory requirements).
- **Reference Library** — guidelines, templates, patterns, reference architectures, and other reusable material (including Foundation / Common Systems / Industry assets adopted from outside).
- **Governance Log** — the record of governance activity: compliance assessments, dispensations / waivers, capability assessments, calendars, project portfolios.
- **Architecture Requirements Repository** — the requirements identified across ADM cycles (the source/sink for Requirements Management).
- **Solutions Landscape** — the SBBs in use that realize the architecture landscape's ABBs.

In practice, the Architecture Repository is implemented in an EA tool (BiZZdesign, Sparx Enterprise Architect, Avolution Abacus, LeanIX, Ardoq, MEGA, Orbus, others) or, in lean setups, in a wiki / document store / model repository.

## SRE and AI-system fit notes

- **AI reference architectures sit at the Common Systems / Industry levels.** Generic AI patterns — RAG, agent loops, tool-use, prompt-chaining, retrieval-augmented agents — are Common Systems Architecture assets. Industry-specific AI patterns (AI for fraud detection in banking, AI for claims processing in insurance, AI for predictive maintenance in manufacturing) are Industry Architecture assets. Adopt these rather than reinventing; specialize to Organization-Specific only where your context genuinely differs.
- **Model providers are Common Systems / Industry Solutions.** The Claude / OpenAI / Google APIs are Common Systems Solutions (commodity AI capability). Vertical AI products (legal-research AI, medical-coding AI, automotive-simulation AI) are Industry Solutions. Knowing where a given AI capability sits shapes the buy-vs-build decision.
- **Standards Information Base for AI.** The SIB should include AI-specific standards: which model providers / tiers are approved, which data classifications can go to which APIs, OWASP LLM Top 10 as a security baseline, ISO 42001 alignment requirements, the organization's AI principles. New AI capabilities check against the SIB.
- **Governance Log for AI dispensations.** When a team wants to use an AI tool / pattern that diverges from the SIB, the dispensation goes in the Governance Log with its rationale and expiry. This is the record of "we allowed X exception for Y reason until Z date."
- **Architecture Landscape for AI.** Maintain a view of which AI capabilities are in use / planned across the organization, at the three landscape levels. Without it, AI adoption sprawls — duplicate RAG implementations, inconsistent vendor relationships, no shared monitoring.

## See also

- [[TOGAF Cluster|cluster MOC]] · [[TOGAF ADM]] · [[TOGAF Content Framework]] · [[TOGAF Architecture Capability]]
