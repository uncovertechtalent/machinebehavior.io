#!/usr/bin/env python3
"""Build the Inside documentation tree (/inside/docs/) from markdown sources.

Sources: scripts/docs/<space>/<slug>.md, one file per page, front matter then a line '---' then the body.
Hand-written spaces (eng, obs, res, fin) are edited in place; vault spaces (sre, std) are written by
scripts/import_vault_docs.py and should not be edited here.

Output: inside/docs/index.html (space directory), inside/docs/<space>/index.html (space home),
inside/docs/<space>/<slug>/index.html (pages), inside/docs/search.json, plus a managed block in
sitemap.xml and a managed section in llms.txt.

Run from the repo root:  python3 scripts/build_docs.py
"""
import datetime, html, json, os, re, shutil, subprocess, sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inside_chrome  # the one top bar of Inside

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'scripts' / 'docs'
OUT = ROOT / 'inside' / 'docs'
BASE = 'https://machinebehavior.io'
REPO = 'https://github.com/uncovertechtalent/machinebehavior.io'
TODAY = datetime.date.today().isoformat()

SPACES = [
    {'key': 'eng', 'name': 'Engineering', 'color': '#FFB547',
     'about': 'How the three sites are built, gated and deployed, the map crawler, Inside and this docs tree.'},
    {'key': 'obs', 'name': 'Observability', 'color': '#3DDC97',
     'about': 'Prometheus, Loki and Grafana behind the public dashboards: the deploy exporter, metrics, streams and runbooks.'},
    {'key': 'res', 'name': 'Research', 'color': '#FF8FD8',
     'about': 'The research programme as an internal wiki: studies, registers, logs and case files, with their data and how to rerun them.'},
    {'key': 'fin', 'name': 'FinOps', 'color': '#FF7A6B',
     'about': 'What the platform costs and how it is metered: the cost model, unit economics, showback, budgets and alerts, an anomaly case and a FOCUS export.'},
    {'key': 'sre', 'name': 'SRE Handbook', 'color': '#6FA8FF',
     'about': 'Site reliability engineering from the knowledge vault: the manifesto, ten pillars, patterns, runbooks, tools and incident records.'},
    {'key': 'std', 'name': 'Standards and Compliance', 'color': '#B79CFF',
     'about': 'Reference clusters from the knowledge vault for 28 standards, regulations and frameworks: ISO 27001 and 42001, NIS2, DORA, the EU AI Act, GDPR, SOC 2, TISAX, NIST and more.'},
]
SPACE = {s['key']: s for s in SPACES}
HAND = {'eng', 'obs', 'res', 'fin'}          # written in the repository; vault spaces come from the knowledge vault
SPACE_OWNER = 'Stefan Coetzee'               # owner of a vault page that names none
TYPES = ('tutorial', 'how-to', 'reference', 'explanation')  # Diátaxis
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
VAULT_TYPES = {  # vault note type -> Diátaxis type
    'runbook': 'how-to',
    'moc': 'reference', 'anchors': 'reference', 'iso-clause': 'reference', 'annex-a-theme': 'reference', 'tool': 'reference',
    'regulation-concept': 'reference', 'framework-concept': 'reference', 'itil-concept': 'reference', 'togaf-component': 'reference',
    'tisax-mechanism': 'reference', 'detection-method': 'reference', 'hardware': 'reference', 'togaf-mechanism': 'reference',
    'tisax-catalogue': 'reference', 'threat-list': 'reference', 'itil-mechanism': 'reference', 'iso-concept': 'reference',
    'framework-profile': 'reference', 'annex-a': 'reference', 'mitigations': 'explanation', 'method': 'explanation',
    'metaphor': 'explanation', 'false-finding': 'explanation',
    'position': 'explanation', 'cross-cutting': 'explanation', 'pattern': 'explanation', 'incident': 'explanation',
    'root-cause': 'explanation', 'concept': 'explanation', 'mitigation': 'explanation', 'practice': 'explanation',
}
if '--only' in sys.argv:  # build a subset while other spaces are being written
    _only = sys.argv[sys.argv.index('--only') + 1].split(',')
    SPACES = [s for s in SPACES if s['key'] in _only]


