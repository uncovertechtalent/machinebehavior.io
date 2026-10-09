title: GDPR Lawful Bases
summary: Article 6 establishes six lawful bases for processing personal data.
parent: gdpr
order: 100
labels: gdpr, regulation-concept
aliases: GDPR Lawful Bases | GDPR Article 6 | GDPR Legal Bases | GDPR Lawful Bases for Processing | GDPR Article 9 Special Category
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/gdpr/GDPR Lawful Bases.md
reviewed: no
---
> Article 6 establishes six lawful bases for processing personal data. Article 9 establishes a stricter regime for special category data. Identifying the correct lawful basis is the foundational compliance step for any processing.

## The six lawful bases (Article 6(1))

### (a) Consent

Data subject has given consent to the processing for one or more specific purposes.

Requirements (Article 7, Recitals 32, 42-43):

- **Freely given** — no imbalance of power, no detriment for refusal.
- **Specific** — for specific purposes, not bundled.
- **Informed** — data subject knows what they consent to.
- **Unambiguous** — clear affirmative action (no pre-ticked boxes per CJEU Planet49).
- **Withdrawable** — as easy to withdraw as to give.
- **Demonstrable** — controller must be able to demonstrate consent given.

For children: parental consent required below age of digital consent (set by member state, 13-16 range).

Common pitfalls:

- Consent as fallback when no other basis applies — fragile if power imbalance present.
- Bundling consent for multiple purposes.
- "Take it or leave it" consent — not freely given.
- Cookie banner consent — quality of consent often questionable.

### (b) Contract

Processing is necessary for performance of a contract with the data subject, or to take steps at the data subject's request prior to entering into a contract.

Scope:

- Processing genuinely necessary for the contract.
- Pre-contractual steps at data subject's request.

Common pitfalls:

- Stretching "necessary" — additional processing beyond what the contract requires.
- Treating contract as basis for processing the contract doesn't strictly need.
- Combining with consent unnecessarily.

### (c) Legal obligation

Processing is necessary for compliance with a legal obligation to which the controller is subject.

Scope:

- Legal obligation in EU or member state law.
- Tax, anti-money-laundering, employment law, sector-specific regulations.

Common usage: compliance reporting, tax records, regulatory submissions.

### (d) Vital interests

Processing is necessary to protect the vital interests of the data subject or another natural person.

Scope:

- Narrow — protecting life or physical integrity.
- Usually emergency situations.

Common usage: emergency medical processing.

### (e) Public task

Processing is necessary for performance of a task carried out in the public interest or in the exercise of official authority vested in the controller.

Scope:

- Public authorities and bodies exercising public authority.
- Private entities exercising specific public-interest functions.

Common usage: government processing, regulatory bodies, public-service providers.

### (f) Legitimate interests

Processing is necessary for the purposes of legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject (especially where the data subject is a child).

Three-part test (often called LIA - Legitimate Interests Assessment):

1. **Purpose test**: is there a legitimate interest?
2. **Necessity test**: is the processing necessary for that interest?
3. **Balancing test**: do the data subject's interests, rights, freedoms override?

Common usage: fraud prevention, security monitoring, direct marketing (with right to object), analytics, AI-feature personalization (with caveats).

Note: not available to public authorities for tasks performed in their official capacity.

Common pitfalls:

- Asserted without conducting / documenting LIA.
- Balancing test not honestly conducted.
- Used as catch-all when other bases would be more appropriate.

## Special category data (Article 9)

Article 9 prohibits processing of special category data except where one of ten exceptions applies. Special category data:

- Racial or ethnic origin
- Political opinions
- Religious or philosophical beliefs
- Trade union membership
- Genetic data
- Biometric data (for unique identification)
- Health data
- Data concerning sex life or sexual orientation

Article 9(2) exceptions:

