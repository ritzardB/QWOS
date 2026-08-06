"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    update_role_request.py

Description:
    Request contract for updating a role.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class UpdateRoleRequest(BaseRequest):
    """
    Request for updating a role.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )
