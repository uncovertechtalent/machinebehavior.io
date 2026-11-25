#!/usr/bin/env python3
"""Tests for the experiment 06 data folder: SHA256SUMS verifies, and conditions/index.json agrees with the files and
with SHA256SUMS (sha256 is the file's bytes; text_sha256 is the text as the runners sent it, without the trailing
newline). Reads the published folder only; no drafts, no network."""
import hashlib, json, os, unittest

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "research", "experiments", "06-stance-instructions-uncensored", "data")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sums():
    out = {}
    for line in open(os.path.join(DATA, "SHA256SUMS"), encoding="utf-8"):
        h, _, name = line.rstrip("\n").partition("  ")
        out[name] = h
    return out


class DataFolder(unittest.TestCase):
    def test_sha256sums_verifies_and_covers_the_folder(self):
        listed = sums()
        on_disk = {os.path.relpath(os.path.join(r, f), DATA) for r, _, fs in os.walk(DATA) for f in fs} - {"SHA256SUMS"}
        self.assertEqual(set(listed), on_disk)
        for name, h in listed.items():
            self.assertEqual(sha(open(os.path.join(DATA, name), "rb").read()), h, name)

    def test_condition_index_agrees_with_files_and_sums(self):
        index = json.load(open(os.path.join(DATA, "conditions", "index.json"), encoding="utf-8"))
        listed = sums()
        self.assertTrue(index)
        for cid, e in index.items():
            raw = open(os.path.join(DATA, e["file"]), "rb").read()
            self.assertEqual(e["sha256"], sha(raw), cid)
            self.assertEqual(e["sha256"], listed[e["file"]], cid)
            self.assertTrue(raw.endswith(b"\n"), cid)
            self.assertEqual(e["text_sha256"], sha(raw[:-1]), cid)
            self.assertEqual(e["words"], len(raw.decode("utf-8").split()), cid)


if __name__ == "__main__":
    unittest.main()
