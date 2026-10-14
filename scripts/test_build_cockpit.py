#!/usr/bin/env python3
"""Tests for scripts/build_cockpit.py: the snapshot contract check (ADR-0031), on variants of the sample snapshot
scripts/fixtures/cockpit-snapshot.json (a key outside the contract at each level, a key twice, free text in a fixed
field, counts of the wrong form, totals that are not the sums, public items of another owner or with a foreign URL),
and the page blocks it writes. Stdlib only; no network.

    python3 scripts/test_build_cockpit.py

Exits 1 when a case fails.
"""
import contextlib, copy, io, json, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cockpit as bc  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / 'fixtures' / 'cockpit-snapshot.json'
PR = {'repo': 'uncovertechtalent/tychat.io', 'kind': 'pr', 'title': 'Pin the gate & bump', 'url': 'https://github.com/uncovertechtalent/tychat.io/pull/7', 'state': 'open'}
ISSUE = {'repo': 'uncovertechtalent/machinebehavior.io', 'kind': 'issue', 'title': 'A site issue', 'url': 'https://github.com/uncovertechtalent/machinebehavior.io/issues/12', 'state': 'open'}


def base():
    return json.loads(FIXTURE.read_text(encoding='utf-8'))


def variant(fn):
    d = copy.deepcopy(base())
    fn(d)
    return d


def fails(doc, text):
    """True when the check reports a violation that contains text."""
    return any(text in e for e in bc.check(doc))


def parse_fails(text):
    try:
        bc.parse(text)
    except bc.ContractError:
        return True
    return False


def stops(fn):
    with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
        try:
            return fn()
        except SystemExit as e:
            return 'stop' if e.code not in (0, None) else 0


