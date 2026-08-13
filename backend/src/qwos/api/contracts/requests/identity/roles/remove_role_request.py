"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    remove_role_request.py

Description:
    Request contract for removing a role from a user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.common.base_request import BaseRequest


class RemoveRoleRequest(BaseRequest):
    """
    Remove a role from a user.
    """

    user_id: str

    role_id: str
