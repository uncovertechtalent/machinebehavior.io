title: Loki streams
summary: The Loki streams the stack writes, with their labels and line fields, for website deploy records and for Claude Code events.
order: 30
labels: loki, logql, reference
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
Loki holds two kinds of data: website deploy records pushed by the deploy-exporter, and Claude Code events sent through Alloy. Retention is 90 days.

## Website deploy streams

The deploy-exporter pushes one JSON line per finished run, step and gate check. Source: `push_loki()` in [deploy-exporter/exporter.py](https://github.com/uncovertechtalent/agent-observability/blob/main/deploy-exporter/exporter.py).

| Stream `job` | Other labels | Timestamp | Line fields |
|---|---|---|---|
| `site-deploys` | site, outcome | run finished | site, `run_id`, `run_number`, event, conclusion, started, finished, `duration_s`, outcome, jobs, plus the parsed gate and map fields |
| `site-deploy-steps` | site, `gh_job`, step | step finished | `run_id`, conclusion, `duration_s` |
| `site-gate-checks` | site, check | run finished | `run_id`, result (pass, partial, pending, fail), state (3, 2, 1, 0) |

On the run line, `jobs` lists each job's name, conclusion and `duration_s`. The parsed fields are trigger, gate, `findings_open`, warnings, checks (result per check) and map (nodes, links, `committed_nodes`, `committed_links`, kept, `carried_links`, `unreachable_pages`, `dropped_pages`, `shipped_nodes`, `shipped_links`). Lines from the public repositories also carry title, sha (seven characters) and url. Lines from the uncovertechtalent.com repository (private) carry none of the three.

Queries from the Website deploys dashboard, with `$__interval` set to 1h:

```logql
sum by (outcome) (count_over_time({job="site-deploys"}[1h]))
max by (site) (max_over_time({job="site-deploys", outcome="deployed"} | json | unwrap duration_s [1h]))
min by (check) (min_over_time({job="site-gate-checks", site="machinebehavior.io"} | json | unwrap state [1h]))
```

## Claude Code events

Claude Code sends events over OTLP through Alloy. Loki keeps `service_name` as the stream label (values match `claude-code.*`) and stores the other attributes as structured metadata, which LogQL filters after the pipe.

| `event_name` | Fields the dashboards read |
|---|---|
| `api_request` | model, `cost_usd`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`, `duration_ms`, `query_source`, `skill_name`, `agent_name` |
| `api_error` | `status_code` |
| `tool_result` | `tool_name`, success, `duration_ms` |
| `user_prompt` | count only |
| `api_refusal`, `api_retries_exhausted`, `internal_error` | shown as log lines |
| `tool_decision`, `permission_mode_changed` | shown as log lines |

Claude Code writes one `api_request` event per API call, so a sum over its fields is exact. Each event also carries `request_id` and `trace_id`. A `keep` stage before `unwrap` drops them, so the sum does not split into one series per request:

```logql
sum by (model) (sum_over_time({service_name=~"claude-code.*"} | event_name="api_request" | keep model, cost_usd | unwrap cost_usd [1h]))
```

Prompt and response text stay redacted, which is Claude Code's default. Alloy deletes the account email, account IDs and organisation ID before Loki stores an event. Why spend comes from these events: [Counter resets from parallel sessions](doc:obs/runbook-counter-resets-parallel-sessions).
