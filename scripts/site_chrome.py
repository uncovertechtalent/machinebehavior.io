#!/usr/bin/env python3
"""The chrome of every page on machinebehavior.io, from one navigation source: site/nav.yml.

One function, apply(html, rel), writes the managed blocks of a page:

    <!-- mb:head -->    stylesheets of the design system and the JSON-LD BreadcrumbList, before </head>
    <!-- mb:bar -->     skip link, the top bar (brand, sections, search) and, on Inside and Docs app pages, the demo banner
    <!-- mb:crumbs -->  the visible breadcrumbs
    <!-- mb:side -->    the section sidebar (sections listed in SIDEBARS)
    <!-- mb:foot -->    the footer: conformity line, page source and history, report an issue, legal links

Each block sits between <!-- mb:NAME --> and <!-- /mb:NAME -->. A page that has the markers keeps them where they are;
a page without them gets them at fixed anchors (after <body>, at the top of <div class="sheet"> or <main>, before
</body>). Everything outside the markers is page content and stays as written, except the old chrome this replaces
(the research menu <nav class="nav">, the Inside bar and banner, the old conformity line), which apply() removes.

Generators (build_docs.py, build_inside.py, slips_page.py, build_hubs.py) call apply() before they write a page. This
script, run on its own, applies the chrome to every page in the repository, so pages written by generators outside
this repository (the gate's /conformity/, the definition at /continuous-conformity/) get it too; the deploy job runs
it again before the upload.

    python3 scripts/site_chrome.py           write every page, then print the report
    python3 scripts/site_chrome.py --check   write nothing; exit 1 when a page differs, a page is outside the tree,
                                             or a page in the tree is missing from sitemap.xml
    python3 scripts/site_chrome.py --deploy  the deploy job: also write /conformity/, which the gate rewrites on every run
Stdlib only.
"""
import html, json, re, sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mini_yaml  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NAV_FILE = ROOT / 'site' / 'nav.yml'

SIDEBARS = {'research', 'inside', 'topics'}  # sections whose pages carry the section sidebar
TOPICS_FILE = ROOT / 'site' / 'topics.yml'
TOPICS_JSON = ROOT / 'topics' / 'topics.json'  # membership, written by scripts/build_hubs.py
SKIP_DIRS = ('.', 'scripts/', 'bench/', 'predictions/', 'node_modules/', 'vendor/', 'fonts/', 'site/', 'design/')
NOT_FOUND = '404.html'     # not in the tree: bar, crumbs (Home, Not found) and footer only
DEPLOY_ONLY = {'conformity/index.html'}  # rewritten by the gate on every run; the deploy job applies the chrome before upload

BLOCK_RE = re.compile(r'<!-- mb:(\w+) -->.*?<!-- /mb:\1 -->', re.S)
LEGACY = [
    re.compile(r'[ \t]*<!-- inside-bar:begin[^>]*-->.*?<!-- inside-bar:end -->\n?', re.S),
    re.compile(r'[ \t]*<!-- inside-banner:begin -->.*?<!-- inside-banner:end -->\n?', re.S),
    re.compile(r'[ \t]*<header class="ib">.*?</header>\n?', re.S),
    re.compile(r'[ \t]*<aside class="ib-demo".*?</aside>\n?', re.S),
    re.compile(r'[ \t]*<nav class="nav">.*?</nav>\n?', re.S),
    re.compile(r'[ \t]*<nav class="crumbs" aria-label="Breadcrumb">.*?</nav>\n?', re.S),
    re.compile(r'[ \t]*<p class="conf mono" data-conformity>.*?</p>\n?', re.S),
    re.compile(r'[ \t]*<script src="/conformity/footer\.js" defer></script>\n?'),
    re.compile(r'[ \t]*<script src="/inside/bar\.js" defer></script>\n?'),
    re.compile(r'[ \t]*<link rel="stylesheet" href="/inside/bar\.css">\n?'),
]


def esc(s):
    return html.escape(str(s), quote=True)


