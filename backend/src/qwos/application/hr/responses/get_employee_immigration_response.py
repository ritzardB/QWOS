from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class GetEmployeeImmigrationResponse:
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
