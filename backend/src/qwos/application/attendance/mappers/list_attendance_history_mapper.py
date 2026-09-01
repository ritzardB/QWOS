"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    list_attendance_history_mapper.py

Description:
    Maps attendance history application responses to API responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.responses.attendance.list_attendance_history_response import (
    AttendanceHistoryListItem,
)
from qwos.api.contracts.responses.attendance.list_attendance_history_response import (
    ListAttendanceHistoryResponse as ApiListAttendanceHistoryResponse,
)
from qwos.application.attendance.responses.list_attendance_history_response import (
    ListAttendanceHistoryResponse,
)


class ListAttendanceHistoryMapper:
    """
    Mapper for Attendance History responses.
    """

    @staticmethod
    def to_response(
        application_response: ListAttendanceHistoryResponse,
    ) -> ApiListAttendanceHistoryResponse:
        """
        Map application response to API response.
        """

        items = [
            AttendanceHistoryListItem(
                attendance_record_id=item.attendance_record_id,
                employee_id=item.employee_id,
                attendance_date=item.attendance_date,
                status=item.status,
                clock_in_at=item.clock_in_at,
                clock_out_at=item.clock_out_at,
                worked_minutes=item.worked_minutes,
                late_minutes=item.late_minutes,
                undertime_minutes=item.undertime_minutes,
                overtime_minutes=item.overtime_minutes,
                notes=item.notes,
            )
            for item in application_response.items
        ]

        return ApiListAttendanceHistoryResponse(
            items=items,
            total=application_response.total,
        )