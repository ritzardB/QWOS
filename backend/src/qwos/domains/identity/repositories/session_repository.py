"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Session Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.identity.models.session import Session


class SessionRepository(Protocol):
    """
    Contract for Session persistence.
    """

    # ------------------------------------------------------------------
    # Base Operations
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        session_id: str,
    ) -> Session | None:
        """
        Retrieve a session by identifier.
        """
        ...

    def save(
        self,
        session: Session,
    ) -> None:
        """
        Persist a session.
        """
        ...

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
        ...

    def list_by_user_id(
        self,
        user_id: str,
    ) -> list[Session]:
        """
        Retrieve sessions belonging to a user.
        """
        ...

    def list_active_by_user_id(
        self,
        user_id: str,
    ) -> list[Session]:
        """
        Retrieve active sessions belonging to a user.
        """
        ...
