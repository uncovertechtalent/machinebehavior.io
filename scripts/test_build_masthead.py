#!/usr/bin/env python3
"""Tests for scripts/build_masthead.py (#99): the contract check on variants of a small data file (a key outside the
contract at each level, a key twice, a JSON constant, a seat twice or out of order, an unknown seat or area, a list
in place of a string, an empty or trailing-newline holder, markup, a hidden character or a URL in free text, a bundle
that is not a slug, a gate with an unknown where, a bad date), the page blocks (the house name comes from the one
field, every seat renders with its areas, machinery and gates, text is escaped), a page with a block missing or twice,
--check on the committed files, and --check on a copy with a changed block or a bad file. Stdlib only.

    python3 scripts/test_build_masthead.py

Exits 1 when a case fails.
"""
import contextlib, copy, io, json, os, shutil, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_masthead as bm  # noqa: E402


def seat(key, title, areas, holder='A. Holder'):
    return {'seat': key, 'title': title, 'holder': holder, 'areas': areas, 'bundle': None,
            'machinery': [{'name': 'direction', 'what': 'The weekly review.'}],
            'gates': [{'check': 'direction.review-memo', 'where': 'module', 'what': 'Every memo has a date.'}]}


def base():
    return {'schema': 1, 'updated': '2026-10-16', 'house': 'Example House', 'source': 'A test file.',
            'where': {'module': 'ships with the module', 'site gate': 'runs here'},
            'seats': [seat('ceo', 'Chief executive', ['direction']),
                      seat('cto', 'Chief technology officer', ['delivery', 'operations'], holder='B. Holder')]}


def variant(fn):
    d = copy.deepcopy(base())
    fn(d)
    return d


