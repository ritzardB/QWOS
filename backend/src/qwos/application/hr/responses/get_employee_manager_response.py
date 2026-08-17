from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class GetEmployeeManagerResponse(BaseModel):
    employee_id: str
    manager_employee_id: str | None
    manager_employee_number: str | None
    relationship_type: str | None
    effective_from: date | None