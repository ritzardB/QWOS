"""
QWOS Filtering

Defines reusable filtering models for repositories.

This module is intentionally independent of:
- SQLAlchemy
- FastAPI
- Pydantic

Repositories translate these filter objects into ORM
expressions.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# ----------------------------------------------------------------------
# Filter Operator
# ----------------------------------------------------------------------


class FilterOperator(str, Enum):
    """Supported comparison operators."""

    EQ = "eq"
    NE = "ne"

    GT = "gt"
    GTE = "gte"

    LT = "lt"
    LTE = "lte"

    IN = "in"
    NOT_IN = "not_in"

    BETWEEN = "between"

    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"

    LIKE = "like"
    ILIKE = "ilike"

    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"


# ----------------------------------------------------------------------
# Filter
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Filter:
    """
    Represents a single filter condition.
    """

    field: str
    operator: FilterOperator
    value: Any | None = None

    # --------------------------------------------------------------
    # Equality
    # --------------------------------------------------------------

    @classmethod
    def equals(cls, field: str, value: Any) -> "Filter":
        return cls(field, FilterOperator.EQ, value)

    @classmethod
    def not_equals(cls, field: str, value: Any) -> "Filter":
        return cls(field, FilterOperator.NE, value)

    # --------------------------------------------------------------
    # Comparison
    # --------------------------------------------------------------

    @classmethod
    def greater_than(cls, field: str, value: Any) -> "Filter":
        return cls(field, FilterOperator.GT, value)

    @classmethod
    def greater_than_or_equal(cls, field: str, value: Any) -> "Filter":
        return cls(field, FilterOperator.GTE, value)

    @classmethod
    def less_than(cls, field: str, value: Any) -> "Filter":
        return cls(field, FilterOperator.LT, value)

    @classmethod
    def less_than_or_equal(cls, field: str, value: Any) -> "Filter":
        return cls(field, FilterOperator.LTE, value)

    # --------------------------------------------------------------
    # String Operations
    # --------------------------------------------------------------

    @classmethod
    def contains(cls, field: str, value: str) -> "Filter":
        return cls(field, FilterOperator.CONTAINS, value)

    @classmethod
    def starts_with(cls, field: str, value: str) -> "Filter":
        return cls(field, FilterOperator.STARTS_WITH, value)

    @classmethod
    def ends_with(cls, field: str, value: str) -> "Filter":
        return cls(field, FilterOperator.ENDS_WITH, value)

    @classmethod
    def like(cls, field: str, value: str) -> "Filter":
        return cls(field, FilterOperator.LIKE, value)

    @classmethod
    def ilike(cls, field: str, value: str) -> "Filter":
        return cls(field, FilterOperator.ILIKE, value)

    # --------------------------------------------------------------
    # Collection Operations
    # --------------------------------------------------------------

    @classmethod
    def in_list(
        cls,
        field: str,
        values: Sequence[Any],
    ) -> "Filter":
        return cls(field, FilterOperator.IN, tuple(values))

    @classmethod
    def not_in_list(
        cls,
        field: str,
        values: Sequence[Any],
    ) -> "Filter":
        return cls(field, FilterOperator.NOT_IN, tuple(values))

    # --------------------------------------------------------------
    # Range
    # --------------------------------------------------------------

    @classmethod
    def between(
        cls,
        field: str,
        start: Any,
        end: Any,
    ) -> "Filter":
        return cls(field, FilterOperator.BETWEEN, (start, end))

    # --------------------------------------------------------------
    # Null Checks
    # --------------------------------------------------------------

    @classmethod
    def is_null(cls, field: str) -> "Filter":
        return cls(field, FilterOperator.IS_NULL)

    @classmethod
    def is_not_null(cls, field: str) -> "Filter":
        return cls(field, FilterOperator.IS_NOT_NULL)

    # --------------------------------------------------------------
    # Debugging
    # --------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Filter("
            f"field={self.field!r}, "
            f"operator={self.operator.value!r}, "
            f"value={self.value!r})"
        )


# ----------------------------------------------------------------------
# Filter Collection
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Filters:
    """
    Immutable collection of filters.
    """

    items: tuple[Filter, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> "Filters":
        """Return an empty filter collection."""
        return cls()

    @classmethod
    def of(cls, *filters: Filter) -> "Filters":
        """Create a collection from filters."""
        return cls(items=tuple(filters))

    def __iter__(self) -> Iterator[Filter]:
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
