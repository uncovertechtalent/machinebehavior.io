title: TISAX position
summary: Current view on what TISAX is good for, what it is not good for, and where it sits as a procurement mechanism vs a security practice.
parent: tisax
order: 5
labels: position, tisax
aliases: TISAX Position | TISAX Current View
type: position
created: 2026-05-12
updated: 2026-05-12
origin: pillars/tisax/position.md
reviewed: no
---
> Current view on what TISAX is good for, what it is not good for, and where it sits as a procurement mechanism vs a security practice. Dated, revisable, diff-tracked.

## State of the view as of 2026-05-12

### What TISAX does well

- **Industry-coordinated assurance.** TISAX removes the redundant individual-OEM audit problem. Before TISAX, a tier-2 supplier serving VW, BMW, and Daimler ran three nearly-identical audits. Now: one assessment, three customer queries to the same ENX registry entry.
- **Sector-tailored scope.** Prototype protection is a real automotive-specific need; ISO 27001 has no native equivalent. Data protection module addresses GDPR explicitly. Information security module is tighter and more applicable than the full Annex A for an automotive supplier.
- **Self-assessment as first-class.** The VDA-ISA workbook is a usable internal-assessment tool whether or not the supplier proceeds to external audit. Maturity-level scoring is more actionable than yes / no controls.
- **Lower entry cost than full ISO 27001.** €5-15k typical audit + €1-5k ENX participation fees per cycle, plus internal effort. Reachable for mid-size suppliers that would struggle with full ISO 27001 certification.
- **Maturity model embedded.** SPICE-style 0-5 scoring per control creates an improvement trajectory rather than binary compliance. Target levels per control prevent over-implementation in low-importance areas.
- **No surveillance audits during the three-year cycle.** Cost predictability across the validity period.

### What TISAX does poorly

- **Closed ecosystem.** TISAX results are only visible to authorized customers via ENX portal. The label has no value outside the automotive supply chain. Non-automotive customers do not recognize it.
- **No public-facing certificate.** The supplier cannot post a "TISAX certified" logo to website or marketing material the way ISO 27001 certificates appear. The recognition is private to OEM-supplier procurement.
- **Limited audit-provider diversity.** Concentrated among large TÜV / DEKRA / Big-Four firms with German-market focus. Smaller specialist auditors absent.
- **Auditor variance.** Same problem as ISO 27001. Inter-auditor reliability not measured publicly. Practitioner reports describe wide variance between audit providers and between auditors within providers.
- **AI-system fit gaps.** VDA-ISA 6.0 (late 2023) acknowledged AI in passing but does not provide deep controls for autonomous-agent operations, prompt-injection threats, or model-vendor relationships. Catalogue-revision cycle is faster than ISO but still lags AI-system maturity.
- **Document-heavy.** Reaching maturity level 3 (documented, established) on the full catalogue requires substantial documentation, similar to ISO 27001 Cl 7.5.
- **Hard to scope down.** OEMs specify labels per supplier relationship; supplier cannot unilaterally narrow scope the way an ISO 27001 SoA permits. If OEM requires Info Sec Very High, supplier must implement at that level even if internal risk assessment would have set the bar lower.
- **Geographic limitation.** Recognized within DE automotive supply chain and EU automotive extensions. Less recognized in US (Detroit, EV-newcomer), Japanese, Korean, or Chinese OEM supply chains, which have their own preferred frameworks.

### Where the evidence currently sits

- **Procurement-mandate adoption is near-universal in German auto.** All major German OEMs (VW Group, BMW, Mercedes-Benz, Audi, Porsche) and tier-1 suppliers (Bosch, Continental, ZF, Schaeffler, Hella, Mahle, Brose) require TISAX from suppliers. New supplier contracts include TISAX flow-down clauses. Existing relationships have grace periods that have largely expired.
- **VDA-ISA 6.0 adoption** — current assessments use 6.0.x. Pre-existing labels obtained under 5.1 remain valid until original three-year expiry, but renewals run against current catalogue.
- **TISAX vs ISO 27001 dual implementation.** Suppliers serving German auto + broader market run both. Implementation overlaps 70-80%. Audits remain separate.
- **AI handling pressure.** OEMs have begun adding contract clauses around AI tool use (employee use, code-generation, customer-data inputs to models). VDA-ISA controls have not caught up; suppliers handle via internal policy + contractual representations.
- **ENX-portal accuracy.** Procurement teams at OEMs increasingly check the registry directly. Spoofing or claiming labels that are not in the registry is detected quickly.
- **Audit conduct shift since pandemic.** AL2 remote audits matured during 2020-2022. AL3 mostly returned to on-site by 2023; some hybrid (one on-site visit + remote follow-up) accepted by audit providers.

## Personal calibration

- **Working assumption for clients touching German auto:** TISAX requirements will flow down whether or not the client recognizes them yet. Plan accordingly when scoping any engagement with automotive-customer exposure.
- **Working assumption for prototype data:** if the engagement touches any pre-release CAD, design data, simulation outputs, or test data, prototype-protection controls (air-gapped or strongly-segregated environments, restricted access, no-AI-tool retention) apply regardless of formal label requirement.
- **Working assumption for AI tooling in automotive scope:** model-vendor data-handling commitments must be verifiable to the level the OEM contract requires. Default models with training-data-use defaults are not acceptable; enterprise tiers with no-retention DPAs are. Configure agent systems accordingly when serving automotive customers.
- **Working assumption for own-positioning:** TISAX is not currently a personal investment. Approach surfaces when an engagement requires it. ISO 27001 alignment plus client-specific TISAX-compatible practice is the working position.

## What would shift this view

- **A major German OEM publishing AI-handling clauses with sharp teeth.** Once VW or BMW issues contract addenda specifying which AI tools are allowed and which are not, supplier-side practice converges fast.
- **VDA-ISA AI module release.** ENX / VDA have signalled interest. An explicit AI control set would shift the implementation work into TISAX scope rather than informal supplier-policy.
- **Cross-recognition between TISAX and ISO 27001.** Currently each is independent; bilateral or unilateral recognition would reduce dual-audit overhead. Not actively in progress as of 2026.
- **TISAX outside automotive.** Aerospace, defence, or industrial-machinery sectors adopting a similar ENX-style exchange would expand the model's reach. Not visible in 2026.

## See also

- [[TISAX Cluster|cluster MOC]] · [[TISAX vs ISO 27001]] · [[TISAX Controversies]]
- [anchors](pillars/tisax/anchors.md)
