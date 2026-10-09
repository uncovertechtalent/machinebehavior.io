title: TOGAF Version History
summary: Evolution from TAFIM (US DoD, early 1990s) through TOGAF 1 (1995), 8 (Enterprise Edition, 2002), 9 (major restructure, 2009), 9.1 (2011), 9.2 (2018), to the Standard 10th Edition (2022).
parent: togaf
order: 100
labels: cross-cutting, togaf
aliases: TOGAF Version History | TOGAF Evolution | TAFIM | TOGAF 9 vs 10 | TOGAF 9.2 vs 10th Edition
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/togaf/TOGAF Version History.md
reviewed: no
---
> Evolution from TAFIM (US DoD, early 1990s) through TOGAF 1 (1995), 8 (Enterprise Edition, 2002), 9 (major restructure, 2009), 9.1 (2011), 9.2 (2018), to the Standard 10th Edition (2022). Why each version happened, what changed structurally, what the practical shifts were.

## TAFIM origins (early 1990s)

**TAFIM** — Technical Architecture Framework for Information Management. US Department of Defense. A framework for managing the DoD's information-technology architecture. The DoD granted The Open Group (then X/Open and the Open Software Foundation, which merged into The Open Group in 1996) permission to develop a public framework based on TAFIM. TAFIM itself was retired by the DoD in 2000; its public descendant — TOGAF — lived on.

## TOGAF 1-7 (1995-2001) — Technical architecture era

- **TOGAF 1** (1995) — the first public version. Essentially TAFIM-derived. Technology-architecture-focused: this was about IT infrastructure architecture, not enterprise architecture.
- **TOGAF 2-7** (1996-2001) — incremental development. The ADM emerged and matured across these versions. Still narrow in scope: "Technical Edition."
- **TOGAF 7** (2001) — "Technical Edition." The last of the narrow-scope versions.

Throughout this era, "TOGAF" meant "a method for developing technical / IT infrastructure architecture."

## TOGAF 8 (2002-2003) — Enterprise Edition

The version where TOGAF became an enterprise architecture framework. Broadened from technology architecture to four architecture domains:

- **Business Architecture**
- **Data Architecture** (later "Information Systems Architecture — Data")
- **Application Architecture** (later "Information Systems Architecture — Application")
- **Technology Architecture**

The ADM was reframed to develop architecture across all four domains. The term "TOGAF" now meant "an enterprise architecture framework." TOGAF 8 (and the 8.1 / 8.1.1 updates) was widely adopted through the mid-2000s.

## TOGAF 9 (2009) — major restructure

The biggest structural revision. TOGAF 9 reorganized the framework into modular parts:

- **Part I: Introduction** — core concepts, definitions.
- **Part II: Architecture Development Method (ADM)** — the phases.
- **Part III: ADM Guidelines and Techniques** — how to apply the ADM (iteration, security, SOA, architecture principles, stakeholder management, gap analysis, etc.).
- **Part IV: Architecture Content Framework** — deliverables, artifacts, building blocks, the content metamodel. (New in TOGAF 9 — TOGAF 8 had no formal content framework.)
- **Part V: Enterprise Continuum and Tools** — the Architecture / Solutions Continua, the Architecture Repository.
- **Part VI: TOGAF Reference Models** — the TRM (Technical Reference Model) and III-RM (Integrated Information Infrastructure Reference Model).
- **Part VII: Architecture Capability Framework** — establishing and operating an architecture practice, the Architecture Board, governance, maturity models, skills framework. (New in TOGAF 9 — formalized the "how to run an EA function" content.)

Key additions in TOGAF 9: the Architecture Content Framework (Part IV), the Capability Framework (Part VII), the content metamodel, the building-block concept formalized, stronger Enterprise Continuum treatment. TOGAF 9 was the version that made TOGAF "complete" as an EA framework.

## TOGAF 9.1 (2011) — maintenance

A maintenance release. Corrections, clarifications, and consistency fixes across the TOGAF 9 content. No structural change. Most "TOGAF 9" implementations in the 2010s were actually 9.1.

## TOGAF 9.2 (2018) — update

A content update (not a restructure):

- **Improved Business Architecture content** — better treatment of business capabilities, value streams, organization mapping, business models. Aligned with the Business Architecture Guild's BIZBOK work.
- **Content metamodel simplification** — streamlined.
- **ArchiMate alignment** — closer mapping between the TOGAF content metamodel and the ArchiMate modeling language (both owned by The Open Group).
- **Modularization groundwork** — some content moved toward a "TOGAF Library" of supplementary guides, presaging the 10th Edition's Series Guide structure.
- **Removed dated content** — older reference material trimmed.

TOGAF 9.2 is still in wide use in 9.x-trained workforces; the 10th Edition bridge exam carries 9.2 certifications forward.

## TOGAF Standard, 10th Edition (2022) — Fundamental Content + Series Guides

