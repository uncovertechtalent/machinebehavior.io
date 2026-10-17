#!/usr/bin/env python3
"""Tests for scripts/build_inside_seats.py (ADR-0034): the seat cards and dashboards on a synthetic seats file and cockpit
document (the chief executive counts every area, another seat its own areas only; blocked before in progress before
open; done and dropped items stay off the lists; decisions waiting are open decisions only; the empty state and the
publisher's placeholder show no invented number; titles are escaped; no panel is hidden in the markup, so the page reads
as a plain list without a script; every id once), a page with the block missing or twice, --check on the committed
files, and --check on a copy with an edited block or a seats file outside its contract. Stdlib only. The tab script in
inside/index.html (roles, arrow keys, hidden panels, the hash, Back and Forward, a first load under a Grafana hash such
as /inside/#dashboards) has no automated test; it is checked by hand in a browser.

    python3 scripts/test_build_inside_seats.py

Exits 1 when a case fails.
"""
import contextlib, copy, io, json, re, shutil, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_inside_seats as bi  # noqa: E402
import test_build_cockpit as tc  # noqa: E402
import test_build_masthead as tm  # noqa: E402


def seats():
    """The masthead tests' file (ceo on direction, cto on delivery and operations) plus a publisher on ai."""
    d = tm.base()
    d['seats'].append(tm.seat('publisher', 'Publisher', ['ai']))
    return d


def cockpit():
    """The cockpit tests' document plus a blocked and an open decision, so ordering and the decisions show."""
    d = tc.base()
    d['items'] += [tc.item(tc.MB, 7, 'operations', 'blocked', kind='decision', title='Pick a pager', created='2026-10-12'),
                   tc.item(tc.MB, 8, 'money', kind='decision', title='Pick a ledger <now>', created='2026-10-02')]
    return d


def panel(html, key):
    start = html.index(f'id="seat-{key}"')
    end = html.find('<section class="in-panel"', start + 1)
    return html[start:end if end > 0 else len(html)]


def card(html, key):
    start = html.index(f'id="in-tab-{key}"')
    return html[start:html.index('</li>', start)]


