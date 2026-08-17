"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    list_employee_immigration_response.py

Description:
    API response contract for employee immigration history.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class EmployeeImmigrationItemResponse(BaseModel):
    """
    Individual employee immigration record.
    """

    id: str
    employee_id: str
    immigration_type: str
    status: str
    document_number: str | None
    sponsor_name: str | None
    issuing_authority: str | None
    issue_date: date | None
    expiry_date: date | None
    notes: str | None


class ListEmployeeImmigrationResponse(BaseModel):
    """
    Response containing employee immigration history.
    """

    items: list[EmployeeImmigrationItemResponse]