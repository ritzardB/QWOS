"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    session.py

Description:
    SQLAlchemy model representing an authenticated user session.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class Session(TenantEntity):
    """
    Represents an authenticated user session.

    A user may have multiple concurrent sessions across devices.
    """

    __tablename__ = "sessions"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("is_active", True)
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
        expires_at: datetime,
        session_name: str | None = None,
        device_name: str | None = None,
        browser_name: str | None = None,
        operating_system: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        created_by: str | None = None,
    ) -> "Session":
        """
        Create a new authenticated session.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            user_id=user_id,
            session_name=session_name,
            device_name=device_name,
            browser_name=browser_name,
            operating_system=operating_system,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
            created_by=created_by,
            updated_by=created_by,
        )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    user_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Session Metadata
    # ------------------------------------------------------------------

    session_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    device_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    browser_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    operating_system: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        INET,
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Authentication Lifecycle
    # ------------------------------------------------------------------

    signed_in_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    signed_out_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )
