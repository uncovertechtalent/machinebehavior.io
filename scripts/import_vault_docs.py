#!/usr/bin/env python3
"""Copy the SRE folder and the standards clusters of the knowledge vault into docs sources.

Writes scripts/docs/sre/*.md and scripts/docs/std/*.md (both directories are replaced on each run),
then scripts/build_docs.py renders them. Run from the repo root on the machine that holds the vault:

    python3 scripts/import_vault_docs.py [~/vault]

What is published and what is changed (decided by Stefan Coetzee, 2026-10-09):
- In: vault/SRE (minus homelab/, .claude/, CLAUDE.md and the README mirror of Home.md) and the 28
  standards clusters under vault/pillars listed in STD_CLUSTERS.
- Redacted mechanically: private IPv4 addresses and LAN shorthand (".161"), e-mail addresses,
  the former employer's name, home directory paths, host names under the owner's private domain.
- Blockquotes in notes that carry a `clause:` field (ISO 27001 clause notes) are dropped unread:
  standards text is not machine-processed here (DIN Media terms on AI processing).
- Placeholder words the deploy gate blocks (TODO, TBD) are written out.
- Every page is labelled as a vault note not reviewed against its source (reviewed: no).
A report of every change is written to scripts/docs/IMPORT-REPORT.md.
"""
import re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / 'vault'
OUT = ROOT / 'scripts' / 'docs'

STD_CLUSTERS = ['iso-27001', 'iso-42001', 'iso-21434', 'iso-22301', 'nis2', 'dora', 'eu-ai-act', 'cyber-resilience-act', 'gdpr',
                'soc2', 'tisax', 'bsi-grundschutz', 'nist-csf', 'nist-ai-rmf', 'oecd-ai', 'owasp-llm-top-10', 'mitre', 'pci-dss',
                'hitrust', 'fedramp-cmmc', 'csa-ccm', 'slsa-sbom', 'un-r155-r156', 'itil', 'togaf', 'cobit', 'cmmi', 'prince2']
SRE_SKIP_DIRS = ('homelab', '.claude')
SRE_SKIP_FILES = ('CLAUDE.md', 'README.md')  # SRE/README.md mirrors SRE/Home.md

