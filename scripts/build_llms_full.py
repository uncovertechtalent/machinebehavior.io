#!/usr/bin/env python3
"""Write the full text of every public page for language models: a markdown twin per page, /llms-full.txt, and
/llms-passages.json, the passage index that the "ask mbio" MCP server searches.

- Pages: every <loc> of sitemap.xml on this site (the gate keeps every page in the sitemap). Each page's file is read
  from the tree as the deploy publishes it.
- Twin: <page dir>/index.html.md (the llms.txt convention: the page URL plus index.html.md), front matter with the
  URL, title, date and description, then the page body in markdown without the site chrome (top bar, menus,
  breadcrumbs, sidebars, footer, scripts).
- /llms-full.txt: every twin in sitemap order, each headed by its title, URL and date.
- /llms-passages.json: the twins cut into passages at headings (about 1,200 characters at most), each with its page,
  heading and text, plus the BM25 statistics of a fixed tokenizer (TOKENIZER below, the server checks the name).

Dates: "date" is the page's lastmod in sitemap.xml; "published" is the page's own article:published_time when it has one.

The deploy job runs this after every step that rewrites a page (artifact only, never committed), so the twins match
the deployed pages. Everything here is derived from published pages, so it can expose nothing the pages do not.

Private terms: --private-terms <file> scans every file this script writes with the matcher of the gate's private.terms
check (.github/actions/conformity/run.py, the same rule as security.private-terms in the CTO powersuit) and the
repository's .private-terms-allow, and exits 1 on a hit. The list stays on the owner's machine, so this runs in the
owner's dry run (conformity/README.md), never in CI; the gate's own scan skips files over 2 MB, and llms-full.txt is
larger, so this scan reads every byte.

Stdlib only. Run from the repo root:
    python3 scripts/build_llms_full.py [--root <site dir>] [--private-terms <file>] [--check-only]
"""
import argparse, datetime, html, json, math, re, sys, unicodedata
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

sys.dont_write_bytecode = True  # no __pycache__ in the repository
ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://machinebehavior.io'
TWIN = 'index.html.md'
FULL = 'llms-full.txt'
PASSAGES = 'llms-passages.json'
TOKENIZER = 'nfkd-lower-alnum-v1'  # the server refuses an index whose tokenizer name it does not know
PASSAGE_MAX = 1200

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
SKIP = {'script', 'style', 'noscript', 'template', 'svg', 'canvas', 'iframe', 'button', 'form', 'select', 'textarea',
        'nav', 'head', 'dialog', 'input', 'label'}
# Site chrome by class: the top bar, the footer, the intranet notice. Navigation elements are skipped as a whole (SKIP).
CHROME_CLASS = re.compile(r'(?:^|\s)(?:mb-bar|mb-foot|mb-demo|mb-menu[\w-]*|mb-crumb\w*|mb-side[\w-]*|mb-skip|mb-sr|mb-topics|'
                          r'skip-link|sr-only)(?:\s|$)')
BLOCK = {'p', 'div', 'section', 'article', 'main', 'header', 'aside', 'figure', 'figcaption', 'address', 'details',
         'summary', 'body', 'html', 'center', 'hgroup', 'search'}
# Elements a new tag of the same family closes when HTML leaves the end tag out.
AUTOCLOSE = {'p': {'p'}, 'li': {'li', 'p'}, 'dt': {'dt', 'dd', 'p'}, 'dd': {'dt', 'dd', 'p'}, 'tr': {'tr', 'td', 'th'},
             'td': {'td', 'th'}, 'th': {'td', 'th'}, 'option': {'option'}}
STOP_AT = {'ul', 'ol', 'dl', 'table', 'tbody', 'thead', 'tfoot', 'div', 'section', 'article', 'main', 'blockquote', 'body'}


class Node:
    __slots__ = ('tag', 'attrs', 'kids', 'parent')

    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.kids, self.parent = tag, dict(attrs or {}), [], parent


class Tree(HTMLParser):
    """A forgiving DOM: void elements, left-out end tags, stray end tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root')
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        closes = AUTOCLOSE.get(tag)
        if closes:
            n = self.cur
            while n is not self.root and n.tag not in STOP_AT:
                if n.tag in closes:
                    self.cur = n.parent
                    break
                n = n.parent
        node = Node(tag, attrs, self.cur)
        self.cur.kids.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root:
            if n.tag == tag:
                self.cur = n.parent
                return
            n = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def parse(doc):
    t = Tree()
    t.feed(doc)
    t.close()
    return t.root


def find(node, pred):
    for k in node.kids:
        if isinstance(k, Node):
            if pred(k):
                return k
            hit = find(k, pred)
            if hit:
                return hit
    return None


def text_of(node):
    if isinstance(node, str):
        return node
    return ''.join(text_of(k) for k in node.kids)


def skipped(node):
    a = node.attrs
    return (node.tag in SKIP or 'hidden' in a or a.get('aria-hidden') == 'true'
            or bool(CHROME_CLASS.search(a.get('class') or '')) or (a.get('role') in ('navigation', 'search')))


class Md:
    """HTML tree -> markdown. Blocks are separated by blank lines; inline text has its whitespace collapsed."""

    def __init__(self, url):
        self.url = url

    def inline(self, node):
        out, prev_el = [], False
        for k in node.kids:
            if isinstance(k, str):
                out.append(re.sub(r'\s+', ' ', k))
                prev_el = prev_el and not k.strip()
                continue
            if skipped(k):
                continue
            if prev_el and out and out[-1] and not out[-1][-1].isspace():
                out.append(' ')  # two elements side by side (a row of links, a meta strip) read as separate words
            prev_el = True
            t = k.tag
            if t == 'br':
                out.append('\n')
            elif t in ('strong', 'b'):
                s = self.inline(k).strip()
                out.append(f'**{s}**' if s else '')
            elif t in ('em', 'i', 'cite'):
                s = self.inline(k).strip()
                out.append(f'*{s}*' if s else '')
            elif t in ('code', 'kbd', 'samp'):
                s = re.sub(r'\s+', ' ', text_of(k)).strip()
                tick = '``' if '`' in s else '`'
                out.append(f'{tick}{s}{tick}' if s else '')
            elif t == 'a':
                s = self.inline(k).strip()
                href = (k.attrs.get('href') or '').strip()
                if not s:
                    continue
                if not href or href.startswith(('#', 'javascript:')):
                    out.append(s)
                else:
                    out.append(f'[{s}]({urljoin(self.url, href)})')
            elif t == 'img':
                alt = (k.attrs.get('alt') or '').strip()
                if alt:
                    out.append(f'[image: {alt}]')
            elif t == 'q':
                out.append('"' + self.inline(k).strip() + '"')
            else:
                out.append(self.inline(k))
        return ''.join(out)

    def blocks(self, node, depth=0):
        """List of markdown blocks for the children of node."""
        out, run = [], []

        def flush():
            s = re.sub(r'[ \t]+', ' ', ''.join(run)).strip()
            s = re.sub(r' *\n *', '\n', s)
            if s:
                out.append(s)
            run.clear()

        prev_el = False
        for k in node.kids:
            if isinstance(k, str):
                run.append(re.sub(r'\s+', ' ', k))
                prev_el = prev_el and not k.strip()
                continue
            if skipped(k):
                continue
            t = k.tag
            if t in BLOCK or t in ('ul', 'ol', 'dl', 'table', 'pre', 'blockquote', 'hr') or re.fullmatch(r'h[1-6]', t):
                flush()
                out.extend(self.block(k, depth))
                prev_el = False
            else:
                if prev_el and run and run[-1] and not run[-1][-1].isspace():
                    run.append(' ')
                wrapper = Node('#inline')
                wrapper.kids = [k]
                run.append(self.inline(wrapper))
                prev_el = True
        flush()
        return out

    def block(self, k, depth):
        t = k.tag
        if re.fullmatch(r'h[1-6]', t):
            s = re.sub(r'\s+', ' ', self.inline(k)).strip()
            return [f"{'#' * int(t[1])} {s}"] if s else []
        if t == 'hr':
            return ['---']
        if t == 'pre':
            body = text_of(k).strip('\n')
            if not body.strip():
                return []
            fence = '````' if '```' in body else '```'
            return [f'{fence}\n{body}\n{fence}']
        if t == 'blockquote':
            inner = '\n\n'.join(self.blocks(k, depth))
            return ['\n'.join('> ' + line if line else '>' for line in inner.split('\n'))] if inner.strip() else []
        if t in ('ul', 'ol'):
            return [self.list(k, depth)] if any(isinstance(c, Node) and c.tag == 'li' for c in k.kids) else []
        if t == 'dl':
            rows = []
            for c in k.kids:
                if isinstance(c, Node) and c.tag == 'dt':
                    s = re.sub(r'\s+', ' ', self.inline(c)).strip()
                    if s:
                        rows.append(('\n' if rows else '') + f'**{s}**')
                elif isinstance(c, Node) and c.tag == 'dd':
                    s = ' '.join(self.blocks(c, depth)).strip()
                    if s:
                        rows.append(f': {s}')
            return ['\n'.join(rows)] if rows else []
        if t == 'table':
            return self.table(k)
        if t == 'summary':
            s = re.sub(r'\s+', ' ', self.inline(k)).strip()
            return [f'**{s}**'] if s else []
        return self.blocks(k, depth)

    def list(self, k, depth):
        lines, n = [], int(k.attrs.get('start') or 1) if (k.attrs.get('start') or '1').isdigit() else 1
        pad = '  ' * depth
        for c in k.kids:
            if not (isinstance(c, Node) and c.tag == 'li') or skipped(c):
                continue
            marker = f'{n}.' if k.tag == 'ol' else '-'
            n += 1
            parts = self.blocks(c, depth + 1)
            if not parts:
                continue
            first, rest = parts[0], parts[1:]
            lines.append(f'{pad}{marker} ' + first.replace('\n', '\n' + pad + '  '))
            for r in rest:
                lines.append(r if r.startswith(pad + '  ') else pad + '  ' + r.replace('\n', '\n' + pad + '  '))
        return '\n'.join(lines)

    def table(self, k):
        rows = []

        def walk(n):
            for c in n.kids:
                if isinstance(c, Node):
                    if c.tag == 'tr':
                        cells = [c2 for c2 in c.kids if isinstance(c2, Node) and c2.tag in ('td', 'th')]
                        rows.append([re.sub(r'\s+', ' ', ' '.join(self.blocks(x)) or self.inline(x)).strip().replace('|', '\\|')
                                     for x in cells])
                    elif c.tag in ('thead', 'tbody', 'tfoot'):
                        walk(c)
                    elif c.tag == 'caption':
                        pass
        walk(k)
        rows = [r for r in rows if any(r)]
        if not rows:
            return []
        width = max(len(r) for r in rows)
        rows = [r + [''] * (width - len(r)) for r in rows]
        out = ['| ' + ' | '.join(rows[0]) + ' |', '|' + '---|' * width]
        out += ['| ' + ' | '.join(r) + ' |' for r in rows[1:]]
        cap = find(k, lambda n: n.tag == 'caption')
        head = [f'*{re.sub(r"\s+", " ", text_of(cap)).strip()}*'] if cap and text_of(cap).strip() else []
        return head + ['\n'.join(out)]


def meta(doc, key):
    for tag in re.findall(r'<meta\b[^>]*>', doc[:60000], re.I):
        k = re.search(r'(?:property|name)\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        v = re.search(r'content\s*=\s*"([^"]*)"', tag, re.I) or re.search(r"content\s*=\s*'([^']*)'", tag, re.I)
        if k and v and k.group(1).lower() == key:
            return re.sub(r'\s+', ' ', html.unescape(v.group(1))).strip()
    return ''


def title_of(doc, url):
    """The page title without the site suffix (same cleaning as scripts/crawl_map.py)."""
    m = re.search(r'<title>([^<]+)</title>', doc)
    t = meta(doc, 'og:title') or (html.unescape(m.group(1)).strip() if m else '')
    t = re.sub(r'\s*(\||:|\u00b7|\u2013|\u2014|-)\s*(Machine Behavior|machinebehavior\.io|Stefan Coetzee)\s*$', '', t)
    t = re.sub(r'(\s*·\s*[^·]+)?\s*·\s*Inside docs$', '', t).strip()
    if not t:
        slug = [x for x in urlparse(url).path.split('/') if x]
        t = slug[-1].replace('-', ' ') if slug else 'Machine Behavior'
    return t


def page_markdown(doc, url):
    tree = parse(doc)
    body = find(tree, lambda n: n.tag == 'body') or tree
    main = find(body, lambda n: n.tag == 'main' or n.attrs.get('role') == 'main') or body
    blocks = Md(url).blocks(main)
    md = '\n\n'.join(blocks)
    md = re.sub(r'\n{3,}', '\n\n', md).strip()
    return md


def sitemap_pages(root):
    sm = (root / 'sitemap.xml').read_text(encoding='utf-8')
    out = []
    for entry in re.findall(r'<url>(.*?)</url>', sm, re.S):
        loc = re.search(r'<loc>([^<]+)</loc>', entry)
        if not loc:
            continue
        url = html.unescape(loc.group(1)).strip()
        if not url.startswith(BASE + '/'):
            continue
        lm = re.search(r'<lastmod>(\d{4}-\d{2}-\d{2})', entry)
        out.append((url, lm.group(1) if lm else ''))
    return out


def page_file(root, url):
    path = urlparse(url).path
    if '..' in path.split('/'):
        return None
    rel = path.lstrip('/')
    f = root / rel / 'index.html' if path.endswith('/') else root / rel
    return f if f.is_file() and f.suffix == '.html' else None


def twin_url(url):
    return url + TWIN if url.endswith('/') else url + '.md'


def twin_path(root, url):
    path = urlparse(url).path
    rel = path.lstrip('/')
    return root / rel / TWIN if path.endswith('/') else root / (rel + '.md')


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def tokens(text):
    """The tokenizer named in TOKENIZER: NFKD, accents dropped, lower case, runs of ASCII letters and digits, 2 to 40 long."""
    t = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()
    return [w for w in re.findall(r'[a-z0-9]+', t) if 2 <= len(w) <= 40]


def passages(md, page_title):
    """Cut a page's markdown at headings, then at paragraphs, into passages of at most PASSAGE_MAX characters."""
    out, heading, buf = [], page_title, []

    def flush():
        text = '\n\n'.join(buf).strip()
        buf.clear()
        if not text:
            return
        while len(text) > PASSAGE_MAX:
            # A paragraph break first, then a line break (table rows, list items), then a sentence end.
            cut = text.rfind('\n\n', 0, PASSAGE_MAX)
            if cut < PASSAGE_MAX // 3:
                cut = text.rfind('\n', 0, PASSAGE_MAX)
            if cut < PASSAGE_MAX // 3:
                cut = text.rfind('. ', 0, PASSAGE_MAX)
                cut = cut + 1 if cut >= PASSAGE_MAX // 3 else PASSAGE_MAX
            out.append((heading, text[:cut].strip()))
            text = text[cut:].strip()
        if text:
            out.append((heading, text))

    for block in md.split('\n\n'):
        m = re.match(r'^(#{1,6}) (.+)$', block)
        if m and '\n' not in block:
            flush()
            heading = m.group(2).strip()
            continue
        if sum(len(b) for b in buf) + len(block) > PASSAGE_MAX:
            flush()
        buf.append(block)
    flush()
    return out


def build(root):
    """{relative path: text} of every file to write, and the page count."""
    pages, files, full = [], {}, []
    for url, lastmod in sitemap_pages(root):
        f = page_file(root, url)
        if not f:
            print(f'  no page file for {url}; skipped', file=sys.stderr)
            continue
        doc = f.read_text(encoding='utf-8', errors='replace')
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', doc, re.I):
            continue
        title = title_of(doc, url)
        md = page_markdown(doc, url)
        md = re.sub(r'(?m)\A((?:(?!^# ).*\n)*?)^# ' + re.escape(title) + r'[ \t]*\n+', r'\1', md + '\n', count=1).strip()
        published = (re.search(r'^(\d{4}-\d{2}-\d{2})', meta(doc, 'article:published_time')) or [None, ''])[1] \
            if meta(doc, 'article:published_time') else ''
        desc = meta(doc, 'description') or meta(doc, 'og:description')
        front = ['---', f'url: {url}', f'title: {yaml_str(title)}']
        if lastmod:
            front.append(f'date: {lastmod}')
        if published:
            front.append(f'published: {published}')
        if desc:
            front.append(f'description: {yaml_str(desc)}')
        front += ['source: machinebehavior.io, Stefan Coetzee', '---', '']
        body = f'# {title}\n\n{md}\n' if md else f'# {title}\n'
        files[str(twin_path(root, url).relative_to(root))] = '\n'.join(front) + body
        head = [f'# {title}', '', f'URL: {url}']
        if lastmod:
            head.append(f'Date: {lastmod}')
        if published:
            head.append(f'Published: {published}')
        head.append(f'Markdown: {twin_url(url)}')
        full.append('\n'.join(head) + '\n\n' + (md + '\n' if md else ''))
        pages.append({'u': url, 't': title, 'd': lastmod, 'p': published, 'm': twin_url(url), 'md': md})

    generated = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    intro = (f'# Machine Behavior: full text\n\n'
             f'> Every public page of {BASE}, a research program by Stefan Coetzee on the behavior of language models '
             f'in their harness, as markdown: one section per page with its URL and date. Cite the page URL. Index: '
             f'{BASE}/llms.txt. Each page also has a markdown twin at its URL plus {TWIN}.\n\n'
             f'Generated: {generated}. Pages: {len(pages)}.\n')
    files[FULL] = intro + '\n\n' + '\n---\n\n'.join(full)

    plist, docs = [], []
    for i, p in enumerate(pages):
        for heading, text in passages(p['md'], p['t']):
            plist.append({'i': i, 'h': heading, 'x': text})
            docs.append(Counter(tokens(f"{p['t']} {heading} {text}")))
    df = Counter()
    for c in docs:
        df.update(c.keys())
    postings = {}
    for pid, c in enumerate(docs):
        for term, tf in c.items():
            postings.setdefault(term, []).extend((pid, tf))
    lengths = [sum(c.values()) for c in docs]
    index = {
        'generated': generated, 'site': BASE, 'source': 'machinebehavior.io, Stefan Coetzee', 'tokenizer': TOKENIZER,
        'pages': [{k: p[k] for k in ('u', 't', 'd', 'p', 'm')} for p in pages],
        'passages': plist,
        'bm25': {'n': len(docs), 'avgdl': round(sum(lengths) / max(1, len(lengths)), 3), 'len': lengths,
                 'postings': dict(sorted(postings.items()))},
    }
    files[PASSAGES] = json.dumps(index, ensure_ascii=False, separators=(',', ':'))
    return files, len(pages)


