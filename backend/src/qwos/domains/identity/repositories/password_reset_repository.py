"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Password Reset Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.identity.models.password_reset import PasswordReset


class PasswordResetRepository(Protocol):
    """
    Contract for PasswordReset persistence.
    """

    # ------------------------------------------------------------------
    # Base Operations
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        reset_id: str,
    ) -> PasswordReset | None:
        """
        Retrieve a password reset request by identifier.
        """
        ...

    def save(
        self,
        password_reset: PasswordReset,
    ) -> None:
        """
        Persist a password reset request.
        """
        ...

    # ------------------------------------------------------------------
    # Token Queries
    # ------------------------------------------------------------------

    def get_by_token_hash(
        self,
        token_hash: str,
    ) -> PasswordReset | None:
        """
        Retrieve a password reset request by its secure token hash.
        """
        ...

    def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> PasswordReset | None:
        """
        Retrieve a pending, non-expired password reset request.
        """
        ...

    # ------------------------------------------------------------------
    # User Queries
    # ------------------------------------------------------------------

    def list_by_user_id(
        self,
        user_id: str,
    ) -> list[PasswordReset]:
        """
        Retrieve password reset requests belonging to a user.
        """
        ...
