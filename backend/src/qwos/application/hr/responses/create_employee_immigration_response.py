from __future__ import annotations

from datetime import date


class CreateEmployeeImmigrationResponse:
    """
    Response returned after creating an immigration record.
    """

    def __init__(
        self,
        *,
        id: str,
        employee_id: str,
        immigration_type: str,
        status: str,
        document_number: str | None,
        sponsor_name: str | None,
        issuing_authority: str | None,
        issue_date: date | None,
        expiry_date: date | None,
        notes: str | None,
    ) -> None:
        self.id = id
        self.employee_id = employee_id
        self.immigration_type = immigration_type
        self.status = status
        self.document_number = document_number
        self.sponsor_name = sponsor_name
        self.issuing_authority = issuing_authority
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.notes = notes