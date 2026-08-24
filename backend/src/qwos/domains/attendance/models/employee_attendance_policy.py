"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    employee_attendance_policy.py

Description:
    SQLAlchemy model representing an employee's effective attendance policy
    assignment.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class EmployeeAttendancePolicy(TenantEntity):
    """
    Represents an attendance policy assignment for an employee.

    The assignment is effective from a specified date and may optionally
    expire on an effective-until date.
    """

    __tablename__ = "employee_attendance_policies"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "is_active",
            True,
        )

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
        attendance_policy_id: str,
        effective_from: date,
        effective_until: date | None = None,
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "EmployeeAttendancePolicy":
        """
        Create a normalized employee attendance policy assignment.
        """

        if effective_until is not None:
            if effective_until < effective_from:
                raise ValueError(
                    "effective_until cannot be earlier than effective_from.",
                )

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            attendance_policy_id=attendance_policy_id,
            effective_from=effective_from,
            effective_until=effective_until,
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Employee
    # -------------------------------------------------------------------------

    employee_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "employees.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Attendance Policy
    # -------------------------------------------------------------------------

    attendance_policy_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "attendance_policies.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Effective Dating
    # -------------------------------------------------------------------------

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )