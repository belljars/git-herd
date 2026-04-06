from __future__ import annotations

import argparse
from pathlib import Path

from git_herd.formatting import format_result, format_summary
from git_herd.runner import handle_repo
from git_herd.scanner import find_repositories


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan directories for Git repositories and pull them safely.")
    parser.add_argument("path", nargs="?", default=".", help="Root directory to scan.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without changing any repositories.")
    parser.add_argument("--auto-stash", action="store_true", help="Stash dirty changes before pulling, then pop the stash.")
    parser.add_argument("--max-depth", type=int, default=None, help="Maximum directory depth to scan below the root.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        parser.error(f"path does not exist: {root}")
    if not root.is_dir():
        parser.error(f"path is not a directory: {root}")
    if args.max_depth is not None and args.max_depth < 0:
        parser.error("--max-depth must be >= 0")

    repos = find_repositories(root, max_depth=args.max_depth)
    if not repos:
        print("No Git repositories found.")
        return 0

    results = [handle_repo(repo, dry_run=args.dry_run, auto_stash=args.auto_stash) for repo in repos]
    for result in results:
        print(format_result(result))
    print()
    print(format_summary(results))

    if any(result.outcome.value in {"failed", "would_fail"} for result in results):
        return 1
    return 0
