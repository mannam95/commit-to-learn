import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pr_utils


class ParseReposAndPrsTests(unittest.TestCase):
    def test_parses_single_line_array(self):
        raw = '[["repo-a", 1], ["repo-b", 2]]'
        self.assertEqual(
            [("repo-a", 1), ("repo-b", 2)],
            pr_utils.parse_repos_and_prs(raw),
        )

    def test_ignores_missing_commas_between_entries(self):
        # Regression: uncommenting one list entry without adding a trailing
        # comma to the previous line used to raise a JSONDecodeError.
        raw = '[\n["repo-a", 1]\n["repo-b", 2]\n]'
        self.assertEqual(
            [("repo-a", 1), ("repo-b", 2)],
            pr_utils.parse_repos_and_prs(raw),
        )

    def test_empty_or_none_returns_empty_list(self):
        self.assertEqual([], pr_utils.parse_repos_and_prs(""))
        self.assertEqual([], pr_utils.parse_repos_and_prs(None))


class LoadDotenvTests(unittest.TestCase):
    def setUp(self):
        self._keys_before = set(os.environ)

    def tearDown(self):
        for key in set(os.environ) - self._keys_before:
            del os.environ[key]

    def _write_env(self, content):
        fd, path = tempfile.mkstemp(suffix=".env")
        with os.fdopen(fd, "w") as f:
            f.write(content)
        self.addCleanup(os.remove, path)
        return path

    def test_reads_simple_key_value_pairs(self):
        path = self._write_env("FOO=bar\nBAZ=qux\n")
        pr_utils.load_dotenv(path)
        self.assertEqual("bar", os.environ["FOO"])
        self.assertEqual("qux", os.environ["BAZ"])

    def test_does_not_override_existing_environment_variable(self):
        os.environ["FOO"] = "already-set"
        path = self._write_env("FOO=bar\n")
        pr_utils.load_dotenv(path)
        self.assertEqual("already-set", os.environ["FOO"])

    def test_skips_blank_and_comment_lines(self):
        path = self._write_env("# a comment\n\nFOO=bar\n")
        pr_utils.load_dotenv(path)
        self.assertEqual("bar", os.environ["FOO"])

    def test_accumulates_multiline_array_and_skips_commented_entries(self):
        path = self._write_env(
            "REPOS=[\n"
            '    # ["skip-me", 1],\n'
            '    ["keep-me", 2]\n'
            "]\n"
            "AFTER=still-parsed\n"
        )
        pr_utils.load_dotenv(path)
        self.assertEqual(
            [("keep-me", 2)],
            pr_utils.parse_repos_and_prs(os.environ["REPOS"]),
        )
        self.assertEqual("still-parsed", os.environ["AFTER"])

    def test_missing_file_is_a_silent_noop(self):
        pr_utils.load_dotenv("/nonexistent/path/.env")  # should not raise


if __name__ == "__main__":
    unittest.main()
