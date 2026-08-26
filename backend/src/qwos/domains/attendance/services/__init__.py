"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Service Layer
===============================================================================
"""

from .attendance_calculation_service import (
    AttendanceCalculationResult,
    AttendanceCalculationService,
)
from .attendance_policy_resolution_service import (
    AttendancePolicyResolutionService,
    ResolvedAttendanceContext,
)

__all__ = [
    "AttendancePolicyResolutionService",
    "ResolvedAttendanceContext",
    "AttendanceCalculationService",
    "AttendanceCalculationResult",
]