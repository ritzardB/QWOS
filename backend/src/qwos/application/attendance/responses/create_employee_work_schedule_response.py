from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class CreateEmployeeWorkScheduleResponse:
    """
    Response returned after creating an employee work schedule assignment.
    """

    id: str
    employee_id: str
    work_schedule_id: str
    effective_from: date
    effective_until: date | None
    is_active: bool
    created_at: datetime