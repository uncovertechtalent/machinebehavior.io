#!/usr/bin/env python3
"""The one top bar of Inside, and helpers for managed blocks in shared files.

Every Inside page (Inside, docs, services, status, board, map, search and the pages built from YAML) carries the
same top bar. Its HTML comes from bar() below and nowhere else:

- scripts/build_docs.py and scripts/build_inside.py call bar() for the pages they generate;
- hand-written pages hold a marked block that sync() rewrites:
      <!-- inside-bar:begin here=board -->...<!-- inside-bar:end -->
  'here' names the entry shown as the current section.

The public-demo banner (banner()) follows the bar on every Inside page except the map; hand-written pages hold
      <!-- inside-banner:begin --><!-- inside-banner:end -->

Check for drift without writing:  python3 scripts/inside_chrome.py --check   (exit 1 when a page differs)
Rewrite the marked blocks:        python3 scripts/inside_chrome.py
"""
import html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (key, label, href). An entry whose page does not exist yet stays out of the bar until it ships.
NAV = [
    ('docs', 'Docs', '/inside/docs/'),
    ('services', 'Services', '/inside/services/'),
    ('status', 'Status', '/inside/status/'),
    ('board', 'Board', '/inside/board/'),
    ('map', 'Map', '/map/'),
    ('infrastructure', 'Infrastructure', '/inside/#dashboards'),
    ('gate', 'Gate', '/conformity/'),
]

# Hand-written pages with a marked bar block.
SYNCED = ['inside/index.html', 'inside/board/index.html', 'inside/search/index.html', 'inside/tour/index.html', 'map/index.html']

BAR_RE = re.compile(r'<!-- inside-bar:begin here=(\w*) -->.*?<!-- inside-bar:end -->', re.S)
BANNER_RE = re.compile(r'<!-- inside-banner:begin -->.*?<!-- inside-banner:end -->', re.S)
BANNER_PAGES = ['inside/index.html', 'inside/board/index.html', 'inside/search/index.html', 'inside/tour/index.html']


def _live(href):
    path = href.split('#')[0]
    return (ROOT / path.lstrip('/') / 'index.html').exists()


def bar(here=''):
    """The top bar: brand, sections, site link, and the search form (Enter submits to the results page)."""
    links = []
    for key, label, href in NAV:
        if not _live(href):
            continue
        cur = ' aria-current="page"' if key == here else ''
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    brand_cur = ' aria-current="page"' if here == 'inside' else ''
    return ('<header class="ib"><a class="ib-skip" href="#main">Skip to content</a>'
            f'<a class="ib-brand" href="/inside/"{brand_cur}><span class="ib-logo" aria-hidden="true">i</span>Inside</a>'
            '<nav class="ib-nav" aria-label="Inside">' + ''.join(links) +
            '<a class="ib-ext" href="/">machinebehavior.io</a></nav>'
            '<form class="ib-search" role="search" action="/inside/search/" method="get">'
            '<label class="ib-sr" for="ib-q">Search Inside</label>'
            '<input type="search" id="ib-q" name="q" placeholder="Search docs, services, pages" autocomplete="off" '
            'aria-controls="ib-hits" aria-describedby="ib-help">'
            '<span class="ib-sr" id="ib-help">Enter opens the results page. Arrow down moves into the suggestions.</span>'
            '<kbd class="ib-key" aria-hidden="true">/</kbd>'
            '<ul id="ib-hits" class="ib-hits" aria-label="Suggestions"></ul></form></header>')


def banner():
    """The public-demo marker: this intranet is open to read; in production it sits behind single sign-on.
    It also links the founder tour, the five-minute walk through the platform."""
    return ('<aside class="ib-demo" aria-label="About this intranet"><span class="ib-demo-tag">Public demo</span>'
            '<span>This intranet is open to read. In production it sits behind single sign-on, with internal and restricted spaces '
            'granted per person and device.</span><a href="/inside/docs/eng/access-model/">Access model</a>'
            '<a href="/inside/tour/">Five-minute tour</a></aside>')


ASSETS = ('<link rel="stylesheet" href="/inside/bar.css">', '<script src="/inside/bar.js" defer></script>')


def sync(check=False):
    """Rewrite (or, with check=True, compare) the marked bar block in every hand-written page."""
    stale, missing = [], []
    for rel in SYNCED:
        p = ROOT / rel
        if not p.exists():
            continue
        src = p.read_text(encoding='utf-8')
        if not BAR_RE.search(src):
            missing.append(rel)
            continue
        new = BAR_RE.sub(lambda m: f'<!-- inside-bar:begin here={m.group(1)} -->{bar(m.group(1))}<!-- inside-bar:end -->', src)
        if rel in BANNER_PAGES:
            if not BANNER_RE.search(new):
                missing.append(f'{rel}: banner block')
            new = BANNER_RE.sub(lambda m: f'<!-- inside-banner:begin -->{banner()}<!-- inside-banner:end -->', new)
        for asset in ASSETS:
            if asset not in new:
                missing.append(f'{rel}: {asset}')
        if new != src:
            stale.append(rel)
            if not check:
                p.write_text(new, encoding='utf-8')
    return stale, missing


# ---------- managed blocks in sitemap.xml and llms.txt ----------
def sitemap_block(name, urls, base='https://machinebehavior.io'):
    """Replace the block <!-- name:begin -->..<!-- name:end --> in sitemap.xml; urls = [(path, lastmod)]."""
    p = ROOT / 'sitemap.xml'
    sm = p.read_text()
    block = f'  <!-- {name}:begin (scripts/build_inside.py) -->\n'
    block += ''.join(f'  <url><loc>{base}{u}</loc><lastmod>{d}</lastmod></url>\n' for u, d in urls)
    block += f'  <!-- {name}:end -->\n'
    pat = re.compile(rf'  <!-- {re.escape(name)}:begin.*?<!-- {re.escape(name)}:end -->\n', re.S)
    sm = pat.sub(lambda m: block, sm) if pat.search(sm) else sm.replace('</urlset>', block + '</urlset>')
    p.write_text(sm)


def llms_section(heading, body):
    """Replace the section '## heading' in llms.txt (up to the next '## ' or the end), or append it."""
    p = ROOT / 'llms.txt'
    ll = p.read_text()
    sec = f'## {heading}\n\n{body.strip()}\n'
    pat = re.compile(rf'^## {re.escape(heading)}\n.*?(?=^## |\Z)', re.S | re.M)
    if pat.search(ll):
        ll = pat.sub(lambda m: sec + ('\n' if m.end() < len(ll) else ''), ll)
    else:
        ll = ll.rstrip('\n') + '\n\n' + sec
    p.write_text(ll)


def esc(s):
    return html.escape(str(s), quote=True)


if __name__ == '__main__':
    check = '--check' in sys.argv
    stale, missing = sync(check=check)
    for m in missing:
        print('no bar block or asset:', m)
    if check:
        for s in stale:
            print('bar differs from scripts/inside_chrome.py:', s)
        sys.exit(1 if stale or missing else 0)
    print(f'bar synced in {len(stale)} page(s)' + (f'; {len(missing)} problem(s)' if missing else ''))
