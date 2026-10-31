#!/usr/bin/env python3
"""The seat tabs of the Inside landing page /inside/ (ADR-0034), from inside/masthead/seats.json and inside/cockpit/cockpit.json.

    python3 scripts/build_inside_seats.py           check both files against their contracts, then write the block
    python3 scripts/build_inside_seats.py --check   write nothing; exit 1 when a file breaks its contract or the page
                                                    block differs from what the two files give

One block in inside/index.html, <!-- static:inside-seats -->: one folder tab per seat in masthead order, then one
dashboard per seat. A tab shows only the seat code and one status pill (ADR-0036): "N blocked" when blocked, else
"N open" when open, else "clear"; the areas and the counts live in the dashboard, not on the tab. A dashboard shows the
lens questions from seats.json, the counts (open, in progress, blocked, and done in the cockpit's 14 days) for the seat's
areas, and the seat's items that are not done, blocked first, each linked to its issue or pull request. The chief
executive's dashboard counts every area, shows one tile per area and the decisions waiting (kind decision, not done) as
on the masthead (ADR-0032), then the items of its own areas, a list new in ADR-0034.

The seats, holders, areas, and lens come from the seats contract (ADR-0032), the items and the area titles from the
cockpit's (ADR-0031), each read through its own loader and check. Two more sources since ADR-0050, each with its own
contract and loader: the house ledger (inside/board/ledger.json, the vault's bead records with the label public), whose
records not done join every seat's queue band for the seat's areas as their own block with their own freshness line,
and the publishing pipeline (inside/publisher/pipeline.json, the drafts with a public teaser), which fills the
publisher's queue band in place of the placeholder it held from ADR-0034. A panel whose data source does not exist
yet is a labelled placeholder with no number; none is pending today.

Each dashboard ends with a hand-written slot, <!-- seat-extra:SEAT --> ... <!-- /seat-extra:SEAT -->: the cards and tools
that belong to the seat (deploy feed, apps, front page and the like). The build writes everything else in the block and
carries each slot's content over from the page unchanged, so the slots are edited by hand in inside/index.html.

Every dashboard follows one pane grammar (ADR-0049): four bands in a fixed order, signal, queue, state, tools. The
signal band holds the seat's one live picture: on the chief executive's dashboard a generated roll-up of the seats (one
tile per seat with its state, linking to its dashboard), then the seat's hand-written visual in the part slot
<!-- seat-extra:SEAT/signal --> (the Second brain and the search dashboard on CKO, the cost dashboards on CFO, the site
cards on CEO). The queue band holds what needs the seat: the decisions waiting on CEO, then the seat's items that are
not done. The state band holds the lens questions, the counts, and the chief executive's area tiles. The tools band is
the seat's own slot. The build refuses a part slot other than SEAT/signal that holds content, and a part slot of a seat
the seats file does not have, so nothing hand-written is dropped by a rebuild.

Without a script the cards are a plain list of links and every dashboard follows in order; the page script turns the
list into tabs. The Conformity checks job runs --check; the deploy job runs the build after the cockpit's fetch,
artifact only, so the tabs are as fresh as the cockpit. Stdlib only. Tests: python3 scripts/test_build_inside_seats.py.
"""
import re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cockpit as bc, build_ledger as bl, build_masthead as bm, build_pipeline as bp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE_REL = 'inside/index.html'
PAGE = ROOT / PAGE_REL
BLOCK = 'inside-seats'
CEO = 'ceo'  # the seat that reads every area (ADR-0032)
# The pane grammar (ADR-0049): the blocks of every dashboard in one fixed order, by band. A name is a generated block;
# '/signal' is the seat's hand-written visual, the part slot <!-- seat-extra:SEAT/signal -->. The seat's own slot comes
# last, as the tools band. A block a seat has nothing for renders as nothing.
BANDS = (('signal', ['rollup', '/signal']), ('queue', ['decisions', 'work', 'ledger', 'pipeline', 'pending']),
         ('state', ['lens', 'kpis', 'areas']))
ORDER = [n for _, names in BANDS for n in names]
PARTS = ('signal',)  # the part slots a seat may hold content in

