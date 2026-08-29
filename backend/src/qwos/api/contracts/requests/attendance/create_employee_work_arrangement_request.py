"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    create_employee_work_arrangement_request.py

Description:
    Request contract for creating an employee work arrangement.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateEmployeeWorkArrangementRequest(BaseRequest):
    """
    Request for creating an employee work arrangement.
    """

    work_arrangement: str = Field(
        default="office",
        max_length=50,
    )

    effective_from: date

    effective_until: date | None = None

    is_active: bool = True