# ---------- the tree ----------
class Node:
    def __init__(self, title, url=None, section=None, parent=None, group=False):
        self.title, self.url, self.section, self.parent, self.group = title, url, section, parent, group
        self.kids = []

    def add(self, node):
        node.parent = self
        self.kids.append(node)
        return node


class Tree:
    """site/nav.yml plus the pages the builds add (docs, services), indexed by URL."""

    def __init__(self):
        cfg = mini_yaml.load_file(NAV_FILE)
        self.site = cfg['site']
        self.base = self.site['base'].rstrip('/')
        self.repo = self.site['repo'].rstrip('/')
        self.legal = cfg.get('legal') or []
        self.sections, self.by_url = [], {}
        self.home = None
        for s in cfg['sections']:
            node = Node(s['title'], s['url'], s['key'])
            node.cfg = s
            if s['key'] == 'home':
                self.home = node
            self.sections.append(node)
            self._index(node)
            self._pages(node, s.get('pages') or [], s['key'])
            if s.get('auto'):
                self._auto(node, s['auto'])
        if self.home is None:
            raise SystemExit('site/nav.yml: no section with key home')
        sm = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
        self.lastmod = {u[len(self.base):]: d for u, d in re.findall(r'<loc>([^<]+)</loc><lastmod>(\d{4}-\d{2}-\d{2})', sm)}

    def _index(self, node):
        if node.url and node.url not in self.by_url:
            self.by_url[node.url] = node

    def _pages(self, parent, items, section):
        for it in items:
            if 'group' in it:
                g = parent.add(Node(it['group'], None, section, group=True))
                self._pages(g, it.get('pages') or [], section)
                continue
            node = parent.add(Node(it['title'], it['url'], section))
            node.cfg_page = it
            self._index(node)
            self._pages(node, it.get('pages') or [], section)
            if it.get('auto'):
                self._auto(node, it['auto'])

    def _auto(self, node, kind):
        if kind == 'docs':
            f = ROOT / 'inside' / 'docs' / 'tree.json'
            if not f.exists():
                return
            pages = json.loads(f.read_text(encoding='utf-8'))['pages']
            made = {node.url: node}
            for p in pages:  # parents come before their children in tree.json
                if p['u'] == node.url:
                    continue
                par = made.get(p.get('p') or node.url, node)
                made[p['u']] = par.add(Node(p['t'], p['u'], node.section))
                self._index(made[p['u']])
        elif kind == 'topics':
            for tp in mini_yaml.load_file(TOPICS_FILE)['topics']:
                self._index(node.add(Node(tp['title'], f'/topics/{tp["key"]}/', node.section)))
        elif kind == 'services':
            f = ROOT / 'inside' / 'services' / 'services.json'
            if not f.exists():
                return
            for s in json.loads(f.read_text(encoding='utf-8'))['services']:
                self._index(node.add(Node(s['name'], s['url'], node.section)))
        else:
            raise SystemExit(f'site/nav.yml: unknown auto source {kind!r}')

    def section(self, key):
        return next((s for s in self.sections if s.section == key), None)

    def trail(self, node):
        """Home first, the page last; groups have no page and stay out."""
        out = []
        while node is not None:
            if not node.group and node.url:
                out.append(node)
            node = node.parent
        out.reverse()
        if not out or out[0] is not self.home:
            out.insert(0, self.home)
        return out

    def page_urls(self):
        return [u for u in self.by_url if '#' not in u]


_TREE = None


def tree(reload=False):
    global _TREE
    if _TREE is None or reload:
        _TREE = Tree()
    return _TREE


def url_of(rel):
    rel = rel.replace('\\', '/')
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel


