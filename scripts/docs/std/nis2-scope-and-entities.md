title: NIS2 Scope and Entities
summary: NIS2 classifies entities as essential or important based on sector (Annex I or II) and size.
parent: nis2
order: 100
labels: nis2, regulation-concept
aliases: NIS2 Scope | NIS2 Entities | NIS2 Essential Important | NIS2 Annex I Annex II
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nis2/NIS2 Scope and Entities.md
reviewed: no
---
> NIS2 classifies entities as essential or important based on sector (Annex I or II) and size. Essential entities face proactive supervision and higher penalties; important entities face reactive supervision. The classification drives the regulatory obligations and supervision regime.

## Essential entities (Annex I — high-criticality sectors)

### Energy
- Electricity (suppliers, DSOs, TSOs, producers, nominated electricity market operators, electricity market participants, charging point operators)
- District heating and cooling
- Oil (transmission, production, refining, storage)
- Gas (suppliers, DSOs, TSOs, storage operators, LNG operators, natural gas undertakings, refining/treatment facility operators)
- Hydrogen (production, storage, transmission)

### Transport
- Air (air carriers, airport managing bodies, air traffic management)
- Rail (infrastructure managers, railway undertakings, service facility operators)
- Water (inland/sea/coastal passenger and freight water transport, managing bodies of ports, vessel traffic services operators)
- Road (road authorities, ITS operators)

### Banking
- Credit institutions (lex specialis with DORA — see [[DORA Cluster]])

### Financial market infrastructures
- Trading venues
- Central counterparties (lex specialis with DORA)

### Health
- Healthcare providers
- EU reference laboratories
- Medical research entities
- Manufacturers of pharmaceuticals
- Manufacturers of medical devices considered critical

### Drinking water
- Drinking water suppliers and distributors

### Waste water
- Collection, disposal, treatment of urban waste water, domestic waste water, industrial waste water

### Digital infrastructure
- Internet exchange point providers (IXPs)
- DNS service providers (excluding root name server operators)
- TLD name registries
- Cloud computing service providers
- Data centre service providers
- Content delivery network (CDN) providers
- Trust service providers (qualified and non-qualified)
- Providers of public electronic communications networks
- Providers of publicly available electronic communications services

### ICT service management (B2B)
- Managed service providers (MSPs)
- Managed security service providers (MSSPs)

### Public administration
- Central government public administration entities
- Regional government public administration entities (Member State discretion on local)

### Space
- Ground-based infrastructure operators owned, managed, operated by Member States or private parties supporting provision of space-based services (excluding public electronic communications networks)

## Important entities (Annex II — other critical sectors)

### Postal and courier services
- Postal service providers, courier service providers

### Waste management
- Undertakings carrying out waste management

### Chemicals
- Manufacture, production, distribution of chemicals

### Food
- Production, processing, distribution of food (B2B and B2C)

### Manufacturing
- Manufacture of medical devices and in vitro diagnostic medical devices
- Manufacture of computer, electronic and optical products
- Manufacture of electrical equipment
- Manufacture of machinery and equipment NEC
- Manufacture of motor vehicles, trailers, semi-trailers
- Manufacture of other transport equipment

### Digital providers
- Online marketplaces
- Online search engines
- Social networking services platforms

### Research
- Research organisations

## Size thresholds

### Default

NIS2 applies by default to medium and large entities in Annex I/II sectors.

- **Medium**: 50+ staff AND/OR annual turnover or balance sheet >€10M.
- **Large**: 250+ staff OR annual turnover >€50M OR balance sheet >€43M.

### Exceptions — smaller entities included regardless of size

- Trust service providers
- Top-level domain name registries
- DNS service providers
- Providers of public electronic communications networks/services
- Sole providers in a Member State of a service essential for maintenance of critical societal/economic activities
- Entities whose disruption could have significant systemic risk
- Entities whose disruption could have significant cross-border impact
- Entities critical due to specific importance at regional/national level
- Public administration entities (central + Member-State-discretion regional/local)

### Member State extension

Member States can extend NIS2 scope to additional entities. DE NIS2UmsuCG includes additional KRITIS-relevant entities.

## Classification consequences

### Essential entities

- Subject to ex-ante (proactive) supervision.
- Higher penalty cap: €10M or 2% global turnover.
- Mandatory registration with competent authority.
- More extensive incident reporting obligations.
- More frequent audits/inspections.

### Important entities

- Subject to ex-post (reactive) supervision primarily.
- Lower penalty cap: €7M or 1.4% global turnover.
- Registration required.
- Incident reporting required.
- Audits/inspections triggered by specific events.

### Common to both

- Article 21 security measures.
- Article 23 incident reporting.
- Article 20 management body accountability.
- Cooperation with competent authorities.

## Self-identification

NIS2 expects entities to self-identify whether they fall in scope and which classification applies. Member State authorities maintain registers. Misclassification (claiming "out of scope" when in scope) is itself a violation.

### Identification process

1. Identify Annex I/II sector applicability.
2. Apply size thresholds.
3. Check size-threshold exceptions.
4. Check Member State extensions.
5. Determine essential vs important classification.
6. Register with competent authority per national procedure.

### Edge cases

Most contested classification scenarios:

- Mixed-activity entities (in multiple sectors).
- Below-size-threshold entities providing services to in-scope entities.
- ICT service providers servicing essential entities (often pulled into scope as MSPs/MSSPs).
- Cloud service customers vs cloud service providers — both potentially in scope.

## Cross-sector entities (Articles 22-24)

Where an entity provides services across multiple Member States, jurisdictional rules apply:

- **Main establishment** — Member State where decisions on cybersecurity risk management are taken, or where operations are physically carried out, depending on context.
- Cooperation between authorities for cross-border supervision.

## SRE and AI-agent fit notes

### Typical SRE client classifications

- **Manufacturing clients (machinery, electronics, vehicles, medical devices, electrical equipment)** — important entity if medium+ size.
- **Healthcare clients** — essential if Annex I health sector, important if medical device manufacturers in Annex II.
- **Cloud service providers** — essential entity.
- **MSPs / MSSPs** — essential entity.
- **Data center operators** — essential entity.
- **Banking / financial market infrastructure clients** — essential entity (but DORA lex specialis).
- **Energy / transport / water clients** — essential entity.
- **Mid-size SaaS providing to in-scope clients** — typically not directly in scope by sector, but supply-chain obligations flow from clients.

### AI systems in NIS2 scope

AI systems used by in-scope entities are part of "network and information systems." Subject to Article 21 risk-management measures. AI Act co-applies for AI-specific obligations.

### Supply-chain implications

Article 21(d) supply-chain security requires due diligence on direct upstream suppliers. For SRE consultancies providing services to NIS2-scope clients: expect client-side questionnaires; document own cybersecurity posture.

## Stefan-context implementation sketch

- For each client engagement, run NIS2 scope assessment:
  - What sector(s) does the client operate in?
  - What size is the client?
  - Essential or important?
  - Already identified themselves under their Member State's transposition?
- For own positioning: as a consultant providing services to NIS2-scope clients, expect supply-chain due diligence; maintain ISO 27001-aligned posture as evidence.

## See also

- [[NIS2 Cluster|cluster MOC]] · [[NIS2 Security Measures]] · [[NIS2 Incident Reporting]] · [[NIS2 Governance and Penalties]]
- [[DORA Cluster]] (financial services lex specialis)