# ---------- sources ----------
def parse_source(path):
    text = path.read_text(encoding='utf-8')
    head, sep, body = text.partition('\n---\n')
    if not sep:
        sys.exit(f'{path}: no front matter separator')
    meta = {}
    for line in head.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    for req in ('title', 'summary'):
        if not meta.get(req):
            sys.exit(f'{path}: missing {req}')
    meta['labels'] = [x.strip() for x in meta.get('labels', '').split(',') if x.strip()]
    meta['aliases'] = [x.strip() for x in meta.get('aliases', '').split('|') if x.strip()]
    meta['order'] = int(meta.get('order') or 1000)
    if meta.get('type') and meta['type'] not in TYPES:
        if not meta.get('origin'):
            sys.exit(f'{path}: type must be one of {", ".join(TYPES)}')
        # a vault note carries its own note type; map it to Diátaxis where the mapping is plain, else leave the type empty
        meta['note_type'] = meta['type']
        meta['type'] = VAULT_TYPES.get(meta['type'].strip().lower(), '')
    rv = meta.get('reviewed', '')
    if rv and rv != 'no' and not DATE.match(rv):
        sys.exit(f'{path}: reviewed must be YYYY-MM-DD or no')
    if meta.get('review_by') and not DATE.match(meta['review_by']):
        sys.exit(f'{path}: review_by must be YYYY-MM-DD')
    return meta, body.strip('\n')


def git_date(path):
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', str(path)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', str(path)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return TODAY if dirty or not out else out
    except Exception:
        return TODAY


pages = {}  # (space, slug) -> page dict
for sp in SPACES:
    d = SRC / sp['key']
    if not d.is_dir():
        continue
    for f in sorted(d.glob('*.md')):
        meta, body = parse_source(f)
        slug = 'index' if f.stem == 'index' else f.stem
        p = dict(meta)
        p.update(space=sp['key'], slug=slug, body=body, src=f.relative_to(ROOT).as_posix())
        p['url'] = f"/inside/docs/{sp['key']}/" + ('' if slug == 'index' else f'{slug}/')
        p['updated'] = meta.get('updated') or meta.get('created') or git_date(f)
        p['created'] = meta.get('created') or p['updated']
        if not p.get('owner') and sp['key'] not in HAND:
            p['owner'], p['owner_default'] = SPACE_OWNER, True
        pages[(sp['key'], slug)] = p

spaces_present = [s for s in SPACES if (s['key'], 'index') in pages]
for s in SPACES:
    if any(k[0] == s['key'] for k in pages) and (s['key'], 'index') not in pages:
        sys.exit(f"space {s['key']} has pages but no index.md")

# tree
children = {}
for (sk, slug), p in pages.items():
    if slug == 'index':
        continue
    par = p.get('parent') or 'index'
    if (sk, par) not in pages:
        print(f'warning: {p["src"]}: parent {par} not found, placed under the space home', file=sys.stderr)
        par = 'index'
    p['parent'] = par
    children.setdefault((sk, par), []).append(p)
for k in children:
    children[k].sort(key=lambda p: (p['order'], p['title'].lower()))


def ancestors(p):
    out, cur = [], p
    while cur['slug'] != 'index':
        cur = pages[(cur['space'], cur['parent'])]
        out.append(cur)
    return list(reversed(out))


# link index: titles, aliases, slugs and vault origin paths
LINK = {}
def reg(key, p):
    k = key.strip().lower()
    if k and k not in LINK:
        LINK[k] = p
for p in pages.values():
    reg(p['title'], p)
    for a in p['aliases']:
        reg(a, p)
    if p.get('origin'):
        o = p['origin']
        reg(o, p); reg(re.sub(r'\.md$', '', o), p)
        reg(Path(o).stem, p)
        if o.endswith('/README.md') or o.endswith('/'):  # folder notes answer to the folder and folder/index
            d = o[:-len('README.md')] if o.endswith('README.md') else o
            reg(d.rstrip('/'), p); reg(d + 'index', p)
for p in pages.values():
    reg(f"{p['space']}/{p['slug']}", p)


# ---------- markdown ----------
def slugify(s):
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'[^a-z0-9]+', '-', html.unescape(s).lower()).strip('-') or 'section'


class Ctx:
    def __init__(self, page):
        self.page = page
        self.out_links = set()
        self.missing = set()


def resolve_href(url, ctx):
    url = url.strip()
    if url.startswith('doc:'):
        key = url[4:].split('#')[0].lower()
        frag = url[4:].split('#')[1] if '#' in url else ''
        t = LINK.get(key)
        if not t:
            sys.exit(f"{ctx.page['src']}: unknown doc link {url}")
        ctx.out_links.add(t['url'])
        return t['url'] + (f'#{slugify(frag)}' if frag else '')
    if re.match(r'(https?:|mailto:)', url):
        return url
    if url.startswith('/'):
        return url
    if url.startswith('#'):
        return '#' + slugify(url[1:])
    # a vault-relative .md link: try from the vault root, then from the note's folder
    path, _, frag = url.partition('#')
    path = re.sub(r'%20', ' ', path)
    cands = [path, re.sub(r'\.md$', '', path)]
    origin = ctx.page.get('origin')
    if origin:
        base = os.path.normpath(os.path.join(os.path.dirname(origin), path))
        cands += [base, re.sub(r'\.md$', '', base)]
    for c in cands:
        t = LINK.get(c.lower())
        if t:
            ctx.out_links.add(t['url'])
            return t['url'] + (f'#{slugify(frag)}' if frag else '')
    return None


