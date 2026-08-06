"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    create_permission_request.py

Description:
    Request contract for creating a permission.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreatePermissionRequest(BaseRequest):
    """
    Request for creating a permission.
    """

    code: str = Field(
        min_length=2,
        max_length=100,
    )

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    module: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )
