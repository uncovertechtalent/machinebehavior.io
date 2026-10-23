#!/usr/bin/env python3
"""The gate reads site/redirects.yml with the site's own mini_yaml (one parser with scripts/build_redirects.py),
skips a stub only when its path is a `from` and the file is stub-shaped, fails loudly on an unparseable file or a
missing loader, and returns an empty set when there is no file (ADR-0038). The stub fixtures come from
build_redirects.stub_html, so the writer and the gate are tested as a pair. Stdlib only.
Run from the repo root: python3 scripts/test_conformity_redirect_skip.py"""
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent / ".github" / "actions" / "conformity" / "run.py"
spec = importlib.util.spec_from_file_location("conformity_run", RUN)
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

sys.path.insert(0, str(HERE))
import build_redirects  # the writer whose stub shape the gate must recognise

BLOCK = "redirects:\n  - from: /old/\n    to: /new/\n    kind: move\n"


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
        write(self.root, "site/redirects.yml", BLOCK)

    def tearDown(self):
        self._tmp.cleanup()

    def test_block_form_parses_to_the_from_set(self):
        self.assertEqual(run.redirect_from_paths(), {"/old/"})

    def test_listed_stub_from_the_writer_is_skipped(self):
        p = write(self.root, "old/index.html", build_redirects.stub_html("/new/"))
        self.assertTrue(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_long_target_stub_still_recognised(self):
        # the shape check reads the first 400 characters; a long target must not push noindex or canonical out of range
        long_to = "/research/" + "x" * 300 + "/"
        write(self.root, "site/redirects.yml", f"redirects:\n  - from: /old/\n    to: {long_to}\n    kind: move\n")
        p = write(self.root, "old/index.html", build_redirects.stub_html(long_to))
        self.assertTrue(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_rogue_sentinel_at_unlisted_path_is_not_skipped(self):
        p = write(self.root, "rogue/index.html", build_redirects.stub_html("/new/"))
        self.assertFalse(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_listed_path_without_stub_shape_is_not_skipped(self):
        p = write(self.root, "old/index.html", "<!doctype html>\n<!-- mb:redirect -->\n<html><body>real</body></html>")
        self.assertFalse(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_no_file_is_empty(self):
        os.remove(Path(self.root) / "site" / "redirects.yml")
        self.assertEqual(run.redirect_from_paths(), set())

    def test_unparseable_file_fails_loud(self):
        # flow mappings are outside mini_yaml's subset, so the writer cannot read them; the gate must fail, not half-read
        write(self.root, "site/redirects.yml", "redirects:\n  - { from: /old/, to: /new/ }\n")
        with self.assertRaises(Exception):
            run.redirect_from_paths()

    def test_missing_loader_fails_loud(self):
        # a redirects.yml with no scripts/mini_yaml.py beside it (the shared action on a site without the builder)
        # must fail, not silently return an empty set. A fresh interpreter has no cached mini_yaml.
        code = ("import importlib.util, pathlib, sys;"
                f"s = importlib.util.spec_from_file_location('r', r'{RUN}');"
                "m = importlib.util.module_from_spec(s); s.loader.exec_module(m);"
                "m.ROOT = pathlib.Path(sys.argv[1]); m.redirect_from_paths()")
        with tempfile.TemporaryDirectory() as root:
            write(root, "site/redirects.yml", BLOCK)
            r = subprocess.run([sys.executable, "-c", code, root], cwd=root, capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
