from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class GetEmployeeManagerResponse:
    employee_id: str
    manager_employee_id: str
    manager_employee_number: str
    relationship_type: str
    effective_from: date