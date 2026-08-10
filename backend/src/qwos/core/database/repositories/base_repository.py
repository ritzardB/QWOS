"""
QWOS Base Repository

Provides generic persistence operations for all aggregate roots.

Design Principles:
- Generic and type-safe
- SQLAlchemy 2.x
- No business logic
- No commit() or rollback()
- Service layer owns transactions
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from qwos.core.database.entity_base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    """
    Generic repository for aggregate roots.

    This class contains only generic persistence operations.
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
    # Persistence
    # ------------------------------------------------------------------

    def save(self, 
             entity: T) -> None:
        self._session.add(entity)
        
        """
        Persist an entity.

        Adds new entities to the current Unit of Work.
        Existing tracked entities are automatically synchronized by SQLAlchemy.

        Does not commit.
        """
        return None

    # ------------------------------------------------------------------
    # Generic Queries
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        entity_id: str,
    ) -> T | None:
        """
        Retrieve an entity by its unique identifier.
        """
        stmt = select(self._model).where(self._model.id == entity_id)

        return self._session.scalar(stmt)

    def exists(
        self,
        entity_id: str,
    ) -> bool:
        """
        Determine whether an entity exists.
        """
        stmt = (
            select(func.count())
            .select_from(self._model)
            .where(self._model.id == entity_id)
        )

        count = self._session.scalar(stmt)

        return (count or 0) > 0

    def count(self) -> int:
        """
        Return the total number of entities.
        """
        stmt = select(func.count()).select_from(self._model)

        count = self._session.scalar(stmt)

        return count or 0

    def find_all(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[T]:
        """
        Retrieve entities with optional pagination.
        """
        stmt = select(self._model).offset(offset).limit(limit)

        return list(self._session.scalars(stmt).all())

    # ------------------------------------------------------------------
    # Query Helpers
    # ------------------------------------------------------------------

    def first_by(
        self,
        **kwargs: Any,
    ) -> T | None:
        """
        Retrieve the first entity matching the given criteria.
        """
        stmt = select(self._model).filter_by(**kwargs).limit(1)

        return self._session.scalar(stmt)

    def list_by(
        self,
        **kwargs: Any,
    ) -> list[T]:
        """
        Retrieve all entities matching the given criteria.
        """
        stmt = select(self._model).filter_by(**kwargs)

        return list(self._session.scalars(stmt).all())

    def exists_by(
        self,
        **kwargs: Any,
    ) -> bool:
        """
        Determine whether an entity exists matching the given criteria.
        """
        stmt = select(func.count()).select_from(self._model).filter_by(**kwargs)

        count = self._session.scalar(stmt)

        return (count or 0) > 0

    def exists_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        """
        Determine whether a profile exists for the given user.
        """
        return self.exists_by(user_id=user_id)

    # ------------------------------------------------------------------
    # Session Helpers
    # ------------------------------------------------------------------

    def flush(self) -> None:
        """
        Flush pending changes.

        Does not commit.
        """
        self._session.flush()

    def refresh(
        self,
        entity: T,
    ) -> None:
        """
        Refresh an entity from the database.
        """
        self._session.refresh(entity)

    def detach(
        self,
        entity: T,
    ) -> None:
        """
        Detach an entity from the current session.
        """
        self._session.expunge(entity)

