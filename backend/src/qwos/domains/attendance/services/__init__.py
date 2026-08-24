"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Service Layer
===============================================================================
"""

from .attendance_policy_resolution_service import (
    AttendancePolicyResolutionService,
    ResolvedAttendanceContext,
)
from .attendance_calculation_service import (
    AttendanceCalculationService,
    AttendanceCalculationResult,
)

__all__ = [
    "AttendancePolicyResolutionService",
    "ResolvedAttendanceContext",
    "AttendanceCalculationService",
    "AttendanceCalculationResult",
]