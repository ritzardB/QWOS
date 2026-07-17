"""
QWOS Specifications

Implements the Specification Pattern used to express
business rules independently of persistence concerns.

Repositories translate specifications into SQLAlchemy
expressions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy import and_, not_, or_

T = TypeVar("T")


# ----------------------------------------------------------------------
# Base Specification
# ----------------------------------------------------------------------


class Specification(Generic[T], ABC):
    """
    Base class for all specifications.
    """

    @abstractmethod
    def to_expression(
        self,
        model: type[T],
    ) -> ColumnElement[bool]:
        """
        Convert the specification into a SQLAlchemy
        boolean expression.
        """
        raise NotImplementedError

    # --------------------------------------------------------------
    # Composition
    # --------------------------------------------------------------

    def __and__(
        self,
        other: "Specification[T]",
    ) -> "Specification[T]":
        return AndSpecification(self, other)

    def __or__(
        self,
        other: "Specification[T]",
    ) -> "Specification[T]":
        return OrSpecification(self, other)

    def __invert__(
        self,
    ) -> "Specification[T]":
        return NotSpecification(self)
    
# --------------------------------------------------------------
# And Specification
# --------------------------------------------------------------

class AndSpecification(Specification[T]):

    def __init__(
        self,
        left: Specification[T],
        right: Specification[T],
    ):
        self.left = left
        self.right = right

    def to_expression(
        self,
        model: type[T],
    ) -> ColumnElement[bool]:

        return and_(
            self.left.to_expression(model),
            self.right.to_expression(model),
        )
    
# ----------------------------------------------------------------------
# Or Specification
# ----------------------------------------------------------------------

class OrSpecification(Specification[T]):

    def __init__(
        self,
        left: Specification[T],
        right: Specification[T],
    ):
        self.left = left
        self.right = right

    def to_expression(
        self,
        model: type[T],
    ) -> ColumnElement[bool]:

        return or_(
            self.left.to_expression(model),
            self.right.to_expression(model),
        )
    
# ----------------------------------------------------------------------
# Not Specification
# ----------------------------------------------------------------------

class NotSpecification(Specification[T]):

    def __init__(
        self,
        specification: Specification[T],
    ):
        self.specification = specification

    def to_expression(
        self,
        model: type[T],
    ) -> ColumnElement[bool]:

        return not_(
            self.specification.to_expression(model)
        )

    
