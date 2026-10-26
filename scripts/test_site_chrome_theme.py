#!/usr/bin/env python3
"""site_chrome.theme_for picks the data-mb-theme of a page by URL prefix: /inside/ gets intranet (ADR-0035), /research/
gets report (ADR-0039), every other page none. A prefix keeps its trailing slash, so /researchers/ is not themed.
Stdlib only. Run from the repo root: python3 scripts/test_site_chrome_theme.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_chrome  # noqa: E402


class ThemeFor(unittest.TestCase):
    def test_research_gets_report(self):
        self.assertEqual(site_chrome.theme_for('/research/'), 'report')
        self.assertEqual(site_chrome.theme_for('/research/red-team/method/'), 'report')

    def test_inside_gets_intranet(self):
        self.assertEqual(site_chrome.theme_for('/inside/docs/eng/'), 'intranet')

    def test_other_pages_get_none(self):
        for url in ('/', '/researchers/', '/cto-powersuit/', '/conformity/'):
            self.assertIsNone(site_chrome.theme_for(url), url)

    def test_html_theme_sets_and_removes(self):
        self.assertIn('data-mb-theme="report"', site_chrome._html_theme('<html lang="en">', 'report'))
        self.assertEqual(site_chrome._html_theme('<html lang="en" data-mb-theme="report">', None), '<html lang="en">')


if __name__ == '__main__':
    unittest.main()
