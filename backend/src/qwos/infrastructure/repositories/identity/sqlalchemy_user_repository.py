"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

File:
    sqlalchemy_user_repository.py

Description:
    SQLAlchemy implementation of the UserRepository contract.

Responsibilities:
    - User persistence
    - User lookups
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
from qwos.domains.identity.models.user import User
from qwos.domains.identity.repositories.user_repository import UserRepository


class SQLAlchemyUserRepository(
    BaseRepository[User],
    UserRepository,
):
    """
    SQLAlchemy implementation of UserRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=User,
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email address.

        Email comparison is case-insensitive.
        """
        stmt = select(User).where(func.lower(User.email) == email.strip().lower())

        return self._session.scalar(stmt)

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Retrieve a user by username.

        Username comparison is case-insensitive.
        """
        stmt = select(User).where(func.lower(User.username) == username.strip().lower())

        return self._session.scalar(stmt)

    def exists_by_email(
        self,
        email: str,
    ) -> bool:
        """
        Determine whether an email already exists.
        """
        return self.get_by_email(email) is not None

    def exists_by_username(
        self,
        username: str,
    ) -> bool:
        """
        Determine whether a username already exists.
        """
        return self.get_by_username(username) is not None
