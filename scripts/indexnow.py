#!/usr/bin/env python3
"""The IndexNow request body for one deploy of the site (issue #85).

    python3 scripts/indexnow.py BEFORE AFTER OUT

Lists the files that changed between the commits BEFORE and AFTER, maps them to their public URLs, and writes the
IndexNow request body to OUT: host, key, keyLocation and urlList. A changed file counts when it is the index.html of a
page listed in sitemap.xml, or llms.txt. The sitemap URL goes with every submission. Removed pages are left out; they
leave the sitemap too. The deploy workflow sends OUT to https://api.indexnow.org/indexnow with curl (deploy pipeline
doc, job 4). Tests: python3 scripts/test_indexnow.py.

Exit 0: OUT written, the URLs printed. Exit 3: nothing a search engine reads changed, or BEFORE is the null commit of
a new branch; OUT not written. Exit 2: an error (no key file or more than one, an unknown commit).

The key is public by design: a search engine fetches /<key>.txt from the site root to check that a submission comes
from the site's owner. The key is the name of the one file at the root whose name is 32 hex characters plus .txt and
whose content is that name. Stdlib only.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_URLS = 10000  # IndexNow accepts up to 10,000 URLs per request
KEY_RE = re.compile(r'^[0-9a-f]{32}\.txt$')
LOC_RE = re.compile(r'<loc>\s*([^<\s]+)\s*</loc>')


def fail(msg):
    print('indexnow: ' + msg, file=sys.stderr)
    sys.exit(2)


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], check=True, capture_output=True, text=True).stdout


def key():
    keys = [p.stem for p in ROOT.iterdir() if p.is_file() and KEY_RE.match(p.name) and p.read_text().strip() == p.stem]
    if len(keys) != 1:
        fail(f'expected one key file at the site root, found {len(keys)}')
    return keys[0]


def url_for(path, base):
    """The public URL of a changed file, or None for a file that is not a page or llms.txt."""
    if path == 'llms.txt':
        return base + '/llms.txt'
    if path == 'index.html':
        return base + '/'
    if path.endswith('/index.html'):
        return base + '/' + path[:-len('index.html')]
    return None


def main(argv):
    if len(argv) != 4:
        fail('usage: python3 scripts/indexnow.py BEFORE AFTER OUT')
    before, after, out = argv[1:]
    if re.fullmatch(r'0{40}', before):
        print('indexnow: no previous commit (new branch); nothing to submit')
        return 3
    try:
        for sha in (before, after):
            git('cat-file', '-e', sha + '^{commit}')
        changed = git('diff', '--name-only', '--no-renames', '--diff-filter=d', '-z', before, after).split('\0')
    except subprocess.CalledProcessError as e:
        fail(f'git {" ".join(e.cmd[3:])} failed: {e.stderr.strip()}')
    changed = [p for p in changed if p]
    host = (ROOT / 'CNAME').read_text().strip()
    base = 'https://' + host
    listed = set(LOC_RE.findall((ROOT / 'sitemap.xml').read_text()))
    urls = sorted({u for u in (url_for(p, base) for p in changed) if u and (u in listed or u.endswith('/llms.txt'))})
    if not urls and 'sitemap.xml' not in changed:
        print(f'indexnow: {len(changed)} changed files, none of them a page in the sitemap or llms.txt; nothing to submit')
        return 3
    urls.append(base + '/sitemap.xml')
    if len(urls) > MAX_URLS:
        print(f'indexnow: {len(urls)} URLs, over the limit of {MAX_URLS} per request; the first {MAX_URLS} are sent')
        urls = urls[:MAX_URLS]
    k = key()
    body = {'host': host, 'key': k, 'keyLocation': f'{base}/{k}.txt', 'urlList': urls}
    Path(out).write_text(json.dumps(body, indent=1) + '\n')
    print(f'indexnow: {len(urls)} URLs from {len(changed)} changed files ({before[:8]}..{after[:8]})')
    for u in urls:
        print('  ' + u)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
