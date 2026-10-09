title: SLSA Levels and SBOM Formats
summary: No supply chain assurance.
parent: slsa-sbom
order: 100
labels: framework-concept, slsa-sbom
aliases: SLSA Levels | SBOM Formats | SPDX vs CycloneDX | SLSA L1 L2 L3 | in-toto | Sigstore
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/slsa-sbom/SLSA Levels and SBOM Formats.md
reviewed: no
---
## SLSA v1.0 levels

### Level 0 — No requirements

No supply chain assurance.

### Level 1 — Provenance exists

- Software produced with provenance (build records).
- Documented build process.
- Provenance available to consumers.

### Level 2 — Provenance authenticated, build platform integrity

- Provenance cryptographically signed by build platform.
- Build platform integrity (limits on tampering during build).
- Source-controlled inputs to build.

### Level 3 — Provenance non-forgeable, hardened build platform

- Provenance unforgeable (strong cryptographic guarantees).
- Build platform hardened against insider compromise.
- Strict isolation between builds.
- Two-person review for build configuration changes.

### Earlier SLSA L4 deprecated

SLSA v0.1 had L4 (two-person source code review, hermetic builds). v1.0 simplified to three levels; L4-equivalent guarantees folded into L3.

## SLSA tracks (v1.0)

SLSA v1.0 introduced "tracks":

- **Build track**: provenance + build integrity (L1, L2, L3).
- **Source track**: source code integrity. Levels mostly to be decided as of 2024.
- **Other tracks**: in development.

## In-toto

Framework for software supply chain attestation. Used by SLSA:

- Each step in supply chain documents its action.
- Cryptographic signatures.
- Chain of custody.
- Verification at consumption.

## Sigstore

Toolset for signing software artifacts:

- **cosign**: signing CLI.
- **fulcio**: certificate authority issuing short-lived certs based on OIDC identity.
- **rekor**: transparency log of signatures.

Reduces friction of code signing — no private key management needed.

## SBOM formats

### SPDX (Software Package Data Exchange)

- ISO/IEC 5962:2021.
- Linux Foundation.
- Tag-value, RDF, JSON, YAML, XML formats.
- Strong license-management content.
- Wide tooling support.

### CycloneDX

- OWASP project.
- JSON, XML formats.
- Strong security/vulnerability focus.
- Wide tooling support.
- Extensions for VEX (Vulnerability Exploitability eXchange).

### SWID Tags

- ISO/IEC 19770-2.
- XML format.
- Limited tooling.
- Mostly federal contexts.

### Comparison

For most use cases, SPDX or CycloneDX work; some orgs maintain both. Tooling typically handles conversion.

## SBOM essential fields (NTIA Minimum)

Per NTIA minimum elements for an SBOM:

- Author of SBOM entry
- Supplier
- Component name
- Version
- Other unique identifiers (PURL, CPE, SWID, etc.)
- Dependency relationships
- Timestamp

## VEX — Vulnerability Exploitability eXchange

Companion to SBOM:

- Vulnerability + product + status (affected / not affected / fixed).
- Justification for status.
- Enables vulnerability triage with provider input.

CSAF (Common Security Advisory Framework) format used.

## Use cases

### Build-time

- Generate SBOM during build.
- Generate SLSA provenance.
- Sign artifact + provenance.

### Distribution

- Distribute SBOM + provenance + signature alongside artifact.

### Consumption

- Verify signature.
- Verify provenance against expected.
- Check SBOM components against vulnerability feeds.
- Apply VEX statements.

### Inventory

- Maintain SBOM inventory per deployed artifact.
- Periodic vulnerability rescanning.
- Procurement-supplied SBOM intake.

## AI / ML SBOM

Emerging concept:

- Model + version + provenance.
- Training data identification.
- Dependencies (transformers, frameworks).
- Fine-tuning data.
- Evaluation data.

Standards developing; current SBOM formats incomplete. ML-BOM emerging concept.

## SRE and AI-agent fit notes

### Build pipeline SLSA adoption

- GitHub Actions: SLSA L2 provenance generation native.
- Builds publish provenance + signatures.
- Downstream verification.

### SBOM for AI features

- Standard SBOM for software components.
- Model + training metadata documented separately (ML-BOM emerging).
- Vendor model providers: limited SBOM provision currently.

### Vulnerability management

- SBOM enables prompt CVE correlation.
- Tools (Trivy, Grype, Snyk) consume SBOM.

## Stefan-context implementation sketch

- For client SDLC engagements: SLSA + SBOM as supply-chain practice baseline.
- For AI features: ML-BOM tracking experimental; standard SBOM for code dependencies.

## See also

- [[SLSA SBOM Cluster|cluster MOC]] · [[SLSA SBOM Controversies]]
- [[Cyber Resilience Act Cluster]] (CRA requires component identification) · [[NIS2 Security Measures]] (Art 21(d) supply chain)
