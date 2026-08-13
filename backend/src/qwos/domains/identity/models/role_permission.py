"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    role_permission.py

Description:
    SQLAlchemy model representing permission assignments to roles.

    This is a business entity rather than a simple junction table.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class RolePermission(TenantEntity):
    """
    Role permission assignment.
    """

    __tablename__ = "role_permissions"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("is_enabled", True)

        super().__init__(**kwargs)

    # -------------------------------------------------------------------------
    # Assignment
    # -------------------------------------------------------------------------

    role_id: Mapped[str] = mapped_column(
        ULID,
        nullable=False,
    )

    permission_id: Mapped[str] = mapped_column(
        ULID,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    granted_by: Mapped[str | None] = mapped_column(
        ULID,
        nullable=True,
    )

    effective_from: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    effective_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    assignment_reason: Mapped[str | None] = mapped_column(
        nullable=True,
    )
