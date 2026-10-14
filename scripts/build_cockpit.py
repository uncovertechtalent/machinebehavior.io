#!/usr/bin/env python3
"""The cockpit page /inside/cockpit/, from the issues and pull requests of the owner's public repositories (ADR-0031).

    python3 scripts/build_cockpit.py --fetch    read GitHub, check, write inside/cockpit/cockpit.json, then build the page
    python3 scripts/build_cockpit.py            build the page from the committed inside/cockpit/cockpit.json (no network)
    python3 scripts/build_cockpit.py --check    write nothing; exit 1 when cockpit.json breaks the contract, or the page
                                                or its sitemap date differ from it (no network)

The deploy job runs --fetch (artifact only, never committed), so the live page is as fresh as the last deploy; a
failed read or check leaves the committed page in place. The Conformity checks job runs --check.

What reaches the page is public GitHub data only:
- the repositories are the owner's own (no forks, nothing archived) that GitHub reports as public; the read uses
  GH_TOKEN if set, else no token, as scripts/board_snapshot.py does. In the deploy job GH_TOKEN is this repository's
  workflow token, which reads no private repository of the owner, and the read stops on any repository not reported
  public;
- an item reaches the page with its title only when a maintainer has given it an area label (area:<area>) and its author
  is the owner, a member, or a collaborator, so a title that a stranger edits after the label stays off the page, and
  when it is not a lead (kind:lead), whose title may name a person or a company; other open items are counted per
  repository, without their text, as the board does with untriaged issues;
- check() allows exactly the keys of the contract, fixed forms for every value, and as free text only an item's title;
  each item's URL must be the GitHub URL of that issue or pull request in a listed repository of the owner.
Stdlib only. Tests: python3 scripts/test_build_cockpit.py.
"""
import datetime, html, json, os, re, sys, unicodedata, urllib.parse, urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mini_yaml, site_chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://machinebehavior.io'
PAGE_URL = '/inside/cockpit/'
PAGE_REL = 'inside/cockpit/index.html'  # the page's path in the site, for the chrome
PAGE = ROOT / PAGE_REL
SITEMAP = ROOT / 'sitemap.xml'
DATA = ROOT / 'inside' / 'cockpit' / 'cockpit.json'
POWERSUIT_YML = ROOT / 'site' / 'powersuit.yml'
MODULES_JSON = ROOT / 'cto-powersuit' / 'modules.json'
OWNER = 'uncovertechtalent'  # the only owner whose repositories are read; another owner is a reviewed change
API = 'https://api.github.com'
WINDOW_DAYS = 14  # the trend; closed items older than this are not kept

# The eight areas, in page order: the label's key and the area's title on the powersuit pages (site/powersuit.yml;
# None is its knowledge layer). The same keys as the cockpit's local tracker.
AREAS = [
    ('direction', 'Direction'),
    ('delivery', 'Delivery'),
    ('operations', 'Operations'),
    ('money', 'Money'),
    ('security', 'Security and risk'),
    ('ai', 'AI'),
    ('people', 'People'),
    ('knowledge', None),
]
AREA_KEYS = [k for k, _ in AREAS]
KINDS = ['finding', 'decision', 'action', 'lead']  # the kind labels; a lead (a sales lead or an application) is only counted
SHOWN_KINDS = KINDS[:3]  # the kinds an item on the page may have
OPEN_STATUSES = ('open', 'in_progress', 'blocked')
STATUSES = OPEN_STATUSES + ('done', 'dropped')

SCHEMA = 1
TOP_KEYS = {'schema', 'generated', 'owner', 'repos', 'items', 'untriaged'}
ITEM_KEYS = {'repo', 'number', 'pr', 'title', 'url', 'area', 'kind', 'status', 'created', 'closed'}
GENERATED_RX = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
DATE_RX = re.compile(r'\d{4}-\d{2}-\d{2}')
REPO_RX = re.compile(rf'{re.escape(OWNER)}/[A-Za-z0-9._-]{{1,100}}')
TRUSTED = ('OWNER', 'MEMBER', 'COLLABORATOR')  # author_association values whose titles may reach the page
MAX_BYTES = 512 * 1024
MAX_TITLE = 300
MAX_ITEMS = 1000
MAX_REPOS = 100


class ContractError(ValueError):
    pass


# ---------- the contract ----------
def _no_dupes(pairs):
    keys = [k for k, _ in pairs]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        raise ContractError(f'a key appears twice in one object: {dup}')
    return dict(pairs)


def _no_constant(name):
    raise ContractError(f'{name} is not a number')


def parse(text):
    """The data as a dict, or ContractError: too large, not JSON, a key twice, NaN or Infinity."""
    if len(text.encode('utf-8')) > MAX_BYTES:
        raise ContractError(f'larger than {MAX_BYTES} bytes')
    try:
        return json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_no_constant)
    except ContractError:
        raise
    except ValueError as e:
        raise ContractError(f'not JSON ({e})') from None


def _count(v):
    return isinstance(v, int) and not isinstance(v, bool) and 0 <= v < 10**7


def _keys(obj, want, where):
    if not isinstance(obj, dict):
        return [f'{where}: not an object']
    extra, missing = sorted(set(obj) - set(want)), sorted(set(want) - set(obj))
    return ([f'{where}: keys outside the contract {extra}'] if extra else []) + ([f'{where}: missing keys {missing}'] if missing else [])


def _day(s):
    if not (isinstance(s, str) and DATE_RX.fullmatch(s)):
        return None
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def _when(g):
    try:
        return datetime.datetime.strptime(g, '%Y-%m-%dT%H:%M:%SZ')
    except (TypeError, ValueError):
        return None


def hidden(t):
    """True when a title holds a control or format character (bidi marks, zero widths, soft hyphens, tag characters) or
    a line or paragraph separator: anything that reorders or hides text."""
    return any(unicodedata.category(ch) in ('Cc', 'Cf', 'Zl', 'Zp') for ch in t)


def item_url(repo, number, pr):
    return f'https://github.com/{repo}/{"pull" if pr else "issues"}/{number}'


def check_item(x, where, repos):
    errs = _keys(x, ITEM_KEYS, where)
    if errs:
        return errs
    if x['repo'] not in repos:
        errs.append(f'{where}.repo: not one of the listed repositories')
    if not (_count(x['number']) and x['number'] > 0):
        errs.append(f'{where}.number: not an issue number')
    if not isinstance(x['pr'], bool):
        errs.append(f'{where}.pr: not true or false')
    elif x['repo'] in repos and _count(x['number']) and x['url'] != item_url(x['repo'], x['number'], x['pr']):
        errs.append(f'{where}.url: not {item_url(x["repo"], x["number"], x["pr"])}')
    t = x['title']
    if not isinstance(t, str) or not t.strip() or len(t) > MAX_TITLE or hidden(t) or t != t.strip():
        errs.append(f'{where}.title: empty, longer than {MAX_TITLE}, padded, or holds a control character')
    if x['area'] not in AREA_KEYS:
        errs.append(f'{where}.area: not one of {AREA_KEYS}')
    if x['kind'] is not None and x['kind'] not in SHOWN_KINDS:
        errs.append(f'{where}.kind: not one of {SHOWN_KINDS} or null')
    if x['status'] not in STATUSES:
        errs.append(f'{where}.status: not one of {list(STATUSES)}')
    created = _day(x['created'])
    if created is None:
        errs.append(f'{where}.created: not a date like 2026-10-14')
    if x['status'] in OPEN_STATUSES:
        if x['closed'] is not None:
            errs.append(f'{where}.closed: must be null for an open item')
    else:
        closed = _day(x['closed'])
        if closed is None:
            errs.append(f'{where}.closed: not a date for a closed item')
        elif created and closed < created:
            errs.append(f'{where}.closed: before created')
    return errs


def check(doc):
    """Every way the data breaks the contract; an empty list means the page may show it."""
    errs = _keys(doc, TOP_KEYS, 'cockpit.json')
    if not isinstance(doc, dict):
        return errs
    if doc.get('schema') != SCHEMA or isinstance(doc.get('schema'), bool):
        errs.append(f'schema: must be {SCHEMA}')
    if not (isinstance(doc.get('generated'), str) and GENERATED_RX.fullmatch(doc['generated']) and _when(doc['generated'])):
        errs.append('generated: not a UTC timestamp like 2026-10-14T14:00:00Z')
    if doc.get('owner') != OWNER:
        errs.append(f'owner: must be {OWNER!r}')
    repos = doc.get('repos')
    if not isinstance(repos, list) or len(repos) > MAX_REPOS or not all(isinstance(r, str) and REPO_RX.fullmatch(r) for r in repos):
        errs.append(f'repos: not a list of {OWNER}/<name>')
        repos = []
    elif len(set(repos)) != len(repos):
        errs.append('repos: a repository twice')
    repos = set(repos)
    items = doc.get('items')
    if not isinstance(items, list) or len(items) > MAX_ITEMS:
        errs.append(f'items: not a list of at most {MAX_ITEMS} items')
        items = []
    seen = set()
    for i, x in enumerate(items):
        errs += check_item(x, f'items[{i}]', repos)
        key = (x.get('repo'), x.get('number')) if isinstance(x, dict) else None
        if key in seen:
            errs.append(f'items[{i}]: the same issue twice')
        seen.add(key)
    un = doc.get('untriaged')
    if not isinstance(un, dict) or not all(r in repos and _count(n) for r, n in un.items()):
        errs.append('untriaged: not an object of listed repositories and counts')
    return errs


def load(path=DATA):
    """The checked data, or ContractError with every violation."""
    try:
        text = Path(path).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        raise ContractError(f'cannot read {path}: {e}') from None
    doc = parse(text)
    errs = check(doc)
    if errs:
        raise ContractError('\n'.join(errs))
    return doc


# ---------- reading GitHub ----------
def get(url):
    """GET a GitHub API URL: with GH_TOKEN when set, then without a token, as scripts/board_snapshot.py does."""
    last = None
    for auth in (True, False):
        if auth and not os.environ.get('GH_TOKEN'):
            continue
        h = {'Accept': 'application/vnd.github+json', 'User-Agent': 'machinebehavior.io cockpit'}
        if auth:
            h['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=20))
        except (OSError, ValueError) as e:  # URLError, timeouts, and resets while the body is read are OSErrors
            print(f'warning: {url.split("?")[0]} (token={auth}) failed: {e}', file=sys.stderr)
            last = e
    raise SystemExit(f'build_cockpit: reading GitHub failed: {last}')


def pages(path, params):
    out = []
    for page in range(1, 11):
        q = urllib.parse.urlencode({**params, 'per_page': 100, 'page': page})
        batch = get(f'{API}/{path}?{q}')
        if not isinstance(batch, list):
            raise SystemExit(f'build_cockpit: {path} did not return a list')
        out += batch
        if len(batch) < 100:
            break
    else:
        print(f'warning: {path}: stopped after 10 full pages; the counts leave out the rest', file=sys.stderr)
    return out


def public_repos(rows):
    """The owner's own public repositories with issues, from GET /users/<owner>/repos; stops on anything not public."""
    out = []
    for r in rows:
        if (r.get('owner') or {}).get('login') != OWNER:
            raise SystemExit(f'build_cockpit: {r.get("full_name")} is not a repository of {OWNER}')
        if r.get('private') is not False or r.get('visibility') != 'public':
            raise SystemExit(f'build_cockpit: {r.get("full_name")} is not reported public; nothing written')
        if r.get('fork') or r.get('archived') or not r.get('has_issues'):
            continue
        out.append(r['full_name'])
    return sorted(out)


def labelled(names, prefix, keys):
    for k in keys:  # the first in page order, when an item carries more than one
        if prefix + k in names:
            return k
    return None


def clean_title(t):
    """The title on one line: control and format characters dropped, whitespace folded."""
    t = ''.join(ch for ch in str(t) if unicodedata.category(ch) not in ('Cc', 'Cf') or ch in '\t\n\r')  # whitespace folds below
    return ' '.join(t.split())[:MAX_TITLE].strip()


def to_item(repo, i):
    """One issue or pull request from the issues API as an item, or None when it has no area label or its author is
    outside the owner's account and its collaborators."""
    names = {l['name'] for l in i.get('labels') or []}
    area = labelled(names, 'area:', AREA_KEYS)
    if area is None or i.get('author_association') not in TRUSTED or 'kind:lead' in names:
        return None
    pr = 'pull_request' in i
    if i['state'] == 'open':
        status = 'blocked' if 'status: blocked' in names else 'in_progress' if pr or 'status: in progress' in names else 'open'
        closed = None
    else:
        done = bool((i.get('pull_request') or {}).get('merged_at')) if pr else i.get('state_reason') in ('completed', None)
        status, closed = ('done' if done else 'dropped'), i['closed_at'][:10]
    url = item_url(repo, i['number'], pr)
    if i.get('html_url') != url:
        raise SystemExit(f'build_cockpit: {i.get("html_url")} is not {url}')
    return {'repo': repo, 'number': i['number'], 'pr': pr, 'title': clean_title(i['title']),
            'url': url, 'area': area, 'kind': labelled(names, 'kind:', KINDS), 'status': status,
            'created': i['created_at'][:10], 'closed': closed}


def fetch(now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    start = (now - datetime.timedelta(days=WINDOW_DAYS)).strftime('%Y-%m-%dT00:00:00Z')
    repos = public_repos(pages(f'users/{OWNER}/repos', {'type': 'owner'}))
    items, untriaged = [], {}
    for repo in repos:
        raw = pages(f'repos/{repo}/issues', {'state': 'open'})
        raw += [i for i in pages(f'repos/{repo}/issues', {'state': 'closed', 'since': start}) if (i.get('closed_at') or '') >= start]
        for i in raw:
            it = to_item(repo, i)
            if it:
                items.append(it)
            elif i['state'] == 'open':
                untriaged[repo] = untriaged.get(repo, 0) + 1
    items.sort(key=lambda x: (x['repo'], x['number']))
    return {'schema': SCHEMA, 'generated': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'owner': OWNER, 'repos': repos,
            'items': items, 'untriaged': untriaged}


# ---------- the page ----------
def esc(s):
    return html.escape(str(s), quote=True)


def stamp(doc):
    return _when(doc['generated']).strftime('%Y-%m-%d %H:%M UTC')


def today(doc):
    return _when(doc['generated']).date()


def plural(n, one, many=None):
    return f'{n} {one if n == 1 else (many or one + "s")}'


def short(repo):
    return repo.split('/', 1)[1]


def area_info():
    """For each area key: its title, its one line, and its plugins (name, page), from the powersuit pages."""
    cfg = mini_yaml.load_file(POWERSUIT_YML)
    mods = json.loads(MODULES_JSON.read_text(encoding='utf-8'))
    about = {a['title']: a['about'] for a in cfg['areas']}
    plugins = {a['title']: [(m['name'], m['url']) for m in a['modules']] for a in mods['areas']}
    out = {}
    for key, title in AREAS:
        if title is None:
            out[key] = (cfg['knowledge']['title'], cfg['knowledge']['about'], [(m['name'], m['url']) for m in mods['knowledge']['modules']])
        elif title in about and title in plugins:
            out[key] = (title, about[title], plugins[title])
        else:
            raise SystemExit(f'build_cockpit: area {title!r} is not in site/powersuit.yml and cto-powersuit/modules.json')
    return out


def counts(items, day):
    week = day - datetime.timedelta(days=7)
    live = [x for x in items if x['status'] in OPEN_STATUSES]
    c = {s: sum(1 for x in live if x['status'] == s) for s in OPEN_STATUSES}
    c['closed_7d'] = sum(1 for x in items if x['status'] == 'done' and _day(x['closed']) > week)
    c.update({k: sum(1 for x in live if x['kind'] == k) for k in KINDS})
    c['oldest'] = max(((day - _day(x['created'])).days for x in live), default=None)
    return c


def b_eyebrow(doc):
    return f'CTO powersuit cockpit · from GitHub Issues · {stamp(doc)}'


def b_lede(doc):
    return (f'This is the CTO powersuit cockpit running on Stefan Coetzee\'s public work: the issues and pull requests of '
            f'his public repositories on GitHub, by area of the CTO job, as of {stamp(doc)}. An install can run the same '
            f'cockpit on beads, a local issue tracker, or on GitHub Issues.')


def b_totals(doc):
    c = counts(doc['items'], today(doc))
    week = (today(doc) - datetime.timedelta(days=7)).isoformat()
    cells = [('Open', c['open'], 'not started, not blocked'), ('In progress', c['in_progress'], 'labelled, or an open pull request'),
             ('Blocked', c['blocked'], 'waiting on a decision or an input'), ('Closed in 7 days', c['closed_7d'], f'done since {week}')]
    return ''.join(f'<li class="card ck-kpi"><span class="k">{k}</span><span class="v">{v}</span><span class="s">{s}</span></li>'
                   for k, v, s in cells)


def trend(doc):
    end = today(doc)
    out = []
    for n in range(WINDOW_DAYS - 1, -1, -1):
        d = end - datetime.timedelta(days=n)
        out.append((d, sum(1 for x in doc['items'] if _day(x['created']) <= d and (x['closed'] is None or _day(x['closed']) > d)),
                    sum(1 for x in doc['items'] if x['status'] == 'done' and _day(x['closed']) == d)))
    return out


def b_trend(doc):
    days = trend(doc)
    top = max(o for _, o, _ in days) or 1
    li = ''.join(
        f'<li><span class="ck-col" aria-hidden="true"><span class="ck-fill" style="height:{round(100 * o / top)}%"></span></span>'
        f'<span class="ck-n" aria-hidden="true">{o}</span><span class="ck-c" aria-hidden="true">{c}</span>'
        f'<span class="ck-day" aria-hidden="true">{d.isoformat()[5:]}</span>'
        f'<span class="mb-sr">{d.isoformat()}: {o} not closed, {c} done that day</span></li>' for d, o, c in days)
    return (f'<figure class="ck-trend"><figcaption>Items with an area label not yet closed at the end of each day (bars), and items '
            f'done that day (the row below), for the {WINDOW_DAYS} days to {days[-1][0].isoformat()}.</figcaption>'
            f'<ol class="ck-days">{li}</ol><p class="ck-legend" aria-hidden="true"><span>not closed</span><span>done that day</span></p></figure>')


STATUS_ORDER = {'blocked': 0, 'in_progress': 1, 'open': 2}
STATUS_TEXT = {'blocked': 'blocked', 'in_progress': 'in progress', 'open': 'open'}


def card(x, day):
    age = (day - _day(x['created'])).days
    chips = (f'<span class="ck-chip ck-st-{x["status"]}">{STATUS_TEXT[x["status"]]}</span>'
             + (f'<span class="ck-chip">{x["kind"]}</span>' if x['kind'] else ''))
    return (f'<li class="ck-item"><a href="{esc(x["url"])}">{esc(x["title"])}</a>'
            f'<span class="ck-meta">{chips}<span>{esc(short(x["repo"]))} · {"pull request" if x["pr"] else "issue"} {x["number"]}</span>'
            f'<span>{plural(age, "day")} old</span></span></li>')


def b_areas(doc):
    info, day = area_info(), today(doc)
    out = ''
    for key, _ in AREAS:
        title, about, plugins = info[key]
        mine = [x for x in doc['items'] if x['area'] == key]
        c = counts(mine, day)
        live = sorted((x for x in mine if x['status'] in OPEN_STATUSES), key=lambda x: (STATUS_ORDER[x['status']], x['created'], x['repo'], x['number']))
        links = ' '.join(f'<a href="{esc(u)}"><code>{esc(n)}</code></a>' for n, u in plugins)
        mix = ''.join(f'<span class="ck-mix-{cls}" style="flex-grow:{c[s]}"></span>' for s, cls in
                      (('open', 'open'), ('in_progress', 'prog'), ('blocked', 'block')) if c[s])
        nums = ''.join(f'<div><dt>{k}</dt><dd>{c[f]}</dd></div>' for k, f in
                       (('Open', 'open'), ('In progress', 'in_progress'), ('Blocked', 'blocked'), ('Closed in 7 days', 'closed_7d')))
        kinds = ''.join(f'<div><dt>{k.capitalize()}s</dt><dd>{c[k]}</dd></div>' for k in ('finding', 'decision', 'action'))
        kinds += f'<div><dt>Oldest open</dt><dd>{plural(c["oldest"], "day") if c["oldest"] is not None else "none open"}</dd></div>'
        cards = (f'<ul class="ck-items">{"".join(card(x, day) for x in live)}</ul>' if live
                 else '<p class="empty">Nothing open in this area.</p>')
        out += (f'<section class="ck-area" id="{key}" aria-labelledby="ck-{key}">'
                f'<div class="ck-area-head"><h3 id="ck-{key}">{esc(title)}</h3><p>{esc(about)}</p>'
                f'<p class="ck-plugins"><span class="ck-label">Powersuit plugins</span><span>{links}</span></p></div>'
                f'<div class="ck-card"><dl class="ck-counts">{nums}</dl>'
                f'<div class="ck-mix{"" if mix else " ck-mix-none"}" aria-hidden="true">{mix}</div>'
                f'<p class="ck-label">Open by kind</p><dl class="ck-kinds">{kinds}</dl></div>'
                f'<div class="ck-open">{cards}</div></section>')
    return f'<div class="ck-areas">{out}</div>'


def b_sources(doc):
    repos = ', '.join(f'<a href="https://github.com/{esc(r)}">{esc(short(r))}</a>' for r in doc['repos'])
    un = sum(doc['untriaged'].values())
    out = f'<p>Read from the public repositories of {esc(doc["owner"])} on GitHub: {repos}.</p>'
    if un:
        per = ', '.join(f'{esc(short(r))} {n}' for r, n in sorted(doc['untriaged'].items()))
        out += (f'<p>{plural(un, "open item")} in these repositories {"is" if un == 1 else "are"} counted here only, without '
                f'{"its" if un == 1 else "their"} text ({per}). Items without an area label, items opened by someone outside the '
                f'owner\'s account and its collaborators, and leads are counted this way.</p>')
    return out


BLOCKS = {
    'cockpit-eyebrow': b_eyebrow,
    'cockpit-lede': b_lede,
    'cockpit-totals': b_totals,
    'cockpit-trend': b_trend,
    'cockpit-areas': b_areas,
    'cockpit-sources': b_sources,
}


def block_rx(name):
    return re.compile(rf'<!-- static:{name} -->(.*?)<!-- /static:{name} -->', re.S)


def put_blocks(src, doc):
    for name, fn in BLOCKS.items():
        rx = block_rx(name)
        if not rx.search(src):
            raise SystemExit(f'build_cockpit: inside/cockpit/index.html has no <!-- static:{name} --> block')
        body = fn(doc)
        src = rx.sub(lambda _: f'<!-- static:{name} -->{body}<!-- /static:{name} -->', src, count=1)
    return src


SITEMAP_RX = re.compile(rf'(<url><loc>{re.escape(BASE + PAGE_URL)}</loc><lastmod>)(\d{{4}}-\d{{2}}-\d{{2}})(</lastmod></url>)')


def sitemap_date(text):
    m = SITEMAP_RX.search(text)
    if not m:
        raise SystemExit(f'build_cockpit: sitemap.xml has no line for {PAGE_URL}')
    return m.group(2)


def report(msg):
    print(f'build_cockpit: {msg}')


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if '--fetch' in argv:
        doc = fetch()
        errs = check(doc)
        if errs:
            print('build_cockpit: the data read from GitHub breaks the contract (ADR-0031); nothing written:', file=sys.stderr)
            for e in errs:
                print('  ' + e, file=sys.stderr)
            return 1
        text = json.dumps(doc, indent=1, ensure_ascii=False) + '\n'
    else:
        try:
            text = DATA.read_text(encoding='utf-8')
            doc = load(DATA)
        except ContractError as e:
            print(f'build_cockpit: {DATA.name} breaks the contract (ADR-0031):', file=sys.stderr)
            for line in str(e).splitlines():
                print('  ' + line, file=sys.stderr)
            return 1
    page = PAGE.read_text(encoding='utf-8')
    new = put_blocks(page, doc)
    sitemap = SITEMAP.read_text(encoding='utf-8')
    day = doc['generated'][:10]
    summary = (f'{len(doc["repos"])} repositories, {sum(x["status"] in OPEN_STATUSES for x in doc["items"])} open items with an area, '
               f'{sum(doc["untriaged"].values())} without, as of {doc["generated"]}')

    if '--check' in argv:
        differ = [n for n in BLOCKS if block_rx(n).search(page).group(1) != block_rx(n).search(new).group(1)]
        if sitemap_date(sitemap) != day:
            differ.append(f'sitemap.xml lastmod of {PAGE_URL} ({sitemap_date(sitemap)}, data {day})')
        for d in differ:
            report(f'differs from what cockpit.json, site/powersuit.yml, and cto-powersuit/modules.json give: {d}')
        report(f'cockpit.json meets the contract ({summary}); ' + ('page up to date' if not differ else f'{len(differ)} differ; run python3 scripts/build_cockpit.py'))
        return 1 if differ else 0

    # The chrome reads the page's Updated line and dateModified from the sitemap on disk, so the sitemap is written first
    # and put back if the chrome fails; the data and the page are written only after the chrome has run.
    SITEMAP.write_text(SITEMAP_RX.sub(lambda m: m.group(1) + day + m.group(3), sitemap, count=1), encoding='utf-8')
    try:
        site_chrome.tree(reload=True)
        out = site_chrome.apply(new, PAGE_REL)
    except BaseException:
        SITEMAP.write_text(sitemap, encoding='utf-8')
        raise
    if out != page:
        PAGE.write_text(out, encoding='utf-8')
    DATA.write_text(text, encoding='utf-8')
    report(f'{PAGE_REL} written: {summary}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