REDACT = [
    ('private IPv4', re.compile(r'\b(?:10(?:\.\d{1,3}){3}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}|192\.168(?:\.\d{1,3}){1,2})(?:/\d{1,2})?\b'), '[private IP]'),
    ('LAN shorthand', re.compile(r'(?<![\w.$/-])\.(?:1\d{1,2}|2[0-4]\d|25[0-5]|[1-9]\d?)\b(?![.\w%-])'), '[host]'),
    ('e-mail', re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[a-z]{2,}'), '[e-mail]'),
    ('employer', re.compile(r'makersite', re.I), '[employer]'),
    ('home path', re.compile(r'/Users/[a-z]+'), '~'),
    ('private host', re.compile(r'\b(?!grafana\.)[a-z0-9-]+\.scoetzee\.de\b', re.I), '[host]'),
    ('ssh user', re.compile(r'\bslaine@'), '[user]@'),
]
PLACEHOLDER = [(re.compile(r'\bTODO\b'), 'to do'), (re.compile(r'\bTBD\b'), 'to be decided'), (re.compile(r'\bLINK PENDING\b'), 'link to follow')]

report = []


def front(text):
    if not text.startswith('---\n'):
        return {}, text
    end = text.find('\n---', 4)
    if end < 0:
        return {}, text
    raw, body = text[4:end], text[end + 4:].lstrip('\n')
    meta, key = {}, None
    for line in raw.splitlines():
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith('[') and val.endswith(']'):
                meta[key] = [x.strip().strip('"\'') for x in val[1:-1].split(',') if x.strip()]
            elif val == '':
                meta[key] = []
            else:
                meta[key] = val.strip('"\'')
        elif key and re.match(r'^\s*-\s+', line) and isinstance(meta.get(key), list):
            meta[key].append(re.sub(r'^\s*-\s+', '', line).strip().strip('"\''))
    return meta, body


def as_list(v):
    return v if isinstance(v, list) else ([v] if v else [])


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def first_h1(body):
    m = re.search(r'^#\s+(.+?)\s*$', body, re.M)
    return m.group(1).strip() if m else None


def summary_of(body):
    for block in re.split(r'\n\s*\n', body):
        b = block.strip()
        if not b or b.startswith(('#', '|', '```', '- ', '* ', '1.', '---', '%%', '![')) or re.match(r'^>\s*\[!', b):
            continue
        b = re.sub(r'^>\s?', '', b, flags=re.M)
        b = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', b)
        b = re.sub(r'\[\[([^\]]+)\]\]', lambda m: m.group(1).split('/')[-1], b)
        b = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', b)
        b = re.sub(r'[*_`=]+', '', b)
        b = re.sub(r'\s+', ' ', b).strip()
        if len(b) < 25:
            continue
        m = re.match(r'(.{25,260}?[.!?])(\s|$)', b)
        s = m.group(1) if m else (b[:240].rsplit(' ', 1)[0] + '.')
        return s.replace(' — ', ', ').replace('—', ', ')
    return None


def clean(body, rel, has_clause):
    lines_out, dropped = [], 0
    for ln in body.split('\n'):
        if has_clause and re.match(r'^\s*>', ln) and not re.match(r'^\s*>\s*\[!', ln):
            dropped += 1
            continue
        lines_out.append(ln)
    if dropped:
        report.append(f'- `{rel}`: {dropped} blockquote lines dropped unread (clause note)')
    body = '\n'.join(lines_out)
    for name, rx, rep in REDACT:
        hits = rx.findall(body)
        if hits:
            body = rx.sub(rep, body)
            report.append(f'- `{rel}`: {len(hits)} x {name} redacted')
    for rx, rep in PLACEHOLDER:
        hits = rx.findall(body)
        if hits:
            body = rx.sub(rep, body)
            report.append(f'- `{rel}`: {len(hits)} x placeholder word written out')
    return body


def redact_text(s):
    for _, rx, rep in REDACT:
        s = rx.sub(rep, s)
    return s


def git_dates(path):
    try:
        out = subprocess.run(['git', 'log', '--format=%cs', '--', str(path)], cwd=VAULT, capture_output=True, text=True).stdout.split()
        return (out[-1], out[0]) if out else (None, None)
    except Exception:
        return (None, None)


def emit(space, slug, meta_out, body):
    lines = [f'{k}: {v}' for k, v in meta_out.items() if v not in (None, '', [])]
    (OUT / space / f'{slug}.md').write_text('\n'.join(lines) + '\n---\n' + body.strip('\n') + '\n', encoding='utf-8')


def note(path, space, slug, parent, order, title=None, title_prefix=''):
    rel = path.relative_to(VAULT).as_posix()
    meta, body = front(path.read_text(encoding='utf-8', errors='replace'))
    h1 = first_h1(body)
    t = title or (h1 if path.name == 'README.md' and h1 else path.stem)
    t = title_prefix + t
    # drop a leading H1 that repeats the title
    body = re.sub(r'^\s*#\s+.+\n', '', body, count=1) if h1 and (h1.strip().lower() == path.stem.lower() or path.name == 'README.md' or h1.strip().lower() == t.lower()) else body
    body = clean(body, rel, bool(meta.get('clause')))
    gc, gu = git_dates(path)
    created = str(meta.get('created') or gc or '')[:10]
    updated = str(meta.get('updated') or gu or created)[:10]
    tags = [x.lstrip('#') for x in as_list(meta.get('tags'))]
    labels = sorted({x.split('/')[-1].lower() for x in tags if x and not x.startswith(('kb/', 'status/'))})
    aliases = [a for a in as_list(meta.get('aliases')) if a and '|' not in a]
    summ = summary_of(body) or f'{t}, from the knowledge vault.'
    emit(space, slug, {
        'title': redact_text(t),
        'summary': redact_text(summ),
        'parent': parent, 'order': order,
        'labels': ', '.join(labels),
        'aliases': ' | '.join(redact_text(a) for a in aliases),
        'type': meta.get('type') if isinstance(meta.get('type'), str) else '',
        'created': created, 'updated': updated,
        'origin': rel, 'reviewed': 'no',
    }, body)
    return t


def reset(space):
    d = OUT / space
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)


# ---------- SRE ----------
reset('sre')
sre = VAULT / 'SRE'
used = set()
def uniq(s):
    base, k = s, 2
    while s in used:
        s = f'{base}-{k}'; k += 1
    used.add(s)
    return s

home_meta, home_body = front((sre / 'Home.md').read_text(encoding='utf-8'))
home_body = clean(re.sub(r'^\s*#\s+.+\n', '', home_body, count=1), 'SRE/Home.md', False)
emit('sre', 'index', {'title': 'SRE Handbook', 'summary': 'Site reliability engineering from the knowledge vault: the manifesto, ten pillars, patterns, runbooks, tools and incident records.',
                      'created': str(home_meta.get('created') or git_dates(sre / 'Home.md')[0] or ''), 'updated': git_dates(sre / 'Home.md')[1] or '',
                      'origin': 'SRE/Home.md', 'reviewed': 'no', 'labels': 'moc, sre'}, home_body)
used.add('index')

