"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    clock_out_request.py

Description:
    Request contract for clocking out an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class ClockOutRequest(BaseRequest):
    """
    Request for clocking out an employee.
    """

    employee_id: str = Field(
        min_length=26,
        max_length=26,
    )

    clock_out_at: datetime | None = None

    event_source: str = Field(
        default="web",
        min_length=1,
        max_length=50,
    )

    notes: str | None = Field(
        default=None,
        max_length=500,
    )
