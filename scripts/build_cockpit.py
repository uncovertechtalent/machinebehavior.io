#!/usr/bin/env python3
"""The cockpit page /inside/cockpit/, from the counts-only snapshot inside/cockpit/snapshot.json (ADR-0031).

    python3 scripts/build_cockpit.py                    check the snapshot, then write the page and its sitemap date
    python3 scripts/build_cockpit.py --check            write nothing; exit 1 when the snapshot breaks the contract,
                                                        or the page or its sitemap date differ from the snapshot
    python3 scripts/build_cockpit.py --snapshot FILE    check (and without --check, publish) another file: the build
                                                        copies a valid FILE to inside/cockpit/snapshot.json first

The cockpit is the local app in which Stefan Coetzee runs his work by the eight areas of the CTO powersuit. Its
`export --public-json` writes the snapshot; the file reaches this repository through a pull request only.

The contract (schema 1) is the guard. check() returns every violation, and the build and --check stop on any:
- exactly the keys schema, generated, source, areas, totals, trend, public_items, at every level exactly the keys
  listed below, nothing else, and no key twice;
- counts are integers from 0; generated is a UTC timestamp; source is beads-desk@<commit> (or "fixture", the sample
  file, which the page labels as sample figures); each area key and its name are fixed;
- totals are the sums of the eight areas, so no count from outside the eight areas reaches the page;
- the only free text is the title of a public item, and an item is a pull request or an issue on GitHub in a repository
  of an owner in PUBLIC_OWNERS, with a URL that matches its repository and kind.
Stdlib only. Tests: python3 scripts/test_build_cockpit.py.
"""
import datetime, html, json, re, shutil, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mini_yaml, site_chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://machinebehavior.io'
PAGE_URL = '/inside/cockpit/'
PAGE = ROOT / 'inside' / 'cockpit' / 'index.html'
SNAPSHOT = ROOT / 'inside' / 'cockpit' / 'snapshot.json'
POWERSUIT_YML = ROOT / 'site' / 'powersuit.yml'
MODULES_JSON = ROOT / 'cto-powersuit' / 'modules.json'
SITE_REPO = 'uncovertechtalent/machinebehavior.io'  # its open issues are on the board; the page counts them and links there

# The eight areas of the cockpit, in page order: the export's key and name, and the area's title on the powersuit
# pages (site/powersuit.yml; None is its knowledge layer). A change here is a change of the contract.
AREAS = [
    ('direction', 'Direction', 'Direction'),
    ('delivery', 'Delivery', 'Delivery'),
    ('operations', 'Operations', 'Operations'),
    ('money', 'Money', 'Money'),
    ('security', 'Security', 'Security and risk'),
    ('ai', 'AI', 'AI'),
    ('people', 'People', 'People'),
    ('knowledge', 'Knowledge', None),
]
NAME = {k: n for k, n, _ in AREAS}
# Owners whose public repositories may appear as public items. Adding an owner is its own reviewed pull request.
PUBLIC_OWNERS = ('uncovertechtalent',)

SCHEMA = 1
TOP_KEYS = {'schema', 'generated', 'source', 'areas', 'totals', 'trend', 'public_items'}
AREA_COUNTS = ('open', 'in_progress', 'blocked', 'closed_7d', 'findings_open', 'decisions_open', 'actions_open', 'oldest_open_days')
AREA_KEYS = {'key', 'name', *AREA_COUNTS}
TOTAL_KEYS = ('open', 'in_progress', 'blocked', 'closed_7d')
TREND_KEYS = {'date', 'open', 'closed'}
ITEM_KEYS = {'repo', 'kind', 'title', 'url', 'state'}
ITEM_KINDS = {'pr': 'pull', 'issue': 'issues'}
ITEM_STATES = ('open', 'closed', 'merged')
GENERATED_RX = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
SOURCE_RX = re.compile(r'beads-desk@[0-9a-f]{7,40}|fixture')
DATE_RX = re.compile(r'\d{4}-\d{2}-\d{2}')
REPO_RX = re.compile(r'([A-Za-z0-9][A-Za-z0-9-]{0,38})/([A-Za-z0-9._-]{1,100})')
CONTROL_RX = re.compile(r'[\x00-\x1f\x7f<>]')
MAX_BYTES = 256 * 1024
MAX_TITLE = 300
MAX_ITEMS = 200
MAX_TREND = 366
TREND_SHOWN = 14


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
    raise ContractError(f'{name} is not a count')


