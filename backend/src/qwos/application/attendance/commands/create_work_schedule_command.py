from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateWorkScheduleCommand:
    """
    Command for creating a master work schedule.
    """

    tenant_id: str
    schedule_code: str
    schedule_name: str
    timezone: str = "UTC"
    is_active: bool = True