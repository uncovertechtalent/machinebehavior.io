#!/usr/bin/env python3
"""Tests for scripts/build_pipeline.py (ADR-0050): the pipeline contract on a synthetic file (every key, form, and limit;
a title or standfirst with a private pattern is refused by name; a pending piece may carry no address; a live piece
needs an https address on one of the house's surfaces and stays within the window; the same slug twice), the block on
the publisher's dashboard (heading with the pending count and the export time, the counts by stage, the order, a live
piece linked and a pending one not, the standfirst and the home line, the escaped title, no due date, the empty state
with no number), and --check on the committed file. Stdlib only.

    python3 scripts/test_build_pipeline.py

Exits 1 when a case fails.
"""
import contextlib, copy, io, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_pipeline as bp  # noqa: E402

GEN = '2026-10-31T08:00:00Z'


def piece(slug, title, stage='drafting', home='open', since='2026-10-20', url=None, standfirst='One line that says what the piece holds.'):
    return {'slug': slug, 'title': title, 'standfirst': standfirst, 'stage': stage, 'home': home, 'url': url, 'since': since}


def base():
    return {'schema': 1, 'generated': GEN, 'source': bp.SOURCE, 'pieces': [
        piece('idea-one', 'An idea', stage='idea', since='2026-10-29'),
        piece('draft-one', 'A draft <b>', stage='drafting', home='machinebehavior.io', since='2026-10-30'),
        piece('review-one', 'In review', stage='review', home='substack', since='2026-10-25'),
        piece('live-one', 'Live piece', stage='live', home='machinebehavior.io', since='2026-10-28',
              url='https://machinebehavior.io/research/experiments/live-one/'),
    ]}


def errs(mut):
    d = base()
    mut(d)
    return bp.check(d)


