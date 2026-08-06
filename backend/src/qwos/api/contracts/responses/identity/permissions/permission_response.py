"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    permission_response.py

Description:
    Response contract representing a permission.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from qwos.api.contracts.responses.common.base_response import BaseResponse


class PermissionResponse(BaseResponse):
    """
    Permission response.
    """

    id: str

    tenant_id: str

    code: str

    name: str

    module: str

    description: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime | None
