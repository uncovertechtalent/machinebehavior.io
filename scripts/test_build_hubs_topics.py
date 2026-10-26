#!/usr/bin/env python3
"""The posts on the topic hubs (scripts/build_hubs.py members(), #192): a post with a copy on Substack links that copy,
which the blog copy names canonical (ADR-0046), and names the Uncover Tech Talent blog copy after it; no post or map node
points at another site's URL with a /research/ path, which the ADR-0038 move once wrote into them (#164). Reads the real
site/topics.yml and map/graph.json. Stdlib only.
Run from the repo root: python3 scripts/test_build_hubs_topics.py"""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_hubs  # noqa: E402
import mini_yaml  # noqa: E402
import site_chrome  # noqa: E402

ROOT = site_chrome.ROOT
FOREIGN_RESEARCH = re.compile(r'https://(?:uncovertechtalent\.com/blog|coetzeestefan\.substack\.com/p)/research/')  # the form #164 wrote


class TopicPosts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = site_chrome.tree(reload=True)
        build_hubs.fetch_issues = lambda: []  # the board issues come from the GitHub API; the posts do not need them
        docs, tag_posts, substack, issues = build_hubs.load_sources()
        cls.posts = {}
        for topic in mini_yaml.load_file(ROOT / 'site' / 'topics.yml')['topics']:
            for p in build_hubs.members(topic, cls.t, docs, tag_posts, substack, issues)['posts']:
                cls.posts[p['t']] = p

    def test_a_post_with_a_substack_copy_links_it_first(self):
        p = self.posts['The Stance Layer Is Still Toil']
        self.assertEqual(p['u'], 'https://coetzeestefan.substack.com/p/the-stance-layer-is-still-toil/')
        self.assertEqual((p['site'], p['also'], p['also_site']),
                         ('Substack', 'https://uncovertechtalent.com/blog/the-stance-layer-is-still-toil/', 'uncovertechtalent.com'))
        twins = [p for p in self.posts.values() if p.get('also')]
        self.assertTrue(twins)
        for p in twins:
            self.assertIn('substack.com/', p['u'], p['t'])
            self.assertIn('uncovertechtalent.com/', p['also'], p['t'])

    def test_a_second_substack_match_keeps_the_blog_copy(self):
        tag_posts = {'tag': [{'id': 'https://uncovertechtalent.com/blog/a/', 'title': 'A Post', 'date': '2026-10-01'}]}
        substack = [{'id': 'https://coetzeestefan.substack.com/p/a/', 'title': 'A Post', 'date': '2026-10-01'},
                    {'id': 'https://coetzeestefan.substack.com/p/a-old/', 'title': 'A Post', 'date': '2026-10-01'}]
        topic = {'key': 'k', 'map_tags': ['tag']}
        (p,) = build_hubs.members(topic, self.t, {'pages': []}, tag_posts, substack, [])['posts']
        self.assertEqual((p['u'], p['also'], p['also_site']),
                         ('https://coetzeestefan.substack.com/p/a/', 'https://uncovertechtalent.com/blog/a/', 'uncovertechtalent.com'))

    def test_no_post_points_at_a_moved_path_on_another_site(self):
        bad = [u for p in self.posts.values() for u in (p['u'], p.get('also') or '') if FOREIGN_RESEARCH.match(u)]
        self.assertEqual(bad, [])

    def test_the_map_snapshot_has_no_moved_path_on_another_site(self):
        text = (ROOT / 'map' / 'graph.json').read_text(encoding='utf-8')
        self.assertEqual(sorted(set(FOREIGN_RESEARCH.findall(text))), [])

    def test_the_hub_page_names_the_blog_copy(self):
        src = (ROOT / 'topics' / 'sycophancy-and-stance' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('<a href="https://coetzeestefan.substack.com/p/the-stance-layer-is-still-toil/">The Stance Layer Is Still Toil</a>', src)
        self.assertIn('also on uncovertechtalent.com</a>', src)
        self.assertNotIn('also on Substack', src)


if __name__ == '__main__':
    unittest.main()
