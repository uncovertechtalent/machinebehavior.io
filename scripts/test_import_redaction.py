#!/usr/bin/env python3
"""import_vault_docs.py refuses to run without VAULT_PRIVATE_USER, so the private user name is never published by a
silent miss; VAULT_PRIVATE_USER=- is the explicit opt-out. Stdlib only, writes only to a temp dir (IMPORT_OUT), needs
no vault. Run from the repo root: python3 scripts/test_import_redaction.py"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "import_vault_docs.py"


def run(env_extra, vault):
    env = dict(os.environ)
    env.pop("VAULT_PRIVATE_USER", None)
    env.update(env_extra)
    with tempfile.TemporaryDirectory() as out:
        env["IMPORT_OUT"] = out
        return subprocess.run([sys.executable, str(SCRIPT), vault], env=env, capture_output=True, text=True)


class Guard(unittest.TestCase):
    def test_refuses_without_the_variable(self):
        # The guard fires before any vault access, so an empty vault path is enough to reach it.
        with tempfile.TemporaryDirectory() as vault:
            r = run({}, vault)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("VAULT_PRIVATE_USER", r.stderr)

    def test_opt_out_passes_the_guard(self):
        # VAULT_PRIVATE_USER=- clears the guard; the run then stops on the empty fixture vault, not on the guard.
        with tempfile.TemporaryDirectory() as vault:
            r = run({"VAULT_PRIVATE_USER": "-"}, vault)
            self.assertNotIn("set VAULT_PRIVATE_USER", r.stderr)


if __name__ == "__main__":
    unittest.main()
