from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CreateWorkScheduleResponse:
    """
    Application response for a newly created work schedule.
    """

    id: str
    schedule_code: str
    schedule_name: str
    timezone: str
    is_active: bool
    created_at: datetime