# ---------- the blocks ----------
def bar(t, node, layout):
    sec = node.section if node else None
    links = []
    for s in t.sections:
        if s.section == 'home':
            continue
        cur = ''
        if node is s:
            cur = ' aria-current="page"'
        elif sec == s.section:
            cur = ' aria-current="true"'
        links.append(f'<a href="{s.url}"{cur}>{esc(s.title)}</a>')
    home_cur = ' aria-current="page"' if node is t.home else ''
    out = ('<a class="mb-skip" href="#main">Skip to content</a>'
           '<header class="mb-bar">'
           f'<a class="mb-brand" href="/"{home_cur}><span class="mb-mark" aria-hidden="true">🛋️</span><span class="mb-name">{esc(t.site["name"])}</span></a>'
           '<nav class="mb-nav" aria-label="Sections">' + ''.join(links) + '</nav>'
           f'<form class="mb-search" role="search" action="{t.site["search"]}" method="get">'
           '<label class="mb-sr" for="ib-q">Search the site</label>'
           '<input type="search" id="ib-q" name="q" placeholder="Search pages, docs, services" autocomplete="off" '
           'aria-controls="ib-hits" aria-describedby="ib-help">'
           '<span class="mb-sr" id="ib-help">Enter opens the results page. Arrow down moves into the suggestions.</span>'
           '<kbd class="mb-key" aria-hidden="true">/</kbd>'
           '<ul id="ib-hits" class="ib-hits" aria-label="Suggestions"></ul></form></header>')
    s = t.section(sec) if sec else None
    if s is not None and s.cfg.get('banner') and layout == 'app' and node is not None and node.url != '/map/':
        out += banner()
    return out


def banner():
    """The public-demo marker on Inside and Docs app pages: open to read here; in production behind single sign-on."""
    return ('<aside class="mb-demo" aria-label="About this intranet"><span class="mb-demo-tag">Public demo</span>'
            '<span>This intranet is open to read. In production it sits behind single sign-on, with internal and restricted spaces '
            'granted per person and device.</span><a href="/inside/docs/eng/access-model/">Access model</a>'
            '<a href="/inside/tour/">Five-minute tour</a></aside>')


def page_meta(t, url):
    """Owner and last update of a hand-written page (the sitemap date the author set), shown beside the breadcrumbs."""
    d = t.lastmod.get(url)
    return (f'<p class="mb-page-meta"><span>Owner {esc(t.site["owner"])}</span>'
            + (f'<span>Updated {d}</span>' if d else '') + '</p>')  # no <time>: the map crawler reads the first <time> as the publish date


def crumbs(trail, meta=''):
    items = []
    for i, n in enumerate(trail):
        cur = ' aria-current="page"' if i == len(trail) - 1 else ''
        items.append(f'<li><a href="{n.url}"{cur}>{esc(n.title)}</a></li>')
    nav = '<nav class="mb-crumbs" aria-label="Breadcrumb"><ol>' + ''.join(items) + '</ol></nav>'
    return f'<div class="mb-crumbbar">{nav}{meta}</div>' if meta else nav


def crumbs_ld(t, trail):
    data = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', '@id': t.base + trail[-1].url + '#breadcrumb', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n.title, 'item': t.base + n.url} for i, n in enumerate(trail)]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'


_MEMBERS = None


def reload_topics():
    global _MEMBERS
    _MEMBERS = None


def topic_members():
    """{topic url: set of page urls}, from topics/topics.json; empty before the first build of the hubs."""
    global _MEMBERS
    if _MEMBERS is None:
        _MEMBERS = {}
        if TOPICS_JSON.exists():
            for tp in json.loads(TOPICS_JSON.read_text(encoding='utf-8'))['topics']:
                _MEMBERS[tp['url']] = set(tp['pages'])
    return _MEMBERS


def topics_block(t, url):
    """The Topics block of a sidebar: every topic hub; a mark on each topic that lists the current page."""
    sec = t.section('topics')
    if sec is None or not sec.kids:
        return ''
    mem = topic_members()
    li = ''
    for k in sec.kids:
        if url in mem.get(k.url, ()):
            li += f'<li><a class="mb-topic-in" href="{k.url}">{esc(k.title)}<span class="mb-sr"> (lists this page)</span></a></li>'
        else:
            li += f'<li><a href="{k.url}">{esc(k.title)}</a></li>'
    return (f'<div class="mb-topics"><a class="mb-side-label" href="{sec.url}">Topics</a>'
            f'<ul>{li}</ul></div>')


