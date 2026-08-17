"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    list_expiring_employee_immigration_response.py

Description:
    API response contract for immigration expiry monitoring.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class ExpiringEmployeeImmigrationItemResponse(BaseModel):
    """
    Immigration record approaching expiry.
    """

    id: str
    employee_id: str
    immigration_type: str
    status: str
    document_number: str | None
    issue_date: date | None
    expiry_date: date
    days_until_expiry: int


class ListExpiringEmployeeImmigrationResponse(BaseModel):
    """
    Response containing immigration records approaching expiry.
    """

    items: list[ExpiringEmployeeImmigrationItemResponse]