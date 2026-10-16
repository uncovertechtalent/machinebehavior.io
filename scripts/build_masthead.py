#!/usr/bin/env python3
"""Build the masthead page /inside/masthead/ from inside/masthead/seats.json (#99).

    python3 scripts/build_masthead.py            check seats.json, then write the masthead blocks of the page
    python3 scripts/build_masthead.py --check    write nothing; exit 1 when seats.json breaks the contract, or the page
                                                 blocks differ from what seats.json gives

seats.json is the public projection of the seats file the cockpit reads: one entry per seat with its key, title,
holder, areas, bundle, the machinery that runs its staff work, and the gates that apply. The house name sits in its
one field `house`; every mention of the name in the generated blocks comes from there, so a rename is one edit.

check() allows exactly the keys of the contract and fixed forms for every value: a seat key from the fixed list, each
listed once and in that order; areas from the eight areas of the cockpit; a bundle that is null or a slug; names and
holders with letters, digits, spaces and a few marks only; and bounded free text in `what`. The Conformity checks job
runs --check, so a data file that breaks the contract can neither merge nor deploy. Stdlib only.
Tests: python3 scripts/test_build_masthead.py.
"""
import html, json, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE_URL = '/inside/masthead/'
PAGE_REL = 'inside/masthead/index.html'
PAGE = ROOT / PAGE_REL
DATA = ROOT / 'inside' / 'masthead' / 'seats.json'

SCHEMA = 1
SEATS = ['ceo', 'cto', 'cfo', 'chro', 'publisher', 'cko']  # masthead order
AREAS = ['direction', 'delivery', 'operations', 'money', 'security', 'ai', 'people', 'knowledge']  # the cockpit's eight
AREA_TITLES = {'direction': 'Direction', 'delivery': 'Delivery', 'operations': 'Operations', 'money': 'Money',
               'security': 'Security and risk', 'ai': 'AI', 'people': 'People', 'knowledge': 'Knowledge layer'}
TOP_KEYS = {'schema', 'house', 'source', 'seats'}
SEAT_KEYS = {'seat', 'title', 'holder', 'areas', 'bundle', 'machinery', 'gates'}
NAME_RX = re.compile(r'^[A-Za-z0-9][A-Za-z0-9 .,&/:()-]{0,79}$')   # titles, holders, machinery and gate names
HOUSE_RX = re.compile(r'^[A-Za-z0-9][A-Za-z0-9 .-]{0,59}$')
SLUG_RX = re.compile(r'^[a-z][a-z0-9-]{0,39}$')
MAX_WHAT = 400
MAX_LIST = 20
MAX_BYTES = 64 * 1024


class ContractError(ValueError):
    pass


def _keys(obj, want, where, errs):
    if not isinstance(obj, dict):
        errs.append(f'{where}: not an object')
        return False
    extra, missing = sorted(set(obj) - want), sorted(want - set(obj))
    if extra:
        errs.append(f'{where}: keys outside the contract: {", ".join(extra)}')
    if missing:
        errs.append(f'{where}: missing keys: {", ".join(missing)}')
    return not (extra or missing)


def _text(v, rx, where, errs, limit=None):
    if not isinstance(v, str) or not v.strip():
        errs.append(f'{where}: not a non-empty string')
        return
    if rx is not None and not rx.match(v):
        errs.append(f'{where}: not in the allowed form')
    if limit is not None and len(v) > limit:
        errs.append(f'{where}: longer than {limit} characters')
    if any(c in v for c in '<>'):
        errs.append(f'{where}: angle brackets')


def _rows(v, key_name, where, errs):
    """A list of {name-or-check, what} objects, bounded."""
    if not isinstance(v, list) or not v:
        errs.append(f'{where}: not a non-empty list')
        return
    if len(v) > MAX_LIST:
        errs.append(f'{where}: more than {MAX_LIST} rows')
    for i, row in enumerate(v):
        w = f'{where}[{i}]'
        if _keys(row, {key_name, 'what'}, w, errs):
            _text(row[key_name], NAME_RX, f'{w}.{key_name}', errs)
            _text(row['what'], None, f'{w}.what', errs, MAX_WHAT)


def check(doc):
    """The contract errors of a parsed seats.json, in order; empty when it conforms."""
    errs = []
    if not _keys(doc, TOP_KEYS, 'top level', errs):
        return errs
    if doc['schema'] != SCHEMA:
        errs.append(f'schema: {doc["schema"]!r}, want {SCHEMA}')
    _text(doc['house'], HOUSE_RX, 'house', errs)
    _text(doc['source'], None, 'source', errs, MAX_WHAT)
    seats = doc['seats']
    if not isinstance(seats, list) or not seats:
        errs.append('seats: not a non-empty list')
        return errs
    keys = []
    for i, s in enumerate(seats):
        w = f'seats[{i}]'
        if not _keys(s, SEAT_KEYS, w, errs):
            continue
        if s['seat'] not in SEATS:
            errs.append(f'{w}.seat: {s["seat"]!r} is not a seat ({", ".join(SEATS)})')
        keys.append(s['seat'])
        _text(s['title'], NAME_RX, f'{w}.title', errs)
        _text(s['holder'], NAME_RX, f'{w}.holder', errs)
        areas = s['areas']
        if not isinstance(areas, list) or not areas or len(set(areas)) != len(areas) or any(a not in AREAS for a in areas):
            errs.append(f'{w}.areas: not a non-empty list of distinct areas from {", ".join(AREAS)}')
        if s['bundle'] is not None and not (isinstance(s['bundle'], str) and SLUG_RX.match(s['bundle'])):
            errs.append(f'{w}.bundle: null or a slug')
        _rows(s['machinery'], 'name', f'{w}.machinery', errs)
        _rows(s['gates'], 'check', f'{w}.gates', errs)
    if len(set(keys)) != len(keys):
        errs.append('seats: a seat is listed twice')
    elif keys != [k for k in SEATS if k in keys]:
        errs.append(f'seats: not in masthead order ({", ".join(SEATS)})')
    return errs


