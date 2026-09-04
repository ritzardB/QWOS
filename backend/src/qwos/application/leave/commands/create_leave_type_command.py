"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Create Leave Type Command

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateLeaveTypeCommand:
    """
    Command for creating a tenant leave type.
    """

    tenant_id: str
    leave_code: str
    leave_name: str
    description: str | None = None
    is_paid: bool = True
    is_active: bool = True