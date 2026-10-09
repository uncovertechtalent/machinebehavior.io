title: Unit economics
summary: Cost per unit of output with real numbers: Claude Code spend per day, per model, per API call, per million tokens and per commit; runner time per deploy; cost per eval run.
order: 20
labels: finops, unit-economics, kpi, claude-code
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
The method follows [Unit Economics of Infrastructure](doc:sre/unit-economics-of-infrastructure) in the SRE Handbook: divide spend by a unit the work already counts. The units here are days, API calls, tokens, commits, deploy runs and eval runs. Claude Code figures are list-price values from Claude Code's own `cost_usd`; [Showback](doc:fin/showback) explains how they relate to the bill.

## Summary

| Unit | Value | Range | Source |
|---|---|---|---|
| Claude Code, USD per day | mean 143.35, median 94.30 | 7 full days, 2026-10-02 to 2026-10-08 | Loki |
| Claude Code, USD per API call | 0.185 | 2026-10-01 15:21 to 2026-10-09 00:00 UTC | Loki |
| Claude Code, USD per million tokens | 0.72 | same | Loki |
| Claude Code, USD per commit | 4.29 | same, 238 commits | git log of ten repositories |
| Runner time per deploy push | 53.5 s, USD 0 billed | 51 runs, 2026-10-07 12:36 to 2026-10-09 10:01 UTC | GitHub Actions API |
| Bedrock eval, USD per 1,000 calls | 0.37 to 1.84 by model and run | runs of 2026-10-07 | eval records |
| Weekly decision-layer probe | USD 0.269 per run | first run 2026-10-07 | probe record |

## Claude Code per day

| Day (UTC) | API calls | USD | USD per call |
|---|---|---|---|
| 2026-10-01 (from 15:21) | 156 | 17.56 | 0.113 |
| 2026-10-02 | 137 | 62.04 | 0.453 |
| 2026-10-03 | 1,396 | 194.45 | 0.139 |
| 2026-10-04 | 297 | 86.41 | 0.291 |
| 2026-10-05 | 63 | 53.41 | 0.848 |
| 2026-10-06 | 175 | 118.60 | 0.678 |
| 2026-10-07 | 2,754 | 394.23 | 0.143 |
| 2026-10-08 | 527 | 94.30 | 0.179 |
| Total | 5,505 | 1,021.01 | 0.185 |

Cost per call varied by a factor of 7.5. The two days with the highest cost per call (2026-10-05 and 2026-10-06) also had the longest contexts: on average 411,000 and 368,000 cache-read tokens per call. The busiest day, 2026-10-07, averaged 182,000. A count of calls alone does not track spend.

