"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_event.py

Description:
    SQLAlchemy model representing an employee attendance event.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class AttendanceEvent(TenantEntity):
    """
    Represents an individual employee attendance event.

    Examples:

        clock_in
        break_start
        break_end
        clock_out

    The event represents what happened.
    AttendanceRecord represents the resulting daily attendance outcome.
    """

    __tablename__ = "attendance_events"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "event_source",
            "web",
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
        attendance_record_id: str,
        employee_id: str,
        event_type: str,
        event_at: datetime,
        event_source: str = "web",
        notes: str | None = None,
        created_by: str | None = None,
    ) -> "AttendanceEvent":
        """
        Create a normalized attendance event.
        """

        normalized_event_type = event_type.strip().lower()
        normalized_event_source = event_source.strip().lower()

        if not normalized_event_type:
            raise ValueError(
                "event_type is required.",
            )

        if not normalized_event_source:
            raise ValueError(
                "event_source is required.",
            )

        if event_at.tzinfo is None:
            raise ValueError(
                "event_at must be timezone-aware.",
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            attendance_record_id=attendance_record_id,
            employee_id=employee_id,
            event_type=normalized_event_type,
            event_at=event_at,
            event_source=normalized_event_source,
            notes=(notes.strip() if notes else None),
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Attendance Record
    # -------------------------------------------------------------------------

    attendance_record_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "attendance_records.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
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
    # Event Type
    # -------------------------------------------------------------------------

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Event Timestamp
    # -------------------------------------------------------------------------

    event_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Event Source
    # -------------------------------------------------------------------------

    event_source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="web",
    )

    # -------------------------------------------------------------------------
    # Notes
    # -------------------------------------------------------------------------

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
