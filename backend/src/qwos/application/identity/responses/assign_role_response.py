"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    assign_role_response.py

Description:
    Application response returned after assigning a role to a user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime


class AssignRoleResponse:
    """
    Response returned after assigning a role.
    """

    def __init__(
        self,
        *,
        id: str,
        user_id: str,
        role_id: str,
        is_primary: bool,
        is_enabled: bool,
        assigned_at: datetime,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.role_id = role_id
        self.is_primary = is_primary
        self.is_enabled = is_enabled
        self.assigned_at = assigned_at
