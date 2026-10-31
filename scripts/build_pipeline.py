#!/usr/bin/env python3
"""The publishing pipeline of the publisher's seat on /inside/ (ADR-0050), from inside/publisher/pipeline.json.

    python3 scripts/build_pipeline.py --check   exit 1 when the file breaks its contract (the block it feeds is checked
                                                by scripts/build_inside_seats.py --check, which renders it)

The pipeline is the pieces the house is writing or has just published: the article drafts of the knowledge vault whose
front matter says teaser: public, exported on the holder's machine by scripts/export_pipeline.py and committed with a
pull request. A pending piece shows as a teaser, its working title, one standfirst, its stage (idea, drafting, in
review), and the surface it is meant for; a live piece links to its page. No piece carries a date it is due: the house
publishes when a piece is ready, so a piece shows the date its stage began and nothing else.

The contract allows exactly the keys below, fixed forms for every value, and as free text only a piece's title and its
standfirst, each on one line with no control character and none of the private patterns of scripts/vault_export.py.
A live piece's url must be an https address on one of the house's surfaces. A piece that breaks the contract keeps the
whole file off the page: the check names the piece, and the fix happens at the source. Stdlib only.
Tests: python3 scripts/test_build_pipeline.py.
"""
import re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cockpit as bc, vault_export as ve  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'inside' / 'publisher' / 'pipeline.json'
SCHEMA = 1
SOURCE = 'the article drafts of the knowledge vault whose front matter says teaser: public'
WINDOW_DAYS = 30  # a live piece stays on the list this long after it went live
TOP_KEYS = {'schema', 'generated', 'source', 'pieces'}
PIECE_KEYS = {'slug', 'title', 'standfirst', 'stage', 'home', 'url', 'since'}
SLUG_RX = re.compile(r'[a-z0-9][a-z0-9-]{0,79}')
STAGES = ('idea', 'drafting', 'review', 'live')
PENDING = STAGES[:3]
STAGE_LABEL = {'idea': ('idea', 'is-open'), 'drafting': ('drafting', 'is-warn'), 'review': ('in review', 'is-warn'),
               'live': ('live', 'is-ok')}
STAGE_RANK = {'review': 0, 'drafting': 1, 'idea': 2, 'live': 3}
HOMES = ('machinebehavior.io', 'uncovertechtalent.com', 'substack', 'open')
HOME_LABEL = {'machinebehavior.io': 'for machinebehavior.io', 'uncovertechtalent.com': 'for uncovertechtalent.com',
              'substack': 'for Substack', 'open': 'home open'}
URL_RX = re.compile(r'https://(?:machinebehavior\.io|uncovertechtalent\.com|tychat\.io|[a-z0-9-]+\.substack\.com)/[A-Za-z0-9._~/-]{0,200}')
MAX_TITLE = 160
MAX_STANDFIRST = 240
MAX_PIECES = 100

ContractError = bc.ContractError
esc, plural = bc.esc, bc.plural


# ---------- the contract ----------
def _text(v, limit, where, errs):
    if not isinstance(v, str) or not v.strip() or len(v) > limit or ve.hidden(v) or v != v.strip():
        errs.append(f'{where}: empty, longer than {limit}, padded, or holds a control character')
        return
    hits = ve.private_hits(v)
    if hits:
        errs.append(f'{where}: holds a private pattern ({", ".join(hits)}); fix the draft at its source')


def check_piece(x, where, generated):
    errs = bc._keys(x, PIECE_KEYS, where)
    if errs:
        return errs
    if not (isinstance(x['slug'], str) and SLUG_RX.fullmatch(x['slug'])):
        errs.append(f'{where}.slug: not a slug like logistics-of-state')
    _text(x['title'], MAX_TITLE, f'{where}.title', errs)
    _text(x['standfirst'], MAX_STANDFIRST, f'{where}.standfirst', errs)
    if x['stage'] not in STAGES:
        errs.append(f'{where}.stage: not one of {list(STAGES)}')
    if x['home'] not in HOMES:
        errs.append(f'{where}.home: not one of {list(HOMES)}')
    if x['stage'] == 'live':
        if not (isinstance(x['url'], str) and URL_RX.fullmatch(x['url'])):
            errs.append(f'{where}.url: a live piece needs an https address on one of the house\'s surfaces')
    elif x['url'] is not None:
        errs.append(f'{where}.url: must be null until the piece is live')
    since = bc._day(x['since'])
    if since is None:
        errs.append(f'{where}.since: not a date like 2026-10-30')
    elif generated:
        if since > generated.date():
            errs.append(f'{where}.since: after generated')
        if x['stage'] == 'live' and since < generated.date() - bc.datetime.timedelta(days=WINDOW_DAYS):
            errs.append(f'{where}.since: a live piece older than the {WINDOW_DAYS}-day window')
    return errs


