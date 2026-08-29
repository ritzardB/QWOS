"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_policy.py

Description:
    SQLAlchemy model representing an attendance policy.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class AttendancePolicy(TenantEntity):
    """
    Defines attendance requirements and payroll-related attendance behavior
    for employees within a tenant.
    """

    __tablename__ = "attendance_policies"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "attendance_requirement",
            "required",
        )
        kwargs.setdefault(
            "clock_in_required",
            True,
        )
        kwargs.setdefault(
            "clock_out_required",
            True,
        )
        kwargs.setdefault(
            "payroll_impact_enabled",
            False,
        )
        kwargs.setdefault(
            "overtime_enabled",
            False,
        )
        kwargs.setdefault(
            "undertime_enabled",
            False,
        )
        kwargs.setdefault(
            "late_deduction_enabled",
            False,
        )
        kwargs.setdefault(
            "grace_period_minutes",
            0,
        )
        kwargs.setdefault(
            "is_active",
            True,
        )

        super().__init__(**kwargs)

    # -------------------------------------------------------------------------
    # Factory
    # -------------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        policy_code: str,
        policy_name: str,
        attendance_requirement: str = "required",
        clock_in_required: bool = True,
        clock_out_required: bool = True,
        payroll_impact_enabled: bool = False,
        overtime_enabled: bool = False,
        undertime_enabled: bool = False,
        late_deduction_enabled: bool = False,
        grace_period_minutes: int = 0,
        created_by: str | None = None,
    ) -> "AttendancePolicy":
        """
        Create a normalized attendance policy.
        """

        normalized_code = policy_code.strip().lower()

        normalized_name = policy_name.strip()

        normalized_requirement = attendance_requirement.strip().lower()

        if not normalized_code:
            raise ValueError(
                "policy_code is required.",
            )

        if not normalized_name:
            raise ValueError(
                "policy_name is required.",
            )

        if normalized_requirement not in {
            "not_required",
            "tracking_only",
            "required",
        }:
            raise ValueError(
                "attendance_requirement must be one of: not_required, tracking_only, required.",
            )

        if grace_period_minutes < 0:
            raise ValueError(
                "grace_period_minutes cannot be negative.",
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            policy_code=normalized_code,
            policy_name=normalized_name,
            attendance_requirement=(normalized_requirement),
            clock_in_required=clock_in_required,
            clock_out_required=clock_out_required,
            payroll_impact_enabled=(payroll_impact_enabled),
            overtime_enabled=overtime_enabled,
            undertime_enabled=undertime_enabled,
            late_deduction_enabled=(late_deduction_enabled),
            grace_period_minutes=(grace_period_minutes),
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Policy Identity
    # -------------------------------------------------------------------------

    policy_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    policy_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Attendance Requirement
    # -------------------------------------------------------------------------

    attendance_requirement: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="required",
    )

    # -------------------------------------------------------------------------
    # Clocking Requirements
    # -------------------------------------------------------------------------

    clock_in_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    clock_out_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # -------------------------------------------------------------------------
    # Payroll Impact
    # -------------------------------------------------------------------------

    payroll_impact_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    overtime_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    undertime_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    late_deduction_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # -------------------------------------------------------------------------
    # Attendance Tolerance
    # -------------------------------------------------------------------------

    grace_period_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
