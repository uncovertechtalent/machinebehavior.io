title: FinOps
summary: The cost side of the platform in the FinOps Foundation's terms (phases, principles, personas, domains, FOCUS) and how each applies to a one-person platform built with Claude Code.
labels: finops, cost, framework, focus
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
The FinOps space documents what the platform behind machinebehavior.io costs, how each cost is metered and which unit costs follow from the meters. It uses the FinOps Foundation's framework for the practice and FOCUS, the FinOps Open Cost and Usage Specification, for the data. Every figure names its date range and its source.

The platform is three static sites on GitHub, a small cloud reverse proxy, a home server with a GPU that runs the [observability stack](doc:obs/index) and a local LLM, model evaluations on Amazon Bedrock, and Claude Code sessions that write most of the code and the pages. From 2026-10-01 15:21 UTC (the first event) to 2026-10-09 00:00 UTC, Claude Code made 5,505 API calls with a list-price value of USD 1,021.01 (Loki). It is the largest metered cost on the platform.

## FinOps in the framework's terms

The FinOps Foundation defines FinOps as "an operational framework and cultural practice" that maximizes the business value of technology, supports timely decisions based on data, and creates financial accountability through collaboration between engineering, finance and business teams ([What is FinOps](https://www.finops.org/introduction/what-is-finops/), updated March 2026).

### Phases

| Phase | In the framework | On this platform |
|---|---|---|
| Inform | Cost, usage and efficiency data; budgets, forecasts, KPIs and benchmarks | Per-request Claude Code events in Loki, Actions job time from the GitHub API, eval cost per run from the harness records: [Cost model](doc:fin/cost-model), [Unit economics](doc:fin/unit-economics), [Showback](doc:fin/showback) |
| Optimize | Fewer resources for the same work, or better rates and contracts | Levers with data behind them: model choice (93% of Claude Code spend is on two models), prompt cache reads (96.3% of input-side tokens), prompt suggestions (4.5% of spend, a feature that can be switched off), offloadable work on the local GPU |
| Operate | Carry out the chosen changes with shared accountability, then return to Inform | The spend alert, [The phantom two million](doc:fin/anomaly-the-phantom-two-million) and [Budgets and alerts](doc:fin/budgets-and-alerts) |

### Principles

The six principles in their 2025 wording, unchanged in the 2026 framework ([Principles](https://www.finops.org/framework/principles/)):

| Principle | On this platform |
|---|---|
| Teams need to collaborate | One person and many parallel Claude Code sessions. Session notes and these pages carry cost decisions from one session to the next. |
| Business value drives technology decisions | Spend is read per unit of output: per commit, per deploy, per eval run ([Unit economics](doc:fin/unit-economics)). |
| Everyone takes ownership for their technology usage | Each Claude Code request carries its model and the subsystem that sent it, so spend splits into main loop, subagents and side calls. |
| FinOps data should be accessible, timely, and accurate | Spend per request is in Loki and on a [public dashboard](doc:obs/public-dashboards). The accuracy failure of 2026-10-09 and its fix: [The phantom two million](doc:fin/anomaly-the-phantom-two-million). |
| FinOps should be enabled centrally | One observability stack holds every meter, recording rule and alert. |
| Take advantage of the variable cost model of the cloud | Evals run on pay-per-token Bedrock models with a budget cap per run; the public repositories use GitHub's free runners. |

### Personas

Core personas: FinOps Practitioner, Engineering, Finance, Product, Procurement and Leadership. Allied personas: ITAM, ITFM, Sustainability, ITSM / ITIL and Security ([Personas](https://www.finops.org/framework/personas/)). On this platform one person holds all six core personas. Sustainability has one meter to work with: the GPU's energy in kWh.

### Domains and capabilities

| Domain | Capabilities | Here |
|---|---|---|
| Understand Usage & Cost | Data Ingestion; Allocation; Reporting & Analytics; Anomaly Management | [Cost model](doc:fin/cost-model), [The phantom two million](doc:fin/anomaly-the-phantom-two-million), [FOCUS export](doc:fin/focus-export) |
| Quantify Business Value | Planning & Estimating; Forecasting; Budgeting; KPIs & Benchmarking; Unit Economics | [Unit economics](doc:fin/unit-economics), [Budgets and alerts](doc:fin/budgets-and-alerts) |
| Optimize Usage & Cost | Architecting & Workload Placement; Rate Optimization; Usage Optimization; Sustainability; Licensing & SaaS | Placement of work between the local GPU, Bedrock and Claude Code; the subscription against list price in [Showback](doc:fin/showback) |
| Manage the FinOps Practice | FinOps Practice Operations; Governance, Policy & Risk; FinOps Assessment; Automation, Tools & Services; FinOps Education & Enablement; Invoicing & Chargeback; Intersecting Disciplines; Executive Strategy Alignment | This space; the [deploy pipeline](doc:eng/deploy-pipeline) as the governance point for every published page |

Source: [Domains](https://www.finops.org/framework/domains/). The 2026 framework added Executive Strategy Alignment and renamed six capabilities, for example Workload Optimization to Usage Optimization.

### Scopes and technology categories

Since the 2026 framework, a technology category says what is being managed (Public Cloud, SaaS, Data Center, Data Cloud Platforms, AI) and a scope says why, by tying spend to a business construct such as a product or a cost centre ([Scopes](https://www.finops.org/framework/scopes/), [Technology categories](https://www.finops.org/framework/technology-categories/)). This space has one scope, the machinebehavior.io platform, across four categories: AI (Claude Code, Bedrock, the local LLM), SaaS (GitHub), Public Cloud (the reverse proxy) and Data Center (the home server).

### Maturity

The framework rates each capability Crawl, Walk or Run ([Maturity model](https://www.finops.org/framework/maturity-model/)). The owner's own reading, without an outside assessment: Reporting & Analytics and Anomaly Management are at Walk for Claude Code spend, with one exact meter, automated sums and a tested alert rule. Allocation stops at model and subsystem, because the events carry no project label. Budgeting and Forecasting are at Crawl for Claude Code, which has no budget. The AWS account has a monthly budget in AWS Budgets, which e-mails at 80% of actual spend, and since 2026-10-09 an internal dashboard and four alert rules compare spend and forecast with it. The Prometheus alerts still reach nobody.

## FOCUS

FOCUS is a technical specification that normalizes billing data across technology vendors ([What is FOCUS](https://focus.finops.org/what-is-focus/)). Versions: 1.1 (ratified 2024-11-07), 1.2 (2025-05-29), 1.3 (2025-12-05) and 1.4 (2026-06-04, the current one). Version 1.3 replaced `ProviderName` with `ServiceProviderName` and `HostProviderName`, and 1.4 removed the old column. Version 1.5 is scheduled for ratification on 2026-12-03; its draft labels AI token charges by model, token direction and cache action inside `SkuPriceDetails` ([FOCUS 1.5 scope](https://focus.finops.org/focus-1-5-release-scope/)).

The platform's metered costs as a FOCUS 1.4 Cost and Usage file: [FOCUS export](doc:fin/focus-export).

## Start here

- [Cost model](doc:fin/cost-model): every cost component, its billing model, its meter and its amount.
- [Unit economics](doc:fin/unit-economics): cost per day, per call, per commit, per deploy and per eval run.
- [Showback](doc:fin/showback): list-price value against the bill.
- [The phantom two million](doc:fin/anomaly-the-phantom-two-million): a data-quality anomaly as a FinOps case.
- [Budgets and alerts](doc:fin/budgets-and-alerts): what exists and what a budget alert would look like.
- [FOCUS export](doc:fin/focus-export): the CSV, the script and the declared deviations.

The method for unit costs comes from the SRE Handbook: [Unit Economics of Infrastructure](doc:sre/unit-economics-of-infrastructure) and [Cost Optimization](doc:sre/cost-optimization).
