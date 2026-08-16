from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class EmployeeSummaryResponse(BaseModel):
    id: str
    employee_number: str
    user_id: str | None
    hire_date: date | None
    employment_status: str
    employment_type: str
    work_email: str | None
    work_phone: str | None
    created_at: datetime


class ListEmployeesResponse(BaseModel):
    employees: list[EmployeeSummaryResponse]