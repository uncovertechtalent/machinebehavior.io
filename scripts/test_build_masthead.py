#!/usr/bin/env python3
"""Tests for scripts/build_masthead.py (#99): the contract check on variants of a small data file (a key outside the
contract at each level, a seat twice or out of order, an unknown seat or area, an empty holder, angle brackets in free
text, a bundle that is not a slug), the page blocks (the house name comes from the one field, every seat renders with
its areas, machinery and gates, text is escaped), and --check on the committed files. Stdlib only.

    python3 scripts/test_build_masthead.py

Exits 1 when a case fails.
"""
import contextlib, copy, io, json, sys
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_masthead as bm  # noqa: E402


def seat(key, title, areas, holder='A. Holder'):
    return {'seat': key, 'title': title, 'holder': holder, 'areas': areas, 'bundle': None,
            'machinery': [{'name': 'direction', 'what': 'The weekly review.'}],
            'gates': [{'check': 'direction.review-memo', 'what': 'Every memo has a date.'}]}


def base():
    return {'schema': 1, 'house': 'Example House', 'source': 'A test file.',
            'seats': [seat('ceo', 'Chief executive', ['direction']),
                      seat('cto', 'Chief technology officer', ['delivery', 'operations'], holder='B. Holder')]}


def variant(fn):
    d = copy.deepcopy(base())
    fn(d)
    return d


FAILS = {
    'top-level key outside the contract': lambda d: d.__setitem__('owner', 'x'),
    'top-level key missing': lambda d: d.pop('source'),
    'wrong schema': lambda d: d.__setitem__('schema', 2),
    'empty house': lambda d: d.__setitem__('house', ' '),
    'house with angle brackets': lambda d: d.__setitem__('house', 'Ex<b>'),
    'seat key outside the contract': lambda d: d['seats'][0].__setitem__('motivators', []),
    'seat key missing': lambda d: d['seats'][0].pop('gates'),
    'unknown seat': lambda d: d['seats'][0].__setitem__('seat', 'coo'),
    'seat listed twice': lambda d: d['seats'].append(seat('ceo', 'Again', ['direction'])),
    'seats out of masthead order': lambda d: d['seats'].reverse(),
    'unknown area': lambda d: d['seats'][0].__setitem__('areas', ['sales']),
    'area twice': lambda d: d['seats'][0].__setitem__('areas', ['direction', 'direction']),
    'no areas': lambda d: d['seats'][0].__setitem__('areas', []),
    'empty holder': lambda d: d['seats'][0].__setitem__('holder', ''),
    'holder with markup': lambda d: d['seats'][0].__setitem__('holder', '<img src=x>'),
    'bundle not a slug': lambda d: d['seats'][0].__setitem__('bundle', 'CEO Bundle'),
    'machinery row key outside the contract': lambda d: d['seats'][0]['machinery'][0].__setitem__('url', 'x'),
    'machinery empty': lambda d: d['seats'][0].__setitem__('machinery', []),
    'gate what too long': lambda d: d['seats'][0]['gates'][0].__setitem__('what', 'x' * (bm.MAX_WHAT + 1)),
    'gate what with angle brackets': lambda d: d['seats'][0]['gates'][0].__setitem__('what', 'a <script> b'),
    'too many gates': lambda d: d['seats'][0].__setitem__('gates', [{'check': 'c', 'what': 'w'}] * (bm.MAX_LIST + 1)),
}

failures = []


def ok(name, cond, detail=''):
    print(('ok   ' if cond else 'FAIL ') + name + (f': {detail}' if detail and not cond else ''))
    if not cond:
        failures.append(name)


# 1. The contract
ok('base conforms', bm.check(base()) == [], str(bm.check(base())))
for name, fn in FAILS.items():
    errs = bm.check(variant(fn))
    ok('refused: ' + name, bool(errs))

# 2. The blocks
doc = base()
lede = bm.b_lede(doc)
ok('lede names the house from the one field', 'Example House is a publishing house' in lede)
ok('lede counts seats and holders', '2 seats, 2 holders today: A. Holder and B. Holder' in lede)
one = variant(lambda d: d['seats'].pop())
ok('lede with one holder', '1 seat, 1 holder today: A. Holder.' in bm.b_lede(one))
ok('eyebrow names the house', bm.b_eyebrow(doc) == 'Inside · Masthead · Example House')
seats = bm.b_seats(doc)
ok('every seat renders', all(f'id="{s}"' in seats for s in ('ceo', 'cto')))
ok('areas link to the cockpit', '<a href="/inside/cockpit/#operations">Operations</a>' in seats)
ok('machinery and gates render', '<b>direction</b> The weekly review.' in seats and '<code>direction.review-memo</code> Every memo has a date.' in seats)
ok('bundle none yet', 'bundle: <span class="mono">none yet</span>' in seats)
esc = variant(lambda d: d['seats'][0]['machinery'][0].__setitem__('what', 'Tags & "names"'))
ok('free text is escaped', 'Tags &amp; &quot;names&quot;' in bm.b_seats(esc))

# 3. put_blocks needs every block
page = '<p><!-- static:masthead-eyebrow --><!-- /static:masthead-eyebrow --></p>'
try:
    bm.put_blocks(page, doc)
    ok('a page without a block stops the build', False)
except SystemExit as e:
    ok('a page without a block stops the build', 'masthead-lede' in str(e))

# 4. The committed files
buf = io.StringIO()
with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
    rc = bm.main(['--check'])
ok('committed seats.json and page pass --check', rc == 0, buf.getvalue().strip())
committed = json.loads(bm.DATA.read_text(encoding='utf-8'))
ok('committed file has every seat in order', [s['seat'] for s in committed['seats']] == bm.SEATS)

print(f'{len(failures)} failures')
sys.exit(1 if failures else 0)
