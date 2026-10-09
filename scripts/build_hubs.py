#!/usr/bin/env python3
"""Build the section and topic hub pages from site/nav.yml and site/topics.yml.

- /research/: the Research section front page, every research page in the order and groups of site/nav.yml,
  with the description each page gives itself (<meta name="description">).
- /topics/<key>/: one hub per topic in site/topics.yml, listing what carries the topic: research, red team and Inside pages
  (the tag map in site/topics.yml), docs pages by label or space (inside/docs/search.json), posts (uncovertechtalent.com
  tag pages on the map and Substack titles, map/graph.json) and board issues (GitHub API; on failure the last list
  in topics/topics.json stays). /topics/ lists the hubs; /topics/topics.json holds the membership, which the
  Topics block in the sidebars reads to mark the topics of the current page.

Each page goes through scripts/site_chrome.py (top bar, breadcrumbs, sidebar, footer) and gets an entry in the
managed sitemap block "hubs" and the llms.txt section "Site sections". Then the chrome of every page is written
again, so the Topics block matches the new membership.

Run from the repo root, after build_docs.py and build_inside.py:  python3 scripts/build_hubs.py
"""
import datetime, html, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inside_chrome, mini_yaml, site_chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://machinebehavior.io'
ICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛋️</text></svg>">'


def esc(s):
    return html.escape(str(s), quote=True)


SITEMAP = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')


def page_meta(url):
    """Description and last change date of a page in this repository."""
    rel = url.lstrip('/') + 'index.html'
    src = (ROOT / rel).read_text(encoding='utf-8')
    m = re.search(r'<meta name="description" content="([^"]*)"', src)
    desc = html.unescape(m.group(1)) if m else ''
    lm = re.search(rf'<loc>{re.escape(BASE + url)}</loc><lastmod>(\d{{4}}-\d{{2}}-\d{{2}})', SITEMAP)
    if lm:  # the date the author gave the page; a site-wide chrome change does not move it
        return desc, lm.group(1)
    out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return desc, out or datetime.date.today().isoformat()


def head(title, desc, url, modified, src):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{url}">
<link rel="stylesheet" href="/style.css">
<meta name="mb-source" content="{esc(src)}">
{ICON}
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{url}">
<meta property="og:site_name" content="Machine Behavior">
<meta property="og:title" content="{esc(title.split(': ')[0])}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE}/map/home-graph.png">
<meta property="article:modified_time" content="{modified}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/map/home-graph.png">
</head>'''


def research():
    t = site_chrome.tree()
    sec = t.section('research')
    url = sec.url
    rows, dates = [], []

    def item(n):
        desc, d = page_meta(n.url)
        dates.append(d)
        return (f'<li class="mb-entry"><a href="{n.url}">{esc(n.title)}</a>'
                f'<p>{esc(desc)}</p><span class="mb-entry-meta">updated {d}</span></li>')

    loose = [k for k in sec.kids if not k.group]
    if loose:
        rows.append('<section><h2 class="label">Registers and logs</h2><ul class="mb-entries">' + ''.join(item(k) for k in loose) + '</ul></section>')
    for g in (k for k in sec.kids if k.group):
        rows.append(f'<section><h2 class="label">{esc(g.title)}</h2><ul class="mb-entries">' + ''.join(item(k) for k in g.kids) + '</ul></section>')
    about = sec.cfg.get('about', '')
    newest = max(dates)
    n = len(dates)
    desc = f'Research on machinebehavior.io: {n} pages. {about}'
    page = f'''{head('Research: Machine Behavior', desc, url, newest, 'scripts/build_hubs.py')}
<body>
<div class="sheet">
  <header>
    <div class="eyebrow">Section · {n} pages · updated {newest}</div>
    <h1>Research</h1>
    <p class="subtitle">{esc(about)}</p>
  </header>
  {''.join(rows)}
  <p class="thesis">The same programme as an internal wiki, with data and rerun steps: <a class="mono" href="/inside/docs/res/">Research docs</a>. Every page and the links between them: <a class="mono" href="/map/">the map</a>.</p>
