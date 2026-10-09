title: Showback
summary: The list-price value of the platform's usage, as Claude Code and the eval harness price it, set against what is billed, and the reasons the two differ.
order: 30
labels: finops, showback, pricing, claude-code
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
Showback reports the cost of usage to the people who caused it, without an internal invoice; chargeback books the cost to their budget. The FinOps Foundation covers both in the capability [Invoicing & Chargeback](https://www.finops.org/framework/capabilities/invoicing-chargeback/). On this platform showback compares two numbers for each component: the list-price value of the usage and the billed amount.

## List-price value against billed amount

| Component | List-price value | Billed | Range |
|---|---|---|---|
| Claude Code | USD 1,021.01 for 5,505 API calls (Loki) | A flat subscription fee; the amount is not published | 2026-10-01 15:21 to 2026-10-09 00:00 UTC |
| GitHub Actions | USD 0.28 for 47.0 runner minutes at the private-repository rate of USD 0.006 a minute | USD 0: public repositories run free | 2026-10-01 to 2026-10-08 |
| Bedrock evals | USD 14.94 for 14,040 calls at the harness's declared on-demand prices | The AWS invoice; not published | Runs of 2026-10-07 |

## Why the Claude Code figures differ

- The plan covers the usage. For Pro and Max subscribers, the Claude Code documentation says "the session cost figure isn't relevant for billing purposes" ([Manage costs](https://code.claude.com/docs/en/costs)).
- The figure is computed on the client. Claude Code multiplies the token counts of each response by list prices and reports the product as `cost_usd`. The Manage costs page calls the figure an estimate and names the Claude Console usage page as the authoritative record for API billing; the [monitoring reference](https://code.claude.com/docs/en/monitoring-usage) lists `cost_usd` as an estimated cost.
- List price is not a contracted rate. An organisation can set `modelPricing` in managed settings so that the figure uses its contracted rates. This platform does not set it, so every figure here is at list price.
- A subscription caps usage. Plans set limits per session window and per week. The list-price value is a proxy for how fast those limits fill. The plan's limit bars are not exported over OpenTelemetry, so the stack cannot meter them.

## The list-price multiple

For a flat plan the useful ratio is list-price value divided by the fee for the same period. With the fee F for October, the October multiple is the October list-price value divided by F. The fee is not published, so the multiple is not published either. The marginal cost of an API call on the plan is zero until a limit binds; after that, the cost is waiting time or usage credits.

## Why the Bedrock figures can differ

The harness prices each reply's tokens at on-demand list prices from the AWS Pricing API (2026-10-07), per model and region. The AWS invoice can differ from that sum, for example through tax or credits. FOCUS requires `BilledCost` to be the invoiced amount, so the [FOCUS export](doc:fin/focus-export) leaves the Bedrock runs out.

## GitHub

GitHub's billing page lists standard runners in public repositories as free, and the run timing endpoint reported 0 billable ms for a machinebehavior.io run checked on 2026-10-09. The private-repository figure is there to show what the same deploys would cost on a private repository.

## Not in the showback

The subscription fee, the AWS invoice lines for Bedrock and the reverse proxy, the domain fees and the electricity tariff. They are kept private, so this page shows list-price value and usage only. The components and their meters: [Cost model](doc:fin/cost-model).
