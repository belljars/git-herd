# git-herd

`git-herd` scans a directory tree, finds Git repositories, and pulls them safely with `git pull --ff-only`.

It is intentionally small: point it at a folder full of repos and get a clear per-repo result plus a summary.

## What it does

- Recursively scans a root directory for Git repositories
- Skips repositories that are unsafe to pull
- Supports dry runs before making changes
- Can auto-stash dirty worktrees before pulling

## Safety rules

By default, a repository is skipped if it has:

- uncommitted changes
- merge conflicts
- a detached `HEAD`
- no upstream branch

All pulls use fast-forward only mode.

## Install

```bash
pip install .
```

Or install it locally for the current user:

```bash
./install.sh
```

Or run it directly from the repository:

```bash
./git-herd .
```

## Usage

```bash
git-herd [PATH] [--dry-run] [--auto-stash] [--max-depth N]
```

Examples:

```bash
git-herd ~/code
git-herd ~/code --dry-run
git-herd ~/code --auto-stash
git-herd ~/code --max-depth 2
```

## Options

- `PATH`: root directory to scan, defaults to `.`
- `--dry-run`: show what would happen without changing repositories
- `--auto-stash`: stash tracked and untracked changes before pulling, then pop the stash
- `--max-depth`: limit how deep the scan goes below the root

## Output

Each repository is reported individually, then a summary is printed.

Typical outcomes:

- `up to date`
- `pulled successfully`
- `skipped`
- `failed`
- dry-run previews such as `would pull` or `would skip`

## Requirements

- Python 3.10+
- Git available on `PATH`
