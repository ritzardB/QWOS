"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    change_password_use_case.py

Description:
    Changes the password of an authenticated user.

Responsibilities:
    - Identify the authenticated user
    - Enforce tenant isolation
    - Verify the current password
    - Hash the new password
    - Update password security state
    - Persist the change atomically

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.password_hasher import PasswordHasher
from qwos.application.identity.commands.change_password_command import (
    ChangePasswordCommand,
)
from qwos.application.identity.responses.change_password_response import (
    ChangePasswordResponse,
)
from qwos.domains.identity.repositories.user_repository import UserRepository


class ChangePasswordUseCase:
    """
    Use case for changing an authenticated user's password.
    """

    def __init__(
        self,
        *,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        clock: Clock,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: ChangePasswordCommand,
    ) -> ChangePasswordResponse:
        """
        Change the authenticated user's password.
        """

        # ------------------------------------------------------------------
        # Authentication context
        # ------------------------------------------------------------------

        user_id = self._request_context.user_id

        if not user_id:
            raise ValueError("Authentication is required.")

        # ------------------------------------------------------------------
        # Locate user
        # ------------------------------------------------------------------

        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        # ------------------------------------------------------------------
        # Tenant isolation
        # ------------------------------------------------------------------

        if user.tenant_id != self._request_context.tenant_id:
            raise ValueError("User not found.")

        # ------------------------------------------------------------------
        # Existing password
        # ------------------------------------------------------------------

        if not user.password_hash:
            raise ValueError("Password is not configured.")

        # ------------------------------------------------------------------
        # Verify current password
        # ------------------------------------------------------------------

        if not self._password_hasher.verify(
            command.current_password,
            user.password_hash,
        ):
            raise ValueError("Current password is incorrect.")

        # ------------------------------------------------------------------
        # Hash new password
        # ------------------------------------------------------------------

        new_password_hash = self._password_hasher.hash(
            command.new_password,
        )

        now = self._clock.now()

        # ------------------------------------------------------------------
        # Update authentication state
        # ------------------------------------------------------------------

        user.password_hash = new_password_hash
        user.password_changed_at = now

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._user_repository.save(user)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return ChangePasswordResponse(
            success=True,
            message="Password changed successfully.",
        )
