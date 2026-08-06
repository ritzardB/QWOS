"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    revoke_permission_request.py

Description:
    Request contract for revoking a permission from a role.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.common.base_request import BaseRequest


class RevokePermissionRequest(BaseRequest):
    """
    Revoke a permission from a role.
    """

    role_id: str

    permission_id: str