# vault notes that are published elsewhere on the sites
ELSEWHERE = {
    'objections and falsification register': '/objections/',
    'continuous conformity - definition draft': '/continuous-conformity-self-assessment/',
    '_series-running-the-golem': 'https://uncovertechtalent.com/blog/',
    'the-trap-file/draft': 'https://uncovertechtalent.com/blog/the-trap-file-is-longer-than-the-instruction-file/',
}


def wikilink(inner, ctx):
    target, _, label = inner.partition('|')
    target, _, frag = target.partition('#')
    label = label or (target if target else frag)
    label = re.sub(r'^.*/', '', label) if '|' not in inner else label
    t = LINK.get(target.strip().lower()) or LINK.get(target.strip().split('/')[-1].lower())
    if not target.strip():
        return f'<a href="#{slugify(frag)}">{html.escape(label)}</a>'
    if t:
        ctx.out_links.add(t['url'])
        return f'<a href="{t["url"]}{("#" + slugify(frag)) if frag else ""}">{html.escape(label)}</a>'
    ext = ELSEWHERE.get(target.strip().lower())
    if ext:
        return f'<a href="{ext}">{html.escape(label)}</a>'
    ctx.missing.add(target.strip())
    return f'<span class="wl-off" title="Vault note not published here">{html.escape(label)}</span>'


def inline(s, ctx):
    stash = []
    def keep(h):
        stash.append(h)
        return f'\x00{len(stash) - 1}\x00'
    s = re.sub(r'`([^`]+)`', lambda m: keep(f'<code>{html.escape(m.group(1))}</code>'), s)
    s = re.sub(r'!\[\[[^\]]*\]\]', '', s)                     # embeds are not carried
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)                 # nor images
    s = re.sub(r'\[\[([^\]]+)\]\]', lambda m: keep(wikilink(m.group(1), ctx)), s)
    def mdlink(m):
        text, url = m.group(1), m.group(2).split(' "')[0]
        href = resolve_href(url, ctx)
        inner_html = inline(text, ctx)
        if href is None:
            return keep(f'<span class="wl-off" title="Vault file not published here">{inner_html}</span>')
        return keep(f'<a href="{html.escape(href)}">{inner_html}</a>')
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+(?: "[^"]*")?)\)', mdlink, s)
    s = re.sub(r'<(https?://[^>\s]+)>', lambda m: keep(f'<a href="{html.escape(m.group(1))}">{html.escape(m.group(1))}</a>'), s)
    s = re.sub(r'(?<![("=\w])(https?://[^\s<>()\]]+[^\s<>()\].,;:!?\'"])', lambda m: keep(f'<a href="{html.escape(m.group(1))}">{html.escape(m.group(1))}</a>'), s)
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'__(.+?)__', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])', r'<em>\1</em>', s)
    s = re.sub(r'~~(.+?)~~', r'<del>\1</del>', s)
    s = re.sub(r'==(.+?)==', r'<mark>\1</mark>', s)
    while '\x00' in s:
        s = re.sub(r'\x00(\d+)\x00', lambda m: stash[int(m.group(1))], s)
    return s


PANEL = {'info': 'info', 'note': 'note', 'tip': 'tip', 'warning': 'warning', 'caution': 'warning', 'danger': 'warning',
         'important': 'note', 'abstract': 'info', 'summary': 'info', 'example': 'note', 'question': 'info', 'quote': 'quote',
         'success': 'tip', 'failure': 'warning', 'bug': 'warning', 'todo': 'note'}


