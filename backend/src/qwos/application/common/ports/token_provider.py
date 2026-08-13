"""
===============================================================================
Token Provider Interface
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any


class TokenProvider(ABC):
    """
    Generates and validates security tokens.
    """

    @abstractmethod
    async def create_access_token(
        self,
        *,
        subject: str,
        claims: dict[str, Any],
        expires_in: timedelta,
    ) -> str: ...

    @abstractmethod
    async def create_refresh_token(
        self,
        *,
        subject: str,
        expires_in: timedelta,
    ) -> str: ...

    @abstractmethod
    async def validate_token(
        self,
        token: str,
    ) -> dict[str, Any]: ...
