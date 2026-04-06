from pathlib import Path
import tempfile
import unittest

from git_herd.scanner import find_repositories


class ScannerTests(unittest.TestCase):
    def test_find_repositories_respects_depth(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            top = tmp_path / "top"
            deep = tmp_path / "a" / "b" / "deep"

            (top / ".git").mkdir(parents=True)
            (deep / ".git").mkdir(parents=True)

            repos = find_repositories(tmp_path, max_depth=1)
            self.assertEqual(repos, [top])

    def test_find_repositories_detects_git_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = tmp_path / "worktree"
            repo.mkdir()
            (repo / ".git").write_text("gitdir: /tmp/example\n", encoding="utf-8")

            repos = find_repositories(tmp_path)
            self.assertEqual(repos, [repo])


if __name__ == "__main__":
    unittest.main()
