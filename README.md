# git-herd

git-herd scans a directory for Git repositories and pulls them safely.

## Usage

```bash
git-herd
git-herd ~/code
git-herd ~/code --dry-run
git-herd ~/code --auto-stash
git-herd ~/code --max-depth 2
```

## Options

- `--dry-run`: show what would happen without changing repositories
- `--auto-stash`: stash dirty changes before pulling, then restore them
- `--max-depth`: limit how deep the scan goes below the root directory
