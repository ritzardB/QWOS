"""
QWOS Sorting

Shared sorting models used throughout the repository layer.

These classes are intentionally independent of:
- FastAPI
- SQLAlchemy
- Pydantic

Repositories translate these objects into ORM expressions.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum

# ----------------------------------------------------------------------
# Sort Direction
# ----------------------------------------------------------------------


class SortDirection(str, Enum):
    """
    Supported sort directions.
    """

    ASC = "asc"
    DESC = "desc"


# ----------------------------------------------------------------------
# Sort
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Sort:
    """
    Represents a single sort criterion.

    Example:
        Sort.asc("last_name")
        Sort.desc("created_at")
    """

    field: str

    direction: SortDirection = SortDirection.ASC

    # --------------------------------------------------------------
    # Factory Methods
    # --------------------------------------------------------------

    @classmethod
    def asc(cls, field: str) -> "Sort":
        """
        Create an ascending sort criterion.
        """
        return cls(field=field,direction=SortDirection.ASC,)

    @classmethod
    def desc(cls, field: str) -> "Sort":
        return cls(field=field,direction=SortDirection.DESC,)
    
    def __post_init__(self) -> None:
        if not self.field.strip():
            raise ValueError("field must not be empty")

    def __repr__(self) -> str:
        return f"Sort(field={self.field!r}, " f"direction={self.direction.value!r})"


@dataclass(frozen=True, slots=True)
class SortCollection:
    
    items: tuple[Sort, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> "SortCollection":
        return cls()

    @classmethod
    def of(cls, *sorts: Sort) -> "SortCollection":
        return cls(items=tuple(sorts))

    def __iter__(self) -> Iterator[Sort]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __bool__(self) -> bool:
        return bool(self.items)

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0

    @property
    def is_not_empty(self) -> bool:
        return not self.is_empty

    