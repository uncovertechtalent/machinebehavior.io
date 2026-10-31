#!/usr/bin/env python3
"""Shared pieces of the two exports from the knowledge vault to Inside (ADR-0050): the private patterns a public record
may not hold, the front matter reader, and the bead tracker call.

The exports run on the holder's machine, where the vault is; nothing here reads the network. A record that holds a
private pattern is refused and named, never rewritten: the fix happens at the source, so the public file never carries
a redaction mark that says something was there. The patterns are those of scripts/import_vault_docs.py; the private
user name that import redacts is not a pattern here, since a bead title or a standfirst never carries a login (the
pre-push hook on the holder's machine stays the backstop for the terms kept off this repository). Stdlib only.
"""
import json, re, subprocess, unicodedata

PRIVATE = [
    ('private IPv4', re.compile(r'\b(?:10(?:\.\d{1,3}){3}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}|192\.168(?:\.\d{1,3}){1,2})(?:/\d{1,2})?\b')),
    ('LAN shorthand', re.compile(r'(?<![\w.$/-])\.(?:1\d{1,2}|2[0-4]\d|25[0-5]|[1-9]\d?)\b(?![.\w%-])')),
    ('e-mail', re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[a-z]{2,}')),
    ('employer', re.compile(r'makersite', re.I)),
    ('home path', re.compile(r'/Users/[a-z]+|~/')),
    ('private host', re.compile(r'\b(?!grafana\.)[a-z0-9-]+\.scoetzee\.de\b', re.I)),
    ('public IPv4', re.compile(r'\b(?!(?:0|127|10|100\.64|169\.254|192\.0\.2|198\.51\.100|203\.0\.113)\.)(?:\d{1,3}\.){3}\d{1,3}\b')),
    ('key path', re.compile(r'\.ssh/[\w.-]+')),
    ('placeholder', re.compile(r'\b(?:TODO|TBD|LINK PENDING)\b')),
]


def private_hits(s):
    """The names of the private patterns a text matches, in list order; empty when it may be public."""
    return [name for name, rx in PRIVATE if rx.search(s)]


def hidden(t):
    """True when a text holds a control or format character or a line or paragraph separator."""
    return any(unicodedata.category(ch) in ('Cc', 'Cf', 'Zl', 'Zp') for ch in t)


def one_line(s, limit):
    """A text on one line, whitespace folded, cut at the limit, for the exports to write; the contracts then check it."""
    t = ''.join(ch for ch in str(s) if unicodedata.category(ch) not in ('Cc', 'Cf') or ch in '\t\n\r')
    return ' '.join(t.split())[:limit].strip()


def front(text):
    """The front matter of a vault note as a dict of strings and lists (the reader of import_vault_docs.py), and the body."""
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


def beads(vault, label):
    """Every bead of the vault's tracker that carries the label, open or closed, as the tracker's JSON records."""
    cmd = ['bd', 'list', '--all', '-n', '0', '--json', '-l', label]
    try:
        out = subprocess.run(cmd, cwd=str(vault), capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise SystemExit(f'vault_export: bd failed: {e}') from None
    if out.returncode != 0:
        raise SystemExit(f'vault_export: bd exited {out.returncode}: {out.stderr.strip()[:400]}')
    try:
        rows = json.loads(out.stdout or '[]')
    except ValueError as e:
        raise SystemExit(f'vault_export: bd gave no JSON ({e})') from None
    if not isinstance(rows, list):
        raise SystemExit('vault_export: bd gave no list')
    return rows
