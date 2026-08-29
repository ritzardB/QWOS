"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Identity Module

File:
    sqlalchemy_user_profile_repository.py

Description:
    SQLAlchemy implementation of the UserProfileRepository contract.

Responsibilities:
    - Persist UserProfile aggregates
    - Execute UserProfile queries
    - No business logic
    - No transaction management

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.identity.models.user_profile import UserProfile
from qwos.domains.identity.repositories.user_profile_repository import (
    UserProfileRepository,
)


class SQLAlchemyUserProfileRepository(
    BaseRepository[UserProfile],
    UserProfileRepository,
):
    """
    SQLAlchemy implementation of UserProfileRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=UserProfile,
        )

    # ------------------------------------------------------------------
    # User Profile Queries
    # ------------------------------------------------------------------

    def get_by_user_id(
        self,
        user_id: str,
    ) -> UserProfile | None:
        """
        Retrieve a user profile by user identifier.
        """
        return self.first_by(
            user_id=user_id,
        )
