"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Tests:
    attendance_policy_resolution_service.py
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pytest

from qwos.domains.attendance.models.attendance_policy import (
    AttendancePolicy,
)
from qwos.domains.attendance.services.attendance_policy_resolution_service import (
    AttendancePolicyResolutionService,
)

EFFECTIVE_DATE = date(2026, 9, 15)


@dataclass
class FakeWorkAgreement:
    compensation_basis: str | None = "monthly"
    pay_frequency: str | None = "monthly"


class FakeAttendancePolicyRepository:
    def __init__(
        self,
        policy: AttendancePolicy | None = None,
    ) -> None:
        self.policy = policy

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> AttendancePolicy | None:
        return self.policy


class FakeWorkArrangementRepository:
    def __init__(
        self,
        work_arrangement: str | None = "office",
    ) -> None:
        self.work_arrangement = work_arrangement

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> str | None:
        return self.work_arrangement


class FakeWorkAgreementRepository:
    def __init__(
        self,
        work_agreement: FakeWorkAgreement | None = None,
    ) -> None:
        self.work_agreement = work_agreement

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> FakeWorkAgreement | None:
        return self.work_agreement


def make_policy(
    **overrides: object,
) -> AttendancePolicy:
    values: dict[str, object] = {
        "policy_code": "STANDARD",
        "policy_name": "Standard Attendance Policy",
        "attendance_requirement": "required",
        "clock_in_required": True,
        "clock_out_required": True,
        "payroll_impact_enabled": True,
        "overtime_enabled": True,
        "undertime_enabled": True,
        "late_deduction_enabled": True,
        "grace_period_minutes": 15,
    }

    values.update(overrides)

    return AttendancePolicy(**values)


def make_service(
    *,
    policy: AttendancePolicy | None = None,
    work_arrangement: str | None = "office",
    work_agreement: FakeWorkAgreement | None = None,
) -> AttendancePolicyResolutionService:
    return AttendancePolicyResolutionService(
        attendance_policy_repository=FakeAttendancePolicyRepository(
            policy=policy or make_policy(),
        ),
        work_arrangement_repository=FakeWorkArrangementRepository(
            work_arrangement=work_arrangement,
        ),
        work_agreement_repository=FakeWorkAgreementRepository(
            work_agreement=(
                work_agreement
                or FakeWorkAgreement()
            ),
        ),
    )


def test_resolve_returns_effective_attendance_context() -> None:
    service = make_service()

    result = service.resolve(
        tenant_id="tenant-001",
        employee_id="employee-001",
        effective_date=EFFECTIVE_DATE,
    )

    assert result.tenant_id == "tenant-001"
    assert result.employee_id == "employee-001"
    assert result.effective_date == EFFECTIVE_DATE
    assert result.work_arrangement == "office"
    assert result.compensation_basis == "monthly"
    assert result.pay_frequency == "monthly"


def test_resolve_sets_attendance_required() -> None:
    service = make_service(
        policy=make_policy(
            attendance_requirement="required",
        ),
    )

    result = service.resolve(
        tenant_id="tenant-001",
        employee_id="employee-001",
        effective_date=EFFECTIVE_DATE,
    )

    assert result.attendance_required is True


def test_resolve_disables_clock_requirements_when_attendance_not_required() -> None:
    policy = make_policy(
        attendance_requirement="not_required",
        clock_in_required=True,
        clock_out_required=True,
    )

    service = make_service(policy=policy)

    result = service.resolve(
        tenant_id="tenant-001",
        employee_id="employee-001",
        effective_date=EFFECTIVE_DATE,
    )

    assert result.attendance_required is False
    assert result.clock_in_required is False
    assert result.clock_out_required is False


def test_resolve_preserves_clock_requirements_when_attendance_required() -> None:
    policy = make_policy(
        attendance_requirement="required",
        clock_in_required=True,
        clock_out_required=True,
    )

    service = make_service(policy=policy)

    result = service.resolve(
        tenant_id="tenant-001",
        employee_id="employee-001",
        effective_date=EFFECTIVE_DATE,
    )

    assert result.clock_in_required is True
    assert result.clock_out_required is True


