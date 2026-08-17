"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    employee_position.py

Description:
    SQLAlchemy model representing an employee's organizational position.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class EmployeePosition(TenantEntity):
    """
    Stores an employee's organizational position.
    """

    __tablename__ = "employee_positions"

    def __init__(self, **kwargs: Any) -> None:
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
        employee_id: str,
        job_title: str,
        organizational_level: str,
        effective_from: date,
        effective_to: date | None = None,
        created_by: str | None = None,
    ) -> "EmployeePosition":
        """
        Create a new employee position.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            job_title=job_title.strip(),
            organizational_level=organizational_level.strip().lower(),
            effective_from=effective_from,
            effective_to=effective_to,
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Ownership
    # -------------------------------------------------------------------------

    employee_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Position
    # -------------------------------------------------------------------------

    job_title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    organizational_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Effective Dating
    # -------------------------------------------------------------------------

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )