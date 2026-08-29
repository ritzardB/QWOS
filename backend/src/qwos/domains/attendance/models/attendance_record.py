"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_record.py

Description:
    SQLAlchemy model representing a daily employee attendance record.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class AttendanceRecord(TenantEntity):
    """
    Represents the daily attendance outcome for an employee.
    """

    __tablename__ = "attendance_records"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "status",
            "present",
        )
        kwargs.setdefault(
            "worked_minutes",
            0,
        )
        kwargs.setdefault(
            "late_minutes",
            0,
        )
        kwargs.setdefault(
            "undertime_minutes",
            0,
        )
        kwargs.setdefault(
            "overtime_minutes",
            0,
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
        attendance_date: date,
        pay_period_id: str | None = None,
        status: str = "present",
        clock_in_at: datetime | None = None,
        clock_out_at: datetime | None = None,
        worked_minutes: int = 0,
        late_minutes: int = 0,
        undertime_minutes: int = 0,
        overtime_minutes: int = 0,
        notes: str | None = None,
        created_by: str | None = None,
    ) -> "AttendanceRecord":
        """
        Create a normalized attendance record.
        """

        normalized_status = status.strip().lower()

        if not normalized_status:
            raise ValueError(
                "status is required.",
            )

        if worked_minutes < 0:
            raise ValueError(
                "worked_minutes cannot be negative.",
            )

        if late_minutes < 0:
            raise ValueError(
                "late_minutes cannot be negative.",
            )

        if undertime_minutes < 0:
            raise ValueError(
                "undertime_minutes cannot be negative.",
            )

        if overtime_minutes < 0:
            raise ValueError(
                "overtime_minutes cannot be negative.",
            )

        if clock_in_at is not None and clock_out_at is not None and clock_out_at < clock_in_at:
            raise ValueError(
                "clock_out_at cannot be earlier than clock_in_at.",
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            pay_period_id=pay_period_id,
            attendance_date=attendance_date,
            status=normalized_status,
            clock_in_at=clock_in_at,
            clock_out_at=clock_out_at,
            worked_minutes=worked_minutes,
            late_minutes=late_minutes,
            undertime_minutes=undertime_minutes,
            overtime_minutes=overtime_minutes,
            notes=(notes.strip() if notes else None),
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
    # Pay Period
    # -------------------------------------------------------------------------

    pay_period_id: Mapped[str | None] = mapped_column(
        ULID,
        ForeignKey(
            "pay_periods.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Attendance Date
    # -------------------------------------------------------------------------

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Attendance Status
    # -------------------------------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="present",
    )

    # -------------------------------------------------------------------------
    # Attendance Times
    # -------------------------------------------------------------------------

    clock_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    clock_out_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Attendance Calculations
    # -------------------------------------------------------------------------

    worked_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    late_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    undertime_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    overtime_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # -------------------------------------------------------------------------
    # Notes
    # -------------------------------------------------------------------------

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
