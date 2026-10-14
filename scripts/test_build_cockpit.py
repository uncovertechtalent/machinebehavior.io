#!/usr/bin/env python3
"""Tests for scripts/build_cockpit.py (ADR-0031): the contract check on variants of a small data file (a key outside
the contract at each level, a key twice, free text in a fixed field, a foreign or mismatched URL, an item of an unlisted
repository), the GitHub read on API rows shaped like the real ones (a private or foreign repository stops it, forks and
archived repositories are skipped, items without an area label are counted without their text, status from labels and
merges), and the page blocks. Stdlib only; no network: the read runs on a stand-in for the API.

    python3 scripts/test_build_cockpit.py

Exits 1 when a case fails.
"""
import contextlib, copy, datetime, io, json, sys
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cockpit as bc  # noqa: E402

MB, PS = 'uncovertechtalent/machinebehavior.io', 'uncovertechtalent/cto-powersuit'


def item(repo, n, area, status='open', kind='action', pr=False, title=None, created='2026-10-10', closed=None):
    return {'repo': repo, 'number': n, 'pr': pr, 'title': title or f'Item {n}', 'url': bc.item_url(repo, n, pr), 'area': area,
            'kind': kind, 'status': status, 'created': created, 'closed': closed}


def base():
    return {'schema': 1, 'generated': '2026-10-14T14:00:00Z', 'owner': 'uncovertechtalent', 'repos': [PS, MB],
            'items': [item(MB, 83, 'security'), item(MB, 82, 'security', 'blocked', created='2026-09-20'),
                      item(MB, 93, 'direction', 'in_progress', pr=True), item(MB, 41, 'operations', kind=None),
                      item(MB, 85, 'ai', 'done', created='2026-10-01', closed='2026-10-13'),
                      item(MB, 46, 'delivery', 'dropped', pr=True, created='2026-10-11', closed='2026-10-11'),
                      item(PS, 13, 'security', kind='finding', title='Tags & <plugin> names')],
            'untriaged': {MB: 2}}


def variant(fn):
    d = copy.deepcopy(base())
    fn(d)
    return d


def fails(doc, text):
    return any(text in e for e in bc.check(doc))


def parse_fails(text):
    try:
        bc.parse(text)
    except bc.ContractError:
        return True
    return False


def quiet(fn):
    with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
        try:
            return fn()
        except SystemExit as e:
            return 'stop' if e.code not in (0, None) else 0


def repo_row(name, private=False, visibility='public', fork=False, archived=False, owner='uncovertechtalent', has_issues=True):
    return {'full_name': f'{owner}/{name}', 'owner': {'login': owner}, 'private': private, 'visibility': visibility,
            'fork': fork, 'archived': archived, 'has_issues': has_issues}


