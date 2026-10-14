"""Small domain record for a future independently tracked operation."""

from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from ._time import now_utc, require_utc


class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Job:
    """A minimal operation lifecycle record; it does not execute work."""

    id: UUID = field(default_factory=uuid4)
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=now_utc)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID):
            raise ValueError("id must be a UUID")
        if not isinstance(self.status, JobStatus):
            raise ValueError("status must be a JobStatus")
        require_utc(self.created_at, "created_at")
        for name, value in (("started_at", self.started_at), ("completed_at", self.completed_at)):
            if value is not None:
                require_utc(value, name)
                if value < self.created_at:
                    raise ValueError(f"{name} cannot precede created_at")
        if self.started_at is not None and self.completed_at is not None and self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")
        if self.error is not None and not self.error.strip():
            raise ValueError("error must not be empty")

        valid = {
            JobStatus.PENDING: self.started_at is None and self.completed_at is None and self.error is None,
            JobStatus.RUNNING: self.started_at is not None and self.completed_at is None and self.error is None,
            JobStatus.COMPLETED: self.started_at is not None and self.completed_at is not None and self.error is None,
            JobStatus.FAILED: self.completed_at is not None and self.error is not None,
        }
        if self.status not in valid or not valid[self.status]:
            raise ValueError("job fields do not match its status")

    def start(self, *, at: datetime | None = None) -> "Job":
        self._require_status(JobStatus.PENDING)
        started_at = at or now_utc()
        require_utc(started_at, "at")
        return replace(self, status=JobStatus.RUNNING, started_at=started_at)

    def complete(self, *, at: datetime | None = None) -> "Job":
        self._require_status(JobStatus.RUNNING)
        completed_at = at or now_utc()
        require_utc(completed_at, "at")
        return replace(self, status=JobStatus.COMPLETED, completed_at=completed_at)

    def fail(self, error: str, *, at: datetime | None = None) -> "Job":
        if self.status not in (JobStatus.PENDING, JobStatus.RUNNING):
            raise ValueError("only a pending or running job can fail")
        if not isinstance(error, str) or not error.strip():
            raise ValueError("error must not be empty")
        completed_at = at or now_utc()
        require_utc(completed_at, "at")
        return replace(self, status=JobStatus.FAILED, error=error.strip(), completed_at=completed_at)

    def _require_status(self, expected: JobStatus) -> None:
        if self.status is not expected:
            raise ValueError(f"job must be {expected.value} to perform this transition")