def main():
    failures = []

    def ok(name, cond, detail=''):
        if not cond:
            failures.append(name)
            print(f'FAIL {name} {detail}')

    doc, ck = seats(), cockpit()
    out = bi.b_seats(doc, ck)

    # 1. Cards: one per seat in masthead order, each a link to its dashboard
    keys = re.findall(r'id="in-tab-([a-z]+)" href="#seat-\1" aria-controls="seat-\1"', out)
    ok('one card per seat in order, linked to its dashboard', keys == ['ceo', 'cto', 'publisher'], str(keys))
    ok('every dashboard follows', [k for k in ('ceo', 'cto', 'publisher') if f'<section class="in-panel" id="seat-{k}"' in out] == ['ceo', 'cto', 'publisher'])
    ok('no panel is hidden in the markup (plain list without a script)', ' hidden' not in out and 'role=' not in out)
    ids = re.findall(r' id="([^"]+)"', out)
    ok('every id once', len(ids) == len(set(ids)), str([i for i in ids if ids.count(i) > 1]))

    # 2. Counts: the chief executive over every area, the others over their own areas; done in the window only
    live_all = [x for x in ck['items'] if x['status'] in ('open', 'in_progress', 'blocked')]
    ceo_open = sum(x['status'] == 'open' for x in live_all)
    ceo_blocked = sum(x['status'] == 'blocked' for x in live_all)
    ok('ceo card counts every area', f'{ceo_open} open · {ceo_blocked} blocked · 1 done in 14 days' in card(out, 'ceo'), card(out, 'ceo'))
    ok('ceo card says it reads every area', 'Direction · reads every area' in card(out, 'ceo'))
    ok('cto card counts delivery and operations only', '1 open · 1 blocked · 0 done in 14 days' in card(out, 'cto'), card(out, 'cto'))
    ok('blocked leads the pill', '<span class="in-pill is-bad">1 blocked</span>' in card(out, 'cto'))
    ok('a seat with only done items is clear', '<span class="in-pill is-ok">clear</span>' in card(out, 'publisher'))
    cto = panel(out, 'cto')
    ok('kpis render the four counts', all(f'<dt>{k}</dt>' in cto for k in ('Open', 'In progress', 'Blocked', 'Done in 14 days')))
    ok('a nonzero blocked count is marked', '<div class="is-bad"><dt>Blocked</dt><dd>1</dd></div>' in cto)

    # 3. Items: not done, blocked first, own areas only, linked, escaped
    ok('cto lists its own areas only', 'Pick a pager' in cto and 'Item 41' in cto and 'Item 83' not in cto and 'Item 93' not in cto)
    ok('blocked before open', cto.index('Pick a pager') < cto.index('Item 41'))
    ok('dropped items stay off', 'Item 46' not in out[out.index('id="seat-cto"'):])
    ok('items link to their issue', 'href="https://github.com/uncovertechtalent/machinebehavior.io/issues/41"' in cto)
    ok('the meta names repo, number, type, and area', 'machinebehavior.io#7 · issue · Operations · decision' in cto)
    ceo = panel(out, 'ceo')
    ok('ceo lists its own area', 'id="seat-ceo"' in ceo and 'Item 93' in ceo and '<span class="in-pill is-warn">in progress</span>' in ceo)
    ok('ceo has a tile per area', ceo.count('<li class="') - ceo.count('<li class="in-item"') == len(bi.bc.AREA_KEYS))
    dec = ceo[ceo.index('Decisions waiting'):ceo.index('Not done')]
    ok('decisions waiting: open decisions only, blocked first', dec.index('Pick a pager') < dec.index('Pick a ledger') and 'Item 83' not in dec)
    ok('titles are escaped', 'Pick a ledger &lt;now&gt;' in dec and '<now>' not in out)
    no_dec = copy.deepcopy(ck)
    no_dec['items'] = [x for x in no_dec['items'] if x['kind'] != 'decision']
    ok('no decision: says so', 'No open decision with an area label.' in panel(bi.b_seats(doc, no_dec), 'ceo'))

    # 4. Empty state and placeholder: no invented number
    pub = panel(out, 'publisher')
    ok('empty state counts the done items', "Nothing open in this seat's areas (AI). 1 item done there in the last 14 days." in pub, pub)
    pending = pub[pub.index('in-pending'):pub.index('</div>', pub.index('in-pending'))]
    ok('publisher placeholder is labelled', 'Publishing pipeline · not wired yet' in pending)
    ok('publisher placeholder shows no number', not re.search(r'\d', re.sub(r'<[^>]+>', '', pending)))
    ok('only the publisher has a placeholder', out.count('in-pending') == 1)
    ok('lens questions render', '<li>Does it move the goal?</li>' in ceo)
    ok('two holders: the line counts them', 'One holder in every seat today' not in out and '2 holders across 3 seats today.' in out)
    solo = copy.deepcopy(doc)
    for s in solo['seats']:
        s['holder'] = 'A. Holder'
    ok('one holder line', 'One holder in every seat today: A. Holder.' in bi.b_seats(solo, ck))

    # 5. put_block needs the block exactly once
    for name, page in (('missing', '<main></main>'), ('twice', f'<!-- static:{bi.BLOCK} --><!-- /static:{bi.BLOCK} -->' * 2)):
        try:
            bi.put_block(page, doc, ck)
            ok(f'a page with the block {name} stops the build', False)
        except SystemExit as e:
            ok(f'a page with the block {name} stops the build', bi.BLOCK in str(e))

    # 6. The committed files
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = bi.main(['--check'])
    ok('committed files pass --check', rc == 0, buf.getvalue().strip())
    with contextlib.redirect_stderr(io.StringIO()):
        ok('an unknown argument is refused', bi.main(['--chek']) == 2)

    # 7. --check on a copy with an edited block, and with a seats file outside its contract
    tmp = Path(tempfile.mkdtemp())
    saved = (bi.PAGE, bi.bm.DATA)
    try:
        for rel in (bi.PAGE_REL, 'inside/masthead/seats.json'):
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(bi.ROOT / rel, tmp / rel)
        bi.PAGE, bi.bm.DATA = tmp / bi.PAGE_REL, tmp / 'inside/masthead/seats.json'
        src = bi.PAGE.read_text(encoding='utf-8')
        bi.PAGE.write_text(src.replace(f'<!-- static:{bi.BLOCK} -->', f'<!-- static:{bi.BLOCK} -->edited ', 1), encoding='utf-8')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = bi.main(['--check'])
        ok('--check fails on an edited block', rc == 1 and 'differs' in buf.getvalue(), buf.getvalue().strip())
        bi.PAGE.write_text(src, encoding='utf-8')
        bad = json.loads(bi.bm.DATA.read_text(encoding='utf-8'))
        bad['seats'][0]['areas'] = ['sales']
        bi.bm.DATA.write_text(json.dumps(bad), encoding='utf-8')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = bi.main(['--check'])
        ok('--check fails on a seats file outside the contract', rc == 1 and 'seats contract' in buf.getvalue(), buf.getvalue().strip())
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = bi.main([])
        ok('the build writes nothing on a bad seats file', rc == 1 and bi.PAGE.read_text(encoding='utf-8') == src)
    finally:
        bi.PAGE, bi.bm.DATA = saved
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'{len(failures)} failures')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
