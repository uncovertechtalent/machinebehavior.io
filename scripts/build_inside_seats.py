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

No new data source: the seats, holders, areas, and lens come from the seats contract (ADR-0032), the items and the area
titles from the cockpit's (ADR-0031), each read through its own loader and check. A panel whose data source does not
exist yet (the publisher's pipeline) is a labelled placeholder with no number.

Each dashboard ends with a hand-written slot, <!-- seat-extra:SEAT --> ... <!-- /seat-extra:SEAT -->: the cards and tools
that belong to the seat (deploy feed, apps, front page and the like). The build writes everything else in the block and
carries each slot's content over from the page unchanged, so the slots are edited by hand in inside/index.html.

A seat can also name the order of its panel in LAYOUT, to put a hand-written card above generated blocks: the card
sits in a part slot, <!-- seat-extra:SEAT/PART -->, which the layout lists next to the generated blocks. A seat without a
layout keeps the order above.

Without a script the cards are a plain list of links and every dashboard follows in order; the page script turns the
list into tabs. The Conformity checks job runs --check; the deploy job runs the build after the cockpit's fetch,
artifact only, so the tabs are as fresh as the cockpit. Stdlib only. Tests: python3 scripts/test_build_inside_seats.py.
"""
import re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cockpit as bc, build_masthead as bm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE_REL = 'inside/index.html'
PAGE = ROOT / PAGE_REL
BLOCK = 'inside-seats'
CEO = 'ceo'  # the seat that reads every area (ADR-0032)
# Panel order for the seats that move something. A name is a generated block (lens, kpis, areas, work, pending) or a
# hand-written part slot written 'seat/part'; blocks and slots not named keep their default order after the named ones,
# the seat's own slot last. A seat without an entry gets the default order.
LAYOUT = {
    'cko': ['cko/map', 'work', 'cko/dash'],
    'cfo': ['cfo/dash'],
}
DEFAULT_ORDER = ['lens', 'kpis', 'areas', 'work', 'pending']

# Panels with no data source yet: a title and one line, shown as a labelled placeholder with no number.
PENDING = {
    'publisher': ('Publishing pipeline', 'Drafts, pieces in review, and pieces live this week. No public data source '
                  'feeds this panel yet, so it shows no count.'),
}

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


def slot(name, extras):
    return f'<!-- seat-extra:{name} -->{extras.get(name, "")}<!-- /seat-extra:{name} -->'


def panel(s, ck, titles, extras=None, layout=None):
    k = esc(s['seat'])
    extras = extras or {}
    own = [x for x in ck['items'] if x['area'] in s['areas']]
    parts = {'lens': (f'<div class="in-lens"><p class="in-label">Lens · the questions for every item in this seat</p>'
                      f'<ol>{"".join(f"<li>{esc(q)}</li>" for q in s["lens"])}</ol></div>'),
             'kpis': kpis(tally(scope(s, ck))), 'areas': '', 'pending': ''}
    if s['seat'] == CEO:
        waiting = [x for x in live(ck['items']) if x['kind'] == 'decision']
        parts['areas'] = (f'<h3>Areas</h3>{area_tiles(ck, titles)}<h3>Decisions waiting</h3>'
                 + (rows(waiting, titles) if waiting else '<p class="in-empty">No open decision with an area label.</p>'))
    mine = live(own)
    names = ' · '.join(esc(titles[a]) for a in s['areas'])
    if mine:
        parts['work'] = f'<h3>Not done, blocked first <span class="in-h-meta">{names}</span></h3>{rows(mine, titles)}'
    else:
        done = tally(own)['done']
        parts['work'] = (f'<p class="in-empty">Nothing open in this seat\'s areas ({names}). {plural(done, "item")} done there in '
                 f'the last {bc.WINDOW_DAYS} days.</p>')
    if s['seat'] in PENDING:
        name, line = PENDING[s['seat']]
        parts['pending'] = (f'<div class="in-pending"><p class="in-label">{esc(name)} · not wired yet</p><p>{esc(line)}</p></div>')
    named = (LAYOUT if layout is None else layout).get(s['seat'], [])
    order = named + [n for n in DEFAULT_ORDER if n not in named]
    body = ''.join(slot(n, extras) if '/' in n else parts[n] for n in order)
    return (f'<section class="in-panel" id="seat-{k}" aria-labelledby="seat-{k}-h">'
            f'<div class="in-panel-head"><div><p class="in-label in-accent">{esc(code(s))} dashboard</p>'
            f'<h2 id="seat-{k}-h">{esc(s["title"])}</h2></div>'
            f'<p class="in-panel-meta">holder {esc(s["holder"])} · {areas_label(s, titles)}</p></div>'
            f'{body}{slot(k, extras)}</section>')


def b_seats(doc, ck, extras=None, layout=None):
    extras = extras or {}
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
            f'<div class="in-panels">{"".join(panel(s, ck, titles, extras, layout) for s in doc["seats"])}</div>'
            f'<p class="in-note">Counts and items: the issues and pull requests with an area label in the public '
            f'<a href="/inside/cockpit/">cockpit</a> data as of {bc.stamp(ck)}; done counts those closed as completed or '
            f'merged in the {bc.WINDOW_DAYS} days to then. Seats, holders, areas, and lens questions: the '
            f'<a href="/inside/masthead/">masthead</a>.</p>')


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


def put_block(src, doc, ck):
    body = b_seats(doc, ck, slots(block(src)))
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
    page = PAGE.read_text(encoding='utf-8')
    new = put_block(page, doc, ck)
    summary = f'{plural(len(doc["seats"]), "seat")}, cockpit data of {ck["generated"]}'
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
