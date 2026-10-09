#!/usr/bin/env python3
"""Build the Inside pages that are not docs, then the site-wide search index.

Steps, in order:
1. the status page: incidents/*.yml plus the catalog -> /inside/status/ and inside/status/incidents.json;
2. the service catalog: services/*.yml -> /inside/services/ and one page per service, plus inside/services/services.json;
3. sync the top bar into the hand-written Inside pages (scripts/inside_chrome.py);
4. managed blocks in sitemap.xml and llms.txt;
5. the search index /inside/search.json (scripts/build_search.py).

Every YAML file is validated; an unknown field, a missing field, a value outside the allowed set, a docs link to a
page that does not exist or a dependency on an unknown service stops the build.

Run after scripts/build_docs.py, from the repo root:  python3 scripts/build_inside.py
"""
import datetime, json, re, subprocess, sys
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
{inside_chrome.banner()}
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
{inside_chrome.banner()}
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


def build_services(svcs, status_live):
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



# ---------- incidents and status ----------
STAGES = ['investigating', 'identified', 'monitoring', 'resolved']
IMPACTS = {'none': 'No reader impact', 'minor': 'Minor', 'major': 'Major', 'critical': 'Critical'}
INCIDENT_FIELDS = {
    'id': (True, str), 'title': (True, str), 'services': (True, list), 'impact': (True, str), 'started': (True, str),
    'resolved': (False, str), 'summary': (True, str), 'updates': (True, list), 'follow_up': (False, str), 'postmortem': (False, list),
}
WHEN = re.compile(r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}Z)?$')


def load_incidents(svcs):
    out = []
    for f in sorted((ROOT / 'incidents').glob('*.yml')):
        where = f.relative_to(ROOT).as_posix()
        try:
            i = mini_yaml.load_file(f)
        except mini_yaml.YamlError as e:
            fail(str(e))
        for k in i:
            if k not in INCIDENT_FIELDS:
                fail(f'{where}: unknown field {k}')
        for k, (req, typ) in INCIDENT_FIELDS.items():
            if i.get(k) is None:
                if req:
                    fail(f'{where}: missing {k}')
                continue
            if not isinstance(i[k], typ):
                fail(f'{where}: {k} must be {typ.__name__}')
        if i['id'] != f.stem:
            fail(f'{where}: id does not match the file name')
        if i['impact'] not in IMPACTS:
            fail(f'{where}: impact must be one of {list(IMPACTS)}')
        for sid in i['services']:
            if sid not in svcs:
                fail(f'{where}: service {sid} is not in the catalog')
        for k in ('started', 'resolved'):
            if i.get(k) and not WHEN.match(i[k]):
                fail(f'{where}: {k} must be YYYY-MM-DD or YYYY-MM-DDTHH:MMZ')
        if not i['updates']:
            fail(f'{where}: at least one update')
        last = -1
        for u in i['updates']:
            if not isinstance(u, dict) or set(u) != {'stage', 'at', 'text'}:
                fail(f'{where}: each update needs stage, at and text')
            if u['stage'] not in STAGES:
                fail(f'{where}: stage must be one of {STAGES}')
            if not WHEN.match(str(u['at'])):
                fail(f'{where}: update time must be YYYY-MM-DD or YYYY-MM-DDTHH:MMZ')
            if STAGES.index(u['stage']) < last:
                fail(f'{where}: stages go forward: investigating, identified, monitoring, resolved')
            last = STAGES.index(u['stage'])
        stage = i['updates'][-1]['stage']
        if (stage == 'resolved') != bool(i.get('resolved')):
            fail(f'{where}: "resolved" is set exactly when the last update is resolved')
        i['stage'] = stage
        i['postmortem_l'] = [doc_ref(r, where) for r in i.get('postmortem') or []]
        i['src'] = where
        out.append(i)
    out.sort(key=lambda i: (i['started'], i['id']), reverse=True)
    return out


def when(t):
    t = str(t)
    return t.replace('T', ' ').replace('Z', ' UTC') if 'T' in t else t + ', time not recorded'


