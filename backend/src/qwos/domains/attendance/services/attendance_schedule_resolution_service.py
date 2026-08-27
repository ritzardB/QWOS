"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_schedule_resolution_service.py

Description:
    Resolves the effective work schedule and weekly day rule for an
    employee on a specific attendance date.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from qwos.domains.attendance.models.employee_work_schedule import (
    EmployeeWorkSchedule,
)
from qwos.domains.attendance.models.work_schedule import WorkSchedule
from qwos.domains.attendance.models.work_schedule_day import WorkScheduleDay
from qwos.domains.attendance.repositories.employee_work_schedule_repository import (
    EmployeeWorkScheduleRepository,
)
from qwos.domains.attendance.repositories.work_schedule_day_repository import (
    WorkScheduleDayRepository,
)
from qwos.domains.attendance.repositories.work_schedule_repository import (
    WorkScheduleRepository,
)


@dataclass(frozen=True, slots=True)
class AttendanceScheduleResolution:
    """
    Resolved schedule information for an employee on an attendance date.
    """

    assignment: EmployeeWorkSchedule
    work_schedule: WorkSchedule
    schedule_day: WorkScheduleDay


class AttendanceScheduleResolutionService:
    """
    Resolves the effective work schedule and matching weekly day rule
    for an employee on a specific date.
    """

    def __init__(
        self,
        *,
        employee_work_schedule_repository: EmployeeWorkScheduleRepository,
        work_schedule_repository: WorkScheduleRepository,
        work_schedule_day_repository: WorkScheduleDayRepository,
    ) -> None:
        self._employee_work_schedule_repository = (
            employee_work_schedule_repository
        )
        self._work_schedule_repository = work_schedule_repository
        self._work_schedule_day_repository = work_schedule_day_repository

    def resolve_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        attendance_date: date,
    ) -> AttendanceScheduleResolution | None:
        """
        Resolve the effective schedule and weekday rule for an employee.
        """

        assignment = (
            self._employee_work_schedule_repository.get_effective_for_employee(
                tenant_id=tenant_id,
                employee_id=employee_id,
                effective_date=attendance_date,
            )
        )

        if assignment is None:
            return None

        work_schedule = self._work_schedule_repository.get_by_id_for_tenant(
            tenant_id=tenant_id,
            schedule_id=assignment.work_schedule_id,
        )

        if work_schedule is None:
            return None

        day_of_week = attendance_date.isoweekday()

        schedule_day = (
            self._work_schedule_day_repository.get_by_schedule_and_day(
                tenant_id=tenant_id,
                work_schedule_id=assignment.work_schedule_id,
                day_of_week=day_of_week,
            )
        )

        if schedule_day is None:
            return None

        return AttendanceScheduleResolution(
            assignment=assignment,
            work_schedule=work_schedule,
            schedule_day=schedule_day,
        )