# Panels with no data source yet: a title and one line, shown as a labelled placeholder with no number. Empty since
# ADR-0050 wired the publisher's pipeline; the mechanism stays for the next seat that gets a panel before its data.
PENDING = {}

STATUS = {'blocked': ('blocked', 'is-bad'), 'in_progress': ('in progress', 'is-warn'), 'open': ('open', 'is-open')}

esc, plural = bc.esc, bc.plural


def tally(items):
    """Open, in progress, and blocked now; done in the cockpit's window (the data keeps no older closed item)."""
    c = {s: sum(1 for x in items if x['status'] == s) for s in bc.OPEN_STATUSES}
    c['done'] = sum(1 for x in items if x['status'] == 'done')
    return c


def live(items):
    return sorted((x for x in items if x['status'] in bc.OPEN_STATUSES),
                  key=lambda x: (bc.STATUS_ORDER[x['status']], x['created'], x['repo'], x['number']))


def code(s):
    return s['seat'].upper()


def areas_label(s, titles):
    names = ' · '.join(esc(titles[a]) for a in s['areas'])
    return names + (' · reads every area' if s['seat'] == CEO else '')


def scope(s, ck):
    """The items the seat's counts cover: every area for the chief executive, the seat's own areas for the others."""
    return ck['items'] if s['seat'] == CEO else [x for x in ck['items'] if x['area'] in s['areas']]


def state(c):
    """The tab's one status (ADR-0036): blocked beats open beats clear; in progress shows in the panel, not the tab.
    Returns (css class, full label, count-only label)."""
    if c['blocked']:
        return 'is-bad', f'{c["blocked"]} blocked', str(c['blocked'])
    if c['open']:
        return 'is-open', f'{c["open"]} open', str(c['open'])
    return 'is-ok', 'clear', '0'


def pill(c):
    """The status pill on a tab: the full label on a wide screen, the count alone (0 for clear) on a phone. Hidden from
    a screen reader, which reads the tab's title and state from the mb-sr text instead, so the state is not said twice."""
    sty, long, short = state(c)
    return (f'<span class="in-pill {sty}" aria-hidden="true"><span class="in-pill-long">{long}</span>'
            f'<span class="in-pill-short">{short}</span></span>')


def short_code(s):
    """PUBLISHER is too wide for a phone tab, so it shows as PUB there; every other code is short already."""
    return 'PUB' if s['seat'] == 'publisher' else code(s)


def cls(name, on):
    return f' class="{name}"' if on else ''


def card(s, ck):
    """A folder tab (ADR-0036): the seat code and one status pill, visible; the full title and state for a screen
    reader. The areas and the counts live in the dashboard below, not on the tab."""
    k, c = esc(s['seat']), tally(scope(s, ck))
    _, long, _ = state(c)
    return (f'<li><a class="in-seat" id="in-tab-{k}" href="#seat-{k}" aria-controls="seat-{k}">'
            f'<span class="in-seat-code" aria-hidden="true"><span class="in-code-long">{esc(code(s))}</span>'
            f'<span class="in-code-short">{esc(short_code(s))}</span></span>'
            f'{pill(c)}'
            f'<span class="mb-sr">{esc(s["title"])}, {long}</span></a></li>')


def kpis(c):
    cells = (('Open', c['open']), ('In progress', c['in_progress']), ('Blocked', c['blocked']),
             (f'Done in {bc.WINDOW_DAYS} days', c['done']))
    return ('<dl class="in-kpis">' + ''.join(
        f'<div{cls("is-bad", k == "Blocked" and v)}><dt>{k}</dt><dd>{v}</dd></div>' for k, v in cells) + '</dl>')


def row(x, titles):
    text, cls = STATUS[x['status']]
    kind = f' · {esc(x["kind"])}' if x['kind'] else ''
    return (f'<li class="in-item"><span class="in-pill {cls}">{text}</span>'
            f'<span class="in-item-main"><a href="{esc(x["url"])}">{esc(x["title"])}</a>'
            f'<span class="in-item-meta">{esc(bc.short(x["repo"]))}#{x["number"]} · {"pull request" if x["pr"] else "issue"} · '
            f'{esc(titles[x["area"]])}{kind}</span></span>'
            f'<span class="in-item-date">opened {esc(x["created"])}</span></li>')


