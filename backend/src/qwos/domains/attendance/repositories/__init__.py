"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Repository Contracts
===============================================================================
"""

from .attendance_event_repository import AttendanceEventRepository
from .attendance_record_repository import AttendanceRecordRepository
from .employee_attendance_policy_repository import (
    EmployeeAttendancePolicyRepository,
)
from .employee_work_agreement_repository import (
    EmployeeWorkAgreementRepository,
)
from .employee_work_arrangement_repository import (
    EmployeeWorkArrangementRepository,
)

__all__ = [
    "AttendanceEventRepository",
    "AttendanceRecordRepository",
    "EmployeeAttendancePolicyRepository",
    "EmployeeWorkAgreementRepository",
    "EmployeeWorkArrangementRepository",
]