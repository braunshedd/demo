import os
import subprocess
import sys
import tempfile
import unittest

LEDGER = "# january\n2026-01-04,groceries,12.50\n2026-01-05,transport,3.20\n"

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(args, stdin=""):
    return subprocess.run(
        [sys.executable, "-m", "tally", *args],
        capture_output=True,
        text=True,
        input=stdin,
        cwd=ROOT,
    )


class TestCli(unittest.TestCase):
    def test_reads_a_ledger_from_stdin(self):
        result = run([], stdin=LEDGER)
        self.assertEqual(result.returncode, 0)
        self.assertIn("total", result.stdout)
        self.assertIn("15.70", result.stdout)

    def test_reads_a_ledger_from_a_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "ledger.csv")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(LEDGER)
            result = run([path])
        self.assertEqual(result.returncode, 0)
        self.assertIn("15.70", result.stdout)

    def test_refuses_a_bad_ledger_without_a_traceback(self):
        result = run([], stdin="2026-01-04,sundries,12.50\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_refuses_a_file_that_is_not_there(self):
        result = run([os.path.join(ROOT, "no-such-ledger.csv")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
