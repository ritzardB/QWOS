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

from qwos.core.database.entity_base import BaseEntity
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
    # Factory
    # -------------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        user_id: str,
        first_name: str,
        last_name: str,
        middle_name: str | None = None,
        preferred_name: str | None = None,
    ) -> "UserProfile":
        """
        Create a new user profile.
        """

        first_name = first_name.strip()
        last_name = last_name.strip()

        display_name = f"{first_name} {last_name}".strip()

        return cls(
            id=id,
            tenant_id=tenant_id,
            user_id=user_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            display_name=display_name,
            preferred_name=preferred_name,
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