def check(doc):
    """Every way the data breaks the contract; an empty list means the page may show it."""
    errs = bc._keys(doc, TOP_KEYS, 'pipeline.json')
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
    pieces = doc.get('pieces')
    if not isinstance(pieces, list) or len(pieces) > MAX_PIECES:
        errs.append(f'pieces: not a list of at most {MAX_PIECES} pieces')
        pieces = []
    seen = set()
    for i, x in enumerate(pieces):
        errs += check_piece(x, f'pieces[{i}]', generated)
        key = x.get('slug') if isinstance(x, dict) else None
        if key in seen:
            errs.append(f'pieces[{i}]: the same slug twice')
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
    """A pipeline with no piece, for a build that has no file to read (the seat tabs' tests)."""
    return {'schema': SCHEMA, 'generated': generated, 'source': SOURCE, 'pieces': []}


# ---------- the block on the publisher's dashboard ----------
def stamp(doc):
    return bc.stamp(doc)


def tally(pieces):
    return {s: sum(1 for x in pieces if x['stage'] == s) for s in STAGES}


def ordered(pieces):
    """Pending pieces first, the nearest to publication at the top (in review, drafting, idea), then the live pieces;
    the newest stage date first within a stage."""
    return sorted(pieces, key=lambda x: (STAGE_RANK[x['stage']], x['since'], x['slug']), reverse=False)


def row(x):
    text, cls = STAGE_LABEL[x['stage']]
    title = f'<a href="{esc(x["url"])}">{esc(x["title"])}</a>' if x['stage'] == 'live' else esc(x['title'])
    verb = 'live since' if x['stage'] == 'live' else f'{text} since'
    return (f'<li class="in-item"><span class="in-pill {cls}">{text}</span>'
            f'<span class="in-item-main">{title}<span class="in-item-lede">{esc(x["standfirst"])}</span>'
            f'<span class="in-item-meta">{esc(HOME_LABEL[x["home"]])}</span></span>'
            f'<span class="in-item-date">{verb} {esc(x["since"])}</span></li>')


def kpis(c):
    cells = (('Idea', c['idea']), ('Drafting', c['drafting']), ('In review', c['review']), (f'Live in {WINDOW_DAYS} days', c['live']))
    return '<dl class="in-kpis">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in cells) + '</dl>'


def block(doc):
    """The pipeline block of the publisher's queue band (ADR-0049): the heading with its freshness, the counts, the
    pieces. With no piece, one line and no number."""
    c = tally(doc['pieces'])
    pending = sum(c[s] for s in PENDING)
    head = (f'<h3>Publishing pipeline <span class="in-h-meta">{plural(pending, "piece")} pending · '
            f'as of {esc(stamp(doc))}, the last export</span></h3>')
    if not doc['pieces']:
        return head + '<p class="in-empty">No piece carries a public teaser.</p>'
    rows = ''.join(row(x) for x in ordered(doc['pieces']))
    return head + kpis(c) + f'<ul class="in-items in-pipeline">{rows}</ul>'


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv != ['--check']:
        print('usage: build_pipeline.py --check', file=sys.stderr)
        return 2
    try:
        doc = load(DATA)
    except ContractError as e:
        print(f'build_pipeline: {DATA.name} breaks the pipeline contract (ADR-0050):', file=sys.stderr)
        for line in str(e).splitlines():
            print('  ' + line, file=sys.stderr)
        return 1
    c = tally(doc['pieces'])
    print(f'build_pipeline: {plural(len(doc["pieces"]), "piece")} ({c["idea"]} idea, {c["drafting"]} drafting, {c["review"]} in review, '
          f'{c["live"]} live), exported {doc["generated"]}; file within its contract')
    return 0


if __name__ == '__main__':
    sys.exit(main())
