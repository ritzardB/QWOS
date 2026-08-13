"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    user_profile_service.py

Description:
    Service responsible for managing UserProfile entities.

    Business logic related to user accounts, authentication, and authorization
    is intentionally delegated to their respective services.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.core.services.base_service import BaseService
from qwos.domains.identity.models.user_profile import UserProfile
from qwos.domains.identity.repositories.user_profile_repository import (
    UserProfileRepository,
)


class UserProfileService(BaseService):
    """
    Business service for managing user profiles.
    """

    def __init__(
        self,
        repository: UserProfileRepository,
    ) -> None:
        super().__init__()

        self._repository = repository

    # -------------------------------------------------------------------------
    # Commands
    # -------------------------------------------------------------------------

    async def create(self, profile: UserProfile) -> UserProfile:
        """
        Create a new user profile.
        """
        raise NotImplementedError()

    async def update(self, profile: UserProfile) -> UserProfile:
        """
        Update an existing user profile.
        """
        raise NotImplementedError()

    async def delete(self, user_id: str) -> None:
        """
        Delete (or soft delete) a user profile.
        """
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    # Queries
    # -------------------------------------------------------------------------

    async def get(self, user_id: str) -> UserProfile | None:
        """
        Retrieve a user profile by user identifier.
        """
        raise NotImplementedError()
