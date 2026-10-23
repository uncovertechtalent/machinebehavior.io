#!/usr/bin/env python3
"""Write GitHub Pages redirect stubs from site/redirects.yml (ADR-0038).

Each entry in site/redirects.yml records a URL that moved. CloudFront issues the real 301 at the edge from the same
file (site-infra); this script writes the Pages fallback: a stub at the old path with a canonical link to the target,
a zero-second meta refresh, and robots noindex, so an engine that reaches the old path through github.io directly
follows the canonical and never indexes it.

    python3 scripts/build_redirects.py           write or refresh every stub
    python3 scripts/build_redirects.py --check    write nothing; exit 1 if a stub is missing or differs from source

Rules the build keeps:
- a stub is written only after the page has moved: the old path must hold no page, or hold a stub this script wrote
  (marked with the sentinel). A real page at the old path stops the build, so a move that forgot its git mv fails
  loudly instead of hiding behind a redirect.
- the target must exist as a page on disk (index.html), unless the entry is kind 'convenience' (its target is a built
  hub that its own build guarantees).
- stubs are noindex and never enter sitemap.xml or llms.txt; a removed page leaves the sitemap through its own build.

An empty redirects list is valid and writes nothing: Phase 0 ships this script with no entries, and each later phase
adds its entries when it moves those pages. Stdlib only. Run from the repo root. Tests: scripts/test_build_redirects.py
"""
import os
import sys

import mini_yaml

SENTINEL = "<!-- mb:redirect -->"
BASE = "https://machinebehavior.io"

STUB = """<!doctype html>
{sentinel}
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved: Machine Behavior</title>
<link rel="canonical" href="{base}{to}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={to}">
</head>
<body>
<p>This page moved to <a href="{to}">{base}{to}</a>.</p>
</body>
</html>
"""


def stub_html(to):
    return STUB.format(sentinel=SENTINEL, base=BASE, to=to)


def path_for(root, url):
    """A root-absolute URL ending in '/' maps to its index.html file under root."""
    return os.path.join(root, url.strip("/"), "index.html")


def load(path="site/redirects.yml"):
    doc = mini_yaml.load_file(path)
    return doc.get("redirects") or []


def _is_stub_or_absent(p):
    if not os.path.exists(p):
        return True
    with open(p, encoding="utf-8") as fh:
        return SENTINEL in fh.read(200)


def _target_ok(root, to, kind):
    if kind == "convenience":
        return True
    return os.path.exists(path_for(root, to))


def run(rows, root=".", check=False):
    """Returns (written, problems). Writes nothing when check is True."""
    written, problems = 0, []
    for r in rows:
        frm, to = r["from"], r["to"]
        kind = r.get("kind", "move")
        p = path_for(root, frm)
        if not _is_stub_or_absent(p):
            problems.append(f"{frm}: a real page is still here; move it (git mv) before writing the stub")
            continue
        if not _target_ok(root, to, kind):
            problems.append(f"{to}: target page does not exist on disk")
            continue
        want = stub_html(to)
        have = None
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                have = fh.read()
        if have == want:
            continue
        if check:
            problems.append(f"{frm}: stub missing or stale")
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(want)
        written += 1
        print("wrote stub", frm, "->", to)
    return written, problems


def main(argv):
    check = "--check" in argv
    rows = load()
    written, problems = run(rows, root=".", check=check)
    if problems:
        for m in problems:
            print("ERROR", m, file=sys.stderr)
        return 1
    if not check:
        print(f"{written} stub(s) written, {len(rows)} redirect(s) in site/redirects.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
