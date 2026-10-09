title: ISO 27001 Clause 4 Context
summary: ISO 27001 Clause 4 Context, from the knowledge vault.
parent: iso-27001
order: 100
labels: clause-4, iso-27001, iso-clause
aliases: ISO 27001 Clause 4 | ISO 27001 Context of the Organization | ISMS Scope
type: iso-clause
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Clause 4 Context.md
reviewed: no
---
# ISO 27001 Clause 4 Context of the Organization


## Sub-clause map

- **4.1** Understanding the organization and its context — external and internal issues relevant to ISMS purpose.
- **4.2** Understanding the needs and expectations of interested parties — interested parties (a), their relevant requirements (b), which of those requirements will be addressed through the ISMS (c, new in :2022; explicitly includes "legal, statutory, regulatory and contractual requirements").
- **4.3** Determining the scope of the ISMS — boundaries and applicability; takes 4.1, 4.2, and interfaces / dependencies as input; the scope statement is documented information.
- **4.4** Information security management system — the org "shall establish, implement, maintain and continually improve" an ISMS, including the processes needed and their interactions.

## Changes from :2013

- **4.2 added subitem (c)** explicitly addressing which interested-party requirements are in scope of the ISMS (previously implicit).
- **4.4 expanded** to call out "the processes needed and their interactions," aligning with Annex SL wording.
- Otherwise structurally unchanged.

## Evidence artefacts an auditor expects

- **Context analysis** — typically a document or section in the ISMS manual covering: org purpose, business model, sector, regulatory environment, market position, strategic direction, internal culture / capability, technology base.
- **Interested parties register** — list of stakeholders (customers, employees, regulators, suppliers, owners, investors, partners, the public where relevant) with their security-relevant requirements and the in-scope / out-of-scope decision per (c).
- **Scope statement** — concise document stating: what is in scope (locations, business units, services, technologies, information assets), what is out of scope, justifications for exclusions, interfaces with out-of-scope and external entities.
- **ISMS process map** — diagram or table of the management-system processes (risk assessment, risk treatment, internal audit, management review, etc.) and how they interact.

## Typical audit observations

- **Scope too narrow.** "We certified the SaaS product but our corporate IT and HR are excluded." Auditor flags if the exclusion creates a control gap (HR runs the joiner-mover-leaver process the ISMS depends on).
- **Generic context analysis.** Boilerplate "we operate in a fast-moving sector facing many cyber threats" is a minor nonconformity in mature audits; the auditor wants company-specific issues.
- **Stale interested-parties register.** Last updated three years ago, missing new regulations (DORA, NIS2, AI Act). Common minor nonconformity post-2024.
- **Interfaces section missing.** 4.3.c is often skipped or treated as a one-line "we integrate with vendor X." Mature audits expect a fuller dependency map.

## Common implementation gaps

- **Scope excludes the build / dev environment** but production depends on it. Build supply chain is in scope of the threat the ISMS is meant to address, regardless of legal scope.
- **Interested-parties register treated as compliance ceremony.** A useful register feeds the risk-assessment input list (Cl 6.1.2) and the communication plan (Cl 7.4). If it does neither, it is a museum piece.
- **Context analysis written once, never revisited.** Cl 4.1 has no explicit re-run cadence but the management review (9.3) shall consider "changes in external and internal issues" — so revisiting is implicit.

## SRE and AI-agent fit notes

- **Vendor agents as interested parties.** Cloud providers, model providers (Anthropic, OpenAI, etc.), self-hosted-but-vendor-built tools (OpenCode, Claude Code) all have terms-of-service requirements that flow into 4.2.b. Their requirements on you and your requirements on them both belong in the register.
- **AI-system context.** The :2022 standard predates the agent-system maturity wave. Capture autonomous-agent operations as an internal-context item: "the org operates autonomous and semi-autonomous AI agents in production, with X human-in-the-loop policy."
- **Multi-tenant / federation scope.** Federated bd workspaces, vault sync across machines, headscale-mediated VPN — all are interfaces under 4.3.c. The org owns one node; the federation graph is the dependency.
- **Out-of-scope but in-threat-path.** Personal devices, home networks, and BYOD endpoints often sit out of formal scope but inside the threat path for a small / remote-first org. Acknowledge the gap; do not pretend it does not exist.

## Stefan-context implementation sketch

- Org context: solo / small-team SRE consulting, vault-as-knowledge-store, multi-machine workspace (Macbook canonical, Mac Studio retrieval, [host] build host, AWS headscale).
- Interested parties: clients ([employer]-class), client clients (Mittelstand procurement), vendors (Anthropic, Apple, Cloudflare, AWS), regulator (no direct supervision for solo work, but client-imposed flow-down GDPR / NIS2 obligations).
- Scope (notional): vault content classification & handling, agent-system operation, client deliverable workflows. Out of scope: personal financial / health information (lives in `whiteout-kb/` with its own handling rules).
- Interfaces: client systems (SaaS APIs, SSH access, repository access), vendor APIs, federation peers.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Clause 5 Leadership]] · [[ISO 27001 Clause 6 Planning]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (specifically A.5.31 legal, statutory, regulatory and contractual requirements; A.5.36 compliance with policies, rules and standards)
