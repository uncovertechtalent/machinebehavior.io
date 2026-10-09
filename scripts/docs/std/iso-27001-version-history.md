title: ISO 27001 Version History
summary: Evolution from BS 7799 (1995) through ISO/IEC 27001:2005, :2013, and :2022.
parent: iso-27001
order: 100
labels: cross-cutting, iso-27001
aliases: ISO 27001 History | BS 7799 History | ISO 27001 Version Evolution | ISO 27001 2013 vs 2022
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Version History.md
reviewed: no
---
> Evolution from BS 7799 (1995) through ISO/IEC 27001:2005, :2013, and :2022. Why each revision happened, what structurally changed, what the practical implementation shifts were, and the transition mechanics that move certified organizations forward.

## The BS 7799 origin (1995-2005)

### BS 7799-1:1995 — Code of practice

UK Department of Trade and Industry (DTI) published Part 1 in February 1995. A code-of-practice document drawn from contributions by UK industry leaders (BT, Shell, Marks & Spencer, others). Not a certifiable standard at this stage — a list of recommended practices.

Roughly 100 controls, organized by topic area. Foundational for the Annex A lineage.

### BS 7799-2:1999, revised 2002 — Specification

Added the auditable specification side. Defined a documented "shall"-style management system for InfoSec. PDCA (Plan-Do-Check-Act) cycle baked in. This is the direct ancestor of ISO 27001 clauses.

UKAS-accredited certification scheme launched against BS 7799-2:2002. By the time of ISO adoption, several thousand UK-based certificates existed.

### ISO/IEC 17799:2000

ISO/IEC 17799:2000 published as ISO equivalent of BS 7799-1 (code of practice). Updated to 17799:2005.

## ISO/IEC 27001:2005 — First ISO version

Published October 2005. Renamed BS 7799-2:2002 to ISO/IEC 27001:2005, with revisions.

Structure: 8 clauses (Cl 4-8) plus Annex A of 133 controls organized in 11 clauses (A.5 through A.15).

PDCA cycle explicit in the clause structure:

- Plan (4.2.1 — establish ISMS, identify risks, select controls)
- Do (4.2.2 — implement)
- Check (4.2.3 — monitor and review)
- Act (4.2.4 — maintain and improve)

ISO/IEC 17799:2005 was the controls implementation companion. Renumbered to ISO/IEC 27002:2005 in 2007 for family-naming consistency.

## ISO/IEC 27001:2013 — Annex SL alignment

Published October 2013. Major restructure to adopt **Annex SL** — the harmonized high-level structure shared with ISO 9001 (quality), 14001 (environmental), 22301 (BC), and other management system standards.

### Structural changes

- **PDCA dropped from the standard wording.** PDCA-as-implementation-pattern persisted but the standard no longer mandated the cycle structure verbatim. Annex SL clauses (Cl 4-10) became the structure: Context, Leadership, Planning, Support, Operation, Performance evaluation, Improvement.
- **Annex A restructured.** 133 controls → 114 controls in 14 categories (A.5 through A.18). New / consolidated controls. Mobile devices and teleworking added (A.6.2). Cryptography elevated to its own category (A.10).
- **Risk methodology decoupled.** :2005 required a specific risk-assessment approach (asset-threat-vulnerability with specific calculation). :2013 only required "a risk assessment process" meeting general criteria — letting orgs use FAIR, NIST 800-30, ISO 27005, or anything that produced consistent, valid, comparable results.
- **Documented information generalized.** ":2005" specified "records" and "documents" separately. ":2013" merged them into "documented information," reducing terminology overhead.
- **Statement of Applicability strengthened.** Mandatory artefact for the certification audit.

### Transition

Transition from :2005 to :2013 was a two-year window from October 2013. Certificates against :2005 ceased to be valid after October 2015.

## ISO/IEC 27001:2022 — Controls modernization

Published 25 October 2022. Mandatory clauses (Cl 4-10) largely unchanged from :2013. Major change is Annex A, driven by the publication of ISO/IEC 27002:2022 in February 2022.

### Annex A changes

- **Control count:** 114 → 93. Net reduction via consolidation.
- **Structure:** 14 categories (A.5-A.18) → 4 themes (A.5 Organizational 37, A.6 People 8, A.7 Physical 14, A.8 Technological 34).
- **Eleven new controls:**
  - A.5.7 Threat intelligence
  - A.5.23 Information security for use of cloud services
  - A.5.30 ICT readiness for business continuity
  - A.7.4 Physical security monitoring
  - A.8.9 Configuration management
  - A.8.10 Information deletion
  - A.8.11 Data masking
  - A.8.12 Data leakage prevention
  - A.8.16 Monitoring activities
  - A.8.23 Web filtering
  - A.8.28 Secure coding
- **57 controls merged into 24.** Reduction without functional loss.
- **One control split into two.** A.18.1.3 (protection of records) and A.18.1.4 (protection of PII) became A.5.33 and A.5.34 respectively, decoupled from the legal-and-compliance category.
- **Five attribute axes added in 27002:2022.** Each control labelled across:
  - Control type (preventive / detective / corrective)
  - Information security properties (confidentiality / integrity / availability)
  - Cybersecurity concepts (identify / protect / detect / respond / recover — aligned with NIST CSF)
  - Operational capabilities (governance, asset management, identity and access management, ...)
  - Security domains (governance and ecosystem / protection / defense / resilience)