def side(t, node):
    """The section sidebar: every page of the section, the current one marked; groups as headings, a page with
    children as a disclosure that is open when the current page is inside it. Open by default; /inside/bar.js
    closes it on narrow screens, where it sits above the content."""
    if node is None or node.section not in SIDEBARS:
        return ''
    sec = t.section(node.section)
    here = {id(n) for n in t.trail(node)}

    def link(n):
        cur = ' aria-current="page"' if n is node else ''
        return f'<a href="{n.url}"{cur}>{esc(n.title)}</a>'

    def items(kids):
        h = ''
        for k in kids:
            if k.group:
                h += f'<li class="mb-side-group"><span class="mb-side-label">{esc(k.title)}</span><ul>{items(k.kids)}</ul></li>'
            elif k.kids:
                op = ' open' if id(k) in here else ''
                h += f'<li><details{op}><summary>{link(k)}</summary><ul>{items(k.kids)}</ul></details></li>'
            else:
                h += f'<li>{link(k)}</li>'
        return h

    count = sum(1 for _ in _pages_under(sec))
    head_cur = ' aria-current="page"' if node is sec else ''
    topics = topics_block(t, node.url) if node.section != 'topics' else ''
    return (f'<nav class="mb-side" aria-label="{esc(sec.title)} pages"><details class="mb-side-wrap" open>'
            f'<summary><span>{esc(sec.title)}</span><span class="mb-side-n">{count} pages</span></summary>'
            f'<a class="mb-side-head" href="{sec.url}"{head_cur}>{esc(sec.title)}</a>'
            f'<ul class="mb-side-tree">{items(sec.kids)}</ul>{topics}</details></nav>')


def _pages_under(n):
    for k in n.kids:
        if k.url and '#' not in k.url:
            yield k
        yield from _pages_under(k)


def foot(t, url, src, title):
    issue = t.repo + '/issues/new?title=' + quote(f'Page {url}: ', safe='')
    legal = ''
    if t.legal:
        legal = '<nav class="mb-foot-legal" aria-label="Legal">' + ''.join(f'<a href="{esc(l["url"])}">{esc(l["title"])}</a>' for l in t.legal) + '</nav>'
    return ('<footer class="mb-foot"><div class="mb-foot-in">'
            f'<p class="mb-foot-site"><a href="/"><span aria-hidden="true">🛋️</span> {esc(t.site["name"])}</a> · {esc(t.site["owner"])}</p>'
            '<p class="mb-foot-conf"><span class="conf mono" data-conformity>conformity: <a class="mono" href="/conformity/">latest run</a></span>'
            ' · self-assessment, not a certification</p>'
            '<nav class="mb-foot-links" aria-label="This page">'
            f'<a href="{t.repo}/blob/main/{esc(src)}">Page source</a>'
            f'<a href="{t.repo}/commits/main/{esc(src)}">History</a>'
            f'<a href="{esc(issue)}">Report an issue</a></nav>'
            f'{legal}</div></footer>'
            '<script src="/conformity/footer.js" defer></script><script src="/inside/bar.js" defer></script>')


# ---------- structured data (ADR-0027) ----------
META_RE = re.compile(r'<meta (?:property|name)="([^"]+)" content="([^"]*)"')


def _metas(src):
    out = {}
    for k, v in META_RE.findall(src):
        out.setdefault(k, []).append(html.unescape(v))
    return out


def _text(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fragment))).strip()


