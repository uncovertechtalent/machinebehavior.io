title: FOCUS export
summary: A FOCUS 1.4-shaped CSV of the platform's metered costs for 2026-10-01 to 2026-10-08, the script that writes it, the column mapping and the declared deviations from the specification.
order: 60
labels: finops, focus, export, csv
---
The file [focus-2026-10-01-to-2026-10-08.csv](/inside/finops/focus-2026-10-01-to-2026-10-08.csv) holds the platform's metered costs in the Cost and Usage columns of FOCUS 1.4. It has 35 rows: 24 for Claude Code (one per UTC day and model) and 11 for GitHub Actions (one per UTC day and public repository). `scripts/focus_export.py` wrote it on 2026-10-09.

Check sums: the `ListCost` of the Claude Code rows adds up to USD 1,021.01, the Loki total for the range; the Actions rows add up to 47.0 runner minutes over 63 runs.

## Run

Loki must be reachable; on the workstation that means an SSH tunnel to the home server. The GitHub token only raises the API rate limit.

```bash
GITHUB_TOKEN="$(gh auth token)" LOKI_URL=http://localhost:13100 \
  python3 scripts/focus_export.py --start 2026-10-01 --end 2026-10-09 \
  --out inside/finops/focus-2026-10-01-to-2026-10-08.csv
```

The script runs one instant LogQL query per day, metric and model (the `request_sum()` pattern from [grafana/build.py](https://github.com/uncovertechtalent/agent-observability/blob/main/grafana/build.py) with a `[1d]` range) and reads job durations from the Actions API.

## Column mapping

| Column | Claude Code rows | GitHub Actions rows |
|---|---|---|
| `BilledCost` | 0: the subscription covers the calls | 0: standard runners are free for public repositories |
| `ListCost` | Sum of `cost_usd`: token counts at Claude API list prices, as Claude Code computes them | 0: the list price for public repositories |
| `ContractedCost` | Equal to `ListCost`: no negotiated rates | 0 |
| `EffectiveCost` | Empty (deviation 1) | 0 |
| `ChargeCategory` | `Usage` | `Usage` |
| `PricingQuantity`, `PricingUnit` | All tokens of the day and model, `Tokens` | Job minutes, `Minutes` |
| `ConsumedQuantity`, `ConsumedUnit` | Same as pricing | Same as pricing |
| `ServiceProviderName`, `HostProviderName`, `InvoiceIssuerName` | Anthropic | GitHub |
| `ServiceCategory` | `AI and Machine Learning` | `Developer Tools` |
| `ServiceName` | Claude Code | GitHub Actions |
| `SkuId`, `SkuPriceId` | The model ID | `actions_linux`, `actions_linux:public-repository` |
| `ResourceName` | Empty | The repository |
| `ChargePeriodStart`, `ChargePeriodEnd` | The UTC day | The UTC day |
| `BillingPeriodStart`, `BillingPeriodEnd` | The calendar month | The calendar month |
| `x_Requests` | API calls | Workflow runs |
| `x_InputTokens`, `x_OutputTokens`, `x_CacheReadTokens`, `x_CacheWriteTokens` | Token counts by class | Empty |
| `x_PrivateRepoEquivalentCost` | Empty | Minutes at USD 0.006, the Linux 2-core rate for private repositories |

Columns that start with `x_` are custom columns, which FOCUS allows with that prefix.

## Declared deviations from FOCUS 1.4

1. `EffectiveCost` is empty on the Claude Code rows. The specification requires the share of the covering purchase (the subscription fee) applied to each charge, and the fee is not published.
2. No `Purchase` rows. The subscription, the domains and the reverse proxy are missing. The Bedrock eval runs are missing too: `BilledCost` must be the invoiced amount, and only the harness's estimates are published ([Unit economics](doc:fin/unit-economics) lists them per run).
3. `BillingAccountId` and `BillingAccountName` read `withheld`.
4. `ListCost` on the Claude Code rows uses the per-token prices of the Claude API, the prices Claude Code applies. The plan in use has no per-token price.
5. Each Claude Code row sums four token classes with different prices into one `PricingQuantity`, so the file gives no `ListUnitPrice`. The FOCUS 1.5 draft adds `TokenDirection` and `TokenCacheAction` properties for this split; until then the counts by class are in the `x_` token columns.
6. The file has not been run through the FOCUS Validator.

## Why export at all

FOCUS gives one schema for every provider. The same file can join the cloud provider's own FOCUS export, once the invoice lines are added, without a mapping per vendor. It also makes the deviations explicit: each empty cell above marks a figure that the owner keeps private or that no meter provides. The FinOps framing of the platform: [FinOps](doc:fin/index).