- (a) Explicit consent.
- (b) Employment, social security, social protection law (with safeguards).
- (c) Vital interests where data subject incapable of consent.
- (d) Not-for-profit body with political/philosophical/religious/trade-union aim (members or contact only).
- (e) Data manifestly made public by data subject.
- (f) Legal claims or judicial capacity of courts.
- (g) Substantial public interest with proportionate safeguards.
- (h) Health-related (preventive medicine, diagnosis, treatment, social/health management) with safeguards.
- (i) Public interest in public health.
- (j) Archiving, research, statistics in public interest with safeguards.

For special category data: need both Article 6 lawful basis AND Article 9 exception.

## Criminal data (Article 10)

Processing of personal data relating to criminal convictions and offences only under:

- Control of official authority, OR
- Authorized by EU or member state law providing appropriate safeguards.

Comprehensive register of criminal convictions only under control of official authority.

## Choosing a lawful basis

Process:

1. Identify the processing activity precisely (specific purpose).
2. Consider each lawful basis in turn.
3. Choose the most appropriate basis — not the most flexible, the most appropriate.
4. Document the choice and rationale (accountability).
5. Communicate the basis to data subjects per Articles 13-14.
6. For special category data, identify both Article 6 basis and Article 9 exception.

Once chosen, switching lawful bases is hard. If consent is withdrawn, processing must generally stop (cannot retroactively switch to legitimate interests).

## Common patterns by use case

### Employee data processing

- **Contract** for processing necessary for the employment contract (payroll, basic HR).
- **Legal obligation** for tax / social security / anti-money-laundering / employment law.
- **Legitimate interests** for fraud prevention, security monitoring (with safeguards).
- **Consent** typically inappropriate due to power imbalance (per Article 88 + national guidance).

### Customer data processing

- **Contract** for processing necessary to deliver the contracted service.
- **Legal obligation** for compliance (e.g., AML, tax).
- **Legitimate interests** for fraud prevention, security, some marketing (with right to object).
- **Consent** for non-essential cookies, marketing email opt-in, certain personalization.

### B2B contact processing

- **Legitimate interests** typically — business-context contact information.
- **Consent** for marketing (overlapping ePrivacy requirements).

### Health data processing

- **Contract + Article 9(h)** for healthcare provision.
- **Explicit consent + Article 9(a)** as fallback.
- **Public interest + Article 9(i)** for public health.

### Research / analytics

- **Legitimate interests + Article 89 safeguards** common.
- **Consent + Article 9(a)** for special category research data.
- **Public interest + Article 9(j)** for public-interest research.

## SRE and AI-agent fit notes

### Lawful basis for AI training

- **Consent** — fragile for training; withdrawable; specific-purpose limit.
- **Contract** — possible for contracted services where AI is integral.
- **Legitimate interests** — most common for general AI training when data subjects' interests don't override (LIA required).
- **Special category data in training** — requires Article 9 exception. Most common: explicit consent (Article 9(a)) or scientific research (Article 9(j)).

### Lawful basis for AI inference

- Inference using customer data: typically the same basis as the underlying service (contract or legitimate interests).
- Inference about non-customers: legitimate interests with LIA.

### Lawful basis for AI evaluation

- Evaluation data often involves real personal data: requires lawful basis.
- Synthetic / anonymized evaluation data preferred where feasible.

### Sending data to model providers (third-country transfers)

- Lawful basis required.
- Additional cross-border transfer mechanism required (see [[GDPR Cross-Border Transfers]]).
- Vendor's DPA covers processor obligations.

## Stefan-context implementation sketch

- Personal vault: mostly not GDPR-relevant (own data).
- Client engagements: lawful basis per processing activity, documented in engagement records.
- AI features touching personal data: legitimate interests for security / fraud / analytics; contract for customer-data processing within contracted services; explicit consent for special-category or marketing scenarios.

## See also

- [[GDPR Cluster|cluster MOC]] · [[GDPR Principles]] · [[GDPR Data Subject Rights]] · [[GDPR Controller and Processor]] · [[GDPR Cross-Border Transfers]]
