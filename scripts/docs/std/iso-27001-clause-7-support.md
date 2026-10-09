title: ISO 27001 Clause 7 Support
summary: ISO 27001 Clause 7 Support, from the knowledge vault.
parent: iso-27001
order: 100
labels: clause-7, iso-27001, iso-clause
aliases: ISO 27001 Clause 7 | ISO 27001 Support | ISO 27001 Resources | ISO 27001 Competence | ISO 27001 Awareness | ISO 27001 Communication | ISO 27001 Documented Information
type: iso-clause
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Clause 7 Support.md
reviewed: no
---
## Sub-clause map

- **7.1** Resources — determine and provide resources needed for ISMS establishment, implementation, maintenance and continual improvement.
- **7.2** Competence — determine competence needed for ISMS-relevant work; ensure persons are competent; take actions to acquire missing competence; retain documented evidence.
- **7.3** Awareness — persons doing work under org control shall be aware of the policy, their contribution to ISMS effectiveness (including the benefits of improved performance), and the implications of not conforming.
- **7.4** Communication — internal and external communications relevant to the ISMS: what, when, with whom, how, who communicates.
- **7.5** Documented information — three sub-sub-clauses:
  - **7.5.1** General — required documented information per the standard plus what the org determines.
  - **7.5.2** Creating and updating — identification, format, review and approval.
  - **7.5.3** Control of documented information — access, distribution, storage and preservation, version control, retention and disposition. Controls external documents and obsolete documents.

## Key "shall" requirements (verbatim selections from :2022)

- 7.2: the org shall:
  - "a) determine the necessary competence of person(s) doing work under its control that affects its information security performance;
  - b) ensure that these persons are competent on the basis of appropriate education, training, or experience;
  - c) where applicable, take actions to acquire the necessary competence, and evaluate the effectiveness of the actions taken;
  - d) retain appropriate documented information as evidence of competence."
- 7.3: persons "shall be aware of:
  - a) the information security policy;
  - b) their contribution to the effectiveness of the information security management system, including the benefits of improved information security performance;
  - c) the implications of not conforming with the information security management system requirements."
- 7.4: org shall determine the need for internal and external communications including:
  - "a) on what to communicate;
  - b) when to communicate;
  - c) with whom to communicate;
  - d) how to communicate."
- 7.5.2: when creating and updating documented information the org shall ensure appropriate "a) identification and description (title, date, author, reference number); b) format (language, software version, graphics) and media (paper, electronic); c) review and approval for suitability and adequacy."
- 7.5.3: documented information required by the ISMS and by the standard shall be controlled to ensure "a) it is available and suitable for use, where and when it is needed; b) it is adequately protected (loss of confidentiality, improper use, loss of integrity)" — and controlled for distribution, access, retrieval, storage, preservation, change control, retention and disposition.

## Changes from :2013

- **7.4 wording tightened** to four explicit communication parameters (a-d). :2013 added a fifth "by whom" — :2022 absorbs this into the four-item structure with no substantive change in expectation.
- **7.5 substantively unchanged.** Wording aligned with Annex SL.

## Evidence artefacts an auditor expects

- **Resource plan / budget** — security spend visible.
- **Competence framework** — required competencies per ISMS role, mapped to people, with gap remediation actions (training, hiring, external support).
- **Training records** — completed training, dates, attendees, content.
- **Awareness programme** — onboarding security module, recurring refreshers, role-targeted awareness (developers vs ops vs HR vs sales), phishing exercises, internal comms artefacts.
- **Communication plan** — who communicates what to whom, internal channels (intranet, all-hands, security newsletter) and external channels (regulator notifications, customer breach notifications, supplier communications).
- **Documented information register** — list of all controlled documents, owner, last-reviewed date, next-review date, location.
- **Document control procedure** — covers creation, review, approval, distribution, retention, disposition.
- **Version-controlled storage** — git, SharePoint with versioning, document management system, or equivalent. Read access for everyone who needs the document; write controlled by document owner.
- **External documents register** — vendor terms, regulator publications, standards, controlled and tracked.
- **Records retention schedule** — how long each record type is kept (often 7 years for audit logs, 3 cycles for ISMS records, longer for certain regulatory artefacts).

