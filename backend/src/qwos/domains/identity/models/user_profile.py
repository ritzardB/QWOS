"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

User Profile Model
===============================================================================
"""

from __future__ import annotations
from typing import Any

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.base import BaseEntity
from qwos.core.database.types import ULID


class UserProfile(BaseEntity):
    """
    Stores personal profile information.

    Authentication and authorization data belong to the User entity.
    """

    __tablename__ = "user_profiles"

    # -------------------------------------------------------------------------
    # Tenant
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("locale", "en-US")
        kwargs.setdefault("language_code", "en")
        kwargs.setdefault("timezone", "UTC")
        super().__init__(**kwargs)

    tenant_id: Mapped[str] = mapped_column(
        ULID,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    user_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # -------------------------------------------------------------------------
    # Personal Information
    # -------------------------------------------------------------------------

    first_name: Mapped[str]

    middle_name: Mapped[str | None]

    last_name: Mapped[str]

    display_name: Mapped[str]

    preferred_name: Mapped[str | None]

    # -------------------------------------------------------------------------
    # Localization
    # -------------------------------------------------------------------------

    locale: Mapped[str] = mapped_column(
        default="en-US",
    )

    language_code: Mapped[str] = mapped_column(
        default="en",
    )

    timezone: Mapped[str] = mapped_column(
        default="UTC",
    )

    # -------------------------------------------------------------------------
    # Profile
    # -------------------------------------------------------------------------

    avatar_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
