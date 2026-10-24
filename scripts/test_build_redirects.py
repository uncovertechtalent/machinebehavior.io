#!/usr/bin/env python3
"""Tests for scripts/build_redirects.py. Stdlib only. Run from the repo root: python3 scripts/test_build_redirects.py"""
import os
import tempfile
import unittest

import build_redirects as br


def page(root, url):
    p = br.path_for(root, url)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("<!doctype html><title>real</title>")
    return p


class WriteStub(unittest.TestCase):
    def test_writes_stub_when_target_exists_and_source_gone(self):
        with tempfile.TemporaryDirectory() as root:
            page(root, "/research/claims/")  # the target page exists; the old path is empty
            rows = [{"from": "/claims/", "to": "/research/claims/", "kind": "move"}]
            written, problems = br.run(rows, root=root)
            self.assertEqual((written, problems), (1, []))
            with open(br.path_for(root, "/claims/"), encoding="utf-8") as fh:
                html = fh.read()
            self.assertIn(br.SENTINEL, html)
            self.assertIn('rel="canonical" href="https://machinebehavior.io/research/claims/"', html)
            self.assertIn('content="0; url=/research/claims/"', html)
            self.assertIn('name="robots" content="noindex', html)

    def test_refuses_when_real_page_still_at_source(self):
        with tempfile.TemporaryDirectory() as root:
            page(root, "/research/claims/")
            page(root, "/claims/")  # a real page (no sentinel) is still at the old path
            rows = [{"from": "/claims/", "to": "/research/claims/", "kind": "move"}]
            written, problems = br.run(rows, root=root)
            self.assertEqual(written, 0)
            self.assertEqual(len(problems), 1)
            self.assertIn("move it", problems[0])

    def test_errors_when_target_missing(self):
        with tempfile.TemporaryDirectory() as root:
            rows = [{"from": "/claims/", "to": "/research/claims/", "kind": "move"}]
            written, problems = br.run(rows, root=root)
            self.assertEqual(written, 0)
            self.assertIn("does not exist", problems[0])

    def test_convenience_skips_target_check(self):
        with tempfile.TemporaryDirectory() as root:
            rows = [{"from": "/services/", "to": "/inside/services/", "kind": "convenience"}]
            written, problems = br.run(rows, root=root)
            self.assertEqual((written, problems), (1, []))

    def test_check_flags_stale_then_passes_after_write(self):
        with tempfile.TemporaryDirectory() as root:
            page(root, "/research/claims/")
            rows = [{"from": "/claims/", "to": "/research/claims/", "kind": "move"}]
            _, problems = br.run(rows, root=root, check=True)
            self.assertEqual(len(problems), 1)  # stub missing
            br.run(rows, root=root)
            _, problems = br.run(rows, root=root, check=True)
            self.assertEqual(problems, [])  # now current

    def test_empty_list_writes_nothing(self):
        with tempfile.TemporaryDirectory() as root:
            written, problems = br.run([], root=root)
            self.assertEqual((written, problems), (0, []))

    def test_article_redirect_requires_permanent(self):
        with tempfile.TemporaryDirectory() as root:
            page(root, "/research/articles/the-cheating-moved/")
            rows = [{"from": "/the-cheating-moved/", "to": "/research/articles/the-cheating-moved/", "kind": "move"}]
            written, problems = br.run(rows, root=root)  # missing permanent
            self.assertEqual(written, 0)
            self.assertIn("permanent", problems[0])
            rows[0]["permanent"] = True
            written, problems = br.run(rows, root=root)  # now allowed
            self.assertEqual((written, problems), (1, []))


if __name__ == "__main__":
    unittest.main()