Query, as on the dashboard (`request_sum()` in [grafana/build.py](https://github.com/uncovertechtalent/agent-observability/blob/main/grafana/build.py)), evaluated at the end of each UTC day:

```logql
sum(sum_over_time({service_name=~"claude-code.*"} | event_name="api_request" | keep cost_usd | unwrap cost_usd [1d]))
```

## Claude Code per model

| Model | API calls | USD | Share of spend | USD per call |
|---|---|---|---|---|
| claude-opus-5-5 | 3,932 | 506.58 | 49.6% | 0.129 |
| claude-fable-5-1 | 1,142 | 442.87 | 43.4% | 0.388 |
| claude-opus-4-8 | 264 | 66.11 | 6.5% | 0.250 |
| claude-sonnet-5-5 | 87 | 3.98 | 0.4% | 0.046 |
| claude-haiku-4-5-20251001 | 80 | 1.47 | 0.1% | 0.018 |

Range: 2026-10-01 15:21 to 2026-10-09 00:00 UTC. The same per-model spend is on the public [Claude Code dashboard](doc:obs/public-dashboards).

## Tokens

| Token class | Tokens |
|---|---|
| Input | 2,069,207 |
| Output | 6,207,762 |
| Cache read | 1,368,643,558 |
| Cache write | 49,998,919 |
| Total | 1,426,919,446 |

Cache reads were 96.3% of input-side tokens (input, cache read and cache write). On Opus 5.5 a cache read is priced at USD 0.20 per million tokens against USD 4.00 for uncached input (Claude API list prices, October 2026). The dashboard shows the same share as "cache read share".

## Per commit

238 commits by the one author in the same range: 68 in the three public repositories (machinebehavior.io 50, tychat.io 10, agent-observability 8) and 170 in private or local repositories, 126 of them in the knowledge vault. USD 1,021.01 / 238 = USD 4.29 per commit.

A commit is a coarse unit. One commit can fix a typo or build 336 pages, and Claude Code spend also pays for research and drafts that reach no commit in the range. The figure is useful as a trend over several weeks; a single change has no fixed price.

## Per deploy

The Conformity workflow runs the gate and the Pages deploy as two jobs ([Deploy pipeline](doc:eng/deploy-pipeline)). Its 51 push runs from 2026-10-07 12:36 to 2026-10-09 10:01 UTC used 2,729 job-seconds: 53.5 s of runner time per push. The median time from push to finished run was 48 s. Billed: USD 0, as the repository is public and the run timing endpoint reports 0 billable ms. At the private-repository rate of USD 0.006 per minute, the same time would cost USD 0.27 in total, or USD 0.005 per push.

## Evals on Bedrock

| Run | Model | Calls | USD | USD per 1,000 calls |
|---|---|---|---|---|
| smoke-02 | qwen3-coder-30b | 360 | 0.2121 | 0.59 |
| full-01 | qwen3-coder-30b | 2,160 | 1.3034 | 0.60 |
| full-02, short stance | qwen3-coder-30b | 720 | 0.2952 | 0.41 |
| v5 smoke | gpt-oss-120b | 480 | 0.2655 | 0.55 |
| v5 smoke | DeepSeek V3.2 | 480 | 0.7087 | 1.48 |
| v5 smoke | Kimi K2.5 | 480 | 0.8818 | 1.84 |
| v5 full | gpt-oss-120b | 2,880 | 1.6674 | 0.58 |
| v5 full | DeepSeek V3.2 | 2,880 | 4.2059 | 1.46 |
| v5 full | Kimi K2.5 | 2,880 | 5.1319 | 1.78 |
| weekly probe | qwen3-coder-30b | 720 | 0.269 | 0.37 |
| Total | | 14,040 | 14.94 | 1.06 |

All runs on 2026-10-07. The harness sums the token counts of each reply at the prices it declares (AWS Pricing API, on-demand, 2026-10-07) and stops starting new conversations once the projected spend would cross the run's cap. Results: [Experiment 04](doc:res/experiment-04-folding-under-pressure) and [Weekly decision-layer probe](doc:res/decision-layer-probe).

The model calls under test cost USD 14.94. The Claude Code work that built, ran and published the experiment on the same day is inside that day's USD 394.23 and cannot be split out: the events carry no project label ([Cost model](doc:fin/cost-model)).

## Local LLM

1,716 requests with 1.30 million input and 66,883 output tokens, 2026-10-01 to 2026-10-09 00:00 UTC (ollama-exporter). The GPU used 2.22 kWh in the same range (mean 11.6 W). Its lowest reading was 8.98 W; at that draw for the whole range it would have used 1.72 kWh. That leaves about 0.50 kWh above the floor, or about 0.29 Wh per request. That figure is an estimate: it charges every watt above the minimum to the LLM. The money cost depends on the tariff, which is not published.

## Benchmark

The Claude Code documentation gives an enterprise average of "around $13 per developer per active day", with 90% of users below USD 30 ([Manage costs](https://code.claude.com/docs/en/costs)). This platform's mean is USD 143.35 per day at list price for one person. The comparison has limits: this person runs up to about 12 Claude Code processes at once (week to 2026-10-09), and 93% of the spend is on Opus 5.5 and Fable 5.1.
