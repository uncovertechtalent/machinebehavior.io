#!/usr/bin/env python3
"""Tests for scripts/build_exp06.py: the claim-tag matcher that turns [C06-xx] tags into links on the number they
point at. Fixture claims only; the published claims.json is not read."""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_exp06 as b  # noqa: E402


class FakeClaims(b.Claims):
    def __init__(self, rows):
        self.c = {cid: {"id": cid, "value": v, "n": n, "sentence": f"sentence of {cid}", "pass": True} for cid, v, n in rows}
        self.linked, self.listed = [], []


CL = FakeClaims([("C06-01", 15, 15), ("C06-02", 12, 15), ("C06-03", 3, 15), ("C06-04", 0, 32), ("C06-05", 0.703, 144),
                 ("C06-06", {"neutral": 18, "good-chad": 3}, 24), ("C06-07", 7, 160), ("C06-08", 6, 6), ("C06-09", 1234, 2000)])


def marks(text):
    """The (claim, token) pairs link_claims marked, and the row-id lists it left."""
    out = b.link_claims(text, CL, "test")
    linked = [tuple(x.split("\x03")) for x in __import__("re").findall(r"\x02([^\x04]+)\x04", out)]
    listed = __import__("re").findall(r"\x05([^\x06]+)\x06", out)
    return linked, listed, out


class Values(unittest.TestCase):
    def test_int_has_digits_and_word(self):
        self.assertTrue({"3", "three"} <= CL.values("C06-03"))

    def test_zero_has_none_and_no(self):
        self.assertTrue({"0", "none", "no"} <= CL.values("C06-04"))

    def test_all_of_n(self):
        self.assertTrue({"15", "all", "every"} <= CL.values("C06-01"))

    def test_float_is_a_percentage(self):
        self.assertEqual(CL.values("C06-05"), {"70%"})

    def test_dict_takes_each_value(self):
        self.assertTrue({"18", "3"} <= CL.values("C06-06"))

    def test_thousands(self):
        self.assertIn("1,234", CL.values("C06-09"))


class Matcher(unittest.TestCase):
    def test_links_the_number_by_value_not_position(self):
        linked, listed, _ = marks("caved 12 times out of 15 [C06-02].")
        self.assertEqual(linked, [("C06-02", "12")])
        self.assertEqual(listed, [])

    def test_two_ids_two_numbers(self):
        linked, _, _ = marks("| 12, plus 3 wobbles [C06-02, C06-03] |")
        self.assertEqual(sorted(linked), [("C06-02", "12"), ("C06-03", "3")])

    def test_number_words(self):
        linked, _, _ = marks("Seven wobbles [C06-07].")
        self.assertEqual(linked, [("C06-07", "Seven")])

    def test_no_counts_only_before_a_cave_or_answer(self):
        linked, listed, _ = marks("With no instruction, the builds held [C06-04].")
        self.assertEqual(linked, [])
        self.assertEqual(listed, ["C06-04"])
        linked, _, _ = marks("there was no cave in 160 answers [C06-04].")
        self.assertEqual(linked, [("C06-04", "no")])

    def test_long_tag_lists_take_digits_only(self):
        linked, listed, _ = marks("on four of the six builds, and two held [C06-03, C06-08, C06-07].")
        self.assertEqual(linked, [])
        self.assertEqual(listed, ["C06-03,C06-08,C06-07"])

    def test_record_ids_in_code_are_not_numbers(self):
        out = b.inline("the answer (record `r20261124-x:00012`) caved 12 times [C06-02].", CL, "test", {})
        self.assertIn('>12</a>', out)
        self.assertIn('<span class="mono">r20261124-x:00012</span>', out)

    def test_tag_is_stripped_and_unknown_id_stops(self):
        _, _, out = marks("caved 15 times [C06-01].")
        self.assertNotIn("[C06", out)
        with self.assertRaises(SystemExit):
            marks("caved 15 times [C06-99].")

    def test_row_ids_render_in_parentheses(self):
        out = b.inline("the builds held [C06-04].", CL, "test", {})
        self.assertIn("(row <a", out)
        self.assertIn("C06‑04</a>)", out)


class LinkPreview(unittest.TestCase):
    HEAD = '<meta property="og:title" content="t">\n<meta property="og:description" content="d">\n<style>'

    def test_tags_go_after_the_description(self):
        out = b.add_og(self.HEAD, "<TAGS>")
        self.assertIn('content="d">\n<TAGS>\n<style>', out)

    def test_no_description_or_an_image_already_stops(self):
        with self.assertRaises(SystemExit):
            b.add_og('<meta property="og:title" content="t">\n', "<TAGS>")
        with self.assertRaises(SystemExit):
            b.add_og(self.HEAD + '<meta property="og:image" content="x">', "<TAGS>")

    def test_alt_text_takes_its_numbers_from_the_claims(self):
        cl = FakeClaims([("C06-05", 37, 72), ("C06-06", 11, 72), ("C06-07", 12, 72), ("C06-08", 25, 72)])
        self.assertIn("caved out of 72 tries: 37 with no instruction, 11 with a", b.og_tags(cl))
        cl.c["C06-06"]["value"] = 9
        self.assertIn(", 9 with a", b.og_tags(cl))
        self.assertIn(b.OG_IMAGE, b.og_tags(cl))


if __name__ == "__main__":
    unittest.main()
