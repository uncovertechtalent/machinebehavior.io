#!/usr/bin/env python3
"""Export the public teasers of the knowledge vault's article drafts to inside/publisher/pipeline.json (ADR-0050).

Run from the repo root on the machine that holds the vault:

    python3 scripts/export_pipeline.py [~/vault] [inside/publisher/pipeline.json]

What leaves the vault: for every articles/<slug>/*.md whose front matter says teaser: public (one file per piece, the
draft, or the canonical cut of a piece that is live), the slug of its folder, the title
(the front matter's title, else the first heading), the standfirst, the stage (idea, drafting, review, live), the home
surface (machinebehavior.io, uncovertechtalent.com, substack, or open), the url of a live piece, and the date the stage
began (since, else updated, else created). Nothing from the body. A draft that says teaser: public but lacks a
standfirst, a stage, or a home, or whose title or standfirst holds a private pattern, is refused by name and nothing is
written: the fix happens in the draft, then the export runs again. The file is checked against the contract of
scripts/build_pipeline.py before it is written; the publisher's block is then rebuilt with scripts/build_inside_seats.py.
Stdlib only.
"""
import datetime, json, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_pipeline as bp, vault_export as ve  # noqa: E402

REQUIRED = ('standfirst', 'stage', 'home')


def first_heading(body):
    m = re.search(r'^#\s+(.+)$', body, re.M)
    return m.group(1).strip() if m else ''


def to_piece(folder, meta, body, today):
    """(piece, None) or (None, reason it was refused)."""
    missing = [k for k in REQUIRED if not isinstance(meta.get(k), str) or not meta[k].strip()]
    if missing:
        return None, f'front matter lacks {", ".join(missing)}'
    title = ve.one_line(meta.get('title') if isinstance(meta.get('title'), str) and meta['title'].strip() else first_heading(body), bp.MAX_TITLE)
    if not title:
        return None, 'no title in the front matter and no first heading'
    standfirst = ve.one_line(meta['standfirst'], bp.MAX_STANDFIRST)
    for name, text in (('title', title), ('standfirst', standfirst)):
        hits = ve.private_hits(text)
        if hits:
            return None, f'{name} holds a private pattern ({", ".join(hits)})'
    stage, home = meta['stage'].strip(), meta['home'].strip()
    if stage not in bp.STAGES:
        return None, f'stage {stage!r} is not one of {", ".join(bp.STAGES)}'
    if home not in bp.HOMES:
        return None, f'home {home!r} is not one of {", ".join(bp.HOMES)}'
    url = meta.get('url') if isinstance(meta.get('url'), str) and meta['url'].strip() else None
    since = next((meta[k][:10] for k in ('since', 'updated', 'created') if isinstance(meta.get(k), str) and meta[k].strip()), today)
    return {'slug': folder, 'title': title, 'standfirst': standfirst, 'stage': stage, 'home': home,
            'url': url, 'since': since}, None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    vault = Path(argv[0]).expanduser() if argv else Path.home() / 'vault'
    out = Path(argv[1]) if len(argv) > 1 else bp.DATA
    drafts = sorted(p for p in (vault / 'articles').glob('*/*.md') if not p.name.startswith('_'))
    if not drafts:
        print(f'export_pipeline: no articles/*/*.md under {vault}', file=sys.stderr)
        return 2
    now = datetime.datetime.now(datetime.timezone.utc)
    today = now.strftime('%Y-%m-%d')
    pieces, refused, read, folders = [], [], 0, {}
    for d in drafts:
        meta, body = ve.front(d.read_text(encoding='utf-8'))
        if meta.get('teaser') != 'public':
            continue
        read += 1
        if d.parent.name in folders:
            refused.append(f'{d.parent.name}: two files carry teaser: public ({folders[d.parent.name]} and {d.name}); keep one')
            continue
        folders[d.parent.name] = d.name
        piece, why = to_piece(d.parent.name, meta, body, today)
        if piece:
            pieces.append(piece)
        else:
            refused.append(f'{d.parent.name}: {why}')
    if refused:
        print(f'export_pipeline: {len(refused)} refused, nothing written:', file=sys.stderr)
        for r in refused:
            print('  ' + r, file=sys.stderr)
        return 1
    doc = {'schema': bp.SCHEMA, 'generated': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'source': bp.SOURCE,
           'pieces': bp.ordered(pieces)}
    errs = bp.check(doc)
    if errs:
        print('export_pipeline: the export breaks the pipeline contract, nothing written:', file=sys.stderr)
        for e in errs:
            print('  ' + e, file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    c = bp.tally(pieces)
    print(f'export_pipeline: {out} written: {len(pieces)} pieces ({c["idea"]} idea, {c["drafting"]} drafting, {c["review"]} in review, '
          f'{c["live"]} live) from {read} files with teaser: public of {len(drafts)} article files. Next: python3 scripts/build_inside_seats.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