def incident_html(i, svcs):
    open_ = i['stage'] != 'resolved'
    svc_links = ', '.join(f'<a href="{svcs[s]["page"]}">{esc(svcs[s]["name"])}</a>' for s in i['services'])
    tl = ''.join(f'<li><span class="when">{esc(when(u["at"]))} · <span class="stage {u["stage"]}">{u["stage"].capitalize()}</span></span>{esc(" ".join(u["text"].split()))}</li>'
                 for u in i['updates'])
    pm = ''
    if i['postmortem_l']:
        pm = '<p class="services">Write-up and runbooks: ' + ', '.join(f'<a href="{u}">{esc(t)}</a>' for u, t in i['postmortem_l']) + '</p>'
    fu = f'<p><b>Follow-up.</b> {esc(" ".join(i["follow_up"].split()))}</p>' if i.get('follow_up') else ''
    span = f'{esc(when(i["started"]))} to {esc(when(i["resolved"]))}' if i.get('resolved') else f'since {esc(when(i["started"]))}'
    return (f'<article class="inc" id="{esc(i["id"])}"><div class="inc-top"><h3>{esc(i["title"])}</h3>'
            f'<span class="stage {i["stage"]}">{i["stage"].capitalize()}</span></div>'
            f'<div class="meta"><span>{span}</span><span>impact: {esc(IMPACTS[i["impact"]].lower())}</span>'
            f'<a href="{REPO}/blob/main/{esc(i["src"])}">record</a></div>'
            f'<p>{esc(" ".join(i["summary"].split()))}</p><p class="services">Services: {svc_links}</p>{fu}{pm}'
            f'<details{" open" if open_ else ""}><summary>Timeline, {len(i["updates"])} updates</summary><ol class="timeline">{tl}</ol></details></article>')


def status_page(svcs, incidents):
    open_inc = [i for i in incidents if i['stage'] != 'resolved']
    by_svc = {}
    for i in open_inc:
        if i['impact'] == 'none':
            continue
        for sid in i['services']:
            by_svc.setdefault(sid, i)
    order = sorted(svcs.values(), key=lambda s: (SYSTEMS.index(s['system']), s['tier'], s['name'].lower()))
    rows, cfg = '', []
    for s in order:
        st = s.get('status') or {}
        src = []
        if st.get('gate'):
            host = st['gate'].split('/')[2]
            src.append(f'<a href="{esc(st["gate"])}">gate record of {esc(host)}</a>')
        if st.get('deploys'):
            src.append('<a href="/inside/deploys.json">deploy feed</a>')
        if s['id'] == 'map-crawler':
            src.append('<a href="/inside/search.json">map snapshot time</a>')
        if not src and s.get('dashboard'):
            src.append(f'no live check from this page; watched on <a href="{esc(s["dashboard"]["url"])}">{esc(s["dashboard"]["name"])}</a>')
        elif not src:
            src.append('no live check from this page; checked by the gate on every push' if s['id'] == 'docs-build' else 'no live check from this page')
        inc = by_svc.get(s['id'])
        if inc:
            src.append(f'open incident: <a href="#{esc(inc["id"])}">{esc(inc["title"])}</a>')
        live = bool(st) or s['id'] == 'map-crawler'
        state, light = ('Degraded', 'warn') if inc else (('reading', 'none') if live else ('No live check', 'none'))
        rows += (f'<li id="{esc(s["id"])}"><span class="light {light}" data-light></span><a class="st-name" href="{s["page"]}">{esc(s["name"])}</a>'
                 f'<span class="st-state" data-state>{state}</span><span class="st-why">{" · ".join(src)}</span></li>')
        cfg.append({'id': s['id'], 'gate': st.get('gate'), 'deploys': st.get('deploys'), 'map': s['id'] == 'map-crawler',
                    'incident': bool(inc), 'site': bool(st.get('gate')) and s.get('url') == 'https://' + st['gate'].split('/')[2] + '/'})
    open_html = ''.join(incident_html(i, svcs) for i in open_inc) or '<p class="note">No open incident.</p>'
    hist_html = ''.join(incident_html(i, svcs) for i in incidents if i['stage'] == 'resolved')
    newest = max([str(u['at'])[:10] for i in incidents for u in i['updates']] + [s['updated'] for s in svcs.values()])
    desc = (f'Status of the {len(svcs)} services behind machinebehavior.io, read from the gate records and the deploy feed, and the incident '
            'history with the stages Investigating, Identified, Monitoring and Resolved.')
    return f'''{head("Status · Inside · Machine Behavior", desc, "/inside/status/", "Inside status: services and incidents", newest)}
<body>
{inside_chrome.bar("status")}
{inside_chrome.banner()}
<main class="wrap" id="main">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/inside/">Inside</a><a href="/inside/status/">Status</a></nav>
<h1>Status</h1>
<p class="lede">The current state of each service in the <a href="/inside/services/">catalog</a>, read in your browser from the records this site already publishes: each site's gate record and the deploy feed written at the last deploy. Services without such a record say so, and an open incident marks the services it affects. Incidents are written blameless; updated {newest}.</p>
<div class="overall" id="overall"><span class="light none" id="ov-light"></span><b id="ov-text">Reading the records</b><span class="asof" id="ov-asof"></span></div>
<h2 class="sec">Services</h2>
<ul class="st-list">{rows}</ul>
<h2 class="sec" id="open">Open incidents</h2>
{open_html}
<h2 class="sec" id="history">Incident history</h2>
{hist_html}
<section class="how"><h2 class="sec">How the state is decided</h2>
<ul class="links">
<li><b>Operational</b>: the gate record passes and the last workflow run on the deploy feed succeeded.</li>
<li><b>Degraded</b>: the gate fails (new deploys are blocked and the previous build stays live), the last run failed, the map snapshot is older than eight days, or an open incident with reader impact names the service.</li>
<li><b>Outage</b>: a site does not answer with its gate record.</li>
<li><b>No live check</b>: this page has no record for the service. Its dashboard and alert rules watch it; see <a href="/inside/docs/obs/alerts-and-slos/">Alerts and SLOs</a>.</li>
</ul>
<p class="note">Stages: Investigating, Identified, Monitoring, Resolved. Records: <a href="{REPO}/tree/main/incidents">incidents/*.yml</a>, machine-readable at <a href="/inside/status/incidents.json">incidents.json</a>. How to open, update and close an incident: <a href="/inside/docs/eng/status-page/">Status page</a> in the Engineering docs.</p></section>
</main>
<script type="application/json" id="st-cfg">{json.dumps(cfg)}</script>
<script src="/inside/status/status.js" defer></script>
{foot(f'Inside status · built from <a href="{REPO}/tree/main/incidents">incidents/*.yml</a> and <a href="{REPO}/tree/main/services">services/*.yml</a> by <a href="{REPO}/blob/main/scripts/build_inside.py">build_inside.py</a>')}
<noscript><p style="padding:0 18px">Without JavaScript the service states are not read; the incidents above are static.</p></noscript>
</body>
</html>
'''


