"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    assign_role_command.py

Description:
    Command representing the intention to assign a role to a user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssignRoleCommand:
    """
    Command for assigning a role to a user.
    """

    user_id: str
    role_id: str
