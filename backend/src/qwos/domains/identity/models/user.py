"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    user.py

Description:
    SQLAlchemy model representing authenticated users.

    This entity stores authentication and account security information only.

    Personal information is intentionally separated into the UserProfile
    entity.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations
from typing import Any

from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.base import BaseEntity
from qwos.core.database.types import ULID, enum_column
from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.enums.authentication_provider import (
    AuthenticationProvider,
)
from qwos.domains.identity.enums.user_type import UserType


class User(BaseEntity):
    """
    Authenticated user.

    Stores authentication credentials and account security information.

    Personal profile information is stored separately in UserProfile.
    """

    __tablename__ = "users"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "account_status",
            AccountStatus.PENDING,
        )

        kwargs.setdefault(
            "authentication_provider",
            AuthenticationProvider.LOCAL,
        )

        kwargs.setdefault(
            "user_type",
            UserType.EMPLOYEE,
        )

        kwargs.setdefault(
            "failed_login_attempts",
            0,
        )

        super().__init__(**kwargs)

    # -------------------------------------------------------------------------
    # Tenant
    # -------------------------------------------------------------------------

    tenant_id: Mapped[str] = mapped_column(
        ULID,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    email: Mapped[str] = mapped_column(
        nullable=False,
    )

    password_hash: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    account_status: Mapped[AccountStatus] = mapped_column(
        enum_column(AccountStatus),
        nullable=False,
        default=AccountStatus.PENDING,
    )

    # -------------------------------------------------------------------------
    # Authentication
    # -------------------------------------------------------------------------

    authentication_provider: Mapped[AuthenticationProvider] = mapped_column(
        enum_column(AuthenticationProvider),
        nullable=False,
        default=AuthenticationProvider.LOCAL,
    )

    user_type: Mapped[UserType] = mapped_column(
        enum_column(UserType),
        nullable=False,
        default=UserType.EMPLOYEE,
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    password_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