def defined_terms(url, src, set_id):
    """The defined terms a page already shows, as DefinedTerm nodes with the page's own wording.
    /terms/: each <dt> and its <dd> (the receipt line left out). /continuous-conformity/: the entries of clause 3."""
    terms = []
    if url == '/terms/':
        for name, dd in re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', src, re.S):
            dd = re.sub(r'<div class="receipt">.*?</div>', '', dd, flags=re.S)
            terms.append((_text(name), _text(dd), re.sub(r'[^a-z0-9]+', '-', _text(name).lower()).strip('-')))
    elif url == '/continuous-conformity/':
        m = re.search(r'<h2 id="3-terms-and-definitions">.*?(?=<h2 )', src, re.S)
        for code, name, rest in re.findall(r'<p class="thesis"><strong>(3\.\d+) ([^<]+)</strong>(.*?)</p>', m.group(0) if m else '', re.S):
            terms.append((_text(name), _text(rest), code))
    return [{'@type': 'DefinedTerm', '@id': f'{set_id}-{code}', 'name': name, 'description': desc, 'termCode': code,
             'inDefinedTermSet': {'@id': set_id}} for name, desc, code in terms if name and desc]


def page_ld(t, node, trail, url, src, layout):
    """One JSON-LD graph per page: the author (Person), the site (WebSite with its search), and the page itself
    (Article, TechArticle, CollectionPage or WebPage) with its dates, author and breadcrumb; DefinedTermSet where the
    page holds definitions. Every value comes from site/nav.yml or from the page's own metadata and text."""
    base, p = t.base, t.site['person']
    person_id, site_id = base + '/#stefan', base + '/#website'
    person = {'@type': 'Person', '@id': person_id, 'name': p['name'], 'url': base + '/', 'sameAs': p['same_as']}
    if p.get('job_title'):
        person['jobTitle'] = p['job_title']
    website = {'@type': 'WebSite', '@id': site_id, 'name': t.site['name'], 'url': base + '/', 'inLanguage': 'en',
               'author': {'@id': person_id}, 'publisher': {'@id': person_id},
               'potentialAction': {'@type': 'SearchAction', 'target': {'@type': 'EntryPoint', 'urlTemplate': base + t.site['search'] + '?q={search_term_string}'},
                                   'query-input': 'required name=search_term_string'}}
    m = _metas(src)
    cfg = getattr(node, 'cfg_page', None) or {}
    title = (m.get('og:title') or [None])[0] or (TITLE_RE.search(src).group(1) if TITLE_RE.search(src) else trail[-1].title)
    title = re.sub(r'\s*(:|·)\s*(Machine Behavior|Inside docs)$', '', html.unescape(title)).strip()
    section = node.section if node else None
    hub = url in ('/research/', '/topics/', '/inside/docs/') or url.startswith('/topics/')
    kind = 'CollectionPage' if hub else 'TechArticle' if section == 'docs' else 'Article' if section == 'research' else 'WebPage'
    page = {'@type': kind, '@id': base + url + '#page', 'url': base + url, 'name': title, 'inLanguage': 'en',
            'isPartOf': {'@id': site_id}, 'breadcrumb': {'@id': base + url + '#breadcrumb'},
            'author': {'@id': person_id}, 'publisher': {'@id': person_id}}
    if kind in ('Article', 'TechArticle'):
        page['headline'] = title[:110]
    desc = (m.get('description') or m.get('og:description') or [''])[0]
    if desc:
        page['description'] = desc
    published = str(cfg.get('published') or (m.get('article:published_time') or [''])[0])
    modified = (m.get('article:modified_time') or [''])[0] or t.lastmod.get(url, '')
    if published:
        page['datePublished'] = published
    if modified:
        page['dateModified'] = modified
    if m.get('article:tag'):
        page['keywords'] = ', '.join(m['article:tag'])
    if cfg.get('contributor'):
        page['contributor'] = {'@type': 'SoftwareApplication', 'name': cfg['contributor']}
    graph = [person, website, page]
    set_id = base + url + '#terms'
    terms = defined_terms(url, src, set_id)
    if terms:
        graph.append({'@type': 'DefinedTermSet', '@id': set_id, 'name': title, 'url': base + url, 'hasDefinedTerm': terms})
        page['mainEntity'] = {'@id': set_id} if url == '/terms/' else page.get('mainEntity')
        if page['mainEntity'] is None:
            del page['mainEntity']
    data = {'@context': 'https://schema.org', '@graph': graph}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def head(t, trail, has_fonts, ld=''):
    css = '' if has_fonts else '<link rel="stylesheet" href="/fonts/fonts.css">'
    css += '<link rel="stylesheet" href="/design/tokens.css"><link rel="stylesheet" href="/design/chrome.css"><link rel="stylesheet" href="/design/components.css">'
    return css + crumbs_ld(t, trail) + ld


