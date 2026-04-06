from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Outcome(str, Enum):
    UP_TO_DATE = "up_to_date"
    PULLED = "pulled"
    SKIPPED = "skipped"
    FAILED = "failed"
    WOULD_PULL = "would_pull"
    WOULD_SKIP = "would_skip"
    WOULD_FAIL = "would_fail"


@dataclass(slots=True)
class RepoState:
    path: Path
    dirty: bool
    detached_head: bool
    has_upstream: bool
    merge_conflicts: bool


@dataclass(slots=True)
class RepoResult:
    path: Path
    outcome: Outcome
    reason: str