</div>
</body>
</html>
'''
    rel = url.lstrip('/') + 'index.html'
    (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / rel).write_text(site_chrome.apply(page, rel), encoding='utf-8')
    return [(url, newest, 'Research', f'the Research section front page: {about}')]


# ---------- topics ----------
REPO_API = 'https://api.github.com/repos/uncovertechtalent/machinebehavior.io/issues?state=all&per_page=100'
TOPICS_JSON = ROOT / 'topics' / 'topics.json'
DOCS_SHOW = 10  # docs per space before the rest folds into a disclosure


def lastmod(url):
    lm = re.search(rf'<loc>{re.escape(BASE + url)}</loc><lastmod>(\d{{4}}-\d{{2}}-\d{{2}})', SITEMAP)
    return lm.group(1) if lm else ''


def words_rx(words):
    return re.compile('|'.join(r'\b' + re.escape(w) for w in words), re.I) if words else None


def fetch_issues():
    """Board issues from the GitHub API, or None when it cannot be read."""
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'machinebehavior.io build_hubs'}
    token = os.environ.get('GH_TOKEN') or subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip()
    if token:
        headers['Authorization'] = 'Bearer ' + token
    out, url = [], REPO_API
    try:
        for _ in range(5):
            r = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20)
            out += [i for i in json.load(r) if 'pull_request' not in i]
            nxt = re.search(r'<([^>]+)>;\s*rel="next"', r.headers.get('Link', ''))
            if not nxt:
                break
            url = nxt.group(1)
    except Exception as e:  # noqa: BLE001
        print(f'warning: board issues not read ({e}); the last list in topics/topics.json stays', file=sys.stderr)
        return None
    return [{'n': i['number'], 't': i['title'], 'state': i['state'], 'u': i['html_url'],
             'labels': [l['name'] for l in i['labels']], 'closed': (i.get('closed_at') or '')[:10],
             'reason': i.get('state_reason') or ''} for i in out]


def load_sources():
    docs = json.loads((ROOT / 'inside' / 'docs' / 'search.json').read_text(encoding='utf-8'))
    graph = json.loads((ROOT / 'map' / 'graph.json').read_text(encoding='utf-8'))
    nodes = {n['id']: n for n in graph['nodes']}
    tag_posts = {}
    for l in graph['links']:
        a, b = nodes.get(l['source']), nodes.get(l['target'])
        if a and b and a['kind'] == 'tag' and b['kind'] == 'page' and l['kind'] == 'body' and '/blog/' in b['id']:
            tag_posts.setdefault(a['title'], []).append(b)
    substack = [n for n in graph['nodes'] if n['kind'] == 'substack']
    issues = fetch_issues()
    if issues is None and TOPICS_JSON.exists():
        issues = json.loads(TOPICS_JSON.read_text(encoding='utf-8')).get('issues', [])
    return docs, tag_posts, substack, issues or []


def norm_title(t):
    return re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()[:40]


def members(topic, t, docs, tag_posts, substack, issues):
    m = {'research': [], 'red-team': [], 'inside': [], 'docs': [], 'posts': [], 'tickets': []}
    for u in topic.get('pages') or []:
        node = t.by_url.get(u)
        if node is None:
            raise SystemExit(f'site/topics.yml: {topic["key"]}: {u} is not a page in site/nav.yml')
        m[node.section if node.section in ('research', 'red-team') else 'inside'].append(node)
    labels, spaces = set(topic.get('docs_labels') or []), set(topic.get('docs_spaces') or [])
    for p in docs['pages']:
        if p['s'] in spaces or labels & set(p['l']):
            m['docs'].append(p)
    for lab in labels - {l for p in docs['pages'] for l in p['l']}:
        print(f'warning: site/topics.yml: {topic["key"]}: no docs page carries the label {lab}', file=sys.stderr)
    posts, seen = [], set()
    for tag in topic.get('map_tags') or []:
        if tag not in tag_posts:
            print(f'warning: site/topics.yml: {topic["key"]}: no tag page {tag} on the map', file=sys.stderr)
        for n in tag_posts.get(tag, []):
            if n['id'] not in seen:
                seen.add(n['id']); posts.append({'t': n['title'], 'u': n['id'], 'date': n.get('date', ''), 'site': 'uncovertechtalent.com', 'd': n.get('desc', '')})
    rx = words_rx(topic.get('post_words'))
    by_title = {norm_title(p['t']): p for p in posts}
    for n in substack:
        twin = by_title.get(norm_title(n['title']))
        if twin is not None:
            twin['also'] = n['id']
        elif rx and rx.search(n['title']):
            posts.append({'t': n['title'].strip(), 'u': n['id'], 'date': n.get('date', ''), 'site': 'Substack', 'd': n.get('desc', '')})
    m['posts'] = sorted(posts, key=lambda p: (p['date'], p['t']), reverse=True)
    tl, trx = set(topic.get('ticket_labels') or []), words_rx(topic.get('ticket_words'))
    m['tickets'] = sorted((i for i in issues if tl & set(i['labels']) or (trx and trx.search(i['t']))),
                          key=lambda i: (i['state'] != 'open', -i['n']))
    return m


def topic_page(topic, m, all_topics, spaces):
    t = site_chrome.tree()
    url = f'/topics/{topic["key"]}/'

    def cards(nodes):
        h = ''
        for n in nodes:
            desc, d = page_meta(n.url)
            h += (f'<li class="mb-entry"><a href="{n.url}">{esc(n.title)}</a><p>{esc(desc)}</p>'
                  f'<span class="mb-entry-meta">updated {d}</span></li>')
        return h

    parts = []
    if m['research']:
        parts.append(f'<section><h2 class="label">Research <span class="mb-n">{len(m["research"])}</span></h2><ul class="mb-entries">{cards(m["research"])}</ul></section>')
    if m['red-team']:
        parts.append(f'<section><h2 class="label">Red team <span class="mb-n">{len(m["red-team"])}</span></h2><ul class="mb-entries">{cards(m["red-team"])}</ul></section>')
    if m['inside']:
        parts.append(f'<section><h2 class="label">Inside <span class="mb-n">{len(m["inside"])}</span></h2><ul class="mb-entries">{cards(m["inside"])}</ul></section>')
    if m['docs']:
        h = f'<section><h2 class="label">Docs <span class="mb-n">{len(m["docs"])}</span></h2>'
        for key, sp in spaces.items():
            ps = sorted((p for p in m['docs'] if p['s'] == key), key=lambda p: (p['u'] != f'/inside/docs/{key}/', p['t'].lower()))
            if not ps:
                continue
            li = lambda p: f'<li><a href="{p["u"]}">{esc(p["t"])}</a><span>{esc(p["d"])}</span></li>'
            h += f'<h3 class="mb-group">{esc(sp["name"])} <span class="mb-n">{len(ps)}</span></h3><ul class="mb-links">' + ''.join(li(p) for p in ps[:DOCS_SHOW]) + '</ul>'
            if len(ps) > DOCS_SHOW:
                h += (f'<details class="mb-more"><summary>All {len(ps)} pages in {esc(sp["name"])}</summary><ul class="mb-links">'
                      + ''.join(li(p) for p in ps[DOCS_SHOW:]) + '</ul></details>')
        parts.append(h + '</section>')
    if m['posts']:
        li = ''
        for p in m['posts']:
            also = f' · <a href="{esc(p["also"])}">also on Substack</a>' if p.get('also') else ''
            li += (f'<li><a href="{esc(p["u"])}">{esc(p["t"])}</a><span>{esc(p["d"])}</span>'
                   f'<span class="mb-links-meta">{esc(p["date"])} · {esc(p["site"])}{also}</span></li>')
        parts.append(f'<section><h2 class="label">Posts <span class="mb-n">{len(m["posts"])}</span></h2><ul class="mb-links">{li}</ul></section>')
    if m['tickets']:
        li = ''
        for i in m['tickets']:
            meta = ' · '.join([i['state']] + [l for l in i['labels'] if l.startswith(('P', 'area: ', 'status: '))])
            li += f'<li><a href="{esc(i["u"])}">#{i["n"]} {esc(i["t"])}</a><span class="mb-links-meta">{esc(meta)}</span></li>'
        parts.append(f'<section><h2 class="label">Tickets <span class="mb-n">{len(m["tickets"])}</span></h2>'
                     f'<p class="thesis">Issues on the <a class="mono" href="/inside/board/">board</a>, open first, as of the last build.</p><ul class="mb-links">{li}</ul></section>')
    others = ''.join(f'<li><a href="/topics/{o["key"]}/">{esc(o["title"])}</a></li>' for o in all_topics if o['key'] != topic['key'])
    parts.append(f'<section><h2 class="label">Other topics</h2><ul class="mb-links mb-links-inline">{others}</ul></section>')
    dates = [lastmod(n.url) for n in m['research'] + m['red-team'] + m['inside']] + [lastmod(p['u']) for p in m['docs']] + [p['date'] for p in m['posts']]
    newest = max(d for d in dates if d) if any(dates) else datetime.date.today().isoformat()
    total = sum(len(v) for v in m.values())
    names = (('research', 'research page'), ('red-team', 'red team page'), ('inside', 'Inside page'), ('docs', 'docs page'), ('posts', 'post'), ('tickets', 'ticket'))
    counts = ', '.join(f'{len(m[k])} {name}{"" if len(m[k]) == 1 else "s"}' for k, name in names if m[k])
    desc = f'Topic hub: {topic["title"]}. {topic["about"]} {counts}.'
    page = f'''{head(f'{topic["title"]}: Machine Behavior', desc, url, newest, 'site/topics.yml')}
