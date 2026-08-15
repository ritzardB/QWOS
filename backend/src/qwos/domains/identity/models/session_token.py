"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    session_token.py

Description:
    SQLAlchemy model representing a session refresh token.

    Raw refresh tokens must never be persisted. Only their secure hash is
    stored in this entity.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class SessionToken(TenantEntity):
    """
    Represents a refresh token associated with an authenticated session.

    The persisted token_hash must be a secure hash of the raw refresh token.
    """

    __tablename__ = "session_tokens"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("token_type", "refresh")
        super().__init__(**kwargs)

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        session_id: str,
        token_hash: str,
        expires_at: datetime,
        token_type: str = "refresh",
        created_by: str | None = None,
        rotated_from_token_id: str | None = None,
    ) -> "SessionToken":
        """
        Create a new session token.

        token_hash must contain a secure hash of the raw refresh token.
        The raw token itself must never be supplied for persistence.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            session_id=session_id,
            token_hash=token_hash,
            token_type=token_type,
            expires_at=expires_at,
            rotated_from_token_id=rotated_from_token_id,
            created_by=created_by,
            updated_by=created_by,
        )

    # ------------------------------------------------------------------
    # Session Ownership
    # ------------------------------------------------------------------

    session_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Token
    # ------------------------------------------------------------------

    token_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    token_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="refresh",
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    revoked_by: Mapped[str | None] = mapped_column(
        String(26),
        nullable=True,
    )

    revocation_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Rotation
    # ------------------------------------------------------------------

    rotated_from_token_id: Mapped[str | None] = mapped_column(
        String(26),
        ForeignKey(
            "session_tokens.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Lifecycle Operations
    # ------------------------------------------------------------------

    def mark_used(
        self,
        *,
        used_at: datetime,
    ) -> None:
        """
        Record the most recent use of this token.
        """

        self.last_used_at = used_at

    def revoke(
        self,
        *,
        revoked_at: datetime,
        revoked_by: str | None = None,
        reason: str | None = None,
    ) -> None:
        """
        Revoke this session token.
        """

        self.revoked_at = revoked_at
        self.revoked_by = revoked_by
        self.revocation_reason = reason

    @property
    def is_revoked(self) -> bool:
        """
        Determine whether the token has been revoked.
        """

        return self.revoked_at is not None
