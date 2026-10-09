title: ISO 27001 Clause 5 Leadership
summary: ISO 27001 Clause 5 Leadership, from the knowledge vault.
parent: iso-27001
order: 100
labels: clause-5, iso-27001, iso-clause
aliases: ISO 27001 Clause 5 | ISO 27001 Leadership | ISO 27001 Policy | ISO 27001 Roles
type: iso-clause
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Clause 5 Leadership.md
reviewed: no
---
## Sub-clause map

- **5.1** Leadership and commitment — top management shall demonstrate leadership and commitment through nine listed actions (a-i).
- **5.2** Policy — top management shall establish an information security policy with seven listed properties (a-g).
- **5.3** Organizational roles, responsibilities and authorities — top management assigns roles for ISMS conformance and ISMS performance reporting.

## Changes from :2013

- **Wording shifts** to align with Annex SL harmonized text. "Top management shall demonstrate leadership and commitment with respect to the ISMS" replaced with "by" + list of actions.
- **No substantive structural change.** Three sub-clauses preserved.

## Evidence artefacts an auditor expects

- **Information security policy document** — short (1-3 pages), board-approved, dated, owner identified, review cadence stated (typically annual).
- **Policy communication evidence** — intranet posting, training records, sign-off acknowledgements, induction materials referencing the policy.
- **Top-management meeting minutes** showing security on the agenda, decisions and resource allocations recorded.
- **RACI matrix or roles register** mapping the management-system processes to named roles (CISO, ISMS Manager, Risk Owner, Asset Owner, Control Owner, Internal Audit Lead, Management Representative).
- **Job descriptions / role descriptions** for security-relevant roles, including the management-representative role (commonly the CISO or equivalent).
- **Resource-allocation evidence** — budget line items, headcount, tooling spend.

## Typical audit observations

- **Policy too long.** Twenty-page policies are typically a sign the org has confused policy with procedure. Auditor finding: policy lacks clarity; recommend separation.
- **Policy never communicated.** Sitting on a shared drive in a folder no one opens. Spot-check: ask a random employee what the security policy commits the company to. If they cannot name two commitments, finding.
- **No board approval visible.** Policy says "approved by management" without a dated signature or meeting reference. Minor nonconformity.
- **Management representative role unclear.** Cl 5.3 expects someone reporting ISMS performance to top management. If the auditor cannot identify the person, finding.
- **Resource gap.** ISMS objectives are ambitious but the team is one part-time person with no budget. Auditor probes whether 5.1 ("ensuring resources needed are available") is met.

## Common implementation gaps

- **Theatre commitment.** CEO signs the policy once at certification and never reviews it. The 5.1 obligation is continuous, not point-in-time.
- **CISO as scapegoat.** Roles register makes the CISO accountable for outcomes the CISO does not control (e.g., dev team's secure coding practices). 5.3 should distribute accountability with authority.
- **Policy disconnect from objectives.** Policy says "we are committed to confidentiality, integrity, availability" but Cl 6.2 objectives are about audit certification rather than C-I-A outcomes. The objectives flow from the policy; mismatch is a Cl 6.2 finding traceable to Cl 5.2.
- **No process to update policy.** Cl 5.2 requires the policy to be "appropriate to the purpose of the organization." Org pivots, scope changes, threat landscape moves; policy must be reviewed and revised.

## SRE and AI-agent fit notes

- **AI-agent operations belong in the policy.** A modern :2022 policy should explicitly cover AI / agent operations: who can deploy autonomous agents, what scopes they have, who reviews their actions, the kill-switch authority.
- **CISO or equivalent for autonomous systems.** If the org operates production autonomous agents, the management representative role should explicitly include AI-system risk reporting (which will increasingly map to ISO 42001 obligations).
- **Role boundary between agent and human.** Cl 5.3 expects clear human accountability. Autonomous-agent decisions that affect customer data must roll up to a named human owner. Document the chain.
- **Resource sufficiency for AI risk.** Allocating zero budget to threat-intelligence subscriptions, monitoring tooling, and external red-teaming while operating production agents is a 5.1 weakness. Auditor will probe if the audit cycle catches up to AI-system practice.

## Stefan-context implementation sketch

- Top management: Stefan + client engagement counterpart on client-bound work. For personal vault operations, top management = Stefan.
- Policy: short statement covering vault classification & handling, vendor-API authorization, agent-action scope, federation peer trust assumptions.
- Roles: personal infra has one role (operator). For client work, RACI maps to client side. Document the model-vendor relationship per engagement.
- Resource: budget line for Anthropic / OpenAI / vendor subscriptions, hardware (Mac Studio retrieval router), accredited audit if procurement signal warrants.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Clause 4 Context]] · [[ISO 27001 Clause 6 Planning]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (specifically A.5.1 policies for information security, A.5.2 information security roles and responsibilities, A.5.4 management responsibilities)
