"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Repository Contracts
===============================================================================
"""

from .attendance_event_repository import AttendanceEventRepository
from .attendance_record_repository import AttendanceRecordRepository

__all__ = [
    "AttendanceEventRepository",
    "AttendanceRecordRepository",
]