title: ITIL position
summary: Current view on what ITIL 4 is good for, what it is not good for, and where it sits as a service-management framework.
parent: itil
order: 5
labels: itil, position
aliases: ITIL Position | ITIL Current View
type: position
created: 2026-05-12
updated: 2026-05-12
origin: pillars/itil/position.md
reviewed: no
---
> Current view on what ITIL 4 is good for, what it is not good for, and where it sits as a service-management framework. Dated, revisable, diff-tracked.

## State of the view as of 2026-05-12

### What ITIL 4 does well

- **Shared vocabulary across enterprise IT.** Words like "incident", "problem", "change", "service level" have ITIL-derived meanings in most enterprise contexts. Adoption of the vocabulary reduces translation cost between teams, vendors, and auditors.
- **Structure for service-management capability.** The 34 practices provide a reasonably complete enumeration of what an IT-service-providing organization needs to do. New leaders can map their gaps against the practice list.
- **Holistic framing via the SVS.** The Service Value System reframed ITIL from a process-heavy lifecycle to a value-creation-oriented operating model. The shift is real and substantive; it explicitly accommodates Agile, DevOps, Lean, and customer-centricity.
- **Guiding Principles are durable.** Focus on value, start where you are, progress iteratively, collaborate, think holistically, keep it simple, optimize and automate — these are widely-applicable beyond service management. They survive translation outside IT.
- **Customer-centric value framing.** Value is co-created with consumers; the provider does not define value unilaterally. The shift from v3's "service provider" framing to ITIL 4's "service relationship" framing is conceptually cleaner.
- **Practice-level granularity supports targeted adoption.** Organizations adopt the practices that match their needs without ingesting the whole framework.
- **High-Velocity IT module reaches toward DevOps / SRE.** ITIL 4's explicit acknowledgment that traditional change-management can stifle high-velocity delivery is a real concession.

### What ITIL 4 does poorly

- **Process-heaviness lineage persists.** Despite the SVS reframe, many organizations implement ITIL 4 as if it were ITIL v3: a process-centric, document-heavy, ticket-system-mediated operating model. The framework allows leaner adoption; practitioner culture often does not.
- **Bureaucratization risk.** "Change Advisory Board" implementations across the industry have produced multi-week change-approval cycles for low-risk changes. ITIL 4's Change Enablement practice explicitly criticizes this pattern, but the cultural inertia is real.
- **Tooling capture.** Service-management tooling (ServiceNow, Jira Service Management, BMC Helix, Ivanti, others) has shaped what "doing ITIL" looks like in practice more than the framework itself has. Tool-driven implementations sometimes diverge from framework intent.
- **Certification mill problem.** The certification scheme generates significant revenue for PeopleCert and training partners. Certificate-counting in CVs and procurement signals incentivizes credential acquisition over capability development. The Foundation exam in particular is widely regarded as memorization-driven rather than capability-validating.
- **AI / autonomous operations gaps.** ITIL 4 acknowledges AI in passing. The deeper questions — how do incidents get classified when an agent generated them, how do problem investigations work when the failure mode is in model behavior, how does SLO definition work for inherently-non-deterministic systems — are not addressed in depth.
- **High-Velocity IT module is partial.** HVIT acknowledges DevOps / SRE but does not fully reconcile with them. The SRE community treats ITIL as adjacent but rarely as integrated; ITIL practitioners treat SRE similarly.
- **Practice-list completeness varies.** Some practices (Knowledge Management, Service Catalogue Management, IT Asset Management) are thinly described relative to their real complexity; others (Incident Management, Change Enablement, Service Level Management) are over-prescriptive.
- **English-language and Anglosphere bias.** Original UK-origin context shapes terminology in ways that translate awkwardly outside English-speaking and ISO-adjacent contexts.

### Where the evidence currently sits

- **ITIL adoption is enterprise-wide.** Most Fortune 500 IT departments use some version of ITIL. Penetration declines in younger, more SaaS-native organizations but remains substantial among regulated industries (finance, healthcare, government, defence).
- **Certification volume is significant.** PeopleCert reports millions of certifications worldwide cumulatively. Foundation-level certificates particularly common in IT-services workforces.
- **DevOps / SRE has displaced ITIL in some pockets.** Tech-native organizations (Google, Netflix, smaller SaaS) often use SRE / DevOps terminology without explicit ITIL framing. Enterprise IT departments serving these orgs as customers still use ITIL.
- **Tool dominance shapes practice.** ServiceNow's dominance (60-70% of enterprise IT-service-management tooling market) means that "doing ITIL" in practice often means "configuring ServiceNow per its opinionated ITIL implementation." Framework intent and tool implementation are not always the same.
- **AIOps and AI assistants are reshaping practices.** AI-assisted incident classification, AI-generated change-impact analysis, AI-suggested problem investigations are entering operations. ITIL 4's 2023 refresh acknowledges but does not formally integrate these.
- **ITIL 4 → ITIL 5?** No public roadmap for ITIL 5 as of 2026. PeopleCert's pattern is incremental refresh (2023, 2025 maintenance updates expected) rather than major version increments. The 2019 ITIL 4 shift was substantial enough that further major shifts are unlikely soon.

## Personal calibration

- **Working assumption for enterprise engagements:** ITIL vocabulary will be load-bearing. Speak it accurately. Avoid both evangelism and dismissal.
- **Working assumption for SRE-adjacent enterprise work:** bridge ITIL and SRE vocabulary explicitly. SLO ↔ Service Level Management. Error budget ↔ continual improvement input. Postmortem ↔ Problem Management. Toil reduction ↔ Optimize and automate guiding principle.
- **Working assumption for AI-system operations:** ITIL practices need adaptation, not wholesale replacement. Monitoring and Event Management, Incident Management, Problem Management, Service Level Management all need AI-system-specific tailoring. Build the tailoring; don't pretend ITIL covers it.
- **Working assumption for own credentialing:** ITIL Foundation is procurement-recognized and a reasonable bar; higher-tier certifications have diminishing returns vs hands-on practitioner work for SRE-track work. Worth holding Foundation; not worth chasing Master.
- **Working assumption for small / solo operations:** ITIL as scaffolding, not as ceremony. Adopt vocabulary and the seven guiding principles; skip the ticket-system-heavy operational layer that assumes enterprise scale.

## What would shift this view

- **Major ITIL 5 release** with substantively rebuilt AI / autonomous-operations content would shift the framework's relevance for AI-system operations.
- **PeopleCert governance changes** affecting certification quality or content openness. PeopleCert is a private company; framework ownership concentration is a long-term concern.
- **A widely-adopted competing service-management framework** emerging (currently nothing matches ITIL's scope). VeriSM had a moment 2018-2020 but did not displace.
- **DevOps / SRE communities adopting ITIL terminology** rather than running parallel. Slow drift in this direction since 2019 but not decisive yet.

## See also

- [[ITIL Cluster|cluster MOC]] · [[ITIL Controversies]]
- [anchors](pillars/itil/anchors.md)
