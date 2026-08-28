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
from .attendance_schedule_resolution_service import (
    AttendanceScheduleResolution,
    AttendanceScheduleResolutionService,
)
from .effective_work_schedule_resolution_service import (
    EffectiveWorkScheduleResolutionService,
)
from .attendance_time_segment_service import (
    AttendanceTimeSegmentService,
)
from .attendance_pay_classification_service import (
    AttendancePayClassificationService,
)

__all__ = [
    "AttendancePayClassificationService",
    "AttendanceTimeSegmentService",
    "AttendanceScheduleResolution",
    "AttendanceScheduleResolutionService",
    "EffectiveWorkScheduleResolutionService",
    "AttendancePolicyResolutionService",
    "ResolvedAttendanceContext",
    "AttendanceCalculationService",
    "AttendanceCalculationResult",
]