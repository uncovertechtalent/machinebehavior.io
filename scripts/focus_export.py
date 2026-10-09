#!/usr/bin/env python3
"""Write the platform's metered costs as a FOCUS-shaped CSV (FOCUS 1.4, Cost and Usage columns).

Sources:
  - Claude Code: api_request events in Loki, one row per UTC day and model. Needs Loki
    (default http://localhost:3100; on the Mac, tunnel to the home server first).
  - GitHub Actions: completed workflow runs of the public repositories, one row per UTC day
    and repository, job time from the Actions API. Set GITHUB_TOKEN to avoid the
    unauthenticated rate limit.

Declared deviations from FOCUS 1.4 are listed on /inside/docs/fin/focus-export/:
EffectiveCost is empty on Claude Code rows (the subscription fee is not published),
BillingAccountId and BillingAccountName are withheld, and no Purchase rows are written.

Run from the repo root:
  python3 scripts/focus_export.py --start 2026-10-01 --end 2026-10-09 \
    --out inside/finops/focus-2026-10-01-to-2026-10-08.csv
"""
import argparse, csv, datetime as dt, json, os, urllib.parse, urllib.request

CC_REQUESTS = '{service_name=~"claude-code.*"} | event_name="api_request"'
TOKEN_FIELDS = (("input_tokens", "x_InputTokens"), ("output_tokens", "x_OutputTokens"),
                ("cache_read_tokens", "x_CacheReadTokens"), ("cache_creation_tokens", "x_CacheWriteTokens"))
REPOS = ("uncovertechtalent/machinebehavior.io", "uncovertechtalent/tychat.io",
         "uncovertechtalent/agent-observability")
LINUX_2CORE_USD_PER_MIN = 0.006  # docs.github.com, GitHub Actions billing, checked 2026-10-09

COLUMNS = [
    "BilledCost", "BillingAccountId", "BillingAccountName", "BillingCurrency", "BillingPeriodStart",
    "BillingPeriodEnd", "ChargeCategory", "ChargeClass", "ChargeDescription", "ChargePeriodStart",
    "ChargePeriodEnd", "ContractedCost", "EffectiveCost", "HostProviderName", "InvoiceIssuerName",
    "ListCost", "PricingQuantity", "PricingUnit", "ServiceProviderName", "ServiceCategory", "ServiceName",
    "ConsumedQuantity", "ConsumedUnit", "ResourceName", "SkuId", "SkuPriceId", "SkuPriceDetails", "Tags",
    "x_Requests", "x_InputTokens", "x_OutputTokens", "x_CacheReadTokens", "x_CacheWriteTokens",
    "x_PrivateRepoEquivalentCost",
]


