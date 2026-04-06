from __future__ import annotations

from collections import defaultdict

from git_herd.models import Outcome, RepoResult


ICON_BY_OUTCOME = {
    Outcome.UP_TO_DATE: "✔",
    Outcome.PULLED: "⬇",
    Outcome.SKIPPED: "⚠",
    Outcome.FAILED: "✖",
    Outcome.WOULD_PULL: "◌",
    Outcome.WOULD_SKIP: "◌",
    Outcome.WOULD_FAIL: "◌",
}


def format_result(result: RepoResult) -> str:
    icon = ICON_BY_OUTCOME[result.outcome]
    name = result.path.name
    message = _message_for(result)
    return f"{icon} {name} -> {message}"


def format_summary(results: list[RepoResult]) -> str:
    grouped: dict[str, list[RepoResult]] = defaultdict(list)
    order = ("failed", "skipped", "pulled", "up_to_date", "would_fail", "would_skip", "would_pull")

    for result in results:
        grouped[result.outcome.value].append(result)

    lines = ["SUMMARY:"]
    for key in order:
        items = grouped.get(key)
        if not items:
            continue
        label = key.replace("_", " ")
        lines.append(f"{label}:")
        for item in items:
            lines.append(f"- {item.path.name} ({item.reason})")
    return "\n".join(lines)


def _message_for(result: RepoResult) -> str:
    if result.outcome is Outcome.UP_TO_DATE:
        return "up to date"
    if result.outcome is Outcome.PULLED:
        return "pulled successfully"
    if result.outcome is Outcome.SKIPPED:
        return f"skipped ({result.reason})"
    if result.outcome is Outcome.FAILED:
        return f"failed ({result.reason})"
    if result.outcome is Outcome.WOULD_PULL:
        return f"dry run ({result.reason})"
    if result.outcome is Outcome.WOULD_SKIP:
        return f"would skip ({result.reason})"
    return f"would fail ({result.reason})"