def rows(items, titles):
    return f'<ul class="in-items">{"".join(row(x, titles) for x in items)}</ul>'


def area_tiles(ck, titles):
    out = ''
    for a in bc.AREA_KEYS:
        c = tally([x for x in ck['items'] if x['area'] == a])
        out += (f'<li{cls("is-bad", c["blocked"])}><a href="/inside/cockpit/#{esc(a)}">{esc(titles[a])}</a>'
                f'<span>{c["open"]} open · {c["in_progress"]} in progress · {c["blocked"]} blocked</span></li>')
    return f'<ul class="in-areas">{out}</ul>'


def ledger_row(x, titles):
    text, cls = STATUS[x['status']]
    kind = f' · {esc(x["kind"])}' if x['kind'] else ''
    return (f'<li class="in-item"><span class="in-pill {cls}">{text}</span>'
            f'<span class="in-item-main">{esc(x["title"])}'
            f'<span class="in-item-meta">ledger {esc(x["id"])} · {esc(titles[x["area"]])}{kind}</span></span>'
            f'<span class="in-item-date">opened {esc(x["created"])}</span></li>')


def ledger_block(s, led, titles):
    """The house ledger in a seat's queue band (ADR-0050): the records not done for the seat's areas (every area for the
    chief executive), blocked first, with the done count and the export time in the heading. A seat with no record in
    its areas gets nothing; one with records but none open gets the done count on one line."""
    mine = [x for x in led['items'] if s['seat'] == CEO or x['area'] in s['areas']]
    if not mine:
        return ''
    done, when = bl.tally(mine)['done'], esc(bl.stamp(led))
    names = ' · '.join(esc(titles[a]) for a in s['areas']) if s['seat'] != CEO else 'every area'
    open_ = bl.live(mine)
    if not open_:
        where = 'any area' if s['seat'] == CEO else names
        return (f'<p class="in-empty">House ledger: nothing open in {where}; {plural(done, "record")} done in '
                f'{bl.WINDOW_DAYS} days, as of {when}.</p>')
    return (f'<h3>House ledger, not done <span class="in-h-meta">{names} · {plural(done, "record")} done in '
            f'{bl.WINDOW_DAYS} days · as of {when}, the last export</span></h3>'
            f'<ul class="in-items in-ledger">{"".join(ledger_row(x, titles) for x in open_)}</ul>')


def slot(name, extras):
    return f'<!-- seat-extra:{name} -->{extras.get(name, "")}<!-- /seat-extra:{name} -->'


def rollup(seats, ck):
    """The chief executive's signal (ADR-0049): one tile per seat in masthead order, the seat code, its title, and its
    state in the tab's pill rule, linking to the seat's dashboard; the counts behind the pill on one line beneath. The
    heading says how fresh the counts are."""
    out = ''
    for s in seats:
        k, c = esc(s['seat']), tally(scope(s, ck))
        sty, long, _ = state(c)
        out += (f'<li{cls("is-bad", c["blocked"])}><a href="#seat-{k}"><span class="in-rollup-code">{esc(code(s))}</span>'
                f'<span class="in-rollup-title">{esc(s["title"])}</span><span class="in-pill {sty}">{long}</span></a>'
                f'<span>{c["open"]} open · {c["in_progress"]} in progress · {c["blocked"]} blocked · '
                f'{c["done"]} done in {bc.WINDOW_DAYS} days</span></li>')
    return (f'<h3>Seats <span class="in-h-meta">one tile per seat · counts as of {esc(bc.stamp(ck))}</span></h3>'
            f'<ul class="in-rollup">{out}</ul>')


def panel(s, ck, titles, extras=None, seats=None, led=None, pipe=None):
    k = esc(s['seat'])
    extras, led, pipe = extras or {}, led or bl.empty(), pipe or bp.empty()
    own = [x for x in ck['items'] if x['area'] in s['areas']]
    parts = {n: '' for n in ORDER}
    parts['lens'] = (f'<div class="in-lens"><p class="in-label">Lens · the questions for every item in this seat</p>'
                     f'<ol>{"".join(f"<li>{esc(q)}</li>" for q in s["lens"])}</ol></div>')
    parts['kpis'] = kpis(tally(scope(s, ck)))
    if s['seat'] == CEO:
        waiting = [x for x in live(ck['items']) if x['kind'] == 'decision']
        parts['rollup'] = rollup(seats or [s], ck)
        parts['decisions'] = ('<h3>Decisions waiting</h3>'
                              + (rows(waiting, titles) if waiting else '<p class="in-empty">No open decision with an area label.</p>'))
        parts['areas'] = f'<h3>Areas</h3>{area_tiles(ck, titles)}'
    mine = live(own)
    names = ' · '.join(esc(titles[a]) for a in s['areas'])
    if mine:
        parts['work'] = f'<h3>Not done, blocked first <span class="in-h-meta">{names}</span></h3>{rows(mine, titles)}'
    else:
        done = tally(own)['done']
        parts['work'] = (f'<p class="in-empty">Nothing open in this seat\'s areas ({names}). {plural(done, "item")} done there in '
                 f'the last {bc.WINDOW_DAYS} days.</p>')
    parts['ledger'] = ledger_block(s, led, titles)
    if s['seat'] == 'publisher':
        parts['pipeline'] = bp.block(pipe)
    if s['seat'] in PENDING:
        name, line = PENDING[s['seat']]
        parts['pending'] = (f'<div class="in-pending"><p class="in-label">{esc(name)} · not wired yet</p><p>{esc(line)}</p></div>')
    body = ''.join(slot(f'{k}{n}', extras) if n.startswith('/') else parts[n] for n in ORDER)
    # The holder is named on a seat line only where the seats differ; with one holder the seats sentence names them once.
    holder = f'holder {esc(s["holder"])} · ' if len({x['holder'] for x in seats or [s]}) > 1 else ''
    return (f'<section class="in-panel" id="seat-{k}" aria-labelledby="seat-{k}-h">'
            f'<div class="in-panel-head"><div><p class="in-label in-accent">{esc(code(s))} dashboard</p>'
            f'<h2 id="seat-{k}-h">{esc(s["title"])}</h2></div>'
            f'<p class="in-panel-meta">{holder}{areas_label(s, titles)}</p></div>'
            f'{body}{slot(k, extras)}</section>')


def b_seats(doc, ck, extras=None, led=None, pipe=None):
    extras, led, pipe = extras or {}, led or bl.empty(), pipe or bp.empty()
    titles, who = bm.area_titles(), bm.holders(doc)
    if len(who) == 1:
        sub = f'One holder in every seat today: {esc(who[0])}.'
    else:
        sub = f'{plural(len(who), "holder")} across {plural(len(doc["seats"]), "seat")} today.'
    sub += (' A seat that moves to another person is one changed line in the <a href="/inside/masthead/">seats file</a>.')
    return (f'<section class="in-sec" id="seats" aria-labelledby="in-seats-h">'
            f'<div class="in-sec-head"><h2 id="in-seats-h">Seats</h2><p>{sub}</p></div>'
            f'<ul class="in-seat-tabs" aria-label="Seat dashboards">{"".join(card(s, ck) for s in doc["seats"])}</ul>'
            f'</section>'
            f'<div class="in-panels">{"".join(panel(s, ck, titles, extras, doc["seats"], led, pipe) for s in doc["seats"])}</div>'
            f'<p class="in-note">Counts and items: the issues and pull requests with an area label in the public '
            f'<a href="/inside/cockpit/">cockpit</a> data as of {bc.stamp(ck)}; done counts those closed as completed or '
            f'merged in the {bc.WINDOW_DAYS} days to then. Seats, holders, areas, and lens questions: the '
            f'<a href="/inside/masthead/">masthead</a>.{sources(led, pipe)}</p>')


def sources(led, pipe):
    """The sentence on the two vault sources (ADR-0050), with each file's export time; nothing when neither has a record."""
    out = []
    if led['items']:
        out.append(f'the house ledger, the vault\'s bead records with the label public, as of {esc(bl.stamp(led))} '
                   f'(<a href="/inside/board/ledger.json">ledger.json</a>, shown in full on the <a href="/inside/board/#ledger-h">board</a>)')
    if pipe['pieces']:
        out.append(f'the publishing pipeline, the drafts with a public teaser, as of {esc(bp.stamp(pipe))} '
                   f'(<a href="/inside/publisher/pipeline.json">pipeline.json</a>)')
    if not out:
        return ''
    return ' From the knowledge vault, exported on the holder\'s machine and committed: ' + '; '.join(out) + '.'


