"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Identity Module

File:
    assign_role_response.py

Description:
    API response returned after assigning a role.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AssignRoleResponse(BaseModel):
    """
    Role assignment response.
    """

    id: str
    user_id: str
    role_id: str
    is_primary: bool
    is_enabled: bool
    assigned_at: datetime