### Mandatory-clause changes

Mostly editorial (Annex SL refinement):

- **Cl 4.2.c added** — explicit requirement to determine which interested-party requirements are addressed through the ISMS.
- **Cl 4.4 expanded** — "processes needed and their interactions."
- **Cl 6.2 added** monitored and documented-information sub-items.
- **Cl 6.3 Planning of Changes added** — new clause for planned ISMS changes.
- **Cl 8.1 final sentence** — explicit obligation to control externally provided processes.
- **Cl 9.3.2 expanded** — changes-in-interested-party-needs added as explicit management-review input.
- **Cl 10 sub-clauses reordered** — 10.1 Continual improvement, 10.2 Nonconformity and corrective action (reverse of :2013).
- **Standard title updated** — adds "cybersecurity and privacy protection."

### Transition

Transition window: three years from publication. Certificates against :2013 ceased to be valid after **31 October 2025**.

As of 2026-05-12, the transition window has closed. New certifications and recertifications must be against :2022. Surveillance audits of certificates issued just before the deadline continue under :2022 wording.

### What the :2022 revision did not address

- **AI / agent systems** — no AI-specific controls in Annex A. Threat intelligence (A.5.7), configuration management (A.8.9), monitoring (A.8.16), and secure coding (A.8.28) cover parts of the problem incidentally. ISO 42001 (December 2023) is the dedicated AI management system standard.
- **Post-quantum cryptography** — A.8.24 (use of cryptography) does not specify post-quantum migration planning. Implied by general "appropriate cryptography" requirements; not enforced.
- **Software supply chain (SLSA / SBOM)** — A.5.21 (ICT supply chain) covers, but at policy level only. Operational guidance lives outside the standard.

## Comparison: structure across versions

| Aspect | :2005 | :2013 | :2022 |
|---|---|---|---|
| Mandatory clauses | 4-8 | 4-10 | 4-10 |
| Annex A controls | 133 | 114 | 93 |
| Annex A structure | 11 categories | 14 categories | 4 themes |
| PDCA explicit | Yes | No | No |
| Risk methodology | Prescribed | General | General |
| Documented information | Separate | Merged | Merged |
| Annex SL aligned | Partial | Yes | Yes |
| Cloud controls explicit | No | No | Yes (A.5.23) |
| AI controls explicit | No | No | No |
| Title scope | InfoSec | InfoSec | InfoSec + cyber + privacy |

## Comparison: Annex A category-to-theme mapping (:2013 → :2022)

| :2013 Category | :2022 Theme(s) |
|---|---|
| A.5 Information security policies | A.5 Organizational |
| A.6 Organization of information security | A.5 Organizational + A.6 People (mobile / teleworking) |
| A.7 Human resource security | A.6 People |
| A.8 Asset management | A.5 Organizational |
| A.9 Access control | A.5 Organizational + A.8 Technological |
| A.10 Cryptography | A.8 Technological |
| A.11 Physical and environmental security | A.7 Physical |
| A.12 Operations security | A.8 Technological |
| A.13 Communications security | A.8 Technological |
| A.14 System acquisition, development and maintenance | A.8 Technological |
| A.15 Supplier relationships | A.5 Organizational |
| A.16 Information security incident management | A.5 Organizational |
| A.17 Business continuity (info sec aspects) | A.5 Organizational |
| A.18 Compliance | A.5 Organizational |

The :2022 themes are cross-cutting; many :2013 categories distribute across themes. Re-mapping the SoA at transition is a one-time effort but non-trivial.

## Why each revision happened

- **:2005:** internationalization of BS 7799. The driver was procurement: UK-only certification limited supplier acceptance internationally; ISO publication broadened it.
- **:2013:** Annex SL harmonization. Organizations operating multiple management systems (9001 + 27001 + 14001 + ...) needed a consistent management-system structure. Driver was implementation cost, not security maturity.
- **:2022:** controls modernization. Cloud computing matured between :2013 and :2022; threat intelligence, DLP, secure coding emerged as standard practice; Annex A had drifted from current operational reality. ISO/IEC 27002:2022 was rewritten first; 27001:2022 followed to reference the new Annex A structure.

## What the next revision will likely address

Speculative, but with directional evidence:

- **AI-system controls** — either Annex A additions or explicit integration guidance with ISO 42001.
- **Post-quantum cryptography migration planning** — explicit clause or A.8.24 expansion.
- **Software supply chain (SLSA, SBOM, signed artefacts)** — more operational A.5.21 / A.8.30 wording.
- **Privacy convergence** — possible deeper 27001 / 27701 integration as GDPR-equivalent regulations proliferate globally.
- **Continuous compliance / automated control evidence** — pressure from cloud-native operations to support continuous assurance rather than point-in-time audit.

Timing: typical ISO revision cycle is 5-10 years. Next revision plausibly 2028-2032.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Certification Process]] · [[ISO 27001 Family and Sector Variants]] · [[ISO 27001 Controversies]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.6 People Controls]] · [[ISO 27001 Annex A.7 Physical Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
