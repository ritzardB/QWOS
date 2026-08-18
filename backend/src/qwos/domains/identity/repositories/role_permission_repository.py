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

from typing import Protocol

from qwos.domains.identity.models.role_permission import RolePermission


class RolePermissionRepository(Protocol):
    """
    Contract for role-permission persistence.
    """

    def get_by_id(
        self,
        role_permission_id: str,
    ) -> RolePermission | None:
        """
        Retrieve a role-permission assignment by identifier.
        """
        ...

    def list_active_permissions(
        self,
        role_id: str,
    ) -> list[RolePermission]:
        """
        Retrieve enabled, non-deleted role-permission assignments.
        """
        ...

    def exists_assignment(
        self,
        role_id: str,
        permission_id: str,
    ) -> bool:
        """
        Determine whether a role already has a permission assignment.
        """
        ...

    def get_assignment(
        self,
        role_id: str,
        permission_id: str,
    ) -> RolePermission | None:
        """
        Retrieve a specific role-permission assignment.
        """
        ...

    def save(
        self,
        role_permission: RolePermission,
    ) -> None:
        """
        Persist a role-permission assignment.
        """
        ...