#!/usr/bin/env python3
"""Crawl Stefan Coetzee's public sites and write the graph for https://machinebehavior.io/map/.
Usage: python3 scripts/crawl_map.py map/graph.json
Body links and navigation links are kept apart (kind 'body' vs 'nav')."""
import json, os, re, sys, urllib.request, html, datetime
from urllib.parse import urljoin, urlparse

SITES = {'machinebehavior.io': 'mb', 'tychat.io': 'tychat', 'uncovertechtalent.com': 'utt'}
SUBSTACK = 'coetzeestefan.substack.com'
UA = {'User-Agent': 'Mozilla/5.0 (site-map crawler; uncovertechtalent)'}

FAILED = set()
CTYPE = {}     # url -> media type of the response
NONHTML = set()  # site pages that answer with something other than HTML (Hugo tag pages without a template serve RSS)
BLOCK = set(filter(None, os.environ.get('CRAWL_BLOCK_HOSTS', '').split(',')))  # test hook: simulate blocked hosts

def get(u):
    if urlparse(u).netloc in BLOCK:
        FAILED.add(u); print('  blocked (test)', u, file=sys.stderr); return ''
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25)
        CTYPE[u] = r.headers.get_content_type()
        return r.read().decode('utf-8', 'ignore')
    except Exception as e:
        FAILED.add(u); print('  fetch failed', u, e, file=sys.stderr); return ''

def norm(u):
    if '\\' in u or '%5C' in u: return None
    p = urlparse(u)
    if not p.scheme.startswith('http'): return None
    if p.netloc.endswith('substack.com') and re.search(r'/(comments|subscribe|share|about|archive)/?$', p.path): return None
    host = p.netloc.lower().removeprefix('www.').removeprefix('old.')
    parts = [x for x in p.path.split('/') if x]
    if host == 'github.com' and len(parts) >= 2:
        return f'https://github.com/{parts[0]}/{parts[1]}/'
    if host == 'reddit.com' and len(parts) >= 4 and parts[2] == 'comments':
        return f'https://reddit.com/r/{parts[1]}/comments/{parts[3]}/' + (parts[4] + '/' if len(parts) > 4 else '')
    path = re.sub(r'/index\.html$', '/', p.path or '/')
    if not path.endswith('/') and '.' not in path.rsplit('/', 1)[-1]: path += '/'
    return f'https://{host}{path}'

def kind_of(u):
    host = urlparse(u).netloc
    if host in SITES:
        path = urlparse(u).path
        if re.search(r'\.(txt|xml|json|csv|css|js|png|jpg|svg|ico|pdf)/?$', path): return None
        if '/tags/' in path or '/categories/' in path: return 'tag'
        return 'page'
    if host == SUBSTACK and '/p/' in u: return 'substack'
    if host == 'github.com' and len([x for x in urlparse(u).path.split('/') if x]) >= 2: return 'github'
    if host in ('reddit.com', 'redd.it', 'old.reddit.com'): return 'reddit'
    return None

def title_of(doc, u):
    m = re.search(r'<meta property="og:title" content="([^"]+)"', doc) or re.search(r'<title>([^<]+)</title>', doc)
    t = html.unescape(m.group(1)).strip() if m else ''
    t = re.sub(r'\s*(\||:|·|–|—|-)\s*(Machine Behavior|machinebehavior\.io|UncoverTechTalent|Uncover Tech Talent|TYChat|Stefan Coetzee)\s*$', '', t)
    t = re.sub(r'\s+on UncoverTechTalent$', '', t).strip()
    if not t:
        slug = [x for x in urlparse(u).path.split('/') if x]
        t = slug[-1].replace('-', ' ') if slug else urlparse(u).netloc
    return t

def desc_of(doc):
    # og:description first, then meta description; attribute order varies by generator
    found = {}
    for tag in re.findall(r'<meta\b[^>]*>', doc[:60000], re.I):
        key = re.search(r'(?:property|name)\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        val = re.search(r'content\s*=\s*"([^"]*)"', tag, re.I) or re.search(r"content\s*=\s*'([^']*)'", tag, re.I)
        if key and val: found.setdefault(key.group(1).lower(), val.group(1))
    d = html.unescape(found.get('og:description') or found.get('description') or '').strip()
    d = re.sub(r'\s+', ' ', d)
    d = re.sub(r'^Originally published at \S+\s*', '', d)  # Substack cross-posts open with the canonical note
    return d if len(d) <= 300 else d[:297].rsplit(' ', 1)[0] + '…'

def strip_chrome(doc):
    body = re.sub(r'<(nav|footer)\b.*?</\1>', ' ', doc, flags=re.S | re.I)
    # drop a <header> only when it is site chrome (it held the nav); keep hero headers with content
    def hdr(m):
        return ' ' if re.search(r'class=["\']?site-header|<nav', m.group(0), re.I) or len(re.sub(r'<[^>]+>', '', m.group(0)).split()) < 12 else m.group(0)
    return re.sub(r'<header\b.*?</header>', hdr, body, flags=re.S | re.I)

