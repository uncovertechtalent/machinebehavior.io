title: SLSA SBOM
summary: Software supply chain integrity.
parent: index
order: 220
labels: moc, slsa-sbom, supply-chain-security
aliases: SLSA SBOM Cluster | SLSA | SBOM | Software Supply Chain Integrity
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/slsa-sbom/SLSA SBOM Cluster.md
reviewed: no
---
# SLSA + SBOM Cluster

> Software supply chain integrity. SLSA (Supply-chain Levels for Software Artifacts) — Google-originated, OpenSSF-stewarded framework. SBOM (Software Bill of Materials) — formal inventory of components. Both increasingly required by CRA, NIS2, US Executive Orders, NIST guidance.

## Anchors

- [position](pillars/slsa-sbom/position.md) · [anchors](pillars/slsa-sbom/anchors.md)

## Provenance

### SLSA

- **Google-developed** internally, then open-sourced ~2021.
- **OpenSSF (Open Source Security Foundation) stewardship** since 2021.
- **SLSA v0.1** through **SLSA v1.0** (2023) — current major version.

### SBOM

- **Concept** decades-old.
- **Executive Order 14028** (May 2021, US) — mandated SBOM for federal software.
- **NTIA Minimum Elements for SBOM** (July 2021).
- **CISA SBOM work** ongoing.
- **EU CRA** requires component identification.

## What SLSA is

Framework for software supply chain security with assurance levels (SLSA levels) and requirements:

- **Build integrity**: how artifact was built.
- **Source integrity**: where source came from.
- **Provenance**: cryptographically signed metadata.

## SLSA levels (SLSA v1.0)

Four levels:

- **L0**: no requirements.
- **L1**: provenance exists. Process documented.
- **L2**: provenance authenticated. Build platform integrity.
- **L3**: provenance non-forgeable. Hardened build platform. Strict isolation.

Higher levels = stronger guarantees.

## What SBOM is

Machine-readable inventory of software components:

- Component name + version.
- Supplier.
- Hash / identifier.
- Relationships (dependencies).
- License.
- Other metadata.

## SBOM formats

Three primary standards:

- **SPDX** (Software Package Data Exchange) — Linux Foundation. ISO/IEC 5962.
- **CycloneDX** — OWASP-stewarded.
- **SWID Tags** — ISO/IEC 19770-2. Used in some federal contexts.

SPDX and CycloneDX dominant.

Detail in [[SLSA Levels and SBOM Formats]].

## Regulatory drivers

- **US EO 14028** (May 2021) — federal software SBOM.
- **EU CRA** (2024) — vulnerability identification including components.
- **EU NIS2** (2022) — supply chain security.
- **US CMMC** (2.0) — defense contractor supply chain.
- **Many sector regulations** referencing SBOM.

## Tooling ecosystem

### SBOM generation

- **Syft** (Anchore).
- **CycloneDX CLI**.
- **SPDX tools**.
- **Build-system integrations** (Bazel, npm, pip, Cargo, Maven, Gradle).
- **Container scanners** generating SBOMs.

### SLSA implementation

- **Sigstore** — code signing.
- **in-toto** — supply chain attestation.
- **GitHub Actions provenance** — automatic SLSA L2/L3 provenance.
- **Tekton Chains** — Tekton SLSA support.

## Why this matters

- **Regulatory pressure** real and rising.
- **Supply chain attacks** (SolarWinds, Kaseya, XZ Utils) demonstrate concrete risk.
- **AI model supply chain** — emerging concern; ML-SBOM concept.
- **Cloud-native build** practice increasingly SLSA-compatible.

## Related clusters

- [[Cyber Resilience Act Cluster|CRA]] — product cybersecurity.
- [[NIS2 Cluster|NIS2]] — supply chain security.
- [[ISO 27001 Cluster|ISO 27001]] — A.5.21 ICT supply chain.

## See also

[[SLSA SBOM Cluster]] (pillars MOC) · [position](pillars/slsa-sbom/position.md) · [anchors](pillars/slsa-sbom/anchors.md) · [[Cyber Resilience Act Cluster]] · [[NIS2 Cluster]]
