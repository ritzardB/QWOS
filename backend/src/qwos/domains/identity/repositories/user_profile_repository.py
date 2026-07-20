"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    user_profile_repository.py

Description:
    Repository for UserProfile entities.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.core.database.persistence.base_repository import BaseRepository
from qwos.domains.identity.models.user_profile import UserProfile


class UserProfileRepository(BaseRepository[UserProfile]):
    """
    Repository for managing user profiles.
    """

    model = UserProfile

    async def get_by_user_id(
        self,
        user_id: str,
    ) -> UserProfile | None:
        """
        Retrieve the profile associated with a user.
        """
        return await self.first_by(
            user_id=user_id,
        )

    async def exists_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        """
        Determine whether a profile exists for a user.
        """
        return await self.exists_by(
            user_id=user_id,
        )
