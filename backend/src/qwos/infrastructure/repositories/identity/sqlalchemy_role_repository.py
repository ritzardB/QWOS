"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

File:
    sqlalchemy_role_repository.py

Description:
    SQLAlchemy implementation of the RoleRepository contract.

Responsibilities:
    - Role persistence
    - Role lookups
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
from qwos.domains.identity.models.role import Role
from qwos.domains.identity.repositories.role_repository import RoleRepository


class SQLAlchemyRoleRepository(
    BaseRepository[Role],
    RoleRepository,
):
    """
    SQLAlchemy implementation of RoleRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=Role,
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def get_by_name(
        self,
        name: str,
    ) -> Role | None:
        """
        Retrieve a role by name.

        Name comparison is case-insensitive.
        """
        normalized_name = name.strip().lower()

        stmt = select(Role).where(func.lower(Role.name) == normalized_name)

        return self._session.scalar(stmt)

    def get_by_code(
        self,
        code: str,
    ) -> Role | None:
        """
        Retrieve a role by its unique code.
        """
        normalized_code = code.strip().upper()

        stmt = select(Role).where(Role.code == normalized_code)

        return self._session.scalar(stmt)

    def exists_by_name(
        self,
        name: str,
    ) -> bool:
        """
        Determine whether a role name already exists.
        """
        return self.get_by_name(name) is not None

    def exists_by_code(
        self,
        code: str,
    ) -> bool:
        """
        Determine whether a role code already exists.
        """
        return self.get_by_code(code) is not None