# ---------- apply ----------
SOURCE_RE = re.compile(r'<meta name="mb-source" content="([^"]+)">')
TITLE_RE = re.compile(r'<title>([^<]*)</title>')


def _body_class(src, add):
    m = re.search(r'<body([^>]*)>', src)
    if not m:
        return src
    attrs = m.group(1)
    cm = re.search(r'\sclass="([^"]*)"', attrs)
    have = [c for c in (cm.group(1).split() if cm else []) if not c.startswith('mb-')]
    cls = ' '.join(have + add)
    attrs = re.sub(r'\sclass="[^"]*"', '', attrs) + f' class="{cls}"'
    return src[:m.start()] + f'<body{attrs}>' + src[m.end():]


def _insert_after(src, pattern, text):
    m = re.search(pattern, src)
    if not m:
        return None
    return src[:m.end()] + text + src[m.end():]


def _insert_before(src, pattern, text):
    m = re.search(pattern, src)
    if not m:
        return None
    return src[:m.start()] + text + src[m.start():]


def apply(src, rel):
    """Return the page with its managed blocks written from site/nav.yml. rel is the path from the repo root."""
    t = tree()
    url = url_of(rel)
    node = t.by_url.get(url)
    if rel == NOT_FOUND:
        trail = [t.home, Node('Page not found', '/404.html')]
    elif node is None:
        title = TITLE_RE.search(src)
        trail = [t.home, Node(html.unescape(title.group(1)).split(':')[0].strip() if title else url, url)]
    else:
        trail = t.trail(node)

    # 1. lift the managed blocks out, leaving a sentinel where each one was
    src = BLOCK_RE.sub(lambda m: f'\x00{m.group(1)}\x00', src)
    # 2. remove the old chrome
    for rx in LEGACY:
        src = rx.sub('', src)
    layout = 'read' if '<link rel="stylesheet" href="/style.css">' in src else 'app'
    ms = SOURCE_RE.search(src)
    source = ms.group(1) if ms else rel
    has_fonts = '/fonts/fonts.css' in src
    has_side = bool(node is not None and node.section in SIDEBARS and side(t, node))
    # page facts beside the breadcrumbs: hand-written pages only (generated pages carry their own byline)
    hand = ms is None and node is not None and node.url not in ('/', '/map/') and rel not in DEPLOY_ONLY and 'class="byline"' not in src

    blocks = {
        'head': head(t, trail, has_fonts, page_ld(t, node, trail, url, src, layout)),
        'bar': bar(t, node, layout),
        'crumbs': crumbs(trail, page_meta(t, url) if hand else ''),
        'side': side(t, node) if has_side else '',
        'foot': foot(t, url, source, trail[-1].title),
        'topics': topics_block(t, url),  # only where a page holds the marker (the docs sidebar)
    }
    main_open = r'<div class="sheet"[^>]*>' if layout == 'read' else r'<main\b[^>]*>'
    main_before = r'<div class="sheet"' if layout == 'read' else r'<main\b'
    anchors = {
        'head': (_insert_before, r'</head>'),
        'bar': (_insert_after, r'<body[^>]*>'),
        'crumbs': (_insert_after, main_open),
        'side': (_insert_before, main_before),
        'foot': (_insert_before, r'</body>'),
    }
    # 3. write each block where its sentinel is, or at its anchor
    for name, body in blocks.items():
        block = f'<!-- mb:{name} -->{body}<!-- /mb:{name} -->'
        sentinel = f'\x00{name}\x00'
        if sentinel in src:
            src = src.replace(sentinel, block, 1)
            continue
        if (name == 'side' and not body) or name == 'topics':
            continue
        fn, pat = anchors[name]
        nl = '\n' if name in ('bar', 'side', 'foot') else ''
        out = fn(src, pat, (block + nl) if fn is _insert_after else (block + nl))
        if out is None and name == 'crumbs':
            out = src.replace('<!-- /mb:bar -->', '<!-- /mb:bar -->' + block, 1)
        if out is None:
            raise ValueError(f'{rel}: no anchor for the {name} block ({pat})')
        src = out
    src = re.sub(r'\x00\w+\x00', '', src)  # a block this page no longer carries

    # 4. body classes and the skip-link target
    sec = node.section if node else 'none'
    src = _body_class(src, [f'mb-{layout}', f'mb-s-{sec}'] + (['mb-has-side'] if has_side else []))
    if 'id="main"' not in src:
        if layout == 'read':
            src = re.sub(r'<div class="sheet"', '<div class="sheet" id="main" role="main"', src, count=1)
        else:
            src = re.sub(r'<main\b', '<main id="main"', src, count=1)
    src = re.sub(r'\n{3,}', '\n\n', src)
    return src