def iso(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def loki_vector(base, query, at):
    url = f"{base}/loki/api/v1/query?" + urllib.parse.urlencode({"query": query, "time": int(at.timestamp())})
    with urllib.request.urlopen(url, timeout=300) as r:
        return json.load(r)["data"]["result"]


def by_model(base, query, at):
    return {s["metric"].get("model", ""): float(s["value"][1]) for s in loki_vector(base, query, at)}


def unwrap(field):
    return f"sum by (model) (sum_over_time({CC_REQUESTS} | keep model, {field} | unwrap {field} [1d]))"


def claude_code_rows(base, days, period):
    rows = []
    for day in days:
        end = day + dt.timedelta(days=1)
        cost = by_model(base, unwrap("cost_usd"), end)
        reqs = by_model(base, f"sum by (model) (count_over_time({CC_REQUESTS} | keep model [1d]))", end)
        toks = {name: by_model(base, unwrap(field), end) for field, name in TOKEN_FIELDS}
        for model in sorted(cost):
            tokens = {name: int(toks[name].get(model, 0)) for _, name in TOKEN_FIELDS}
            total = sum(tokens.values())
            list_cost = round(cost[model], 6)
            rows.append({
                **period, "BilledCost": 0, "ChargeCategory": "Usage", "ChargeClass": "",
                "ChargeDescription": f"Claude Code API calls on {model}, covered by a subscription plan",
                "ChargePeriodStart": iso(day), "ChargePeriodEnd": iso(end),
                "ContractedCost": list_cost, "EffectiveCost": "", "HostProviderName": "Anthropic",
                "InvoiceIssuerName": "Anthropic", "ListCost": list_cost,
                "PricingQuantity": total, "PricingUnit": "Tokens", "ServiceProviderName": "Anthropic",
                "ServiceCategory": "AI and Machine Learning", "ServiceName": "Claude Code",
                "ConsumedQuantity": total, "ConsumedUnit": "Tokens", "ResourceName": "",
                "SkuId": model, "SkuPriceId": model, "SkuPriceDetails": "",
                "Tags": json.dumps({"x_Source": "loki api_request events"}),
                "x_Requests": int(reqs.get(model, 0)), **tokens, "x_PrivateRepoEquivalentCost": "",
            })
    return rows


def gh(path, token):
    req = urllib.request.Request("https://api.github.com/" + path, headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def actions_rows(days, period, token):
    first, last = days[0].date(), days[-1].date()
    rows = []
    for repo in REPOS:
        per_day = {}
        page = 1
        while True:
            d = gh(f"repos/{repo}/actions/runs?per_page=100&page={page}&status=completed&created={first}..{last}", token)
            for run in d["workflow_runs"]:
                jobs = gh(f"repos/{repo}/actions/runs/{run['id']}/jobs", token)["jobs"]
                secs = sum((ts(j["completed_at"]) - ts(j["started_at"])).total_seconds()
                           for j in jobs if j.get("started_at") and j.get("completed_at"))
                key = ts(run["run_started_at"]).date()
                runs, total = per_day.get(key, (0, 0.0))
                per_day[key] = (runs + 1, total + max(secs, 0))
            if len(d["workflow_runs"]) < 100:
                break
            page += 1
        for key in sorted(per_day):
            runs, secs = per_day[key]
            minutes = round(secs / 60, 2)
            day = dt.datetime.combine(key, dt.time(), dt.timezone.utc)
            rows.append({
                **period, "BilledCost": 0, "ChargeCategory": "Usage", "ChargeClass": "",
                "ChargeDescription": f"GitHub Actions standard Linux runner, public repository {repo}",
                "ChargePeriodStart": iso(day), "ChargePeriodEnd": iso(day + dt.timedelta(days=1)),
                "ContractedCost": 0, "EffectiveCost": 0, "HostProviderName": "GitHub",
                "InvoiceIssuerName": "GitHub", "ListCost": 0, "PricingQuantity": minutes, "PricingUnit": "Minutes",
                "ServiceProviderName": "GitHub", "ServiceCategory": "Developer Tools", "ServiceName": "GitHub Actions",
                "ConsumedQuantity": minutes, "ConsumedUnit": "Minutes", "ResourceName": repo,
                "SkuId": "actions_linux", "SkuPriceId": "actions_linux:public-repository",
                "SkuPriceDetails": json.dumps({"x_PublicRepository": True}),
                "Tags": json.dumps({"x_Source": "github actions api, job durations"}),
                "x_Requests": runs, "x_InputTokens": "", "x_OutputTokens": "", "x_CacheReadTokens": "",
                "x_CacheWriteTokens": "", "x_PrivateRepoEquivalentCost": round(minutes * LINUX_2CORE_USD_PER_MIN, 4),
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True, help="first UTC day, YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="UTC day after the last one, YYYY-MM-DD")
    ap.add_argument("--loki", default=os.environ.get("LOKI_URL", "http://localhost:3100"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    start = dt.datetime.fromisoformat(a.start).replace(tzinfo=dt.timezone.utc)
    end = dt.datetime.fromisoformat(a.end).replace(tzinfo=dt.timezone.utc)
    days = [start + dt.timedelta(days=i) for i in range((end - start).days)]
    month = start.replace(day=1)
    next_month = (month + dt.timedelta(days=32)).replace(day=1)
    period = {"BillingAccountId": "withheld", "BillingAccountName": "withheld", "BillingCurrency": "USD",
              "BillingPeriodStart": iso(month), "BillingPeriodEnd": iso(next_month)}
    rows = claude_code_rows(a.loki, days, period) + actions_rows(days, period, os.environ.get("GITHUB_TOKEN"))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    cc = [r for r in rows if r["ServiceName"] == "Claude Code"]
    gha = [r for r in rows if r["ServiceName"] == "GitHub Actions"]
    print(f"{len(rows)} rows: Claude Code {len(cc)} (ListCost USD {sum(r['ListCost'] for r in cc):.2f}), "
          f"GitHub Actions {len(gha)} ({sum(r['ConsumedQuantity'] for r in gha):.1f} min, "
          f"{sum(r['x_Requests'] for r in gha)} runs)")


if __name__ == "__main__":
    main()
