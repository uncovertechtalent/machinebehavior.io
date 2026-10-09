title: NIST AI RMF Core Functions
summary: Four core functions of the NIST AI Risk Management Framework: Govern, Map, Measure, Manage.
parent: nist-ai-rmf
order: 100
labels: framework-concept, nist-ai-rmf
aliases: NIST AI RMF Core Functions | NIST AI RMF Govern Map Measure Manage | AI RMF Functions
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nist-ai-rmf/NIST AI RMF Core Functions.md
reviewed: no
---
> Four core functions of the NIST AI Risk Management Framework: Govern, Map, Measure, Manage. Each function has categories and sub-categories; the Playbook provides suggested actions per sub-category. Functions are cyclical and interdependent; GOVERN underlies the others.

## GOVERN

The leadership, culture, policy, and process spine. Without GOVERN, the other functions lack direction and resourcing.

### Categories

- **GOVERN 1**: Policies, processes, procedures, practices are in place to support, develop, and use AI systems responsibly.
- **GOVERN 2**: Accountability structures are in place so the appropriate teams and individuals are empowered, responsible, and trained for AI risk management.
- **GOVERN 3**: Workforce diversity, equity, inclusion, and accessibility processes are prioritized in AI risk-management decisions.
- **GOVERN 4**: Organizational teams are committed to a culture that considers and communicates AI risk.
- **GOVERN 5**: Processes are in place for engagement with relevant AI actors.
- **GOVERN 6**: Policies and procedures are in place to address AI risks and benefits arising from third-party software and data.

### Example sub-categories

- GOVERN 1.1: Legal and regulatory requirements involving AI are understood, managed, and documented.
- GOVERN 1.2: The characteristics of trustworthy AI are integrated into organizational policies, processes, procedures.
- GOVERN 2.1: Roles and responsibilities and lines of communication related to mapping, measuring, and managing AI risks are documented.
- GOVERN 4.1: Organizational policies and practices are in place to foster a critical thinking and safety-first mindset.
- GOVERN 6.1: Policies and procedures are in place that address AI risks associated with third-party entities, including risks of infringement of a third-party's intellectual property.

Mappings: GOVERN parallels ISO 42001 Cl 5 Leadership + parts of Cl 4 Context + parts of Cl 6 Planning. Also parallels ISO 27001 Cl 5 + ITIL Continual Improvement at the management level.

## MAP

Context establishment and risk identification. The function that determines what AI systems are in scope, what they do, where they operate, and what risks they pose.

### Categories

- **MAP 1**: Context is established and understood.
- **MAP 2**: Categorization of the AI system is performed.
- **MAP 3**: AI capabilities, targeted usage, goals, expected benefits, costs are understood.
- **MAP 4**: Risks and benefits are mapped for all components of the AI system, including third-party software and data.
- **MAP 5**: Impacts to individuals, groups, communities, organizations, society are characterized.

### Example sub-categories

- MAP 1.1: Intended purposes, potentially beneficial uses, context-specific laws, norms, expectations, prospective settings in which the AI system will be deployed are understood and documented.
- MAP 2.2: Information about the AI system's knowledge limits and how system output may be utilized and overseen by humans is documented.
- MAP 3.1: Potential benefits of intended AI system functionality and performance are examined and documented.
- MAP 4.1: Approaches for mapping AI technology and legal risks of its components — including the use of third-party data or software — are in place, followed, and documented.
- MAP 5.1: Likelihood and magnitude of each identified impact (both potentially beneficial and harmful) based on expected use, past uses of AI systems in similar contexts, public incident reports, feedback from those external to the team that developed or deployed the AI system, or other data are identified and documented.

Mappings: MAP parallels ISO 42001 Cl 4 Context + Cl 6 Planning (risk identification) + Cl 6.1.4 AI system impact assessment + ISO 42001 Annex A.5 controls.

## MEASURE

Analysis and tracking of identified risks. Quantitative, qualitative, and mixed methods. Evaluates trustworthy AI characteristics.

### Categories

- **MEASURE 1**: Appropriate methods and metrics are identified and applied.
- **MEASURE 2**: AI systems are evaluated for trustworthy characteristics.
- **MEASURE 3**: Mechanisms for tracking identified AI risks over time are in place.
- **MEASURE 4**: Feedback about efficacy of measurement is gathered and assessed.

### Example sub-categories

- MEASURE 1.1: Approaches and metrics for measurement of AI risks enumerated during the MAP function are selected for implementation.
- MEASURE 2.3: AI system performance or assurance criteria are measured qualitatively or quantitatively and demonstrated for conditions similar to deployment setting(s).
- MEASURE 2.4: The functionality and behavior of the AI system and its components — as identified in the MAP function — are monitored when in production.
- MEASURE 2.5: The AI system to be deployed is demonstrated to be valid and reliable.
- MEASURE 2.7: AI system security and resilience — as identified in the MAP function — are evaluated and documented.
- MEASURE 2.11: Fairness and bias — as identified in the MAP function — are evaluated and results are documented.
- MEASURE 3.1: Approaches, personnel, and documentation are in place to regularly identify and track existing, unanticipated, and emergent AI risks based on factors such as intended and actual performance in deployed contexts.

Mappings: MEASURE parallels ISO 42001 Cl 9 Performance Evaluation + parts of Cl 8 Operation + ISO 42001 Annex A.6 (V&V, monitoring) + Annex A.5 (impact assessment).

## MANAGE