def main():
    failures = []

    def ok(name, cond, detail=''):
        if not cond:
            failures.append(name)
            print(f'FAIL {name} {detail}')

    # 1. The contract
    ok('the base file passes', bp.check(base()) == [], str(bp.check(base())))
    ok('an empty pipeline passes', bp.check(bp.empty(GEN)) == [])
    cases = [
        ('a key outside the contract', lambda d: d.__setitem__('extra', 1), 'keys outside'),
        ('the wrong schema', lambda d: d.__setitem__('schema', True), 'schema'),
        ('a bad timestamp', lambda d: d.__setitem__('generated', 'yesterday'), 'generated'),
        ('another source', lambda d: d.__setitem__('source', 'somewhere'), 'source'),
        ('too many pieces', lambda d: d.__setitem__('pieces', [piece(f'p-{i}', 't') for i in range(bp.MAX_PIECES + 1)]), 'at most'),
        ('a piece key outside the contract', lambda d: d['pieces'][0].__setitem__('due', '2026-11-01'), 'pieces[0]: keys outside'),
        ('a bad slug', lambda d: d['pieces'][0].__setitem__('slug', 'Not A Slug'), 'pieces[0].slug'),
        ('an empty title', lambda d: d['pieces'][0].__setitem__('title', ''), 'pieces[0].title'),
        ('a long standfirst', lambda d: d['pieces'][0].__setitem__('standfirst', 'x' * (bp.MAX_STANDFIRST + 1)), 'pieces[0].standfirst'),
        ('a hidden character in the standfirst', lambda d: d['pieces'][0].__setitem__('standfirst', 'a⁠b'), 'pieces[0].standfirst'),
        ('a private address in the standfirst', lambda d: d['pieces'][0].__setitem__('standfirst', 'the box at 10.0.0.7'), 'private IPv4'),
        ('a host shorthand in the title', lambda d: d['pieces'][0].__setitem__('title', 'Notes from .77'), 'LAN shorthand'),
        ('the former employer in the title', lambda d: d['pieces'][0].__setitem__('title', 'Inside Makersite'), 'employer'),
        ('a bad stage', lambda d: d['pieces'][0].__setitem__('stage', 'published'), 'pieces[0].stage'),
        ('a bad home', lambda d: d['pieces'][0].__setitem__('home', 'medium'), 'pieces[0].home'),
        ('an address on a pending piece', lambda d: d['pieces'][0].__setitem__('url', 'https://machinebehavior.io/x/'), 'until the piece is live'),
        ('a live piece without an address', lambda d: d['pieces'][3].__setitem__('url', None), 'pieces[3].url'),
        ('a live piece on a foreign host', lambda d: d['pieces'][3].__setitem__('url', 'https://example.org/x/'), 'pieces[3].url'),
        ('a live piece over http', lambda d: d['pieces'][3].__setitem__('url', 'http://machinebehavior.io/x/'), 'pieces[3].url'),
        ('a live piece with a query string', lambda d: d['pieces'][3].__setitem__('url', 'https://machinebehavior.io/x/?a=1'), 'pieces[3].url'),
        ('a live piece whose path holds a private pattern', lambda d: d['pieces'][3].__setitem__('url', 'https://machinebehavior.io/10.0.0.7/'), 'private IPv4'),
        ('a bad since date', lambda d: d['pieces'][0].__setitem__('since', 'soon'), 'pieces[0].since'),
        ('since after generated', lambda d: d['pieces'][0].__setitem__('since', '2026-11-03'), 'after generated'),
        ('a live piece older than the window', lambda d: d['pieces'][3].__setitem__('since', '2026-09-01'), 'older than'),
        ('the same slug twice', lambda d: d['pieces'].append(dict(d['pieces'][0])), 'twice'),
    ]
    for name, mut, word in cases:
        e = errs(mut)
        ok(f'{name} is refused and named', any(word in x for x in e), str(e))
    ok('a pending piece may be old', errs(lambda d: d['pieces'][0].__setitem__('since', '2026-01-01')) == [])
    ok('a Substack address is one of the surfaces', errs(lambda d: d['pieces'][3].__setitem__('url', 'https://someone.substack.com/p/live-one')) == [])

    # 2. The block
    doc = base()
    out = bp.block(doc)
    ok('the heading carries the pending count and the export time', '<h3>Publishing pipeline <span class="in-h-meta">3 pieces pending · as of 2026-10-31 08:00 UTC, the last export</span></h3>' in out, out)
    ok('the counts by stage', all(f'<dt>{k}</dt><dd>{v}</dd>' in out for k, v in (('Idea', 1), ('Drafting', 1), ('In review', 1), (f'Live in {bp.WINDOW_DAYS} days', 1))), out)
    order = [out.index(x) for x in ('In review', 'A draft', 'An idea', 'Live piece')]
    ok('in review, then drafting, then idea, then live', order == sorted(order), str(order))
    two = copy.deepcopy(doc)
    two['pieces'].append(piece('review-two', 'Older review', stage='review', since='2026-10-20'))
    out2 = bp.block(two)
    lst = out2[out2.index('<ul class="in-items'):]  # the list, past the counts (whose labels repeat the stage names)
    ok('within a stage the longest waiting first', lst.index('Older review') < lst.index('>In review<') < lst.index('A draft'), lst)
    ok('a live piece links to its page', '<a href="https://machinebehavior.io/research/experiments/live-one/">Live piece</a>' in out)
    ok('a pending piece is not a link', '>In review<span class="in-item-lede">' in out and 'href' not in out.split('Live piece')[0].split('In review')[1].split('</li>')[0])
    ok('the stage pill', '<span class="in-pill is-warn">in review</span>' in out and '<span class="in-pill is-open">idea</span>' in out and '<span class="in-pill is-ok">live</span>' in out)
    ok('the standfirst and the home line', '<span class="in-item-lede">One line that says what the piece holds.</span><span class="in-item-meta">for Substack</span>' in out, out)
    ok('an open home says so', '<span class="in-item-meta">home open</span>' in out)
    ok('the date is the stage date, never a due date', 'in review since 2026-10-25' in out and 'live since 2026-10-28' in out and 'due' not in out.lower())
    ok('titles are escaped', 'A draft &lt;b&gt;' in out and '<b>' not in out)
    empty = bp.block(bp.empty(GEN))
    ok('the empty state is one line with no number beyond the heading', 'No piece carries a public teaser.' in empty and 'in-kpis' not in empty and '0 pieces pending' in empty)
    ok('ordered() keeps every piece', sorted(x['slug'] for x in bp.ordered(doc['pieces'])) == sorted(x['slug'] for x in doc['pieces']))

    # 2b. The export leaves an aged live piece out and refuses a private pattern in the url
    import export_pipeline as ep
    meta = {'teaser': 'public', 'title': 'T', 'standfirst': 'S line.', 'stage': 'live', 'home': 'machinebehavior.io',
            'url': 'https://machinebehavior.io/x/', 'since': '2026-09-01'}
    ok('export: a live piece older than the window is left out, not refused', ep.to_piece('x', dict(meta), '', '2026-10-31') == (None, ''))
    ok('export: a live piece inside the window is kept', ep.to_piece('x', dict(meta, since='2026-10-20'), '', '2026-10-31')[0]['since'] == '2026-10-20')
    ok('export: an old pending piece is kept', ep.to_piece('x', dict(meta, stage='drafting', url=''), '', '2026-10-31')[0]['stage'] == 'drafting')
    bad_url = ep.to_piece('x', dict(meta, since='2026-10-20', url='https://machinebehavior.io/10.0.0.7/'), '', '2026-10-31')
    ok('export: a private pattern in the url is refused by name', bad_url[0] is None and 'private IPv4' in bad_url[1], str(bad_url))

    # 3. The committed file
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = bp.main(['--check'])
    ok('the committed file passes --check', rc == 0, buf.getvalue().strip())
    with contextlib.redirect_stderr(io.StringIO()):
        ok('an unknown argument is refused', bp.main([]) == 2)
    bad = copy.deepcopy(doc)
    bad['pieces'][0]['standfirst'] = 'see 10.0.0.7'
    ok('load() raises on a bad file', bool(bp.check(bad)))

    print(f'{len(failures)} failures')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
