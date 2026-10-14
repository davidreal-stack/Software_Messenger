"""Logical message content, independent of delivery provider and recipient."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Message:
    """A non-empty message body prepared for delivery."""

    content: str
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID):
            raise ValueError("id must be a UUID")
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("content must not be empty or whitespace")
