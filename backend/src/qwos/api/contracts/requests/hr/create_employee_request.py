"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    create_employee_request.py

Description:
    Request contract for creating an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from pydantic import EmailStr, Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateEmployeeRequest(BaseRequest):
    """
    Request for creating an employee.
    """

    user_id: str | None = Field(
        default=None,
        min_length=26,
        max_length=26,
    )

    hire_date: date | None = None

    employment_status: str = Field(
        default="active",
        min_length=2,
        max_length=50,
    )

    employment_type: str = Field(
        default="full_time",
        min_length=2,
        max_length=50,
    )

    work_email: EmailStr | None = Field(
        default=None,
    )

    work_phone: str | None = Field(
        default=None,
        max_length=30,
    )
