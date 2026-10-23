#!/usr/bin/env python3
"""The gate skips a redirect stub only when its path is a `from` in site/redirects.yml and the file carries the stub
shape; a sentinel at an unlisted path is a real page masking itself and must still be scanned (ADR-0038).
Stdlib only. Run from the repo root: python3 scripts/test_conformity_redirect_skip.py"""
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

RUN = Path(__file__).resolve().parent.parent / ".github" / "actions" / "conformity" / "run.py"
spec = importlib.util.spec_from_file_location("conformity_run", RUN)
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

STUB = ('<!doctype html>\n<!-- mb:redirect -->\n<html><head>'
        '<link rel="canonical" href="https://machinebehavior.io/new/">'
        '<meta name="robots" content="noindex, follow">'
        '<meta http-equiv="refresh" content="0; url=/new/"></head><body><p>moved</p></body></html>\n')


def write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class RedirectSkip(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        run.ROOT = Path(self.root)
        write(self.root, "site/redirects.yml", "redirects:\n  - { from: /old/, to: /new/, kind: move }\n")

    def tearDown(self):
        self._tmp.cleanup()

    def test_from_paths_parsed(self):
        self.assertEqual(run.redirect_from_paths(), {"/old/"})

    def test_listed_shaped_stub_is_skipped(self):
        p = write(self.root, "old/index.html", STUB)
        self.assertTrue(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_rogue_sentinel_at_unlisted_path_is_not_skipped(self):
        # a real page masking itself with the sentinel at a path not in redirects.yml
        p = write(self.root, "rogue/index.html", STUB)
        self.assertFalse(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_listed_path_without_stub_shape_is_not_skipped(self):
        # the path is listed, but the file is not a well-formed stub (no noindex), so it is scanned
        p = write(self.root, "old/index.html",
                  '<!doctype html>\n<!-- mb:redirect -->\n<html><head>'
                  '<link rel="canonical" href="https://machinebehavior.io/new/"></head><body>real content</body></html>')
        self.assertFalse(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_no_redirects_file_skips_nothing(self):
        os.remove(Path(self.root) / "site" / "redirects.yml")
        p = write(self.root, "old/index.html", STUB)
        self.assertEqual(run.redirect_from_paths(), set())
        self.assertFalse(run.is_redirect_stub(p, set()))


if __name__ == "__main__":
    unittest.main()
