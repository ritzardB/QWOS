"""
QWOS Base Repository

Provides generic CRUD operations for all aggregate roots.

Design Principles:
- Generic and type-safe
- SQLAlchemy 2.x
- No business logic
- No commit() or rollback()
- Service layer owns transactions
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar
import builtins
 
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from qwos.core.database.entity_base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    """
    Generic repository for aggregate roots.

    This class should never contain business rules.
    Domain-specific queries belong in derived repositories.
    """

    def __init__(
        self,
        session: Session,
        model: type[T],
    ) -> None:
        self._session = session
        self._model = model

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create(self, entity: T) -> T:
        """
        Add a new entity to the current unit of work.

        Does not commit.
        """
        self._session.add(entity)
        return entity

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, entity: T) -> T:
        """
        Merge detached entity into current session.

        Does not commit.
        """
        return self._session.merge(entity)

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete(self, entity: T) -> None:
        """
        Delete entity.

        Does not commit.
        """
        self._session.delete(entity)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_by_id(self, entity_id: str) -> T | None:
        """
        Retrieve entity by primary key.
        """
        stmt = select(self._model).where(self._model.id == entity_id)

        return self._session.scalar(stmt)

    def exists(self, entity_id: str) -> bool:
        """
        Check whether entity exists.
        """
        stmt = (
            select(func.count())
            .select_from(self._model)
            .where(self._model.id == entity_id)
        )

        count = self._session.scalar(stmt)

        if count is None:
            return False

        return (count or 0) > 0

    def count(self) -> int:
        """
        Return total entity count.
        """
        stmt = select(func.count()).select_from(self._model)

        count = self._session.scalar(stmt)

        if count is None:
            return 0

        return count

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[T]:
        """
        Retrieve entities.

        Pagination support included.
        """
        stmt = select(self._model).offset(offset).limit(limit)

        return list(self._session.scalars(stmt).all())

    # ------------------------------------------------------------------
    # Session Helpers
    # ------------------------------------------------------------------

    def flush(self) -> None:
        """
        Flush pending changes.

        Does not commit.
        """
        self._session.flush()

    def refresh(self, entity: T) -> None:
        """
        Refresh entity from database.
        """
        self._session.refresh(entity)

    def detach(self, entity: T) -> None:
        """
        Remove entity from current session.
        """
        self._session.expunge(entity)


    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    async def first_by(self, **kwargs: Any) -> T | None:
        """
        Retrieve the first entity matching the given keyword criteria.
        """
        # Note: If your app uses async drivers, change self._session.scalar to await self._session.scalar
        stmt = select(self._model).filter_by(**kwargs).limit(1)
        return self._session.scalar(stmt)

    async def list_by(self, **kwargs: Any) -> builtins.list[T]:
        """
        Retrieve all entities matching the given keyword criteria.
        """
        stmt = select(self._model).filter_by(**kwargs)
        return list(self._session.scalars(stmt).all())

    async def exists_by(self, **kwargs: Any) -> bool:
        """
        Check whether an entity exists matching the given keyword criteria.
        """
        stmt = (
            select(func.count())
            .select_from(self._model)
            .filter_by(**kwargs)
        )
        count = self._session.scalar(stmt)
        return (count or 0) > 0