def render(md, ctx, toc):
    lines = md.replace('\t', '    ').split('\n')
    out, i, n = [], 0, len(lines)
    para = []

    def flush():
        if para:
            out.append('<p>' + inline(' '.join(x.strip() for x in para), ctx) + '</p>')
            para.clear()

    while i < n:
        line = lines[i]
        st = line.strip()
        m = re.match(r'^(\s*)(```|~~~)\s*([\w+-]*)', line)
        if m:
            flush()
            fence, lang, buf = m.group(2), m.group(3), []
            i += 1
            while i < n and not lines[i].strip().startswith(fence):
                buf.append(lines[i]); i += 1
            i += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ''
            out.append(f'<pre><code{cls}>' + html.escape('\n'.join(buf)) + '</code></pre>')
            continue
        if st.startswith('%%'):
            flush()
            if not (st.endswith('%%') and len(st) > 2):
                i += 1
                while i < n and '%%' not in lines[i]:
                    i += 1
            i += 1
            continue
        if not st:
            flush(); i += 1; continue
        m = re.match(r'^(#{1,6})\s+(.*?)\s*#*$', st)
        if m:
            flush()
            lvl = len(m.group(1))
            text = inline(m.group(2), ctx)
            hid = slugify(text)
            base, k = hid, 2
            while hid in ctx.__dict__.setdefault('ids', set()):
                hid = f'{base}-{k}'; k += 1
            ctx.ids.add(hid)
            tag = min(max(lvl, 2), 4)
            if lvl in (1, 2, 3):
                toc.append((min(max(lvl, 2), 3), hid, re.sub(r'<[^>]+>', '', text)))
            out.append(f'<h{tag} id="{hid}">{text}</h{tag}>')
            i += 1; continue
        if re.match(r'^(\*\s*\*\s*\*|-\s*-\s*-|_\s*_\s*_)[\s*_-]*$', st):
            flush(); out.append('<hr>'); i += 1; continue
        if st.startswith('|') and i + 1 < n and re.match(r'^\s*\|?\s*:?-{2,}', lines[i + 1]):
            flush()
            def cells(row):
                row = row.strip().strip('|')
                return [c.strip() for c in re.split(r'(?<!\\)\|', row)]
            head = cells(lines[i]); i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(cells(lines[i])); i += 1
            t = '<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{inline(c, ctx)}</th>' for c in head) + '</tr></thead><tbody>'
            for r in rows:
                t += '<tr>' + ''.join(f'<td>{inline(c, ctx)}</td>' for c in r) + '</tr>'
            out.append(t + '</tbody></table></div>')
            continue
        if st.startswith('>'):
            flush()
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            m = re.match(r'^\[!(\w+)\][+-]?\s*(.*)$', buf[0].strip())
            if m:
                kind = PANEL.get(m.group(1).lower(), 'note')
                title = m.group(2)
                inner = render('\n'.join(buf[1:]), ctx, []) if len(buf) > 1 else ''
                if title and not inner:
                    inner, title = '<p>' + inline(title, ctx) + '</p>', ''
                head = f'<div class="panel-title">{inline(title, ctx)}</div>' if title else ''
                out.append(f'<div class="panel panel-{kind}">{head}{inner}</div>')
            else:
                out.append('<blockquote>' + render('\n'.join(buf), ctx, []) + '</blockquote>')
            continue
        if re.match(r'^\s*([-*+]|\d+[.)])\s+', line):
            flush()
            block = []
            while i < n and (re.match(r'^\s*([-*+]|\d+[.)])\s+', lines[i]) or (lines[i].startswith('  ') and lines[i].strip() and block)):
                block.append(lines[i]); i += 1
            out.append(render_list(block, ctx))
            continue
        para.append(line)
        i += 1
    flush()
    return '\n'.join(out)