## Typical audit observations

- **Training is generic.** Off-the-shelf online module, "security awareness 101." Not role-targeted. Auditor expects developers to have secure-coding training, ops to have incident-response training, HR to have personal-data handling training. Generic-only = minor nonconformity.
- **Awareness metrics absent.** Phishing-exercise click rates not tracked. Cl 7.3.b ("benefits of improved performance") not visible without measurement.
- **Onboarding gap.** New joiner reads the policy on day one and never sees it again. Cl 7.3 is continuous; awareness must persist.
- **Communication plan written, not used.** Auditor asks: when was the last external comms about the ISMS sent? If no one can recall, finding.
- **Document control inconsistent.** Policies versioned and dated; procedures live in Google Docs without version metadata. Cl 7.5.3 nonconformity.
- **Obsolete documents in circulation.** Old policy reachable via internal search; superseded version not marked. Cl 7.5.3 nonconformity.
- **Competence claimed, not evidenced.** "The CISO is competent" — but no CISSP / CISM / ISO 27001 Lead Auditor / equivalent training or experience documented. Cl 7.2.d nonconformity.

## Common implementation gaps

- **The "documented information" trap.** Orgs over-document, generating procedures that nobody reads and that drift from actual practice. Cl 7.5 requires control of documented information; it does not require documenting everything. The standard's expectation: document what is required by 7.5.1 ("documented information required by this document" — i.e., the artefacts the standard explicitly requires) plus what the org determines necessary for effectiveness. Over-documenting creates maintenance burden without security gain.
- **Read access too tight.** Procedures locked to a security team folder, so the people who need to follow them cannot find them. Cl 7.5.3 wants availability where and when needed.
- **External documents not tracked.** Vendor SaaS terms, regulator notices, threat intel reports, standard updates — all are external documents. Cl 7.5 covers them; most orgs forget.
- **Records vs documents conflation.** Documents capture intent (policy, procedure). Records capture evidence (training log, audit log, incident report). Both are documented information under :2022 wording. Procedures should distinguish.

## SRE and AI-agent fit notes

- **Competence for AI-system work.** A "secure coding" training that does not cover prompt injection, tool-use scope, output-validation patterns, and OWASP LLM Top 10 is incomplete for any team operating production AI features. Cl 7.2 evaluation in :2022+ should test for this.
- **Awareness for autonomous-agent operations.** End users (employees) need to know what AI agents are doing on their behalf, what data the agents touch, and how to escalate concerns. Cl 7.3 maps naturally; the implementation is novel.
- **Documented agent system prompts and tool scopes.** Cl 7.5 control of documented information applies to system prompts, tool definitions, model versions, and policy boundaries embedded in prompts. Version them. Review them. They are policy artefacts, not just code.
- **Audit log retention for agent actions.** Cl 7.5.3 retention rules apply to agent action logs. Decide retention period explicitly (12 months default for personal infra; longer for client work depending on contract / regulation).
- **External-documents register for vendor TOS shifts.** Anthropic, OpenAI, vendor terms shift regularly. The version under which the org's controls were designed may differ from the current version. Track them as external documented information.

## Stefan-context implementation sketch

- Resources: hardware (Macbook canonical, Mac Studio incoming, [host], AWS headscale), software (vendor APIs, OpenCode plus opskit plugin, bd, vault tooling).
- Competence: maintained via continuous learning, course progress (UTT), client engagements, plus formal credentials where buyer signal warrants.
- Awareness: self-applied for solo work; for client work, the awareness obligation flows from client. Document mutual expectations.
- Communication: internal = single operator; external = engagement-specific comms plans with clients.
- Documented information: vault itself is the documentation regime. Git history = version control. AGENTS.md, CLAUDE.md, and per-corpus index files are policy-equivalent. Status lifecycle in `KNOWLEDGE-FRAMEWORK.md` covers Cl 7.5.3 retention and disposition for atoms.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Clause 6 Planning]] · [[ISO 27001 Clause 8 Operation]]
- [[ISO 27001 Annex A.6 People Controls]] (A.6.3 information security awareness, education and training; A.6.4 disciplinary process)
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.10 acceptable use; A.5.37 documented operating procedures)
