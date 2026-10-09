title: GDPR Cross-Border Transfers
summary: Chapter V (Articles 44-50) governs transfers of personal data to third countries (outside EU/EEA) and international organizations.
parent: gdpr
order: 100
labels: gdpr, regulation-concept
aliases: GDPR Cross-Border Transfers | GDPR International Transfers | GDPR Chapter V | GDPR Schrems II | GDPR Adequacy | GDPR SCCs | GDPR BCRs | EU-US Data Privacy Framework
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/gdpr/GDPR Cross-Border Transfers.md
reviewed: no
---
> Chapter V (Articles 44-50) governs transfers of personal data to third countries (outside EU/EEA) and international organizations. Multiple transfer mechanisms available: adequacy decisions, appropriate safeguards (SCCs, BCRs, codes, certifications), derogations. The Schrems II ruling (July 2020) reshaped the landscape; the EU-US Data Privacy Framework (July 2023) restored a US-specific path.

## General principle (Article 44)

Transfer of personal data to third country / international organization only takes place if:

- Conditions of Chapter V complied with.
- Provisions of GDPR more generally complied with.

No transfer permitted that would undermine GDPR protection.

## Adequacy decisions (Article 45)

Commission can decide that third country / sector / international organization ensures adequate level of protection. Adequacy decision allows free flow of data; no additional safeguards required.

Adequacy assessment factors:

- Rule of law, fundamental rights, relevant legislation (data protection, public security, defence, national security, criminal law, public authority access).
- Independent supervisory authorities.
- International commitments.

Periodic review required (at least every four years).

Current adequacy decisions (as of 2026-05-12):

- Andorra
- Argentina
- Faroe Islands
- Guernsey
- Isle of Man
- Israel
- Japan (commercial sector)
- Jersey
- New Zealand
- South Korea
- Switzerland
- United Kingdom (post-Brexit; review pending periodically)
- Uruguay
- **United States** — under EU-US Data Privacy Framework (July 2023), for certified organizations only

Withdrawn adequacy decisions historically: US Safe Harbor (Schrems I, 2015), US Privacy Shield (Schrems II, 2020).

## Appropriate safeguards (Article 46)

Where adequacy decision doesn't apply, transfer subject to appropriate safeguards. Options:

### (a) Legally binding and enforceable instrument between public authorities/bodies

For public-sector transfers.

### (b) Binding Corporate Rules (BCRs)

Article 47 details. For intra-group transfers within multinational organizations.

BCRs require:

- Approval by competent supervisory authority.
- Legally binding on each member of group.
- Enforceable rights for data subjects.
- Coverage of standard requirements per Article 47(2).

BCR approval is multi-year, multi-DPA process. Practical for large multinationals; impractical for smaller orgs.

### (c) Standard Contractual Clauses (SCCs)

Adopted by Commission. Most widely used safeguard for non-adequacy transfers.

Current SCCs: Commission Implementing Decision (EU) 2021/914, June 2021. Modular structure covering:

- Module 1: Controller to controller
- Module 2: Controller to processor
- Module 3: Processor to processor
- Module 4: Processor to controller

Older SCCs (2001, 2010) had to be repapered to 2021 SCCs by 27 December 2022.

### (d) SCCs adopted by supervisory authority

Approved by Commission.

### (e) Approved code of conduct (Article 40) with enforceable commitments

In a third country.

### (f) Approved certification mechanism (Article 42) with enforceable commitments

In a third country.

### (g) Ad-hoc contractual clauses with supervisory authority approval

Bespoke; rarely used in practice.

## Schrems II ruling (2020) and supplementary measures

**Case C-311/18 Schrems II (July 2020)** had major impact:

- Invalidated the EU-US Privacy Shield adequacy decision.
- Confirmed SCCs valid in principle.
- Required transfer-impact assessment: controllers must assess whether SCCs are sufficient in the destination country, considering local law access by public authorities.
- Where SCCs insufficient: supplementary measures required (technical, contractual, organizational) or transfer cannot proceed.

Implications:

- Controllers must conduct transfer-impact assessment (TIA) per transfer.
- Supplementary measures may include encryption, pseudonymization, contractual clauses adding rights, organizational measures.
- For destinations with substantial public authority access (US under FISA 702, China, Russia, others): supplementary measures often technically demanding.
- Encryption with EU-held keys is the strongest technical supplementary measure.

EDPB guidelines on supplementary measures (Recommendations 01/2020, finalized June 2021) provide framework.

## EU-US Data Privacy Framework (July 2023)

After Schrems II invalidated Privacy Shield, EU and US negotiated successor framework:

- **Executive Order 14086** (October 2022) — US-side commitments including:
  - Limitations on US signals intelligence activities (necessity / proportionality).
  - Data Protection Review Court for EU complainant redress.
- **Commission Implementing Decision (EU) 2023/1795** — July 2023 adequacy decision for EU-US transfers to certified US organizations.

Operation:

- US organizations self-certify under the DPF (administered by US Department of Commerce).
- Certified organizations subject to DPF Principles enforced by FTC and DOT.
- EU-to-US transfers to certified organizations covered by adequacy decision.
- Periodic Commission review.

Status as of 2026-05-12:

- DPF operational since July 2023.
- Many major US tech companies certified.
- Schrems III challenge pending in CJEU (filed by noyb). Outcome plausibly 2026-2027.
- If invalidated, organizations revert to SCCs + supplementary measures.

For transfers to non-certified US organizations: SCCs required (with Schrems II supplementary measures assessment).

## UK adequacy (post-Brexit)

- UK adequacy decision: Commission Implementing Decision (EU) 2021/1772, June 2021.
- Allows EU-UK personal data transfers without additional safeguards.
- Sunset clause: four-year automatic expiry unless renewed (2025).
- Renewal process underway 2025-2026.

## Derogations for specific situations (Article 49)

In absence of adequacy decision or appropriate safeguards, transfer permitted on narrow grounds:

- (a) Explicit consent after being informed of risks.
- (b) Necessary for contract performance with data subject.
- (c) Necessary for contract performance in data subject's interest.
- (d) Important public interest reasons (EU or member state law).
- (e) Establishment, exercise, defence of legal claims.
- (f) Vital interests of data subject (where incapable of consent).
- (g) Transfer from public register (with limits).
- Additional narrow derogations.

Derogations are exceptions and interpreted narrowly. EDPB Guidelines 2/2018 caution against using as routine basis.

## Onward transfers

When data transferred from EU to third country and then transferred onward to another third country, the second transfer is also a cross-border transfer subject to Chapter V.

SCC Module 3 (processor to processor) addresses some onward transfer scenarios. BCRs typically cover within-group onward transfers.

## Practical transfer assessment workflow

For each transfer:

1. **Identify transfer**: is data flowing to a third country or international organization?
2. **Check adequacy**: is destination covered by adequacy decision? If yes, transfer permissible.
3. **Choose safeguard**: if no adequacy, select SCCs, BCRs, code, certification, or ad-hoc.
4. **Conduct TIA (post-Schrems II)**: assess whether safeguard provides essentially equivalent protection in destination.
5. **Apply supplementary measures** if needed.
6. **Document**: maintain transfer records per Article 30.
7. **Inform data subjects** per Article 13/14 information rights.

Transfer-impact assessment depth varies with destination risk. EU-US under DPF: lighter assessment for certified organizations. EU-US non-DPF or high-risk destinations: substantial assessment with technical measures.

## Notable transfer-related enforcement

- **Meta €1.2B fine** (May 2023, Ireland DPC): for EU-US data transfers under SCCs without sufficient supplementary measures. Pre-dated DPF; DPF subsequently provided remediation path.
- **TikTok €345M fine** (September 2023, Ireland DPC): involved transfers among other issues.
- **Uber €290M fine** (August 2024, Netherlands DPA): for international transfer issues.

Transfer-related enforcement is significant; willful or careless transfer practice attracts large penalties.

## SRE and AI-agent fit notes

### Transfers to model providers

- Anthropic, OpenAI, Google, Cohere, others are US-based primarily.
- Most are certified under EU-US Data Privacy Framework; transfers to certified entities covered by adequacy.
- Non-certified providers: SCCs + Schrems II supplementary measures required.
- For high-stakes processing: supplementary measures (encryption with EU-held keys, pseudonymization, contractual additions) regardless of DPF coverage.

### Transfer assessment for AI features

For each AI feature involving cross-border processing:

- Identify destination country / region per processing step.
- Check provider's transfer mechanism (DPF certification, SCCs, etc.).
- Document supplementary measures if used.
- Update transfer records per Article 30.

### Schrems III consequences (if/when materializes)

If DPF invalidated:

- Revert to SCCs + supplementary measures for EU-US transfers.
- Some processing may become unviable without technical supplementary measures.
- Watch CJEU docket and EDPB guidance.

### Vendor due diligence transfer items

For each model / AI vendor:

- DPF certification status (if US-based)
- SCC module used
- Sub-processor list and their transfer mechanisms
- Encryption / pseudonymization commitments
- Audit / inspection rights

## Stefan-context implementation sketch

- Vault: largely personal data of self; transfers irrelevant.
- For client work: identify all cross-border transfers; ensure DPF certification or SCCs in place; document supplementary measures.
- Anthropic (primary AI vendor): track DPF certification status; align engagement-level DPA references.
- For prototype / sensitive data scenarios (TISAX Prototype Protection): cross-border transfer often restricted or prohibited by client contract regardless of GDPR mechanism.

## See also

- [[GDPR Cluster|cluster MOC]] · [[GDPR Principles]] · [[GDPR Lawful Bases]] · [[GDPR Controller and Processor]] · [[GDPR Enforcement and DPAs]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.20 supplier agreements; A.5.34 PII)
- [[ISO 27001 Annex A.8 Technological Controls]] (A.8.24 cryptography supports supplementary measures)
