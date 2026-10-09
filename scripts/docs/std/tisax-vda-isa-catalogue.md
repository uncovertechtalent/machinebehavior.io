title: TISAX VDA-ISA Catalogue
summary: The control set against which TISAX assessments are conducted.
parent: tisax
order: 100
labels: tisax, tisax-catalogue
aliases: VDA-ISA Catalogue | VDA-ISA 6.0 | TISAX Controls | TISAX Catalogue
type: tisax-catalogue
created: 2026-05-12
updated: 2026-06-08
origin: pillars/tisax/TISAX VDA-ISA Catalogue.md
reviewed: no
---
> The control set against which TISAX assessments are conducted. Authored by VDA, current major version VDA-ISA 6.0 (late 2023) with maintenance updates. Three modules, maturity-level scoring per control, OEM-specified protection requirements per label.

## Catalogue structure

The VDA-ISA workbook is an Excel-format spreadsheet containing three modules:

- **Information Security** — primary module, required for most TISAX labels.
- **Prototype Protection** — automotive-specific, required when handling pre-series components or design data.
- **Data Protection** — GDPR-aligned, required when processing personal data on behalf of OEM.

Each control row in the catalogue contains:

- Control number and title
- Control objective
- Reference to applicable ISO 27001 Annex A control (where mapping exists)
- Maturity-level criteria (per level 0-5)
- Notes and clarifications
- Self-assessment scoring fields
- Auditor scoring fields
- Comments and evidence reference fields

## Maturity levels (SPICE-style 0-5)

Each control is scored across the same six maturity levels:

- **0 — Incomplete** — control not implemented or partially implemented in an ad-hoc way that does not meet the objective.
- **1 — Performed** — control implemented and meets the objective, but informally; depends on individual effort. No process discipline.
- **2 — Managed** — control planned, tracked, verified. Process exists. Outcomes consistent.
- **3 — Established** — control documented as part of standard organizational process. Tailored from a standard. Consistent across the org.
- **4 — Predictable** — control quantitatively managed. Performance is measured, statistically controlled, and predictable.
- **5 — Optimizing** — control continuously improved based on quantitative feedback.

**Target maturity is typically 3** for AL2 and AL3 assessments. The OEM-specified protection requirement determines whether a higher target applies to specific controls.

Maturity-level criteria are defined per control; reaching level 3 on control X may require different evidence than level 3 on control Y. The workbook provides the per-control criteria.

## Information Security module

The largest module. Aligned with ISO/IEC 27001:2022 Annex A four-theme layout in VDA-ISA 6.0:

- **Organizational controls** — policies, roles, asset management, classification, supplier relationships, incident management, regulatory compliance.
- **People controls** — screening, awareness, employment terms, post-employment obligations.
- **Physical controls** — perimeter, entry, environmental, equipment, off-premises, disposal.
- **Technological controls** — endpoints, access, malware, vulnerability, configuration, deletion, masking, DLP, backup, logging, monitoring, network, cryptography, SDLC, secure coding, change management.

Control count varies slightly between VDA-ISA versions but is in the 40-50 range overall — narrower than ISO 27001's 93 Annex A controls. The catalogue selects controls considered automotive-supplier-relevant and folds related controls together.

Headline controls (illustrative, not the full list):

- Information security policy
- Information security responsibilities
- Asset inventory (including information assets)
- Information classification scheme
- Access control management (incl. privileged access)
- Cryptographic controls
- Physical access controls
- Employee onboarding and offboarding
- Training and awareness
- Network segmentation
- Logging and monitoring
- Vulnerability and patch management
- Backup and recovery
- Change management
- Supplier security management
- Incident response
- Business continuity
- Cloud service use (VDA-ISA 6.0 expansion)
- Configuration management (VDA-ISA 6.0 explicit)
- Secure software development
- Outsourced development oversight

VDA-ISA 6.0 introduced or strengthened controls around:

- Cloud services and shared-responsibility models
- Configuration baselines and drift detection
- Secure coding and SDLC integration
- Information deletion (including vendor-side commitments)
- Monitoring and anomaly detection
- AI / new-technology consideration (light-touch reference, not deep)

## Prototype Protection module

Automotive-specific. Covers the handling of:

- **Pre-series components** — physical parts before production launch
- **Prototype vehicles** — test mules, validation vehicles, pre-production builds
- **Design data** — CAD, simulation, test data, supplier-provided component specifications
- **Test environments** — dynos, environmental chambers, proving grounds
- **Photographic and video evidence** — restrictions on capturing and storing imagery

Typical Prototype Protection controls:

- **Restricted-access rooms** — secured spaces with badge / biometric entry, log retention
- **No-photo / no-mobile zones** — physical signage, device check-in, occasional searches
- **Camouflage requirements** — for vehicle prototypes leaving controlled premises
- **Vendor / visitor escort policies** — non-employees escorted at all times in prototype areas
- **Air-gapped networks** — for CAD and simulation data on prototype projects
- **Time-bounded retention** — pre-series data deleted on prescribed schedule post-launch
- **Travel and transport rules** — prototype components in transit with security measures
- **Subcontractor / sub-supplier flow-down** — Prototype Protection requirements pass through

