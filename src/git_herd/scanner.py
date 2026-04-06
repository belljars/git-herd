from __future__ import annotations

import os
from pathlib import Path


def find_repositories(root: Path, max_depth: int | None = None) -> list[Path]:
    root = root.resolve()
    repos: list[Path] = []

    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)
        rel_depth = len(current_path.relative_to(root).parts)

        if max_depth is not None and rel_depth > max_depth:
            dirnames[:] = []
            continue

        has_git_dir = ".git" in dirnames
        has_git_file = ".git" in filenames
        if has_git_dir or has_git_file:
            repos.append(current_path)
            dirnames[:] = []
            continue

        if max_depth is not None and rel_depth == max_depth:
            dirnames[:] = []

    return sorted(repos)
