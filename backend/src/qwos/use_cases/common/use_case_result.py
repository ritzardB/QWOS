"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    use_case_result.py

Description:
    Standard result object returned by every application use case.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .use_case_error import UseCaseError

T = TypeVar("T")


@dataclass(slots=True)
class UseCaseResult(Generic[T]):
    """
    Represents the outcome of a use case.
    """

    succeeded: bool

    data: T | None = None

    message: str | None = None

    errors: list[UseCaseError] | None = None

    @classmethod
    def success(
        cls,
        data: T | None = None,
        message: str | None = None,
    ) -> "UseCaseResult[T]":
        return cls(
            succeeded=True,
            data=data,
            message=message,
            errors=None,
        )

    @classmethod
    def failure(
        cls,
        *,
        message: str,
        errors: list[UseCaseError] | None = None,
    ) -> "UseCaseResult[T]":
        return cls(
            succeeded=False,
            data=None,
            message=message,
            errors=errors,
        )

    @property
    def failed(self) -> bool:
        return not self.succeeded