def parse(text):
    """The snapshot as a dict, or ContractError: too large, not JSON, a key twice, NaN or Infinity."""
    if len(text.encode('utf-8')) > MAX_BYTES:
        raise ContractError(f'larger than {MAX_BYTES} bytes')
    try:
        return json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_no_constant)
    except ValueError as e:
        if isinstance(e, ContractError):
            raise
        raise ContractError(f'not JSON ({e})') from None


def _count(v):
    return isinstance(v, int) and not isinstance(v, bool) and 0 <= v < 10**7


def _keys(obj, want, where):
    if not isinstance(obj, dict):
        return [f'{where}: not an object']
    extra, missing = sorted(set(obj) - set(want)), sorted(set(want) - set(obj))
    out = []
    if extra:
        out.append(f'{where}: keys outside the contract {extra}')
    if missing:
        out.append(f'{where}: missing keys {missing}')
    return out


def _date(s):
    try:
        return datetime.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def check_item(x, where):
    errs = _keys(x, ITEM_KEYS, where)
    if errs:
        return errs
    repo, kind = x['repo'], x['kind']
    m = REPO_RX.fullmatch(repo) if isinstance(repo, str) else None
    if not m:
        errs.append(f'{where}.repo: not owner/name')
    elif m.group(1) not in PUBLIC_OWNERS:
        errs.append(f'{where}.repo: owner {m.group(1)!r} is not in PUBLIC_OWNERS {list(PUBLIC_OWNERS)}')
    if kind not in ITEM_KINDS:
        errs.append(f'{where}.kind: not one of {sorted(ITEM_KINDS)}')
    if x['state'] not in ITEM_STATES:
        errs.append(f'{where}.state: not one of {list(ITEM_STATES)}')
    t = x['title']
    if not isinstance(t, str) or not t.strip() or len(t) > MAX_TITLE or CONTROL_RX.search(t) or t != t.strip():
        errs.append(f'{where}.title: empty, longer than {MAX_TITLE}, padded, or holds a control character or < >')
    if m and kind in ITEM_KINDS:
        if not (isinstance(x['url'], str) and re.fullmatch(rf'https://github\.com/{re.escape(repo)}/{ITEM_KINDS[kind]}/[1-9]\d{{0,6}}', x['url'])):
            errs.append(f'{where}.url: not https://github.com/{repo}/{ITEM_KINDS[kind]}/<number>')
    return errs


