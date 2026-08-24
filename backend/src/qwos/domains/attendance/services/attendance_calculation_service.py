"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Attendance Calculation Service
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AttendanceCalculationResult:
    """
    Result produced by attendance calculations.
    """

    worked_minutes: int = 0
    late_minutes: int = 0
    undertime_minutes: int = 0
    overtime_minutes: int = 0

    def __post_init__(self) -> None:
        if self.worked_minutes < 0:
            raise ValueError(
                "worked_minutes cannot be negative.",
            )

        if self.late_minutes < 0:
            raise ValueError(
                "late_minutes cannot be negative.",
            )

        if self.undertime_minutes < 0:
            raise ValueError(
                "undertime_minutes cannot be negative.",
            )

        if self.overtime_minutes < 0:
            raise ValueError(
                "overtime_minutes cannot be negative.",
            )


class AttendanceCalculationService:
    """
    Calculates normalized attendance outcomes.

    This service contains attendance mathematics only.

    Policy resolution, event sequencing, and persistence belong to their
    respective layers.
    """

    def calculate(
        self,
        *,
        worked_minutes: int,
        late_minutes: int = 0,
        undertime_minutes: int = 0,
        overtime_minutes: int = 0,
    ) -> AttendanceCalculationResult:
        """
        Create a normalized attendance calculation result.
        """

        return AttendanceCalculationResult(
            worked_minutes=worked_minutes,
            late_minutes=late_minutes,
            undertime_minutes=undertime_minutes,
            overtime_minutes=overtime_minutes,
        )
