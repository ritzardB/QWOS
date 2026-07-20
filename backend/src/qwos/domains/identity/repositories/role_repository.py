"""
QWOS Role Repository

Repository implementation for the Role aggregate.

Responsibilities:
- Role persistence
- Role lookups
- No business logic
- No transaction management
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from qwos.core.database.persistence.base_repository import BaseRepository
from qwos.domains.identity.models.role import Role


class RoleRepository(BaseRepository[Role]):
    """
    Repository for Role aggregate.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(
            session=session,
            model=Role,
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def get_by_name(self, name: str) -> Role | None:
        """
        Retrieve a role by name.

        Comparison is case-insensitive.
        """
        stmt = select(Role).where(func.lower(Role.name) == name.lower())

        return self._session.scalar(stmt)

    def exists_by_name(self, name: str) -> bool:
        """
        Determine whether a role exists.
        """
        return self.get_by_name(name) is not None

    # ------------------------------------------------------------------
    # System Roles
    # ------------------------------------------------------------------

    def get_system_roles(self) -> list[Role]:
        """
        Retrieve all system-defined roles.
        """
        stmt = select(Role).where(Role.is_system.is_(True)).order_by(Role.name)

        return list(self._session.scalars(stmt))
