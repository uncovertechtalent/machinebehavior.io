title: ITIL Version History
summary: Evolution from CCTA Government Information Technology Infrastructure Method (1989) through ITIL v2, v3, v3 2011 refresh, ITIL 4 (2019), to the 2023 PeopleCert refresh.
parent: itil
order: 100
labels: cross-cutting, itil
aliases: ITIL History | ITIL Version Evolution | ITIL v1 v2 v3 4
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/itil/ITIL Version History.md
reviewed: no
---
> Evolution from CCTA Government Information Technology Infrastructure Method (1989) through ITIL v2, v3, v3 2011 refresh, ITIL 4 (2019), to the 2023 PeopleCert refresh. Why each major version happened, what structurally changed, what the practical shifts meant.

## CCTA origin (1986-1989)

The UK Central Computer and Telecommunications Agency (CCTA) — part of HM Treasury — developed a set of recommendations to standardize IT operations across UK government departments. Originally called the **Government Information Technology Infrastructure Method (GITIM)**.

Renamed to **Information Technology Infrastructure Library (ITIL)** around 1989. First books published 1989-1996.

Drivers:

- Rising IT costs across UK government in the 1980s
- Inconsistent IT operations across departments
- Need for procurement-comparison criteria
- Influence of Edwards Deming and TQM thinking on UK government management

## ITIL v1 (1989-1996)

Approximately 40 books published over seven years. Organized by topic area:

- Service Support (Problem Management, Change Management, etc.)
- Service Delivery (Capacity, Availability, etc.)
- Software Lifecycle
- Computer Operations
- Management of Customer Relationships
- Many topic-specific publications

Adoption: UK government departments. Some early adoption among UK and Commonwealth private-sector organizations.

Style: process-oriented, detailed, function-centric.

## ITIL v2 (2000-2004)

Consolidated v1's ~40 books into ~10 books grouped around two core domains:

- **Service Support** — Service Desk, Incident Management, Problem Management, Configuration Management, Change Management, Release Management
- **Service Delivery** — Service Level Management, Availability Management, Capacity Management, IT Service Continuity Management, Financial Management for IT Services

Additional books covered Security Management, Application Management, ICT Infrastructure Management, Planning to Implement Service Management.

This was the version that gained meaningful international adoption. Many enterprise IT departments aligned to v2 in the early 2000s.

Style: process-centric, with explicit process definitions (purpose, scope, basic concepts, sub-processes, roles, KPIs).

Owning body shift: CCTA dissolved in 2001; ownership passed to the Office of Government Commerce (OGC).

## ITIL v3 (2007)

Significant restructure. Replaced the v2 two-domain organization with a **service lifecycle**:

- **Service Strategy** — strategic management, demand management, financial management for IT services, business relationship management
- **Service Design** — service catalogue management, service level management, capacity management, availability management, IT service continuity management, information security management, supplier management
- **Service Transition** — change management, release and deployment management, service validation and testing, service asset and configuration management, knowledge management
- **Service Operation** — event management, incident management, problem management, request fulfillment, access management, plus four functions (service desk, technical management, IT operations management, application management)
- **Continual Service Improvement** — 7-step improvement process, service measurement, service reporting

**26 processes + 4 functions** organized across the five lifecycle phases.

Driver for v3: v2's two-domain organization felt incomplete; the industry wanted a holistic lifecycle view. Influence of business process management, value-stream thinking, and quality management (Deming PDCA, Six Sigma).

Adoption: v3 became the de facto enterprise IT-service-management framework. Penetration into Fortune 500 IT departments was near-universal by 2010.

## ITIL v3 2011 refresh

Minor revision in 2011. Same five-book / five-lifecycle structure. Improvements:

- Clarification of process descriptions
- Addition of Strategy Management for IT Services as a v3 Service Strategy process (had been less-explicit in 2007)
- Addition of Business Relationship Management as a v3 Service Strategy process
- Minor renumbering and renaming

Not a major version increment. Most "ITIL v3" references in 2012-2018 mean the 2011 refresh content.

## ITIL 4 (2019)

Major restructure announced in 2018, published 2019. Owning body: AXELOS (joint venture of UK Cabinet Office and Capita, formed 2013).

Driver: v3's process-centric, lifecycle-organized model was increasingly mismatched with Agile, DevOps, cloud-native, and customer-centric practice. Practitioner pushback. Risk of irrelevance to younger, faster-moving organizations.

### Structural changes from v3 to ITIL 4

- **Lifecycle dropped.** v3's Service Strategy → Design → Transition → Operation → CSI sequence replaced by the **Service Value System (SVS)**, a network of components rather than a sequence.
- **Service Value Chain (SVC)** introduced — six interconnected activities (Plan, Improve, Engage, Design & Transition, Obtain/Build, Deliver & Support) rather than a five-stage lifecycle.
- **Processes + functions** collapsed into **34 practices** organized in three categories (General Management 14, Service Management 17, Technical Management 3).
- **Seven Guiding Principles** lifted from ITIL Practitioner (2016) and made central.
- **Four Dimensions of Service Management** introduced — Organizations & People, Information & Technology, Partners & Suppliers, Value Streams & Processes.
- **Agile, Lean, DevOps integration** explicit in terminology and recommendations. High-Velocity IT module specifically addresses DevOps / SRE integration.
- **Customer-centric value framing** — value co-created with consumers; service-relationship framing rather than service-provider framing.
- **Practice-level granularity** — each of the 34 practices described independently, allowing selective adoption.
- **Looser tooling assumptions** — less prescriptive about specific tooling shapes than v3 had become.

