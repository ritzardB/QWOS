"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    grant_permission_request.py

Description:
    Request contract for granting a permission to a role.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.core.contracts.requests.common.base_request import BaseRequest


class GrantPermissionRequest(BaseRequest):
    """
    Grant a permission to a role.
    """

    role_id: str

    permission_id: str
