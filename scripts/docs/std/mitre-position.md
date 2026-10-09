title: MITRE position
summary: Current view on MITRE ATT&CK / D3FEND / ATLAS as operational frameworks for threat intel and defense.
parent: mitre
order: 5
labels: mitre, position
aliases: MITRE Position
type: position
created: 2026-05-12
updated: 2026-05-12
origin: pillars/mitre/position.md
reviewed: no
---
# MITRE Frameworks Position

> Current view on MITRE ATT&CK / D3FEND / ATLAS as operational frameworks for threat intel and defense.

## What they do well

- **Practitioner-accessible.** Free, open, well-organized.
- **Continuously updated.** Multiple major updates per year for ATT&CK.
- **Vendor-neutral.** No commercial agenda; community-driven.
- **De facto standard.** Most security tooling, threat-intel feeds, red-team reports use ATT&CK language.
- **D3FEND-ATT&CK mapping** supports control-selection workflows.
- **ATLAS fills AI threat gap.** First major framework dedicated to AI-system adversaries.

## What they do poorly

- **Coverage gaps.** Some sectors (ICS-specific, supply chain) less mature.
- **D3FEND less adopted than ATT&CK.** Defensive side less visible than offensive.
- **ATLAS depth varies.** Some AI threat categories well-covered (prompt injection, model extraction); others lighter (agent-specific threats, multi-modal attacks).
- **Operational implementation effort.** Mapping organizational controls to D3FEND requires substantial work.
- **Framework sprawl.** Multiple matrices (Enterprise, Mobile, ICS, Cloud) plus D3FEND plus ATLAS creates navigation cost.

## Evidence

- **ATT&CK adoption widespread.** Major SIEM, EDR, XDR vendors map products to ATT&CK. Threat intel feeds tag indicators with ATT&CK techniques.
- **D3FEND adoption growing** but lags ATT&CK.
- **ATLAS adoption** active in AI security community; less mainstream than OWASP LLM Top 10.
- **Government adoption.** US federal, NATO, multiple allied national cybersecurity agencies reference ATT&CK.

## Personal calibration

- **For threat modeling**: ATT&CK + ATLAS as taxonomy.
- **For control selection**: D3FEND-ATT&CK mapping inputs.
- **For incident classification**: ATT&CK techniques.
- **For AI-feature threat modeling**: ATLAS + OWASP LLM Top 10 together.

## See also

- [[MITRE Cluster|cluster MOC]] · [[MITRE ATT&CK]] · [[MITRE ATLAS]]
- [anchors](pillars/mitre/anchors.md)