<body>
<div class="sheet">
  <header>
    <div class="eyebrow">Topic · {total} entries · updated {newest}</div>
    <h1>{esc(topic["title"])}</h1>
    <p class="subtitle">{esc(topic["about"])}</p>
    <p class="mb-counts">{esc(counts)}</p>
  </header>
  {''.join(parts)}
  <p class="page-note">Built by <a href="https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/build_hubs.py">build_hubs.py</a> from <a href="https://github.com/uncovertechtalent/machinebehavior.io/blob/main/site/topics.yml">site/topics.yml</a>, the docs labels, the tag pages on the <a href="/map/">map</a> and the board. Machine-readable: <a href="/topics/topics.json">topics.json</a>.</p>
</div>
</body>
</html>
'''
    rel = url.lstrip('/') + 'index.html'
    (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / rel).write_text(site_chrome.apply(page, rel), encoding='utf-8')
    return url, newest, total, counts


def topics():
    cfg = mini_yaml.load_file(ROOT / 'site' / 'topics.yml')['topics']
    docs, tag_posts, substack, issues = load_sources()
    spaces = docs['spaces']
    t = site_chrome.tree()
    data, entries, rows = [], [], ''
    for topic in cfg:
        m = members(topic, t, docs, tag_posts, substack, issues)
        data.append({'key': topic['key'], 'title': topic['title'], 'url': f'/topics/{topic["key"]}/', 'about': topic['about'],
                     'pages': [n.url for n in m['research'] + m['red-team'] + m['inside']] + [p['u'] for p in m['docs']],
                     'posts': [{'t': p['t'], 'u': p['u'], 'also': p.get('also'), 'date': p['date']} for p in m['posts']],
                     'tickets': [i['n'] for i in m['tickets']]})
    TOPICS_JSON.parent.mkdir(exist_ok=True)
    TOPICS_JSON.write_text(json.dumps({'generated': datetime.date.today().isoformat(), 'source': 'site/topics.yml', 'topics': data, 'issues': issues},
                                      ensure_ascii=False, indent=1), encoding='utf-8')
    site_chrome.reload_topics()
    for topic in cfg:
        m = members(topic, t, docs, tag_posts, substack, issues)
        url, newest, total, counts = topic_page(topic, m, cfg, spaces)
        entries.append((url, newest, topic['title'], f'topic hub, {counts}. {topic["about"]}'))
        rows += (f'<li class="mb-entry"><a href="{url}">{esc(topic["title"])}</a><p>{esc(topic["about"])}</p>'
                 f'<span class="mb-entry-meta">{esc(counts)} · updated {newest}</span></li>')
    newest = max(e[1] for e in entries)
    desc = f'Topics on machinebehavior.io: {len(cfg)} hubs, each listing the research pages, Inside pages, docs, posts and tickets on one subject.'
    page = f'''{head('Topics: Machine Behavior', desc, '/topics/', newest, 'site/topics.yml')}
