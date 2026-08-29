"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    link_employee_to_user_command.py

Description:
    Command representing the intention to link an employee to a QWOS user
    and create the corresponding user profile.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinkEmployeeToUserCommand:
    """
    Command for linking an employee to a QWOS user.
    """

    tenant_id: str
    employee_id: str
    user_id: str

    first_name: str
    last_name: str

    middle_name: str | None = None
    preferred_name: str | None = None
