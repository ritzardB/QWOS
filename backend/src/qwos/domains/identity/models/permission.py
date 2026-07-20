"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    permission.py

Description:
    SQLAlchemy model representing system permissions.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import BaseEntity


class Permission(BaseEntity):
    """
    System permission.
    """

    __tablename__ = "permissions"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("is_system", True)
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

    module: Mapped[str] = mapped_column(
        nullable=False,
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