def main():
    failures = []

    def case(name, got, want=True):
        print(('ok   ' if got == want else 'FAIL ') + name)
        if got != want:
            failures.append(f'{name}: got {got!r}, want {want!r}')

    def setitem(path, value):
        def fn(d):
            o = d
            for k in path[:-1]:
                o = o[k]
            o[path[-1]] = value
        return fn

    # the sample passes, and so does a real source with public items
    case('sample snapshot meets the contract', bc.check(base()), [])
    real = variant(setitem(['source'], 'beads-desk@64f5afb'))
    real['public_items'] = [PR, ISSUE]
    case('real source with a pull request and a site issue meets the contract', bc.check(real), [])

    # keys outside the contract, at every level
    case('top level: an extra key', fails(variant(setitem(['notes'], 'x')), 'keys outside the contract'))
    case('top level: a missing key', fails(variant(lambda d: d.pop('trend')), 'missing keys'))
    case('area: an extra key with text', fails(variant(setitem(['areas', 0, 'title'], 'a bead title')), 'areas[0]: keys outside the contract'))
    case('totals: an extra key', fails(variant(setitem(['totals', 'deferred'], 3)), 'totals: keys outside the contract'))
    case('trend day: an extra key', fails(variant(setitem(['trend', 0, 'note'], 'x')), 'trend[0]: keys outside the contract'))
    item_extra = dict(PR, author='someone')
    case('public item: an extra key', fails(variant(setitem(['public_items'], [item_extra])), 'public_items[0]: keys outside the contract'))
    case('parse: a key twice in one object', parse_fails('{"schema": 1, "schema": 1}'))
    case('parse: NaN', parse_fails('{"schema": NaN}'))
    case('parse: not JSON', parse_fails('{schema: 1}'))
    case('parse: larger than the limit', parse_fails('"' + 'x' * (bc.MAX_BYTES + 1) + '"'))

    # fixed forms: no free text outside the titles of public items
    case('area name: free text', fails(variant(setitem(['areas', 1, 'name'], 'Delivery work')), "areas[1].name: must be 'Delivery'"))
    case('area key: an area outside the eight', fails(variant(setitem(['areas', 7, 'key'], 'personal')), 'not one of the eight areas'))
    case('areas: one area twice', fails(variant(setitem(['areas', 7], copy.deepcopy(base()['areas'][0]))), 'each of the eight areas exactly once'))
    case('areas: seven areas', fails(variant(lambda d: d['areas'].pop()), 'each of the eight areas exactly once'))
    case('source: free text', fails(variant(setitem(['source'], 'my laptop')), 'source:'))
    case('source: a commit too short', fails(variant(setitem(['source'], 'beads-desk@abc12')), 'source:'))
    case('generated: not UTC', fails(variant(setitem(['generated'], '2026-10-14T14:00:00+02:00')), 'generated:'))
    case('generated: not a real time', fails(variant(setitem(['generated'], '2026-13-40T25:00:00Z')), 'generated:'))
    case('schema: 2', fails(variant(setitem(['schema'], 2)), 'schema:'))
    case('schema: true', fails(variant(setitem(['schema'], True)), 'schema:'))

    # counts
    for bad in ('4', 4.0, -1, True, None):
        case(f'count: {bad!r} is not a count', fails(variant(setitem(['areas', 1, 'open'], bad)), 'areas[1].open: not a count'))
    case('totals: not the sum of the eight areas', fails(variant(setitem(['totals', 'open'], 99)), 'is not the sum of the eight areas'))
    case('trend: dates out of order', fails(variant(lambda d: d['trend'].reverse()), 'not after the day before it'))
    case('trend: not a date', fails(variant(setitem(['trend', 0, 'date'], 'Monday')), 'trend[0].date'))

    # public items
    def items(*xs):
        return variant(setitem(['public_items'], list(xs)))
    case('item: owner outside PUBLIC_OWNERS', fails(items(dict(PR, repo='someone/repo', url='https://github.com/someone/repo/pull/7')), 'is not in PUBLIC_OWNERS'))
    case('item: URL of another repository', fails(items(dict(PR, url='https://github.com/uncovertechtalent/other/pull/7')), '.url:'))
    case('item: URL off GitHub', fails(items(dict(PR, url='https://example.test/uncovertechtalent/tychat.io/pull/7')), '.url:'))
    case('item: issue with a pull request URL', fails(items(dict(PR, kind='issue')), '.url:'))
    case('item: kind outside the contract', fails(items(dict(PR, kind='commit')), '.kind:'))
    case('item: state outside the contract', fails(items(dict(PR, state='draft')), '.state:'))
    case('item: title with markup', fails(items(dict(PR, title='<b>x</b>')), '.title:'))
    case('item: title with a line break', fails(items(dict(PR, title='one\ntwo')), '.title:'))
    case('item: title too long', fails(items(dict(PR, title='x' * (bc.MAX_TITLE + 1))), '.title:'))
    case('item: empty title', fails(items(dict(PR, title='  ')), '.title:'))
    case('item: the same URL twice', fails(items(PR, dict(PR)), 'listed twice'))

    # the blocks
    case('lede: the sample says so', 'sample figures from the test file' in bc.b_lede(base()))
    case('lede: a real snapshot does not', 'sample' not in bc.b_lede(real))
    case('eyebrow: the snapshot time in UTC', bc.b_eyebrow(real), 'Counts only · snapshot 2026-10-14 14:00 UTC')
    case('totals: closed in 7 days counts from the snapshot date', 'since 2026-10-07' in bc.b_totals(base()))
    out = bc.b_items(real)
    case('items: a pull request is listed, its title escaped', 'Pin the gate &amp; bump</a>' in out and 'pull request 7' in out)
    case('items: an issue of this site is counted and links the board', 'A site issue' not in out and '1 open issue' in out and 'href="/inside/board/"' in out)
    closed = copy.deepcopy(real)
    closed['public_items'] = [dict(PR, state='merged')]
    case('items: closed and merged items are left out', 'No open public pull request or issue' in bc.b_items(closed))
    long_trend = variant(lambda d: d['trend'].extend({'date': f'2026-10-{n}', 'open': 40, 'closed': 1} for n in range(15, 21)))
    case('trend: the last 14 days of a longer trend', bc.b_trend(long_trend).count('<li>') == 14 and '2026-10-20:' in bc.b_trend(long_trend))
    case('trend: none in the snapshot', 'has no trend' in bc.b_trend(variant(setitem(['trend'], []))))
    areas = bc.b_areas(base())
    case('areas: every area in page order', [areas.find(f'id="{k}"') for k, _, _ in bc.AREAS] == sorted(areas.find(f'id="{k}"') for k, _, _ in bc.AREAS))
    case('areas: delivery links its plugin pages', all(f'href="/cto-powersuit/{p}/"' in areas.split('id="delivery"')[1].split('<section')[0] for p in ('sdlc', 'gate', 'docs')))
    case('areas: security uses the powersuit title', '>Security and risk</h3>' in areas)
    case('areas: knowledge links the knowledge layer', 'href="/cto-powersuit/vestige/"' in areas.split('id="knowledge"')[1])
    case('areas: an area with nothing open says so', 'none open' in areas.split('id="people"')[1].split('<section')[0])
    case('page: a missing block stops the build', stops(lambda: bc.put_blocks('<p>no blocks</p>', base())), 'stop')

    # the command
    case('--check: the committed snapshot and page agree', stops(lambda: bc.main(['--check'])), 0)
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / 'bad.json'
        bad.write_text(json.dumps(variant(setitem(['areas', 0, 'title'], 'a bead title'))), encoding='utf-8')
        case('--check --snapshot: a file that breaks the contract exits 1', stops(lambda: bc.main(['--check', '--snapshot', str(bad)])), 1)
        case('build --snapshot: a file that breaks the contract writes nothing', stops(lambda: bc.main(['--snapshot', str(bad)])), 1)

    for f in failures:
        print(f, file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
