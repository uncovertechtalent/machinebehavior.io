#!/usr/bin/env python3
"""Tests for scripts/build_ledger.py (ADR-0050): the ledger contract on a synthetic file (every key, form, and limit; a
title with a private pattern is refused by name; a done record outside the window is refused; the same id twice), the
four lanes on the board page (order, counts, newest first, the empty lane, a row's id, escaped title, area, kind and
date, the freshness line), --check on the committed files, and --check on a copy with an edited block or a file
outside its contract. Stdlib only.

    python3 scripts/test_build_ledger.py

Exits 1 when a case fails.
"""
import contextlib, copy, io, json, re, shutil, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ledger as bl  # noqa: E402

GEN = '2026-10-31T08:00:00Z'


def rec(id, title, area='delivery', status='open', kind='action', created='2026-10-20', closed=None):
    return {'id': id, 'title': title, 'area': area, 'kind': kind, 'status': status, 'created': created, 'closed': closed}


def base():
    return {'schema': 1, 'generated': GEN, 'source': bl.SOURCE, 'window_days': bl.WINDOW_DAYS, 'items': [
        rec('vault-aaa1', 'Open one', created='2026-10-28'),
        rec('vault-aaa2', 'Open two <b>', created='2026-10-29'),
        rec('vault-bbb1', 'Blocked one', area='operations', status='blocked', kind='decision', created='2026-10-10'),
        rec('vault-ccc1', 'Progress one', area='ai', status='in_progress', kind=None, created='2026-10-25'),
        rec('vault-ddd1', 'Done old', area='knowledge', status='done', kind='finding', created='2026-10-01', closed='2026-10-05'),
        rec('vault-ddd2.3', 'Done new', area='knowledge', status='done', created='2026-10-20', closed='2026-10-30'),
    ]}


def errs(mut):
    d = base()
    mut(d)
    return bl.check(d)