# name: (change, the text every error list for it must contain)
FAILS = {
    'top-level key outside the contract': (lambda d: d.__setitem__('owner', 'x'), 'keys outside the contract: owner'),
    'top-level key missing': (lambda d: d.pop('source'), 'missing keys: source'),
    'wrong schema': (lambda d: d.__setitem__('schema', 2), 'schema: 2'),
    'schema true': (lambda d: d.__setitem__('schema', True), 'schema: True'),
    'bad updated': (lambda d: d.__setitem__('updated', '2026-13-01'), 'updated: not a real date'),
    'updated not a date': (lambda d: d.__setitem__('updated', 'yesterday'), 'updated: not a date'),
    'empty house': (lambda d: d.__setitem__('house', ' '), 'house: not a non-empty string'),
    'house with angle brackets': (lambda d: d.__setitem__('house', 'Ex<b>'), 'house: angle brackets'),
    'where empty': (lambda d: d.__setitem__('where', {}), 'where: not an object'),
    'where value with URL': (lambda d: d['where'].__setitem__('module', 'see https://example.test/'), 'where.module: URL in free text'),
    'seat key outside the contract': (lambda d: d['seats'][0].__setitem__('motivators', []), 'seats[0]: keys outside the contract: motivators'),
    'seat key missing': (lambda d: d['seats'][0].pop('gates'), 'seats[0]: missing keys: gates'),
    'unknown seat': (lambda d: d['seats'][0].__setitem__('seat', 'coo'), "seats[0].seat: 'coo' is not a seat"),
    'seat as a list': (lambda d: d['seats'][0].__setitem__('seat', ['ceo']), 'seats[0].seat:'),
    'seat listed twice': (lambda d: d['seats'].append(seat('ceo', 'Again', ['direction'])), 'seats: a seat is listed twice'),
    'seats out of masthead order': (lambda d: d['seats'].reverse(), 'seats: not in masthead order'),
    'unknown area': (lambda d: d['seats'][0].__setitem__('areas', ['sales']), 'seats[0].areas:'),
    'area twice': (lambda d: d['seats'][0].__setitem__('areas', ['direction', 'direction']), 'seats[0].areas:'),
    'area not a string': (lambda d: d['seats'][0].__setitem__('areas', [['direction']]), 'seats[0].areas:'),
    'no areas': (lambda d: d['seats'][0].__setitem__('areas', []), 'seats[0].areas:'),
    'empty holder': (lambda d: d['seats'][0].__setitem__('holder', ''), 'seats[0].holder: not a non-empty string'),
    'holder with trailing newline': (lambda d: d['seats'][0].__setitem__('holder', 'A. Holder\n'), 'seats[0].holder:'),
    'holder with markup': (lambda d: d['seats'][0].__setitem__('holder', '<img src=x>'), 'seats[0].holder: angle brackets'),
    'bundle not a slug': (lambda d: d['seats'][0].__setitem__('bundle', 'CEO Bundle'), 'seats[0].bundle: null or a slug'),
    'machinery row key outside the contract': (lambda d: d['seats'][0]['machinery'][0].__setitem__('url', 'x'), 'seats[0].machinery[0]: keys outside the contract: url'),
    'machinery empty': (lambda d: d['seats'][0].__setitem__('machinery', []), 'seats[0].machinery: not a non-empty list'),
    'gate without where': (lambda d: d['seats'][0]['gates'][0].pop('where'), 'seats[0].gates[0]: missing keys: where'),
    'gate with unknown where': (lambda d: d['seats'][0]['gates'][0].__setitem__('where', 'somewhere'), 'seats[0].gates[0].where: not a key of the where map'),
    'gate what too long': (lambda d: d['seats'][0]['gates'][0].__setitem__('what', 'x' * (bm.MAX_WHAT + 1)), f'longer than {bm.MAX_WHAT} characters'),
    'gate what with angle brackets': (lambda d: d['seats'][0]['gates'][0].__setitem__('what', 'a <script> b'), 'seats[0].gates[0].what: angle brackets'),
    'gate what with a bidi override': (lambda d: d['seats'][0]['gates'][0].__setitem__('what', 'a ‮ b'), 'control or format character'),
    'gate what with a URL': (lambda d: d['seats'][0]['gates'][0].__setitem__('what', 'see https://example.test/'), 'URL in free text'),
    'too many gates': (lambda d: d['seats'][0].__setitem__('gates', [{'check': 'c', 'where': 'module', 'what': 'w'}] * (bm.MAX_LIST + 1)), f'more than {bm.MAX_LIST} rows'),
}


