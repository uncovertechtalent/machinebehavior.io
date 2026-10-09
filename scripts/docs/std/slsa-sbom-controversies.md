title: SLSA SBOM Controversies
summary: SBOM generation widespread; SBOM consumption / operational use less.
parent: slsa-sbom
order: 100
labels: cross-cutting, slsa-sbom
aliases: SLSA SBOM Controversies
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/slsa-sbom/SLSA SBOM Controversies.md
reviewed: no
---
# SLSA + SBOM Controversies

## Generation vs use gap

SBOM generation widespread; SBOM consumption / operational use less mature:

- Most SBOMs go unused after generation.
- Vulnerability matching imperfect.
- Limited tooling for SBOM-based decision-making.

## Multi-format friction

SPDX vs CycloneDX dual standards:

- Conversion friction.
- Tool support split.
- Procurement complications.

## Maintainer burden

Open-source maintainer pressure:

- Compliance burden shifts upstream.
- Unfunded mandates.
- Maintainer burnout risk.

## Vulnerability matching imperfect

SBOM → CVE matching not always accurate:

- Component identification ambiguity.
- Version-string variance.
- False positive / negative noise.

## AI / ML-SBOM nascent

Current SBOM formats not built for ML:

- Models + training data + dependencies need different representation.
- Standards in development; operational tooling limited.
- AI vendor SBOM provision spotty.

## SLSA adoption gap

Most software not SLSA L1 yet:

- Build pipeline configurations not consistently producing provenance.
- SLSA L3 requires hardened build infrastructure — significant uplift.

## Regulatory dependency

Adoption largely regulatory-driven (EO 14028, CRA):

- Voluntary adoption slower.
- Procurement signal still emerging.

## Counterpoint

- Genuinely useful supply-chain integrity work.
- Tooling ecosystem maturing fast.
- Regulatory pressure forcing adoption.
- Real supply-chain attacks justify investment.

## See also

- [[SLSA SBOM Cluster|cluster MOC]] · [[SLSA Levels and SBOM Formats]]
- [[Cyber Resilience Act Controversies]]
