"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    list_attendance_history_use_case.py

Description:
    Lists attendance history for an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.responses.list_attendance_history_response import (
    AttendanceHistoryListItem,
    ListAttendanceHistoryResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.domains.attendance.repositories.attendance_record_repository import (
    AttendanceRecordRepository,
)


class ListAttendanceHistoryUseCase:
    """
    Use case for listing attendance history for an employee.
    """

    def __init__(
        self,
        *,
        attendance_record_repository: AttendanceRecordRepository,
        request_context: RequestContext,
    ) -> None:
        self._attendance_record_repository = (
            attendance_record_repository
        )
        self._request_context = request_context

    async def execute(
        self,
        employee_id: str,
    ) -> ListAttendanceHistoryResponse:
        """
        List attendance history for an employee.
        """

        records = (
            self._attendance_record_repository.list_by_employee(
                tenant_id=self._request_context.tenant_id,
                employee_id=employee_id,
            )
        )

        items = [
            AttendanceHistoryListItem(
                attendance_record_id=record.id,
                employee_id=record.employee_id,
                attendance_date=record.attendance_date,
                status=record.status,
                clock_in_at=record.clock_in_at,
                clock_out_at=record.clock_out_at,
                worked_minutes=record.worked_minutes,
                late_minutes=record.late_minutes,
                undertime_minutes=record.undertime_minutes,
                overtime_minutes=record.overtime_minutes,
                notes=record.notes,
            )
            for record in records
        ]

        return ListAttendanceHistoryResponse(
            items=items,
            total=len(items),
        )