def block_rx():
    return re.compile(rf'<!-- static:{BLOCK} -->(.*?)<!-- /static:{BLOCK} -->', re.S)


def block(src):
    found = block_rx().findall(src)
    if len(found) != 1:
        raise SystemExit(f'build_inside_seats: {PAGE_REL} has {len(found)} <!-- static:{BLOCK} --> blocks, want 1')
    return found[0]


def slots(text):
    """The hand-written content of each slot in a block, by slot name: the seat key, or 'seat/part'."""
    return {m.group(1): m.group(2) for m in re.finditer(r'<!-- seat-extra:(\w+(?:/\w+)?) -->(.*?)<!-- /seat-extra:\1 -->', text, re.S)}


def put_block(src, doc, ck, led=None, pipe=None):
    found = slots(block(src))
    keys = {s['seat'] for s in doc['seats']}
    lost = sorted(k for k, v in found.items()
                  if '/' in k and v.strip() and (k.split('/', 1)[0] not in keys or k.split('/', 1)[1] not in PARTS))
    if lost:
        raise SystemExit(f'build_inside_seats: {PAGE_REL} holds content in slot {", ".join(lost)}, which the pane grammar '
                         f'(ADR-0049) has no place for; a rebuild would drop it. Move the content to the seat\'s signal slot '
                         f'(SEAT/signal) or its own slot (SEAT)')
    body = b_seats(doc, ck, found, led, pipe)
    return block_rx().sub(lambda _: f'<!-- static:{BLOCK} -->{body}<!-- /static:{BLOCK} -->', src, count=1)


def report(msg):
    print(f'build_inside_seats: {msg}')


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv not in ([], ['--check']):
        print('usage: build_inside_seats.py [--check]', file=sys.stderr)
        return 2
    try:
        doc = bm.load(bm.DATA)
    except bm.ContractError as e:
        print(f'build_inside_seats: {bm.DATA.name} breaks the seats contract (ADR-0032):', file=sys.stderr)
        for line in str(e).splitlines():
            print('  ' + line, file=sys.stderr)
        return 1
    try:
        ck = bc.load(bc.DATA)
    except bc.ContractError as e:
        print(f'build_inside_seats: {bc.DATA.name} breaks the cockpit contract (ADR-0031):', file=sys.stderr)
        for line in str(e).splitlines():
            print('  ' + line, file=sys.stderr)
        return 1
    try:
        led = bl.load(bl.DATA)
    except bl.ContractError as e:
        print(f'build_inside_seats: {bl.DATA.name} breaks the ledger contract (ADR-0050):', file=sys.stderr)
        for line in str(e).splitlines():
            print('  ' + line, file=sys.stderr)
        return 1
    try:
        pipe = bp.load(bp.DATA)
    except bp.ContractError as e:
        print(f'build_inside_seats: {bp.DATA.name} breaks the pipeline contract (ADR-0050):', file=sys.stderr)
        for line in str(e).splitlines():
            print('  ' + line, file=sys.stderr)
        return 1
    page = PAGE.read_text(encoding='utf-8')
    new = put_block(page, doc, ck, led, pipe)
    summary = (f'{plural(len(doc["seats"]), "seat")}, cockpit data of {ck["generated"]}, ledger of {led["generated"]} '
               f'({plural(len(led["items"]), "record")}), pipeline of {pipe["generated"]} ({plural(len(pipe["pieces"]), "piece")})')
    if argv == ['--check']:
        same = block(page) == block(new)
        if not same:
            report(f'the {BLOCK} block of {PAGE_REL} differs from what seats.json and cockpit.json give')
        report(f'{summary}; ' + ('page up to date' if same else 'run python3 scripts/build_inside_seats.py'))
        return 0 if same else 1
    if new != page:
        PAGE.write_text(new, encoding='utf-8')
    report(f'{PAGE_REL} written: {summary}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
