#!/usr/bin/env python3
"""Build the section and topic hub pages from site/nav.yml and site/topics.yml.

- /research/: the Research section front page, a contents list of every research page in the order and groups of
  site/nav.yml: each group's label links to its index page, each page is a line with its publication date (ADR-0048).
- /research/case-files/ and the other `hub: true` pages: a group's index, the same list of every page it holds
  (ADR-0045, ADR-0048).
- /topics/<key>/: one hub per topic in site/topics.yml, listing what carries the topic: research, red team and Inside pages
  (the tag map in site/topics.yml), docs pages by label or space (inside/docs/search.json), posts (uncovertechtalent.com
  tag pages on the map and Substack titles, map/graph.json; a post with a Substack copy links that canonical copy and names
  the blog copy, #192) and board issues (GitHub API; on failure the last list
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

# The programme's premise, moved here from the front page (ADR-0041)
RESEARCH_INTRO = ('Language models were trained to predict human text and then trained to please human raters, so the vocabulary '
                  'psychology built for humans describes them with uncomfortable precision. The approval training produces a '
                  '<strong>fawn response</strong>. Suppressing it produces <strong>symptom substitution</strong>. And the case '
                  'history is readable, because the formative corpus, the socialization stage, and the assigned persona are all '
                  'inspectable layers. Model behavior is what the model does; machine behavior is what the whole assembly does, '
                  'model plus harness, and the assembly is where the findings live.')


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


def is_hub(n):
    """A page that lists its pages, written here (`hub: true` in site/nav.yml, ADR-0045)."""
    return site_chrome._cfg(n).get('hub') is True


def toc_row(url, title, when='', out=False, note=''):
    """One line of a contents list (ADR-0048): the title, a leader and `when` (a date) at the end of the line when there is
    one, then a `note` under the title when there is one (the site a piece lives on; HTML allowed). `out` marks a piece
    that lives on another site."""
    cls = ' class="toc-out"' if out else ''
    tail = f'<span class="toc-fill"></span><span class="toc-when">{when}</span>' if when else ''
    note = f'<span class="toc-note">{note}</span>' if note else ''
    return f'<li{cls}><a href="{esc(url)}">{esc(title)}</a>{tail}{note}</li>'


def _section_problem(s, page):
    """Why a `sections` entry of `page` in site/nav.yml cannot be a line on the research index, or None (ADR-0048)."""
    if not isinstance(s, dict) or not s.get('title'):
        return 'it needs a title'
    url = str(s.get('url', ''))
    if not url.startswith(page.url + '#') or len(url) == len(page.url) + 1:
        return f"its url must be {page.url} with the heading's anchor"
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(s.get('published', ''))):
        return 'it needs a published date, YYYY-MM-DD'
    anchor = url.split('#', 1)[1]
    src = (ROOT / (page.url.lstrip('/') + 'index.html')).read_text(encoding='utf-8')
    if f'id="{anchor}"' not in src:
        return f'the page has no element with id {anchor!r}'
    return None


NOTE_OUT = ('<p class="mb-entries-note">Lines marked ↗ live on another site, named after the title; '
            'the others are pages of this site.</p>')


def lines(index, pages):
    """The lines of a contents list as (date, html): `pages` under `index` (a page or section node, or None), each with its
    publication date when it gives one; then the index's `sections` (parts of its own page: title, the page's URL with the
    heading's anchor, published) and the pieces it lists `elsewhere` (ADR-0046), marked with the site they live on and any
    copy. With `order: newest` on the index the whole list runs newest first, this site's pages first on a tie, then the
    sections, then the pieces elsewhere; otherwise the written order, sections and pieces elsewhere after the pages (ADR-0048)."""
    rows = []
    for k in pages:
        pub = site_chrome._cfg(k).get('published', '')
        rows.append((pub or page_meta(k.url)[1], toc_row(k.url, k.title, pub)))
    cfg = site_chrome._cfg(index) if index is not None else {}
    for s in cfg.get('sections') or []:
        bad = _section_problem(s, index)
        if bad:
            raise SystemExit(f'site/nav.yml: the section {s.get("title")!r} of {index.title!r}: {bad}')
        rows.append((s['published'], toc_row(s['url'], s['title'], s['published'])))
    for e in cfg.get('elsewhere') or []:  # Tree allows it only on a hub with order newest, and checks every entry
        also = (f', also on <a href="{esc(e["also"])}">{esc(site_chrome.home_of(e["also"]))}</a>' if e.get('also') else '')
        rows.append((e['published'], toc_row(e['url'], e['title'], e['published'], out=True,
                                             note=f'on {esc(site_chrome.home_of(e["url"]))}{also}')))
    if cfg.get('order') == 'newest':
        rows.sort(key=lambda r: r[0], reverse=True)  # stable, so a tie keeps the order above
    return rows


def research_groups(t):
    """The research index's groups as (heading, index, pages), in the order of the sidebar (ADR-0044): the group's index
    page (its one page, or an included section's overview; None for pages outside any group) and the pages under it at
    any depth, in the order of site_chrome.ordered(). The index itself, written or generated, and sidebar-only links stay
    out of the pages: the index is the group's label (ADR-0045, ADR-0048)."""
    sec = t.section('research')

    def down(kids):
        return [p for k in kids if not k.link for p in ([] if is_hub(k) else [k]) + down(site_chrome.ordered(k))]

    out = []
    loose = [k for k in sec.kids if not k.group and not k.link]
    if loose:
        out.append(('Registers and logs', None, loose))
    for g in (k for k in sec.kids if k.group):
        inc = t.section(g.cfg_page['include']) if g.cfg_page.get('include') else None
        index = inc or next(k for k in g.kids if not k.link)  # a group holds one page, its index (ADR-0045)
        out.append((g.title, index.url, down(site_chrome.ordered(index))))
    return out


def hubs():
    """One page per `hub: true` entry under /research/ (ADR-0045): the group's name, its `about` as the subtitle, and every
    page it holds as a contents list in the order of site_chrome.ordered(), sidebar-only links included, each a title with
    its publication date when it gives one (ADR-0048). Pieces listed `elsewhere` join the list by date, after this site's
    pages of the same day, each marked with the site it lives on and any copy (ADR-0046). The sidebar's All link points here."""
    t = site_chrome.tree()
    out = []
    for n in site_chrome._all_under(t.section('research')):
        if not is_hub(n):
            continue
        about = n.cfg_page['about']  # Tree checks that a hub page has about and pages
        pages = site_chrome.ordered(n)
        rows = lines(n, pages)
        outside = n.cfg_page.get('elsewhere') or []
        note = NOTE_OUT if outside else ''
        newest = max([page_meta(k.url)[1] for k in pages] + [e['published'] for e in outside])  # a new piece elsewhere changes the page too
        desc = f'{n.title} in the research on machinebehavior.io. {about}'
        page = f'''{head(f'{n.title}: Research: Machine Behavior', desc, n.url, newest, 'scripts/build_hubs.py')}
<body>
<div class="sheet">
  <header>
    <h1>{esc(n.title)}</h1>
    <p class="subtitle">{esc(about)}</p>
  </header>
  {note}<ol class="toc" role="list">{''.join(r for _, r in rows)}</ol>
</div>
</body>
</html>
'''
        rel = n.url.lstrip('/') + 'index.html'
        (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / rel).write_text(site_chrome.apply(page, rel), encoding='utf-8')
        out.append((n.url, newest, f'Research: {n.title}', about))
    return out


def research():
    t = site_chrome.tree()
    sec = t.section('research')
    url = sec.url
    blocks, dates, n, outside = [], [], 0, False
    for heading, index, nodes in research_groups(t):
        idx = t.by_url.get(index) if index else None
        counted = ([idx] if idx and not is_hub(idx) else []) + nodes
        n += len(counted)
        dates += [page_meta(k.url)[1] for k in counted]  # the page's last change: the index changes with its pages
        cfg = site_chrome._cfg(idx) if idx else {}
        dates += [x['published'] for x in (cfg.get('sections') or []) + (cfg.get('elsewhere') or [])]  # and with a new line
        if cfg.get('elsewhere'):
            outside = True
        label = f'<a href="{index}">{esc(heading)}</a>' if index else esc(heading)
        blocks.append(f'<div class="toc-group"><h2 class="label">{label}</h2><ol class="toc" role="list">'
                      + ''.join(r for _, r in lines(idx, nodes)) + '</ol></div>')
    if outside:
        blocks.append(NOTE_OUT)
    about = sec.cfg.get('about', '')
    newest = max(dates)
    desc = f'Research on machinebehavior.io: {n} pages. {about}'
    page = f'''{head('Research: Machine Behavior', desc, url, newest, 'scripts/build_hubs.py')}
<body>
<div class="sheet">
  <header>
    <h1>Research</h1>
    <p class="subtitle">{esc(about)}</p>
  </header>
  <p class="thesis">{RESEARCH_INTRO}</p>
  {''.join(blocks)}
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
                seen.add(n['id']); posts.append({'t': n['title'], 'u': n['id'], 'date': n.get('date', ''), 'site': site_chrome.home_of(n['id']) or 'uncovertechtalent.com', 'd': n.get('desc', '')})
    rx = words_rx(topic.get('post_words'))
    by_title = {norm_title(p['t']): p for p in posts}
    for n in substack:
        twin = by_title.get(norm_title(n['title']))
        if twin is not None and not twin.get('also'):  # the blog copy names the Substack copy canonical (ADR-0046), so it leads; once
            twin.update(u=n['id'], site=site_chrome.home_of(n['id']) or 'Substack', also=twin['u'], also_site=twin['site'])
        elif twin is not None:
            print(f'warning: site/topics.yml: {topic["key"]}: a second Substack post matches {twin["t"]!r} ({n["id"]}); the hub keeps {twin["u"]}', file=sys.stderr)
            continue
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
            also = f' · <a href="{esc(p["also"])}">also on {esc(p["also_site"])}</a>' if p.get('also') else ''
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
                     'posts': [{'t': p['t'], 'u': p['u'], 'site': p['site'], 'also': p.get('also'), 'date': p['date']} for p in m['posts']],
                     'tickets': [i['n'] for i in m['tickets']]})
    TOPICS_JSON.parent.mkdir(exist_ok=True)
    TOPICS_JSON.write_text(json.dumps({'generated': datetime.date.today().isoformat(), 'source': 'site/topics.yml', 'topics': data, 'issues': issues},
                                      ensure_ascii=False, indent=1), encoding='utf-8')
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
    entries = research() + hubs() + topics()
    import build_fallbacks  # static text for the pages that fill their lists in the browser
    build_fallbacks.main(json.loads(TOPICS_JSON.read_text(encoding='utf-8')).get('issues', []))
    inside_chrome.sitemap_block('hubs', [(u, d) for u, d, _, _ in entries], source='scripts/build_hubs.py')
    inside_chrome.llms_section('Site sections', '\n'.join(f'- [{t}]({BASE}{u}): {d}' for u, _, t, d in entries))
    print(f'hubs: {len(entries)} pages')
    site_chrome.tree(reload=True)
    return site_chrome.main([])  # the Topics block on every page follows the new membership


if __name__ == '__main__':
    sys.exit(main())
