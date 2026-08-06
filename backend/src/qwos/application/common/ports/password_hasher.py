"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Password Hasher Port

Description:
    Defines the contract for password hashing.

Responsibilities:
    - Hash passwords
    - Verify password hashes

Notes:
    Infrastructure provides the implementation.
===============================================================================
"""

from __future__ import annotations

from typing import Protocol


class PasswordHasher(Protocol):
    """
    Password hashing contract.
    """

    def hash(
        self,
        plain_password: str,
    ) -> str:
        """
        Hash a plain-text password.
        """
        ...

    def verify(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a password against its hash.
        """
        ...
