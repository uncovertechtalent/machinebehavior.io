title: NIS2 vs ISO 27001
summary: NIS2 is regulation; ISO 27001 is voluntary standard.
parent: nis2
order: 100
labels: cross-cutting, iso-27001, nis2
aliases: NIS2 vs ISO 27001 | ISO 27001 vs NIS2 | NIS2 ISO 27001 Mapping
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nis2/NIS2 vs ISO 27001.md
reviewed: no
---
> NIS2 is regulation; ISO 27001 is voluntary standard. Strong content overlap — Article 21 measures map heavily to Annex A controls. ISO 27001 certification supports NIS2 compliance but does not substitute. Combined implementation is the practical path for in-scope entities.

## Side-by-side mechanics

| Aspect | NIS2 | ISO 27001 |
|---|---|---|
| Type | Regulatory directive | Voluntary standard |
| Source | EU + Member State transposition | ISO/IEC |
| Recognition | Compliance with regulation | Certification |
| Mandatory | For in-scope entities | Voluntary |
| Penalties | €10M / 2% turnover (essential), €7M / 1.4% (important) | None directly |
| Audit | Authority supervision | Third-party certification audit |
| Scope flexibility | Defined by directive + transposition | Org-defined SoA |
| Geographic | EU + Member State | International |
| Update cycle | Regulatory amendment | ~10-year ISO cycle |
| Management accountability | Explicit (Art 20) | Cl 5.1 leadership (lighter) |

## Content overlap

### Article 21 measures → ISO 27001 mapping

| Article 21 measure | Primary ISO 27001 controls |
|---|---|
| (a) Risk analysis + InfoSec policies | Cl 6.1.2 risk assessment, A.5.1 policies |
| (b) Incident handling | A.5.24-A.5.28 incident management |
| (c) Business continuity | A.5.29-A.5.30 (also ISO 22301) |
| (d) Supply chain security | A.5.19-A.5.23 supplier relationships |
| (e) Secure development | A.8.25-A.8.30 SDLC controls |
| (f) Measure effectiveness | Cl 9 performance evaluation |
| (g) Cyber hygiene + training | A.6.3 awareness/training, Cl 7.2 competence |
| (h) Cryptography | A.8.24 cryptography |
| (i) HR security + access + asset mgmt | A.5.9-A.5.18 + A.6 |
| (j) MFA + secured comms | A.5.17 + A.8.5 + A.8.21 |

Coverage estimate: ISO 27001 implementation provides 70-85% of Article 21 substantive coverage.

### Management system overlap

NIS2 Article 20 management body accountability + Article 21(f) effectiveness assessment + Article 23 incident reporting + record-keeping obligations → ISO 27001 Cl 4-10 management system substantially provides the management-system infrastructure.

## What NIS2 covers that ISO 27001 does not directly

- **Regulatory enforcement.** ISO 27001 has no penalty mechanism; NIS2 does.
- **Mandatory scope and timing.** ISO 27001 scope is org-defined; NIS2 scope is regulatory.
- **Incident reporting timelines.** 24h/72h/1m timelines are NIS2-specific (though parallel to GDPR breach reporting).
- **Sector-specific obligations.** NIS2 has sector tailoring; ISO 27001 is generic.
- **Management body specifics.** NIS2 Article 20 is more prescriptive on management body involvement than ISO 27001 Cl 5.
- **Cooperation obligations.** With authorities, CSIRTs, other entities — NIS2-specific.

## What ISO 27001 covers that NIS2 does not directly

- **Certifiable mechanism.** Third-party attestation infrastructure.
- **Detailed control set.** 93 Annex A controls vs Art 21's 10 categories.
- **SoA mechanism.** Standardized scope/coverage documentation.
- **International recognition.** ISO 27001 cert recognized globally; NIS2 is EU.
- **Procurement signal.** ISO 27001 cert is procurement-readable; NIS2 compliance harder to communicate.

## Combined implementation pattern

For NIS2-scope entities already certified to ISO 27001:

1. **Map ISO 27001 implementation to Article 21 categories.** Most coverage exists.
2. **Identify NIS2-specific gaps.** Typically:
   - 24h incident-reporting capability
   - Management body training and approval records (Article 20)
   - Supply chain due diligence depth (Article 21(d))
   - Sector-specific requirements per Member State implementing acts
3. **Build NIS2-specific evidence packages.** Authorities expect different evidence formats than ISO auditors.
4. **Integrate incident response.** Single workflow covering ISO 27001 incident management + GDPR breach response + NIS2 incident reporting + sector-specific.

### Effort estimate

For an ISO 27001-certified essential entity adding NIS2 compliance: 20-40% incremental implementation effort.

For a non-ISO-27001 entity implementing both: typically pursue ISO 27001 first (clearer implementation guidance, certifiable signal); then NIS2 compliance layered on.

## Combined audits not yet established

ISO 27001 certification audits and NIS2 supervisory audits are separate processes by different parties (ISO certification body vs national competent authority). No combined-audit mechanism currently. Some certification bodies offer "NIS2-readiness assessment" services as adjuncts to ISO 27001 audits; not a regulatory substitute.

## What ISO 27001 certification does for NIS2 compliance

- **Strong baseline evidence.** Certification demonstrates substantive cybersecurity management.
- **Mitigating factor** in penalty determination (Article 34(3) — cooperation/effort considered).
- **Audit-trail infrastructure** transfers.
- **Procurement leverage** for NIS2-affected supply chains.

What ISO 27001 certification does NOT do:

- **Substitute for NIS2 compliance.** Authority can find NIS2 non-compliance regardless of cert.
- **Cover NIS2-specific obligations** (24h reporting, management body, sector-specifics) without targeted work.
- **Eliminate authority supervision** for in-scope entities.

## Recommendation patterns

### For new implementations

If org is NIS2-scope and not ISO-certified:

- Start with ISO 27001 implementation (provides ~70-85% of NIS2 substantive baseline).
- Layer NIS2-specific requirements (incident reporting, supply chain depth, management body).
- Pursue ISO 27001 cert when budget allows; NIS2 compliance is mandatory regardless.

### For existing ISO 27001 holders

If org is NIS2-scope and ISO-certified:

- Map existing ISO 27001 implementation to Article 21.
- Identify gaps; remediate.
- Build NIS2-specific evidence packages.
- Update incident response workflow for NIS2 timelines.

### For non-NIS2-scope orgs

ISO 27001 alone provides robust cybersecurity baseline. NIS2 alignment optional unless future scope expansion expected.

## See also

- [[NIS2 Cluster|cluster MOC]] · [[NIS2 Security Measures]]
- [[ISO 27001 Cluster|ISO 27001]] · [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
