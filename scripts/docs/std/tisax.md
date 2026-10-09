title: TISAX
summary: Map of TISAX (Trusted Information Security Assessment Exchange), the German-automotive-sector mechanism for information security assessment and result-sharing.
parent: index
order: 110
labels: automotive-compliance, moc, security-compliance, tisax
aliases: TISAX Cluster | TISAX | Trusted Information Security Assessment Exchange | VDA-ISA Cluster
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/tisax/TISAX Cluster.md
reviewed: no
---
> Map of TISAX (Trusted Information Security Assessment Exchange), the German-automotive-sector mechanism for information security assessment and result-sharing. Built on the VDA-ISA catalogue, operated by ENX Association, required by every major German OEM and tier-1 supplier. Sibling to ISO 27001 but with different mechanics (no "certification", labels via exchange registry, sector-specific scope). Reference cluster for any work touching German automotive supply chain.

## Anchors

- [position](pillars/tisax/position.md): current view, dated, revisable
- [anchors](pillars/tisax/anchors.md): primary documents, ENX, VDA, audit providers, named voices

## Provenance

- **VDA-ISA** (Information Security Assessment) — content authored by Verband der Automobilindustrie (VDA), the German automotive industry association. Originated as VDA's internal supplier-assessment questionnaire.
- **ENX Association** — operator, founded 2000 in Frankfurt originally for European Network Exchange (a managed-network service among automotive partners). Expanded into TISAX in 2017 as a neutral operator for cross-company assessment exchange.
- **TISAX launch** — 2017. Mandatory for VW Group suppliers from 2017, with other German OEMs (BMW, Mercedes-Benz / Daimler, Audi, Porsche) and tier-1 suppliers (Bosch, Continental, ZF, Schaeffler, Hella, Mahle) adopting through 2018-2020.
- **VDA-ISA versions** — 4.x (2017-2019), 5.0 (2020), 5.1 (2022), 6.0 (late 2023), 6.0.x maintenance updates. Each version moves the catalogue forward; current assessments use the most recent applicable version.
- **VDA-ISA 6.0 changes** — restructured to align with ISO 27001:2022 Annex A four-theme layout. Added AI / new-technology considerations. Expanded prototype protection criteria. Aligned data protection module with GDPR enforcement reality.

## What TISAX is, in one paragraph

TISAX is a sector-specific mechanism for information security assurance in the German automotive supply chain. Suppliers complete a self-assessment against the VDA-ISA catalogue, are audited by an ENX-accredited audit provider (at AL2 or AL3 levels), and have their results published as labels in the ENX exchange portal. OEMs and other prospective customers query the portal for supplier labels rather than running individual supplier audits. The mechanism is described as "trusted assessment exchange" rather than "certification" because no certificate is issued; the artefact is a registry entry with one or more labels and a validity period.

## How TISAX differs from ISO 27001 (one-page view)

| Aspect | ISO 27001 | TISAX |
|---|---|---|
| Standard owner | ISO / IEC (international) | VDA (DE automotive); ENX operates |
| Type of recognition | Certificate | Label in shared registry |
| Audit output | Certificate document | Assessment report (private) + label (registry) |
| Validity | 3 years (with 2 surveillance audits) | 3 years (no surveillance audits) |
| Scope flexibility | Org defines scope; SoA records | OEM specifies required labels; scope follows |
| Self-assessment role | Internal audit feeds external | Self-assessment is the explicit start of the process |
| Audit independence | Cert body accredited under 17021-1 | Audit provider accredited by ENX |
| Sector breadth | Cross-sector, universal | German automotive supply chain |
| Mandatory triggers | Procurement requirement (RFP) | OEM contract clause flowing down tiers |
| Result-sharing | Customer requests certificate | OEM queries ENX portal directly |
| Cost | €15-40k+ first cert (varies) | €5-15k typical audit + ENX participation fees |
| Coverage of controls | All Annex A (with SoA exclusions) | VDA-ISA catalogue (smaller, focused) |

Fuller comparison in [[TISAX vs ISO 27001]].

## VDA-ISA catalogue (the assessment criteria)

The VDA-ISA catalogue is the question set. Three modules:

- **Information Security** — the primary module. Required for most labels. Aligned with ISO 27001 Annex A controls but reshaped for automotive supplier context. ~40-50 controls in VDA-ISA 6.0.
- **Prototype Protection** — automotive-specific. Covers handling of pre-series components, prototypes, design data, test vehicles. Has its own controls for physical and logical protection of pre-release IP.
- **Data Protection** — GDPR alignment. Required when supplier processes personal data on behalf of OEM.

Each control is scored across **maturity levels 0-5** following an SPICE-style scale:

