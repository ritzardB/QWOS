"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

JWT Token Provider
===============================================================================
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from qwos.application.common.ports.token_provider import TokenProvider
from qwos.core.config.settings import settings


class JWTTokenProvider(TokenProvider):
    """
    PyJWT implementation of the TokenProvider contract.

    Responsibilities:
        - Create JWT access tokens
        - Create JWT refresh tokens
        - Validate JWT tokens

    Token claims:
        - sub: token subject
        - type: access or refresh
        - iat: issued-at timestamp
        - exp: expiration timestamp
        - Additional access-token claims are preserved
    """

    def __init__(self) -> None:
        self._secret_key = settings.JWT_SECRET_KEY
        self._algorithm = settings.JWT_ALGORITHM

    async def create_access_token(
        self,
        *,
        subject: str,
        claims: dict[str, Any],
        expires_in: timedelta,
    ) -> str:
        now = datetime.now(timezone.utc)
        expires_at = now + expires_in

        logger.warning(
            "JWT ACCESS DEBUG: now=%s expires_at=%s expires_in=%s subject=%s",
            now,
            expires_at,
            expires_in,
            subject,
        )

        payload = {
            "sub": subject,
            "type": "access",
            "iat": now,
            "exp": expires_at,
            **claims,
        }

        token = jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

        logger.warning(
            "JWT ACCESS DEBUG: token generated successfully"
        )

        return token

    async def create_refresh_token(
        self,
        *,
        subject: str,
        expires_in: timedelta,
    ) -> str:
        """
        Create a signed JWT refresh token.
        """

        now = datetime.now(timezone.utc)
        expires_at = now + expires_in

        payload: dict[str, Any] = {
            "sub": subject,
            "type": "refresh",
            "iat": now,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

    async def validate_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Validate and decode a JWT token.

        Raises:
            jwt.InvalidTokenError:
                If the token is invalid, expired, malformed,
                or signed with an unexpected algorithm.
        """

        return jwt.decode(
            token,
            self._secret_key,
            algorithms=[self._algorithm],
        )
