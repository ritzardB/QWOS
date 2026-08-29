"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

User Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.identity.models.user import User


class UserRepository(Protocol):
    """
    Contract for User persistence.
    """

    # ------------------------------------------------------------------
    # Base Repository Operations
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        user_id: str,
    ) -> User | None:
        """
        Retrieve a user by its identifier.
        """
        ...

    def save(
        self,
        user: User,
    ) -> None:
        """
        Persist a user.
        """
        ...

    # ------------------------------------------------------------------
    # User-specific Queries
    # ------------------------------------------------------------------

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """
        ...

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Retrieve a user by username.
        """
        ...

    def exists_by_email(
        self,
        email: str,
    ) -> bool:
        """
        Determine whether an email already exists.
        """
        ...

    def exists_by_username(
        self,
        username: str,
    ) -> bool:
        """
        Determine whether a username already exists.
        """
        ...
