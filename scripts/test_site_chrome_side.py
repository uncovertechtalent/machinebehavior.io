#!/usr/bin/env python3
"""The section sidebar from site/nav.yml (ADR-0044, ADR-0045): research groups as an accordion of <details name="mb-side">,
the group holding the current page open, each group opening with its index page (All case files) and at most five of its
pages under it, newest first where nav.yml asks, the red-team pages on the research sidebar, sidebar-only links kept out
of the page tree, the group index in the breadcrumbs, pieces listed elsewhere on the Articles index only (ADR-0046),
and no Topics block. Reads the real site/nav.yml. Stdlib only.
Run from the repo root: python3 scripts/test_site_chrome_side.py"""
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_hubs  # noqa: E402
import site_chrome  # noqa: E402

PROBE = '/research/experiments/stance-vs-censorship-abliteration/'
CASE12 = '/research/case-files/case-12-licence-rule-mid-task/'
TOC_LINE = re.compile(r'<li(?: class="toc-out")?><a href="([^"]+)">[^<]*</a>(?:<span class="toc-fill"></span><span class="toc-when">(.*?)</span>)?</li>')  # one line of a contents list (ADR-0048): url, what follows the leader


def toc_lines(src):
    """The lines of a page's first contents list (ADR-0048) as (url, what follows the leader); the chrome's lists stay out."""
    block = src[src.index('<ol class="toc">'):]
    return TOC_LINE.findall(block[:block.index('</ol>')])


def tree_from(text):
    """A Tree built from a changed copy of site/nav.yml."""
    with tempfile.TemporaryDirectory() as d:
        nav = Path(d) / 'nav.yml'
        nav.write_text(text, encoding='utf-8')
        real, site_chrome.NAV_FILE = site_chrome.NAV_FILE, nav
        try:
            return site_chrome.Tree()
        finally:
            site_chrome.NAV_FILE = real


