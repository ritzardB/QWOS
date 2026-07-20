"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    permission_service.py

Description:
    Service responsible for managing Permission entities.

    Business logic related to assigning permissions to roles is
    intentionally delegated to the AuthorizationService.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import builtins
from qwos.core.services.base_service import BaseService
from qwos.domains.identity.models.permission import Permission
from qwos.domains.identity.repositories.permission_repository import (
    PermissionRepository,
)


class PermissionService(BaseService):
    """
    Business service for managing permissions.
    """

    def __init__(
        self,
        repository: PermissionRepository,
    ) -> None:
        super().__init__()

        self._repository = repository

    # -------------------------------------------------------------------------
    # Commands
    # -------------------------------------------------------------------------

    async def create(self, permission: Permission) -> Permission:
        """
        Create a new permission.
        """
        raise NotImplementedError()

    async def update(self, permission: Permission) -> Permission:
        """
        Update an existing permission.
        """
        raise NotImplementedError()

    async def enable(self, permission_id: str) -> None:
        """
        Enable a permission.
        """
        raise NotImplementedError()

    async def disable(self, permission_id: str) -> None:
        """
        Disable a permission.
        """
        raise NotImplementedError()

    async def delete(self, permission_id: str) -> None:
        """
        Delete (or soft delete) a permission.
        """
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    # Queries
    # -------------------------------------------------------------------------

    async def get(self, permission_id: str) -> Permission | None:
        """
        Retrieve a permission by identifier.
        """
        raise NotImplementedError()

    async def get_by_code(self, code: str) -> Permission | None:
        """
        Retrieve a permission by its unique code.
        """
        raise NotImplementedError()

    async def get_by_name(self, name: str) -> Permission | None:
        """
        Retrieve a permission by its display name.
        """
        raise NotImplementedError()

    async def list(self, offset: int = 0, limit: int = 100) -> builtins.list[Permission]:
        """
        Retrieve all permissions.
        """
        raise NotImplementedError()

      
