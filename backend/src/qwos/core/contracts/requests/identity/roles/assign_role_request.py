"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    assign_role_request.py

Description:
    Request contract for assigning a role to a user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.core.contracts.requests.common.base_request import BaseRequest


class AssignRoleRequest(BaseRequest):
    """
    Assign a role to a user.
    """

    user_id: str

    role_id: str
