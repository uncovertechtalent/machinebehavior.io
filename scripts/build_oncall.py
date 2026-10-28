#!/usr/bin/env python3
"""The on-call snapshot on /inside/docs/obs/on-call/ and /inside/docs/sre/principle-standby/ (#36, ADR-0037).

    python3 scripts/build_oncall.py --fetch    read the rotation and the pager records from GitHub, check, and write
                                               inside/oncall/oncall.json
    python3 scripts/build_oncall.py            rewrite oncall.json from its own data (no network): new html, same data
    python3 scripts/build_oncall.py --check    write nothing; exit 1 when oncall.json breaks the contract or its html
                                               differs from what its data renders (no network)

The deploy job runs --fetch (artifact only, never committed); a failed read or check leaves the committed snapshot live.
The Conformity checks job runs --check. The docs build embeds the committed snapshot's html at the marker
<!-- oncall-snapshot -->, and docs.js swaps in the deploy job's fresh copy, so the pages need no request to GitHub.

Both sources are public:
- pager/rotation.yml in uncovertechtalent/agent-observability (main): people by name, schedules, the escalation policy,
  overrides. Read with scripts/mini_yaml.py, which refuses anything outside its subset.
- the pager records on this repository's alert issues: a JSON list in an HTML comment `<!-- pager-record [...] -->`,
  which the pager writes through alert-issues. An issue counts only when the machine account opened it and a
  maintainer label (kind:finding) is on it, so text a stranger writes never reaches the page.
What reaches the page: names from the rotation, alert names, times and durations. check() allows exactly the keys and
forms of the contract; no Discord ID, channel or token exists in either source.
Stdlib only. Tests: python3 scripts/test_build_oncall.py.
"""
import datetime, html, json, os, re, statistics, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mini_yaml  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'inside' / 'oncall' / 'oncall.json'
REPO = 'uncovertechtalent/machinebehavior.io'
ROTATION_URL = 'https://raw.githubusercontent.com/uncovertechtalent/agent-observability/main/pager/rotation.yml'
BOT = 'uncovertechtalent'
ROLE = 'Operator'  # what a table cell calls the site's owner (the docs: "the operator")
WEEKS, LAST_PAGES = 8, 20
DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
RECORD = re.compile(r'<!-- pager-record (\[.*?\]) -->', re.S)
ISO = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ')
NAME = re.compile(r"[\w .,'()-]{1,80}")
DRILL = re.compile(r'PagerTest.*')  # test pages: listed as drills, left out of the weekly load
ALERT = re.compile(r'[A-Za-z_:][A-Za-z0-9_:]{0,99}')


class ContractError(ValueError):
    pass


def utc(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))


def iso(dt):
    return dt.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def minutes_of(s):
    m = re.fullmatch(r'(\d+)([smhd])', str(s))
    if not m:
        raise ContractError(f'bad duration {s!r}')
    return int(m[1]) * {'s': 1 / 60, 'm': 1, 'h': 60, 'd': 1440}[m[2]]


# ------------------------------------------------------------------ the rotation (same rules as the pager's core.py)

def hhmm(s):
    h, m = str(s).split(':')
    return datetime.time(int(h), int(m))


def allows(r, local):
    days, start, end = {DAYS.index(d) for d in r.get('days', DAYS)}, hhmm(r['from']), hhmm(r['to'])
    t, d = local.time(), local.weekday()
    if start < end:
        return d in days and start <= t < end
    if t >= start:
        return d in days
    return t < end and (d - 1) % 7 in days


