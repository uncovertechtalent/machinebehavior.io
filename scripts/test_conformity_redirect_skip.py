#!/usr/bin/env python3
"""The gate reads site/redirects.yml with the site's own scripts/mini_yaml.py (one parser with build_redirects),
skips a stub only when its path is a `from` and the file is stub-shaped (sentinel, noindex, canonical), fails loudly
on a missing loader or an unparseable file, and returns an empty set when there is no file (ADR-0038). Stub fixtures
come from build_redirects.stub_html, so the writer and the gate are tested as a pair. Stdlib only.
Run from the repo root: python3 scripts/test_conformity_redirect_skip.py"""
import importlib.util
import os
import shutil
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


def drop_line(html, needle):
    return "\n".join(ln for ln in html.splitlines() if needle not in ln) + "\n"


class RedirectSkip(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        run.ROOT = self.root
        (self.root / "scripts").mkdir()
        shutil.copy(HERE / "mini_yaml.py", self.root / "scripts" / "mini_yaml.py")
        write(self.root, "site/redirects.yml", BLOCK)

    def tearDown(self):
        self._tmp.cleanup()

    def test_block_form_parses_to_the_from_set(self):
        self.assertEqual(run.redirect_from_paths(), {"/old/"})

    def test_listed_stub_from_the_writer_is_skipped(self):
        p = write(self.root, "old/index.html", build_redirects.stub_html("/new/"))
        self.assertTrue(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_long_target_stub_still_recognised(self):
        # the shape check reads the first 2000 characters; a long target must not push noindex or canonical past it
        long_to = "/research/" + "x" * 300 + "/"
        write(self.root, "site/redirects.yml", f"redirects:\n  - from: /old/\n    to: {long_to}\n    kind: move\n")
        p = write(self.root, "old/index.html", build_redirects.stub_html(long_to))
        self.assertTrue(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_rogue_sentinel_at_unlisted_path_is_not_skipped(self):
        p = write(self.root, "rogue/index.html", build_redirects.stub_html("/new/"))
        self.assertFalse(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_stub_without_noindex_is_not_skipped(self):
        p = write(self.root, "old/index.html", drop_line(build_redirects.stub_html("/new/"), "robots"))
        self.assertFalse(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_stub_without_canonical_is_not_skipped(self):
        p = write(self.root, "old/index.html", drop_line(build_redirects.stub_html("/new/"), "canonical"))
        self.assertFalse(run.is_redirect_stub(p, run.redirect_from_paths()))

    def test_no_file_is_empty(self):
        os.remove(self.root / "site" / "redirects.yml")
        self.assertEqual(run.redirect_from_paths(), set())

    def test_unparseable_file_fails_loud(self):
        # flow mappings are outside mini_yaml's subset, so the writer cannot read them; the gate must fail, not half-read
        write(self.root, "site/redirects.yml", "redirects:\n  - { from: /old/, to: /new/ }\n")
        with self.assertRaisesRegex(RuntimeError, "did not parse"):
            run.redirect_from_paths()

    def test_missing_loader_fails_loud(self):
        # a redirects.yml with no scripts/mini_yaml.py beside it must fail, not silently return an empty set
        with tempfile.TemporaryDirectory() as bare:
            run.ROOT = Path(bare)
            write(bare, "site/redirects.yml", BLOCK)
            with self.assertRaisesRegex(RuntimeError, "not importable"):
                run.redirect_from_paths()


if __name__ == "__main__":
    unittest.main()
