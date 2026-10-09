#!/usr/bin/env python3
"""Build the one search index of Inside: /inside/search.json.

Sources, merged into one list of items:
- the docs pages, from inside/docs/search.json (written by scripts/build_docs.py);
- the services, from inside/services/services.json (written by scripts/build_inside.py), when present;
- every other node of the map, from map/graph.json (pages on the three sites, Substack posts, repos, threads).

The top bar (/inside/bar.js) and the results page (/inside/search/) read only this file. The deploy job runs this
script again after it refreshes the map, so the deployed index matches the deployed graph (artifact only).
Stdlib only. Run from the repo root:  python3 scripts/build_search.py
"""
import datetime, json, sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'inside' / 'search.json'
BASE = 'https://machinebehavior.io'

SITE_GROUPS = {
    'mb': ('machinebehavior.io', '#FFB547'), 'utt': ('uncovertechtalent.com', '#6FA8FF'), 'tychat': ('tychat.io', '#3DDC97'),
    'substack': ('Substack', '#FF8FD8'), 'github': ('GitHub', '#EFE6D2'), 'reddit': ('Reddit', '#FF4D5E'),
    'dashboard': ('Grafana dashboard', '#5EEAD4'),
}
SKIP_PATHS = ('/inside/search/',)


def main():
    groups, items, seen = {}, [], set()

    docs = json.loads((ROOT / 'inside' / 'docs' / 'search.json').read_text(encoding='utf-8'))
    for key, sp in docs['spaces'].items():
        groups['doc-' + key] = {'name': sp['name'] + ' docs', 'color': sp['color']}
    for p in docs['pages']:
        items.append({'t': p['t'], 'u': p['u'], 'g': 'doc-' + p['s'], 'd': p['d'], 'l': p['l'], 'x': p['x'][:280]})
        seen.add(p['u'])

    svc_file = ROOT / 'inside' / 'services' / 'services.json'
    if svc_file.exists():
        svc = json.loads(svc_file.read_text(encoding='utf-8'))
        groups['service'] = {'name': 'Service', 'color': '#FFB547'}
        for s in svc['services']:
            items.append({'t': s['name'], 'u': s['url'], 'g': 'service', 'd': s['description'],
                          'l': [s['tier'], s['lifecycle'], s['system'], s['owner']], 'w': 2})
            seen.add(s['url'])

    graph = json.loads((ROOT / 'map' / 'graph.json').read_text(encoding='utf-8'))
    for n in graph['nodes']:
        if n['kind'] in ('doc', 'tag', 'service'):
            continue
        u = n['id']
        if u.startswith(BASE + '/'):
            u = u[len(BASE):]
        path = urlparse(n['id']).path
        if u in seen or path in SKIP_PATHS or (u.startswith('/inside/services/') and 'service' in groups):
            continue
        g = n.get('site') if n.get('site') in SITE_GROUPS else n['kind']
        if g not in SITE_GROUPS:
            continue
        groups.setdefault(g, {'name': SITE_GROUPS[g][0], 'color': SITE_GROUPS[g][1]})
        it = {'t': n['title'], 'u': u, 'g': g, 'd': n.get('desc', '')}
        if g == 'mb':
            it['w'] = 1
        items.append(it)
        seen.add(u)

    out = {'generated': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'),
           'map_generated': graph.get('generated'), 'groups': groups, 'items': items}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    from collections import Counter
    c = Counter(i['g'].split('-')[0] for i in items)
    print(f'search index: {len(items)} items, {OUT.stat().st_size // 1024} KB', dict(c))


if __name__ == '__main__':
    sys.exit(main())
