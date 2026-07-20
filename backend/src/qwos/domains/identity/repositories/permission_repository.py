"""
QWOS Permission Repository

Repository implementation for the Permission aggregate.

Responsibilities:
- Permission persistence
- Permission lookups
- No business logic
- No transaction management

All generic CRUD functionality is inherited from BaseRepository.
"""

from __future__ import annotations

import builtins # Prevents name-clashing errors if 'list' is shadowed
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from qwos.core.database.persistence.base_repository import BaseRepository
from qwos.domains.identity.models.permission import Permission


class PermissionRepository(BaseRepository[Permission]):
    """
    Repository for Permission aggregate.

    Inherits generic CRUD operations from BaseRepository and
    previews permission-specific queries.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(
            session=session,
            model=Permission,
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def get_by_name(self, name: str) -> Permission | None:
        """
        Retrieve a permission by name.

        Comparison is case-insensitive.
        """
        stmt = select(Permission).where(func.lower(Permission.name) == name.lower())

        return self._session.scalar(stmt)

    def exists_by_code(self, code: str) -> bool:
        """
        Determine whether a permission code already exists.
        """
        # Fixes Line 45: Call the base repository 'first_by' helper instead of the missing method
        return self._session.scalar(select(Permission).where(Permission.code == code)) is not None

    # ------------------------------------------------------------------
    # Module
    # ------------------------------------------------------------------

    def list_by_module(
        self,
        module: str,
    ) -> builtins.list[Permission]:
        """
        Retrieve all permissions for a given module.

        Results are ordered by permission name.
        """
        stmt = select(Permission).where(func.lower(Permission.module) == module.lower())

        # Fixes Line 64: Wrap execution results with .all() inside a builtins.list call
        return builtins.list(self._session.scalars(stmt).all())