def render_list(block, ctx):
    items = []  # (indent, ordered, text)
    for ln in block:
        m = re.match(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$', ln)
        if m:
            items.append([len(m.group(1)), m.group(2)[0].isdigit(), m.group(3)])
        elif items:
            items[-1][2] += ' ' + ln.strip()

    def build(idx, indent):
        ordered = items[idx][1]
        tag = 'ol' if ordered else 'ul'
        h = f'<{tag}>'
        while idx < len(items) and items[idx][0] >= indent:
            ind, _, text = items[idx]
            if ind > indent:
                sub, idx = build(idx, ind)
                h = h[:-5] + sub + '</li>' if h.endswith('</li>') else h + sub
                continue
            m = re.match(r'^\[([ xX])\]\s+(.*)$', text)
            if m:
                box = '☑' if m.group(1).lower() == 'x' else '☐'
                h += f'<li class="task"><span class="box">{box}</span> {inline(m.group(2), ctx)}</li>'
            else:
                h += f'<li>{inline(text, ctx)}</li>'
            idx += 1
        return h + f'</{tag}>', idx

    html_out, idx = '', 0
    while idx < len(items):
        part, idx = build(idx, items[idx][0])
        html_out += part
    return html_out


# ---------- render pages ----------
def esc(s):
    return html.escape(str(s), quote=True)


def text_of(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


for p in pages.values():
    ctx = Ctx(p)
    toc = []
    p['html'] = render(p['body'], ctx, toc)
    p['toc'] = toc
    p['out_links'] = ctx.out_links - {p['url']}
    p['missing'] = ctx.missing
    p['words'] = len(text_of(p['html']).split())

backlinks = {}
for p in pages.values():
    for u in p['out_links']:
        backlinks.setdefault(u, set()).add((p['space'], p['slug']))
BY_URL = {p['url']: p for p in pages.values()}


def tree_html(space, current):
    open_set = {(a['space'], a['slug']) for a in ancestors(current)} | {(current['space'], current['slug'])}

    def walk(key, depth):
        kids = children.get(key, [])
        if not kids:
            return ''
        h = '<ul>'
        for c in kids:
            ck = (c['space'], c['slug'])
            cur = ' aria-current="page"' if ck == (current['space'], current['slug']) else ''
            link = f'<a href="{c["url"]}"{cur}>{esc(c["title"])}</a>'
            sub = walk(ck, depth + 1)
            if sub:
                op = ' open' if ck in open_set else ''
                h += f'<li><details{op}><summary>{link}</summary>{sub}</details></li>'
            else:
                h += f'<li class="leaf">{link}</li>'
        return h + '</ul>'
    return walk((space, 'index'), 0)


FONTS = '<link rel="stylesheet" href="/fonts/fonts.css">'
ICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛋️</text></svg>">'


def topbar():
    return inside_chrome.bar('docs') + '\n' + inside_chrome.banner()


def footer(p=None):
    src = ''
    if p:
        src = f'<a href="{REPO}/blob/main/{esc(p["src"])}">page source</a> · <a href="{REPO}/commits/main/{esc(p["src"])}">history</a>'
        if p.get('origin'):
            src += f' · from the knowledge vault, <span class="mono">{esc(p["origin"])}</span>'
        src += '<br>'
    return (f'<footer>{src}Inside docs · Stefan Coetzee · built from <a href="{REPO}/tree/main/scripts/docs">scripts/docs</a> by '
            f'<a href="{REPO}/blob/main/scripts/build_docs.py">build_docs.py</a><br>'
            '<span class="conf mono" data-conformity>conformity: <a class="mono" href="/conformity/">latest run</a></span> '
            '(self-assessment, not a certification)</footer>')


def head(title, desc, url, extra='', og_title=None):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{BASE}{url}">
<meta property="og:site_name" content="Machine Behavior">
<meta property="og:title" content="{esc(og_title or title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE}/inside/og.png">
<meta name="twitter:card" content="summary_large_image">
{extra}{ICON}
{FONTS}
<link rel="stylesheet" href="/inside/docs/docs.css">
<link rel="stylesheet" href="/inside/bar.css">
</head>'''


def scripts():
    return '<script src="/inside/bar.js" defer></script>\n<script src="/inside/docs/docs.js" defer></script>\n<script src="/conformity/footer.js" defer></script>'


def child_list(key):
    kids = children.get(key, [])
    if not kids:
        return ''
    h = '<nav class="children" aria-label="Child pages"><h2>Child pages</h2><ul>'
    for c in kids:
        h += f'<li><a href="{c["url"]}">{esc(c["title"])}</a><span>{esc(c["summary"])}</span></li>'
    return h + '</ul></nav>'


def recent(pool, k=8):
    rows = sorted(pool, key=lambda p: (p['updated'], p['title']), reverse=True)[:k]
    h = '<ul class="recent">'
    for r in rows:
        sp = SPACE[r['space']]
        h += (f'<li><span class="dot" style="background:{sp["color"]}"></span><a href="{r["url"]}">{esc(r["title"])}</a>'
              f'<span class="mono">{esc(sp["name"])} · {r["updated"]}</span></li>')
    return h + '</ul>'


def page_html(p):
    sp = SPACE[p['space']]
    anc = ancestors(p)
    is_home = p['slug'] == 'index'
    title = f'{p["title"]} · {sp["name"]} · Inside docs' if not is_home else f'{sp["name"]} · Inside docs'
    extra = f'<meta name="docs-space" content="{sp["key"]}">\n'
    extra += f'<meta property="article:published_time" content="{p["created"]}">\n<meta property="article:modified_time" content="{p["updated"]}">\n'
    extra += ''.join(f'<meta property="article:tag" content="{esc(l)}">\n' for l in p['labels'])
    for k in ('owner', 'reviewed', 'review_by', 'type'):
        if p.get(k):
            extra += f'<meta name="docs-{k.replace("_", "-")}" content="{esc(p[k])}">\n'
    if not is_home:
        par = pages[(p['space'], p['parent'])]
        extra += f'<link rel="up" href="{par["url"]}">\n'
    crumbs = '<a href="/inside/docs/">Docs</a>' + ''.join(f'<a href="{a["url"]}">{esc(SPACE[a["space"]]["name"] if a["slug"] == "index" else a["title"])}</a>' for a in anc)
    if is_home:
        crumbs = '<a href="/inside/docs/">Docs</a>'
    by = f'<span>owner {esc(p["owner"])}</span>' if p.get('owner') else '<span class="rv late">no owner</span>'
    by += f'<span>created {p["created"]}</span><span>updated {p["updated"]}</span>'
    rv, rb = p.get('reviewed', ''), p.get('review_by', '')
    if rv == 'no' or not rv:
        by += '<span class="rv no">not reviewed</span>'
    elif rb and rb < TODAY:
        by += f'<span>reviewed {rv}</span><span class="rv late">review overdue since {rb}</span>'
    else:
        by += f'<span>reviewed {rv}</span>' + (f'<span>review by {rb}</span>' if rb else '')
    by += f'<span>{max(1, round(p["words"] / 220))} min read</span>'
    if p.get('type'):
        by += f'<span class="type">{esc(p["type"])}</span>'
    review = ''
    if p.get('reviewed', '').lower() == 'no':
        review = (f'<div class="review"><b>Vault note, not reviewed against the source.</b> Written in the knowledge vault on {p["created"]} by models '
                  'working with Stefan Coetzee and published as it stands, with private addresses, e-mail addresses and an employer name redacted. '
                  'Check claims against the primary source before relying on them.</div>')
    labels = ''
    if p['labels']:
        labels = '<nav class="labels" aria-label="Labels">' + ''.join(f'<a href="/inside/search/?q={esc(quote(l))}">{esc(l)}</a>' for l in p['labels']) + '</nav>'
    bl = sorted((pages[k] for k in backlinks.get(p['url'], set())), key=lambda x: x['title'].lower())
    back = ''
    if bl:
        back = '<nav class="backlinks" aria-label="Linked from"><h2>Linked from</h2><ul>' + ''.join(
            f'<li><a href="{b["url"]}">{esc(b["title"])}</a><span class="mono">{esc(SPACE[b["space"]]["name"])}</span></li>' for b in bl) + '</ul></nav>'
    toc = ''
    if len(p['toc']) >= 2:
        toc = '<nav class="toc" aria-label="On this page"><div class="toc-h">On this page</div><ul>' + ''.join(
            f'<li class="l{l}"><a href="#{i}">{esc(t)}</a></li>' for l, i, t in p['toc']) + '</ul></nav>'
    home_extra = ''
    if is_home:
        pool = [q for q in pages.values() if q['space'] == p['space'] and q['slug'] != 'index']
        home_extra = f'<section class="home-recent"><h2>Recently updated in this space</h2>{recent(pool, 6)}</section>'
    side = (f'<nav class="side" aria-label="Pages in {esc(sp["name"])}"><details class="side-wrap" open><summary>Pages in this space</summary>'
            f'<a class="space-head" href="/inside/docs/{sp["key"]}/"><span class="sp-icon" style="background:{sp["color"]}">{sp["key"].upper()}</span>'
            f'<span>{esc(sp["name"])}</span></a>{tree_html(p["space"], p)}</details></nav>')
    h1 = esc(sp['name']) if is_home else esc(p['title'])
    return f'''{head(title, p["summary"], p["url"], extra, og_title=sp["name"] if is_home else p["title"])}
<body>
{topbar()}
<div class="layout">
{side}
<main id="main">
<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
<h1>{h1}</h1>
<div class="byline">{by}</div>
{review}
<article class="doc">
{p["html"]}
</article>
{home_extra}
{child_list((p["space"], p["slug"]))}
{labels}
{back}
</main>
{toc}
</div>
{footer(p)}
{scripts()}
</body>
</html>
'''


def docs_home():
    url = '/inside/docs/'
    desc = 'Inside docs: the documentation tree of Stefan Coetzee\'s work in six spaces, Engineering, Observability, Research, FinOps, an SRE handbook and standards and compliance reference clusters.'
    cards = ''
    for s in spaces_present:
        n = sum(1 for k in pages if k[0] == s['key'])
        upd = max(p['updated'] for p in pages.values() if p['space'] == s['key'])
        cards += (f'<a class="space-card" href="/inside/docs/{s["key"]}/"><span class="sp-icon" style="background:{s["color"]}">{s["key"].upper()}</span>'
                  f'<b>{esc(s["name"])}</b><span class="about">{esc(s["about"])}</span><span class="mono">{n} pages · updated {upd}</span></a>')
    total = len(pages)
    links_n = sum(len(p['out_links']) for p in pages.values())
    newest = max(p['updated'] for p in pages.values())
    return f'''{head('Inside docs · Machine Behavior', desc, url, f'<meta property="article:modified_time" content="{newest}">' + chr(10))}
<body>
{topbar()}
<div class="layout wide">
<main id="main">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/inside/">Inside</a></nav>
<h1>Docs</h1>
<p class="lede">{total} pages in {len(spaces_present)} spaces, {links_n} links between them, updated {newest}. Each page is a node in the <a href="/map/">map of the work</a>; front matter becomes its labels, dates and place in the tree. Hand-written spaces document the systems behind this site; the SRE handbook and the standards clusters come from the knowledge vault and carry a review label. Owners and review dates: <a href="/inside/docs/health/">Docs health</a>.</p>
<section class="spaces">{cards}</section>
<section class="home-recent"><h2>Recently updated</h2>{recent(pages.values(), 12)}</section>
</main>
</div>
{footer()}
{scripts()}
</body>
</html>
'''


def health_page():
    url = '/inside/docs/health/'
    allp = sorted(pages.values(), key=lambda p: (p['space'], p['title'].lower()))
    hand = [p for p in allp if p['space'] in HAND]
    def due(p):
        return p.get('reviewed') not in (None, '', 'no') and p.get('review_by')
    overdue = sorted((p for p in allp if due(p) and p['review_by'] < TODAY), key=lambda p: p['review_by'])
    soon_limit = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
    soon = sorted((p for p in allp if due(p) and TODAY <= p['review_by'] <= soon_limit), key=lambda p: p['review_by'])
    no_owner = [p for p in allp if not p.get('owner')]
    no_type = [p for p in hand if not p.get('type')]
    not_rev = [p for p in allp if p.get('reviewed') in (None, '', 'no')]
    reviewed = [p for p in allp if due(p)]

    def table(rows, cols):
        if not rows:
            return '<p class="lede">None today.</p>'
        h = '<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{c}</th>' for c, _ in cols) + '</tr></thead><tbody>'
        for p in rows:
            h += '<tr>' + ''.join(f'<td>{f(p)}</td>' for _, f in cols) + '</tr>'
        return h + '</tbody></table></div>'
    link = lambda p: f'<a href="{p["url"]}">{esc(p["title"])}</a>'
    spn = lambda p: esc(SPACE[p['space']]['name'])
    cols_review = [('Page', link), ('Space', spn), ('Owner', lambda p: esc(p.get('owner', ''))), ('Reviewed', lambda p: p['reviewed']), ('Review by', lambda p: p['review_by'])]
    by_space = ''
    for sp in spaces_present:
        ps = [p for p in allp if p['space'] == sp['key']]
        nr = sum(1 for p in ps if p.get('reviewed') in (None, '', 'no'))
        od = sum(1 for p in ps if due(p) and p['review_by'] < TODAY)
        ty = sum(1 for p in ps if p.get('type'))
        by_space += (f'<tr><td><a href="/inside/docs/{sp["key"]}/">{esc(sp["name"])}</a></td><td>{len(ps)}</td><td>{len(ps) - nr}</td><td>{nr}</td><td>{od}</td>'
                     f'<td>{ty}</td><td>{"space default" if sp["key"] not in HAND else "per page"}</td></tr>')
    desc = f'Docs health: which of the {len(allp)} docs pages have an owner, a type and a review date, which are past review and which have never been reviewed.'
    return f'''{head('Docs health · Inside docs', desc, url, f'<meta property="article:modified_time" content="{TODAY}">' + chr(10), og_title='Docs health')}
<body>
{topbar()}
<div class="layout wide">
<main id="main">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/inside/docs/">Docs</a><a href="{url}">Health</a></nav>
<h1>Docs health</h1>
<div class="byline"><span>built {TODAY}</span><span>{len(allp)} pages</span></div>
<p class="lede">Each page should name an owner, the date it was last reviewed, the date of its next review and a type (tutorial, how-to, reference or explanation, after Diátaxis). This page lists what is missing or late. {len(reviewed)} pages have a review date, {len(overdue)} are past it, {len(not_rev)} have never been reviewed, and {len(no_owner)} have no owner. Pages from the knowledge vault start as not reviewed and take the space owner until a page names its own. A missing field or a late review does not block a deploy; whether it should is an open decision.</p>
<article class="doc">
<h2 id="overdue">Past the review date</h2>
{table(overdue, cols_review)}
<h2 id="soon">Due in the next 30 days</h2>
{table(soon, cols_review)}
<h2 id="no-owner">Without an owner</h2>
{table(no_owner, [('Page', link), ('Space', spn)])}
<h2 id="no-type">Hand-written pages without a type</h2>
{table(no_type, [('Page', link), ('Space', spn)])}
<h2 id="spaces">By space</h2>
<div class="tbl"><table><thead><tr><th>Space</th><th>Pages</th><th>Reviewed</th><th>Not reviewed</th><th>Overdue</th><th>With type</th><th>Owner</th></tr></thead><tbody>{by_space}</tbody></table></div>
<h2 id="fields">The fields</h2>
<p>In the front matter of each source file: <code>owner</code> (who keeps the page true), <code>reviewed</code> (the date the page was last checked against the system or source it describes, or <code>no</code>), <code>review_by</code> (the date of the next check; 90 days after the review by default) and <code>type</code>. For a hand-written page, the date it was written from the source counts as its first review. How to set them: <a href="/inside/docs/eng/docs-tree/">Docs tree</a>.</p>
</article>
</main>
</div>
{footer()}
{scripts()}
</body>
</html>
'''


# ---------- write ----------
if OUT.exists():
    for d in OUT.iterdir():
        if d.is_dir() and d.name in SPACE:
            shutil.rmtree(d)
OUT.mkdir(parents=True, exist_ok=True)
for p in pages.values():
    target = ROOT / p['url'].lstrip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page_html(p), encoding='utf-8')
(OUT / 'index.html').write_text(docs_home(), encoding='utf-8')
(OUT / 'health').mkdir(exist_ok=True)
(OUT / 'health' / 'index.html').write_text(health_page(), encoding='utf-8')
_missing = [p['src'] for p in pages.values() if p['space'] in HAND and not all(p.get(k) for k in ('owner', 'reviewed', 'review_by', 'type'))]
for m in _missing:
    print(f'warning: {m}: missing owner, reviewed, review_by or type', file=sys.stderr)

index = [{'t': p['title'], 'u': p['url'], 's': p['space'], 'd': p['summary'], 'l': p['labels'],
          'x': text_of(p['html'])[:400]} for p in sorted(pages.values(), key=lambda p: (p['space'], p['url']))]
(OUT / 'search.json').write_text(json.dumps({'spaces': {s['key']: {'name': s['name'], 'color': s['color']} for s in SPACES}, 'pages': index},
                                            ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

# sitemap: managed block
sm = (ROOT / 'sitemap.xml').read_text()
block = '  <!-- docs:begin (scripts/build_docs.py) -->\n' + f'  <url><loc>{BASE}/inside/docs/</loc><lastmod>{max(p["updated"] for p in pages.values())}</lastmod></url>\n'
block += f'  <url><loc>{BASE}/inside/docs/health/</loc><lastmod>{TODAY}</lastmod></url>\n'
block += ''.join(f'  <url><loc>{BASE}{p["url"]}</loc><lastmod>{p["updated"]}</lastmod></url>\n' for p in sorted(pages.values(), key=lambda p: p['url']))
block += '  <!-- docs:end -->\n'
sm = re.sub(r'  <!-- docs:begin.*?<!-- docs:end -->\n', '', sm, flags=re.S)
sm = sm.replace('</urlset>', block + '</urlset>')
(ROOT / 'sitemap.xml').write_text(sm)

# llms.txt: managed section "## Inside docs" (replaced in place, other sections untouched)
sec = f'The documentation tree at {BASE}/inside/docs/ ({len(pages)} pages). Search index: {BASE}/inside/docs/search.json (docs only; the site-wide index is {BASE}/inside/search.json). Pages from the knowledge vault (SRE Handbook, Standards and Compliance) are labelled as not reviewed against their sources. Owner, review date and type per page, and the pages past review: {BASE}/inside/docs/health/.\n'
for s in spaces_present:
    home = pages[(s['key'], 'index')]
    sec += f'\n### {s["name"]}\n\n- [{s["name"]}]({BASE}{home["url"]}): {s["about"]}\n'
    for p in sorted((q for q in pages.values() if q['space'] == s['key'] and q['slug'] != 'index'), key=lambda q: q['url']):
        sec += f'- [{p["title"]}]({BASE}{p["url"]})\n'
inside_chrome.llms_section('Inside docs', sec)

miss = sorted({m for p in pages.values() for m in p['missing']})
print(f'pages {len(pages)} in {len(spaces_present)} spaces; links {sum(len(p["out_links"]) for p in pages.values())}; unresolved wikilinks {len(miss)}')
if '-v' in sys.argv:
    for m in miss:
        print('  unresolved:', m)