The current version. The headline change is structural: TOGAF is split into two parts with different stability characteristics.

### TOGAF Fundamental Content

The stable core, expected to change rarely:

- Introduction and Core Concepts
- Architecture Development Method (the ADM — substantially unchanged from TOGAF 9)
- ADM Techniques
- Applying the ADM
- Architecture Content
- Enterprise Architecture Capability and Governance

### TOGAF Series Guides

A modular, expandable library of topic-specific guidance, expected to update faster:

- Practitioner approaches and leader's guides
- Business Architecture, Information Architecture, the Technical Reference Model
- Integrating Risk and Security
- Enabling Enterprise Agility (the agile-EA guidance)
- Digital Technology Adoption
- Microservices Architecture
- Government Reference Model
- Organization Mapping, Value Streams, Business Capabilities, Business Models
- Others — the library expands over time

### Why the restructure

The recurring complaint with TOGAF (and frameworks generally): the framework is frozen for years while the world moves. TOGAF 9 → 9.1 → 9.2 → 10 spans 2009-2022 — thirteen years with the core largely stable, which is a strength (stability) and a weakness (slow to address agile, digital, cloud, AI). The Fundamental Content / Series Guide split lets the core stay stable (you do not have to relearn the ADM every few years) while topic guidance evolves quickly (agile-EA, digital-EA, security guidance can be updated without a full standard revision).

### What did not change in the 10th Edition

- The ADM phases (Preliminary, A-H, Requirements Management) — substantially the same as TOGAF 9.
- The content framework's deliverable / artifact / building-block structure.
- The Enterprise Continuum's generic-to-specific ordering.
- The Architecture Capability Framework's governance model.

The 10th Edition is a *re-packaging* with some content modernization, not a re-invention. Someone trained on TOGAF 9.x can take the bridge exam and is mostly current.

## Comparison: structure across versions

| Aspect | TOGAF 8 (2002) | TOGAF 9 (2009) | TOGAF 9.2 (2018) | 10th Edition (2022) |
|---|---|---|---|---|
| Scope | Enterprise (4 domains) | Enterprise (4 domains) | Enterprise (4 domains) | Enterprise (4 domains) |
| ADM | Yes | Yes (refined) | Yes (refined) | Yes (stable) |
| Content Framework | No | Yes (new) | Yes (simplified) | Yes (in Fundamental Content) |
| Capability Framework | Partial | Yes (formalized) | Yes | Yes (in Fundamental Content) |
| Enterprise Continuum | Partial | Yes (formalized) | Yes | Yes |
| Reference Models | TRM | TRM + III-RM | TRM + III-RM | TRM (in a Series Guide) |
| ArchiMate alignment | No | Loose | Closer | Maintained |
| Modular topic guides | No | No | TOGAF Library (nascent) | TOGAF Series Guides (full) |
| Agile-EA guidance | No | Minimal | Some | Yes (Series Guide) |

## Why each major version happened

- **TOGAF 8 (2002):** market shift. "Enterprise architecture" became the term of art; "IT architecture" was too narrow. TOGAF broadened to stay relevant.
- **TOGAF 9 (2009):** completeness. TOGAF 8 had a method (ADM) but no content framework, no formal capability framework, no formal continuum treatment. TOGAF 9 filled the gaps to make TOGAF a complete EA framework, not just a method.
- **TOGAF 9.2 (2018):** business-architecture pressure plus modeling alignment. Business architecture had matured as a discipline (BIZBOK); TOGAF needed to keep up. ArchiMate alignment reflected The Open Group's interest in a coherent method-plus-notation offering.
- **10th Edition (2022):** velocity. The thirteen-year stability of the core was both an asset and a liability. The Series Guide split decouples core stability from topic-guidance velocity.

## What the next revision will likely address

Speculative, with directional evidence:

- **AI-system architecture** — a Series Guide on architecting AI capabilities into the enterprise, governing AI-system risk, AI reference architectures. The Series Guide structure is built for exactly this kind of fast-moving topic.
- **Deeper agile-EA integration** — the "enabling team" / "minimum viable architecture" thinking maturing into more concrete guidance.
- **Cloud-native and platform-engineering patterns** — beyond the current microservices guide.
- **Sustainability architecture** — environmental impact as an architecture concern.
- **Tighter Open Agile Architecture (O-AA) integration** — The Open Group's separate agile-architecture standard converging with or feeding into TOGAF Series Guides.

Timing: the Fundamental Content is likely stable for years (the ADM has been substantially the same since 2009). Series Guides will be added and updated continuously — that is the point of the restructure. A "TOGAF 11" major version increment is not on any public roadmap.

## See also

- [[TOGAF Cluster|cluster MOC]] · [[TOGAF ADM]] · [[TOGAF Content Framework]] · [[TOGAF vs Other EA Frameworks]] · [[TOGAF Controversies]]
