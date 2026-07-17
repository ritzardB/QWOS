"""
QWOS Specification Combinators

Provides logical composition for Specifications.

These classes allow Specifications to be combined
using AND, OR and NOT operators.

Business Specifications should inherit only from
Specification.

Repositories consume composed Specifications.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from sqlalchemy import and_, not_, or_
from sqlalchemy.sql.elements import ColumnElement

from .specification import Specification

T = TypeVar("T")


# ----------------------------------------------------------------------
# AND
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AndSpecification(
    Specification[T],
    Generic[T],
):
    left: Specification[T]
    right: Specification[T]

    def as_expression(
        self,
        model: type[T],
    ) -> ColumnElement[bool]:

        return and_(
            self.left.as_expression(model),
            self.right.as_expression(model),
        )


# ----------------------------------------------------------------------
# OR
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class OrSpecification(
    Specification[T],
    Generic[T],
):
    left: Specification[T]
    right: Specification[T]

    def as_expression(
        self,
        model: type[T],
    ) -> ColumnElement[bool]:

        return or_(
            self.left.as_expression(model),
            self.right.as_expression(model),
        )


# ----------------------------------------------------------------------
# NOT
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class NotSpecification(
    Specification[T],
    Generic[T],
):
    specification: Specification[T]

    def as_expression(
        self,
        model: type[T],
    ) -> ColumnElement[bool]:

        return not_(
            self.specification.as_expression(model)
        )