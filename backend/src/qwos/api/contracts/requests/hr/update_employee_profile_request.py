from __future__ import annotations

from datetime import date

from pydantic import EmailStr, Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class UpdateEmployeeProfileRequest(BaseRequest):
    """
    Request for updating an employee profile.
    """

    date_of_birth: date | None = None

    gender: str | None = Field(
        default=None,
        max_length=50,
    )

    nationality: str | None = Field(
        default=None,
        max_length=50,
    )

    marital_status: str | None = Field(
        default=None,
        max_length=50,
    )

    personal_email: EmailStr | None = None

    personal_phone: str | None = Field(
        default=None,
        max_length=30,
    )

    address_line_1: str | None = None
    address_line_2: str | None = None

    city: str | None = Field(
        default=None,
        max_length=150,
    )

    state_province: str | None = Field(
        default=None,
        max_length=150,
    )

    postal_code: str | None = Field(
        default=None,
        max_length=30,
    )

    country_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )

    emergency_contact_name: str | None = Field(
        default=None,
        max_length=100,
    )

    emergency_contact_relationship: str | None = Field(
        default=None,
        max_length=50,
    )

    emergency_contact_phone: str | None = Field(
        default=None,
        max_length=30,
    )