def who(rot, schedule, at):
    """The person key on call for a schedule at a time: overrides first, then the last layer with someone."""
    tz = ZoneInfo(rot.get('timezone', 'UTC'))
    for o in sorted(rot.get('overrides') or [], key=lambda o: o['start'], reverse=True):
        start = datetime.datetime.fromisoformat(o['start']).replace(tzinfo=tz)
        end = datetime.datetime.fromisoformat(o['end']).replace(tzinfo=tz)
        if o.get('schedule', rot['escalation_policy']['rules'][0]['schedule']) == schedule and start <= at < end:
            return o['person']
    for layer in reversed(rot['schedules'][schedule].get('layers') or []):
        if layer.get('restrictions') and not any(allows(r, at.astimezone(tz)) for r in layer['restrictions']):
            continue
        members = layer['members']
        start = datetime.datetime.fromisoformat(layer.get('start', '2026-01-05T00:00')).replace(tzinfo=tz)
        turn = datetime.timedelta(minutes=minutes_of(layer.get('turn', '7d')))
        return members[int(max(0, (at - start) // turn)) % len(members)]
    return None


def hours_text(layer):
    rs = layer.get('restrictions') or []
    if not rs:
        return 'all hours'
    out = []
    for r in rs:
        days = r.get('days', DAYS)
        when = 'every day' if len(days) == 7 else ', '.join(DAY_NAMES[DAYS.index(d)] for d in days)
        out.append(f'{when} {r["from"]} to {r["to"]}')
    return '; '.join(out)


def from_rotation(rot, now):
    people = rot['people']
    name = lambda k: people[k]['name'] if k in people else None  # noqa: E731
    on_call, layers = [], []
    for sched, s in rot['schedules'].items():
        p = who(rot, sched, now)
        on_call.append({'schedule': sched, 'description': ' '.join(str(s.get('description', '')).split()),
                        'person': name(p), 'kind': people[p]['kind'] if p else None})
        for lay in s.get('layers') or []:
            layers.append({'schedule': sched, 'name': lay['name'], 'members': [name(m) for m in lay['members']],
                           'hours': hours_text(lay)})
    pol = rot['escalation_policy']
    policy = {'name': pol.get('name', 'default'),
              'steps': [{'after_min': int(minutes_of(r['after'])), 'schedule': r['schedule']} for r in pol['rules']],
              'renotify_min': int(minutes_of(pol.get('renotify_after', '5m'))),
              'renotify_limit': int(pol.get('renotify_limit', 3))}
    tz = ZoneInfo(rot.get('timezone', 'UTC'))
    overrides = []
    for o in rot.get('overrides') or []:
        end = datetime.datetime.fromisoformat(o['end']).replace(tzinfo=tz)
        if end > now:
            overrides.append({'person': name(o['person']), 'schedule': o.get('schedule', pol['rules'][0]['schedule']),
                              'start': iso(datetime.datetime.fromisoformat(o['start']).replace(tzinfo=tz)), 'end': iso(end)})
    return {'timezone': rot.get('timezone', 'UTC'), 'on_call': on_call, 'layers': layers, 'policy': policy,
            'overrides': overrides}


# ------------------------------------------------------------------ the pager records

def records_from_issue(issue):
    """The pager records on one issue, or [] when the issue does not qualify."""
    if (issue.get('user') or {}).get('login') != BOT or 'pull_request' in issue:
        return []
    if 'kind:finding' not in {l['name'] for l in issue.get('labels', [])}:
        return []
    m = RECORD.search(issue.get('body') or '')
    if not m:
        return []
    try:
        views = json.loads(m.group(1))
    except ValueError:
        return []
    return [v for v in views if isinstance(v, dict)]


def page_rows(views, rot, now):
    primary = rot['escalation_policy']['rules'][0]['schedule']
    # Only names the rotation knows, or Alertmanager itself: anything else (an ID, a stranger's name) becomes None.
    known = {p['name'] for p in rot['people'].values()} | {'Alertmanager', 'Alertmanager (stale)'}
    rows = []
    for v in views:
        if not (isinstance(v.get('alert'), str) and ALERT.fullmatch(v['alert']) and isinstance(v.get('fired'), str)
                and ISO.fullmatch(v['fired'])):
            continue
        fired = utc(v['fired'])
        if fired < now - datetime.timedelta(weeks=WEEKS):
            continue
        clean = lambda x: x.replace('\u200b', '') if isinstance(x, str) else None  # noqa: E731
        num = lambda x: x if isinstance(x, int) and not isinstance(x, bool) and x >= 0 else None  # noqa: E731
        ack, res = clean(v.get('acknowledged_by')), clean(v.get('resolved_by'))
        rows.append({'alert': v['alert'], 'fired': v['fired'], 'drill': bool(DRILL.fullmatch(v['alert'])),
                     'acknowledged_by': ack if ack in known else None,
                     'time_to_acknowledge_s': num(v.get('time_to_acknowledge_s')),
                     'resolved_by': res if res in known else None,
                     'time_to_resolve_s': num(v.get('time_to_resolve_s')),
                     'responder_ran': v.get('responder_ran') is True,
                     'out_of_hours': who(rot, primary, fired) is None})
    rows.sort(key=lambda r: r['fired'], reverse=True)
    return rows


def weeks(rows, now):
    out = []
    for back in range(WEEKS - 1, -1, -1):
        y, w, _ = (now - datetime.timedelta(weeks=back)).isocalendar()
        key = f'{y}-W{w:02d}'
        mine = [r for r in rows if not r['drill'] and '{}-W{:02d}'.format(*utc(r['fired']).isocalendar()[:2]) == key]
        ttas = [r['time_to_acknowledge_s'] for r in mine if r['time_to_acknowledge_s'] is not None]
        out.append({'week': key, 'pages': len(mine), 'out_of_hours': sum(r['out_of_hours'] for r in mine),
                    'median_tta_s': int(statistics.median(ttas)) if ttas else None})
    return out


def build(rot, views, now):
    data = {'generated': iso(now), **from_rotation(rot, now)}
    rows = page_rows(views, rot, now)
    data['pages'] = rows[:LAST_PAGES]
    data['weeks'] = weeks(rows, now)
    data['html'] = render(data)
    check(data)
    return data


# ------------------------------------------------------------------ contract

SHAPE = {
    'generated': 'iso', 'timezone': 'tz', 'html': 'html',
    'on_call': [{'schedule': 'key', 'description': 'text', 'person': 'name?', 'kind': 'kind?'}],
    'layers': [{'schedule': 'key', 'name': 'name', 'members': ['name'], 'hours': 'text'}],
    'policy': {'name': 'name', 'steps': [{'after_min': 'int', 'schedule': 'key'}], 'renotify_min': 'int', 'renotify_limit': 'int'},
    'overrides': [{'person': 'name', 'schedule': 'key', 'start': 'iso', 'end': 'iso'}],
    'pages': [{'alert': 'alert', 'fired': 'iso', 'drill': 'bool', 'acknowledged_by': 'name?', 'time_to_acknowledge_s': 'int?',
               'resolved_by': 'name?', 'time_to_resolve_s': 'int?', 'responder_ran': 'bool', 'out_of_hours': 'bool'}],
    'weeks': [{'week': 'week', 'pages': 'int', 'out_of_hours': 'int', 'median_tta_s': 'int?'}],
}
FORMS = {
    'iso': lambda v: isinstance(v, str) and ISO.fullmatch(v),
    'tz': lambda v: isinstance(v, str) and re.fullmatch(r'[A-Za-z_]+(/[A-Za-z_]+)*', v),
    'key': lambda v: isinstance(v, str) and re.fullmatch(r'[a-z][a-z0-9_-]{0,39}', v),
    'name': lambda v: isinstance(v, str) and NAME.fullmatch(v) and not re.search(r'\d{15,}', v),
    'kind': lambda v: v in ('human', 'agent'),
    'text': lambda v: isinstance(v, str) and len(v) <= 300 and not re.search(r'[<>]|https?://|\d{15,}', v),
    'alert': lambda v: isinstance(v, str) and ALERT.fullmatch(v),
    'int': lambda v: isinstance(v, int) and not isinstance(v, bool) and v >= 0,
    'bool': lambda v: isinstance(v, bool),
    'week': lambda v: isinstance(v, str) and re.fullmatch(r'\d{4}-W\d\d', v),
    'html': lambda v: isinstance(v, str),
}


def check_shape(value, shape, where):
    if isinstance(shape, dict):
        if not isinstance(value, dict) or set(value) != set(shape):
            raise ContractError(f'{where}: keys {sorted(value) if isinstance(value, dict) else type(value).__name__}, want {sorted(shape)}')
        for k, s in shape.items():
            check_shape(value[k], s, f'{where}.{k}')
    elif isinstance(shape, list):
        if not isinstance(value, list) or len(value) > 200:
            raise ContractError(f'{where}: want a list')
        for i, v in enumerate(value):
            check_shape(v, shape[0], f'{where}[{i}]')
    else:
        optional = shape.endswith('?')
        if value is None and optional:
            return
        if not FORMS[shape.rstrip('?')](value):
            raise ContractError(f'{where}: {value!r} is not a {shape}')


def check(data):
    check_shape(data, SHAPE, 'oncall')
    if data['html'] != render(data):
        raise ContractError('oncall.html differs from what the data renders; run scripts/build_oncall.py')


# ------------------------------------------------------------------ html (escaped; the docs build and docs.js embed it)

def span(s):
    if s is None:
        return '-'
    m = s // 60
    return f'{m} min' if m < 120 else f'{m // 60} h {m % 60} min'


def operator():
    """The site's owner from site/nav.yml: the one human the rotation names. The tables show the role, not the name."""
    return mini_yaml.load_file(ROOT / 'site' / 'nav.yml')['site']['owner']


def render(data):
    e = html.escape
    owner = operator()

    def who(name, lead=True):
        return (ROLE if lead else ROLE.lower()) if name == owner else name
    out = ['<div class="oncall-snapshot">', '<h3>Rotation</h3>', '<div class="tbl"><table><thead><tr>'
           '<th>Schedule</th><th>On call at the snapshot</th><th>Layers</th></tr></thead><tbody>']
    for oc in data['on_call']:
        lays = '; '.join(f'{e(l["name"])}: {e(", ".join(who(m, False) for m in l["members"]))}, {e(l["hours"])}'
                         for l in data['layers'] if l['schedule'] == oc['schedule'])
        person = e(who(oc['person'])) + (' (agent)' if oc['kind'] == 'agent' else '') if oc['person'] else 'nobody'
        out.append(f'<tr><td>{e(oc["schedule"])}</td><td>{person}</td><td>{lays}</td></tr>')
    out.append('</tbody></table></div>')
    pol = data['policy']
    def delay(minutes):
        return 'At once' if minutes == 0 else f'After {minutes} minutes'
    steps = ''.join(f'<li>{delay(s["after_min"])}: {e(s["schedule"])}</li>' for s in pol['steps'])
    out += [f'<h3>Escalation policy: {e(pol["name"])}</h3>', f'<ol>{steps}</ol>',
            f'<p>Until somebody acknowledges, the person on call is mentioned again every {pol["renotify_min"]} '
            f'minutes, {pol["renotify_limit"]} times. A level with nobody on call passes the page on at once.</p>']
    if data['overrides']:
        out.append('<p>Overrides: ' + '; '.join(f'{e(who(o["person"], False))} on {e(o["schedule"])}, {o["start"][:16].replace("T", " ")} '
                                                 f'to {o["end"][:16].replace("T", " ")} UTC' for o in data['overrides']) + '.</p>')
    out.append('<h3>Last pages</h3>')
    if data['pages']:
        out.append('<div class="tbl"><table><thead><tr><th>Fired (UTC)</th><th>Alert</th><th>Acknowledged</th>'
                   '<th>Time to acknowledge</th><th>Resolved by</th><th>Time to resolve</th></tr></thead><tbody>')
        for p in data['pages']:
            when = p['fired'][:16].replace('T', ' ') + (' (out of hours)' if p['out_of_hours'] else '') + (' (drill)' if p['drill'] else '')
            ack = e(who(p['acknowledged_by'])) if p['acknowledged_by'] else ('responder only' if p['responder_ran'] else 'no')
            out.append(f'<tr><td>{when}</td><td><code>{e(p["alert"])}</code></td><td>{ack}</td>'
                       f'<td>{span(p["time_to_acknowledge_s"])}</td><td>{e(who(p["resolved_by"]) if p["resolved_by"] else "open")}</td>'
                       f'<td>{span(p["time_to_resolve_s"])}</td></tr>')
        out.append('</tbody></table></div>')
    else:
        out.append(f'<p>No page has gone through the pager in the last {WEEKS} weeks.</p>')
    out.append('<h3>Pager load per week</h3><p>Drills left out. Out of hours means nobody was on the primary schedule '
               'when the page fired, by the current rotation.</p><div class="tbl"><table><thead><tr><th>Week</th>'
               '<th>Pages</th><th>Out of hours</th><th>Median time to acknowledge</th></tr></thead><tbody>')
    for w in data['weeks']:
        out.append(f'<tr><td>{w["week"]}</td><td>{w["pages"]}</td><td>{w["out_of_hours"]}</td><td>{span(w["median_tta_s"])}</td></tr>')
    out.append('</tbody></table></div>')
    out.append(f'<p class="oncall-asof">Snapshot of {data["generated"][:16].replace("T", " ")} UTC. Rotation from '
               '<a href="https://github.com/uncovertechtalent/agent-observability/blob/main/pager/rotation.yml">pager/rotation.yml</a>; '
               'pages from the pager records on the alert issues of this repository.</p>')
    out.append('</div>')
    return '\n'.join(out)


# ------------------------------------------------------------------ GitHub

def fetch(url, raw=False):
    last = None
    for auth in (True, False):
        if auth and (raw or not os.environ.get('GH_TOKEN')):  # raw files are read without the token
            continue
        h = {'User-Agent': 'machinebehavior.io on-call snapshot'}
        if not raw:
            h['Accept'] = 'application/vnd.github+json'
        if auth and not raw:
            h['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=20) as r:
                body = r.read()
            return body.decode() if raw else json.loads(body)
        except (urllib.error.URLError, ValueError) as err:
            print(f'::warning::{url.split("?")[0]} (auth={auth}) failed: {err}')
            last = err
    raise SystemExit(f'on-call snapshot: read failed: {last}')


def fetch_views(now):
    since = iso(now - datetime.timedelta(weeks=WEEKS))
    views = []
    for page in range(1, 11):
        q = urllib.parse.urlencode({'labels': 'kind:finding', 'state': 'all', 'creator': BOT, 'since': since,
                                    'per_page': 100, 'page': page})
        batch = fetch(f'https://api.github.com/repos/{REPO}/issues?{q}')
        for issue in batch:
            views += records_from_issue(issue)
        if len(batch) < 100:
            break
    return views


def parse_rotation(text):
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.yml', delete=False) as f:
        f.write(text)
    try:
        return mini_yaml.load_file(f.name)
    finally:
        os.unlink(f.name)


def write(data):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n')


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    if '--fetch' in argv:
        rot = parse_rotation(fetch(ROTATION_URL, raw=True))
        data = build(rot, fetch_views(now), now)
        write(data)
        print(f'on-call snapshot: {len(data["pages"])} pages, on call now: '
              + ', '.join(f'{o["schedule"]}={o["person"] or "nobody"}' for o in data['on_call']))
        return 0
    data = json.loads(DATA.read_text())
    if '--check' in argv:
        try:
            check(data)
        except ContractError as err:
            print(f'::error::{DATA.relative_to(ROOT)}: {err}')
            return 1
        print(f'on-call snapshot ok: {len(data["pages"])} pages, {len(data["weeks"])} weeks')
        return 0
    data['html'] = render(data)
    check(data)
    write(data)
    return 0


if __name__ == '__main__':
    sys.exit(main())
