"""
===============================================================================
Quantum Workforce OS (QWOS)

Domain Layer

Leave Type Repository

Author:
    Richard Balabarcon
===============================================================================
"""

from typing import Protocol

from qwos.domains.leave.models.leave_type import LeaveType


class LeaveTypeRepository(Protocol):
    def get_by_id(
        self,
        leave_type_id: str,
    ) -> LeaveType | None:
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        leave_type_id: str,
    ) -> LeaveType | None:
        ...

    def save(
        self,
        leave_type: LeaveType,
    ) -> None:
        ...

    def list_by_tenant(
        self,
        *,
        tenant_id: str,
    ) -> list[LeaveType]:
        ...

    def get_active_by_code(
        self,
        *,
        tenant_id: str,
        leave_code: str,
    ) -> LeaveType | None:
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: str,
        leave_code: str,
    ) -> bool:
        ...