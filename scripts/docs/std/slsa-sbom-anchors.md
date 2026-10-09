title: SLSA SBOM anchors
summary: SLSA SBOM anchors, from the knowledge vault.
parent: slsa-sbom
order: 6
labels: anchors, slsa-sbom
aliases: SLSA SBOM Anchors
type: anchors
created: 2026-05-12
updated: 2026-05-12
origin: pillars/slsa-sbom/anchors.md
reviewed: no
---
# SLSA + SBOM Anchors

## Primary documents

### SLSA

- **SLSA Specification v1.0** — slsa.dev.
- **SLSA Threats and Mitigations** documentation.

### SBOM

- **SPDX 2.3 specification** (ISO/IEC 5962:2021) — Linux Foundation.
- **CycloneDX 1.6 specification** — OWASP.
- **NTIA Minimum Elements for an SBOM** (July 2021).
- **CISA SBOM resources**.

## Operating bodies

- **OpenSSF** (Open Source Security Foundation) — SLSA stewardship; Linux Foundation project.
- **Linux Foundation** — SPDX.
- **OWASP** — CycloneDX.
- **NTIA / CISA** — US federal SBOM coordination.

## Adjacent standards

- **NIST SP 800-218 (SSDF)** — Secure Software Development Framework.
- **NIST SP 800-161 Rev. 1** — Cybersecurity Supply Chain Risk Management.
- **CISA Secure by Design** guidance.

## Tooling

### SBOM generation

- **Syft** (Anchore)
- **CycloneDX CLI**
- **SPDX tools**
- **Build-system integrations**: npm audit, pip, Maven, Gradle, Cargo, Bazel
- **Container scanners**: Trivy, Grype, Clair

### SLSA implementation

- **Sigstore**: cosign, rekor, fulcio
- **in-toto**: attestation framework
- **GitHub Actions provenance** native
- **GitLab attestations**
- **Tekton Chains**

### Vulnerability matching

- **GUAC** (Graph for Understanding Artifact Composition)
- **OSV** (Open Source Vulnerabilities)
- **CVE feeds**
- **EPSS** (Exploit Prediction Scoring System)

## Reference resources

- **slsa.dev**
- **spdx.dev**
- **cyclonedx.org**
- **openssf.org**
- **cisa.gov/sbom**

## See also

- [[SLSA SBOM Cluster|cluster MOC]] · [position](pillars/slsa-sbom/position.md)
- [[Cyber Resilience Act Cluster]] · [[NIS2 Cluster]]
