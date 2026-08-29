from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class CreateEmployeeImmigrationResponse(BaseModel):
    """
    API response for a created immigration record.
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
