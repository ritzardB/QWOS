"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_pay_classification_service.py

Description:
    Determines the pay classifications that apply to an attendance time
    segment.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.domains.attendance.models.attendance_pay_classification import (
    AttendancePayClassification,
)
from qwos.domains.attendance.models.attendance_time_segment import (
    AttendanceTimeSegment,
)


class AttendancePayClassificationService:
    """
    Determines the pay classifications applicable to an attendance segment.

    This service does not calculate rates, multipliers, or monetary amounts.
    """

    def classify(
        self,
        segment: AttendanceTimeSegment,
    ) -> AttendancePayClassification:
        """
        Convert an attendance time segment into pay classifications.
        """

        return AttendancePayClassification(
            is_regular=not (
                segment.is_holiday or segment.is_rest_day or segment.is_overtime or segment.is_night_differential
            ),
            is_night_differential=segment.is_night_differential,
            is_holiday=segment.is_holiday,
            is_rest_day=segment.is_rest_day,
            is_overtime=segment.is_overtime,
        )
