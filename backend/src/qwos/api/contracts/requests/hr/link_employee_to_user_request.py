"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    link_employee_to_user_request.py

Description:
    Request contract for linking an employee to an existing QWOS user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class LinkEmployeeToUserRequest(BaseRequest):
    """
    Request for linking an employee to an existing QWOS user.
    """

    user_id: str = Field(
        min_length=26,
        max_length=26,
    )

    first_name: str = Field(
        min_length=1,
        max_length=100,
    )

    middle_name: str | None = Field(
        default=None,
        max_length=100,
    )

    last_name: str = Field(
        min_length=1,
        max_length=100,
    )

    preferred_name: str | None = Field(
        default=None,
        max_length=100,
    )