def scan_private_terms(root, files, term_file, repo=ROOT):
    """Hits of the owner's private term list in the files this script writes; the matcher of the gate's private.terms
    and the allow entries of the repository's .private-terms-allow."""
    sys.path.insert(0, str(ROOT / '.github' / 'actions' / 'conformity'))
    import run as gate  # noqa: E402  (the gate's module; main() runs only as a script)
    path = Path(term_file).expanduser().resolve()
    if not path.is_file():
        return [f'no term list at {path}']
    if any(r == path or r in path.parents for r in (repo.resolve(), root.resolve())):
        return ['the term list is inside the scanned tree; keep it outside every repository']
    terms = gate.pt_terms(path.read_text(encoding='utf-8', errors='replace'))
    if not terms:
        print('private terms: the list has no terms yet; nothing to scan')
        return []
    allow = repo / gate.PT_ALLOW
    entries, no_reason = gate.pt_allow(allow.read_text(encoding='utf-8', errors='replace') if allow.is_file() else '')
    hits = [f'{gate.PT_ALLOW}:{n} allow entry without a reason' for n in no_reason]
    allowed = 0
    for rel, text in sorted(files.items()):
        h, a = gate.pt_scan(rel, text, terms, entries)
        allowed += a
        hits += [f"{x['file']}{':' + str(x['line']) if x['line'] else ''} {x['snippet']}" for x in h]
    print(f'private terms: {len(terms)} terms, {len(files)} files read, {len(hits)} hits, {allowed} allowed by {gate.PT_ALLOW}')
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', default=str(ROOT), help='site directory (default: the repository)')
    ap.add_argument('--private-terms', metavar='FILE', help="the owner's private term list; exit 1 on a hit in the output")
    ap.add_argument('--check-only', action='store_true', help='build and scan in memory, write nothing')
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    files, n = build(root)
    if args.private_terms:
        hits = scan_private_terms(root, files, args.private_terms)
        if hits:
            for h in hits:
                print('  ' + h)
            print('private terms: hits in the generated full text; nothing written', file=sys.stderr)
            return 1
    if not args.check_only:
        for rel, text in files.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')
    size = {k: len(files[k].encode('utf-8')) // 1024 for k in (FULL, PASSAGES)}
    print(f'llms full text: {n} pages, {n} twins, {FULL} {size[FULL]} KB, {PASSAGES} {size[PASSAGES]} KB'
          + (' (not written)' if args.check_only else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
