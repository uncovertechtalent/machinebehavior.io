#!/usr/bin/env python3
"""The section sidebar from site/nav.yml (ADR-0044): research groups as an accordion of <details name="mb-side">, the group
holding the current page open, the red-team pages on the research sidebar, sidebar-only links kept out of the page tree,
breadcrumbs unchanged, and no Topics block. Reads the real site/nav.yml. Stdlib only.
Run from the repo root: python3 scripts/test_site_chrome_side.py"""
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_chrome  # noqa: E402

PROBE = '/research/experiments/stance-vs-censorship-abliteration/'


def groups(html):
    """[(name, open), ...] of the accordion groups in a sidebar."""
    return [(name, bool(op)) for op, name in re.findall(r'<details class="mb-side-acc" name="mb-side"( open)?><summary>([^<]+)</summary>', html)]


class ResearchSidebar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = site_chrome.tree(reload=True)

    def side(self, url):
        return site_chrome.side(self.t, self.t.by_url[url])

    def test_groups_in_reading_order_with_the_current_one_open(self):
        self.assertEqual(groups(self.side(PROBE)), [('Experiments', True), ('Case files', False), ('Articles', False),
                                                    ('Red team', False), ('Registers', False), ('Reference', False)])

    def test_current_page_marked_and_register_renamed(self):
        h = self.side(PROBE)
        self.assertIn(f'<a href="{PROBE}" aria-current="page">', h)
        self.assertIn('<a href="/research/experiments/">All experiments</a>', h)

    def test_red_team_pages_show_the_research_sidebar(self):
        h = self.side('/research/red-team/method/')
        self.assertIn('aria-label="Research pages"', h)
        self.assertEqual([g for g, op in groups(h) if op], ['Red team'])
        self.assertIn('<a href="/research/red-team/">Overview</a>', h)

    def test_topics_is_a_link_not_a_research_page(self):
        self.assertIn('<a href="/topics/">Topics</a>', self.side(PROBE))
        self.assertEqual(self.t.by_url['/topics/'].section, 'topics')
        self.assertNotIn('/topics/', [n.url for n in site_chrome._pages_under(self.t.section('research'))])

    def test_count_includes_the_red_team_and_skips_links(self):
        # 12 research pages, the red-team overview and its 2 pages; the Topics link is not a page
        self.assertIn('<span class="mb-side-n">15 pages</span>', self.side(PROBE))

    def test_unknown_include_stops_the_build(self):
        bad = site_chrome.NAV_FILE.read_text(encoding='utf-8').replace('include: red-team', 'include: no-such-section', 1)
        with tempfile.TemporaryDirectory() as d:
            nav = Path(d) / 'nav.yml'
            nav.write_text(bad, encoding='utf-8')
            real, site_chrome.NAV_FILE = site_chrome.NAV_FILE, nav
            try:
                with self.assertRaises(SystemExit) as e:
                    site_chrome.Tree()
                self.assertIn('no-such-section', str(e.exception))
            finally:
                site_chrome.NAV_FILE = real

    def test_breadcrumbs_unchanged(self):
        self.assertEqual([n.title for n in self.t.trail(self.t.by_url[PROBE])],
                         ['Home', 'Research', 'Experiments', 'Stance versus censorship: an abliteration probe'])

    def test_no_sidebar_lists_the_topics(self):
        for url in (PROBE, '/research/red-team/', '/conformity/', '/your-next-cto/', '/topics/'):
            self.assertNotIn('mb-topics', self.side(url), url)


if __name__ == '__main__':
    unittest.main()
