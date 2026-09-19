"""Run each verification script against tests/fixtures/{good,bad} and check exit codes and messages.

    python3 -m unittest discover tests
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "codebase-vault-docs" / "scripts"
GOOD = ROOT / "tests" / "fixtures" / "good"
BAD = ROOT / "tests" / "fixtures" / "bad"


def run(script: str, *args: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class GoodVaultPasses(unittest.TestCase):
    def test_wikilinks(self):
        code, out = run("check_wikilinks.py", str(GOOD))
        self.assertEqual(code, 0, out)

    def test_unwrap_check(self):
        code, out = run("unwrap.py", str(GOOD), "--check")
        self.assertEqual(code, 0, out)

    def test_canvas(self):
        code, out = run("validate_canvas.py", str(GOOD))
        self.assertEqual(code, 0, out)
        self.assertIn("0 warning(s)", out)


class BadVaultFails(unittest.TestCase):
    def test_wikilinks(self):
        code, out = run("check_wikilinks.py", str(BAD))
        self.assertEqual(code, 1)
        self.assertIn("unresolved link [[missing/note]]", out)
        self.assertIn("unresolved link [[nowhere.png]]", out)
        self.assertIn("ambiguous link [[00-overview]]", out)
        self.assertIn("pipe-aliased link inside a table cell", out)

    def test_unwrap_check(self):
        code, out = run("unwrap.py", str(BAD), "--check")
        self.assertEqual(code, 1)
        self.assertIn("index.md: 1 hard-wrapped line(s)", out)

    def test_canvas(self):
        code, out = run("validate_canvas.py", str(BAD))
        self.assertEqual(code, 1)
        self.assertIn("invalid JSON", out)
        self.assertIn("references a missing node", out)
        self.assertIn("edge a -> d skips 1 row(s)", out)
        self.assertIn("overlap in row 0", out)
        self.assertIn("px apart in row 0", out)


class UnwrapRewrite(unittest.TestCase):
    def test_joins_paragraph_and_keeps_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(BAD, Path(tmp) / "v")
            code, out = run("unwrap.py", str(Path(tmp) / "v"))
            self.assertEqual(code, 0, out)
            text = (Path(tmp) / "v" / "index.md").read_text()
            self.assertTrue(text.startswith("---\nsource_commit: abc1234\ntags: rate-limiter\naliases: limiter\n---\n"))
            self.assertIn("\nThis paragraph is hard wrapped.\n", text)
            self.assertIn("| a | [[libs/core/01-solve\\|solve]] |", text)  # table rows untouched
            code, _ = run("unwrap.py", str(Path(tmp) / "v"), "--check")
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
