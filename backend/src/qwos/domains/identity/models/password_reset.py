"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    password_reset.py

Description:
    SQLAlchemy model representing a password reset request.

    Raw password-reset tokens must never be persisted. Only their secure
    cryptographic hash is stored.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import enum_column
from qwos.domains.identity.enums.password_reset_status import (
    PasswordResetStatus,
)


class PasswordReset(TenantEntity):
    """
    Represents a password reset request for a user.
    """

    __tablename__ = "password_resets"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "password_reset_status",
            PasswordResetStatus.PENDING,
        )
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
        user_id: str,
        reset_token_hash: str,
        expires_at: datetime,
        requested_at: datetime,
        request_ip_address: str | None = None,
        request_user_agent: str | None = None,
        created_by: str | None = None,
    ) -> "PasswordReset":
        """
        Create a new password reset request.

        The raw reset token must never be supplied to this entity.
        Only its cryptographic hash is persisted.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            user_id=user_id,
            reset_token_hash=reset_token_hash,
            requested_at=requested_at,
            expires_at=expires_at,
            request_ip_address=request_ip_address,
            request_user_agent=request_user_agent,
            created_by=created_by,
            updated_by=created_by,
        )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Reset Token
    # ------------------------------------------------------------------

    reset_token_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    password_reset_status: Mapped[PasswordResetStatus] = mapped_column(
        enum_column(PasswordResetStatus),
        nullable=False,
        default=PasswordResetStatus.PENDING,
    )

    # ------------------------------------------------------------------
    # Request Metadata
    # ------------------------------------------------------------------

    request_ip_address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    request_user_agent: Mapped[str | None] = mapped_column(
        Text,
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
        Mark the reset request as used.
        """

        self.used_at = used_at
        self.password_reset_status = PasswordResetStatus.USED

    def mark_expired(self) -> None:
        """
        Mark the reset request as expired.
        """

        self.password_reset_status = PasswordResetStatus.EXPIRED

    def revoke(
        self,
        *,
        revoked_at: datetime,
    ) -> None:
        """
        Revoke the reset request.
        """

        self.revoked_at = revoked_at
        self.password_reset_status = PasswordResetStatus.REVOKED

    # ------------------------------------------------------------------
    # State Properties
    # ------------------------------------------------------------------

    @property
    def is_pending(self) -> bool:
        """
        Determine whether the reset request is pending.
        """

        return self.password_reset_status == PasswordResetStatus.PENDING

    @property
    def is_used(self) -> bool:
        """
        Determine whether the reset request has been used.
        """

        return self.password_reset_status == PasswordResetStatus.USED

    @property
    def is_expired(self) -> bool:
        """
        Determine whether the reset request has expired.
        """

        return self.password_reset_status == PasswordResetStatus.EXPIRED

    @property
    def is_revoked(self) -> bool:
        """
        Determine whether the reset request has been revoked.
        """

        return self.password_reset_status == PasswordResetStatus.REVOKED
