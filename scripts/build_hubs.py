#!/usr/bin/env python3
"""Build the section and topic hub pages from site/nav.yml.

- /research/: the Research section front page, every research page in the order and groups of site/nav.yml,
  with the description each page gives itself (<meta name="description">).

Each page goes through scripts/site_chrome.py (top bar, breadcrumbs, sidebar, footer) and gets an entry in the
managed sitemap block "hubs" and the llms.txt section "Site sections".

Run from the repo root:  python3 scripts/build_hubs.py
"""
import datetime, html, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inside_chrome, site_chrome  # noqa: E402

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


def main():
    entries = research()
    inside_chrome.sitemap_block('hubs', [(u, d) for u, d, _, _ in entries], source='scripts/build_hubs.py')
    inside_chrome.llms_section('Site sections', '\n'.join(f'- [{t}]({BASE}{u}): {d}' for u, _, t, d in entries))
    print(f'hubs: {len(entries)} pages')


if __name__ == '__main__':
    main()
