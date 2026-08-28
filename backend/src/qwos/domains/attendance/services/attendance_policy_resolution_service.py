"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_policy_resolution_service.py

Description:
    Resolves the effective attendance policy and work arrangement for an
    employee on a specific date.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol

from qwos.domains.attendance.models.attendance_policy import (
    AttendancePolicy,
)

# =============================================================================
# Resolved Attendance Context
# =============================================================================


@dataclass(frozen=True)
class ResolvedAttendanceContext:
    """
    Effective attendance configuration for an employee on a specific date.

    This object represents the result of attendance policy resolution.

    It does not perform attendance calculations.
    """

    tenant_id: str
    employee_id: str
    effective_date: date

    attendance_policy: AttendancePolicy

    work_arrangement: str
    compensation_basis: str
    pay_frequency: str

    attendance_required: bool
    clock_in_required: bool
    clock_out_required: bool

    payroll_impact_enabled: bool
    overtime_enabled: bool
    undertime_enabled: bool
    late_deduction_enabled: bool

    grace_period_minutes: int


# =============================================================================
# Repository Contracts
# =============================================================================


class AttendancePolicyAssignmentRepository(Protocol):
    """
    Contract required to resolve an employee's effective attendance policy.
    """

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> AttendancePolicy | None:
        """
        Retrieve the effective attendance policy assignment.

        Implementations should return None when no policy assignment
        exists for the employee on the requested date.
        """
        ...


class WorkArrangementRepository(Protocol):
    """
    Contract required to resolve an employee's work arrangement.
    """

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> str | None:
        """
        Retrieve the effective work arrangement.

        Expected values include:

            office
            remote
            hybrid
        """
        ...
class WorkAgreementRepository(Protocol):
    """
    Contract required to resolve an employee's effective work agreement.
    """

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> object:
        """
        Retrieve the effective employee work agreement.

        The returned object is expected to expose:

            compensation_basis
            pay_frequency
        """
        ...

# =============================================================================
# Service
# =============================================================================


class AttendancePolicyResolutionService:
    """
    Resolves the effective attendance rules for an employee.

    Resolution is date-sensitive.

    The service combines:

        Employee Attendance Policy
        +
        Employee Work Arrangement

    into a single immutable attendance context.

    This service does not:

        • create attendance records
        • create attendance events
        • calculate worked minutes
        • calculate overtime
        • calculate undertime
        • calculate late minutes
        • perform payroll calculations
    """

    def __init__(
        self,
        *,
        attendance_policy_repository: AttendancePolicyAssignmentRepository,
        work_arrangement_repository: WorkArrangementRepository,
        work_agreement_repository: WorkAgreementRepository,
    ) -> None:
        self._attendance_policy_repository = (
            attendance_policy_repository
        )

        self._work_arrangement_repository = (
            work_arrangement_repository
        )

        self._work_agreement_repository = (
            work_agreement_repository
        )

    # -------------------------------------------------------------------------
    # Resolution
    # -------------------------------------------------------------------------

    def resolve(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> ResolvedAttendanceContext:
        """
        Resolve the effective attendance configuration.

        Args:
            tenant_id:
                Tenant owning the employee.

            employee_id:
                Employee whose attendance rules are being resolved.

            effective_date:
                Date for which the rules must apply.

        Returns:
            ResolvedAttendanceContext.

        Raises:
            ValueError:
                When tenant_id, employee_id, or effective_date is invalid.

            LookupError:
                When an effective policy or work arrangement cannot
                be resolved.
        """

        self._validate_inputs(
            tenant_id=tenant_id,
            employee_id=employee_id,
            effective_date=effective_date,
        )

        policy = self._attendance_policy_repository.get_effective_for_employee(
            tenant_id=tenant_id,
            employee_id=employee_id,
            effective_date=effective_date,
        )

        if policy is None:
            raise LookupError(
                f"No effective attendance policy found for employee '{employee_id}' on {effective_date}.",
            )

        work_arrangement = self._work_arrangement_repository.get_effective_for_employee(
            tenant_id=tenant_id,
            employee_id=employee_id,
            effective_date=effective_date,
        )

        if not work_arrangement:
            raise LookupError(
                f"No effective work arrangement found for employee '{employee_id}' on {effective_date}.",
            )

        work_agreement = (
            self._work_agreement_repository
            .get_effective_for_employee(
                tenant_id=tenant_id,
                employee_id=employee_id,
                effective_date=effective_date,
            )
        )

        if work_agreement is None:
            raise LookupError(
                "No effective work agreement found for "
                f"employee '{employee_id}' on {effective_date}."
            )

        attendance_required = (
            policy.attendance_requirement != "not_required"
        )

        return ResolvedAttendanceContext(
            tenant_id=tenant_id,
            employee_id=employee_id,
            effective_date=effective_date,
            attendance_policy=policy,
            work_arrangement=(
                work_arrangement.strip().lower()
            ),
            compensation_basis=(
                self._normalize_required_value(
                    work_agreement.compensation_basis,
                    "compensation_basis",
                )
            ),
            pay_frequency=(
                self._normalize_required_value(
                    work_agreement.pay_frequency,
                    "pay_frequency",
                )
            ),
            attendance_required=attendance_required,
            clock_in_required=(
                attendance_required
                and policy.clock_in_required
            ),
            clock_out_required=(
                attendance_required
                and policy.clock_out_required
            ),
            payroll_impact_enabled=(
                policy.payroll_impact_enabled
            ),
            overtime_enabled=policy.overtime_enabled,
            undertime_enabled=policy.undertime_enabled,
            late_deduction_enabled=(
                policy.late_deduction_enabled
            ),
            grace_period_minutes=(
                policy.grace_period_minutes
            ),
        )

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    @staticmethod
    def _validate_inputs(
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> None:
        """
        Validate service inputs.
        """

        if not tenant_id.strip():
            raise ValueError(
                "tenant_id is required.",
            )

        if not employee_id.strip():
            raise ValueError(
                "employee_id is required.",
            )

        if not isinstance(effective_date, date):
            raise ValueError(
                "effective_date must be a date.",
        )

    # -------------------------------------------------------------------------
    # Normalize value
    # -------------------------------------------------------------------------

    @staticmethod
    def _normalize_required_value(
        value: str | None,
        field_name: str,
    ) -> str:
        """
        Normalize a required string value.
        """

        if value is None:
            raise ValueError(
                f"{field_name} is required.",
            )

        normalized = value.strip().lower()

        if not normalized:
            raise ValueError(
                f"{field_name} is required.",
            )

        return normalized