OEM contracts often specify which Prototype Protection sub-label is required, calibrated to the sensitivity of the supplier's prototype access.

## Data Protection module

GDPR alignment. Required when supplier processes personal data on behalf of OEM (Article 28 processor scenarios). Controls cover:

- **Lawful basis for processing**
- **Purpose limitation**
- **Data minimization**
- **Accuracy of personal data**
- **Storage limitation** (retention schedules)
- **Integrity and confidentiality** (technical and organizational measures, TOM)
- **Accountability** (records of processing activities)
- **Data subject rights** (access, rectification, erasure, portability, objection)
- **Breach notification** processes
- **Data protection impact assessments** for high-risk processing
- **Cross-border transfer mechanisms** (SCCs, adequacy decisions, additional safeguards)
- **Sub-processor management** (controller approval, flow-down obligations)

Data Protection has two label tiers:

- **Standard** — for general personal-data processing
- **Special-category data** — when processing data subject to GDPR Article 9 (health, biometric, ethnic origin, political opinion, etc.)

## Scoring and audit conduct

For each applicable control:

1. **Supplier self-scores** using the workbook. Selects target level (per OEM requirement) and self-assesses current level. Documents evidence per level achieved.
2. **Audit provider scores independently** in AL2 / AL3 assessments. Reviews evidence, conducts interviews, observes practice.
3. **Reconciliation** — significant gaps between self-assessment and auditor scoring become discussion points. Often the auditor moderates the self-assessment downward; significant downward moderation is a yellow flag.
4. **Major findings** — controls where the audited maturity is below the target maturity for the label. Must be remediated for label issuance; remediation typically allowed within an agreed window.
5. **Minor findings** — controls slightly below target but with clear remediation path. May be issued with conditional label.
6. **Observations** — items not blocking label issuance but flagged for attention at next assessment cycle.

## Common assessment patterns

- **AL2 + Info Sec High** — most common combination. Typical maturity targets level 3.
- **AL3 + Info Sec High + Prototype Protection** — for development-partner-tier suppliers. AL3 brings on-site audit.
- **AL3 + Info Sec Very High + Prototype Protection + Data Protection** — for strategic-partner-tier with sensitive prototype access and PII processing.
- **Multi-site assessments** — large suppliers cover multiple sites in one assessment cycle; ENX portal records site-level labels.

## VDA-ISA versioning and transitions

Catalogue revisions affect existing labels in a calibrated way:

- New assessments after the revision use the current catalogue.
- Existing labels remain valid until their original three-year expiry.
- Renewal assessments at expiry use the current catalogue.
- Major revisions (4.x → 5.0, 5.x → 6.0) sometimes trigger ENX-announced transition windows for already-mid-cycle suppliers.

## SRE and AI-agent fit notes

- **Cloud-service controls (VDA-ISA 6.0)** — model API providers (Anthropic, OpenAI, Google) are cloud services for catalogue purposes. Configure DPAs, no-training-data-use settings, enterprise tiers.
- **Configuration management** — extends naturally to AI agent system prompts, tool scopes, model versions. Treat as configuration artefacts under VDA-ISA 6.0 expectations.
- **Secure coding and outsourced development** — apply to AI-coding-assistant output. The catalogue does not yet name this explicitly; mature implementations cover it within secure-development controls.
- **Information deletion** — automotive-specific retention controls plus VDA-ISA general deletion controls combine to require vendor-side retention proof. Model providers' zero-retention enterprise tiers are the path.
- **Prototype Protection × AI tools** — pre-series data must not flow to AI tools that retain or use it for training. Default ChatGPT, Claude.ai, Copilot configurations typically fail Prototype Protection criteria. Enterprise configurations with retention controls + DPAs are the workable path.
- **Monitoring and anomaly detection** — VDA-ISA 6.0 expansion lands close to needed AI-agent monitoring practice. Use the control to anchor agent action logging and anomaly detection.

## Stefan-context implementation sketch

Solo / small-team operation against automotive client:

- Use VDA-ISA workbook as self-assessment tool even without formal assessment. Internal target maturity level 3 against the Info Sec module covers most engagement needs.
- For engagements touching prototype data: apply Prototype Protection controls regardless of formal label requirement. Air-gapped (or strongly segregated) work environment, no-AI-tool-retention configuration, time-bounded retention.
- For engagements touching customer PII: apply Data Protection module controls. GDPR-aligned processing records, sub-processor (vendor) documentation, retention schedules.
- Map self-implementation back to ISO 27001 cluster atoms where controls overlap; avoid duplicating documentation.

## See also

- [[TISAX Cluster|cluster MOC]] · [[TISAX Assessment Levels]] · [[TISAX Labels and Scopes]] · [[TISAX Assessment Process]] · [[TISAX vs ISO 27001]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.8 Technological Controls]] (heavy control overlap)
