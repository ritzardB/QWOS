"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    user_role_repository.py

Description:
    Repository contract for the UserRole aggregate.

Responsibilities:
    - Define user role assignment persistence operations.
    - Remain independent of persistence technology.
    - Serve as the abstraction used by application use cases.

Notes:
    This contract belongs to the Domain layer. Implementations reside in the
    Infrastructure layer (e.g. SQLAlchemyUserRoleRepository).

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.identity.models.user_role import UserRole


class UserRoleRepository(Protocol):
    """
    Contract for UserRole persistence.

    The Domain defines WHAT operations are required.
    Infrastructure defines HOW they are implemented.
    """

    def get_by_id(
        self,
        user_role_id: str,
    ) -> UserRole | None:
        """
        Retrieve a user role assignment by its unique identifier.
        """
        ...

    def get_primary_role(
        self,
        user_id: str,
    ) -> UserRole | None:
        """
        Retrieve the user's primary role assignment.
        """
        ...

    def list_active_roles(
        self,
        user_id: str,
    ) -> list[UserRole]:
        """
        Retrieve all active role assignments for a user.
        """
        ...

    def exists_assignment(
        self,
        user_id: str,
        role_id: str,
    ) -> bool:
        """
        Determine whether a role assignment already exists.
        """
        ...

    def save(
        self,
        user_role: UserRole,
    ) -> None:
        """
        Persist a UserRole aggregate.

        Implementations may insert or update the aggregate
        as appropriate.
        """
        ...
