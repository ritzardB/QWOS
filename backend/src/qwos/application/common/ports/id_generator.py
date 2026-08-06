"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

ID Generator Contract

File:
    id_generator.py

Description:
    Defines the contract for generating unique identifiers.

Responsibilities:
    - Generate unique identifiers
    - Remain independent of implementation

Notes:
    Infrastructure provides the concrete implementation.
    The implementation may use ULID, UUIDv7, Snowflake, NanoID,
    or any future identifier strategy.
===============================================================================
"""

from __future__ import annotations

from typing import Protocol


class IdGenerator(Protocol):
    """
    Contract for generating unique identifiers.
    """

    def generate(self) -> str:
        """
        Generate a unique identifier.

        Returns:
            A unique string identifier.
        """
        ...