def sub(html, label):
    """The links listed under the All link `label`, in order."""
    m = re.search(rf'>{re.escape(label)}</a><ul class="mb-side-sub">(.*?)</ul></li>', html)
    return re.findall(r'<a href="([^"]+)"', m.group(1)) if m else None


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
        self.assertIn('<a href="/research/red-team/">All red-team pages</a>', h)
        self.assertEqual(sub(h, 'All red-team pages'), ['/research/red-team/tactics/', '/research/red-team/method/'])

    def test_every_group_opens_with_its_all_link(self):
        h = self.side(CASE12)
        alls = re.findall(r'<summary>[^<]+</summary><ul><li><a href="([^"]+)"[^>]*>([^<]+)</a><ul class="mb-side-sub">', h)
        self.assertEqual(alls, [('/research/experiments/', 'All experiments'), ('/research/case-files/', 'All case files'),
                                ('/research/articles/', 'All articles'), ('/research/red-team/', 'All red-team pages'),
                                ('/research/registers/', 'All registers'), ('/research/reference/', 'All reference texts')])

    def test_newest_first_where_asked_written_order_elsewhere(self):
        h = self.side(CASE12)
        self.assertEqual(sub(h, 'All case files'), ['/research/case-files/running-conjobs-for-ai/', CASE12])
        self.assertEqual(sub(h, 'All articles'), ['/research/articles/chaos-engineering-for-behaviour/',
                                                  '/research/articles/the-cheating-moved/'])
        self.assertEqual(sub(h, 'All registers'), ['/research/claims/', '/research/objections/', '/research/evidence/', '/research/slips/'])

    def test_five_newest_and_the_current_page_when_older(self):
        extra = ''.join(f'              - title: Extra {i}\n                url: /research/case-files/extra-{i}/\n'
                        f'                published: 2026-10-1{i}\n' for i in range(6))
        anchor = '                published: 2026-10-06\n'
        text = site_chrome.NAV_FILE.read_text(encoding='utf-8')
        self.assertIn(anchor, text)
        t = tree_from(text.replace(anchor, anchor + extra, 1))
        newest = [f'/research/case-files/extra-{i}/' for i in range(5, 0, -1)]
        self.assertEqual(sub(site_chrome.side(t, t.by_url['/research/case-files/extra-5/']), 'All case files'), newest)
        self.assertEqual(sub(site_chrome.side(t, t.by_url[CASE12]), 'All case files'), newest + [CASE12])

    def test_newest_first_needs_a_date_on_every_page(self):
        text = site_chrome.NAV_FILE.read_text(encoding='utf-8')
        anchor = '                url: /research/case-files/running-conjobs-for-ai/\n                published: 2026-10-06\n'
        self.assertIn(anchor, text)
        with self.assertRaises(SystemExit) as e:
            tree_from(text.replace(anchor, '                url: /research/case-files/running-conjobs-for-ai/\n', 1))
        self.assertIn('Running conjobs for AI', str(e.exception))
        with self.assertRaises(SystemExit) as e:  # a date that would sort as text in the wrong place
            tree_from(text.replace(anchor, anchor.replace('2026-10-06', '2026-9-6'), 1))
        self.assertIn('Running conjobs for AI', str(e.exception))

    def test_a_hub_page_needs_about_and_pages(self):
        text = site_chrome.NAV_FILE.read_text(encoding='utf-8')
        about = '            about: Longer arguments from the research programme, with their sources.\n'
        self.assertIn(about, text)
        with self.assertRaises(SystemExit) as e:
            tree_from(text.replace(about, '', 1))
        self.assertIn('Articles', str(e.exception))
        start = text.index('            pages:\n              - title: Terms\n')  # the Reference index without its pages
        end = text.index('  - key: red-team')
        with self.assertRaises(SystemExit) as e:
            tree_from(text[:start] + text[end:])
        self.assertIn('Reference', str(e.exception))

    def test_index_page_rows_follow_the_order(self):
        src = (site_chrome.ROOT / 'research' / 'case-files' / 'index.html').read_text(encoding='utf-8')
        rows = toc_lines(src)
        self.assertEqual([u for u, _ in rows], [k.url for k in site_chrome.ordered(self.t.by_url['/research/case-files/'])])
        self.assertEqual([m for _, m in rows], ['2026-10-06', '2026-10-03'])
        self.assertNotIn('mb-entry', src)  # a contents list, not cards (ADR-0048)
        self.assertNotIn('<span class="kind">', src)

    def test_research_index_is_a_contents_list(self):
        src = (site_chrome.ROOT / 'research' / 'index.html').read_text(encoding='utf-8')
        labels = re.findall(r'<h2 class="label"><a href="([^"]+)">([^<]+)</a></h2>', src)
        self.assertEqual(labels, [('/research/experiments/', 'Experiments'), ('/research/case-files/', 'Case files'),
                                  ('/research/articles/', 'Articles'), ('/research/red-team/', 'Red team'),
                                  ('/research/registers/', 'Registers'), ('/research/reference/', 'Reference')])
        self.assertNotIn('mb-entry', src)
        self.assertNotIn('<span class="kind">', src)
        toc = src[src.index('<div class="toc-group">'):src.index('<p class="thesis">The same programme')]
        self.assertNotIn('<li><a href="/research/experiments/">', toc)  # a group's index is its label, never a line
        self.assertIn('<li><a href="/research/experiments/stance-vs-censorship-abliteration/">Stance versus censorship: an abliteration probe</a>'
                      '<span class="toc-fill"></span><span class="toc-when">2026-10-23</span></li>', toc)
        self.assertIn('<li><a href="/research/claims/">Claims ledger</a></li>', toc)  # no publication date, so no date
        self.assertEqual(len(re.findall(r'<li[ >]', toc)), sum(len(nodes) for _, _, nodes in build_hubs.research_groups(self.t)))

    def test_articles_index_lists_pieces_elsewhere_by_date(self):
        src = (site_chrome.ROOT / 'research' / 'articles' / 'index.html').read_text(encoding='utf-8')
        rows = toc_lines(src)
        urls = [u for u, _ in rows]
        self.assertEqual(urls[:4], ['/research/articles/chaos-engineering-for-behaviour/',
                                    'https://coetzeestefan.substack.com/p/knowledge-infrastructure-for-llms',
                                    'https://coetzeestefan.substack.com/p/the-stance-layer-is-still-toil',
                                    '/research/articles/the-cheating-moved/'])  # same day: this site's page first
        self.assertEqual(len(urls), 2 + len(self.t.by_url['/research/articles/'].cfg_page['elsewhere']))
        meta = dict(rows)
        self.assertIn('on Substack, also on <a href="https://uncovertechtalent.com/blog/write-for-the-codec/">the Uncover Tech Talent blog</a>',
                      meta['https://coetzeestefan.substack.com/p/write-for-the-codec'])
        self.assertTrue(meta['https://coetzeestefan.substack.com/p/sycophancy-is-layered-symptom-substitution'].endswith('on Substack'))
        self.assertIn('mb-entries-note', src)

    def test_pieces_elsewhere_stay_out_of_the_sidebar_and_the_research_index(self):
        self.assertEqual(sub(self.side(CASE12), 'All articles'), ['/research/articles/chaos-engineering-for-behaviour/',
                                                                 '/research/articles/the-cheating-moved/'])
        urls = [n.url for _, _, nodes in build_hubs.research_groups(self.t) for n in nodes]
        self.assertFalse([u for u in urls if u.startswith('https://')])
        self.assertNotIn('mb-entries-note', (site_chrome.ROOT / 'research' / 'registers' / 'index.html').read_text(encoding='utf-8'))

    def test_a_piece_elsewhere_is_checked(self):
        text = site_chrome.NAV_FILE.read_text(encoding='utf-8')
        url = '                url: https://coetzeestefan.substack.com/p/compaction-is-the-new-oom\n'
        date = '                published: 2026-09-28\n                about: Most agent harnesses ship without swap.\n'
        self.assertIn(url, text)
        self.assertIn(date, text)
        for old, bad, why in ((url, url.replace('coetzeestefan.substack.com', 'example.com'), 'ELSEWHERE_HOMES'),
                              (url, url.replace('https://', 'http://'), 'ELSEWHERE_HOMES'),
                              (url, '', 'needs url'),
                              (date, date.replace('2026-09-28', '2026-9-28'), 'YYYY-MM-DD'),
                              (date, '                published: 2026-09-28\n', 'needs title and about')):
            with self.assertRaises(SystemExit) as e:
                tree_from(text.replace(old, bad, 1))
            self.assertIn('Compaction Is the New OOM', str(e.exception))
            self.assertIn(why, str(e.exception))
        anchor = '            about: Terms, man pages and topics for reading the research.\n'
        self.assertIn(anchor, text)
        with self.assertRaises(SystemExit) as e:  # the Reference index lists in written order, so nothing can merge by date
            tree_from(text.replace(anchor, anchor + '            elsewhere:\n              - title: X\n                url: https://coetzeestefan.substack.com/p/x\n'
                                                    '                published: 2026-10-01\n                about: X.\n', 1))
        self.assertIn('Reference', str(e.exception))

    def test_hub_pages_only_under_research(self):
        text = site_chrome.NAV_FILE.read_text(encoding='utf-8')
        anchor = '        url: /aieo/this-site/\n'
        self.assertIn(anchor, text)
        with self.assertRaises(SystemExit) as e:
            tree_from(text.replace(anchor, anchor + '        hub: true\n', 1))
        self.assertIn('This site', str(e.exception))

    def test_a_group_holds_one_index_page(self):
        text = site_chrome.NAV_FILE.read_text(encoding='utf-8')
        anchor = '      - group: Articles\n        pages:\n'
        self.assertIn(anchor, text)
        with self.assertRaises(SystemExit) as e:
            tree_from(text.replace(anchor, anchor + '          - title: Loose\n            url: /research/loose/\n', 1))
        self.assertIn('Articles', str(e.exception))

    def test_topics_is_a_link_not_a_research_page(self):
        self.assertIn('<a href="/topics/">Topics</a>', self.side(PROBE))
        self.assertEqual(self.t.by_url['/topics/'].section, 'topics')
        self.assertNotIn('/topics/', [n.url for n in site_chrome._pages_under(self.t.section('research'))])

    def test_count_includes_the_red_team_and_skips_links(self):
        # 12 research pages, 4 group index pages, the red-team overview and its 2 pages; the Topics link is not a page
        self.assertIn('<span class="mb-side-n">19 pages</span>', self.side(PROBE))

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

    def test_nested_group_stops_the_build(self):
        bad = site_chrome.NAV_FILE.read_text(encoding='utf-8').replace(
            '            side: All experiments\n            order: newest\n            pages:\n',
            '            side: All experiments\n            order: newest\n            pages:\n              - group: Inner\n                pages: []\n', 1)
        self.assertIn('group: Inner', bad)
        with tempfile.TemporaryDirectory() as d:
            nav = Path(d) / 'nav.yml'
            nav.write_text(bad, encoding='utf-8')
            real, site_chrome.NAV_FILE = site_chrome.NAV_FILE, nav
            try:
                with self.assertRaises(SystemExit) as e:
                    site_chrome.Tree()
                self.assertIn('Inner', str(e.exception))
            finally:
                site_chrome.NAV_FILE = real

    def test_research_index_follows_the_groups(self):
        groups = build_hubs.research_groups(self.t)
        self.assertEqual([h for h, _, _ in groups], ['Experiments', 'Case files', 'Articles', 'Red team', 'Registers', 'Reference'])
        self.assertEqual([i for _, i, _ in groups], ['/research/experiments/', '/research/case-files/', '/research/articles/',
                                                     '/research/red-team/', '/research/registers/', '/research/reference/'])
        urls = [n.url for _, _, nodes in groups for n in nodes]
        self.assertEqual(len(urls), 13)                  # the two written indexes are labels now, not lines (ADR-0048)
        self.assertNotIn('/research/experiments/', urls)
        self.assertIn(PROBE, urls)                      # a page's child, listed under it
        self.assertIn('/research/red-team/method/', urls)  # the included section
        self.assertNotIn('/topics/', urls)               # the sidebar-only link
        self.assertNotIn('/research/case-files/', urls)  # a generated group index lists the same pages
        self.assertLess(urls.index('/research/case-files/running-conjobs-for-ai/'), urls.index(CASE12))

    def test_breadcrumbs_pass_through_the_group_index(self):
        self.assertEqual([n.title for n in self.t.trail(self.t.by_url[PROBE])],
                         ['Home', 'Research', 'Experiments', 'Stance versus censorship: an abliteration probe'])
        self.assertEqual([n.title for n in self.t.trail(self.t.by_url[CASE12])],
                         ['Home', 'Research', 'Case files', 'Case 12: a licence rule mid-task'])
        self.assertEqual([n.title for n in self.t.trail(self.t.by_url['/research/claims/'])],
                         ['Home', 'Research', 'Registers', 'Claims ledger'])

    def test_group_index_pages_are_generated(self):
        hubs = [n.url for n in site_chrome._all_under(self.t.section('research')) if build_hubs.is_hub(n)]
        self.assertEqual(hubs, ['/research/case-files/', '/research/articles/', '/research/registers/', '/research/reference/'])
        for url in hubs:
            self.assertTrue((site_chrome.ROOT / url.lstrip('/') / 'index.html').exists(), url)

    def test_no_sidebar_lists_the_topics(self):
        for url in (PROBE, '/research/red-team/', '/conformity/', '/your-next-cto/', '/topics/'):
            self.assertNotIn('mb-topics', self.side(url), url)


if __name__ == '__main__':
    unittest.main()
