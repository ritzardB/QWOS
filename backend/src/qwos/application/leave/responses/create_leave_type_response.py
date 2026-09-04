"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Create Leave Type Response

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateLeaveTypeResponse:
    """
    Response returned after creating a leave type.
    """

    id: str
    leave_code: str
    leave_name: str
    description: str | None
    is_paid: bool
    is_active: bool
    created_at: datetime