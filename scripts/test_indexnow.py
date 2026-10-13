#!/usr/bin/env python3
"""Tests for scripts/indexnow.py on a small repository built in a temporary folder (#85). Stdlib and git only.

    python3 scripts/test_indexnow.py

Exits 1 when a case fails.
"""
import contextlib, io, json, subprocess, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import indexnow  # noqa: E402

KEY = '0123456789abcdef0123456789abcdef'
BASE = 'https://example.test'
SITEMAP = '<urlset>' + ''.join(f'<url><loc>{BASE}{u}</loc></url>' for u in ('/', '/a/', '/a/b/')) + '</urlset>\n'


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), '-c', 'user.name=test', '-c', 'user.email=test@example.test', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def commit(root, files, msg):
    for path, text in files.items():
        p = root / path
        if text is None:
            p.unlink()
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
    git(root, 'add', '-A')
    git(root, 'commit', '-q', '-m', msg)
    return git(root, 'rev-parse', 'HEAD')


def run(root, out, before, after):
    indexnow.ROOT = root
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            rc = indexnow.main(['indexnow.py', before, after, str(out)])
        except SystemExit as e:
            rc = e.code
    body = json.loads(out.read_text()) if rc == 0 else None
    if out.exists():
        out.unlink()
    return rc, body


def main():
    failures = []

    def case(name, got, want):
        print(('ok   ' if got == want else 'FAIL ') + name)
        if got != want:
            failures.append(f'{name}: got {got!r}, want {want!r}')

    with tempfile.TemporaryDirectory() as tmp:
        root, out = Path(tmp) / 'site', Path(tmp) / 'body.json'
        root.mkdir()
        git(root, 'init', '-q')
        c0 = commit(root, {'CNAME': 'example.test\n', 'sitemap.xml': SITEMAP, f'{KEY}.txt': KEY + '\n',
                           'index.html': '0', 'a/index.html': '0', 'a/b/index.html': '0', 'orphan/index.html': '0',
                           'llms.txt': '0', 'scripts/x.py': '0', 'a/style.css': '0'}, 'base')
        c1 = commit(root, {'a/b/index.html': '1', 'orphan/index.html': '1', 'scripts/x.py': '1', 'a/style.css': '1'},
                    'nested page, a page outside the sitemap, a script and a stylesheet')
        rc, body = run(root, out, c0, c1)
        case('nested page in the sitemap; the others left out', (rc, body and body['urlList']),
             (0, [f'{BASE}/a/b/', f'{BASE}/sitemap.xml']))
        case('host, key and key location', body and (body['host'], body['key'], body['keyLocation']),
             ('example.test', KEY, f'{BASE}/{KEY}.txt'))
        c2 = commit(root, {'scripts/x.py': '2'}, 'script only')
        case('no page changed: exit 3', run(root, out, c1, c2)[0], 3)
        c3 = commit(root, {'index.html': '3', 'llms.txt': '3'}, 'home page and llms.txt')
        case('home page and llms.txt', run(root, out, c2, c3)[1]['urlList'],
             [f'{BASE}/', f'{BASE}/llms.txt', f'{BASE}/sitemap.xml'])
        c4 = commit(root, {'a/index.html': None, 'sitemap.xml': SITEMAP.replace(f'<url><loc>{BASE}/a/</loc></url>', '')},
                    'page removed')
        case('removed page left out; the changed sitemap still goes', run(root, out, c3, c4)[1]['urlList'],
             [f'{BASE}/sitemap.xml'])
        case('range over several commits', run(root, out, c0, c3)[1]['urlList'],
             [f'{BASE}/', f'{BASE}/a/b/', f'{BASE}/llms.txt', f'{BASE}/sitemap.xml'])
        case('null commit of a new branch: exit 3', run(root, out, '0' * 40, c4)[0], 3)
        case('unknown commit: exit 2', run(root, out, '1' * 40, c4)[0], 2)
        c5 = commit(root, {'fedcba9876543210fedcba9876543210.txt': 'fedcba9876543210fedcba9876543210', 'index.html': '5'},
                    'second key file')
        case('two key files: exit 2', run(root, out, c4, c5)[0], 2)

    for f in failures:
        print(f, file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
