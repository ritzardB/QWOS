"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    request_password_reset_use_case.py

Description:
    Initiates a password reset request.

Responsibilities:
    - Locate the user by email
    - Generate a secure reset token
    - Hash the token before persistence
    - Create a password reset request
    - Persist the request atomically

Security:
    - Raw reset tokens are never persisted
    - Unknown email addresses do not produce a distinct response
===============================================================================
"""

from __future__ import annotations

from datetime import timedelta

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.ports.secure_token_generator import (
    SecureTokenGenerator,
)
from qwos.application.common.ports.token_hasher import TokenHasher
from qwos.application.identity.commands.request_password_reset_command import (
    RequestPasswordResetCommand,
)
from qwos.application.identity.responses.request_password_reset_response import (
    RequestPasswordResetResponse,
)
from qwos.domains.identity.models.password_reset import PasswordReset
from qwos.domains.identity.repositories.password_reset_repository import (
    PasswordResetRepository,
)
from qwos.domains.identity.repositories.user_repository import UserRepository


class RequestPasswordResetUseCase:
    """
    Use case for initiating a password reset.
    """

    RESET_TOKEN_LIFETIME = timedelta(minutes=30)

    def __init__(
        self,
        *,
        user_repository: UserRepository,
        password_reset_repository: PasswordResetRepository,
        id_generator: IdGenerator,
        secure_token_generator: SecureTokenGenerator,
        token_hasher: TokenHasher,
        clock: Clock,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._user_repository = user_repository
        self._password_reset_repository = password_reset_repository
        self._id_generator = id_generator
        self._secure_token_generator = secure_token_generator
        self._token_hasher = token_hasher
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: RequestPasswordResetCommand,
    ) -> RequestPasswordResetResponse:
        """
        Initiate a password reset request.
        """

        email = command.email.strip().lower()

        user = self._user_repository.get_by_email(email)

        # Do not reveal whether the email address exists.
        if user is None:
            return RequestPasswordResetResponse(
                success=True,
                message=(
                    "If an account exists for this email address, "
                    "a password reset request has been created."
                ),
            )

        # ------------------------------------------------------------------
        # Tenant isolation
        # ------------------------------------------------------------------

        if user.tenant_id != self._request_context.tenant_id:
            return RequestPasswordResetResponse(
                success=True,
                message=(
                    "If an account exists for this email address, "
                    "a password reset request has been created."
                ),
            )

        # ------------------------------------------------------------------
        # Generate secure reset token
        # ------------------------------------------------------------------

        reset_token = self._secure_token_generator.generate()

        reset_token_hash = self._token_hasher.hash(
            reset_token,
        )

        # ------------------------------------------------------------------
        # Time
        # ------------------------------------------------------------------

        requested_at = self._clock.now()
        expires_at = requested_at + self.RESET_TOKEN_LIFETIME

        # ------------------------------------------------------------------
        # Create password reset request
        # ------------------------------------------------------------------

        password_reset = PasswordReset.create(
            id=self._id_generator.generate(),
            tenant_id=user.tenant_id,
            user_id=user.id,
            reset_token_hash=reset_token_hash,
            requested_at=requested_at,
            expires_at=expires_at,
            request_ip_address=self._request_context.ip_address,
            request_user_agent=self._request_context.user_agent,
            created_by=user.id,
        )

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._password_reset_repository.save(password_reset)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return RequestPasswordResetResponse(
            success=True,
            message=(
                "If an account exists for this email address, "
                "a password reset request has been created."
            ),
        )
