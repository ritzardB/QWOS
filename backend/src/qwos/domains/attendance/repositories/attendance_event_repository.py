"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Attendance Event Repository Contract
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.attendance.models.attendance_event import (
    AttendanceEvent,
)


class AttendanceEventRepository(Protocol):
    """
    Contract for AttendanceEvent persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        attendance_event_id: str,
    ) -> AttendanceEvent | None:
        """
        Retrieve an attendance event by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        attendance_event_id: str,
    ) -> AttendanceEvent | None:
        """
        Retrieve a non-deleted attendance event within a tenant.
        """
        ...

    def save(
        self,
        attendance_event: AttendanceEvent,
    ) -> None:
        """
        Persist an attendance event.
        """
        ...

    # -------------------------------------------------------------------------
    # Attendance Event Queries
    # -------------------------------------------------------------------------

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[AttendanceEvent]:
        """
        Retrieve attendance events for an employee.
        """
        ...

    def list_by_employee_and_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        attendance_date: date,
    ) -> list[AttendanceEvent]:
        """
        Retrieve attendance events for an employee on a specific date.
        """
        ...

    def list_by_record(
        self,
        *,
        tenant_id: str,
        attendance_record_id: str,
    ) -> list[AttendanceEvent]:
        """
        Retrieve all events belonging to an attendance record.
        """
        ...

    def list_by_record_ordered(
        self,
        *,
        tenant_id: str,
        attendance_record_id: str,
    ) -> list[AttendanceEvent]:
        """
        Retrieve attendance events for a record ordered chronologically.
        """
        ...

    def get_latest_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> AttendanceEvent | None:
        """
        Retrieve the most recent attendance event for an employee.
        """
        ...

    def get_latest_by_record(
        self,
        *,
        tenant_id: str,
        attendance_record_id: str,
    ) -> AttendanceEvent | None:
        """
        Retrieve the most recent attendance event for an attendance record.
        """
        ...
