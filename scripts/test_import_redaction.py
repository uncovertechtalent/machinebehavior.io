#!/usr/bin/env python3
"""import_vault_docs.py refuses to run without a usable VAULT_PRIVATE_USER, so the private user name is never
published by a silent miss; VAULT_PRIVATE_USER=- is the explicit opt-out. Stdlib only, writes only to a temp dir
(IMPORT_OUT), needs no vault. Run from the repo root: python3 scripts/test_import_redaction.py"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "import_vault_docs.py"


def run(env_extra, vault, out):
    env = dict(os.environ)
    env.pop("VAULT_PRIVATE_USER", None)
    env.update(env_extra)
    env["IMPORT_OUT"] = out
    return subprocess.run([sys.executable, str(SCRIPT), vault], env=env, capture_output=True, text=True)


class Guard(unittest.TestCase):
    def test_refuses_without_the_variable(self):
        # The guard fires before any vault access, so an empty vault path is enough to reach it.
        with tempfile.TemporaryDirectory() as vault, tempfile.TemporaryDirectory() as out:
            r = run({}, vault, out)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("VAULT_PRIVATE_USER", r.stderr)
            self.assertFalse((Path(out) / "sre").exists())  # stopped before any import work

    def test_refuses_a_placeholder_value(self):
        # A copy-pasted placeholder like "<name>" is non-empty but cannot be a login name, so it must not pass.
        with tempfile.TemporaryDirectory() as vault, tempfile.TemporaryDirectory() as out:
            r = run({"VAULT_PRIVATE_USER": "<name>"}, vault, out)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("login name", r.stderr)
            self.assertFalse((Path(out) / "sre").exists())

    def test_opt_out_clears_the_guard_and_reaches_the_vault(self):
        # VAULT_PRIVATE_USER=- clears the guard; the run then creates OUT/sre and stops on the empty fixture vault,
        # which pins the order "guard first, vault second".
        with tempfile.TemporaryDirectory() as vault, tempfile.TemporaryDirectory() as out:
            r = run({"VAULT_PRIVATE_USER": "-"}, vault, out)
            self.assertNotIn("set VAULT_PRIVATE_USER", r.stderr)
            self.assertTrue((Path(out) / "sre").exists())


if __name__ == "__main__":
    unittest.main()
