"""
===============================================================================
Password Hasher Interface
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """
    Password hashing abstraction.
    """

    @abstractmethod
    async def hash(
        self,
        password: str,
    ) -> str: ...

    @abstractmethod
    async def verify(
        self,
        *,
        password: str,
        password_hash: str,
    ) -> bool: ...
