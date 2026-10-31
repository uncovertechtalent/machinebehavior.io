#!/usr/bin/env python3
"""Export the public records of the knowledge vault's bead tracker to inside/board/ledger.json (ADR-0050).

Run from the repo root on the machine that holds the vault:

    python3 scripts/export_ledger.py [~/vault] [inside/board/ledger.json]

What leaves the vault: every bead that carries the label public, with its id, its title, its area (the label
area:<key>, one of the cockpit's eight), its kind (the label kind:<kind>, else by the bead's type: a decision, a bug as
a finding, anything else as an action), its status, and its dates. Nothing else: no description, no notes, no close
reason, no assignee. A done record older than the ledger's window is left out. A bead that carries the label but has no
area label, or whose title holds a private pattern, is refused by name and nothing is written: the fix happens at the
source, then the export runs again. The file is then checked against the contract of scripts/build_ledger.py before it
is written, and the board block is rebuilt with scripts/build_ledger.py. Stdlib only.
"""
import datetime, json, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cockpit as bc, build_ledger as bl, vault_export as ve  # noqa: E402

LABEL = 'public'
KIND_BY_TYPE = {'decision': 'decision', 'bug': 'finding'}
STATUS = {'open': 'open', 'in_progress': 'in_progress', 'blocked': 'blocked', 'closed': 'done'}
DROPPED = ('dropped', 'superseded', "won't", 'wont', 'duplicate', 'not planned')


def labelled(labels, prefix, keys):
    for k in keys:
        if prefix + k in labels:
            return k
    return None


def to_record(b, now):
    """(record, None), (None, reason it was refused), or (None, '') when it is left out on purpose."""
    labels = set(b.get('labels') or [])
    area = labelled(labels, 'area:', bc.AREA_KEYS)
    if area is None:
        return None, f'no area label (one of {", ".join("area:" + k for k in bc.AREA_KEYS)})'
    status = STATUS.get(b.get('status'))
    if status is None:
        return None, ''  # deferred and other states are not public work in flight
    closed = None
    if status == 'done':
        reason = (b.get('close_reason') or '').lower()
        if any(reason.startswith(d) for d in DROPPED):
            return None, ''
        closed = (b.get('closed_at') or '')[:10]
        if not closed:
            return None, 'closed without a closed_at date'
        if bc._day(closed) < now.date() - datetime.timedelta(days=bl.WINDOW_DAYS):
            return None, ''
    title = ve.one_line(b.get('title') or '', bl.MAX_TITLE)
    hits = ve.private_hits(title)
    if hits:
        return None, f'title holds a private pattern ({", ".join(hits)})'
    kind = labelled(labels, 'kind:', bc.KINDS)
    if kind == 'lead':
        return None, 'a lead is never public'
    if kind is None:
        kind = KIND_BY_TYPE.get(b.get('issue_type'), 'action')
    return {'id': b['id'], 'title': title, 'area': area, 'kind': kind, 'status': status,
            'created': (b.get('created_at') or '')[:10], 'closed': closed}, None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    vault = Path(argv[0]).expanduser() if argv else Path.home() / 'vault'
    out = Path(argv[1]) if len(argv) > 1 else bl.DATA
    if not (vault / '.beads').is_dir():
        print(f'export_ledger: {vault} has no .beads tracker', file=sys.stderr)
        return 2
    now = datetime.datetime.now(datetime.timezone.utc)
    rows = ve.beads(vault, LABEL)
    items, refused, left = [], [], 0
    for b in sorted(rows, key=lambda b: b.get('id', '')):
        rec, why = to_record(b, now)
        if rec:
            items.append(rec)
        elif why:
            refused.append(f'{b.get("id")}: {why}')
        else:
            left += 1
    if refused:
        print(f'export_ledger: {len(refused)} refused, nothing written:', file=sys.stderr)
        for r in refused:
            print('  ' + r, file=sys.stderr)
        return 1
    items.sort(key=lambda x: (bc.STATUS_ORDER.get(x['status'], 9), x['created'], x['id']))
    doc = {'schema': bl.SCHEMA, 'generated': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'source': bl.SOURCE,
           'window_days': bl.WINDOW_DAYS, 'items': items}
    errs = bl.check(doc)
    if errs:
        print('export_ledger: the export breaks the ledger contract, nothing written:', file=sys.stderr)
        for e in errs:
            print('  ' + e, file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    c = bl.tally(items)
    print(f'export_ledger: {out} written: {len(items)} records ({c["in_progress"]} in progress, {c["blocked"]} blocked, '
          f'{c["open"]} open, {c["done"]} done in {bl.WINDOW_DAYS} days) from {len(rows)} beads with the label {LABEL}; '
          f'{left} left out (older than the window, dropped, or not in flight). Next: python3 scripts/build_ledger.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
