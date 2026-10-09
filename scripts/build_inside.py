#!/usr/bin/env python3
"""Build the Inside pages that are not docs, then the site-wide search index.

Steps, in order:
1. the service catalog: services/*.yml -> /inside/services/ and one page per service, plus inside/services/services.json;
2. sync the top bar into the hand-written Inside pages (scripts/inside_chrome.py);
3. managed blocks in sitemap.xml and llms.txt;
4. the search index /inside/search.json (scripts/build_search.py).

Every YAML file is validated; an unknown field, a missing field, a value outside the allowed set, a docs link to a
page that does not exist or a dependency on an unknown service stops the build.

Run after scripts/build_docs.py, from the repo root:  python3 scripts/build_inside.py
"""
import datetime, json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inside_chrome
import build_search
import mini_yaml
from inside_chrome import esc

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://machinebehavior.io'
REPO = 'https://github.com/uncovertechtalent/machinebehavior.io'
TODAY = datetime.date.today().isoformat()
GRAFANA = 'https://grafana.scoetzee.de/public-dashboards/'

TIERS = {
    1: ('Tier 1', 'Readers meet it directly, or it decides whether a deploy goes out. First in line when something breaks.'),
    2: ('Tier 2', 'Keeps the platform observable and the research running: data, dashboards, search, the agents. Fixed the same day.'),
    3: ('Tier 3', 'Tooling a reader does not meet directly. Waits for the next working session.'),
}
LIFECYCLES = {'experimental': 'Experimental', 'production': 'Production', 'deprecated': 'Deprecated'}
SYSTEMS = ['Publishing', 'Observability', 'Research tooling', 'Agents']

# field -> (required, type)
SERVICE_FIELDS = {
    'id': (True, str), 'name': (True, str), 'description': (True, str), 'owner': (True, str), 'operator': (False, str),
    'tier': (True, int), 'lifecycle': (True, str), 'system': (True, str), 'url': (False, str), 'repository': (False, str),
    'dashboard': (False, dict), 'slo': (False, list), 'docs': (True, list), 'runbooks': (True, list),
    'depends_on': (True, list), 'external': (False, list), 'status': (False, dict),
}


def fail(msg):
    sys.exit(f'build_inside: {msg}')


def git_date(path):
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', str(path)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', str(path)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return TODAY if dirty or not out else out
    except Exception:
        return TODAY


DOCS = {p['u']: p for p in json.loads((ROOT / 'inside' / 'docs' / 'search.json').read_text(encoding='utf-8'))['pages']}


def doc_ref(ref, where):
    """'doc:space/slug' -> (url, title); the page must exist in the docs build."""
    if not isinstance(ref, str) or not ref.startswith('doc:'):
        fail(f'{where}: docs and runbooks entries are doc:space/slug, got {ref!r}')
    space, _, slug = ref[4:].partition('/')
    url = f'/inside/docs/{space}/' + (f'{slug}/' if slug and slug != 'index' else '')
    if url not in DOCS:
        fail(f'{where}: {ref} is not a docs page (run scripts/build_docs.py first?)')
    return url, DOCS[url]['t']


