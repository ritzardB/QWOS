"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    user_profile_response.py

Description:
    Response contract representing a user profile.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import EmailStr

from qwos.api.contracts.responses.common.base_response import BaseResponse


class UserProfileResponse(BaseResponse):
    """
    User profile response.
    """

    id: str

    user_id: str

    first_name: str

    middle_name: str | None

    last_name: str

    preferred_name: str | None

    mobile_number: str | None

    alternate_email: EmailStr | None

    birth_date: date | None

    created_at: datetime

    updated_at: datetime | None
