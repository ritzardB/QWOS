"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    role_response.py

Description:
    Response contract representing a role.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from qwos.api.contracts.responses.common.base_response import BaseResponse


class RoleResponse(BaseResponse):
    """
    Role response.
    """

    id: str

    tenant_id: str

    code: str

    name: str

    description: str | None

    is_system: bool

    is_active: bool

    created_at: datetime

    updated_at: datetime | None
