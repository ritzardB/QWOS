"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

File:
    sqlalchemy_user_role_repository.py

Description:
    SQLAlchemy implementation of the UserRoleRepository contract.

Responsibilities:
    - User role assignment persistence
    - Primary role lookup
    - Active role queries
    - Assignment existence checks
    - No business logic
    - No transaction management

Notes:
    Generic persistence functionality is inherited from BaseRepository.
    Business rules belong in application use cases.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.identity.models.user_role import UserRole
from qwos.domains.identity.repositories.user_role_repository import (
    UserRoleRepository,
)


class SQLAlchemyUserRoleRepository(
    BaseRepository[UserRole],
    UserRoleRepository,
):
    """
    SQLAlchemy implementation of UserRoleRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=UserRole,
        )

    # ------------------------------------------------------------------
    # Role Assignment Queries
    # ------------------------------------------------------------------

    def get_primary_role(
        self,
        user_id: str,
    ) -> UserRole | None:
        """
        Retrieve the user's primary active role.
        """
        stmt = (
            select(UserRole)
            .where(
                UserRole.user_id == user_id,
                UserRole.is_primary.is_(True),
                UserRole.deleted_at.is_(None),
            )
            .limit(1)
        )

        return self._session.scalar(stmt)

    def list_active_roles(
        self,
        user_id: str,
    ) -> list[UserRole]:
        """
        Retrieve all active role assignments for a user.
        """
        stmt = (
            select(UserRole)
            .where(
                UserRole.user_id == user_id,
                UserRole.deleted_at.is_(None),
            )
            .order_by(
                UserRole.is_primary.desc(),
                UserRole.created_at.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all()
        )

    def exists_assignment(
        self,
        user_id: str,
        role_id: str,
    ) -> bool:
        """
        Determine whether an active role assignment exists.
        """
        stmt = (
            select(UserRole.id)
            .where(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
                UserRole.deleted_at.is_(None),
            )
            .limit(1)
        )

        return self._session.scalar(stmt) is not None