def main():
    failures = []

    def ok(name, cond, detail=''):
        if not cond:
            failures.append(name)
            print(f'FAIL {name} {detail}')

    # 1. The contract
    ok('the base file passes', bl.check(base()) == [], str(bl.check(base())))
    ok('an empty ledger passes', bl.check(bl.empty(GEN)) == [])
    cases = [
        ('a key outside the contract', lambda d: d.__setitem__('extra', 1), 'keys outside'),
        ('a missing key', lambda d: d.pop('window_days'), 'missing keys'),
        ('the wrong schema', lambda d: d.__setitem__('schema', 2), 'schema'),
        ('a bad timestamp', lambda d: d.__setitem__('generated', '2026-10-31'), 'generated'),
        ('another source', lambda d: d.__setitem__('source', 'somewhere'), 'source'),
        ('another window', lambda d: d.__setitem__('window_days', 7), 'window_days'),
        ('too many items', lambda d: d.__setitem__('items', [rec(f'vault-{i:04x}', 't') for i in range(bl.MAX_ITEMS + 1)]), 'at most'),
        ('an item key outside the contract', lambda d: d['items'][0].__setitem__('url', 'x'), 'items[0]: keys outside'),
        ('a bad id', lambda d: d['items'][0].__setitem__('id', 'issue-12'), 'items[0].id'),
        ('an empty title', lambda d: d['items'][0].__setitem__('title', '  '), 'items[0].title'),
        ('a padded title', lambda d: d['items'][0].__setitem__('title', ' x'), 'items[0].title'),
        ('a long title', lambda d: d['items'][0].__setitem__('title', 'x' * (bl.MAX_TITLE + 1)), 'items[0].title'),
        ('a hidden character', lambda d: d['items'][0].__setitem__('title', 'a​b'), 'items[0].title'),
        ('a private address', lambda d: d['items'][0].__setitem__('title', 'box at 10.0.0.9 down'), 'private IPv4'),
        ('a host shorthand', lambda d: d['items'][0].__setitem__('title', 'rsyslog on .77'), 'LAN shorthand'),
        ('an e-mail address', lambda d: d['items'][0].__setitem__('title', 'mail someone@example.org'), 'e-mail'),
        ('the former employer', lambda d: d['items'][0].__setitem__('title', 'Makersite numbers'), 'employer'),
        ('a home path', lambda d: d['items'][0].__setitem__('title', 'fix ~/vault/x'), 'home path'),
        ('a placeholder word', lambda d: d['items'][0].__setitem__('title', 'TODO later'), 'placeholder'),
        ('a bad area', lambda d: d['items'][0].__setitem__('area', 'sales'), 'items[0].area'),
        ('a bad kind', lambda d: d['items'][0].__setitem__('kind', 'lead'), 'items[0].kind'),
        ('a bad status', lambda d: d['items'][0].__setitem__('status', 'dropped'), 'items[0].status'),
        ('a bad created date', lambda d: d['items'][0].__setitem__('created', '20 Oct'), 'items[0].created'),
        ('closed set on an open record', lambda d: d['items'][0].__setitem__('closed', '2026-10-21'), 'items[0].closed'),
        ('closed missing on a done record', lambda d: d['items'][5].__setitem__('closed', None), 'items[5].closed'),
        ('closed before created', lambda d: d['items'][5].__setitem__('closed', '2026-10-19'), 'before created'),
        ('closed older than the window', lambda d: d['items'][4].__setitem__('closed', '2026-09-30'), 'older than'),
        ('closed after generated', lambda d: d['items'][5].__setitem__('closed', '2026-11-02'), 'after generated'),
        ('the same id twice', lambda d: d['items'].append(dict(d['items'][0])), 'twice'),
    ]
    for name, mut, word in cases:
        e = errs(mut)
        ok(f'{name} is refused and named', any(word in x for x in e), str(e))
    ok('a violation names the record and the fix', any('fix the record at its source' in x for x in errs(cases[13][1])))
    ok('a refusal says which pattern', any('(LAN shorthand)' in x for x in errs(cases[14][1])), str(errs(cases[14][1])))

    # 2. The block
    doc = base()
    titles = bl.bm.area_titles()
    out = bl.block_html(doc, titles)
    lanes = re.findall(r'<h2>([^<]+) <span class="mb-n">(\d+)</span></h2>', out)
    ok('four lanes in order with their counts', lanes == [('In progress', '1'), ('Blocked', '1'), ('Open', '2'), (f'Done in {bl.WINDOW_DAYS} days', '2')], str(lanes))
    open_lane = out[out.index('<h2>Open'):out.index(f'<h2>Done')]
    ok('open lane: the longest waiting first', open_lane.index('Open one') < open_lane.index('Open two'))
    done_lane = out[out.index('<h2>Done'):]
    ok('done lane: newest closed first', done_lane.index('Done new') < done_lane.index('Done old'))
    ok('a row carries the id, the title, the area, the kind and the date',
       '<li><span class="mb-ledger-id">vault-bbb1</span><span class="mb-ledger-title">Blocked one</span>'
       f'<span class="mb-links-meta">{titles["operations"]} · decision · opened 2026-10-10</span></li>' in out, out)
    ok('a done row says closed', 'closed 2026-10-30</span>' in out)
    ok('a null kind renders no kind', f'{titles["ai"]} · opened 2026-10-25' in out)
    ok('titles are escaped', 'Open two &lt;b&gt;' in out and '<b>' not in out)
    ok('no row links anywhere', '<a ' not in out.split('<p class="note">')[0])
    ok('the freshness line counts and names the export', f'6 records as of 2026-10-31 08:00 UTC, the last export: 1 in progress, 1 blocked, 2 open, 2 done in {bl.WINDOW_DAYS} days.' in out, out)
    only_open = copy.deepcopy(doc)
    only_open['items'] = [x for x in only_open['items'] if x['status'] == 'open']
    e_out = bl.block_html(only_open, titles)
    ok('an empty lane says none', e_out.count('<li class="mb-ledger-empty">none</li>') == 3, e_out)
    ok('a lane is labelled for a screen reader', 'aria-label="Open, 2 records"' in out)
    ok('one id per record, none on the lanes', ' id=' not in out)

    # 3. The committed files
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = bl.main(['--check'])
    ok('committed files pass --check', rc == 0, buf.getvalue().strip())
    with contextlib.redirect_stderr(io.StringIO()):
        ok('an unknown argument is refused', bl.main(['--chek']) == 2)

    # 4. --check on a copy with an edited block, and with a file outside its contract
    tmp = Path(tempfile.mkdtemp())
    saved = (bl.PAGE, bl.DATA)
    try:
        for rel in (bl.PAGE_REL, 'inside/board/ledger.json'):
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(bl.ROOT / rel, tmp / rel)
        bl.PAGE, bl.DATA = tmp / bl.PAGE_REL, tmp / 'inside/board/ledger.json'
        src = bl.PAGE.read_text(encoding='utf-8')
        bl.PAGE.write_text(src.replace(f'<!-- static:{bl.BLOCK} -->', f'<!-- static:{bl.BLOCK} -->edited ', 1), encoding='utf-8')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = bl.main(['--check'])
        ok('--check fails on an edited block', rc == 1 and 'differs' in buf.getvalue(), buf.getvalue().strip())
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = bl.main([])
        ok('the build restores the block', rc == 0 and bl.PAGE.read_text(encoding='utf-8') == src)
        bad = json.loads(bl.DATA.read_text(encoding='utf-8'))
        bad['items'].insert(0, rec('vault-zzz9', 'host .77 down'))
        bl.DATA.write_text(json.dumps(bad), encoding='utf-8')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = bl.main(['--check'])
        ok('--check fails on a file outside the contract, naming the pattern', rc == 1 and 'ledger contract' in buf.getvalue() and 'LAN shorthand' in buf.getvalue(), buf.getvalue().strip())
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = bl.main([])
        ok('the build writes nothing on a bad file', rc == 1 and bl.PAGE.read_text(encoding='utf-8') == src)
    finally:
        bl.PAGE, bl.DATA = saved
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'{len(failures)} failures')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
