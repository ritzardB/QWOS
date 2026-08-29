from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CreateEmployeeImmigrationCommand:
    """
    Command for creating an employee immigration record.
    """

    tenant_id: str
    employee_id: str
    immigration_type: str
    status: str
    document_number: str | None = None
    sponsor_name: str | None = None
    issuing_authority: str | None = None
    issue_date: date | None = None
    expiry_date: date | None = None
    notes: str | None = None