def links(doc, base):
    out = []
    for a in re.findall(r'href=["\']?([^"\' >]+)', doc):
        if a.startswith(('#', 'mailto:', 'javascript:')): continue
        n = norm(urljoin(base, html.unescape(a)))
        if n: out.append(n)
    return out

nodes, edges = {}, {}
def add_node(u, kind, title=None, site=None):
    if u not in nodes:
        host = urlparse(u).netloc
        nodes[u] = {'id': u, 'title': title or '', 'kind': kind, 'site': site or SITES.get(host, kind)}
    elif title and not nodes[u]['title']:
        nodes[u]['title'] = title

def add_edge(a, b, k):
    if a == b: return
    key = (a, b)
    if key not in edges or edges[key] == 'nav' and k == 'body': edges[key] = k

# 1. pages from sitemaps
pages = []
DATES = {}  # url -> YYYY-MM-DD, best known: the page's own date, else sitemap lastmod, else the Substack post date
for host in SITES:
    sm = get(f'https://{host}/sitemap.xml')
    for entry in re.findall(r'<url>(.*?)</url>', sm, re.S):
        loc = re.search(r'<loc>([^<]+)</loc>', entry)
        n = norm(html.unescape(loc.group(1))) if loc else None
        if n and kind_of(n):
            pages.append(n)
            lm = re.search(r'<lastmod>(\d{4}-\d{2}-\d{2})', entry)
            if lm: DATES[n] = lm.group(1)
# 2. substack posts from the archive API
OUT = sys.argv[1] if len(sys.argv) > 1 else 'graph.json'
try:
    PREV = json.load(open(OUT))
except Exception:
    PREV = {'nodes': [], 'links': []}
subs = []
try:
    arch = json.loads(get(f'https://{SUBSTACK}/api/v1/archive?sort=new&limit=50') or '[]')
    for p in arch:
        u = norm(p.get('canonical_url', ''))
        if u:
            subs.append(u); add_node(u, 'substack', p.get('title'), 'substack')
            if (p.get('post_date') or '')[:10]: DATES[u] = p['post_date'][:10]
except Exception as e:
    print('substack archive failed', e, file=sys.stderr)
if not subs:  # RSS fallback
    rss = get(f'https://{SUBSTACK}/feed')
    for item in re.findall(r'<item>(.*?)</item>', rss, re.S):
        lm = re.search(r'<link>([^<]+)</link>', item); tm = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item, re.S)
        u = norm(lm.group(1).strip()) if lm else None
        if u:
            subs.append(u); add_node(u, 'substack', html.unescape(tm.group(1)).strip() if tm else None, 'substack')
            pd = re.search(r'<pubDate>([^<]+)</pubDate>', item)
            if pd:
                try: DATES[u] = datetime.datetime.strptime(pd.group(1).strip()[:16], '%a, %d %b %Y').strftime('%Y-%m-%d')
                except ValueError: pass
if not subs:  # last resort: posts known from the previous snapshot
    for n in PREV['nodes']:
        if n.get('kind') == 'substack' and '/p/' in n['id']:
            subs.append(n['id']); add_node(n['id'], 'substack', n.get('title'), 'substack')
    print(f'substack listing unreachable, carried forward {len(subs)} posts', file=sys.stderr)

for u in sorted(set(pages)) + subs:
    doc = get(u)
    if not doc: continue
    if CTYPE.get(u) not in ('text/html', 'application/xhtml+xml'):
        NONHTML.add(u); print('  not html, dropped', CTYPE.get(u), u, file=sys.stderr); continue
    k = kind_of(u) or 'substack'
    add_node(u, k, title_of(doc, u))
    if desc_of(doc): nodes[u]['desc'] = desc_of(doc)
    own = re.search(r'<meta[^>]+article:published_time[^>]+content="(\d{4}-\d{2}-\d{2})', doc) or \
        (k == 'page' and re.search(r'<time[^>]*datetime=["\']?(\d{4}-\d{2}-\d{2})', doc)) or \
        (k == 'page' and re.search(r'class="[^"]*(?:eyebrow|kicker|dateline)[^"]*"[^>]*>[^<]{0,120}?(\d{4}-\d{2}-\d{2})', doc))  # machinebehavior.io headers
    if own: DATES[u] = own.group(1)
    body = strip_chrome(doc)
    if k == 'substack':  # only the post body counts on Substack
        m = re.search(r'<div class="available-content".*', doc, re.S)
        body = m.group(0) if m else ''
    body_links = set(links(body, u))
    nav_links = set(links(doc, u)) - body_links
    for tgt, lk in [(t, 'body') for t in body_links] + [(t, 'nav') for t in nav_links]:
        tk = kind_of(tgt)
        if not tk: continue
        if urlparse(tgt).path in ('/tags/', '/categories/'): lk = 'nav'  # "all tags" back-links are navigation
        if k == 'tag' and urlparse(tgt).path == '/blog/': lk = 'nav'      # so is "all posts" on a tag page
        if tk in ('github', 'reddit'):
            add_node(tgt, tk, None, tk)
        elif tk in ('page', 'tag') and tgt not in nodes:
            add_node(tgt, tk)
        elif tk == 'substack':
            add_node(tgt, 'substack', None, 'substack')
        add_edge(u, tgt, lk)

