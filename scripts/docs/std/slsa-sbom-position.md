title: SLSA SBOM position
summary: SLSA SBOM position, from the knowledge vault.
parent: slsa-sbom
order: 5
labels: position, slsa-sbom
aliases: SLSA SBOM Position
type: position
created: 2026-05-12
updated: 2026-05-12
origin: pillars/slsa-sbom/position.md
reviewed: no
---
# SLSA + SBOM Position

## What they do well

- **Concrete supply-chain integrity** — moving beyond vague "supply chain security."
- **Tooling ecosystem mature** for major build systems.
- **Regulatory alignment** — CRA, NIS2, EO 14028, CMMC all reference.
- **SLSA levels** progression supports incremental adoption.
- **SBOM formats stable** (SPDX, CycloneDX).

## What they do poorly

- **Operational adoption gap** — SBOM generation widespread, SBOM consumption / use less mature.
- **AI / ML-SBOM emerging** — model + training data + dependencies; current SBOM formats incomplete.
- **Open-source maintainer burden** — supply-chain pressure shifts to maintainers.
- **Multi-format friction** — SPDX vs CycloneDX.
- **Vulnerability matching** to SBOM components imperfect.

## Evidence

- US federal SBOM mandate via EO 14028.
- EU CRA component identification requirements approaching.
- Major build platforms (GitHub, GitLab, CircleCI) supporting SLSA provenance.
- Industry SBOM adoption rapid.

## Personal calibration

- For client SDLC engagements: SLSA + SBOM emerging baseline.
- For AI features: ML-SBOM concept worth tracking but operational tooling limited.

## See also

- [[SLSA SBOM Cluster|cluster MOC]] · [anchors](pillars/slsa-sbom/anchors.md)
