"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Session Token Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.identity.models.session_token import SessionToken


class SessionTokenRepository(Protocol):
    """
    Contract for SessionToken persistence.
    """

    # ------------------------------------------------------------------
    # Base Operations
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        token_id: str,
    ) -> SessionToken | None:
        """
        Retrieve a token by identifier.
        """
        ...

    def save(
        self,
        token: SessionToken,
    ) -> None:
        """
        Persist a session token.
        """
        ...

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
        ...

    def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> SessionToken | None:
        """
        Retrieve a non-revoked token by its secure hash.
        """
        ...

    def list_by_session_id(
        self,
        session_id: str,
    ) -> list[SessionToken]:
        """
        Retrieve tokens belonging to a session.
        """
        ...
