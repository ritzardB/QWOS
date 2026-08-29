"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Identity Module

File:
    sqlalchemy_session_token_repository.py

Description:
    SQLAlchemy implementation of the SessionTokenRepository contract.

Responsibilities:
    - Session token persistence
    - Session token queries
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
from qwos.domains.identity.models.session_token import SessionToken
from qwos.domains.identity.repositories.session_token_repository import (
    SessionTokenRepository,
)


class SQLAlchemySessionTokenRepository(
    BaseRepository[SessionToken],
    SessionTokenRepository,
):
    """
    SQLAlchemy implementation of SessionTokenRepository.
    """

    def __init__(
        self,
        session: SQLAlchemySession,
    ) -> None:
        super().__init__(
            session=session,
            model=SessionToken,
        )

    # ------------------------------------------------------------------
    # Token Queries
    # ------------------------------------------------------------------

    def get_by_token_hash(
        self,
        token_hash: str,
    ) -> SessionToken | None:
        """
        Retrieve a token by its secure hash.
        """

        return self.first_by(
            token_hash=token_hash,
        )

    def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> SessionToken | None:
        """
        Retrieve a non-revoked token by its secure hash.
        """

        stmt = select(SessionToken).where(
            SessionToken.token_hash == token_hash,
            SessionToken.revoked_at.is_(None),
        )

        return self._session.scalar(stmt)

    def list_by_session_id(
        self,
        session_id: str,
    ) -> list[SessionToken]:
        """
        Retrieve all tokens belonging to a session.
        """

        stmt = select(SessionToken).where(SessionToken.session_id == session_id).order_by(SessionToken.issued_at.desc())

        return list(self._session.scalars(stmt).all())