### Certification scheme change

- v3: Foundation, Intermediate (multiple modules), Expert, Master.
- ITIL 4: Foundation, Managing Professional, Strategic Leader, Master (different module structure).

Bridging credentials offered for v3-certified practitioners moving to ITIL 4.

### Adoption pattern

- Existing v3-trained workforces continued operating under v3 vocabulary; gradual migration to ITIL 4 vocabulary over 2019-2023.
- New adoption typically went directly to ITIL 4.
- Tooling vendors (ServiceNow, Jira SM) added ITIL 4 alignment to existing v3-aligned product features.

## 2021: PeopleCert acquisition of AXELOS

PeopleCert acquired AXELOS in 2021. ITIL ownership transferred to PeopleCert along with PRINCE2, MSP, and adjacent IP.

Implications:

- Consolidation of best-practice IP under a single private company
- Concentration of certification revenue stream
- Some practitioner concern over governance and openness
- No immediate change to framework content; ongoing maintenance continued

## ITIL 4 2023 refresh

Practice Manager stream and Master capstone refreshed. Practice content updated to reflect:

- Cloud-native operations maturity
- DevOps / SRE integration patterns
- AI / ML / AIOps adoption
- Sustainability considerations (new ITIL 4 Specialist module)

Not a major version increment; framework structure preserved.

PeopleCert also introduced Continuing Professional Development (CPD) renewal requirements for certifications, replacing the earlier "lifetime" certification model.

## Comparison: structure across versions

| Aspect | v1 | v2 | v3 (2011) | ITIL 4 |
|---|---|---|---|---|
| Number of core books | ~40 | ~10 | 5 (core) | 1 Foundation + multiple modules |
| Organizing model | Topics | Two domains (Support / Delivery) | Five-phase lifecycle | Service Value System (network) |
| Process count | n/a | ~14 | 26 + 4 functions | 34 practices |
| Customer framing | Provider-focused | Provider-focused | Provider-focused | Relationship-focused |
| Agile / DevOps integration | None | Minimal | Limited | Explicit |
| AI / automation integration | None | None | None | Explicit |
| Owning body | CCTA | OGC | OGC / AXELOS (2013+) | AXELOS / PeopleCert (2021+) |

## Why each major version happened

- **v1 (1989-1996):** standardize UK government IT operations. Driver: cost and consistency.
- **v2 (2000-2004):** international adoption needed simpler structure. Driver: usability for non-government adopters.
- **v3 (2007):** holistic lifecycle view demanded by industry. Driver: business process management influence and quality movement maturation.
- **v3 2011:** incremental clarifications. Driver: practitioner feedback on v3 ambiguities.
- **ITIL 4 (2019):** existential modernization. Driver: Agile / DevOps / cloud-native displacement risk; v3 was becoming "the framework that DevOps people work around."
- **2023 refresh:** content currency. Driver: cloud / DevOps / AI maturation since 2019; practice depth gaps.

## What the next revision will likely address

Speculative, based on directional evidence:

- **AI-system service management as first-class content.** Current ITIL 4 acknowledges AI; future revision likely incorporates dedicated practices or module for AI / agent operations.
- **Sustainability deepening.** ITIL 4 Specialist: Sustainability already exists; broader integration expected.
- **Further DevOps / SRE convergence.** HVIT module is a partial bridge; deeper integration plausible.
- **AIOps and machine-assisted operations.** Tooling has moved faster than framework guidance.
- **Hybrid / multi-cloud as default assumption.** ITIL 4 acknowledges cloud; further normalization expected.

Timing: PeopleCert's pattern is incremental refresh rather than major version increments. ITIL 5 plausibly 2027-2030 if it happens; refresh continuation more likely.

## Practical implications of version history

- **Vocabulary mixing in workforces.** Long-tenured IT practitioners often mix v2, v3, and ITIL 4 vocabulary. "Change Management" (v3) and "Change Enablement" (ITIL 4) used interchangeably.
- **Tooling vintage.** Many enterprise ITSM tools have v3-aligned defaults; "doing ITIL" via tooling often means doing v3-vintage practice with ITIL 4 vocabulary.
- **Certification vintage variance.** Practitioners certified in v3 era hold lifetime-equivalent certs (pre-2023 PeopleCert change) and may not have updated to ITIL 4 terminology.

## See also

- [[ITIL Cluster|cluster MOC]] · [[ITIL 4 Service Value System]] · [[ITIL 4 Practices]] · [[ITIL Controversies]]
- [anchors](pillars/itil/anchors.md)
