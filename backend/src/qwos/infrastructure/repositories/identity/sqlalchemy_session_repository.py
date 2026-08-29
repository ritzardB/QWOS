"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Identity Module

File:
    sqlalchemy_session_repository.py

Description:
    SQLAlchemy implementation of the SessionRepository contract.

Responsibilities:
    - Session persistence
    - Session queries
    - No business logic
    - No transaction management

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session as SQLAlchemySession

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.identity.models.session import Session
from qwos.domains.identity.repositories.session_repository import (
    SessionRepository,
)


class SQLAlchemySessionRepository(
    BaseRepository[Session],
    SessionRepository,
):
    """
    SQLAlchemy implementation of SessionRepository.
    """

    def __init__(
        self,
        session: SQLAlchemySession,
    ) -> None:
        super().__init__(
            session=session,
            model=Session,
        )

    # ------------------------------------------------------------------
    # Session Queries
    # ------------------------------------------------------------------

    def get_active_by_id(
        self,
        session_id: str,
    ) -> Session | None:
        """
        Retrieve an active session by identifier.
        """

        stmt = select(Session).where(
            Session.id == session_id,
            Session.is_active.is_(True),
            Session.signed_out_at.is_(None),
        )

        return self._session.scalar(stmt)

    def list_by_user_id(
        self,
        user_id: str,
    ) -> list[Session]:
        """
        Retrieve all sessions belonging to a user.
        """

        stmt = select(Session).where(Session.user_id == user_id).order_by(Session.signed_in_at.desc())

        return list(self._session.scalars(stmt).all())

    def list_active_by_user_id(
        self,
        user_id: str,
    ) -> list[Session]:
        """
        Retrieve active sessions belonging to a user.
        """

        stmt = (
            select(Session)
            .where(
                Session.user_id == user_id,
                Session.is_active.is_(True),
                Session.signed_out_at.is_(None),
            )
            .order_by(Session.signed_in_at.desc())
        )

        return list(self._session.scalars(stmt).all())
