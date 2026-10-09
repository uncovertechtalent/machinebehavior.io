#!/usr/bin/env python3
"""Static text for the pages that fill their lists in the browser, so a reader or crawler without JavaScript
gets the content too. Each list sits between <!-- static:NAME --> and <!-- /static:NAME --> inside the element
the page script fills; the script replaces it on load with the live version.

- /inside/: the three sites, the latest pieces, the living documents and the repositories (map/graph.json);
- /inside/board/: the open issues by column and the issues closed in the last 30 days (GitHub Issues, as of the build);
- /inside/mission-control/: the three sites, the open incidents (inside/status/incidents.json), the gate and the feed.

Called by scripts/build_hubs.py with the board issues it read; run on its own it uses topics/topics.json.
"""
import datetime, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES = [('machinebehavior.io', 'var(--mb-data-amber)'), ('tychat.io', 'var(--mb-data-green)'), ('uncovertechtalent.com', 'var(--mb-data-blue)')]
SITE_LABEL = {'mb': 'machinebehavior.io', 'tychat': 'tychat.io', 'utt': 'uncovertechtalent.com', 'substack': 'Substack', 'github': 'GitHub', 'reddit': 'Reddit'}
BASE = 'https://machinebehavior.io'


def esc(s):
    return html.escape(str(s), quote=True)


def local(u):
    return u[len(BASE):] if u.startswith(BASE + '/') else u


def put(rel, name, body):
    p = ROOT / rel
    src = p.read_text(encoding='utf-8')
    rx = re.compile(rf'<!-- static:{name} -->.*?<!-- /static:{name} -->', re.S)
    if not rx.search(src):
        raise SystemExit(f'{rel}: no <!-- static:{name} --> block')
    new = rx.sub(lambda m: f'<!-- static:{name} -->{body}<!-- /static:{name} -->', src)
    if new != src:
        p.write_text(new, encoding='utf-8')


def fmt(d):
    try:
        return datetime.date.fromisoformat(d[:10]).strftime('%-d %b %Y')
    except ValueError:
        return ''


def site_cards():
    return ''.join(f'<div class="card"><b><span class="dot" style="background:{c}"></span> <a href="https://{h}/">{h}</a></b>'
                   f'<p class="note">Gate record: <a href="https://{h}/conformity/">https://{h}/conformity/</a></p></div>' for h, c in SITES)


def inside_front():
    g = json.loads((ROOT / 'map' / 'graph.json').read_text(encoding='utf-8'))
    src = (ROOT / 'inside' / 'index.html').read_text(encoding='utf-8')
    living = set(re.findall(r"'(/[^']*/)'", re.search(r'const LIVING = new Set\(\[(.*?)\]\)', src, re.S).group(1)))
    path = lambda n: re.sub(r'^https?://[^/]+', '', n['id'])
    inbound = {}
    nodes = {n['id']: n for n in g['nodes']}
    for l in g['links']:
        if l['kind'] == 'body' and nodes.get(l['source'], {}).get('kind') != 'tag':
            inbound.setdefault(l['target'], set()).add(l['source'])
    def piece(n):
        pth = path(n)
        return (n['kind'] in ('page', 'substack') and pth not in ('/', '/blog/', '/conformity/')
                and not (n.get('site') == 'mb' and (pth in living or pth.startswith(('/inside/', '/topics/', '/research/')))))
    prefer = {'mb': 0, 'utt': 1, 'tychat': 2, 'substack': 3}
    rows = {}
    for n in filter(piece, g['nodes']):
        k = re.sub(r'[^a-z0-9]+', ' ', n['title'].lower()).strip()
        links = len(inbound.get(n['id'], ()))
        r = rows.get(k)
        if not r:
            rows[k] = {'main': n, 'also': [], 'links': links, 'date': n.get('date', '')}
            continue
        if prefer.get(n.get('site'), 9) < prefer.get(r['main'].get('site'), 9):
            r['also'].append(r['main']); r['main'] = n
        else:
            r['also'].append(n)
        r['links'] += links; r['date'] = max(r['date'], n.get('date', ''))
    top = sorted(rows.values(), key=lambda r: (r['date'], r['links']), reverse=True)[:18]
    items = ''
    for i, r in enumerate(top, 1):
        n = r['main']
        also = ''.join(f' <a href="{esc(local(a["id"]))}">also on {esc(SITE_LABEL.get(a.get("site"), a.get("site")))}</a>' for a in r['also'])
        items += (f'<li><span class="rank">{i}</span><a class="title" href="{esc(local(n["id"]))}">{esc(n["title"])}</a>'
                  f'<span class="count">{r["links"]}<small>{"link in" if r["links"] == 1 else "links in"}</small></span>'
                  f'<span class="meta"><span>{esc(SITE_LABEL.get(n.get("site"), n.get("site")))}</span><span>{fmt(r["date"])}</span>{also}</span></li>')
    put('inside/index.html', 'latest', items)
    put('inside/index.html', 'sites', site_cards())
    liv = sorted((n for n in g['nodes'] if n.get('site') == 'mb' and n['kind'] == 'page' and path(n) in living), key=lambda n: n.get('date', ''), reverse=True)
    put('inside/index.html', 'living', ''.join(f'<li><a href="{esc(path(n))}">{esc(n["title"])}</a><span class="mono">{"updated " + fmt(n["date"]) if n.get("date") else ""}</span></li>' for n in liv))
    repos = sorted((n for n in g['nodes'] if n['kind'] == 'github'), key=lambda n: len(inbound.get(n['id'], ())), reverse=True)
    put('inside/index.html', 'repos', ''.join(f'<li><a href="{esc(n["id"])}">{esc(n["title"])}</a><span class="mono">GitHub</span></li>' for n in repos))
    return len(top)


