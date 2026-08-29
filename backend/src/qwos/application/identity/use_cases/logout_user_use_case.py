"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    logout_user_use_case.py

Description:
    Terminates an authenticated user session by revoking the refresh token
    and deactivating its associated session.

Responsibilities:
    - Validate the refresh JWT
    - Locate the persisted refresh token
    - Validate tenant ownership
    - Locate the associated session
    - Revoke the refresh token
    - Deactivate the session
    - Persist changes atomically

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import jwt

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.token_hasher import TokenHasher
from qwos.application.common.ports.token_provider import TokenProvider
from qwos.application.identity.commands.logout_user_command import (
    LogoutUserCommand,
)
from qwos.application.identity.responses.logout_user_response import (
    LogoutUserResponse,
)
from qwos.domains.identity.repositories.session_repository import (
    SessionRepository,
)
from qwos.domains.identity.repositories.session_token_repository import (
    SessionTokenRepository,
)


class LogoutUserUseCase:
    """
    Use case for terminating an authenticated user session.
    """

    def __init__(
        self,
        *,
        session_repository: SessionRepository,
        session_token_repository: SessionTokenRepository,
        token_provider: TokenProvider,
        token_hasher: TokenHasher,
        clock: Clock,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._session_repository = session_repository
        self._session_token_repository = session_token_repository
        self._token_provider = token_provider
        self._token_hasher = token_hasher
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: LogoutUserCommand,
    ) -> LogoutUserResponse:
        """
        Terminate the session associated with the supplied refresh token.
        """

        # ------------------------------------------------------------------
        # Validate JWT
        # ------------------------------------------------------------------

        try:
            claims = await self._token_provider.validate_token(
                command.refresh_token,
            )
        except jwt.InvalidTokenError as exc:
            raise ValueError("Invalid refresh token.") from exc

        # ------------------------------------------------------------------
        # Validate token type
        # ------------------------------------------------------------------

        if claims.get("type") != "refresh":
            raise ValueError("Invalid refresh token.")

        subject = claims.get("sub")

        if not isinstance(subject, str) or not subject:
            raise ValueError("Invalid refresh token.")

        # ------------------------------------------------------------------
        # Locate persisted refresh token
        # ------------------------------------------------------------------

        token_hash = self._token_hasher.hash(
            command.refresh_token,
        )

        session_token = self._session_token_repository.get_active_by_token_hash(
            token_hash,
        )

        if session_token is None:
            raise ValueError("Refresh token has been revoked or is invalid.")

        # ------------------------------------------------------------------
        # Tenant isolation
        # ------------------------------------------------------------------

        if session_token.tenant_id != command.tenant_id:
            raise ValueError("Invalid refresh token.")

        # ------------------------------------------------------------------
        # Token lifecycle
        # ------------------------------------------------------------------

        now = self._clock.now()

        if session_token.expires_at <= now:
            raise ValueError("Refresh token has expired.")

        if session_token.is_revoked:
            raise ValueError("Refresh token has been revoked.")

        # ------------------------------------------------------------------
        # Locate session
        # ------------------------------------------------------------------

        session = self._session_repository.get_by_id(
            session_token.session_id,
        )

        if session is None:
            raise ValueError("Session not found.")

        # ------------------------------------------------------------------
        # Validate session ownership
        # ------------------------------------------------------------------

        if session.tenant_id != command.tenant_id:
            raise ValueError("Invalid session.")

        # The refresh token JWT subject identifies the authenticated user.
        if session.user_id != subject:
            raise ValueError("Invalid session.")

        # ------------------------------------------------------------------
        # Revoke token
        # ------------------------------------------------------------------

        session_token.revoke(
            revoked_at=now,
            revoked_by=subject,
            reason="User logout",
        )

        # ------------------------------------------------------------------
        # Deactivate session
        # ------------------------------------------------------------------

        session.is_active = False
        session.signed_out_at = now
        session.last_activity_at = now

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._session_token_repository.save(session_token)
            self._session_repository.save(session)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return LogoutUserResponse(
            success=True,
            message="User logged out successfully.",
        )
