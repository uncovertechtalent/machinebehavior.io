#!/usr/bin/env python3
"""Tests for scripts/build_llms_full.py: the HTML to markdown pass, the twins, llms-full.txt, the passage index, and the
private-terms scan, on small sites built in a temporary folder. The term lists here are made up. Stdlib only.

    python3 scripts/test_build_llms_full.py

Exits 1 when a case fails.
"""
import contextlib, io, json, sys, tempfile
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_llms_full as b  # noqa: E402

BASE = b.BASE
FAILS = []


def check(name, cond, detail=''):
    if not cond:
        FAILS.append(f'{name}: {detail}')


CHROME = ('<a class="mb-skip" href="#main">Skip to content</a><header class="mb-bar"><a href="/">Machine Behavior</a>'
          '<nav class="mb-nav"><a href="/research/">Research</a></nav></header>'
          '<div class="mb-crumbbar"><nav class="mb-crumbs"><a href="/">Home</a></nav>'
          '<p class="mb-page-meta"><span>Owner X</span><span>Updated 2026-01-01</span></p></div>')
FOOT = '<div class="mb-topics"><a href="/topics/">Topics</a></div><footer class="mb-foot"><a href="/conformity/">Gate</a></footer>'


def page(title, body, head=''):
    return (f'<!doctype html><html><head><title>{title} | Machine Behavior</title>{head}</head>'
            f'<body>{CHROME}<div class="sheet" id="main" role="main">{body}</div>{FOOT}'
            '<script>var leak = "script text";</script></body></html>')


def md(body, url=BASE + '/x/'):
    return b.page_markdown(page('T', body), url)


def test_markdown():
    out = md('<h1>T</h1><p>One <strong>bold</strong> and <em>soft</em> word, <code>a|b</code>.</p>'
             '<h2>Lists</h2><ul><li>first<ul><li>nested</li></ul></li><li>second</li></ul>'
             '<ol start="3"><li>three<li>four</ol>'
             '<pre>line 1\n  line 2</pre><blockquote><p>quoted</p></blockquote>'
             '<table><tr><th>a</th><th>b</th></tr><tr><td>1|2</td><td>3</td></tr></table>'
             '<dl><dt>term</dt><dd>meaning</dd><dt>two</dt><dd>second</dd></dl>'
             '<p><a href="/research/claims/">claims</a><a href="#top">top</a> <a href="https://tychat.io/">tychat</a></p>'
             '<p hidden>secret</p><p aria-hidden="true">decor</p><p><span>Owner</span><span>Me</span></p>')
    for want in ('# T', 'One **bold** and *soft* word, `a|b`.', '## Lists', '- first\n  - nested\n- second',
                 '3. three\n4. four', '```\nline 1\n  line 2\n```', '> quoted', '| a | b |\n|---|---|\n| 1\\|2 | 3 |',
                 '**term**\n: meaning\n\n**two**\n: second', f'[claims]({BASE}/research/claims/) top [tychat](https://tychat.io/)',
                 'Owner Me'):
        check('markdown has ' + want.split('\n')[0], want in out, repr(out))
    for gone in ('Skip to content', 'Research', 'Home', 'Updated 2026', 'Topics', 'Gate', 'script text', 'secret', 'decor'):
        check('markdown drops ' + gone, gone not in out, repr(out))


def test_no_main_element():
    doc = ('<html><body>' + CHROME + '<h1>T</h1><p>Body <em><span>left</span><span>right</span></em>.</p>' + FOOT +
           '</body></html>')
    out = b.page_markdown(doc, BASE + '/x/')
    check('no main: body text kept', '# T' in out and 'Body *left right*.' in out, repr(out))
    for gone in ('Skip to content', 'Research', 'Home', 'Updated 2026', 'Topics', 'Gate'):
        check('no main: chrome dropped ' + gone, gone not in out, repr(out))


def test_forgiving_parse():
    out = md('<p>open para<p>next para<ul><li>a<li>b</ul></p><div>stray</span> end</div>')
    check('left-out end tags', 'open para\n\nnext para' in out and '- a\n- b' in out and 'stray end' in out, repr(out))


def site(tmp, pages, lastmod='2026-10-01'):
    root = Path(tmp)
    urls = []
    for path, html_text in pages.items():
        f = root / path.lstrip('/') / 'index.html' if path.endswith('/') else root / path.lstrip('/')
        if html_text is not None:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(html_text, encoding='utf-8')
        urls.append(f'<url><loc>{BASE}{path}</loc><lastmod>{lastmod}</lastmod></url>')
    urls.append('<url><loc>https://other.example/</loc></url>')
    (root / 'sitemap.xml').write_text('<urlset>' + ''.join(urls) + '</urlset>', encoding='utf-8')
    return root


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
        rc = fn(*a, **k)
    return rc, out.getvalue() + err.getvalue()


