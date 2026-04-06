from pathlib import Path
import unittest

from git_herd.formatting import format_result, format_summary
from git_herd.models import Outcome, RepoResult


class FormattingTests(unittest.TestCase):
    def test_format_result_for_skip(self) -> None:
        result = RepoResult(path=Path("/tmp/repo-c"), outcome=Outcome.SKIPPED, reason="uncommitted changes")
        self.assertEqual(format_result(result), "⚠ repo-c -> skipped (uncommitted changes)")

    def test_summary_groups_by_outcome(self) -> None:
        results = [
            RepoResult(path=Path("/tmp/repo-d"), outcome=Outcome.FAILED, reason="no upstream branch"),
            RepoResult(path=Path("/tmp/repo-c"), outcome=Outcome.SKIPPED, reason="dirty working tree"),
        ]
        summary = format_summary(results)
        self.assertIn("failed:", summary)
        self.assertIn("- repo-d (no upstream branch)", summary)
        self.assertIn("skipped:", summary)
        self.assertIn("- repo-c (dirty working tree)", summary)


if __name__ == "__main__":
    unittest.main()
