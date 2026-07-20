"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    user_role_repository.py

Description:
    Repository for UserRole entities.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.core.database.persistence.base_repository import BaseRepository
from qwos.domains.identity.models.user_role import UserRole
from typing import Any, Generic, TypeVar


class UserRoleRepository(BaseRepository[UserRole]):
    """
    Repository for managing user role assignments.
    """

    model = UserRole

    async def get_primary_role(self, user_id: str) -> UserRole | None:
        """
        Retrieve the user's primary role.
        """
        return await self.first_by(
            user_id=user_id,
            is_primary=True,
            is_enabled=True,
        )

    async def list_active_roles(self, user_id: str) -> list[UserRole]:
        """
        Retrieve all active role assignments for a user.
        """
        return await self.list_by(
            user_id=user_id,
            is_enabled=True,
        )

    async def exists_assignment(
        self,
        user_id: str,
        role_id: str,
    ) -> bool:
        """
        Check whether a role assignment already exists.
        """
        return await self.exists_by(
            user_id=user_id,
            role_id=role_id,
        )
