"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    user_role.py

Description:
    SQLAlchemy model representing role assignments to users.

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


class UserRole(TenantEntity):
    """
    Role assignment for a user.

    A user may have multiple roles.
    """

    __tablename__ = "user_roles"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("is_enabled", True)
        kwargs.setdefault("is_primary", False)

        super().__init__(**kwargs)

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
        role_id: str,
        assigned_at: datetime,
        assigned_by: str | None = None,
        is_primary: bool = False,
        effective_from: datetime | None = None,
        effective_until: datetime | None = None,
        assignment_reason: str | None = None,
    ) -> "UserRole":
        """
        Create a new user-role assignment.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            user_id=user_id,
            role_id=role_id,
            is_primary=is_primary,
            is_enabled=True,
            assigned_at=assigned_at,
            assigned_by=assigned_by,
            effective_from=effective_from,
            effective_until=effective_until,
            assignment_reason=assignment_reason,
            created_by=assigned_by,
            updated_by=assigned_by,
        )
    
    # -------------------------------------------------------------------------
    # Assignment
    # -------------------------------------------------------------------------

    user_id: Mapped[str] = mapped_column(
        ULID,
        nullable=False,
    )

    role_id: Mapped[str] = mapped_column(
        ULID,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Assignment Lifecycle
    # -------------------------------------------------------------------------

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    assigned_by: Mapped[str | None] = mapped_column(
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
