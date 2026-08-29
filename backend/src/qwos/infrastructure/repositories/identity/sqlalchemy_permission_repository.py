"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

File:
    sqlalchemy_permission_repository.py

Description:
    SQLAlchemy implementation of the PermissionRepository contract.

Responsibilities:
    - Permission persistence
    - Permission lookups
    - No business logic
    - No transaction management

Notes:
    Generic persistence functionality is inherited from BaseRepository.
    Business rules belong in application use cases.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.identity.models.permission import Permission
from qwos.domains.identity.repositories.permission_repository import (
    PermissionRepository,
)


class SQLAlchemyPermissionRepository(
    BaseRepository[Permission],
    PermissionRepository,
):
    """
    SQLAlchemy implementation of PermissionRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=Permission,
        )

    def save(self, permission: Permission) -> None:
        self._session.add(permission)

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def get_by_name(
        self,
        name: str,
    ) -> Permission | None:
        """
        Retrieve a permission by name.

        Name comparison is case-insensitive.
        """
        normalized_name = name.strip().lower()

        stmt = select(Permission).where(func.lower(Permission.name) == normalized_name)

        return self._session.scalar(stmt)

    def get_by_code(
        self,
        code: str,
    ) -> Permission | None:
        """
        Retrieve a permission by its unique code.
        """
        normalized_code = code.strip().upper()

        stmt = select(Permission).where(Permission.code == normalized_code)

        return self._session.scalar(stmt)

    def list_by_module(
        self,
        module: str,
    ) -> list[Permission]:
        """
        Retrieve all permissions belonging to a module.
        """
        normalized_module = module.strip().lower()

        stmt = select(Permission).where(func.lower(Permission.module) == normalized_module).order_by(Permission.code)

        return list(self._session.scalars(stmt).all())

    def exists_by_code(
        self,
        code: str,
    ) -> bool:
        """
        Determine whether a permission code already exists.
        """
        return self.get_by_code(code) is not None
