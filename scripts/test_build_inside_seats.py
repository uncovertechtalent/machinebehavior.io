#!/usr/bin/env python3
"""Tests for scripts/build_inside_seats.py (ADR-0034): the seat cards and dashboards on a synthetic seats file and cockpit
document (the chief executive counts every area, another seat its own areas only; blocked before in progress before
open; done and dropped items stay off the lists; decisions waiting are open decisions only; the empty state and the
publisher's placeholder show no invented number; titles are escaped; no panel is hidden in the markup, so the page reads
as a plain list without a script; every id once), the pane grammar and the chief executive's roll-up (ADR-0049: the band
order on a synthetic seat, the signal slot, the roll-up's tiles, pills, links and freshness line, the refusal of a stray
or orphaned part slot, the order on the real page), the tab's pill rule and short code (ADR-0036), a page with the block
missing or twice, --check on the committed files, and --check on a copy with an edited block or a seats file outside its
contract. Stdlib only. The tab script in inside/seat-tabs.js (roles, roving tabindex, arrow keys, hidden panels, the
hash, Back and Forward, a first load under a Grafana hash such as /inside/#dashboards) is tested in
scripts/test_seat_tabs.mjs (node --test).

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

    # 1b. Slots: every panel ends in an empty seat-extra slot, and a rebuild keeps what a slot holds
    ok('every panel has a slot', all(f'<!-- seat-extra:{k} --><!-- /seat-extra:{k} --></section>' in out for k in ('ceo', 'cto', 'publisher')))
    kept = bi.b_seats(doc, ck, {'cto': '<p id="mine">kept</p>'})
    ok('a slot keeps its hand-written content', '<!-- seat-extra:cto --><p id="mine">kept</p><!-- /seat-extra:cto -->' in kept)
    ok('slots() reads it back, the signal slots included', bi.slots(kept) == {'ceo/signal': '', 'ceo': '', 'cto/signal': '', 'cto': '<p id="mine">kept</p>', 'publisher/signal': '', 'publisher': ''}, str(bi.slots(kept)))

    # 1c. The pane grammar (ADR-0049): signal, queue, state, tools in that order on every seat; the signal slot is the one
    # part slot a seat may fill; the chief executive opens with a roll-up of the seats
    ok('the order is signal, queue, state, by band', bi.ORDER == ['rollup', '/signal', 'decisions', 'work', 'pending', 'lens', 'kpis', 'areas'] and bi.PARTS == ('signal',), str(bi.ORDER))
    sig = bi.b_seats(doc, ck, {'cto/signal': '<p id="top">first</p>'})
    seg = panel(sig, 'cto')
    pos = [seg.find(x) for x in ('in-panel-head', '<!-- seat-extra:cto/signal -->', 'Not done, blocked first', 'class="in-lens"', 'class="in-kpis"', '<!-- seat-extra:cto -->')]
    ok('a seat: head, signal slot, work, lens, kpis, then the seat slot', -1 not in pos and pos == sorted(pos), str(pos))
    ok('the signal slot keeps its content and reads back', '<!-- seat-extra:cto/signal --><p id="top">first</p><!-- /seat-extra:cto/signal -->' in sig and bi.slots(sig)['cto/signal'] == '<p id="top">first</p>')
    ok('every seat has an empty signal slot by default', all(f'<!-- seat-extra:{k}/signal --><!-- /seat-extra:{k}/signal -->' in out for k in ('ceo', 'cto', 'publisher')))
    ok('the seat slot is still last', seg.rstrip().endswith('<!-- seat-extra:cto --><!-- /seat-extra:cto --></section>'))
    ok("another seat's slot leaves a seat unchanged", panel(sig, 'ceo') == panel(out, 'ceo') and panel(sig, 'publisher') == panel(out, 'publisher'))
    ceo = panel(out, 'ceo')
    pos = [ceo.find(x) for x in ('in-panel-head', '<ul class="in-rollup">', '<!-- seat-extra:ceo/signal -->', 'Decisions waiting', 'Not done, blocked first', 'class="in-lens"', 'class="in-kpis"', '<ul class="in-areas">', '<!-- seat-extra:ceo -->')]
    ok('ceo: head, roll-up, signal slot, decisions, work, lens, kpis, area tiles, seat slot', -1 not in pos and pos == sorted(pos), str(pos))
    roll = ceo[ceo.index('<ul class="in-rollup">'):ceo.index('</ul>', ceo.index('<ul class="in-rollup">'))]
    blocked_all = sum(x['status'] == 'blocked' for x in ck['items'])
    ok('roll-up: one tile per seat in masthead order, each linking to its dashboard', re.findall(r'<a href="#seat-([a-z]+)">', roll) == ['ceo', 'cto', 'publisher'], roll)
    ok("roll-up: a tile carries the seat's code, title and the tab's state in the pill rule",
       f'<span class="in-rollup-code">CEO</span><span class="in-rollup-title">Chief executive</span><span class="in-pill is-bad">{blocked_all} blocked</span>' in roll
       and '<span class="in-rollup-code">CTO</span><span class="in-rollup-title">Chief technology officer</span><span class="in-pill is-bad">1 blocked</span>' in roll
       and '<span class="in-rollup-code">PUBLISHER</span><span class="in-rollup-title">Publisher</span><span class="in-pill is-ok">clear</span>' in roll, roll)
    ok('roll-up: the counts line names open, in progress, blocked, and done', re.search(r'<span>\d+ open · \d+ in progress · \d+ blocked · \d+ done in 14 days</span></li>', roll) is not None, roll)
    ok('roll-up: a tile with a blocked item is marked', '<li class="is-bad"><a href="#seat-cto">' in roll and '<li><a href="#seat-publisher">' in roll)
    ok('roll-up: the heading says how fresh the counts are', re.search(r'<h3>Seats <span class="in-h-meta">one tile per seat · counts as of \d{4}-\d\d-\d\d \d\d:\d\d UTC</span></h3><ul class="in-rollup">', ceo) is not None)
    ok('roll-up: only on the chief executive', out.count('<ul class="in-rollup">') == 1)
    ok('roll-up: carries no id', ' id=' not in roll)
    src = f'<!-- static:{bi.BLOCK} -->{sig}<!-- /static:{bi.BLOCK} -->'
    ok('a rebuild keeps the signal slot', '<p id="top">first</p>' in bi.put_block(src, doc, ck))
    for name, stray in (('a part slot the grammar has no place for', 'cto/top'), ('a part slot of a seat the file does not have', 'cmo/signal')):
        bad = f'<!-- static:{bi.BLOCK} -->{out}<!-- seat-extra:{stray} --><p>x</p><!-- /seat-extra:{stray} --><!-- /static:{bi.BLOCK} -->'
        try:
            bi.put_block(bad, doc, ck)
            refused = ''
        except SystemExit as e:
            refused = str(e)
        ok(f'{name} holding content stops the build, naming the slot and the way out', stray in refused and 'SEAT/signal' in refused, refused)
    empty = f'<!-- static:{bi.BLOCK} -->{out}<!-- seat-extra:cto/top --><!-- /seat-extra:cto/top --><!-- /static:{bi.BLOCK} -->'
    ok('an empty stray slot is not an error', bi.put_block(empty, doc, ck) is not None)
    page = bi.PAGE.read_text(encoding='utf-8')
    pceo, pcko, pcfo = (page[page.index(f'id="seat-{k}"'):] for k in ('ceo', 'cko', 'cfo'))
    ordered = lambda t, marks: all(x in t for x in marks) and [t.index(x) for x in marks] == sorted(t.index(x) for x in marks)
    ok('page: ceo roll-up, site cards, decisions, lens, kpis, area tiles', ordered(pceo, ('<ul class="in-rollup">', 'id="sites"', 'Decisions waiting', 'class="in-lens"', 'class="in-kpis"', '<ul class="in-areas">')))
    ok('page: cko second brain, search dashboard, work, lens, kpis, living documents, repos', ordered(pcko, ('id="map-embed"', 'id="dash-cko"', 'class="in-empty"', 'class="in-lens"', 'class="in-kpis"', 'id="ld"', 'id="rt"')))
    ok('page: cfo cost dashboards, work, lens, kpis', ordered(pcfo, ('id="dash-cfo"', 'Not done, blocked first', 'class="in-lens"', 'class="in-kpis"')))
    ok('page: the only part slots are signal slots', all(k.split('/')[1] == 'signal' for k in bi.slots(bi.block(page)) if '/' in k), str([k for k in bi.slots(bi.block(page)) if '/' in k]))
    ids2 = re.findall(r' id="([^"]+)"', sig)
    ok('every id once with a signal slot', len(ids2) == len(set(ids2)))

    # 2. Counts: the chief executive over every area, the others over their own areas; done in the window only
    live_all = [x for x in ck['items'] if x['status'] in ('open', 'in_progress', 'blocked')]
    ceo_open = sum(x['status'] == 'open' for x in live_all)
    ceo_blocked = sum(x['status'] == 'blocked' for x in live_all)
    ok('ceo pill leads with blocked, counting every area',
       f'<span class="in-pill is-bad" aria-hidden="true"><span class="in-pill-long">{ceo_blocked} blocked</span><span class="in-pill-short">{ceo_blocked}</span></span>' in card(out, 'ceo'), card(out, 'ceo'))
    ok('ceo screen-reader text gives the full title and state', f'<span class="mb-sr">Chief executive, {ceo_blocked} blocked</span>' in card(out, 'ceo'))
    ok('ceo reads every area, in the panel not on the tab', 'Direction · reads every area' in panel(out, 'ceo') and 'reads every area' not in card(out, 'ceo'))
    ok('cto tab shows only the code and pill, blocked leading',
       '<span class="in-pill is-bad" aria-hidden="true"><span class="in-pill-long">1 blocked</span><span class="in-pill-short">1</span></span>' in card(out, 'cto'), card(out, 'cto'))
    ok('cto code and pill are hidden from a screen reader, which reads the title and state once',
       card(out, 'cto').count('aria-hidden="true"') == 2 and '<span class="mb-sr">Chief technology officer, 1 blocked</span>' in card(out, 'cto'))
    ok('the tab carries no area or count text', 'Delivery' not in card(out, 'cto') and 'done in 14 days' not in card(out, 'cto'))
    ok('a seat with only done items is clear',
       '<span class="in-pill is-ok" aria-hidden="true"><span class="in-pill-long">clear</span><span class="in-pill-short">0</span></span>' in card(out, 'publisher'), card(out, 'publisher'))
    ok('a panel is named by its own heading', 'id="seat-cto" aria-labelledby="seat-cto-h"' in out and 'id="seat-cto-h"' in out)
    ok('no empty class attribute', 'class=""' not in out)

    # 2b. The pill rule (ADR-0036): blocked beats open beats clear; in progress never reaches the tab
    ok('pill: blocked wins', bi.state({'blocked': 3, 'open': 5, 'in_progress': 2}) == ('is-bad', '3 blocked', '3'))
    ok('pill: open when nothing blocked', bi.state({'blocked': 0, 'open': 5, 'in_progress': 2}) == ('is-open', '5 open', '5'))
    ok('pill: clear when nothing blocked or open, even with in progress', bi.state({'blocked': 0, 'open': 0, 'in_progress': 4}) == ('is-ok', 'clear', '0'))
    ok('pill markup carries the full label and the count alone',
       bi.pill({'blocked': 0, 'open': 2, 'in_progress': 0}) == '<span class="in-pill is-open" aria-hidden="true"><span class="in-pill-long">2 open</span><span class="in-pill-short">2</span></span>')

    # 2c. The short code (ADR-0036): PUBLISHER is PUB on a phone; every other code is already short
    ok('publisher tab carries both the long code and PUB', '<span class="in-code-long">PUBLISHER</span><span class="in-code-short">PUB</span>' in card(out, 'publisher'))
    ok('a short code equals the long code for the others', '<span class="in-code-long">CTO</span><span class="in-code-short">CTO</span>' in card(out, 'cto'))
    ok('short_code only shortens the publisher', bi.short_code({'seat': 'publisher'}) == 'PUB' and bi.short_code({'seat': 'cfo'}) == 'CFO')
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
    tiles = ceo[ceo.index('<ul class="in-areas">'):ceo.index('</ul>', ceo.index('<ul class="in-areas">'))]
    ok('ceo has a tile per area', tiles.count('<li') == len(bi.bc.AREA_KEYS), tiles)
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
    one = bi.b_seats(solo, ck)
    metas = re.findall(r'<p class="in-panel-meta">(.*?)</p>', one)
    ok('one holder: no seat line names the holder', len(metas) == 3 and not any('holder' in m or 'A. Holder' in m for m in metas), str(metas))
    ok('one holder: the seat line keeps the areas', metas[0] == 'Direction · reads every area' and metas[1].startswith('Delivery'), str(metas))
    ok('one holder: the name is on the page once', one.count('A. Holder') == 1)
    ok('two holders: each seat line names its holder', '<p class="in-panel-meta">holder A. Holder · Direction · reads every area</p>' in out
       and '<p class="in-panel-meta">holder B. Holder · ' in out)

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
