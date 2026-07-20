"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    create_role_request.py

Description:
    Request contract for creating a role.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import Field

from qwos.core.contracts.requests.common.base_request import BaseRequest


class CreateRoleRequest(BaseRequest):
    """
    Request for creating a role.
    """

    code: str = Field(
        min_length=2,
        max_length=50,
    )

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    is_system: bool = False
