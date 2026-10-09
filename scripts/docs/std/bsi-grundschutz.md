title: BSI IT-Grundschutz
summary: Map of BSI IT-Grundschutz, German national InfoSec framework from BSI (Bundesamt für Sicherheit in der Informationstechnik).
parent: index
order: 120
labels: bsi-grundschutz, de-national-framework, moc, security-compliance
aliases: BSI IT-Grundschutz Cluster | IT-Grundschutz | BSI IT-Grundschutz | Grundschutz | BSI Standards 200-x
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/bsi-grundschutz/BSI IT-Grundschutz Cluster.md
reviewed: no
---
> Map of BSI IT-Grundschutz — German national InfoSec framework from BSI (Bundesamt für Sicherheit in der Informationstechnik). National alternative to ISO 27001. Common in DE public sector, KRITIS critical infrastructure, Mittelstand. Now harmonized with ISO 27001 — Grundschutz-based certification under ISO 27001 possible. Reference cluster for DE-specific InfoSec engagement work.

## Anchors

- [position](pillars/bsi-grundschutz/position.md) · [anchors](pillars/bsi-grundschutz/anchors.md)

## Provenance

- **BSI** — Bundesamt für Sicherheit in der Informationstechnik. German federal cyber agency. Established 1991. bund.de/BSI.
- **IT-Grundschutzhandbuch** — first edition 1994. Methodology + control catalog.
- **BSI Standards 200-1, 200-2, 200-3, 200-4** — current methodology series replacing earlier 100-x series.
- **IT-Grundschutz Kompendium** — current catalog of building blocks (Bausteine). Annual edition; current ~2024/2025.
- **ISO 27001 mapping** — Grundschutz harmonized with ISO 27001; ISO 27001 certification "auf Basis IT-Grundschutz" available.

## What IT-Grundschutz is

A methodology + control catalog for InfoSec management. Three core concepts:

- **Schutzbedarfsfeststellung** (protection requirement assessment): classify info / systems by protection requirement (normal / hoch / sehr hoch).
- **Modellierung** (modeling): map building blocks (Bausteine) to systems based on protection requirements.
- **Sicherheitscheck** (security check): assess implementation of measures.

## BSI Standards series

### BSI Standard 200-1: ISMS — Information Security Management Systems

High-level ISMS requirements. ISO 27001-compatible. Foundation.

### BSI Standard 200-2: IT-Grundschutz Methodology

The methodology in detail. Three approaches:

- **Basis-Absicherung** (basic protection): minimum baseline.
- **Standard-Absicherung** (standard protection): default, comprehensive.
- **Kern-Absicherung** (core protection): focus on critical assets first.

### BSI Standard 200-3: Risk Analysis

Risk analysis approach for systems with protection requirement "hoch" or "sehr hoch" or other risk-elevated situations.

### BSI Standard 200-4: Business Continuity Management

Recently published. BCM methodology. ISO 22301-aligned.

## IT-Grundschutz Kompendium

Catalog of building blocks (Bausteine) grouped:

- **ISMS**: management-level Bausteine.
- **ORP** (Organisation und Personal): organization, personnel.
- **CON** (Konzepte und Vorgehensweisen): concepts.
- **OPS** (Betrieb): operations.
- **DER** (Detection und Reaktion): detection, response.
- **APP** (Anwendungen): applications.
- **SYS** (IT-Systeme): IT systems.
- **IND** (Industrielle IT): industrial IT.
- **NET** (Netze und Kommunikation): networks, communications.
- **INF** (Infrastruktur): infrastructure.

Each Baustein:

- Has identification number (e.g., SYS.1.5 Virtualisierung).
- Lists threat catalog references.
- Defines required and optional measures.
- Categorized by lifecycle (planning, procurement, implementation, operations, decommissioning).

Annual updates expand catalog.

Detail in [[IT-Grundschutz Methodology and Bausteine]].

## Certification path

Three certification paths:

1. **ISO 27001 auf Basis von IT-Grundschutz** — ISO 27001 certification using Grundschutz as implementation methodology. Issued by BSI-licensed auditors.
2. **IT-Grundschutz Testat** — lower-tier confirmation.
3. **ISO 27001 standard** — international standard certification.

Detail in [[IT-Grundschutz Certification]].

## KRITIS regulation

For critical infrastructure operators (KRITIS):

- BSI-Kritisverordnung defines KRITIS sectors and thresholds.
- KRITIS operators must implement state-of-the-art InfoSec (§8a BSIG).
- IT-Grundschutz commonly used as evidence framework.
- KRITIS reporting obligations under §8b BSIG.

NIS2 + KRITIS landscape currently being harmonized via NIS2UmsuCG.

## Why this matters for SRE work

- **DE public sector engagements**: IT-Grundschutz often required.
- **KRITIS clients**: Mittelstand industrial / critical-infrastructure customers use Grundschutz.
- **DE Mittelstand**: many use Grundschutz instead of ISO 27001.
- **NIS2 transposition (NIS2UmsuCG)**: Grundschutz methodology integrates with NIS2 obligations.

## Related clusters

- [[ISO 27001 Cluster|ISO 27001]] — harmonized; combined certification possible.
- [[NIS2 Cluster|NIS2]] — KRITIS aspects overlap.

## See also

[[BSI IT-Grundschutz Cluster]] (pillars MOC) · [position](pillars/bsi-grundschutz/position.md) · [anchors](pillars/bsi-grundschutz/anchors.md) · [[IT-Grundschutz Methodology and Bausteine]] · [[IT-Grundschutz Certification]] · [[IT-Grundschutz Controversies]] · [[ISO 27001 Cluster]]