COLS = [('backlog', 'Backlog'), ('ready', 'Ready'), ('progress', 'In progress'), ('blocked', 'Blocked'), ('done', 'Done in the last 30 days')]


def board(issues):
    cutoff = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    col = {}
    for i in issues:
        if not any(l.startswith('type: ') for l in i['labels']):
            continue  # untriaged reports stay off the page, as on the live board
        st = [l[len('status: '):] for l in i['labels'] if l.startswith('status: ')]
        if i['state'] == 'closed':
            if i.get('reason') == 'not_planned' or not i.get('closed') or i['closed'] < cutoff:
                continue
            c = 'done'
        else:
            c = 'blocked' if 'blocked' in st else 'progress' if 'in progress' in st else 'ready' if 'ready' in st else 'backlog'
        col.setdefault(c, []).append(i)
    h = ''
    for key, name in COLS:
        rows = sorted(col.get(key, []), key=lambda i: -i['n'])
        li = ''.join(f'<li><a href="{esc(i["u"])}">#{i["n"]} {esc(i["t"])}</a><span class="mb-links-meta">'
                     f'{esc(" · ".join(l for l in i["labels"] if l.startswith(("type: ", "area: ")) or re.fullmatch(r"P[0-3]", l)))}</span></li>' for i in rows)
        h += f'<section class="static-col"><h2>{name} <span class="mb-n">{len(rows)}</span></h2><ul class="mb-links">{li}</ul></section>'
    put('inside/board/index.html', 'issues', h)
    put('inside/board/index.html', 'asof', f'Issues as of the last build, {datetime.date.today().isoformat()}; the snapshot of the last deploy loads in the browser.')
    return sum(len(v) for v in col.values())


def mission_control():
    put('inside/mission-control/index.html', 'sites', ''.join(
        f'<div class="site"><b><span class="dot" style="background:{c}"></span>{h}</b><span class="f"><a href="https://{h}/conformity/">gate record</a></span></div>' for h, c in SITES))
    inc = json.loads((ROOT / 'inside' / 'status' / 'incidents.json').read_text(encoding='utf-8'))
    open_ = [i for i in inc['incidents'] if i['stage'] != 'resolved']
    li = ''.join(f'<li><a href="/inside/status/#{esc(i["id"])}">{esc(i["title"])}</a><span class="meta"><span class="stage {esc(i["stage"])}">{esc(i["stage"])}</span>'
                 f'<span>impact {esc(i["impact"])}</span><span>since {esc(i["started"])}</span></span></li>' for i in open_)
    put('inside/mission-control/index.html', 'incidents', li or '<li class="empty">none open at the last build</li>')
    return len(open_)


def main(issues=None):
    if issues is None:
        tj = ROOT / 'topics' / 'topics.json'
        issues = json.loads(tj.read_text(encoding='utf-8')).get('issues', []) if tj.exists() else []
    n_items = inside_front()
    n_issues = board(issues)
    n_inc = mission_control()
    print(f'fallbacks: Inside {n_items} pieces, board {n_issues} issues, Mission Control {n_inc} open incidents')


if __name__ == '__main__':
    sys.exit(main())
