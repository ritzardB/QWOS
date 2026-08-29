"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    effective_work_schedule_resolution_service.py

Description:
    Resolves the employee work schedule that is effective for a
    specific date.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from qwos.domains.attendance.models.employee_work_schedule import (
    EmployeeWorkSchedule,
)
from qwos.domains.attendance.repositories.employee_work_schedule_repository import (
    EmployeeWorkScheduleRepository,
)


class EffectiveWorkScheduleResolutionService:
    """
    Resolves the work schedule assignment effective for an employee
    on a specific date.
    """

    def __init__(
        self,
        *,
        employee_work_schedule_repository: EmployeeWorkScheduleRepository,
    ) -> None:
        self._employee_work_schedule_repository = employee_work_schedule_repository

    def resolve(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> EmployeeWorkSchedule | None:
        """
        Resolve the employee work schedule effective on a date.
        """

        return self._employee_work_schedule_repository.get_effective_for_employee(
            tenant_id=tenant_id,
            employee_id=employee_id,
            effective_date=effective_date,
        )
