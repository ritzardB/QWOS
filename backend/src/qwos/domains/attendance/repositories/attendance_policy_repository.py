"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Attendance Policy Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.attendance.models.attendance_policy import (
    AttendancePolicy,
)


class AttendancePolicyRepository(Protocol):
    """
    Contract for AttendancePolicy persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        attendance_policy_id: str,
    ) -> AttendancePolicy | None:
        """
        Retrieve an attendance policy by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        attendance_policy_id: str,
    ) -> AttendancePolicy | None:
        """
        Retrieve a non-deleted attendance policy within a tenant.
        """
        ...

    def save(
        self,
        attendance_policy: AttendancePolicy,
    ) -> None:
        """
        Persist an attendance policy.
        """
        ...

    # -------------------------------------------------------------------------
    # Attendance Policy Queries
    # -------------------------------------------------------------------------

    def get_by_policy_code(
        self,
        *,
        tenant_id: str,
        policy_code: str,
    ) -> AttendancePolicy | None:
        """
        Retrieve an attendance policy by tenant-scoped policy code.
        """
        ...

    def list_active(
        self,
        *,
        tenant_id: str,
    ) -> list[AttendancePolicy]:
        """
        Retrieve active attendance policies for a tenant.
        """
        ...

    def exists_by_policy_code(
        self,
        *,
        tenant_id: str,
        policy_code: str,
    ) -> bool:
        """
        Determine whether a policy code already exists for a tenant.
        """
        ...
