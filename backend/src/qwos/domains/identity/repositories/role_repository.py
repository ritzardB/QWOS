"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Repository Contract

Role Repository
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.identity.models.role import Role


class RoleRepository(Protocol):
    """
    Contract for Role persistence.
    """

    # ------------------------------------------------------------------
    # Generic Persistence
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        entity_id: str,
    ) -> Role | None:
        """
        Retrieve a role by its identifier.
        """
        ...

    def save(
        self,
        entity: Role,
    ) -> None:
        """
        Persist a role.
        """
        ...

    # ------------------------------------------------------------------
    # Role Queries
    # ------------------------------------------------------------------

    def get_by_name(
        self,
        name: str,
    ) -> Role | None:
        """
        Retrieve a role by name.
        """
        ...

    def get_by_code(
        self,
        code: str,
    ) -> Role | None:
        """
        Retrieve a role by code.
        """
        ...

    def exists_by_name(
        self,
        name: str,
    ) -> bool:
        """
        Determine whether a role name exists.
        """
        ...

    def exists_by_code(
        self,
        code: str,
    ) -> bool:
        """
        Determine whether a role code exists.
        """
        ...