def load(path=DATA):
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ContractError(f'{path.name} is larger than {MAX_BYTES} bytes')
    try:
        doc = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError) as e:
        raise ContractError(f'{path.name} is not valid JSON: {e}') from None
    errs = check(doc)
    if errs:
        raise ContractError('\n'.join(errs))
    return doc


def esc(s):
    return html.escape(str(s), quote=True)


def plural(n, one, many=None):
    return f'{n} {one if n == 1 else (many or one + "s")}'


def holders(doc):
    out = []
    for s in doc['seats']:
        if s['holder'] not in out:
            out.append(s['holder'])
    return out


def b_eyebrow(doc):
    return f'Inside · Masthead · {esc(doc["house"])}'


def b_lede(doc):
    n, h = len(doc['seats']), holders(doc)
    who = ' and '.join(esc(x) for x in h) if len(h) <= 2 else ', '.join(esc(x) for x in h[:-1]) + ', and ' + esc(h[-1])
    return (f'{esc(doc["house"])} is a publishing house run with the engineering principles of a CTO in everything it puts out. '
            f'{plural(n, "seat")}, {plural(len(h), "holder")} today: {who}. Each seat reads some of the eight areas of the '
            f'<a href="/inside/cockpit/">cockpit</a>, its staff work runs on the open modules of the '
            f'<a href="/cto-powersuit/">CTO powersuit</a>, and every piece passes the gates listed under the seat. '
            f'The seats together are the C-suit: one suit per seat, the whole suit for a company. '
            f'The seats are a data file, <a href="/inside/masthead/seats.json">seats.json</a>; a seat that moves to another '
            f'person is one changed line in it.')


def b_seats(doc):
    out = ['<div class="mh-seats">']
    for s in doc['seats']:
        areas = ''.join(f'<li><a href="/inside/cockpit/#{esc(a)}">{esc(AREA_TITLES[a])}</a></li>' for a in s['areas'])
        machinery = ''.join(f'<li><b>{esc(r["name"])}</b> {esc(r["what"])}</li>' for r in s['machinery'])
        gates = ''.join(f'<li><code>{esc(r["check"])}</code> {esc(r["what"])}</li>' for r in s['gates'])
        bundle = esc(s['bundle']) if s['bundle'] else 'none yet'
        out.append(
            f'<section class="mh-seat card" id="{esc(s["seat"])}" aria-labelledby="mh-{esc(s["seat"])}">'
            f'<div class="mh-seat-head"><p class="mh-label">{esc(s["seat"]).upper()}</p>'
            f'<h3 id="mh-{esc(s["seat"])}">{esc(s["title"])}</h3>'
            f'<p class="mh-holder">Holder: <b>{esc(s["holder"])}</b> · bundle: <span class="mono">{bundle}</span></p>'
            f'<ul class="mh-areas" aria-label="Areas">{areas}</ul></div>'
            f'<div class="mh-cols"><div><h4>Machinery</h4><ul class="mh-list">{machinery}</ul></div>'
            f'<div><h4>Gates</h4><ul class="mh-list">{gates}</ul></div></div>'
            f'</section>')
    out.append('</div>')
    return ''.join(out)


BLOCKS = {
    'masthead-eyebrow': b_eyebrow,
    'masthead-lede': b_lede,
    'masthead-seats': b_seats,
}


def block_rx(name):
    return re.compile(rf'<!-- static:{name} -->(.*?)<!-- /static:{name} -->', re.S)


def put_blocks(src, doc):
    for name, fn in BLOCKS.items():
        rx = block_rx(name)
        if not rx.search(src):
            raise SystemExit(f'build_masthead: {PAGE_REL} has no <!-- static:{name} --> block')
        body = fn(doc)
        src = rx.sub(lambda _: f'<!-- static:{name} -->{body}<!-- /static:{name} -->', src, count=1)
    return src


def report(msg):
    print(f'build_masthead: {msg}')


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        doc = load(DATA)
    except ContractError as e:
        print(f'build_masthead: {DATA.name} breaks the contract:', file=sys.stderr)
        for line in str(e).splitlines():
            print('  ' + line, file=sys.stderr)
        return 1
    page = PAGE.read_text(encoding='utf-8')
    new = put_blocks(page, doc)
    summary = f'{plural(len(doc["seats"]), "seat")}, {plural(len(holders(doc)), "holder")}, house {doc["house"]}'

    if '--check' in argv:
        differ = [n for n in BLOCKS if block_rx(n).search(page).group(1) != block_rx(n).search(new).group(1)]
        for d in differ:
            report(f'differs from what seats.json gives: {d}')
        report(f'seats.json meets the contract ({summary}); ' + ('page up to date' if not differ else f'{len(differ)} differ; run python3 scripts/build_masthead.py'))
        return 1 if differ else 0

    site_chrome.tree(reload=True)
    out = site_chrome.apply(new, PAGE_REL)
    if out != page:
        PAGE.write_text(out, encoding='utf-8')
    report(f'{PAGE_REL} written: {summary}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