Risk treatment and ongoing management. Allocation of resources to mapped and measured risks. Decisions about acceptable risk. Monitoring.

### Categories

- **MANAGE 1**: AI risks based on assessments and other analytical output from the MAP and MEASURE functions are prioritized, responded to, and managed.
- **MANAGE 2**: Strategies to maximize AI benefits and minimize negative impacts are planned, prepared, implemented, documented, informed by input from relevant AI actors.
- **MANAGE 3**: AI risks and benefits from third-party entities are managed.
- **MANAGE 4**: Risk treatments — including response and recovery, and communication plans — for the identified and measured AI risks are documented and monitored regularly.

### Example sub-categories

- MANAGE 1.1: A determination is made as to whether the AI system achieves its intended purpose and stated objectives and whether its development or deployment should proceed.
- MANAGE 1.3: Responses to the AI risks deemed high priority — as identified by the MAP function — are developed, planned, and documented.
- MANAGE 2.3: Procedures are followed to respond to and recover from a previously unknown risk when it is identified.
- MANAGE 3.1: AI risks and benefits from third-party resources are regularly monitored, and risk controls are applied and documented.
- MANAGE 4.1: Post-deployment AI system monitoring plans are implemented, including mechanisms for capability requirements as required, decommissioning of the system, and incident response.

Mappings: MANAGE parallels ISO 42001 Cl 6.1.3 Risk Treatment + Cl 8 Operation + Cl 10 Improvement + ISO 42001 Annex A.6.2.6 Operation and monitoring + Annex A.10 third-party relationships.

## How the functions work together

The four functions are cyclical and interdependent:

- **GOVERN** establishes the policies, accountability, culture under which the other functions operate.
- **MAP** identifies the AI systems, their context, the risks they pose. Outputs feed MEASURE and MANAGE.
- **MEASURE** evaluates the identified risks and the AI system characteristics. Outputs feed MANAGE.
- **MANAGE** treats the risks based on MEASURE outputs. Treatment effectiveness feeds back into MAP (new risks identified) and MEASURE (treatment effectiveness measurement).

GOVERN is foundational — without it, the operational cycle (MAP → MEASURE → MANAGE) lacks direction.

The framework explicitly notes that the order is not strict; orgs may iterate in different sequences as appropriate to their context.

## Function-to-trustworthy-AI-characteristics mapping

The characteristics of trustworthy AI (valid / reliable, safe, secure / resilient, accountable / transparent, explainable / interpretable, privacy-enhanced, fair) are evaluated primarily under MEASURE but managed under MANAGE and contextualized under MAP. GOVERN provides the policy framing for which characteristics matter and how trade-offs are resolved.

## Practical application patterns

### Function-driven adoption

Pick one function to mature first, then expand. Common starting points:

- **GOVERN first**: when leadership commitment and policy infrastructure are weak.
- **MAP first**: when the org operates AI without clear understanding of its scope and risks.
- **MEASURE first**: when AI is in production without effective evaluation infrastructure.
- **MANAGE first**: when risks are mapped and measured but treatment decisions are missing.

### Function-and-characteristic matrix adoption

For mature implementations: matrix of functions × characteristics. Cells identify whether the function covers the characteristic adequately.

Example: GOVERN × Fairness — are policies on fairness in place? MAP × Fairness — are fairness risks identified in scope? MEASURE × Fairness — are fairness metrics in place? MANAGE × Fairness — are fairness risk treatments active?

### Sub-category-driven adoption

For very mature implementations: the ~70 sub-categories provide actionable adoption criteria. Track adoption status per sub-category.

## SRE and AI-agent fit notes

### Function-to-operational-practice mapping

- **GOVERN** → AI risk policy, AI roles, model-vendor management policy, third-party risk policy, organizational AI culture.
- **MAP** → AI system inventory, agent capability documentation, prompt and tool documentation, threat modeling (with OWASP LLM Top 10 + MITRE ATLAS), impact assessment.
- **MEASURE** → evaluation harness, prompt-injection testing, output validation, fairness testing, robustness testing, behavioral monitoring, vendor-side change detection.
- **MANAGE** → risk treatment decisions, kill-switch implementation, human-in-the-loop for high-stakes actions, incident response, vendor-relationship management.

### GenAI Profile actions per function

The GenAI Profile (NIST AI 600-1) organizes 200+ actions across the four functions and 12 risk categories. For an agent system org, actions of particular relevance:

- GOVERN actions on third-party model provider management
- MAP actions on prompt-injection threat identification
- MEASURE actions on adversarial-input evaluation
- MANAGE actions on incident response for AI-related incidents

Detail in [[NIST AI RMF GenAI Profile]].

## Stefan-context implementation sketch

For solo / small-team work on agent systems:

- **GOVERN**: short AI policy in vault, role identity self-documented, vendor authorization criteria explicit.
- **MAP**: agent inventory in bd / vault, threat modeling per significant agent (OWASP LLM Top 10 as starting taxonomy), impact assessment per agent.
- **MEASURE**: lightweight evaluation harnesses, periodic prompt-injection testing, output validation patterns.
- **MANAGE**: explicit autonomy decisions per agent, kill-switches documented, incident response procedure in vault.

## See also

- [[NIST AI RMF Cluster|cluster MOC]] · [[NIST AI RMF GenAI Profile]] · [[NIST AI RMF vs ISO 42001]]
- [[ISO 42001 Annex A Controls]] (parallel control set; many mappings)
- [[OWASP LLM Top 10 Cluster]] (operational threat content feeding MAP)
