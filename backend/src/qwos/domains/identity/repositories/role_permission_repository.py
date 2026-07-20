"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    role_permission_repository.py

Description:
    Repository for RolePermission entities.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.core.database.persistence.base_repository import BaseRepository
from qwos.domains.identity.models.role_permission import RolePermission


class RolePermissionRepository(BaseRepository[RolePermission]):
    """
    Repository for managing role permission assignments.
    """

    model = RolePermission

    async def list_active_permissions(
        self,
        role_id: str,
    ) -> list[RolePermission]:
        """
        Retrieve all active permissions assigned to a role.
        """
        return await self.list_by(
            role_id=role_id,
            is_enabled=True,
        )

    async def exists_assignment(
        self,
        role_id: str,
        permission_id: str,
    ) -> bool:
        """
        Check whether a permission assignment already exists.
        """
        return await self.exists_by(
            role_id=role_id,
            permission_id=permission_id,
        )

    async def get_assignment(
        self,
        role_id: str,
        permission_id: str,
    ) -> RolePermission | None:
        """
        Retrieve a specific role-permission assignment.
        """
        return await self.first_by(
            role_id=role_id,
            permission_id=permission_id,
        )
