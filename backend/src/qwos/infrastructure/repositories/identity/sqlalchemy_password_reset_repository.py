"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Identity Module

File:
    sqlalchemy_password_reset_repository.py

Description:
    SQLAlchemy implementation of the PasswordResetRepository contract.

Responsibilities:
    - Password reset persistence
    - Password reset queries
    - No business logic
    - No transaction management

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session as SQLAlchemySession

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.identity.enums.password_reset_status import (
    PasswordResetStatus,
)
from qwos.domains.identity.models.password_reset import PasswordReset
from qwos.domains.identity.repositories.password_reset_repository import (
    PasswordResetRepository,
)


class SQLAlchemyPasswordResetRepository(
    BaseRepository[PasswordReset],
    PasswordResetRepository,
):
    """
    SQLAlchemy implementation of PasswordResetRepository.
    """

    def __init__(
        self,
        session: SQLAlchemySession,
    ) -> None:
        super().__init__(
            session=session,
            model=PasswordReset,
        )

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

        return self.first_by(
            reset_token_hash=token_hash,
        )

    def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> PasswordReset | None:
        """
        Retrieve a pending, non-revoked password reset request.

        Expiration is evaluated by the application use case because the
        repository does not own the application's Clock dependency.
        """

        stmt = select(PasswordReset).where(
            PasswordReset.reset_token_hash == token_hash,
            PasswordReset.password_reset_status == PasswordResetStatus.PENDING,
            PasswordReset.revoked_at.is_(None),
        )

        return self._session.scalar(stmt)

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

        stmt = select(PasswordReset).where(PasswordReset.user_id == user_id).order_by(PasswordReset.requested_at.desc())

        return list(self._session.scalars(stmt).all())
