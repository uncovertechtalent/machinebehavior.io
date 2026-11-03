#!/usr/bin/env python3
"""Tests for the six request forms in .github/ISSUE_TEMPLATE/ and their links on the Inside landing page (ADR-0052).

One form per seat of inside/masthead/seats.json, in masthead order, named request-<seat>.yml. Each form is read with
scripts/mini_yaml.py (GitHub renders the file; this checks the shape GitHub needs and the shape the ADR fixes): the name
"Request: <seat title>", a one-sentence description, exactly one label that is the seat's first area and one of the
cockpit's eight, no title prefix, and the body in order (a markdown rule line, What, Why, Blocked on, Done when,
Constraints, Kind, the public checkbox) with the ids, the required flags, and the Kind options the ADR fixes. Every id is
unique and GitHub-legal, and no copy holds an em dash. A config.yml, if the folder has one, keeps blank issues on and
names no contact link (ADR-0010). The landing page holds, in each seat's tools slot, one Request card whose link opens
that seat's form. A mutated copy of a form must fail each rule. Stdlib only.

    python3 scripts/test_issue_forms.py

Exits 1 when a case fails.
"""
import copy, json, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cockpit as bc  # noqa: E402
import mini_yaml  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / '.github' / 'ISSUE_TEMPLATE'
SEATS = ROOT / 'inside' / 'masthead' / 'seats.json'
PAGE = ROOT / 'inside' / 'index.html'
REPO_URL = 'https://github.com/uncovertechtalent/machinebehavior.io'
RULE = ('Issue text is public. Leave out private addresses, host names, personal and financial details. '
        'List prices, specs, and measured results are fine.')
KINDS = ['decision', 'action', 'finding']
# (type, id, label, required) in body order after the markdown rule line; None where GitHub has no such key
FIELDS = [('textarea', 'what', 'What', True), ('textarea', 'why', 'Why', True),
          ('textarea', 'blocked_on', 'Blocked on', True), ('textarea', 'done_when', 'Done when', True),
          ('textarea', 'constraints', 'Constraints', False), ('dropdown', 'kind', 'Kind', True),
          ('checkboxes', 'public', None, None)]
TOP_KEYS = {'name', 'description', 'labels', 'body'}  # no title prefix, no assignees, no projects
ID_RX = re.compile(r'[A-Za-z0-9_-]+')


def seats():
    return json.loads(SEATS.read_text())['seats']


def problems(form, seat):
    """Everything wrong with one parsed form for one seat of the seats file; [] when it holds the ADR's shape."""
    p = []
    if not isinstance(form, dict) or set(form) != TOP_KEYS:
        return [f'top-level keys {sorted(form) if isinstance(form, dict) else form!r}, want {sorted(TOP_KEYS)}']
    if form['name'] != f"Request: {seat['title']}":
        p.append(f"name {form['name']!r}")
    d = form['description']
    if not isinstance(d, str) or not d.endswith('.') or d.count('. ') or len(d) > 240:
        p.append('description is not one sentence of at most 240 characters')
    want = ['area:' + seat['areas'][0]]
    if form['labels'] != want or form['labels'][0][5:] not in bc.AREA_KEYS:
        p.append(f"labels {form['labels']!r}, want {want}")
    body = form['body']
    if not isinstance(body, list) or len(body) != len(FIELDS) + 1:
        return p + [f'body has {len(body) if isinstance(body, list) else body!r} items, want {len(FIELDS) + 1}']
    md = body[0]
    if md.get('type') != 'markdown' or 'id' in md or md.get('attributes') != {'value': RULE}:
        p.append('first body item is not the markdown rule line')
    seen = set()
    for item, (typ, ident, label, required) in zip(body[1:], FIELDS):
        where = ident
        if item.get('type') != typ or item.get('id') != ident:
            p.append(f'{where}: type/id {item.get("type")!r}/{item.get("id")!r}')
            continue
        if not ID_RX.fullmatch(ident) or ident in seen:
            p.append(f'{where}: id is not unique and alphanumeric')
        seen.add(ident)
        a = item.get('attributes', {})
        if label is not None and a.get('label') != label:
            p.append(f'{where}: label {a.get("label")!r}')
        if typ != 'checkboxes' and not isinstance(a.get('description'), str):
            p.append(f'{where}: no description')
        if typ == 'checkboxes':
            opts = a.get('options')
            if opts != [{'label': 'This text holds nothing private.', 'required': True}] or 'validations' in item:
                p.append(f'{where}: want one required option "This text holds nothing private." and no validations')
        else:
            if item.get('validations') != {'required': required}:
                p.append(f'{where}: validations {item.get("validations")!r}, want required={required}')
        if typ == 'dropdown':
            if a.get('options') != KINDS or 'maintainer' not in a.get('description', ''):
                p.append(f'{where}: want options {KINDS} and a description that names the maintainer')
    for text in strings(form):
        if '\u2014' in text or '\u2013' in text:
            p.append(f'dash in {text[:40]!r}')
    return p


def strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from strings(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from strings(x)


def main():
    failures = []

    def ok(name, cond, detail=''):
        if not cond:
            failures.append(name)
            print(f'FAIL {name} {detail}')

    ss = seats()
    keys = [s['seat'] for s in ss]
    forms = {}

    # 1. One form per seat, nothing else named request-*, and each form holds the shape
    names = sorted(p.name for p in FORMS.glob('request-*.yml'))
    ok('one request form per seat', names == sorted(f'request-{k}.yml' for k in keys), str(names))
    for s in ss:
        path = FORMS / f'request-{s["seat"]}.yml'
        if not path.exists():
            continue
        try:
            forms[s['seat']] = mini_yaml.load(path.read_text(), path.name)
        except mini_yaml.YamlError as e:
            ok(f'{path.name} parses', False, str(e))
            continue
        pr = problems(forms[s['seat']], s)
        ok(f'{path.name} holds the shape', not pr, '; '.join(pr))

    # 2. The six bodies are the same except for the name, the description, and the label
    if len(forms) == len(keys):
        bodies = {json.dumps(f['body'], sort_keys=True) for f in forms.values()}
        ok('the six bodies are identical', len(bodies) == 1, f'{len(bodies)} distinct bodies')
        ok('the six descriptions differ', len({f['description'] for f in forms.values()}) == len(keys))

    # 3. The folder keeps blank issues and names no third party (ADR-0010)
    cfg = FORMS / 'config.yml'
    if cfg.exists():
        c = mini_yaml.load(cfg.read_text(), 'config.yml')
        ok('config.yml keeps blank issues on', c.get('blank_issues_enabled') is True, str(c))
        ok('config.yml names no contact link', 'contact_links' not in c, str(c))

    # 4. The landing page: one Request card per tools slot, linking to that seat's form, the same card on every seat
    html = PAGE.read_text()
    cards = []
    for k in keys:
        m = re.search(r'<!-- seat-extra:%s -->(.*?)<!-- /seat-extra:%s -->' % (k, k), html, re.S)
        ok(f'{k}: tools slot exists', m is not None)
        if not m:
            continue
        slot = m.group(1)
        link = f'{REPO_URL}/issues/new?template=request-{k}.yml'
        ok(f'{k}: one link to its form', slot.count(f'href="{link}"') == 1, slot.count(link))
        ok(f'{k}: no link to another seat form', len(re.findall(r'template=request-', slot)) == 1)
        card = re.search(r'<section class="card" aria-labelledby="req-%s">(.*?)</section>' % k, slot, re.S)
        ok(f'{k}: Request card', card is not None)
        if card:
            ok(f'{k}: Request card is last in the slot', slot.rstrip().endswith('</section>') and slot.rstrip().rfind('<section') == card.start())
            cards.append(card.group(1).replace(k, 'SEAT'))
    ok('the Request card is the same on every seat', len(set(cards)) == 1, f'{len(set(cards))} variants')
    ok('every card id is unique on the page', all(html.count(f'id="req-{k}"') == 1 for k in keys))

    # 5. A mutated copy of a form fails each rule
    if keys and keys[0] in forms:
        s = ss[0]
        base = forms[s['seat']]

        def fails(name, mut):
            f = copy.deepcopy(base)
            mut(f)
            ok(f'mutation fails: {name}', problems(f, s) != [])

        fails('a title prefix', lambda f: f.__setitem__('title', '[Request] '))
        fails('another name', lambda f: f.__setitem__('name', 'Request'))
        fails('a second label', lambda f: f['labels'].append('kind:action'))
        fails('a label outside the areas', lambda f: f.__setitem__('labels', ['area:docs']))
        fails('a space after the colon', lambda f: f.__setitem__('labels', ['area: direction']))
        fails('a missing field', lambda f: f['body'].pop(3))
        fails('fields in another order', lambda f: f['body'].insert(1, f['body'].pop(2)))
        fails('Why not required', lambda f: f['body'][2]['validations'].__setitem__('required', False))
        fails('Constraints required', lambda f: f['body'][5]['validations'].__setitem__('required', True))
        fails('another Kind option', lambda f: f['body'][6]['attributes']['options'].append('lead'))
        fails('an optional public box', lambda f: f['body'][7]['attributes']['options'][0].__setitem__('required', False))
        fails('a changed rule line', lambda f: f['body'][0]['attributes'].__setitem__('value', 'Be nice.'))
        fails('an em dash', lambda f: f['body'][1]['attributes'].__setitem__('description', 'One paragraph \u2014 no more.'))
        fails('a duplicated id', lambda f: f['body'][2].__setitem__('id', 'what'))
        fails('an extra top-level key', lambda f: f.__setitem__('assignees', ['someone']))

    if failures:
        print(f'{len(failures)} failed')
        return 1
    print('test_issue_forms: all cases pass')
    return 0


if __name__ == '__main__':
    sys.exit(main())