def test_build_and_write():
    long_section = ' '.join(f'Sentence {i} about fawn response and stance.' for i in range(120))
    pages = {
        '/': page('Machine Behavior', '<h1>Machine Behavior</h1><p>Home text.</p>'),
        '/research/claims/': page('Claims ledger', '<header><h1>Claims ledger</h1></header><p>Claim one.</p>'
                         f'<h2>Long</h2><p>{long_section}</p><h2>Table</h2><table>'
                         + ''.join(f'<tr><td>row {i}</td><td>cell text. More cell text here.</td></tr>' for i in range(60)) + '</table>',
                         head='<meta property="article:published_time" content="2026-09-01T10:00:00Z">'
                              '<meta name="description" content="Every claim with &quot;receipts&quot;.">'),
        '/hidden/': page('Hidden', '<p>x</p>', head='<meta name="robots" content="noindex">'),
        '/missing/': None,
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = site(tmp, pages)
        rc, log = quiet(b.main, ['--root', str(root), '--check-only'])
        check('check-only exit', rc == 0, log)
        check('check-only writes nothing', not (root / b.FULL).exists() and not (root / 'research' / 'claims' / b.TWIN).exists())
        check('missing page reported', 'no page file for https://machinebehavior.io/missing/' in log, log)
        rc, log = quiet(b.main, ['--root', str(root)])
        check('write exit', rc == 0, log)
        twin = (root / 'research' / 'claims' / b.TWIN).read_text(encoding='utf-8')
        check('twin front matter', twin.startswith('---\nurl: https://machinebehavior.io/research/claims/\ntitle: "Claims ledger"\n'
                                                   'date: 2026-10-01\npublished: 2026-09-01\n'
                                                   'description: "Every claim with \\"receipts\\"."\n'), twin[:300])
        check('twin has one title heading', twin.count('# Claims ledger') == 1, twin[:400])
        check('home twin path', (root / b.TWIN).is_file())
        check('noindex page skipped', not (root / 'hidden' / b.TWIN).exists())
        full = (root / b.FULL).read_text(encoding='utf-8')
        check('full text section', '# Claims ledger\n\nURL: https://machinebehavior.io/research/claims/\nDate: 2026-10-01\n'
                                   'Published: 2026-09-01\nMarkdown: https://machinebehavior.io/research/claims/index.html.md' in full, full[:600])
        check('full text page count', 'Pages: 2.' in full, full[:400])
        idx = json.loads((root / b.PASSAGES).read_text(encoding='utf-8'))
        check('index tokenizer', idx['tokenizer'] == b.TOKENIZER)
        check('index pages', [p['u'] for p in idx['pages']] == [BASE + '/', BASE + '/research/claims/'], idx['pages'])
        check('passage length cap', all(len(p['x']) <= b.PASSAGE_MAX for p in idx['passages']),
              max(len(p['x']) for p in idx['passages']))
        check('long section split', sum(1 for p in idx['passages'] if p['h'] == 'Long') >= 4)
        table = [p['x'] for p in idx['passages'] if p['h'] == 'Table']
        check('long table split at row ends', len(table) >= 2 and all(t.startswith('|') and t.endswith('|') for t in table),
              [t[:40] + ' ... ' + t[-40:] for t in table])
        bm = idx['bm25']
        check('bm25 counts', bm['n'] == len(idx['passages']) == len(bm['len']))
        tf = Counter()
        for term, post in bm['postings'].items():
            for pid, n in zip(post[0::2], post[1::2]):
                tf[pid] += n
        check('postings sum to lengths', [tf[i] for i in range(bm['n'])] == bm['len'])
        check('postings find a word', any(idx['passages'][pid]['h'] == 'Long' for pid in bm['postings']['fawn'][0::2]))


def test_private_terms():
    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
        root = site(tmp, {'/': page('Machine Behavior', '<p>We met Zorblax Industries on Tuesday.</p>'),
                          '/clean/': page('Clean', '<p>Nothing here.</p>')})
        terms = Path(outside) / 'terms.txt'
        terms.write_text('# made-up terms\nzorb = Zorblax Industries\n', encoding='utf-8')
        repo = Path(outside) / 'repo'
        repo.mkdir()
        rc, log = quiet(b.main, ['--root', str(root), '--private-terms', str(terms)])
        check('term hit exits 1', rc == 1, log)
        check('term hit names the label, never the term', 'private term zorb ****' in log and 'Zorblax' not in log, log)
        check('nothing written on a hit', not (root / b.FULL).exists())
        files, _ = b.build(root)
        hits = quiet(b.scan_private_terms, root, files, str(terms), repo)[0]
        check('hit in the twin and the full text', any(h.startswith('index.html.md:') for h in hits)
              and any(h.startswith(b.FULL + ':') for h in hits), hits)
        (repo / '.private-terms-allow').write_text('* zorb made-up fixture term\n', encoding='utf-8')
        hits = quiet(b.scan_private_terms, root, files, str(terms), repo)[0]
        check('allow entry honoured', hits == [], hits)
        inside = root / 'terms.txt'
        inside.write_text('zorb = Zorblax Industries\n', encoding='utf-8')
        hits = quiet(b.scan_private_terms, root, files, str(inside), repo)[0]
        check('term list inside the tree refused', hits and 'inside the scanned tree' in hits[0], hits)
        terms.write_text('# empty\n', encoding='utf-8')
        rc, log = quiet(b.main, ['--root', str(root), '--check-only', '--private-terms', str(terms)])
        check('empty list passes', rc == 0 and 'no terms yet' in log, log)


def main():
    for t in (test_markdown, test_no_main_element, test_forgiving_parse, test_build_and_write, test_private_terms):
        try:
            t()
        except Exception as e:  # a crash is a failed case, the others still run
            FAILS.append(f'{t.__name__}: {type(e).__name__}: {e}')
    for f in FAILS:
        print('FAIL', f)
    print(f'{len(FAILS)} failures' if FAILS else 'all cases pass')
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