def check(doc):
    """Every way the snapshot breaks the contract; an empty list means the page may show it."""
    errs = _keys(doc, TOP_KEYS, 'snapshot')
    if not isinstance(doc, dict):
        return errs
    if doc.get('schema') != SCHEMA or isinstance(doc.get('schema'), bool):
        errs.append(f'schema: must be {SCHEMA}')
    g = doc.get('generated')
    if not (isinstance(g, str) and GENERATED_RX.fullmatch(g) and _when(g)):
        errs.append('generated: not a UTC timestamp like 2026-10-14T14:00:00Z')
    s = doc.get('source')
    if not (isinstance(s, str) and SOURCE_RX.fullmatch(s)):
        errs.append('source: not beads-desk@<commit> or fixture')

    areas = doc.get('areas')
    if not isinstance(areas, list):
        errs.append('areas: not a list')
        areas = []
    seen = []
    for i, a in enumerate(areas):
        w = f'areas[{i}]'
        e = _keys(a, AREA_KEYS, w)
        if e:
            errs += e
            continue
        if a['key'] not in NAME:
            errs.append(f'{w}.key: not one of the eight areas')
        else:
            seen.append(a['key'])
            if a['name'] != NAME[a['key']]:
                errs.append(f'{w}.name: must be {NAME[a["key"]]!r}')
        errs += [f'{w}.{k}: not a count' for k in AREA_COUNTS if not _count(a[k])]
    if len(areas) != len(NAME) or sorted(seen) != sorted(NAME):
        errs.append(f'areas: each of the eight areas exactly once ({", ".join(NAME)})')

    totals = doc.get('totals')
    e = _keys(totals, TOTAL_KEYS, 'totals')
    if e:
        errs += e
    else:
        errs += [f'totals.{k}: not a count' for k in TOTAL_KEYS if not _count(totals[k])]
        good = [a for a in areas if isinstance(a, dict) and not _keys(a, AREA_KEYS, '') and all(_count(a[k]) for k in TOTAL_KEYS)]
        if len(good) == len(areas) == len(NAME):
            for k in TOTAL_KEYS:
                if _count(totals[k]) and totals[k] != sum(a[k] for a in good):
                    errs.append(f'totals.{k}: {totals[k]} is not the sum of the eight areas ({sum(a[k] for a in good)})')

    trend = doc.get('trend')
    if not isinstance(trend, list) or len(trend) > MAX_TREND:
        errs.append(f'trend: not a list of at most {MAX_TREND} days')
        trend = []
    last = None
    for i, t in enumerate(trend):
        w = f'trend[{i}]'
        e = _keys(t, TREND_KEYS, w)
        if e:
            errs += e
            continue
        d = _date(t['date']) if isinstance(t['date'], str) and DATE_RX.fullmatch(t['date']) else None
        if d is None:
            errs.append(f'{w}.date: not a date like 2026-10-14')
        elif last is not None and d <= last:
            errs.append(f'{w}.date: not after the day before it')
        last = d or last
        errs += [f'{w}.{k}: not a count' for k in ('open', 'closed') if not _count(t[k])]

    items = doc.get('public_items')
    if not isinstance(items, list) or len(items) > MAX_ITEMS:
        errs.append(f'public_items: not a list of at most {MAX_ITEMS} items')
        items = []
    urls = []
    for i, x in enumerate(items):
        errs += check_item(x, f'public_items[{i}]')
        if isinstance(x, dict) and x.get('url') in urls:
            errs.append(f'public_items[{i}].url: listed twice')
        urls.append(x.get('url') if isinstance(x, dict) else None)
    return errs


def load_snapshot(path):
    """The checked snapshot, or ContractError with every violation."""
    try:
        text = Path(path).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        raise ContractError(f'cannot read {path}: {e}') from None
    doc = parse(text)
    errs = check(doc)
    if errs:
        raise ContractError('\n'.join(errs))
    return doc


# ---------- the page ----------
def esc(s):
    return html.escape(str(s), quote=True)


def _when(g):
    try:
        return datetime.datetime.strptime(g, '%Y-%m-%dT%H:%M:%SZ')
    except (TypeError, ValueError):
        return None


def stamp(doc):
    return _when(doc['generated']).strftime('%Y-%m-%d %H:%M UTC')


def plural(n, one, many=None):
    return f'{n} {one if n == 1 else (many or one + "s")}'


def area_info():
    """For each area key: its title, its one line, and its plugins (name, page) from the powersuit pages."""
    cfg = mini_yaml.load_file(POWERSUIT_YML)
    mods = json.loads(MODULES_JSON.read_text(encoding='utf-8'))
    about = {a['title']: a['about'] for a in cfg['areas']}
    plugins = {a['title']: [(m['name'], m['url']) for m in a['modules']] for a in mods['areas']}
    out = {}
    for key, _, title in AREAS:
        if title is None:
            t, ab, pl = cfg['knowledge']['title'], cfg['knowledge']['about'], [(m['name'], m['url']) for m in mods['knowledge']['modules']]
        else:
            if title not in about or title not in plugins:
                raise SystemExit(f'build_cockpit: area {title!r} is not in site/powersuit.yml and cto-powersuit/modules.json')
            t, ab, pl = title, about[title], plugins[title]
        out[key] = (t, ab, pl)
    return out


def b_eyebrow(doc):
    sample = ' · sample figures' if doc['source'] == 'fixture' else ''
    return f'Counts only · snapshot {stamp(doc)}{sample}'


