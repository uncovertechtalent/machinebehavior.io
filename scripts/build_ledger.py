#!/usr/bin/env python3
"""The house ledger on the board page /inside/board/ (ADR-0050), from inside/board/ledger.json.

    python3 scripts/build_ledger.py           check the file against its contract, then write the block
    python3 scripts/build_ledger.py --check   write nothing; exit 1 when the file breaks its contract or the page
                                              block differs from what the file gives

The ledger is the work of the house that is tracked outside GitHub: the records of the knowledge vault's bead tracker
that carry the label public, exported on the holder's machine by scripts/export_ledger.py and committed with a pull
request (the deploy job has no vault to read, so this file is as fresh as the last export, and the page says so). One
block in inside/board/index.html, <!-- static:ledger -->: four lanes, in progress, blocked, open, and done in the last
30 days, each record with its bead id, its title, its area, its kind, and its date; the open lanes list the longest
waiting first, the done lane the newest closed first. No link: a bead has no public page.

The contract allows exactly the keys below, fixed forms for every value, and as free text only a record's title, which
may hold no control character and none of the private patterns of scripts/vault_export.py (a private address, a host
shorthand, an e-mail address, a home path, the former employer). A record that breaks the contract keeps the whole file
off the page: the check names the record, and the fix happens at the source. The Conformity checks job runs --check.
Stdlib only. Tests: python3 scripts/test_build_ledger.py.
"""
import re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cockpit as bc, build_masthead as bm, vault_export as ve  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE_REL = 'inside/board/index.html'
PAGE = ROOT / PAGE_REL
DATA = ROOT / 'inside' / 'board' / 'ledger.json'
BLOCK = 'ledger'
SCHEMA = 1
SOURCE = 'the bead tracker of the knowledge vault, records with the label public'
WINDOW_DAYS = 30  # as the board's done column
TOP_KEYS = {'schema', 'generated', 'source', 'window_days', 'items'}
ITEM_KEYS = {'id', 'title', 'area', 'kind', 'status', 'created', 'closed'}
ID_RX = re.compile(r'vault-[a-z0-9]{3,6}(?:\.\d{1,3})?')
STATUSES = bc.OPEN_STATUSES + ('done',)  # a dropped record is not exported
MAX_TITLE = 200
MAX_ITEMS = 500
LANES = (('in_progress', 'In progress', 'being worked on'), ('blocked', 'Blocked', 'waits on a decision or an input'),
         ('open', 'Open', 'recorded, not started'), ('done', f'Done in {WINDOW_DAYS} days', 'closed as done'))

ContractError = bc.ContractError
esc, plural = bc.esc, bc.plural


# ---------- the contract ----------
def check_item(x, where, generated):
    errs = bc._keys(x, ITEM_KEYS, where)
    if errs:
        return errs
    if not (isinstance(x['id'], str) and ID_RX.fullmatch(x['id'])):
        errs.append(f'{where}.id: not a bead id like vault-8cuc')
    t = x['title']
    if not isinstance(t, str) or not t.strip() or len(t) > MAX_TITLE or ve.hidden(t) or t != t.strip():
        errs.append(f'{where}.title: empty, longer than {MAX_TITLE}, padded, or holds a control character')
    else:
        hits = ve.private_hits(t)
        if hits:
            errs.append(f'{where}.title: holds a private pattern ({", ".join(hits)}); fix the record at its source')
    if x['area'] not in bc.AREA_KEYS:
        errs.append(f'{where}.area: not one of {bc.AREA_KEYS}')
    if x['kind'] is not None and x['kind'] not in bc.SHOWN_KINDS:
        errs.append(f'{where}.kind: not one of {bc.SHOWN_KINDS} or null')
    if x['status'] not in STATUSES:
        errs.append(f'{where}.status: not one of {list(STATUSES)}')
    created = bc._day(x['created'])
    if created is None:
        errs.append(f'{where}.created: not a date like 2026-10-30')
    if x['status'] in bc.OPEN_STATUSES:
        if x['closed'] is not None:
            errs.append(f'{where}.closed: must be null for an open record')
    else:
        closed = bc._day(x['closed'])
        if closed is None:
            errs.append(f'{where}.closed: not a date for a done record')
        else:
            if created and closed < created:
                errs.append(f'{where}.closed: before created')
            if generated and closed < generated.date() - bc.datetime.timedelta(days=WINDOW_DAYS):
                errs.append(f'{where}.closed: older than the {WINDOW_DAYS}-day window')
            if generated and closed > generated.date():
                errs.append(f'{where}.closed: after generated')
    return errs


def check(doc):
    """Every way the data breaks the contract; an empty list means the page may show it."""
    errs = bc._keys(doc, TOP_KEYS, 'ledger.json')
    if not isinstance(doc, dict):
        return errs
    if doc.get('schema') != SCHEMA or isinstance(doc.get('schema'), bool):
        errs.append(f'schema: must be {SCHEMA}')
    generated = None
    if not (isinstance(doc.get('generated'), str) and bc.GENERATED_RX.fullmatch(doc['generated']) and bc._when(doc['generated'])):
        errs.append('generated: not a UTC timestamp like 2026-10-31T09:00:00Z')
    else:
        generated = bc._when(doc['generated'])
    if doc.get('source') != SOURCE:
        errs.append(f'source: must be {SOURCE!r}')
    if doc.get('window_days') != WINDOW_DAYS or isinstance(doc.get('window_days'), bool):
        errs.append(f'window_days: must be {WINDOW_DAYS}')
    items = doc.get('items')
    if not isinstance(items, list) or len(items) > MAX_ITEMS:
        errs.append(f'items: not a list of at most {MAX_ITEMS} records')
        items = []
    seen = set()
    for i, x in enumerate(items):
        errs += check_item(x, f'items[{i}]', generated)
        key = x.get('id') if isinstance(x, dict) else None
        if key in seen:
            errs.append(f'items[{i}]: the same record twice')
        seen.add(key)
    return errs


def load(path=DATA):
    """The checked data, or ContractError with every violation."""
    try:
        text = Path(path).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        raise ContractError(f'cannot read {path}: {e}') from None
    doc = bc.parse(text)
    errs = check(doc)
    if errs:
        raise ContractError('\n'.join(errs))
    return doc


def empty(generated='1970-01-01T00:00:00Z'):
    """A ledger with no record, for a build that has no file to read (the seat tabs' tests)."""
    return {'schema': SCHEMA, 'generated': generated, 'source': SOURCE, 'window_days': WINDOW_DAYS, 'items': []}


# ---------- the block ----------
def stamp(doc):
    return bc.stamp(doc)


def tally(items):
    return {s: sum(1 for x in items if x['status'] == s) for s in STATUSES}


def live(items):
    """The records not done, blocked first, then in progress, then open; the longest waiting first within a status, as the
    cockpit lists its items."""
    return sorted((x for x in items if x['status'] in bc.OPEN_STATUSES),
                  key=lambda x: (bc.STATUS_ORDER[x['status']], x['created'], x['id']))


def row(x, titles):
    kind = f' · {esc(x["kind"])}' if x['kind'] else ''
    when = f'closed {esc(x["closed"])}' if x['status'] == 'done' else f'opened {esc(x["created"])}'
    return (f'<li><span class="mb-ledger-id">{esc(x["id"])}</span><span class="mb-ledger-title">{esc(x["title"])}</span>'
            f'<span class="mb-links-meta">{esc(titles[x["area"]])}{kind} · {when}</span></li>')


def lane(key, name, about, items, titles):
    if key == 'done':
        rows = sorted(items, key=lambda x: (x['closed'], x['id']), reverse=True)  # the newest closed first, as the board's Done
    else:
        rows = sorted(items, key=lambda x: (x['created'], x['id']))  # the longest waiting first, as the board's open columns
    body = ''.join(row(x, titles) for x in rows) if rows else f'<li class="mb-ledger-empty">none</li>'
    return (f'<section class="static-col ledger-col" aria-label="{esc(name)}, {plural(len(rows), "record")}">'
            f'<h2>{esc(name)} <span class="mb-n">{len(rows)}</span></h2><p class="col-about">{esc(about)}</p>'
            f'<ul class="mb-links">{body}</ul></section>')


def block_html(doc, titles=None):
    titles = titles or bm.area_titles()
    cols = ''.join(lane(k, n, a, [x for x in doc['items'] if x['status'] == k], titles) for k, n, a in LANES)
    c = tally(doc['items'])
    return (f'<div class="ledger-cols">{cols}</div>'
            f'<p class="note">{plural(len(doc["items"]), "record")} as of {esc(stamp(doc))}, the last export: '
            f'{c["in_progress"]} in progress, {c["blocked"]} blocked, {c["open"]} open, {c["done"]} done in {WINDOW_DAYS} days. '
            f'Data: <a href="/inside/board/ledger.json">ledger.json</a>.</p>')


def block_rx():
    return re.compile(rf'<!-- static:{BLOCK} -->(.*?)<!-- /static:{BLOCK} -->', re.S)


def block(src):
    found = block_rx().findall(src)
    if len(found) != 1:
        raise SystemExit(f'build_ledger: {PAGE_REL} has {len(found)} <!-- static:{BLOCK} --> blocks, want 1')
    return found[0]


def put_block(src, doc):
    body = block_html(doc)
    return block_rx().sub(lambda _: f'<!-- static:{BLOCK} -->{body}<!-- /static:{BLOCK} -->', src, count=1)


def report(msg):
    print(f'build_ledger: {msg}')


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv not in ([], ['--check']):
        print('usage: build_ledger.py [--check]', file=sys.stderr)
        return 2
    try:
        doc = load(DATA)
    except ContractError as e:
        print(f'build_ledger: {DATA.name} breaks the ledger contract (ADR-0050):', file=sys.stderr)
        for line in str(e).splitlines():
            print('  ' + line, file=sys.stderr)
        return 1
    page = PAGE.read_text(encoding='utf-8')
    new = put_block(page, doc)
    summary = f'{plural(len(doc["items"]), "record")}, exported {doc["generated"]}'
    if argv == ['--check']:
        same = block(page) == block(new)
        if not same:
            report(f'the {BLOCK} block of {PAGE_REL} differs from what ledger.json gives')
        report(f'{summary}; ' + ('page up to date' if same else 'run python3 scripts/build_ledger.py'))
        return 0 if same else 1
    if new != page:
        PAGE.write_text(new, encoding='utf-8')
    report(f'{PAGE_REL} written: {summary}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
