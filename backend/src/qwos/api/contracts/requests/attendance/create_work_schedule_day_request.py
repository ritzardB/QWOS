"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    create_work_schedule_day_request.py

Description:
    Request contract for creating a work schedule day rule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import time

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateWorkScheduleDayRequest(BaseRequest):
    """
    Request for creating a work schedule day rule.
    """

    day_of_week: int = Field(
        ge=1,
        le=7,
    )

    day_type: str = Field(
        default="workday",
        max_length=20,
    )

    start_time: time | None = None

    end_time: time | None = None

    break_minutes: int = Field(
        default=0,
        ge=0,
    )

    is_overnight: bool = False