def b_lede(doc):
    out = (f'This page shows Stefan Coetzee\'s operation as he runs it through the cockpit: the work in each of the eight '
           f'areas of the CTO job, as counts only, from the snapshot of {stamp(doc)}.')
    if doc['source'] == 'fixture':
        out += ' These are sample figures from the test file; the first snapshot of the operation replaces them.'
    return out


def b_totals(doc):
    t = doc['totals']
    week = (_when(doc['generated']).date() - datetime.timedelta(days=7)).isoformat()
    cells = [('Open', t['open'], 'not started, not blocked'), ('In progress', t['in_progress'], 'being worked on'),
             ('Blocked', t['blocked'], 'waiting on another item'), ('Closed in 7 days', t['closed_7d'], f'since {week}')]
    return ''.join(f'<li class="card ck-kpi"><span class="k">{k}</span><span class="v">{v}</span><span class="s">{s}</span></li>'
                   for k, v, s in cells)


def b_trend(doc):
    days = doc['trend'][-TREND_SHOWN:]
    if not days:
        return '<p class="empty">This snapshot has no trend.</p>'
    top = max(d['open'] for d in days) or 1
    li = ''
    for d in days:
        h = round(100 * d['open'] / top)
        li += (f'<li><span class="ck-col" aria-hidden="true"><span class="ck-fill" style="height:{h}%"></span></span>'
               f'<span class="ck-n" aria-hidden="true">{d["open"]}</span><span class="ck-c" aria-hidden="true">{d["closed"]}</span>'
               f'<span class="ck-day" aria-hidden="true">{d["date"][5:]}</span>'
               f'<span class="mb-sr">{d["date"]}: {d["open"]} not closed, {d["closed"]} closed that day</span></li>')
    return (f'<figure class="ck-trend"><figcaption>Items in the eight areas not yet closed at the end of each day '
            f'(bars), and items closed that day (the row below), for the {plural(len(days), "day")} to {days[-1]["date"]}.</figcaption>'
            f'<ol class="ck-days">{li}</ol><p class="ck-legend" aria-hidden="true"><span>not closed</span><span>closed that day</span></p></figure>')


def b_areas(doc):
    info = area_info()
    by_key = {a['key']: a for a in doc['areas']}
    out = ''
    for key, _, _ in AREAS:
        a, (title, about, plugins) = by_key[key], info[key]
        live = a['open'] + a['in_progress'] + a['blocked']
        links = ' '.join(f'<a href="{esc(u)}"><code>{esc(n)}</code></a>' for n, u in plugins)
        mix = ''.join(f'<span class="ck-mix-{c}" style="flex-grow:{a[k]}"></span>' for k, c in
                      (('open', 'open'), ('in_progress', 'prog'), ('blocked', 'block')) if a[k])
        counts = ''.join(f'<div><dt>{k}</dt><dd>{a[f]}</dd></div>' for k, f in
                         (('Open', 'open'), ('In progress', 'in_progress'), ('Blocked', 'blocked'), ('Closed in 7 days', 'closed_7d')))
        oldest = plural(a['oldest_open_days'], 'day') if live or a['oldest_open_days'] else 'none open'
        kinds = ''.join(f'<div><dt>{k}</dt><dd>{a[f]}</dd></div>' for k, f in
                        (('Findings', 'findings_open'), ('Decisions', 'decisions_open'), ('Actions', 'actions_open')))
        kinds += f'<div><dt>Oldest open</dt><dd>{oldest}</dd></div>'
        out += (f'<section class="ck-area" id="{key}" aria-labelledby="ck-{key}">'
                f'<div class="ck-area-head"><h3 id="ck-{key}">{esc(title)}</h3><p>{esc(about)}</p>'
                f'<p class="ck-plugins"><span class="ck-label">Powersuit plugins</span><span>{links}</span></p></div>'
                f'<div class="ck-card"><dl class="ck-counts">{counts}</dl>'
                + (f'<div class="ck-mix" aria-hidden="true">{mix}</div>' if live else '<div class="ck-mix ck-mix-none" aria-hidden="true"></div>')
                + f'<p class="ck-label">Open by kind</p><dl class="ck-kinds">{kinds}</dl></div></section>')
    return f'<div class="ck-areas">{out}</div>'


