"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    refresh_access_token_use_case.py

Description:
    Refreshes an authenticated user's access and refresh tokens.

Responsibilities:
    - Validate the supplied refresh JWT
    - Verify the refresh-token type
    - Locate the persisted refresh-token record
    - Validate token lifecycle
    - Validate the associated session
    - Validate the associated user
    - Rotate the refresh token
    - Generate a new access token
    - Persist the new refresh-token hash
    - Update session activity
    - Commit the operation atomically

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import timedelta

import jwt

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.account_locked_exception import AccountLockedException
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.ports.token_hasher import TokenHasher
from qwos.application.common.ports.token_provider import TokenProvider
from qwos.application.identity.commands.refresh_access_token_command import (
    RefreshAccessTokenCommand,
)
from qwos.application.identity.responses.refresh_access_token_response import (
    RefreshAccessTokenResponse,
)
from qwos.application.common.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.models.session_token import SessionToken
from qwos.domains.identity.repositories.session_repository import (
    SessionRepository,
)
from qwos.domains.identity.repositories.session_token_repository import (
    SessionTokenRepository,
)
from qwos.domains.identity.repositories.user_repository import UserRepository


class RefreshAccessTokenUseCase:
    """
    Use case for refreshing an authenticated session.
    """

    ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)

    def __init__(
        self,
        *,
        user_repository: UserRepository,
        session_repository: SessionRepository,
        session_token_repository: SessionTokenRepository,
        token_provider: TokenProvider,
        token_hasher: TokenHasher,
        id_generator: IdGenerator,
        clock: Clock,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._session_token_repository = session_token_repository
        self._token_provider = token_provider
        self._token_hasher = token_hasher
        self._id_generator = id_generator
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: RefreshAccessTokenCommand,
    ) -> RefreshAccessTokenResponse:
        """
        Refresh the access and refresh tokens for an authenticated session.
        """

        # ------------------------------------------------------------------
        # Validate JWT
        # ------------------------------------------------------------------

        try:
            claims = await self._token_provider.validate_token(
                command.refresh_token,
            )
        except jwt.InvalidTokenError as exc:
            raise InvalidCredentialsException() from exc

        # ------------------------------------------------------------------
        # Validate token type
        # ------------------------------------------------------------------

        if claims.get("type") != "refresh":
            raise InvalidCredentialsException()

        subject = claims.get("sub")

        if not isinstance(subject, str) or not subject:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Locate persisted refresh token
        # ------------------------------------------------------------------

        token_hash = self._token_hasher.hash(
            command.refresh_token,
        )

        session_token = (
            self._session_token_repository.get_active_by_token_hash(
                token_hash,
            )
        )

        if session_token is None:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Time
        # ------------------------------------------------------------------

        now = self._clock.now()

        # ------------------------------------------------------------------
        # Token lifecycle
        # ------------------------------------------------------------------

        if session_token.expires_at <= now:
            raise InvalidCredentialsException()
        if session_token.is_revoked:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Locate session
        # ------------------------------------------------------------------

        session = self._session_repository.get_active_by_id(
            session_token.session_id,
        )

        if session is None:
            raise InvalidCredentialsException()

        if session.expires_at <= now:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Locate user
        # ------------------------------------------------------------------

        user = self._user_repository.get_by_id(
            subject,
        )

        if user is None:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Tenant isolation
        # ------------------------------------------------------------------

        if user.tenant_id != session_token.tenant_id:
            raise InvalidCredentialsException()

        if user.tenant_id != session.tenant_id:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Account status
        # ------------------------------------------------------------------

        if user.account_status == AccountStatus.LOCKED:
            raise AccountLockedException()

        if user.account_status != AccountStatus.ACTIVE:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Session ownership
        # ------------------------------------------------------------------

        if session.user_id != user.id:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Generate access-token lifetime
        # ------------------------------------------------------------------

        session_remaining = session.expires_at - now

        access_expires_in = min(
            self.ACCESS_TOKEN_LIFETIME,
            session_remaining,
        )

        if access_expires_in <= timedelta(0):
            raise InvalidCredentialsException()

        access_expires_at = now + access_expires_in

        # ------------------------------------------------------------------
        # Generate identifiers
        # ------------------------------------------------------------------

        new_session_token_id = self._id_generator.generate()

        # ------------------------------------------------------------------
        # Generate new access token
        # ------------------------------------------------------------------

        access_token = await self._token_provider.create_access_token(
            subject=user.id,
            claims={
                "tenant_id": user.tenant_id,
                "user_type": str(user.user_type),
                "session_id": session.id,
            },
            expires_in=access_expires_in,
        )

        # ------------------------------------------------------------------
        # Generate new refresh token
        # ------------------------------------------------------------------

        refresh_expires_in = session_remaining

        refresh_token = await self._token_provider.create_refresh_token(
            subject=user.id,
            expires_in=refresh_expires_in,
        )

        # ------------------------------------------------------------------
        # Hash new refresh token
        # ------------------------------------------------------------------

        refresh_token_hash = self._token_hasher.hash(
            refresh_token,
        )

        # ------------------------------------------------------------------
        # Rotate existing refresh token
        # ------------------------------------------------------------------

        session_token.revoke(
            revoked_at=now,
            revoked_by=user.id,
            reason="ROTATED",
        )

        session_token.mark_used(
            used_at=now,
        )

        # ------------------------------------------------------------------
        # Create replacement refresh-token record
        # ------------------------------------------------------------------

        new_session_token = SessionToken.create(
            id=new_session_token_id,
            tenant_id=user.tenant_id,
            session_id=session.id,
            token_hash=refresh_token_hash,
            expires_at=session.expires_at,
            created_by=user.id,
            rotated_from_token_id=session_token.id,
        )

        new_session_token.issued_at = now

        # ------------------------------------------------------------------
        # Update session activity
        # ------------------------------------------------------------------

        session.last_activity_at = now

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._session_token_repository.save(session_token)
            self._session_token_repository.save(new_session_token)
            self._session_repository.save(session)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return RefreshAccessTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_at=access_expires_at,
            user_id=user.id,
            session_id=session.id,
        )