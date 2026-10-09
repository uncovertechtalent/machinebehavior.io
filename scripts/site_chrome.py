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

SIDEBARS = {'research', 'inside'}  # sections whose pages carry the section sidebar
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


def crumbs(trail):
    items = []
    for i, n in enumerate(trail):
        cur = ' aria-current="page"' if i == len(trail) - 1 else ''
        items.append(f'<li><a href="{n.url}"{cur}>{esc(n.title)}</a></li>')
    return '<nav class="mb-crumbs" aria-label="Breadcrumb"><ol>' + ''.join(items) + '</ol></nav>'


def crumbs_ld(t, trail):
    data = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n.title, 'item': t.base + n.url} for i, n in enumerate(trail)]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'


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
    return (f'<nav class="mb-side" aria-label="{esc(sec.title)} pages"><details class="mb-side-wrap" open>'
            f'<summary><span>{esc(sec.title)}</span><span class="mb-side-n">{count} pages</span></summary>'
            f'<a class="mb-side-head" href="{sec.url}"{head_cur}>{esc(sec.title)}</a>'
            f'<ul class="mb-side-tree">{items(sec.kids)}</ul></details></nav>')


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


def head(t, trail, has_fonts):
    css = '' if has_fonts else '<link rel="stylesheet" href="/fonts/fonts.css">'
    css += '<link rel="stylesheet" href="/design/tokens.css"><link rel="stylesheet" href="/design/chrome.css"><link rel="stylesheet" href="/design/components.css">'
    return css + crumbs_ld(t, trail)


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

    blocks = {
        'head': head(t, trail, has_fonts),
        'bar': bar(t, node, layout),
        'crumbs': crumbs(trail),
        'side': side(t, node) if has_side else '',
        'foot': foot(t, url, source, trail[-1].title),
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
        if name == 'side' and not body:
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
