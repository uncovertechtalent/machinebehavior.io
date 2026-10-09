#!/usr/bin/env python3
"""Helpers for managed blocks in shared files: sitemap.xml and llms.txt.

The top bar, the demo banner, the breadcrumbs and the footer of every page moved to scripts/site_chrome.py, which
writes them from site/nav.yml. This file keeps the block helpers the builds share.

    python3 scripts/inside_chrome.py --check   same as python3 scripts/site_chrome.py --check
"""
import html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ---------- managed blocks in sitemap.xml and llms.txt ----------
def sitemap_block(name, urls, base='https://machinebehavior.io', source='scripts/build_inside.py'):
    """Replace the block <!-- name:begin -->..<!-- name:end --> in sitemap.xml; urls = [(path, lastmod)]."""
    p = ROOT / 'sitemap.xml'
    sm = p.read_text()
    block = f'  <!-- {name}:begin ({source}) -->\n'
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
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import site_chrome
    sys.exit(site_chrome.main(sys.argv[1:]))