def main():
    failures = []

    def ok(name, cond, detail=''):
        print(('ok   ' if cond else 'FAIL ') + name + (f': {detail}' if detail and not cond else ''))
        if not cond:
            failures.append(name)

    # 1. The contract
    ok('base conforms', bm.check(base()) == [], str(bm.check(base())))
    for name, (fn, text) in FAILS.items():
        errs = bm.check(variant(fn))
        ok('refused: ' + name, any(text in e for e in errs), f'errors {errs}')
    for name, text in (('key twice', '{"schema": 1, "schema": 1}'), ('NaN', '{"schema": NaN}'), ('Infinity', '[Infinity]')):
        try:
            bm.parse(text)
            ok('parse refuses ' + name, False)
        except bm.ContractError:
            ok('parse refuses ' + name, True)

    # 2. The blocks
    doc = base()
    lede = bm.b_lede(doc)
    ok('lede names the house from the one field', 'Example House is a publishing house' in lede)
    ok('lede names the C-suit', 'The seats together are the C-suit' in lede)
    ok('lede counts seats and holders', '2 seats, 2 holders today: A. Holder and B. Holder' in lede)
    one = variant(lambda d: d['seats'].pop())
    ok('lede with one holder', '1 seat, 1 holder today: A. Holder.' in bm.b_lede(one))
    ok('eyebrow names the house and the date', bm.b_eyebrow(doc) == 'Inside · Masthead · Example House · 2026-10-16')
    ok('where map renders', '<dt>site gate</dt><dd>runs here</dd>' in bm.b_where(doc))
    seats = bm.b_seats(doc)
    ok('every seat renders', all(f'id="{s}"' in seats for s in ('ceo', 'cto')))
    ok('areas link to the cockpit', '<a href="/inside/cockpit/#operations">Operations</a>' in seats)
    ok('machinery renders', '<b>direction</b> The weekly review.' in seats)
    ok('gates render with where', '<code>direction.review-memo</code> <span class="mh-where-chip">module</span> Every memo has a date.' in seats)
    ok('bundle none yet', 'bundle: <span class="mono">none yet</span>' in seats)
    esc = variant(lambda d: d['seats'][0]['machinery'][0].__setitem__('what', 'Tags & "names"'))
    ok('free text is escaped', 'Tags &amp; &quot;names&quot;' in bm.b_seats(esc))

    # 3. put_blocks needs every block exactly once
    page = '<p><!-- static:masthead-eyebrow --><!-- /static:masthead-eyebrow --></p>'
    try:
        bm.put_blocks(page, doc)
        ok('a page without a block stops the build', False)
    except SystemExit as e:
        ok('a page without a block stops the build', 'masthead-lede' in str(e))
    twice = ''.join(f'<!-- static:{n} --><!-- /static:{n} -->' for n in bm.BLOCKS) + '<!-- static:masthead-lede --><!-- /static:masthead-lede -->'
    try:
        bm.put_blocks(twice, doc)
        ok('a page with a block twice stops the build', False)
    except SystemExit as e:
        ok('a page with a block twice stops the build', '2 <!-- static:masthead-lede -->' in str(e))

    # 4. The committed files
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = bm.main(['--check'])
    ok('committed seats.json and page pass --check', rc == 0, buf.getvalue().strip())
    committed = json.loads(bm.DATA.read_text(encoding='utf-8'))
    ok('committed file has every seat in order', [s['seat'] for s in committed['seats']] == bm.SEATS)
    ok('an unknown argument is refused', bm.main(['--chek']) == 2)

    # 5. --check on a copy with a changed block, and with a bad file
    tmp = Path(tempfile.mkdtemp())
    try:
        for rel in (bm.PAGE_REL, 'inside/masthead/seats.json', 'sitemap.xml'):
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(bm.ROOT / rel, tmp / rel)
        saved = (bm.PAGE, bm.SITEMAP, bm.DATA)
        bm.PAGE, bm.SITEMAP, bm.DATA = tmp / bm.PAGE_REL, tmp / 'sitemap.xml', tmp / 'inside/masthead/seats.json'
        try:
            src = bm.PAGE.read_text(encoding='utf-8')
            bm.PAGE.write_text(src.replace('<!-- static:masthead-lede -->', '<!-- static:masthead-lede -->edited ', 1), encoding='utf-8')
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                rc = bm.main(['--check'])
            ok('--check fails on an edited block', rc == 1 and 'masthead-lede' in buf.getvalue(), buf.getvalue().strip())
            bm.PAGE.write_text(src, encoding='utf-8')
            bad = json.loads(bm.DATA.read_text(encoding='utf-8'))
            bad['seats'][0]['holder'] = '<b>x</b>'
            bm.DATA.write_text(json.dumps(bad), encoding='utf-8')
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                rc = bm.main(['--check'])
            ok('--check fails on a file outside the contract', rc == 1 and 'angle brackets' in buf.getvalue(), buf.getvalue().strip())
            bm.DATA.write_text(json.dumps(committed), encoding='utf-8')
            sm = bm.SITEMAP.read_text(encoding='utf-8')
            bm.SITEMAP.write_text(bm.SITEMAP_RX.sub(lambda m: m.group(1) + '2020-01-01' + m.group(3), sm, count=1), encoding='utf-8')
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                rc = bm.main(['--check'])
            ok('--check fails on a stale sitemap date', rc == 1 and 'lastmod' in buf.getvalue(), buf.getvalue().strip())
        finally:
            bm.PAGE, bm.SITEMAP, bm.DATA = saved
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'{len(failures)} failures')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
