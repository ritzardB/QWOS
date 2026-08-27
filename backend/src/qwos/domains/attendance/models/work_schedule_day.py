"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    work_schedule_day.py

Description:
    SQLAlchemy model representing a weekly work schedule day rule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import time
from enum import Enum
from typing import Any

from sqlalchemy import Boolean, ForeignKey, Integer, SmallInteger, Time
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID, enum_column


class ScheduleDayType(str, Enum):
    """
    Supported schedule day types.
    """

    WORKDAY = "workday"
    REST_DAY = "rest_day"


class WorkScheduleDay(TenantEntity):
    """
    Represents the weekly rule for one day within a work schedule.
    """

    __tablename__ = "work_schedule_days"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "day_type",
            ScheduleDayType.WORKDAY,
        )
        kwargs.setdefault(
            "break_minutes",
            0,
        )
        kwargs.setdefault(
            "is_overnight",
            False,
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
        work_schedule_id: str,
        day_of_week: int,
        day_type: str = "workday",
        start_time: time | None = None,
        end_time: time | None = None,
        break_minutes: int = 0,
        is_overnight: bool = False,
        created_by: str | None = None,
    ) -> "WorkScheduleDay":
        """
        Create a normalized work schedule day.
        """

        normalized_day_type = day_type.strip().lower()

        if day_of_week < 1 or day_of_week > 7:
            raise ValueError(
                "day_of_week must be between 1 and 7.",
            )

        if not normalized_day_type:
            raise ValueError(
                "day_type is required.",
            )

        if normalized_day_type not in {
            day_type.value
            for day_type in ScheduleDayType
        }:
            raise ValueError(
                "day_type must be one of: workday, rest_day.",
            )

        if break_minutes < 0:
            raise ValueError(
                "break_minutes cannot be negative.",
            )

        if normalized_day_type == ScheduleDayType.REST_DAY.value:
            if start_time is not None or end_time is not None:
                raise ValueError(
                    "rest_day cannot define start_time or end_time.",
                )

            if break_minutes != 0:
                raise ValueError(
                    "rest_day break_minutes must be zero.",
                )

            if is_overnight:
                raise ValueError(
                    "rest_day cannot be overnight.",
                )

        else:
            if start_time is None:
                raise ValueError(
                    "workday start_time is required.",
                )

            if end_time is None:
                raise ValueError(
                    "workday end_time is required.",
                )

        return cls(
            id=id,
            tenant_id=tenant_id,
            work_schedule_id=work_schedule_id,
            day_of_week=day_of_week,
            day_type=normalized_day_type,
            start_time=start_time,
            end_time=end_time,
            break_minutes=break_minutes,
            is_overnight=is_overnight,
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Work Schedule
    # -------------------------------------------------------------------------

    work_schedule_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "work_schedules.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Day
    # -------------------------------------------------------------------------

    day_of_week: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    day_type: Mapped[ScheduleDayType] = mapped_column(
        enum_column(ScheduleDayType),
        nullable=False,
        default=ScheduleDayType.WORKDAY,
    )

    # -------------------------------------------------------------------------
    # Working Times
    # -------------------------------------------------------------------------

    start_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    end_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Break
    # -------------------------------------------------------------------------

    break_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # -------------------------------------------------------------------------
    # Overnight
    # -------------------------------------------------------------------------

    is_overnight: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )