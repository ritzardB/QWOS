"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    authenticate_user_use_case.py

Description:
    Authenticates an existing user and establishes an authenticated session.

Responsibilities:
    - Locate the user
    - Validate account status
    - Verify the password
    - Generate the authenticated session
    - Generate access and refresh tokens
    - Persist the session and refresh-token hash
    - Update the user's last-login timestamp

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import logging
from datetime import timedelta

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.account_locked_exception import (
    AccountLockedException,
)
from qwos.application.common.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.ports.password_hasher import PasswordHasher
from qwos.application.common.ports.token_hasher import TokenHasher
from qwos.application.common.ports.token_provider import TokenProvider
from qwos.application.identity.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from qwos.application.identity.responses.authenticate_user_response import (
    AuthenticateUserResponse,
)
from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.models.session import Session
from qwos.domains.identity.models.session_token import SessionToken
from qwos.domains.identity.repositories.session_repository import (
    SessionRepository,
)
from qwos.domains.identity.repositories.session_token_repository import (
    SessionTokenRepository,
)
from qwos.domains.identity.repositories.user_repository import UserRepository


class AuthenticateUserUseCase:
    """
    Use case for authenticating an existing user.
    """

    def __init__(
        self,
        *,
        user_repository: UserRepository,
        session_repository: SessionRepository,
        session_token_repository: SessionTokenRepository,
        password_hasher: PasswordHasher,
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
        self._password_hasher = password_hasher
        self._token_provider = token_provider
        self._token_hasher = token_hasher
        self._id_generator = id_generator
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: AuthenticateUserCommand,
    ) -> AuthenticateUserResponse:
        """
        Authenticate a user and establish a session.
        """

        logger = logging.getLogger(__name__)

        # ------------------------------------------------------------------
        # Diagnostic logging
        # ------------------------------------------------------------------

        logger.warning(
            "AUTH DEBUG: email=%r tenant=%r password_length=%d",
            command.email,
            command.tenant_id,
            len(command.password),
        )

        # ------------------------------------------------------------------
        # Locate user
        # ------------------------------------------------------------------

        user = self._user_repository.get_by_email(
            command.email,
        )

        logger.warning(
            "AUTH DEBUG: user_found=%s",
            user is not None,
        )

        if user is None:
            raise InvalidCredentialsException()

        # ------------------------------------------------------------------
        # Tenant isolation
        # ------------------------------------------------------------------

        logger.warning(
            "AUTH DEBUG: user_tenant=%r type=%s len=%d",
            user.tenant_id,
            type(user.tenant_id).__name__,
            len(user.tenant_id),
        )

        logger.warning(
            "AUTH DEBUG: request_tenant=%r type=%s len=%d",
            command.tenant_id,
            type(command.tenant_id).__name__,
            len(command.tenant_id),
        )

        logger.warning(
            "AUTH DEBUG: tenant_equal=%s",
            user.tenant_id == command.tenant_id,
        )

        if user.tenant_id != command.tenant_id:
            logger.warning(
                "AUTH DEBUG: TENANT MISMATCH user=%r request=%r",
                user.tenant_id,
                command.tenant_id,
            )
            raise InvalidCredentialsException()

        logger.warning(
            "AUTH DEBUG: tenant_match=True",
        )

        # ------------------------------------------------------------------
        # Account status
        # ------------------------------------------------------------------

        logger.warning(
            "AUTH DEBUG: account_status=%r",
            user.account_status,
        )

        if user.account_status == AccountStatus.LOCKED:
            raise AccountLockedException()

        if user.account_status != AccountStatus.ACTIVE:
            raise ValueError("Account is not active.")

        # ------------------------------------------------------------------
        # Password
        # ------------------------------------------------------------------

        logger.warning(
            "AUTH DEBUG: password_hash_present=%s hash_length=%s hash_prefix=%r",
            bool(user.password_hash),
            len(user.password_hash) if user.password_hash else None,
            user.password_hash[:7] if user.password_hash else None,
        )

        if not user.password_hash:
            raise InvalidCredentialsException()

        password_valid = self._password_hasher.verify(
            command.password,
            user.password_hash,
        )

        logger.warning(
            "AUTH DEBUG: password_valid=%s",
            password_valid,
        )

        if not password_valid:
            raise ValueError("Invalid email or password.")

        # ------------------------------------------------------------------
        # Time
        # ------------------------------------------------------------------

        now = self._clock.now()

        access_expires_in = timedelta(minutes=15)

        refresh_expires_in = timedelta(
            days=30 if command.remember_me else 7,
        )

        access_expires_at = now + access_expires_in
        refresh_expires_at = now + refresh_expires_in

        # ------------------------------------------------------------------
        # Generate identifiers
        # ------------------------------------------------------------------

        session_id = self._id_generator.generate()
        session_token_id = self._id_generator.generate()

        # ------------------------------------------------------------------
        # Generate tokens
        # ------------------------------------------------------------------

        access_token = await self._token_provider.create_access_token(
            subject=user.id,
            claims={
                "tenant_id": user.tenant_id,
                "user_type": str(user.user_type),
                "session_id": session_id,
            },
            expires_in=access_expires_in,
        )

        refresh_token = await self._token_provider.create_refresh_token(
            subject=user.id,
            expires_in=refresh_expires_in,
        )

        # ------------------------------------------------------------------
        # Hash refresh token
        # ------------------------------------------------------------------

        refresh_token_hash = self._token_hasher.hash(
            refresh_token,
        )

        # ------------------------------------------------------------------
        # Create session
        # ------------------------------------------------------------------

        session = Session.create(
            id=session_id,
            tenant_id=user.tenant_id,
            user_id=user.id,
            expires_at=refresh_expires_at,
            session_name=None,
            device_name=None,
            browser_name=None,
            operating_system=None,
            ip_address=self._request_context.ip_address,
            user_agent=self._request_context.user_agent,
            created_by=user.id,
        )

        session.signed_in_at = now
        session.last_activity_at = now

        # ------------------------------------------------------------------
        # Create refresh-token record
        # ------------------------------------------------------------------

        session_token = SessionToken.create(
            id=session_token_id,
            tenant_id=user.tenant_id,
            session_id=session_id,
            token_hash=refresh_token_hash,
            expires_at=refresh_expires_at,
            created_by=user.id,
        )

        session_token.issued_at = now

        # ------------------------------------------------------------------
        # Update user authentication state
        # ------------------------------------------------------------------

        user.last_login_at = now
        user.failed_login_attempts = 0

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._session_repository.save(session)
            self._session_token_repository.save(session_token)
            self._user_repository.save(user)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return AuthenticateUserResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_at=access_expires_at,
            user_id=user.id,
            session_id=session_id,
        )