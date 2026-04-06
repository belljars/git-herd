from __future__ import annotations

from pathlib import Path

from git_herd.git import run_git
from git_herd.models import Outcome, RepoResult, RepoState


def inspect_repo(path: Path) -> RepoState:
    dirty = bool(run_git(path, "status", "--porcelain").stdout.strip())
    detached_head = run_git(path, "symbolic-ref", "-q", "HEAD").returncode != 0
    has_upstream = run_git(path, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}").returncode == 0
    merge_conflicts = bool(run_git(path, "diff", "--name-only", "--diff-filter=U").stdout.strip())
    return RepoState(
        path=path,
        dirty=dirty,
        detached_head=detached_head,
        has_upstream=has_upstream,
        merge_conflicts=merge_conflicts,
    )


def handle_repo(path: Path, *, dry_run: bool, auto_stash: bool) -> RepoResult:
    state = inspect_repo(path)

    blocked_reason = _blocked_reason(state, auto_stash=auto_stash)
    if blocked_reason is not None:
        outcome = Outcome.WOULD_SKIP if dry_run else Outcome.SKIPPED
        return RepoResult(path=path, outcome=outcome, reason=blocked_reason)

    if dry_run:
        preview = run_git(path, "pull", "--ff-only", "--dry-run")
        if preview.returncode != 0:
            return RepoResult(path=path, outcome=Outcome.WOULD_FAIL, reason=_stderr_reason(preview.stderr))
        if _pull_has_updates(preview.stdout, preview.stderr):
            return RepoResult(path=path, outcome=Outcome.WOULD_PULL, reason="would pull updates")
        return RepoResult(path=path, outcome=Outcome.UP_TO_DATE, reason="already up to date")

    if auto_stash and state.dirty:
        return _pull_with_auto_stash(path)

    pull = run_git(path, "pull", "--ff-only")
    if pull.returncode != 0:
        return RepoResult(path=path, outcome=Outcome.FAILED, reason=_stderr_reason(pull.stderr))
    if _pull_has_updates(pull.stdout, pull.stderr):
        return RepoResult(path=path, outcome=Outcome.PULLED, reason="pulled successfully")
    return RepoResult(path=path, outcome=Outcome.UP_TO_DATE, reason="already up to date")


def _blocked_reason(state: RepoState, *, auto_stash: bool) -> str | None:
    if state.merge_conflicts:
        return "merge conflicts"
    if state.detached_head:
        return "detached HEAD"
    if not state.has_upstream:
        return "no upstream branch"
    if state.dirty and not auto_stash:
        return "uncommitted changes"
    return None


def _pull_with_auto_stash(path: Path) -> RepoResult:
    stash = run_git(path, "stash", "push", "--include-untracked", "--message", "git-herd-auto-stash")
    if stash.returncode != 0:
        return RepoResult(path=path, outcome=Outcome.FAILED, reason=f"auto-stash failed: {_stderr_reason(stash.stderr)}")

    pull = run_git(path, "pull", "--ff-only")
    if pull.returncode != 0:
        restore = run_git(path, "stash", "pop")
        reason = _stderr_reason(pull.stderr)
        if restore.returncode != 0:
            reason = f"{reason}; stash pop failed: {_stderr_reason(restore.stderr)}"
        return RepoResult(path=path, outcome=Outcome.FAILED, reason=reason)

    pop = run_git(path, "stash", "pop")
    if pop.returncode != 0:
        return RepoResult(path=path, outcome=Outcome.FAILED, reason=f"pulled, but stash pop failed: {_stderr_reason(pop.stderr)}")

    if _pull_has_updates(pull.stdout, pull.stderr):
        return RepoResult(path=path, outcome=Outcome.PULLED, reason="pulled successfully with auto-stash")
    return RepoResult(path=path, outcome=Outcome.UP_TO_DATE, reason="already up to date after auto-stash")


def _pull_has_updates(stdout: str, stderr: str) -> bool:
    combined = f"{stdout}\n{stderr}"
    return "Already up to date." not in combined


def _stderr_reason(stderr: str) -> str:
    cleaned = [line.strip() for line in stderr.splitlines() if line.strip()]
    if cleaned:
        return cleaned[-1]
    return "git command failed"
