"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Validation Error

File:
    validation_error.py

Description:
    Represents a single validation error.

Responsibilities:
    - Store field name
    - Store validation message
    - Remain immutable
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationError:
    """
    Represents a validation error.
    """

    field: str
    message: str
