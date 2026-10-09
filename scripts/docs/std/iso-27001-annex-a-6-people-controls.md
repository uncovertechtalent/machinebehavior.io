title: ISO 27001 Annex A.6 People Controls
summary: Eight controls covering the human element of the ISMS: screening, contractual obligations, awareness and training, disciplinary process, post-employment obligations, NDAs, remote work, and event reporting.
parent: iso-27001
order: 100
labels: annex-a-theme, iso-27001, theme-people
aliases: ISO 27001 Annex A.6 | ISO 27001 People Controls | Annex A.6 Controls
type: annex-a-theme
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Annex A.6 People Controls.md
reviewed: no
---
> Eight controls covering the human element of the ISMS: screening, contractual obligations, awareness and training, disciplinary process, post-employment obligations, NDAs, remote work, and event reporting. Smallest theme by control count; the human element is consistently the largest breach-cause category, so the controls' weight is disproportionate to their number.

## How to read this atom

Each control listed below has its reference number and title from ISO 27001:2022 Annex A. Notes cover purpose, typical implementation, common evidence, SRE / AI-agent fit notes.

No new controls in A.6 in :2022 (consolidations from :2013's A.7 People + parts of A.13).

## A.6.1 Screening

Background verification of candidates for employment, contractors, and third-party users proportionate to the role, the access to be granted, and the classification of information they will handle. Re-screening at planned intervals for sensitive roles.

Common practice: identity verification, right-to-work check, reference checks, criminal-record check (jurisdiction-dependent), credit check (for roles handling financial systems), social media review (more contested).

Evidence: screening procedure, sample of completed screenings (redacted), supplier flow-down to background-screening provider.

## A.6.2 Terms and conditions of employment

Employment contracts state the employee's and the org's responsibilities for information security. Confidentiality clauses, acceptable use commitments, post-termination obligations, IP assignment.

Evidence: contract template, signed contracts, clause-tracking.

## A.6.3 Information security awareness, education and training

Personnel receive appropriate awareness, education, and training. Onboarding plus periodic refreshers plus role-targeted modules.

Mirrors Cl 7.2 (competence) and Cl 7.3 (awareness).

AI-agent fit: awareness for AI tool use (acceptable inputs, output trust calibration, prompt-injection recognition), training for engineers building AI features (OWASP LLM Top 10, secure prompting, tool-scope design, output validation), executive awareness on AI risk (model-vendor relationships, customer-facing AI accountability, AI Act obligations).

Evidence: training curriculum mapped to roles, completion records, refresher cadence, content currency (when was the AI-awareness module last updated?), effectiveness measurement (phishing click rate, knowledge test scores, observed behavior).

## A.6.4 Disciplinary process

Formal disciplinary process for personnel committing a security breach. Communicated, documented, applied consistently.

Evidence: disciplinary procedure, HR-side records (typically not auditor-accessible at individual level; statistical summary suffices).

## A.6.5 Responsibilities after termination or change of employment

Responsibilities and duties that remain valid post-termination or after a role change. Confidentiality, non-disclosure, return of assets (A.5.11), access removal.

Common gap: long-tail post-termination obligations not communicated. Auditor may interview a recently-promoted internal-mover and ask whether they know which of their previous-role obligations still apply.

## A.6.6 Confidentiality or non-disclosure agreements

NDAs identified, documented, regularly reviewed, signed by personnel and parties as needed.

Common shapes: employee NDA (in contract), contractor NDA (separate document), customer NDA (per engagement), supplier NDA (in supplier contract or standalone).

## A.6.7 Remote working

Security measures for remote work: equipment security, network security (VPN, ZTNA), data-handling rules in home / non-office environments, physical security of home workspace, family / household considerations.

AI-agent fit: BYO-machine considerations. If employees use personal devices for any AI tool access, the security boundary becomes ambiguous. Common implementation: managed devices only for confidential-or-higher data; defined posture requirements (encryption at rest, OS patching cadence, EDR coverage); session-level controls (MFA, conditional access, agent API key scope).

Evidence: remote working policy, equipment provisioning records, posture-check telemetry, secure-network-access architecture description.

## A.6.8 Information security event reporting

Reporting channels for security events. Whistleblower-style accessibility, anonymous reporting option, clear escalation paths, no-blame culture for genuine reports.

Evidence: reporting channel documented, awareness materials referencing it, event-log showing reports flowing in, response-time metrics.

## SRE and AI-agent quick map (load-bearing A.6 controls)

| Concern | Primary A.6 controls |
|---|---|
| Engineer competence for AI-system work | A.6.3 |
| Acceptable use of AI tools | A.6.2 (in contract), A.6.3 (in awareness) |
| Remote / hybrid security posture | A.6.7 |
| Joiner-mover-leaver for human + agent identities | A.6.1, A.6.5, A.5.16, A.5.18 |
| Security event reporting (incl AI-system anomalies) | A.6.8 |

## Common audit observations

- **Awareness is generic.** Same module for engineers, sales, HR. Tailored content expected.
- **AI-specific training absent.** Companies that ship AI features without role-targeted AI security training are increasingly flagged in 2025+ audits.
- **Re-screening cadence missed.** Sensitive roles (admin, finance, security team) screened at hiring, never again. Recommended cadence: 3-5 years for sensitive roles.
- **Remote working policy outdated.** Pre-pandemic policy with strict office-only-confidential rules, never updated to match remote-first reality. Either the policy is being followed and the business is unworkable, or the business has overridden it and the policy is fictional.

## Stefan-context implementation sketch

- Screening: self-applicable for solo work; for client work, screening commitments flow from client side and are honored.
- Terms and conditions: client engagement letters carry the equivalent obligations (confidentiality, IP, post-engagement).
- Awareness / training: continuous self-development; UTT course progress is evidence of competence currency.
- Remote working: 100% remote across Macbook (canonical), Mac Studio (incoming retrieval router), [host] (build host), AWS headscale (control plane). Network security via headscale + Tailscale; device posture per Macbook security defaults plus FileVault, Secure Enclave, MFA on critical accounts.
- Event reporting: self-reporting to bd. For client work, channels documented per engagement.

## See also

- [[ISO 27001 Cluster|cluster MOC]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.7 Physical Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
- [[ISO 27001 Clause 7 Support]] (Cl 7.2 competence, Cl 7.3 awareness)