FOLDER_TITLES = {'manifesto': 'Manifesto', 'pillars': 'The ten pillars', 'patterns': 'Patterns', 'runbooks': 'Runbooks', 'tools': 'Tools', 'incidents': 'Incidents'}
FOLDER_ORDER = {'manifesto': 10, 'pillars': 20, 'patterns': 30, 'runbooks': 40, 'tools': 50, 'incidents': 60}
FOLDER_ABOUT = {
    'pillars': 'The ten pillars of the SRE framework, one page each: reliability, scalability, observability, incident management, infrastructure as code, CI/CD and deployment, performance, security, cost optimisation and toil reduction.',
    'incidents': 'Incident, cause and mitigation records from the vault, written up from trap files and session logs. Each record names its source.',
}
count = 0
for top in sorted(p for p in sre.iterdir() if p.is_dir() and p.name not in SRE_SKIP_DIRS):
    fslug = uniq(top.name)
    readme = top / 'README.md'
    if readme.exists():
        note(readme, 'sre', fslug, 'index', FOLDER_ORDER.get(top.name, 90), title=FOLDER_TITLES.get(top.name))
    else:
        about = FOLDER_ABOUT.get(top.name, f'{FOLDER_TITLES.get(top.name, top.name.title())} from the SRE folder of the vault.')
        emit('sre', fslug, {'title': FOLDER_TITLES.get(top.name, top.name.title()), 'summary': about, 'parent': 'index',
                            'order': FOLDER_ORDER.get(top.name, 90), 'origin': f'SRE/{top.name}/', 'reviewed': 'no', 'labels': 'folder'}, about)
    count += 1
    if top.name == 'pillars':
        for pd in sorted(x for x in top.iterdir() if x.is_dir()):
            pslug = uniq(re.sub(r'^\d+-', '', pd.name))
            num = int(pd.name.split('-')[0]) if pd.name[0].isdigit() else 99
            if (pd / 'README.md').exists():
                note(pd / 'README.md', 'sre', pslug, fslug, num * 10, title_prefix=f'{num}. ')
            count += 1
            for f in sorted(pd.glob('*.md')):
                if f.name == 'README.md':
                    continue
                note(f, 'sre', uniq(slugify(f.stem)), pslug, 100); count += 1
        continue
    for f in sorted(top.rglob('*.md')):
        if f.name == 'README.md' and f.parent == top:
            continue
        note(f, 'sre', uniq(slugify(f.stem)), fslug, 100); count += 1
for f in sorted(sre.glob('*.md')):
    if f.name in SRE_SKIP_FILES or f.name == 'Home.md':
        continue
    note(f, 'sre', uniq(slugify(f.stem)), 'index', 80); count += 1
print('sre pages', count + 1)

# ---------- standards ----------
reset('std')
used = {'index'}
groups = {}
std_count = 0
for c in STD_CLUSTERS:
    d = VAULT / 'pillars' / c
    cl = next(d.glob('*Cluster.md'))
    cmeta, _ = front(cl.read_text(encoding='utf-8'))
    short = cl.stem.replace(' Cluster', '')
    cslug = uniq(c)
    note(cl, 'std', cslug, 'index', STD_CLUSTERS.index(c) * 10 + 10, title=short)
    std_count += 1
    cat = next((t.split('/', 1)[1] for t in as_list(cmeta.get('tags')) if t.startswith('cat/')), 'other')
    groups.setdefault(cat, []).append((short, cslug))
    for f in sorted(d.glob('*.md')):
        if f == cl:
            continue
        if f.stem in ('position', 'anchors'):
            note(f, 'std', uniq(f'{c}-{f.stem}'), cslug, 5 if f.stem == 'position' else 6, title=f'{short} {f.stem}')
        else:
            note(f, 'std', uniq(slugify(f.stem)), cslug, 100)
        std_count += 1

CAT_NAMES = {'eu-regulation': 'EU regulation', 'iso-standard': 'ISO standards', 'us-framework': 'US frameworks'}
body = ('Reference clusters from the knowledge vault, one per standard, regulation or framework. Each cluster page is the map of its notes: '
        'provenance, structure, controls or articles, comparisons and controversies, plus a dated position and a list of anchors to primary sources. '
        'The notes were written from public sources and model knowledge; no standards text was machine-processed for them.\n\n'
        '> [!warning] Every page in this space is a vault note that has not been reviewed against the standard or regulation it describes. '
        'Use it as a map, and read the primary text before relying on a clause.\n\n## Clusters\n\n| Group | Clusters |\n|---|---|\n')
for cat in sorted(groups):
    name = CAT_NAMES.get(cat, cat.replace('-', ' ').capitalize())
    body += f'| {name} | ' + ', '.join(f'[{short}](doc:std/{slug})' for short, slug in sorted(groups[cat])) + ' |\n'
emit('std', 'index', {'title': 'Standards and Compliance', 'summary': 'Reference clusters from the knowledge vault for 28 standards, regulations and frameworks, from ISO 27001 and NIS2 to the EU AI Act and TOGAF.',
                      'origin': 'pillars/', 'reviewed': 'no', 'labels': 'moc, compliance', 'created': '2026-05-12'}, body)
print('std pages', std_count + 1)

(OUT / 'IMPORT-REPORT.md').write_text('# Vault import report\n\nWritten by scripts/import_vault_docs.py. One line per note that was changed on the way in.\n\n'
                                      + '\n'.join(report) + '\n', encoding='utf-8')
print('changes', len(report))
