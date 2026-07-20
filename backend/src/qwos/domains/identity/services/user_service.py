"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    user_service.py

Description:
    Service responsible for managing the lifecycle of User entities.

    Business logic related to authentication, authorization, and user profiles
    is intentionally delegated to their respective services.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.core.services.base_service import BaseService
from qwos.domains.identity.models.user import User
from qwos.domains.identity.repositories.user_repository import UserRepository


class UserService(BaseService):
    """
    Business service for managing users.
    """

    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        super().__init__()

        self._repository = repository

    # -------------------------------------------------------------------------
    # Commands
    # -------------------------------------------------------------------------

    async def create(self, user: User) -> User:
        """
        Create a new user.
        """
        raise NotImplementedError()

    async def update(self, user: User) -> User:
        """
        Update an existing user.
        """
        raise NotImplementedError()

    async def activate(self, user_id: str) -> None:
        """
        Activate a user account.
        """
        raise NotImplementedError()

    async def deactivate(self, user_id: str) -> None:
        """
        Deactivate a user account.
        """
        raise NotImplementedError()

    async def suspend(self, user_id: str) -> None:
        """
        Suspend a user account.
        """
        raise NotImplementedError()

    async def delete(self, user_id: str) -> None:
        """
        Delete (or soft delete) a user.
        """
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    # Queries
    # -------------------------------------------------------------------------

    async def get(self, user_id: str) -> User | None:
        """
        Retrieve a user by identifier.
        """
        raise NotImplementedError()

    async def list(self) -> list[User]:
        """
        Retrieve all users.
        """
        raise NotImplementedError()
