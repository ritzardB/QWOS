"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Attendance Record Repository Contract
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.attendance.models.attendance_record import (
    AttendanceRecord,
)


class AttendanceRecordRepository(Protocol):
    """
    Contract for AttendanceRecord persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        attendance_record_id: str,
    ) -> AttendanceRecord | None:
        """
        Retrieve an attendance record by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        attendance_record_id: str,
    ) -> AttendanceRecord | None:
        """
        Retrieve a non-deleted attendance record within a tenant.
        """
        ...

    def save(
        self,
        attendance_record: AttendanceRecord,
    ) -> None:
        """
        Persist an attendance record.
        """
        ...

    # -------------------------------------------------------------------------
    # Attendance Queries
    # -------------------------------------------------------------------------

    def get_by_employee_and_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        attendance_date: date,
    ) -> AttendanceRecord | None:
        """
        Retrieve an employee attendance record for a specific date.
        """
        ...

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[AttendanceRecord]:
        """
        Retrieve attendance records for an employee.
        """
        ...

    def list_by_employee_and_period(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        pay_period_id: str,
    ) -> list[AttendanceRecord]:
        """
        Retrieve attendance records for an employee within a pay period.
        """
        ...

    def list_by_date(
        self,
        *,
        tenant_id: str,
        attendance_date: date,
    ) -> list[AttendanceRecord]:
        """
        Retrieve attendance records for all employees on a specific date.
        """
        ...
