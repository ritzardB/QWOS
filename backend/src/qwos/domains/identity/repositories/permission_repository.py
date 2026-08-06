"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    permission_repository.py

Description:
    Repository contract for the Permission aggregate.

Responsibilities:
    - Define permission persistence operations.
    - Remain independent of persistence technology.
    - Serve as the abstraction used by application use cases.

Notes:
    This contract belongs to the Domain layer. Implementations reside in the
    Infrastructure layer (e.g. SQLAlchemyPermissionRepository).

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from abc import ABC, abstractmethod
from qwos.domains.identity.models.permission import Permission


class PermissionRepository(Protocol):
    """
    Contract for Permission persistence.

    The Domain defines WHAT operations are required.
    Infrastructure defines HOW they are implemented.
    """

    def get_by_id(
        self,
        permission_id: str,
    ) -> Permission | None:
        """
        Retrieve a permission by its unique identifier.
        """
        ...

    def get_by_name(
        self,
        name: str,
    ) -> Permission | None:
        """
        Retrieve a permission by name.

        Name comparison should be case-insensitive.
        """
        ...

    def get_by_code(
        self,
        code: str,
    ) -> Permission | None:
        """
        Retrieve a permission by its unique code.
        """
        ...

    def list_by_module(
        self,
        module: str,
    ) -> list[Permission]:
        """
        Retrieve all permissions belonging to a module.

        Module comparison should be case-insensitive.
        """
        ...

    def exists_by_code(
        self,
        code: str,
    ) -> bool:
        """
        Determine whether a permission code already exists.
        """
        ...

    def save(
        self,
        permission: Permission,
    ) -> None:
        """
        Persist a Permission aggregate.

        Implementations may insert or update the aggregate
        as appropriate.
        """
        ...
