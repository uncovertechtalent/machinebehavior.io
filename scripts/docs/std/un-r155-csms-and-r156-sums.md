title: UN R155 CSMS and R156 SUMS
summary: CSMS certificate prerequisite to type approval.
parent: un-r155-r156
order: 100
labels: regulation-concept, un-r155-r156
aliases: UN R155 CSMS | UN R156 SUMS | Vehicle Type Approval Cybersecurity | OTA Update Regulation
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/un-r155-r156/UN R155 CSMS and R156 SUMS.md
reviewed: no
---
## R155 — Cybersecurity and CSMS

### Two-tier assessment

1. **CSMS Certificate of Compliance** — organizational-level approval. Manufacturer demonstrates CSMS conforms to R155. Issued by approval authority.
2. **Vehicle type approval** with cybersecurity — type-level. Manufacturer demonstrates the specific vehicle type implements cybersecurity within the CSMS umbrella.

CSMS certificate prerequisite to type approval.

### CSMS requirements (R155 Para 7.2)

CSMS covers cybersecurity throughout development, production, post-production:

- **Processes** to manage cybersecurity risks throughout the vehicle's lifetime.
- **Processes** for ensuring cybersecurity risks of vehicle types are managed.
- **Processes** for assessing and addressing risks identified after vehicle entry to service.
- **Processes** for monitoring, detecting, responding to attacks, threats, vulnerabilities.
- **Processes** to ensure cyber attacks are properly handled.
- **Processes** to provide forensic evidence.

### Vehicle type cybersecurity (R155 Para 7.3)

Per vehicle type:

- Risk assessment documented.
- Risks managed.
- Mitigations implemented.
- Verification of mitigations.
- Detection capabilities.
- Vulnerability disclosure capability.
- Information sharing capability.

### Annex 5 threat catalog

R155 Annex 5 lists threats to vehicles. Manufacturer demonstrates risk assessment considered these threats.

Threat categories:

- Back-end servers
- Communication channels
- Update procedures
- Unintended human actions
- External connectivity
- Vehicle data
- ECUs / sensors
- Other

### Validity and review

- CSMS certificate valid limited period (typically 3 years).
- Periodic renewal.
- Renewal includes audit.

## R156 — Software Update and SUMS

### SUMS Certificate

Manufacturer demonstrates SUMS conforms to R156. Issued by approval authority.

### SUMS requirements (R156 Para 7.1)

SUMS covers software update management:

- **Documented processes** for software update.
- **Configuration management** of vehicle software.
- **Software identifiers** (RxSWIN — Software Identification Number for type approval relevance).
- **Dependency analysis** before updates.
- **Update authorization**.
- **Validation** of updates.
- **Recording** of update activity.
- **Information** to vehicle owners.

### Vehicle type SUMS (R156 Para 7.2)

Per vehicle type:

- Software update mechanisms implemented.
- Identifier management.
- Update authentication / integrity.
- User notification.
- Rollback capability where applicable.

### Wireless updates (OTA) specific requirements

Additional R156 provisions for OTA:

- Pre-condition checks (vehicle state, energy, environment).
- Failure handling.
- User awareness of update.
- Where vehicle in use, safety considerations.

### RxSWIN

The Software Identification Number per regulation. Identifies software relevant to vehicle type approval. Updated software requiring re-approval triggers RxSWIN change and type-approval workflow.

## OEM-supplier responsibilities

CSMS / SUMS belong to OEM (vehicle manufacturer). But:

- Tier-1/2 suppliers contribute components.
- Supplier-side cybersecurity engineering required.
- Coordination via Cybersecurity Interface Agreements.
- ISO 21434 distributed cybersecurity activities frame this.

## Type approval flow

1. OEM has CSMS Certificate and SUMS Certificate.
2. OEM applies for vehicle type approval to Type Approval Authority.
3. TAA assesses vehicle type against R155 / R156 requirements.
4. Documentation submitted: risk assessments, design choices, test results, supplier coordination.
5. TAA grants approval if requirements met.
6. Vehicle can be sold in UNECE 1958 Agreement contracting parties.

## AI features and autonomous driving

For AI features (ADAS, autonomous driving):

- R155 risk assessment includes AI-related threats.
- R156 software update applies to AI feature updates.
- Cross-application with ISO/PAS 21448 SOTIF and ISO 21434.
- AI Act co-applies for high-risk AI in vehicles.

## SRE and AI-agent fit notes

Direct applicability limited outside automotive. For automotive engagements:

- R155 / R156 regulatory context.
- ISO 21434 / ISO 24089 implementation.
- TISAX supplier-side cybersecurity.

## Stefan-context implementation sketch

- Limited direct relevance for general SRE work.
- For automotive client engagements: vocabulary load-bearing.

## See also

- [[UN R155 R156 Cluster|cluster MOC]] · [[UN R155 R156 Controversies]]
- [[ISO 21434 Cluster]] · [[TISAX Cluster]] · [[ASPICE Cluster]]
