from __future__ import annotations

from datetime import date

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateEmployeeImmigrationRequest(BaseRequest):
    """
    Request for creating an employee immigration record.
    """

    immigration_type: str = Field(
        min_length=1,
        max_length=50,
    )

    status: str = Field(
        min_length=1,
        max_length=30,
    )

    document_number: str | None = Field(
        default=None,
        max_length=100,
    )

    sponsor_name: str | None = Field(
        default=None,
        max_length=150,
    )

    issuing_authority: str | None = Field(
        default=None,
        max_length=150,
    )

    issue_date: date | None = None

    expiry_date: date | None = None

    notes: str | None = None