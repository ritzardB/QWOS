"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    use_case_error.py

Description:
    Represents a business or application error.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UseCaseError:
    """
    Represents an application error.
    """

    code: str

    message: str

    field: str | None = None