def test_resolve_normalizes_work_arrangement() -> None:
    service = make_service(
        work_arrangement="  REMOTE  ",
    )

    result = service.resolve(
        tenant_id="tenant-001",
        employee_id="employee-001",
        effective_date=EFFECTIVE_DATE,
    )

    assert result.work_arrangement == "remote"


def test_resolve_normalizes_work_agreement_values() -> None:
    service = make_service(
        work_agreement=FakeWorkAgreement(
            compensation_basis="  DAILY ",
            pay_frequency="  WEEKLY ",
        ),
    )

    result = service.resolve(
        tenant_id="tenant-001",
        employee_id="employee-001",
        effective_date=EFFECTIVE_DATE,
    )

    assert result.compensation_basis == "daily"
    assert result.pay_frequency == "weekly"


def test_resolve_raises_when_policy_is_missing() -> None:
    service = make_service(
        policy=None,
    )

    service._attendance_policy_repository.policy = None

    with pytest.raises(LookupError, match="No effective attendance policy"):
        service.resolve(
            tenant_id="tenant-001",
            employee_id="employee-001",
            effective_date=EFFECTIVE_DATE,
        )


def test_resolve_raises_when_work_arrangement_is_missing() -> None:
    service = make_service(
        work_arrangement=None,
    )

    with pytest.raises(LookupError, match="No effective work arrangement"):
        service.resolve(
            tenant_id="tenant-001",
            employee_id="employee-001",
            effective_date=EFFECTIVE_DATE,
        )


def test_resolve_raises_when_work_agreement_is_missing() -> None:
    service = make_service()

    service._work_agreement_repository.work_agreement = None

    with pytest.raises(LookupError, match="No effective work agreement"):
        service.resolve(
            tenant_id="tenant-001",
            employee_id="employee-001",
            effective_date=EFFECTIVE_DATE,
        )


@pytest.mark.parametrize(
    "tenant_id",
    [
        "",
        "   ",
    ],
)
def test_resolve_rejects_invalid_tenant_id(
    tenant_id: str,
) -> None:
    service = make_service()

    with pytest.raises(ValueError, match="tenant_id is required"):
        service.resolve(
            tenant_id=tenant_id,
            employee_id="employee-001",
            effective_date=EFFECTIVE_DATE,
        )


@pytest.mark.parametrize(
    "employee_id",
    [
        "",
        "   ",
    ],
)
def test_resolve_rejects_invalid_employee_id(
    employee_id: str,
) -> None:
    service = make_service()

    with pytest.raises(ValueError, match="employee_id is required"):
        service.resolve(
            tenant_id="tenant-001",
            employee_id=employee_id,
            effective_date=EFFECTIVE_DATE,
        )


def test_resolve_rejects_invalid_effective_date() -> None:
    service = make_service()

    with pytest.raises(ValueError, match="effective_date must be a date"):
        service.resolve(
            tenant_id="tenant-001",
            employee_id="employee-001",
            effective_date="2026-09-15",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("compensation_basis", None),
        ("compensation_basis", ""),
        ("compensation_basis", "   "),
        ("pay_frequency", None),
        ("pay_frequency", ""),
        ("pay_frequency", "   "),
    ],
)
def test_resolve_rejects_missing_required_work_agreement_value(
    field: str,
    value: str | None,
) -> None:
    work_agreement = FakeWorkAgreement()

    setattr(work_agreement, field, value)

    service = make_service(
        work_agreement=work_agreement,
    )

    with pytest.raises(
        ValueError,
        match=f"{field} is required",
    ):
        service.resolve(
            tenant_id="tenant-001",
            employee_id="employee-001",
            effective_date=EFFECTIVE_DATE,
        )


def test_resolve_exposes_policy_configuration() -> None:
    policy = make_policy(
        payroll_impact_enabled=False,
        overtime_enabled=False,
        undertime_enabled=False,
        late_deduction_enabled=False,
        grace_period_minutes=30,
    )

    service = make_service(policy=policy)

    result = service.resolve(
        tenant_id="tenant-001",
        employee_id="employee-001",
        effective_date=EFFECTIVE_DATE,
    )

    assert result.payroll_impact_enabled is False
    assert result.overtime_enabled is False
    assert result.undertime_enabled is False
    assert result.late_deduction_enabled is False
    assert result.grace_period_minutes == 30