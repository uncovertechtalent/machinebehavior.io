#!/usr/bin/env python3
"""Build the Inside pages that are not docs, then the site-wide search index.

Steps, in order:
1. sync the top bar into the hand-written Inside pages (scripts/inside_chrome.py);
2. write the search index /inside/search.json (scripts/build_search.py).

Run after scripts/build_docs.py, from the repo root:  python3 scripts/build_inside.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inside_chrome
import build_search


def main():
    stale, missing = inside_chrome.sync()
    print(f'bar synced in {len(stale)} page(s)')
    if missing:
        for m in missing:
            print('no bar block or asset:', m)
        sys.exit(1)
    build_search.main()


if __name__ == '__main__':
    main()