# ---------- services ----------
def load_services():
    out = {}
    files = sorted((ROOT / 'services').glob('*.yml'))
    if not files:
        fail('no services/*.yml')
    for f in files:
        where = f.relative_to(ROOT).as_posix()
        try:
            s = mini_yaml.load_file(f)
        except mini_yaml.YamlError as e:
            fail(str(e))
        if not isinstance(s, dict):
            fail(f'{where}: top level must be a mapping')
        for k in s:
            if k not in SERVICE_FIELDS:
                fail(f'{where}: unknown field {k}')
        for k, (req, typ) in SERVICE_FIELDS.items():
            if s.get(k) is None:
                if req:
                    fail(f'{where}: missing {k}')
                continue
            if not isinstance(s[k], typ):
                fail(f'{where}: {k} must be {typ.__name__}')
        if s['id'] != f.stem:
            fail(f'{where}: id {s["id"]} does not match the file name')
        if s['tier'] not in TIERS:
            fail(f'{where}: tier must be one of {sorted(TIERS)}')
        if s['lifecycle'] not in LIFECYCLES:
            fail(f'{where}: lifecycle must be one of {sorted(LIFECYCLES)}')
        if s['system'] not in SYSTEMS:
            fail(f'{where}: system must be one of {SYSTEMS}')
        d = s.get('dashboard')
        if d and (set(d) != {'name', 'url'} or not str(d['url']).startswith(GRAFANA)):
            fail(f'{where}: dashboard needs name and a public dashboard url under {GRAFANA}')
        for slo in s.get('slo') or []:
            if not isinstance(slo, dict) or set(slo) != {'name', 'target', 'good'}:
                fail(f'{where}: each slo needs name, target and good')
        for k in ('url', 'repository'):
            v = s.get(k)
            if v and not (v.startswith('https://') or v == 'private'):
                fail(f'{where}: {k} must be an https URL' + (' or "private"' if k == 'repository' else ''))
        st = s.get('status') or {}
        for k in st:
            if k not in ('gate', 'deploys'):
                fail(f'{where}: status keys are gate and deploys')
        s['docs_l'] = [doc_ref(r, where) for r in s['docs']]
        s['runbooks_l'] = [doc_ref(r, where) for r in s['runbooks']]
        s['src'] = where
        s['updated'] = git_date(f)
        s['page'] = f'/inside/services/{s["id"]}/'
        out[s['id']] = s
    for s in out.values():
        for dep in s['depends_on']:
            if dep not in out:
                fail(f'{s["src"]}: depends_on {dep} is not a service')
            if dep == s['id']:
                fail(f'{s["src"]}: a service cannot depend on itself')
    for s in out.values():
        s['used_by'] = sorted((o for o in out.values() if s['id'] in o['depends_on']), key=lambda o: o['name'].lower())
    return out


