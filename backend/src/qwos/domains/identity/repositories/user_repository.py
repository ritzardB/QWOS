"""
QWOS User Repository

Repository implementation for the User aggregate.

Responsibilities:
- User-specific persistence operations
- Identity lookups
- No business logic
- No transaction management

All generic CRUD functionality is inherited from BaseRepository.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from qwos.core.database.persistence.base_repository import BaseRepository
from qwos.domains.identity.models.user import User


class UserRepository(BaseRepository[User]):
    """
    Repository for User aggregate.

    Inherits generic CRUD operations from BaseRepository and
    provides user-specific queries.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(
            session=session,
            model=User,
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email address.

        Email comparison is case-insensitive.
        """
        stmt = select(User).where(func.lower(User.email) == email.lower())

        return self._session.scalar(stmt)

    def exists_by_email(self, email: str) -> bool:
        """
        Determine whether a user exists with the specified email.
        """
        return self.get_by_email(email) is not None

    # ------------------------------------------------------------------
    # External Identity
    # ------------------------------------------------------------------

    def get_by_external_id(
        self,
        provider: str,
        external_id: str,
    ) -> User | None:
        """
        Retrieve a user using an external identity provider.
        """
        stmt = (
            select(User)
            .where(User.authentication_provider == provider)
            .where(User.external_id == external_id)
        )

        return self._session.scalar(stmt)

    # ------------------------------------------------------------------
    # Username
    # ------------------------------------------------------------------

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Retrieve a user by username.
        """
        stmt = select(User).where(func.lower(User.username) == username.lower())

        return self._session.scalar(stmt)

    def exists_by_username(
        self,
        username: str,
    ) -> bool:
        """
        Determine whether a username already exists.
        """
        return self.get_by_username(username) is not None
