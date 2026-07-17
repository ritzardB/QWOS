"""
QWOS Pagination

Shared pagination models used throughout the repository layer.

These classes are intentionally independent of:
- FastAPI
- SQLAlchemy
- Pydantic

They belong to the Core layer and may be reused by
REST APIs, GraphQL, background jobs, and CLI tools.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil
from typing import Generic, TypeVar

T = TypeVar("T")


# ----------------------------------------------------------------------
# Page Request
# ----------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PageRequest:
    """
    Represents a pagination request.

    Example:
        PageRequest(page=2, page_size=25)
    """

    page: int = 1
    page_size: int = 25

    def __post_init__(self) -> None:
        if self.page < 1:
            raise ValueError("page must be >= 1")

        if self.page_size < 1:
            raise ValueError("page_size must be >= 1")

    @property
    def offset(self) -> int:
        """
        SQL offset.
        """
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """
        SQL limit.
        """
        return self.page_size


# ----------------------------------------------------------------------
# Page Result
# ----------------------------------------------------------------------

@dataclass(slots=True)
class PageResult(Generic[T]):
    """
    Represents a paginated response.
    """

    items: list[T] = field(default_factory=list)

    total_items: int = 0

    page: int = 1

    page_size: int = 25

    @property
    def total_pages(self) -> int:
        if self.total_items == 0:
            return 0

        return ceil(self.total_items / self.page_size)

    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def is_first_page(self) -> bool:
        return self.page == 1

    @property
    def is_last_page(self) -> bool:
        return self.page >= self.total_pages