def head(title, desc, url, og_title, modified, extra=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{url}">
<meta property="og:site_name" content="Machine Behavior">
<meta property="og:title" content="{esc(og_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE}/inside/og.png">
<meta property="og:image:width" content="2400">
<meta property="og:image:height" content="1254">
<meta property="og:image:alt" content="The Inside front page of machinebehavior.io.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/inside/og.png">
<meta property="article:modified_time" content="{modified}">
{extra}<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛋️</text></svg>">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/inside/docs/docs.css">
<link rel="stylesheet" href="/inside/bar.css">
<link rel="stylesheet" href="/inside/inside.css">
</head>'''


def foot(src_links):
    return (f'<footer>{src_links}<br><span class="conf mono" data-conformity>conformity: <a class="mono" href="/conformity/">latest run</a></span> '
            '(self-assessment, not a certification)</footer>\n'
            '<script src="/inside/bar.js" defer></script>\n<script src="/conformity/footer.js" defer></script>')


def chip_tier(t):
    return f'<span class="chip tier-{t}" title="{esc(TIERS[t][1])}">{TIERS[t][0]}</span>'


def chip_life(l):
    return f'<span class="chip life-{l}">{LIFECYCLES[l]}</span>'


def ext_link(url, text):
    return f'<a href="{esc(url)}">{esc(text)}</a>'


def service_page(s, all_s, status_live):
    rows = [('Owner', esc(s['owner']))]
    if s.get('operator'):
        rows.append(('Operated by', esc(s['operator'])))
    rows += [('Tier', f'{chip_tier(s["tier"])} {esc(TIERS[s["tier"]][1])}'),
             ('Lifecycle', chip_life(s['lifecycle'])),
             ('System', f'<a href="/inside/services/#{esc(s["system"].lower().replace(" ", "-"))}">{esc(s["system"])}</a>')]
    if s.get('url'):
        rows.append(('Address', ext_link(s['url'], s['url'].replace('https://', '').rstrip('/') if 'public-dashboards' not in s['url'] else 'public dashboard')))
    if s.get('repository'):
        rows.append(('Repository', 'private repository' if s['repository'] == 'private' else ext_link(s['repository'], s['repository'].replace('https://github.com/', ''))))
    if s.get('dashboard'):
        rows.append(('Dashboard', ext_link(s['dashboard']['url'], s['dashboard']['name'] + ' (Grafana)')))
    if status_live:
        rows.append(('Current state', f'<a href="/inside/status/#{esc(s["id"])}">on the status page</a>'))
    facts = '<dl class="facts">' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows) + '</dl>'

    slo = ''
    if s.get('slo'):
        slo = ('<h2 id="slo">Service level objectives</h2><div class="tbl"><table><thead><tr><th>SLO</th><th>Target</th><th>Good event</th></tr></thead><tbody>' +
               ''.join(f'<tr><td>{esc(o["name"])}</td><td class="mono">{esc(o["target"])}</td><td>{esc(o["good"])}</td></tr>' for o in s['slo']) +
               '</tbody></table></div><p class="note">Defined and measured in Prometheus; see <a href="/inside/docs/obs/alerts-and-slos/">Alerts and SLOs</a>.</p>')
    else:
        slo = '<h2 id="slo">Service level objectives</h2><p class="note">None defined. Health is read from the records listed on the status page.</p>'

    def links(items, empty):
        if not items:
            return f'<p class="note">{empty}</p>'
        return '<ul class="links">' + ''.join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in items) + '</ul>'

    deps = links([(all_s[d]['page'], all_s[d]['name']) for d in s['depends_on']], 'No other service in this catalog.')
    used = links([(o['page'], o['name']) for o in s['used_by']], 'No other service in this catalog.')
    ext = ', '.join(esc(x) for x in s.get('external') or []) or 'none'
    desc = ' '.join(s['description'].split())
    body = f'''<h2 id="docs">Docs</h2>{links(s["docs_l"], "No docs page yet.")}
<h2 id="runbooks">Runbooks</h2>{links(s["runbooks_l"], "No runbook yet.")}
{slo}
<h2 id="dependencies">Dependencies</h2>
<div class="cols"><div><h3>Depends on</h3>{deps}<p class="note">Outside the catalog: {ext}.</p></div><div><h3>Used by</h3>{used}</div></div>'''
    title = f'{s["name"]} · Services · Inside · Machine Behavior'
    extra = (f'<meta name="service-tier" content="{s["tier"]}">\n<meta name="service-lifecycle" content="{s["lifecycle"]}">\n'
             f'<meta property="article:tag" content="{esc(s["system"])}">\n<link rel="up" href="/inside/services/">\n')
    return f'''{head(title, desc, s["page"], s["name"] + " (service)", s["updated"], extra)}
<body>
{inside_chrome.bar("services")}
<main class="wrap svc" id="main">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/inside/">Inside</a><a href="/inside/services/">Services</a></nav>
<h1>{esc(s["name"])}</h1>
<div class="byline"><span>service</span><span>updated {s["updated"]}</span><a class="report" href="{REPO}/blob/main/{esc(s["src"])}">edit the YAML</a></div>
<p class="lede">{esc(desc)}</p>
{facts}
<article class="doc">
{body}
</article>
</main>
{foot(f'Service catalog · built from <a href="{REPO}/blob/main/{esc(s["src"])}">{esc(s["src"])}</a> by <a href="{REPO}/blob/main/scripts/build_inside.py">build_inside.py</a> · <a href="/inside/services/services.json">services.json</a>')}
</body>
</html>
'''


def catalog_page(svcs, status_live):
    newest = max(s['updated'] for s in svcs.values())
    groups = ''
    for sys_name in SYSTEMS:
        members = sorted((s for s in svcs.values() if s['system'] == sys_name), key=lambda s: (s['tier'], s['name'].lower()))
        if not members:
            continue
        cards = ''
        for s in members:
            slo = ', '.join(f'{o["name"]} {o["target"]}' for o in s.get('slo') or []) or 'none'
            dash = ext_link(s['dashboard']['url'], s['dashboard']['name']) if s.get('dashboard') else '<span class="dim">none</span>'
            stat = f' · <a href="/inside/status/#{esc(s["id"])}">status</a>' if status_live else ''
            cards += (f'<li class="svc-card" id="{esc(s["id"])}"><div class="svc-top"><a class="svc-name" href="{s["page"]}">{esc(s["name"])}</a>'
                      f'{chip_tier(s["tier"])}{chip_life(s["lifecycle"])}</div>'
                      f'<p class="svc-desc">{esc(" ".join(s["description"].split()))}</p>'
                      f'<dl class="svc-facts"><dt>owner</dt><dd>{esc(s["owner"])}</dd><dt>SLO</dt><dd>{esc(slo)}</dd>'
                      f'<dt>dashboard</dt><dd>{dash}</dd><dt>docs</dt><dd>{len(s["docs_l"])} pages · {len(s["runbooks_l"])} runbooks{stat}</dd></dl></li>')
        sid = sys_name.lower().replace(' ', '-')
        groups += f'<section class="sys" aria-labelledby="{sid}"><h2 id="{sid}">{esc(sys_name)} <span class="n">{len(members)}</span></h2><ul class="svc-list">{cards}</ul></section>'
    tiers = ''.join(f'<li>{chip_tier(t)} {esc(d)}</li>' for t, (_, d) in TIERS.items())
    n = len(svcs)
    desc = f'The service catalog of the platform behind machinebehavior.io: {n} services with owner, tier, lifecycle, SLO, dashboard, runbooks, docs, repository and dependencies, built from YAML in the repository.'
    return f'''{head("Services · Inside · Machine Behavior", desc, "/inside/services/", "Inside services: the service catalog", newest)}
<body>
{inside_chrome.bar("services")}
<main class="wrap" id="main">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/inside/">Inside</a><a href="/inside/services/">Services</a></nav>
<h1>Services</h1>
<p class="lede">{n} services run the platform: the three sites, the gate and the deploy job, the build tools, the observability stack, the research tools and the agent sessions. Each one has an owner, a tier, a lifecycle and the links an on-call responder needs. The catalog is built from <a href="{REPO}/tree/main/services">one YAML file per service</a>, validated at build; updated {newest}.</p>
<ul class="tiers">{tiers}</ul>
{groups}
<p class="note">Machine-readable: <a href="/inside/services/services.json">services.json</a>. How to add or change a service: <a href="/inside/docs/eng/service-catalog/">Service catalog</a> in the Engineering docs.</p>
</main>
{foot(f'Service catalog · built from <a href="{REPO}/tree/main/services">services/*.yml</a> by <a href="{REPO}/blob/main/scripts/build_inside.py">build_inside.py</a>')}
</body>
</html>
'''


def build_services():
    svcs = load_services()
    status_live = (ROOT / 'inside' / 'status' / 'index.html').exists()
    out = ROOT / 'inside' / 'services'
    for d in out.iterdir() if out.exists() else []:
        if d.is_dir() and d.name not in svcs:
            for f in d.iterdir():
                f.unlink()
            d.rmdir()
    out.mkdir(parents=True, exist_ok=True)
    for s in svcs.values():
        p = out / s['id'] / 'index.html'
        p.parent.mkdir(exist_ok=True)
        p.write_text(service_page(s, svcs, status_live), encoding='utf-8')
    (out / 'index.html').write_text(catalog_page(svcs, status_live), encoding='utf-8')
    data = {'generated': TODAY, 'source': f'{REPO}/tree/main/services', 'services': [
        {'id': s['id'], 'name': s['name'], 'url': s['page'], 'description': ' '.join(s['description'].split()), 'owner': s['owner'],
         'operator': s.get('operator'), 'tier': s['tier'], 'lifecycle': s['lifecycle'], 'system': s['system'], 'address': s.get('url'),
         'repository': s.get('repository'), 'dashboard': s.get('dashboard'), 'slo': s.get('slo') or [],
         'docs': [u for u, _ in s['docs_l']], 'runbooks': [u for u, _ in s['runbooks_l']], 'depends_on': s['depends_on'],
         'external': s.get('external') or [], 'status': s.get('status') or {}, 'updated': s['updated']}
        for s in sorted(svcs.values(), key=lambda s: (SYSTEMS.index(s['system']), s['tier'], s['name'].lower()))]}
    (out / 'services.json').write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'services: {len(svcs)} pages')
    return svcs


def main():
    svcs = build_services()
    stale, missing = inside_chrome.sync()
    print(f'bar synced in {len(stale)} page(s)')
    if missing:
        for m in missing:
            print('no bar block or asset:', m)
        sys.exit(1)
    newest = max(s['updated'] for s in svcs.values())
    urls = [('/inside/services/', newest)] + [(s['page'], s['updated']) for s in sorted(svcs.values(), key=lambda s: s['page'])]
    inside_chrome.sitemap_block('services', urls)
    sec = (f'The service catalog at {BASE}/inside/services/ ({len(svcs)} services), built from YAML in the repository. '
           f'Machine-readable: {BASE}/inside/services/services.json.\n\n')
    for s in sorted(svcs.values(), key=lambda s: (SYSTEMS.index(s['system']), s['tier'], s['name'].lower())):
        sec += f'- [{s["name"]}]({BASE}{s["page"]}): {s["system"]}, tier {s["tier"]}, {s["lifecycle"]}. {" ".join(s["description"].split())}\n'
    inside_chrome.llms_section('Inside services', sec)
    build_search.main()


if __name__ == '__main__':
    main()
