from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class ListEmployeesResponse:
    employees: list["EmployeeSummaryResponse"]


@dataclass(frozen=True, slots=True)
class EmployeeSummaryResponse:
    id: str
    employee_number: str
    user_id: str | None
    hire_date: date | None
    employment_status: str
    employment_type: str
    work_email: str | None
    work_phone: str | None
    created_at: datetime