def build_status(svcs):
    incidents = load_incidents(svcs)
    out = ROOT / 'inside' / 'status'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(status_page(svcs, incidents), encoding='utf-8')
    data = {'generated': TODAY, 'source': f'{REPO}/tree/main/incidents', 'stages': STAGES, 'incidents': [
        {'id': i['id'], 'title': i['title'], 'services': i['services'], 'impact': i['impact'], 'stage': i['stage'],
         'started': i['started'], 'resolved': i.get('resolved'), 'summary': ' '.join(i['summary'].split()),
         'updates': [{'stage': u['stage'], 'at': str(u['at']), 'text': ' '.join(u['text'].split())} for u in i['updates']],
         'follow_up': ' '.join((i.get('follow_up') or '').split()) or None, 'postmortem': [u for u, _ in i['postmortem_l']]}
        for i in incidents]}
    (out / 'incidents.json').write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'status: {len(incidents)} incidents, {sum(1 for i in incidents if i["stage"] != "resolved")} open')
    return incidents


def main():
    svcs = load_services()
    incidents = build_status(svcs)
    build_services(svcs, status_live=True)
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
    newest_inc = max(str(u['at'])[:10] for i in incidents for u in i['updates'])
    inside_chrome.sitemap_block('status', [('/inside/status/', newest_inc)])
    sec = (f'The status page at {BASE}/inside/status/: the state of each service from the gate records and the deploy feed, and the incident '
           f'history (stages Investigating, Identified, Monitoring, Resolved), written blameless. Machine-readable: {BASE}/inside/status/incidents.json.\n\n')
    for i in incidents:
        sec += f'- [{i["title"]}]({BASE}/inside/status/#{i["id"]}): {i["stage"]}, started {i["started"]}. {" ".join(i["summary"].split())}\n'
    inside_chrome.llms_section('Inside status', sec)
    build_search.main()


if __name__ == '__main__':
    main()