def api_issue(repo, n, labels=(), state='open', pr=False, merged=False, reason=None, created='2026-10-10T08:00:00Z', closed=None, title='T'):
    i = {'number': n, 'title': title, 'state': state, 'labels': [{'name': l} for l in labels], 'created_at': created,
         'closed_at': closed, 'state_reason': reason, 'html_url': bc.item_url(repo, n, pr)}
    if pr:
        i['pull_request'] = {'merged_at': '2026-10-12T10:00:00Z' if merged else None}
    return i


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

    case('the base data meets the contract', bc.check(base()), [])
    case('the committed cockpit.json meets the contract', quiet(lambda: bc.load() and 0), 0)

    # keys outside the contract, at every level
    case('top level: an extra key', fails(variant(setitem(['notes'], 'x')), 'keys outside the contract'))
    case('top level: a missing key', fails(variant(lambda d: d.pop('untriaged')), 'missing keys'))
    case('item: an extra key with text', fails(variant(setitem(['items', 0, 'body'], 'issue text')), 'items[0]: keys outside the contract'))
    case('item: a missing key', fails(variant(lambda d: d['items'][0].pop('kind')), 'items[0]: missing keys'))
    case('parse: a key twice in one object', parse_fails('{"schema": 1, "schema": 1}'))
    case('parse: NaN', parse_fails('{"schema": NaN}'))
    case('parse: not JSON', parse_fails('{schema: 1}'))
    case('parse: larger than the limit', parse_fails('"' + 'x' * (bc.MAX_BYTES + 1) + '"'))

    # fixed forms
    case('owner: another owner', fails(variant(setitem(['owner'], 'someone')), 'owner:'))
    case('repos: a repository of another owner', fails(variant(setitem(['repos'], [PS, MB, 'someone/repo'])), 'repos:'))
    case('repos: free text', fails(variant(setitem(['repos'], [PS, MB, 'my private notes'])), 'repos:'))
    case('repos: a repository twice', fails(variant(setitem(['repos'], [MB, MB, PS])), 'a repository twice'))
    case('generated: not UTC', fails(variant(setitem(['generated'], '2026-10-14T14:00:00+02:00')), 'generated:'))
    case('generated: not a real time', fails(variant(setitem(['generated'], '2026-13-40T25:00:00Z')), 'generated:'))
    case('schema: true', fails(variant(setitem(['schema'], True)), 'schema:'))
    case('item: area outside the eight', fails(variant(setitem(['items', 0, 'area'], 'personal')), '.area:'))
    case('item: kind outside the four', fails(variant(setitem(['items', 0, 'kind'], 'note')), '.kind:'))
    case('item: status outside the contract', fails(variant(setitem(['items', 0, 'status'], 'waiting')), '.status:'))
    case('item: number as text', fails(variant(setitem(['items', 0, 'number'], '83')), '.number:'))
    case('item: pr as text', fails(variant(setitem(['items', 0, 'pr'], 'no')), '.pr:'))
    case('item: created not a date', fails(variant(setitem(['items', 0, 'created'], 'yesterday')), '.created:'))
    case('item: open with a closed date', fails(variant(setitem(['items', 0, 'closed'], '2026-10-12')), 'must be null'))
    case('item: done without a closed date', fails(variant(setitem(['items', 4, 'closed'], None)), 'not a date for a closed item'))
    case('item: closed before created', fails(variant(setitem(['items', 4, 'closed'], '2026-09-01')), 'before created'))
    case('untriaged: an unlisted repository', fails(variant(setitem(['untriaged'], {'uncovertechtalent/other': 1})), 'untriaged:'))
    case('untriaged: not a count', fails(variant(setitem(['untriaged'], {MB: '2'})), 'untriaged:'))

    # only public GitHub data: URLs, repositories, titles
    case('item: repository not listed', fails(variant(setitem(['items', 0, 'repo'], 'uncovertechtalent/private-notes')), 'not one of the listed'))
    case('item: URL off GitHub', fails(variant(setitem(['items', 0, 'url'], 'https://example.test/x')), '.url:'))
    case('item: URL of another issue', fails(variant(setitem(['items', 0, 'url'], bc.item_url(MB, 84, False))), '.url:'))
    case('item: issue with a pull request URL', fails(variant(setitem(['items', 0, 'url'], bc.item_url(MB, 83, True))), '.url:'))
    case('item: title with a line break', fails(variant(setitem(['items', 0, 'title'], 'one\ntwo')), '.title:'))
    case('item: title too long', fails(variant(setitem(['items', 0, 'title'], 'x' * (bc.MAX_TITLE + 1))), '.title:'))
    case('item: empty title', fails(variant(setitem(['items', 0, 'title'], ' ')), '.title:'))
    case('item: the same issue twice', fails(variant(lambda d: d['items'].append(copy.deepcopy(d['items'][0]))), 'the same issue twice'))

    # the GitHub read
    rows = [repo_row('machinebehavior.io'), repo_row('cto-powersuit'), repo_row('preloop', fork=True), repo_row('old', archived=True),
            repo_row('no-issues', has_issues=False)]
    case('repos: forks, archived, and repositories without issues are skipped', bc.public_repos(rows), [PS, MB])
    case('repos: a private repository stops the read', quiet(lambda: bc.public_repos(rows + [repo_row('notes', private=True, visibility='private')])), 'stop')
    case('repos: an internal repository stops the read', quiet(lambda: bc.public_repos([repo_row('x', visibility='internal')])), 'stop')
    case('repos: another owner stops the read', quiet(lambda: bc.public_repos([repo_row('x', owner='someone')])), 'stop')
    to = bc.to_item
    case('item: no area label, so no item', to(MB, api_issue(MB, 5, ['type: bug'])), None)
    case('item: the board label "area: security" is not an area label', to(MB, api_issue(MB, 5, ['area: security'])), None)
    case('item: area and kind from labels', (lambda x: (x['area'], x['kind'], x['status']))(to(MB, api_issue(MB, 5, ['area:money', 'kind:finding']))), ('money', 'finding', 'open'))
    case('item: two area labels, the first in page order', to(MB, api_issue(MB, 5, ['area:people', 'area:delivery']))['area'], 'delivery')
    case('item: status: blocked wins', to(MB, api_issue(MB, 5, ['area:ai', 'status: blocked', 'status: in progress']))['status'], 'blocked')
    case('item: an open pull request is in progress', to(MB, api_issue(MB, 6, ['area:ai'], pr=True))['status'], 'in_progress')
    case('item: a merged pull request is done', to(MB, api_issue(MB, 6, ['area:ai'], 'closed', pr=True, merged=True, closed='2026-10-12T10:00:00Z'))['status'], 'done')
    case('item: a pull request closed without a merge is dropped', to(MB, api_issue(MB, 6, ['area:ai'], 'closed', pr=True, closed='2026-10-12T10:00:00Z'))['status'], 'dropped')
    case('item: an issue closed as not planned is dropped', to(MB, api_issue(MB, 7, ['area:ai'], 'closed', reason='not_planned', closed='2026-10-12T10:00:00Z'))['status'], 'dropped')
    case('item: whitespace in a title is folded', to(MB, api_issue(MB, 8, ['area:ai'], title='  a\tb\n c '))['title'], 'a b c')
    bad = api_issue(MB, 9, ['area:ai'])
    bad['html_url'] = 'https://github.com/someone/else/issues/9'
    case('item: an html_url of another repository stops the read', quiet(lambda: to(MB, bad)), 'stop')

    api = {
        f'{bc.API}/users/uncovertechtalent/repos': [repo_row('machinebehavior.io'), repo_row('preloop', fork=True)],
        f'{bc.API}/repos/{MB}/issues|open': [api_issue(MB, 83, ['area:security', 'kind:action']), api_issue(MB, 84, ['type: bug'], title='A stranger\'s report'),
                                            api_issue(MB, 93, ['area:direction'], pr=True)],
        f'{bc.API}/repos/{MB}/issues|closed': [api_issue(MB, 85, ['area:ai'], 'closed', reason='completed', closed='2026-10-13T09:00:00Z'),
                                              api_issue(MB, 20, ['area:ai'], 'closed', reason='completed', closed='2026-09-01T09:00:00Z')],
    }

    def fake_get(url):
        path, _, query = url.partition('?')
        if path.endswith('/issues'):
            if 'page=1' not in query.split('&'):
                return []
            return api[path + ('|open' if 'state=open' in query else '|closed')]
        return api[path]
    real_get, bc.get = bc.get, fake_get
    try:
        doc = bc.fetch(now=datetime.datetime(2026, 10, 14, 14, 0, tzinfo=datetime.timezone.utc))
    finally:
        bc.get = real_get
    case('fetch: the result meets the contract', bc.check(doc), [])
    case('fetch: forks are not read', doc['repos'], [MB])
    case('fetch: labelled items kept, a closed item older than the window left out', [x['number'] for x in doc['items']], [83, 85, 93])
    case('fetch: an unlabelled report is counted without its text', (doc['untriaged'], 'stranger' in json.dumps(doc)), ({MB: 1}, False))

    # the blocks
    d = base()
    case('eyebrow: names GitHub Issues and the time in UTC', bc.b_eyebrow(d), 'CTO powersuit cockpit · from GitHub Issues · 2026-10-14 14:00 UTC')
    case('lede: installs can use beads or GitHub Issues', 'on beads, a local issue tracker, or on GitHub Issues' in bc.b_lede(d))
    c = bc.counts(d['items'], bc.today(d))
    case('counts: open, in progress, blocked, done in 7 days', (c['open'], c['in_progress'], c['blocked'], c['closed_7d']), (3, 1, 1, 1))
    case('counts: open by kind, an item without a kind left out', (c['action'], c['finding'], c['decision']), (3, 1, 0))
    case('counts: oldest open in days', c['oldest'], 24)
    case('trend: 14 days to the data date', [t[0].isoformat() for t in bc.trend(d)][::13], ['2026-10-01', '2026-10-14'])
    case('trend: a closed item counts until its close, and as done on that day', [(t[1], t[2]) for t in bc.trend(d) if t[0].isoformat() in ('2026-10-12', '2026-10-13')], [(6, 0), (5, 1)])
    areas = bc.b_areas(d)
    sec = areas.split('id="security"')[1].split('<section')[0]
    case('areas: every area in page order', [areas.find(f'id="{k}"') for k in bc.AREA_KEYS] == sorted(areas.find(f'id="{k}"') for k in bc.AREA_KEYS))
    case('areas: security uses the powersuit title and links its plugins', '>Security and risk</h3>' in sec and all(f'href="/cto-powersuit/{p}/"' in sec for p in ('security', 'compliance', 'red-team')))
    case('areas: open items as cards with the GitHub link, blocked first', sec.index('issues/82') < sec.index('issues/83') and f'href="{bc.item_url(PS, 13, False)}"' in sec)
    case('areas: titles are escaped', 'Tags &amp; &lt;plugin&gt; names' in sec)
    case('areas: closed items are not cards', 'issues/85' not in areas and 'pull/46' not in areas)
    case('areas: knowledge links the knowledge layer', 'href="/cto-powersuit/vestige/"' in areas.split('id="knowledge"')[1])
    case('areas: an area with nothing open says so', 'Nothing open in this area.' in areas.split('id="people"')[1].split('<section')[0])
    case('sources: repositories linked, untriaged counted without text', 'href="https://github.com/uncovertechtalent/cto-powersuit"' in bc.b_sources(d) and '2 open items' in bc.b_sources(d))
    case('page: a missing block stops the build', quiet(lambda: bc.put_blocks('<p>no blocks</p>', d)), 'stop')
    case('--check: the committed data and page agree', quiet(lambda: bc.main(['--check'])), 0)

    for f in failures:
        print(f, file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
