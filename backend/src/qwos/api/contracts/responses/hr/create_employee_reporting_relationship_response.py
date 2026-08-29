from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class CreateEmployeeReportingRelationshipResponse(BaseModel):
    id: str
    employee_id: str
    manager_employee_id: str
    relationship_type: str
    effective_from: date
    effective_to: date | None
    is_primary: bool
    created_at: datetime
