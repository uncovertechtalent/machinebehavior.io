#!/usr/bin/env python3
"""Snapshot the GitHub Issues of this repository for the board at /inside/board/.

Run by the deploy job (artifact only, never committed). Writes inside/board/issues.json with the open
issues and the issues closed in the last 30 days, pull requests skipped. The board page reads this file,
so a visitor's browser sends no request to GitHub.

Only triaged issues (with a 'type: ...' label, which only a maintainer can set) carry their title and text.
New reports without one are counted, so text from a stranger reaches the page only after triage.

Auth: GH_TOKEN if set, then anonymous (the repository is public), as in the deploy feed step.
Run from the repo root:  python3 scripts/board_snapshot.py inside/board/issues.json
"""
import datetime, json, os, re, sys, urllib.error, urllib.parse, urllib.request

REPO = 'uncovertechtalent/machinebehavior.io'
DAYS = 30
BODY_MAX = 2000
OUT = sys.argv[1] if len(sys.argv) > 1 else 'inside/board/issues.json'
NOW = datetime.datetime.now(datetime.timezone.utc)


def fetch(url):
    last = None
    for auth in (True, False):
        if auth and not os.environ.get('GH_TOKEN'):
            continue
        h = {'Accept': 'application/vnd.github+json', 'User-Agent': 'machinebehavior.io board snapshot'}
        if auth:
            h['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=20))
        except (urllib.error.URLError, ValueError) as e:
            print(f'::warning::issues {url.split("?")[1]} (auth={auth}) failed: {e}')
            last = e
    raise SystemExit(f'issues snapshot failed: {last}')


def pages(params):
    out = []
    for page in range(1, 11):  # 1000 issues is far beyond this repository
        q = urllib.parse.urlencode({**params, 'per_page': 100, 'page': page})
        batch = fetch(f'https://api.github.com/repos/{REPO}/issues?{q}')
        out += batch
        if len(batch) < 100:
            break
    return out


since = (NOW - datetime.timedelta(days=DAYS)).strftime('%Y-%m-%dT%H:%M:%SZ')
raw = pages({'state': 'open'}) + [i for i in pages({'state': 'closed', 'since': since})
                                  if i.get('closed_at') and i['closed_at'] >= since]

issues, untriaged = [], 0
for i in raw:
    if 'pull_request' in i:
        continue
    labels = sorted(l['name'] for l in i.get('labels', []))
    if not any(l.startswith('type: ') for l in labels):
        untriaged += i['state'] == 'open'
        continue
    body = re.sub(r'<!--.*?-->', '', i.get('body') or '', flags=re.S).strip()
    if len(body) > BODY_MAX:
        body = body[:BODY_MAX].rsplit(' ', 1)[0] + ' …'
    issues.append({
        'n': i['number'], 'title': i['title'], 'state': i['state'], 'reason': i.get('state_reason'),
        'labels': labels, 'assignees': [a['login'] for a in i.get('assignees') or []],
        'milestone': (i.get('milestone') or {}).get('title'),
        'created': i['created_at'], 'updated': i['updated_at'], 'closed': i.get('closed_at'),
        'comments': i.get('comments', 0), 'url': i['html_url'], 'body': body,
    })
issues.sort(key=lambda x: x['n'])

out = {'generated': NOW.strftime('%Y-%m-%dT%H:%M:%SZ'), 'repo': REPO, 'closed_window_days': DAYS,
       'untriaged': untriaged, 'issues': issues}
os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
with open(OUT, 'w') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print(f'board snapshot: {sum(x["state"] == "open" for x in issues)} open, {sum(x["state"] == "closed" for x in issues)} closed in {DAYS} days, '
      f'{untriaged} untriaged -> {OUT}')