# carry forward: for any page we could not fetch, keep its outgoing links from the previous snapshot
prev_nodes = {n['id']: n for n in PREV['nodes']}
carried = 0
for l in PREV['links']:
    if l['source'] in FAILED and l['source'] in nodes:
        if l['target'] not in nodes and l['target'] in prev_nodes:
            pn = prev_nodes[l['target']]; add_node(pn['id'], pn['kind'], pn.get('title'), pn.get('site'))
        if (l['source'], l['target']) not in edges:
            edges[(l['source'], l['target'])] = l['kind']; carried += 1
for u in FAILED:
    if u in nodes and not nodes[u]['title'] and u in prev_nodes:
        nodes[u]['title'] = prev_nodes[u].get('title', '')

# repo descriptions for the GitHub satellites (the preview card shows them)
for n in nodes.values():
    if n['kind'] == 'github' and 'desc' not in n:
        d = desc_of(get(n['id']))
        d = re.sub(r'\s*-\s*' + re.escape('/'.join(urlparse(n['id']).path.strip('/').split('/')[:2])) + r'$', '', d)
        d = re.sub(r'^Contribute to \S+ development by creating an account on GitHub\.?$', '', d)
        if d: n['desc'] = d
# any node still without a description keeps the one from the previous snapshot
for n in nodes.values():
    old = re.sub(r'^Originally published at \S+\s*', '', prev_nodes.get(n['id'], {}).get('desc', ''))
    if 'desc' not in n and old and n['id'] in FAILED:
        n['desc'] = old
if carried:
    print(f'carried forward {carried} links from {len(FAILED)} unreachable pages', file=sys.stderr)

# a node a reader cannot open as a page does not belong on the map
for u in NONHTML:
    nodes.pop(u, None)
for key in [k for k in edges if k[0] in NONHTML or k[1] in NONHTML]:
    del edges[key]
if NONHTML:
    print(f'dropped {len(NONHTML)} non-html pages', file=sys.stderr)

# dates: what this crawl found, else the previous snapshot's
for n in nodes.values():
    d = DATES.get(n['id']) or prev_nodes.get(n['id'], {}).get('date')
    if d: n['date'] = d

# a description shared by three or more pages is the site default, not a summary of the page
from collections import Counter as _C
_shared = {d for d, c in _C(n.get('desc') for n in nodes.values() if n.get('desc')).items() if c >= 3}
for n in nodes.values():
    if n.get('desc') in _shared: del n['desc']

# titles for satellites without one
for n in nodes.values():
    if not n['title']:
        parts = [x for x in urlparse(n['id']).path.split('/') if x]
        if n['kind'] == 'github': n['title'] = '/'.join(parts[:2])
        elif n['kind'] == 'reddit':
            if len(parts) >= 5: n['title'] = 'r/' + parts[1] + ': ' + parts[4].replace('_', ' ')
            elif len(parts) >= 2 and parts[0] == 'r': n['title'] = 'r/' + parts[1]
            else: n['title'] = 'Reddit post'
        elif n['kind'] == 'tag': n['title'] = '#' + parts[-1]
        else: n['title'] = (parts[-1] if parts else urlparse(n['id']).netloc).replace('-', ' ')

# drop listing pages with no content links (empty tag pages)
has_body = {a for (a, b), k in edges.items() if k == 'body'} | {b for (a, b), k in edges.items() if k == 'body'}
for u in [u for u, n in nodes.items() if n['kind'] == 'tag' and u not in has_body]:
    del nodes[u]
edges = {(a, b): k for (a, b), k in edges.items() if a in nodes and b in nodes}

out = {
    'generated': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'),
    'nodes': list(nodes.values()),
    'links': [{'source': a, 'target': b, 'kind': k} for (a, b), k in edges.items()],
}
os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
json.dump(out, open(OUT, 'w'), indent=1)
from collections import Counter
print('nodes', len(out['nodes']), Counter(n['kind'] for n in out['nodes']))
print('links', len(out['links']), Counter(l['kind'] for l in out['links']))