<body>
<div class="sheet">
  <header>
    <div class="eyebrow">Section · {len(cfg)} topics · updated {newest}</div>
    <h1>Topics</h1>
    <p class="subtitle">Each topic gathers what the site and its posts say about one subject, across research pages, Inside, the docs, posts and the board.</p>
  </header>
  <section><ul class="mb-entries">{rows}</ul></section>
  <p class="page-note">Built by <a href="https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/build_hubs.py">build_hubs.py</a> from <a href="https://github.com/uncovertechtalent/machinebehavior.io/blob/main/site/topics.yml">site/topics.yml</a>. Machine-readable: <a href="/topics/topics.json">topics.json</a>.</p>
</div>
</body>
</html>
'''
    (ROOT / 'topics' / 'index.html').write_text(site_chrome.apply(page, 'topics/index.html'), encoding='utf-8')
    return [('/topics/', newest, 'Topics', desc)] + entries


def main():
    entries = research() + topics()
    import build_fallbacks  # static text for the pages that fill their lists in the browser
    build_fallbacks.main(json.loads(TOPICS_JSON.read_text(encoding='utf-8')).get('issues', []))
    inside_chrome.sitemap_block('hubs', [(u, d) for u, d, _, _ in entries], source='scripts/build_hubs.py')
    inside_chrome.llms_section('Site sections', '\n'.join(f'- [{t}]({BASE}{u}): {d}' for u, _, t, d in entries))
    print(f'hubs: {len(entries)} pages')
    site_chrome.tree(reload=True)
    return site_chrome.main([])  # the Topics block on every page follows the new membership


if __name__ == '__main__':
    sys.exit(main())
