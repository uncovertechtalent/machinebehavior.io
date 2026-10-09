title: ISO 27001 Annex A.7 Physical Controls
summary: Fourteen controls covering physical perimeter, entry, monitoring, environmental threats, secure-area working, clear-desk, equipment, off-premises assets, media, utilities, cabling, maintenance, and disposal.
parent: iso-27001
order: 100
labels: annex-a-theme, iso-27001, theme-physical
aliases: ISO 27001 Annex A.7 | ISO 27001 Physical Controls | Annex A.7 Controls
type: annex-a-theme
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Annex A.7 Physical Controls.md
reviewed: no
---
> Fourteen controls covering physical perimeter, entry, monitoring, environmental threats, secure-area working, clear-desk, equipment, off-premises assets, media, utilities, cabling, maintenance, and disposal. The theme most often partially-excluded for remote-first SaaS — with caveats: if humans handle org-controlled hardware anywhere (home offices, co-working, in transit), A.7 has work to do.

## How to read this atom

Each control listed below has its reference number and title from ISO 27001:2022 Annex A. Notes cover purpose, typical implementation, common evidence.

A.7.4 (Physical security monitoring) is new in :2022.

## A.7.1 Physical security perimeters

Physical perimeters defined and used to protect areas containing information processing facilities. Fences, walls, doors, controlled-entry points.

Remote-first applicability: cloud providers carry this through their own ISO 27001 / SOC 2; org responsibility is supplier oversight (A.5.22-A.5.23). For owned premises (HQ, satellite offices, home offices for certain risk profiles), direct applicability.

## A.7.2 Physical entry

Authorization controls for physical entry. Badging, visitor management, escorted-visitor procedure, tailgating prevention.

## A.7.3 Securing offices, rooms and facilities

Physical security designed and applied to offices, rooms, facilities containing sensitive information or processing.

## A.7.4 Physical security monitoring (NEW)

Premises continuously monitored for unauthorized physical access. CCTV, intrusion detection systems, environmental sensors, smart locks with audit logs.

Remote-first applicability: gradient. Pure remote = supplier-side only (cloud provider's data center). Hybrid with offices = direct. Home-office with org-controlled devices in higher-risk roles (security operations, finance leadership, executives) = considered, may not extend to home monitoring but acceptable use policy + clear-desk-equivalent + secure storage applies.

## A.7.5 Protecting against physical and environmental threats

Fire, flood, earthquake, explosion, civil unrest, theft, vandalism, supply disruption. Environmental monitoring, fire suppression, water detection, climate control, redundancy.

## A.7.6 Working in secure areas

Procedures for personnel working in secure areas. Photography / recording rules, access logs, two-person rules where relevant.

## A.7.7 Clear desk and clear screen

Information not visible to unauthorized parties. Locked workstations, no sensitive printouts on desks, no whiteboards visible through windows.

AI-agent fit: extends to virtual workspace. AI chat history visible during screen-share, prompt drafts not cleaned up, agent action results lingering in browser tabs. Awareness component.

## A.7.8 Equipment siting and protection

Equipment sited to reduce risks from environmental threats, hazards, unauthorized access. Server racks in secure rooms, not under desks. Laptops not in cars unattended.

## A.7.9 Security of assets off-premises

Security applied to off-premises assets: laptops in transit, equipment at conferences, remote-worker equipment.

## A.7.10 Storage media

Storage media managed across the lifecycle: acquisition, use, transport, disposal. Includes removable media (USB drives, external SSDs), backup media, cloud-stored data on org-controlled storage.

Common implementation: removable media policy (often "no removable media without explicit approval"), encryption requirements for any media leaving secure premises, asset register for org-issued media.

## A.7.11 Supporting utilities

Power, water, cooling, telecommunications, gas (where applicable). Protection from failure and disruption.

Cloud-customer applicability: largely supplier-side. Org responsibility for owned-premises gear (network equipment, on-prem servers, edge devices).

## A.7.12 Cabling security

Power and telecommunication cabling protected from interception, interference, damage.

## A.7.13 Equipment maintenance

Maintenance procedures preventing security compromise. Vendor maintenance subject to A.5.19 supplier controls; on-premises spare-parts handling, decommissioning of replaced parts.

## A.7.14 Secure disposal or re-use of equipment

Equipment containing data wiped per data-classification before disposal, re-use, or return to lessor. Certificates of destruction for sensitive-data media.

Common gap: org-issued devices returned by leavers without secure-wipe before re-issue. Often a Cl 8 / A.5.18 finding.

## SRE and AI-agent quick map (load-bearing A.7 controls)

| Concern | Primary A.7 controls |
|---|---|
| Cloud / SaaS infrastructure physical security | A.7.1-A.7.5 (supplier-side, monitored via A.5.22) |
| Remote-worker laptop and home-office posture | A.7.7, A.7.8, A.7.9, A.7.10 |
| Conference / travel security | A.7.7, A.7.9 |
| Storage media (incl backup tapes / drives) | A.7.10, A.7.14 |
| Disposal of org-issued devices | A.7.14 |

## Typical audit observations

- **Over-exclusion of A.7.** "We are remote-first" excludes too much. A.7.7, A.7.8, A.7.9, A.7.10, A.7.14 apply regardless. Exclude only what is genuinely not applicable; explain narrowly.
- **A.7.4 not addressed in SoA post-:2022.** New control, often missed in transition. Update the SoA to either apply or justify exclusion.
- **Disposal evidence missing.** Org has a procedure but no records of executed disposals. Cl 7.5 + A.7.14 finding.

## Stefan-context implementation sketch

- Premises: no commercial office; home office is the physical workspace. Apply A.7.7, A.7.8, A.7.9 within proportionate scope.
- Devices: Macbook (canonical), Mac Studio (incoming), iPhone, possibly secondary laptops. FileVault on macOS, encrypted storage volumes, locked-screen idle timeout, MDM optional.
- Cloud / SaaS: A.7.1-A.7.5 monitored via A.5.22 supplier oversight (AWS, Cloudflare, Anthropic, OpenAI, Apple, etc.).
- Disposal: Apple T2 / Secure Enclave secure-erase for retired devices. Document the procedure.

## See also

- [[ISO 27001 Cluster|cluster MOC]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.6 People Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
- [[ISO 27001 Family and Sector Variants]] (ISO 27017 cloud, ISO 27018 PII processor for cloud-physical considerations)