- **0 Incomplete** — control not implemented
- **1 Performed** — implemented informally, success depends on individual effort
- **2 Managed** — planned, tracked, verified
- **3 Established** — documented as part of standard org process
- **4 Predictable** — quantitatively managed
- **5 Optimizing** — continuously improved

Target maturity is typically **3** for AL2 / AL3 assessments. Some controls have higher target levels in specific scenarios.

Full per-control mapping is the VDA-ISA workbook (Excel format); see [[TISAX VDA-ISA Catalogue]].

## Assessment levels

Three levels, OEM-specified per supplier per label:

- **AL1** — self-assessment only. No audit. Plausibility self-declared. Not externally validated. Rare in practice; OEMs typically require AL2 or AL3.
- **AL2** — self-assessment + plausibility check by audit provider via remote interview / document review. Lower-effort, suits most non-critical labels.
- **AL3** — self-assessment + full on-site audit by audit provider. Required for high-risk labels (high or very high protection requirement, prototype protection at sensitive scope).

Detail in [[TISAX Assessment Levels]].

## Labels (the assessment objectives)

Suppliers obtain labels per assessment objective. Each label corresponds to a protection requirement level. Major label categories:

- **Information Security with High protection requirement** — standard label for confidential business information.
- **Information Security with Very High protection requirement** — highest tier, for strategic information.
- **Prototype Protection** — sub-labels for prototype components, vehicles, test environments.
- **Data Protection** — GDPR processing context. Additional sub-label for special-category personal data.
- **Connection to third parties** — when supplier accesses OEM networks.

OEM contract clauses specify which labels and which assessment level. Common patterns: AL2 + Info Sec High for most tier-2 suppliers; AL3 + Info Sec Very High + Prototype Protection for development partners.

Detail in [[TISAX Labels and Scopes]].

## Assessment process

End-to-end mechanics:

1. **Registration** with ENX (annual fee).
2. **Scope definition** — which sites, which OEM relationships, which labels.
3. **Self-assessment** using the VDA-ISA workbook.
4. **Audit provider selection** (TÜV SÜD, TÜV Rheinland, TÜV Nord, DEKRA, DQS, KPMG, Deloitte, BSI Germany, others).
5. **Audit conduct** (remote for AL2, on-site for AL3).
6. **Findings remediation** (minor findings ok; major must be addressed for label issuance).
7. **Label issuance** — published in ENX portal.
8. **Validity** — 3 years from successful audit completion.

Detail in [[TISAX Assessment Process]].

## Why this matters for SRE and AI-agent work

The cluster bears on multiple real concerns:

- **German automotive customers** — [employer]-class buyers, German Mittelstand manufacturing, any work touching the OEM supply chain triggers TISAX requirements via flow-down clauses.
- **Prototype protection mechanics** — atypical handling rules: air-gapped environments, restricted-access rooms, no-photo zones, time-bounded retention. SRE work touching prototype data faces unusual constraints.
- **AI-system handling of automotive data** — pre-series CAD, simulation results, test data — automotive sensitivity classifications often higher than general business data. AI tools that retain or train on inputs become problematic against prototype-protection criteria.
- **Audit provider capability for AI controls** — auditor depth varies; TISAX-side AI audit competence is patchier than the ISO 27001 ecosystem.
- **Solo / small-team consulting fit** — TISAX scope can be narrow (a single site, a single set of labels) making it more accessible than full ISO 27001 certification for small operations serving automotive clients.

## Stefan-context relevance

Stefan does SRE / staff-engineer-track work potentially touching:

- German manufacturing customers ([employer], broader Mittelstand consulting)
- Multi-tenant infrastructure where automotive supplier customer data might transit
- AI-agent systems consuming or producing customer-specific outputs that may contain confidential supply chain data

Cluster atoms should:

- Stay practitioner-grounded (named controls, named audit providers, named OEM clauses)
- Make the ISO 27001 / TISAX overlap and delta explicit
- Surface AI-system fit gaps the standard does not address
- Carry the SRE / AI-agent angle through Stefan's likely engagement paths

## Related clusters and atoms

- [[ISO 27001 Cluster|ISO 27001]] — the international sibling; controls overlap heavily but mechanics differ
- [[work-kb/business/index|work-kb business]] — client engagement context
- [[SRE/pillars/08-security/index|SRE Security pillar]] — operational security; TISAX is one audit layer

## Conventions for this cluster

- Atoms named `TISAX <Topic>.md` with consistent structure
- All atoms cite the relevant VDA-ISA version and section number where applicable
- Cross-reference ISO 27001 cluster atoms when the control is shared
- Mark VDA-ISA 6.0 changes explicitly where they shift practitioner expectation

## See also

[[TISAX Cluster]] (pillars MOC) · [position](pillars/tisax/position.md) · [anchors](pillars/tisax/anchors.md) · [[ISO 27001 Cluster]]
