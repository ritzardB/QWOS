"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_time_segment.py

Description:
    Domain value object representing a segment of worked attendance time
    together with its applicable time classifications.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AttendanceTimeSegment:
    """
    Represents a classified segment of attendance time.

    A segment is a continuous interval during which the same attendance
    classifications apply.
    """

    start_at: datetime
    end_at: datetime
    is_overnight: bool = False
    is_holiday: bool = False
    is_rest_day: bool = False
    is_night_differential: bool = False
    is_overtime: bool = False

    def __post_init__(self) -> None:
        """
        Validate the segment boundaries.
        """

        if self.end_at <= self.start_at:
            raise ValueError(
                "end_at must be later than start_at.",
            )

    @property
    def duration_minutes(self) -> int:
        """
        Return the segment duration in whole minutes.
        """

        return int(
            (self.end_at - self.start_at).total_seconds() / 60,
        )

    @property
    def has_premium_classification(self) -> bool:
        """
        Return whether any premium-related classification applies.
        """

        return self.is_holiday or self.is_rest_day or self.is_night_differential or self.is_overtime
