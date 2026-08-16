from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class CreateEmployeeReportingRelationshipResponse:
    id: str
    employee_id: str
    manager_employee_id: str
    relationship_type: str
    effective_from: date
    effective_to: date | None
    is_primary: bool
    created_at: datetime