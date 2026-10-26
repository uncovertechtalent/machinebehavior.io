#!/usr/bin/env python3
"""site_chrome.theme_for picks the data-mb-theme of a page by URL prefix: /inside/ gets intranet (ADR-0035), /research/
gets report (ADR-0039), every other page none. A prefix keeps its trailing slash, so /researchers/ is not themed.
On report pages, number_exhibits writes "Exhibit N" into captions and exhibit references, and read_minutes gives the
reading time (ADR-0040). Stdlib only. Run from the repo root: python3 scripts/test_site_chrome_theme.py"""
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


PAGE = ('<div class="sheet" id="main"><p>See <a class="exhibit-ref" href="#b">Exhibit</a>.</p>'
        '<table id="a"><caption>First finding</caption><tr><td>1</td></tr></table>'
        '<table><tr><td>a ledger table, no caption</td></tr></table>'
        '<table id="b">\n<caption>Second finding</caption><tr><td>2</td></tr></table></div>')


class NumberExhibits(unittest.TestCase):
    def test_numbers_captions_in_page_order(self):
        out = site_chrome.number_exhibits(PAGE)
        self.assertIn('<caption><span class="exhibit-n">Exhibit 1</span> First finding</caption>', out)
        self.assertIn('<caption><span class="exhibit-n">Exhibit 2</span> Second finding</caption>', out)
        self.assertEqual(out.count('exhibit-n'), 2)  # the uncaptioned table is no exhibit

    def test_reference_gets_the_number_of_its_table(self):
        self.assertIn('<a class="exhibit-ref" href="#b">Exhibit 2</a>', site_chrome.number_exhibits(PAGE))

    def test_idempotent(self):
        once = site_chrome.number_exhibits(PAGE)
        self.assertEqual(site_chrome.number_exhibits(once), once)

    def test_renumbers_after_a_table_moves(self):
        moved = site_chrome.number_exhibits(PAGE).replace('<table id="a">', '<table id="z">').replace('href="#b"', 'href="#z"')
        out = site_chrome.number_exhibits(moved)
        self.assertIn('<a class="exhibit-ref" href="#z">Exhibit 1</a>', out)

    def test_reference_to_unknown_id_raises(self):
        with self.assertRaises(ValueError):
            site_chrome.number_exhibits(PAGE.replace('href="#b"', 'href="#nope"'), 'x.html')


class ReadMinutes(unittest.TestCase):
    def test_counts_sheet_text_only_and_rounds_up(self):
        words = ' '.join(['word'] * 231)
        src = f'<!-- mb:bar -->{"chrome " * 500}<!-- /mb:bar --><div class="sheet"><p>{words}</p><script>{"x " * 900}</script></div>'
        self.assertEqual(site_chrome.read_minutes(src), 2)

    def test_at_least_one_minute(self):
        self.assertEqual(site_chrome.read_minutes('<div class="sheet"><p>short</p></div>'), 1)

    def test_same_before_and_after_numbering(self):
        # PAGE's own text is 6 words (See, ., First finding, a ledger table, no caption, Second finding) besides the reference;
        # padding to exactly 230 puts the page on a minute boundary, where one extra counted word would show
        base = site_chrome.number_exhibits(PAGE)
        own = len(site_chrome._text(site_chrome.EXHIBIT_REF_RE.sub(' ', base.replace('<span class="exhibit-n">Exhibit 1</span>', '').replace('<span class="exhibit-n">Exhibit 2</span>', ''))).split())
        page = PAGE.replace('<p>See', '<p>' + ' '.join(['w'] * (230 - own)) + ' See')
        self.assertEqual(site_chrome.read_minutes(page), 1)
        self.assertEqual(site_chrome.read_minutes(site_chrome.number_exhibits(page)), 1)

    def test_reference_in_any_attribute_order(self):
        out = site_chrome.number_exhibits(PAGE.replace('<a class="exhibit-ref" href="#b">', '<a href="#b" class="exhibit-ref" title="x">'))
        self.assertIn('Exhibit 2</a>', out.split('</p>')[0])
        with self.assertRaises(ValueError):
            site_chrome.number_exhibits(PAGE.replace('<a class="exhibit-ref" href="#b">', '<a href="#nope" class="exhibit-ref">'))


if __name__ == '__main__':
    unittest.main()
