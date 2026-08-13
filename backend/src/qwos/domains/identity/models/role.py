"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    role.py

Description:
    SQLAlchemy model representing application roles.

    Roles group permissions and are assigned to users.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class Role(TenantEntity):
    """
    Application role.
    """

    __tablename__ = "roles"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("is_system", False)
        kwargs.setdefault("is_active", True)

        super().__init__(**kwargs)

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    code: Mapped[str] = mapped_column(
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Classification
    # -------------------------------------------------------------------------

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
