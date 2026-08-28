"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_pay_classification.py

Description:
    Domain value object representing the pay classifications that apply
    to a segment of attendance time.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AttendancePayClassification:
    """
    Describes the pay-related classifications that apply to a period
    of attendance time.

    This object intentionally contains no rates or monetary values.
    Rates are supplied later by the applicable premium policy.
    """

    is_regular: bool = True
    is_night_differential: bool = False
    is_holiday: bool = False
    is_rest_day: bool = False
    is_overtime: bool = False

    @property
    def has_premium(self) -> bool:
        """
        Return whether any premium-related classification applies.
        """

        return (
            self.is_night_differential
            or self.is_holiday
            or self.is_rest_day
            or self.is_overtime
        )

    @property
    def is_combined_premium(self) -> bool:
        """
        Return whether multiple premium classifications apply.
        """

        premium_flags = (
            self.is_night_differential,
            self.is_holiday,
            self.is_rest_day,
            self.is_overtime,
        )

        return sum(premium_flags) > 1