title: ISO 42001 vs ISO 27001 Integration
summary: ISO/IEC 42001 (AI Management System) and ISO/IEC 27001 (Information Security Management System) are sibling Annex SL standards with substantial structural overlap and partial content overlap.
parent: iso-42001
order: 100
labels: cross-cutting, iso-27001, iso-42001
aliases: ISO 42001 vs ISO 27001 | ISO 42001 ISO 27001 Integration | AIMS ISMS Integration | ISO 42001 Combined Implementation
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-42001/ISO 42001 vs ISO 27001 Integration.md
reviewed: no
---
> ISO/IEC 42001 (AI Management System) and ISO/IEC 27001 (Information Security Management System) are sibling Annex SL standards with substantial structural overlap and partial content overlap. Most organizations pursuing both implement them as an integrated management system, with combined audits. This atom maps the integration mechanics.

## Side-by-side mechanics

| Aspect | ISO 27001:2022 | ISO 42001:2023 |
|---|---|---|
| Scope | Information security | AI management |
| Published | 2022-10-25 | 2023-12-18 |
| Annex SL alignment | Yes | Yes |
| Mandatory clauses | 4-10 | 4-10 (parallel) |
| Annex A controls | 93 | ~38 |
| Annex A themes | 4 (Organizational, People, Physical, Technological) | 10 control-objective areas |
| Risk-based | Yes | Yes (plus impact assessment) |
| SoA required | Yes | Yes |
| Lifecycle concept | Implicit | Explicit (AI system lifecycle) |
| Impact assessment | Information-security-related | AI-system-impact-specific |
| Certifiable | Yes | Yes |
| Audit overlap | n/a | High with ISO 27001 |

## Clause-level overlap

Clauses 4-10 mirror each other structurally. Content-level overlap:

- **Cl 4 Context**: same approach; AIMS adds AI-specific interested parties (data subjects, affected communities, AI ethics advisors).
- **Cl 5 Leadership**: same approach; AIMS requires AI policy distinct from but compatible with InfoSec policy.
- **Cl 6 Planning**: parallel risk assessment / risk treatment processes; AIMS adds 6.1.4 AI system impact assessment as distinct activity.
- **Cl 7 Support**: same approach; AIMS adds AI-specific competence requirements.
- **Cl 8 Operation**: parallel operational risk assessment / treatment / impact assessment.
- **Cl 9 Performance evaluation**: same approach; both internal-audit and management-review structures parallel.
- **Cl 10 Improvement**: identical structure.

Implementation work: most clause-level documentation can be authored once and referenced by both management systems. Integration is straightforward.

## Annex A control overlap

ISO 27001 Annex A (93 controls in 4 themes) and ISO 42001 Annex A (~38 controls in 10 control-objective areas) have substantial overlap, particularly:

- **Asset management** — ISO 27001 A.5.9 (information assets) ≈ ISO 42001 A.4 (AI resources, including data, tooling, infrastructure, human resources).
- **Classification and labelling** — ISO 27001 A.5.12 / A.5.13 ≈ ISO 42001 A.7 (data for AI systems classification, provenance).
- **Supplier relationships** — ISO 27001 A.5.19-A.5.23 ≈ ISO 42001 A.10 (third-party and customer relationships, particularly model-provider relationships).
- **Access control** — ISO 27001 A.5.15-A.5.18 + A.8.2 ≈ ISO 42001 A.4 + A.9 (use of AI systems with appropriate access controls).
- **Incident management** — ISO 27001 A.5.24-A.5.28 ≈ ISO 42001 A.8.4 (AI-specific incident communication aspects).
- **Cryptography** — ISO 27001 A.8.24 ≈ implicit in ISO 42001 (cryptography applies to AI data and model handling).
- **Logging and monitoring** — ISO 27001 A.8.15 / A.8.16 ≈ ISO 42001 A.6.2.8 (AI system event logging).
- **Configuration management** — ISO 27001 A.8.9 ≈ ISO 42001 A.6 (AI system configuration including model versions, prompts, tool scopes).
- **Secure development** — ISO 27001 A.8.25 / A.8.27 / A.8.28 ≈ ISO 42001 A.6.1-A.6.2 (responsible AI development).

ISO 42001 Annex A also covers content not directly in ISO 27001:

- **Impact assessment** (A.5) — ISO 27001 has no equivalent; ISO 27701 (PIMS) has data protection impact assessment with different focus.
- **AI system lifecycle** (A.6) — ISO 27001 implicit in development controls; ISO 42001 explicit.
- **Information to interested parties about AI** (A.8) — ISO 27001 doesn't address user-facing AI transparency.
- **Use of AI systems** (A.9) — ISO 27001 doesn't address employees / org as AI consumer.

## Integration patterns

Three common patterns for combined ISO 27001 + ISO 42001 implementation:

### Pattern 1: ISO 27001 first, ISO 42001 added

Common for orgs already certified to ISO 27001. Steps:

1. Extend Cl 4 scope to include AIMS where applicable.
2. Author AI policy aligned with existing InfoSec policy.
3. Extend risk register with AI-specific risks.
4. Add AI system impact assessment process.
5. Build AI system inventory and lifecycle tracking.
6. Map Annex A control overlap; add ISO 42001 Annex A controls not covered.
7. Update SoA with combined coverage.
8. Engage certification body for combined audit or sequential audits.

Effort: 30-50% of ISO 42001 implementation effort already done via ISO 27001.

### Pattern 2: ISO 27001 + ISO 42001 simultaneously

For orgs without prior certification choosing both at once. Steps:

1. Single management-system scope covering both.
2. Combined risk methodology and risk register (with AI-specific sub-register).
3. Combined controls implementation against unified SoA.
4. Combined internal audit programme.
5. Combined management review.
6. Combined certification audit.

Effort: 70-85% of dual-implementation effort vs running both separately.

### Pattern 3: ISO 42001 first, ISO 27001 added later

Less common but viable for AI-first orgs. Steps:

1. Implement ISO 42001 standalone.
2. Identify InfoSec content already covered.
3. Add ISO 27001 Annex A controls not yet covered.
4. Build out management-system content for ISO 27001 scope (often broader than ISO 42001 scope).
5. Extend SoA.

Effort: 40-60% of ISO 27001 implementation already done via ISO 42001 — but ISO 27001 covers more breadth so additional work is meaningful.

## Combined audit mechanics

Audit providers that hold accreditation for both standards offer combined audits. Common practice:

- **Combined Stage 1**: single documentation review covering both management systems.
- **Combined Stage 2**: single on-site / remote audit; auditor samples both ISMS and AIMS controls.
- **Sampling per standard**: auditor selects samples from each Annex A; some controls satisfy both audits.
- **Combined report**: single report with findings categorized per standard.
- **Combined certification**: separate certificates issued, single audit engagement.

Cost saving: typically 20-40% vs separate audits.

Audit providers offering combined audits include BSI, DNV, TÜV Süd, TÜV Rheinland, LRQA, Schellman, A-LIGN. Capability for the combined audit varies; confirm AI-specific competence with the provider.

## Documentation integration

Combined documentation set:

- **Single management system manual** covering both (or two compact manuals cross-referencing each other).
- **Single context analysis** with AI-specific section.
- **Single interested parties register** with stakeholder categorization (some are AI-specific).
- **Single risk methodology** with AI-specific risk categories.
- **Two risk registers** (or one with explicit AI flag) — separation aids per-standard review.
- **Combined SoA** with per-control standard mapping.
- **Single internal audit programme** covering both.
- **Single management review** with both standards on the agenda.

Documentation overhead is dominated by ISO 27001 with ~10-20% incremental for ISO 42001.

## Integration with ISO 27701 (privacy)

Three-way integration (ISO 27001 + ISO 27701 + ISO 42001) is increasingly common for orgs handling personal data in AI systems:

- **ISO 27001** — InfoSec management spine.
- **ISO 27701** — privacy extension; PIMS controls on top of ISMS.
- **ISO 42001** — AI management; impact assessment covers AI-system effects including privacy effects.

Overlap on data subject rights, data protection impact assessments, PII processor relationships. Mapping documents (planned ISO/IEC TR or similar) expected to deepen the integration story through 2025-2027.

## SRE and AI-agent fit notes

- **Combined implementation is the default for AI-feature SaaS.** SaaS orgs serving enterprise customers typically need both. Single management system, combined audits.
- **For agent systems**: ISO 42001 covers the AI-specific operational controls; ISO 27001 covers the underlying InfoSec controls. Together they cover the system; separately each leaves gaps.
- **For model-vendor relationships**: ISO 27001 A.5.19-A.5.23 + ISO 42001 A.10 together cover the relationship lifecycle from due diligence through performance monitoring. Vendor due-diligence packages should address both.
- **For audit log retention**: ISO 27001 A.8.15 (logging) + ISO 42001 A.6.2.8 (AI system event logging) together cover the retention. Single log infrastructure satisfies both with appropriate retention policy.

## Stefan-context implementation sketch

- Solo / small-team operation: not currently warranted to certify either. Implement aligned-but-not-certified.
- For client engagements: client may be certified to ISO 27001 and/or ISO 42001; supplier flow-down obligations apply. Document compliance with relevant clauses per client requirement.
- Re-evaluate certification when client portfolio reaches the scale where dual-cert positioning is commercially significant — likely a 2027+ horizon for solo operations.

## See also

- [[ISO 42001 Cluster|cluster MOC]] · [[ISO 42001 Clause Structure]] · [[ISO 42001 Annex A Controls]] · [[ISO 42001 Certification Process]]
- [[ISO 27001 Cluster|ISO 27001]] · [[ISO 27001 Family and Sector Variants]]
