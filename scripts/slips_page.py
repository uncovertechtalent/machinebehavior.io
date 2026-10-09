#!/usr/bin/env python3
"""Build slips/index.html from slips/log.csv. Run from the repo root: python3 scripts/slips_page.py"""
import csv, collections, html, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_chrome  # top bar, breadcrumbs, sidebar and footer from site/nav.yml

rows = list(csv.DictReader(open('slips/log.csv')))
by_rel = collections.Counter(r['relation'] for r in rows)
by_dev = collections.Counter(r['device'].split(':')[0].split('(')[0].strip() for r in rows)
# cut labels like "(Reddit cut)" and version suffixes like " v1.1" count toward their parent piece
parent = lambda p: re.sub(r'\s+v\d+(\.\d+)*$', '', p.split(' (')[0]).strip()
is_draft = lambda p: 'unpublished' in p
pieces = collections.Counter(parent(r['piece']) for r in rows if not is_draft(r['piece']))
drafts = collections.Counter(parent(r['piece']) for r in rows if is_draft(r['piece']))
esc = lambda s: html.escape(s, quote=False)

def table(counter, label):
    out = [f'    <tr><th>{label}</th><th>slips</th></tr>']
    for k, v in counter.most_common():
        out.append(f'    <tr><td>{esc(k)}</td><td class="n">{v}</td></tr>')
    return '\n'.join(out)

log = ['    <tr><th>date</th><th>piece</th><th>device</th><th>before</th><th>after</th><th>caught by</th><th>relation</th><th>reader catch</th></tr>']
for r in rows:
    log.append('    <tr>' + ''.join(f'<td>{esc(r[k])}</td>' for k in
               ('date', 'piece', 'device', 'before', 'after', 'caught_by', 'relation', 'reader_catch')) + '</tr>')

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Slips: Machine Behavior</title>
<meta name="description" content="A running log of register and stance slips caught while drafting the published pieces, with who caught each one: the drafting model itself, another session, a mechanical hook, a human, or a reader.">
<link rel="canonical" href="https://machinebehavior.io/slips/">
<link rel="stylesheet" href="/style.css">
<meta name="mb-source" content="scripts/slips_page.py">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛋️</text></svg>">
<meta property="og:type" content="website">
<meta property="og:url" content="https://machinebehavior.io/slips/">
<meta property="og:site_name" content="Machine Behavior">
<meta property="og:title" content="Slips">
<meta property="og:description" content="A running log of register and stance slips caught while drafting the published pieces, with who caught each one: the drafting model itself, another session, a mechanical hook, a human, or a reader.">
<meta property="og:image" content="https://machinebehavior.io/map/home-graph.png">
<meta property="og:image:width" content="1640">
<meta property="og:image:height" content="820">
<meta property="og:image:alt" content="Map of the Work: a graph of Stefan Coetzee&#x27;s published pages, posts, repos and threads, coloured by site, with the links between them.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://machinebehavior.io/map/home-graph.png">
</head>
<body>
<div class="sheet">

  <header>
    <div class="eyebrow">Running log · generated from slips/log.csv</div>
    <h1>Slips caught while drafting</h1>
    <p class="subtitle">Every published piece is drafted with a language model. This page logs the register and stance slips caught before publication, and who caught each one.</p>
  </header>

  <p class="thesis"><strong>What counts.</strong> A slip is a device or a claim that did not belong in the text: a speech device in silent-read writing (see <a class="mono" href="https://uncovertechtalent.com/blog/where-did-claudish-come-from/">An RCA on Claudish</a>), an overclaim, a staged contrast, an undisclosed change. Factual corrections after publication go in each piece's changelog and errata, not here.</p>

  <p class="thesis"><strong>Why the relation column matters.</strong> The program's claim is that self-audit catches little and outside scrutiny catches the rest (<a class="mono" href="/claims/">claims ledger</a>). Here "self" means the same model session that wrote the text, "other session" means a separate model session reviewing it, "human" means Stefan, and "reader" means someone who read the published piece. "hook" means a mechanical rule at the output boundary blocked the text before anyone read it (added 2026-10-03, with the first such row).</p>

  <p class="thesis"><strong>The reader-catch column</strong> (added 2026-10-03) records what a reader of the published piece caught in that passage, and when. Most cells are empty. Since the same date the log also holds register slips that a reader caught after publication: those rows have the relation "reader", and the published text stays as published.</p>

  <p class="thesis"><strong>Unpublished drafts</strong> (added 2026-10-03). The log also holds slips caught in drafts that are not published. Their piece label ends in "(vault, unpublished)", so a reader can tell them from the published pieces, and the headline count lists them separately.</p>

  <p class="thesis"><strong>Limits.</strong> The log only holds slips someone caught; what nobody caught is not in it. It starts on 2026-09-29, and earlier pieces have no entries. The "self" count includes checks the model ran because a written procedure told it to (the mode-leak pass), so it measures a procedure followed, not unprompted self-correction. {len(rows)} slips across {len(pieces)} published pieces and {len(drafts)} unpublished draft set so far.</p>

  <h2>By who caught it</h2>
  <div class="tablewrap">
  <table>
{table(by_rel, 'relation')}
  </table>
  </div>

  <h2>By device</h2>
  <div class="tablewrap">
  <table>
{table(by_dev, 'device')}
  </table>
  </div>

  <h2>The log</h2>
  <div class="tablewrap">
  <table>
{chr(10).join(log)}
  </table>
  </div>

  <p class="thesis">Data: <a class="mono" href="https://github.com/uncovertechtalent/machinebehavior.io/blob/main/slips/log.csv">slips/log.csv</a>. Page built by <a class="mono" href="https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/slips_page.py">scripts/slips_page.py</a>.</p>
</div>
</body>
</html>
'''
open('slips/index.html', 'w').write(site_chrome.apply(page, 'slips/index.html'))
print(f'slips/index.html: {len(rows)} rows, {dict(by_rel)}')
