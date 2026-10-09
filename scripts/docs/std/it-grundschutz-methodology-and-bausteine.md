title: IT-Grundschutz Methodology and Bausteine
summary: Core methodology and building blocks (Bausteine) of IT-Grundschutz.
parent: bsi-grundschutz
order: 100
labels: bsi-grundschutz, framework-concept
aliases: IT-Grundschutz Methodology | IT-Grundschutz Bausteine | Grundschutz Methodology | BSI Methodology
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/bsi-grundschutz/IT-Grundschutz Methodology and Bausteine.md
reviewed: no
---
> Core methodology and building blocks (Bausteine) of IT-Grundschutz. Three protection-level approaches; modular Bausteine map to systems based on protection requirements.

## Methodology phases

### Schutzbedarfsfeststellung (protection requirement assessment)

Each information / system classified by protection requirement per Grundwerte (basic values):

- **Vertraulichkeit** (confidentiality)
- **Integrität** (integrity)
- **Verfügbarkeit** (availability)

Three protection levels:

- **Normal** — limited / tolerable impact
- **Hoch** — substantial impact, restrictions on operations
- **Sehr hoch** — existential impact

### Strukturanalyse

Map of organization:

- Information assets
- Business processes
- Applications
- IT systems
- Network connections
- Locations
- Personnel

### Modellierung

Map applicable Bausteine to systems based on Strukturanalyse + Schutzbedarf.

### Soll-Ist-Vergleich (target vs actual comparison)

Compare required measures (Soll) per Baustein against current implementation (Ist).

### Risikoanalyse

For systems with protection level "hoch" or "sehr hoch" or special threats, additional risk analysis per BSI Standard 200-3.

### Realisierungsplan

Plan for implementing missing measures.

### Aufrechterhaltung und Verbesserung

Ongoing maintenance and improvement.

## Three protection-level approaches (BSI 200-2)

### Basis-Absicherung

Minimum baseline. Only "Basis"-tier measures from each applicable Baustein implemented. Quick entry, limited protection.

### Standard-Absicherung

Default. All "Basis" + "Standard"-tier measures implemented. Comprehensive.

### Kern-Absicherung

Critical-assets focus. Highest-priority systems get "Hoch"-tier measures including "Sehr hoch" where applicable. Risk-based prioritization.

Combined approach common: Kern for critical assets, Standard for rest.

## Bausteine structure

Bausteine grouped:

- **ISMS** (B 1.x — Management): Sicherheitsmanagement, Organisation, Personal, Berechtigungsmanagement, Datenschutz, etc.
- **CON** (Konzepte und Vorgehensweisen): Kryptokonzept, Patch- und Änderungsmanagement, Notfallmanagement, etc.
- **OPS** (Betrieb): Datenträgermanagement, Outsourcing, Software-Tests, Datenträger / IT-Komponenten, etc.
- **DER** (Detection und Reaktion): Behandlung von Sicherheitsvorfällen, Detektion, Schadprogramme, etc.
- **APP** (Anwendungen): Browser, Office-Produkte, E-Mail, Webserver, Datenbanken, Container, etc.
- **SYS** (IT-Systeme): Allgemeiner Server, Allgemeiner Client, Mobile Geräte, Virtualisierung, Cloud-Komponenten, IoT, etc.
- **IND** (Industrielle IT): ICS, SCADA, Industrial Ethernet, etc.
- **NET** (Netze und Kommunikation): Netz-Komponenten, WLAN, VPN, etc.
- **INF** (Infrastruktur): Allgemeines Gebäude, Server-Räume, häuslicher Arbeitsplatz, mobile Arbeit, etc.

Each Baustein:

- Description of subject
- Threat references (linked to Gefährdungskatalog)
- Required measures (Anforderungen) by tier (Basis / Standard / höher)
- Cross-references to other Bausteine

## Annual updates

Kompendium updated annually (typically January edition). Updates:

- New Bausteine for emerging topics (cloud, container, AI, IoT, smart home).
- Revised existing Bausteine.
- Updated threat catalog.

Recent additions / strengthening:

- Cloud-specific Bausteine (APP.4, SYS.1.5 Virtualisierung, OPS.2 Cloud-Nutzung).
- Container Bausteine (SYS.1.6 Container).
- IoT Bausteine.
- AI / ML (limited; Kompendium 2025 added some AI-related guidance).

## Bridge to ISO 27001 Annex A

IT-Grundschutz Bausteine map to ISO 27001 Annex A controls:

- Most Annex A controls have corresponding Baustein coverage.
- Some Bausteine are more prescriptive than Annex A.
- Cross-walk documents published by BSI.

ISO 27001 auf Basis IT-Grundschutz uses Bausteine implementation as evidence for Annex A coverage.

## Tools

- **Verinice** — open-source ISMS tool with IT-Grundschutz support.
- **HiScout, ibi Systems, others** — commercial tools.
- **GSTOOL** (BSI tool) — historical; superseded.

## SRE and AI-agent fit notes

### AI features in Grundschutz

Cloud-component Bausteine (OPS.2 Cloud-Nutzung) apply when using model APIs. Application Bausteine for AI features themselves; IT-Grundschutz Kompendium expanding AI coverage.

### KRITIS sector-specific

KRITIS operators apply Grundschutz with sector-specific orientation. Energy, water, telecoms, healthcare have sector-specific guidance.

## Stefan-context implementation sketch

- For DE Mittelstand engagements: Grundschutz vocabulary load-bearing.
- For KRITIS clients: Grundschutz implementation guidance.

## See also

- [[BSI IT-Grundschutz Cluster|cluster MOC]] · [[IT-Grundschutz Certification]] · [[ISO 27001 Annex A.5 Organizational Controls]]
