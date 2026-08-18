"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Identity Module

File:
    sqlalchemy_role_permission_repository.py

Description:
    SQLAlchemy implementation of RolePermissionRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.identity.models.role_permission import RolePermission
from qwos.domains.identity.repositories.role_permission_repository import (
    RolePermissionRepository,
)


class SQLAlchemyRolePermissionRepository(
    BaseRepository[RolePermission],
    RolePermissionRepository,
):
    """
    SQLAlchemy implementation of RolePermissionRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=RolePermission,
        )

    def list_active_permissions(
        self,
        role_id: str,
    ) -> list[RolePermission]:
        """
        Retrieve currently effective role-permission assignments.
        """

        now = datetime.now(timezone.utc)

        stmt = (
            select(RolePermission)
            .where(
                RolePermission.role_id == role_id,
                RolePermission.is_enabled.is_(True),
                RolePermission.deleted_at.is_(None),
                (
                    RolePermission.effective_from.is_(None)
                    | (
                        RolePermission.effective_from
                        <= now
                    )
                ),
                (
                    RolePermission.effective_until.is_(None)
                    | (
                        RolePermission.effective_until
                        >= now
                    )
                ),
            )
            .order_by(RolePermission.created_at.asc())
        )

        return list(
            self._session.scalars(stmt).all()
        )

    def exists_assignment(
        self,
        role_id: str,
        permission_id: str,
    ) -> bool:
        """
        Determine whether an active assignment exists.
        """

        stmt = (
            select(RolePermission.id)
            .where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
                RolePermission.deleted_at.is_(None),
            )
            .limit(1)
        )

        return self._session.scalar(stmt) is not None

    def get_assignment(
        self,
        role_id: str,
        permission_id: str,
    ) -> RolePermission | None:
        """
        Retrieve a role-permission assignment.
        """

        stmt = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
            RolePermission.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def save(
        self,
        role_permission: RolePermission,
    ) -> None:
        """
        Persist a role-permission assignment.
        """

        self._session.add(role_permission)