def b_items(doc):
    items = [x for x in doc['public_items'] if x['state'] == 'open']
    site_issues = [x for x in items if x['repo'] == SITE_REPO and x['kind'] == 'issue']
    shown = sorted((x for x in items if x not in site_issues),
                   key=lambda x: (x['repo'], x['kind'], int(x['url'].rsplit('/', 1)[1])))
    out = ''
    if shown:
        out += '<ul class="mb-links ck-items">' + ''.join(
            f'<li><a href="{esc(x["url"])}">{esc(x["title"])}</a><span class="mb-links-meta">{esc(x["repo"])} · '
            f'{"pull request" if x["kind"] == "pr" else "issue"} {x["url"].rsplit("/", 1)[1]}</span></li>' for x in shown) + '</ul>'
    else:
        out += '<p class="empty">No open public pull request or issue in this snapshot.</p>'
    if site_issues:
        out += (f'<p class="ck-board">This site has {plural(len(site_issues), "open issue")} in the snapshot; they are '
                f'on the <a href="/inside/board/">board</a>, with their columns.</p>')
    return out


BLOCKS = {
    'cockpit-eyebrow': b_eyebrow,
    'cockpit-lede': b_lede,
    'cockpit-totals': b_totals,
    'cockpit-trend': b_trend,
    'cockpit-areas': b_areas,
    'cockpit-items': b_items,
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


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    check_only = '--check' in argv
    src_path = SNAPSHOT
    if '--snapshot' in argv:
        i = argv.index('--snapshot')
        if i + 1 >= len(argv):
            print('build_cockpit: --snapshot needs a file', file=sys.stderr)
            return 2
        src_path = Path(argv[i + 1])
    try:
        doc = load_snapshot(src_path)
    except ContractError as e:
        print(f'build_cockpit: {src_path} breaks the snapshot contract (ADR-0031):', file=sys.stderr)
        for line in str(e).splitlines():
            print('  ' + line, file=sys.stderr)
        return 1
    page = PAGE.read_text(encoding='utf-8')
    new = put_blocks(page, doc)
    sm_path = ROOT / 'sitemap.xml'
    sitemap = sm_path.read_text(encoding='utf-8')
    day = doc['generated'][:10]

    if check_only:
        differ = [n for n in BLOCKS if block_rx(n).search(page).group(1) != block_rx(n).search(new).group(1)]
        on_disk = SNAPSHOT.read_text(encoding='utf-8') if SNAPSHOT.exists() else None
        if src_path != SNAPSHOT and on_disk != Path(src_path).read_text(encoding='utf-8'):
            differ.append(f'{SNAPSHOT.relative_to(ROOT)} (not the file given)')
        if sitemap_date(sitemap) != day:
            differ.append(f'sitemap.xml lastmod of {PAGE_URL} ({sitemap_date(sitemap)}, snapshot {day})')
        for d in differ:
            print(f'build_cockpit: differs from the snapshot: {d}')
        print(f'build_cockpit: snapshot {doc["generated"]} ({doc["source"]}) meets the contract; '
              + ('page up to date' if not differ else f'{len(differ)} differ; run python3 scripts/build_cockpit.py'))
        return 1 if differ else 0

    if src_path != SNAPSHOT:
        shutil.copyfile(src_path, SNAPSHOT)
    sitemap_date(sitemap)
    sm_path.write_text(SITEMAP_RX.sub(lambda m: m.group(1) + day + m.group(3), sitemap, count=1), encoding='utf-8')
    site_chrome.tree(reload=True)  # the page's Updated line and dateModified come from the sitemap date
    out = site_chrome.apply(new, PAGE.relative_to(ROOT).as_posix())
    if out != page:
        PAGE.write_text(out, encoding='utf-8')
    print(f'build_cockpit: {PAGE.relative_to(ROOT)} from the snapshot of {doc["generated"]} ({doc["source"]})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