# ---------- the whole site ----------
def page_files():
    out = []
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(SKIP_DIRS) or '/.' in rel or '/node_modules/' in rel:
            continue
        if rel.endswith('/index.html') or rel in ('index.html', NOT_FOUND):
            out.append((rel, p))
    return out


def report(t, files):
    """Orphans (pages outside the tree), tree pages missing from sitemap.xml or llms.txt, sitemap URLs outside the tree."""
    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    llms = (ROOT / 'llms.txt').read_text(encoding='utf-8')
    in_sitemap = {u[len(t.base):] for u in re.findall(r'<loc>([^<]+)</loc>', sitemap)}
    on_disk = {url_of(rel) for rel, _ in files if rel != NOT_FOUND}
    tree_pages = set(t.page_urls())
    errors, warnings = [], []
    for rel, p in files:  # every JSON-LD block on every page must parse (ADR-0027)
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', p.read_text(encoding='utf-8'), re.S):
            try:
                json.loads(block)
            except ValueError as e:
                errors.append(f'json-ld: {rel}: invalid JSON ({e})')
    for u in sorted(on_disk - tree_pages):
        errors.append(f'orphan: {u} is a page outside site/nav.yml')
    for u in sorted(tree_pages - on_disk):
        errors.append(f'missing page: {u} is in site/nav.yml but has no index.html')
    for u in sorted(tree_pages & on_disk):
        if u not in in_sitemap:
            errors.append(f'sitemap: {u} is missing from sitemap.xml')
        if u != '/' and (t.base + u) not in llms:
            warnings.append(f'llms.txt: {u} is not listed')
    for u in sorted(in_sitemap - tree_pages):
        errors.append(f'sitemap: {u} is in sitemap.xml but outside site/nav.yml')
    return errors, warnings


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    check = '--check' in argv
    deploy = '--deploy' in argv  # the deploy job: also write the pages in DEPLOY_ONLY
    t = tree()
    files = page_files()
    stale = []
    for rel, p in files:
        src = p.read_text(encoding='utf-8')
        new = apply(src, rel)
        if new != src:
            if rel in DEPLOY_ONLY and not deploy:
                continue
            stale.append(rel)
            if not check:
                p.write_text(new, encoding='utf-8')
    errors, warnings = report(t, files)
    for w in warnings:
        print('warning', w)
    for e in errors:
        print('error', e)
    if check:
        for s in stale:
            print('chrome differs from site/nav.yml:', s)
        print(f'{len(files)} pages checked: {len(stale)} differ, {len(errors)} errors, {len(warnings)} warnings')
        return 1 if stale or errors else 0
    print(f'{len(files)} pages: chrome written to {len(stale)}; {len(errors)} errors, {len(warnings)} warnings')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
