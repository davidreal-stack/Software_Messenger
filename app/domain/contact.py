"""Contact entity and its minimal domain validation."""

from dataclasses import dataclass, field
import re
from uuid import UUID, uuid4


_PHONE_FORMATTING = re.compile(r"[\s().-]")
_PHONE_DIGITS = re.compile(r"\+?[1-9][0-9]{6,14}\Z")


@dataclass(frozen=True, slots=True)
class Contact:
    """A person addressable by a minimally validated telephone number."""

    name: str
    phone: str
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID):
            raise ValueError("id must be a UUID")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must not be empty")
        if not isinstance(self.phone, str):
            raise ValueError("phone must be a string")

        normalized_phone = _PHONE_FORMATTING.sub("", self.phone)
        if not _PHONE_DIGITS.fullmatch(normalized_phone):
            raise ValueError("phone must contain 7 to 15 digits and an optional leading '+'")

        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "phone", normalized_phone)
