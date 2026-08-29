"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    reset_password_use_case.py

Description:
    Resets a user's password using a valid password-reset token.

Responsibilities:
    - Validate the reset request
    - Hash the supplied reset token
    - Locate the active password reset
    - Enforce tenant isolation
    - Validate token expiration
    - Load the associated user
    - Hash the new password
    - Update password security state
    - Mark the reset request as used
    - Persist all changes atomically

Security:
    - Raw reset tokens are never persisted
    - Reset tokens are single-use
    - Expired and revoked tokens cannot be used
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.password_hasher import PasswordHasher
from qwos.application.common.ports.token_hasher import TokenHasher
from qwos.application.identity.commands.reset_password_command import (
    ResetPasswordCommand,
)
from qwos.application.identity.responses.reset_password_response import (
    ResetPasswordResponse,
)
from qwos.domains.identity.repositories.password_reset_repository import (
    PasswordResetRepository,
)
from qwos.domains.identity.repositories.user_repository import UserRepository


class ResetPasswordUseCase:
    """
    Use case for resetting a user's password.
    """

    def __init__(
        self,
        *,
        user_repository: UserRepository,
        password_reset_repository: PasswordResetRepository,
        password_hasher: PasswordHasher,
        token_hasher: TokenHasher,
        clock: Clock,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._user_repository = user_repository
        self._password_reset_repository = password_reset_repository
        self._password_hasher = password_hasher
        self._token_hasher = token_hasher
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: ResetPasswordCommand,
    ) -> ResetPasswordResponse:
        """
        Reset a user's password.
        """

        # ------------------------------------------------------------------
        # Validate passwords
        # ------------------------------------------------------------------

        if command.new_password != command.confirm_password:
            raise ValueError("Passwords do not match.")

        # ------------------------------------------------------------------
        # Hash reset token
        # ------------------------------------------------------------------

        reset_token_hash = self._token_hasher.hash(
            command.token,
        )

        # ------------------------------------------------------------------
        # Locate active reset request
        # ------------------------------------------------------------------

        password_reset = self._password_reset_repository.get_active_by_token_hash(
            reset_token_hash,
        )

        if password_reset is None:
            raise ValueError("Invalid or expired password reset token.")

        # ------------------------------------------------------------------
        # Tenant isolation
        # ------------------------------------------------------------------

        if password_reset.tenant_id != self._request_context.tenant_id:
            raise ValueError("Invalid or expired password reset token.")

        # ------------------------------------------------------------------
        # Expiration
        # ------------------------------------------------------------------

        now = self._clock.now()

        if password_reset.expires_at <= now:
            password_reset.mark_expired()

            with self._unit_of_work:
                self._password_reset_repository.save(password_reset)
                self._unit_of_work.flush()

            raise ValueError("Invalid or expired password reset token.")

        # ------------------------------------------------------------------
        # Locate user
        # ------------------------------------------------------------------

        user = self._user_repository.get_by_id(
            password_reset.user_id,
        )

        if user is None:
            raise ValueError("Invalid or expired password reset token.")

        # ------------------------------------------------------------------
        # Tenant isolation for user
        # ------------------------------------------------------------------

        if user.tenant_id != password_reset.tenant_id:
            raise ValueError("Invalid or expired password reset token.")

        # ------------------------------------------------------------------
        # Hash new password
        # ------------------------------------------------------------------

        new_password_hash = self._password_hasher.hash(
            command.new_password,
        )

        # ------------------------------------------------------------------
        # Update authentication state
        # ------------------------------------------------------------------

        user.password_hash = new_password_hash
        user.password_changed_at = now

        # ------------------------------------------------------------------
        # Consume reset token
        # ------------------------------------------------------------------

        password_reset.mark_used(
            used_at=now,
        )

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._user_repository.save(user)
            self._password_reset_repository.save(password_reset)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return ResetPasswordResponse(
            success=True,
            message="Password reset successfully.",
        )
