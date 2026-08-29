"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    employee.py

Description:
    SQLAlchemy model representing an HR employee record.

    Authentication information belongs to User.
    Personal profile information belongs to UserProfile.
    Workforce information belongs to Employee.

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


class Employee(TenantEntity):
    """
    Represents an employee within the HR domain.
    """

    __tablename__ = "employees"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("employment_status", "active")
        kwargs.setdefault("employment_type", "full_time")

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
        employee_number: str,
        user_id: str | None = None,
        hire_date: date | None = None,
        employment_status: str = "active",
        employment_type: str = "full_time",
        work_email: str | None = None,
        work_phone: str | None = None,
        created_by: str | None = None,
    ) -> "Employee":
        """
        Create a new employee record.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            user_id=user_id,
            employee_number=employee_number.strip().upper(),
            hire_date=hire_date,
            employment_status=employment_status,
            employment_type=employment_type,
            work_email=(work_email.strip().lower() if work_email else None),
            work_phone=(work_phone.strip() if work_phone else None),
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Authentication / Identity Link
    # -------------------------------------------------------------------------

    user_id: Mapped[str | None] = mapped_column(
        ULID,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Workforce Identity
    # -------------------------------------------------------------------------

    employee_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Employment
    # -------------------------------------------------------------------------

    hire_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    employment_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
    )

    employment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="full_time",
    )

    # -------------------------------------------------------------------------
    # Work Contact
    # -------------------------------------------------------------------------

    work_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    work_phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )
