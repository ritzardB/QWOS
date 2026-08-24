"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Tests:
    Attendance Policy Resolution Service
===============================================================================
"""

from datetime import date

import pytest

from qwos.domains.attendance.models.attendance_policy import (
    AttendancePolicy,
)
from qwos.domains.attendance.services.attendance_policy_resolution_service import (
    AttendancePolicyResolutionService,
)

TENANT_ID = "01M0TEN00000000000000000001"
EMPLOYEE_ID = "01M0EMP00000000000000000001"


class FakeAttendancePolicyRepository:
    def __init__(self, policy: AttendancePolicy | None) -> None:
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
    def __init__(self, arrangement: str | None) -> None:
        self.arrangement = arrangement

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> str | None:
        return self.arrangement


class FakeWorkAgreement:
    def __init__(
        self,
        *,
        compensation_basis: str,
        pay_frequency: str,
    ) -> None:
        self.compensation_basis = compensation_basis
        self.pay_frequency = pay_frequency


class FakeWorkAgreementRepository:
    def __init__(
        self,
        agreement: FakeWorkAgreement | None,
    ) -> None:
        self.agreement = agreement

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> FakeWorkAgreement | None:
        return self.agreement


def build_service(
    *,
    policy: AttendancePolicy | None,
    arrangement: str | None = "office",
    compensation_basis: str = "monthly",
    pay_frequency: str = "monthly",
) -> AttendancePolicyResolutionService:

    agreement = (
        FakeWorkAgreement(
            compensation_basis=compensation_basis,
            pay_frequency=pay_frequency,
        )
        if arrangement is not None
        else None
    )

    return AttendancePolicyResolutionService(
        attendance_policy_repository=(
            FakeAttendancePolicyRepository(policy)
        ),
        work_arrangement_repository=(
            FakeWorkArrangementRepository(arrangement)
        ),
        work_agreement_repository=(
            FakeWorkAgreementRepository(agreement)
        ),
    )


def make_policy(
    *,
    requirement: str = "required",
    clock_in_required: bool = True,
    clock_out_required: bool = True,
    payroll_impact_enabled: bool = False,
    overtime_enabled: bool = False,
    undertime_enabled: bool = False,
    late_deduction_enabled: bool = False,
    grace_period_minutes: int = 0,
) -> AttendancePolicy:

    return AttendancePolicy.create(
        id="01M0ATP00000000000000000001",
        tenant_id=TENANT_ID,
        policy_code="TEST_POLICY",
        policy_name="Test Attendance Policy",
        attendance_requirement=requirement,
        clock_in_required=clock_in_required,
        clock_out_required=clock_out_required,
        payroll_impact_enabled=payroll_impact_enabled,
        overtime_enabled=overtime_enabled,
        undertime_enabled=undertime_enabled,
        late_deduction_enabled=late_deduction_enabled,
        grace_period_minutes=grace_period_minutes,
    )


def test_required_policy_resolves_clocking_rules() -> None:
    service = build_service(
        policy=make_policy(
            requirement="required",
            clock_in_required=True,
            clock_out_required=True,
        ),
    )

    context = service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=date(2026, 8, 24),
    )

    assert context.attendance_required is True
    assert context.clock_in_required is True
    assert context.clock_out_required is True


def test_not_required_policy_disables_clocking_requirement() -> None:
    service = build_service(
        policy=make_policy(
            requirement="not_required",
            clock_in_required=True,
            clock_out_required=True,
        ),
    )

    context = service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=date(2026, 8, 24),
    )

    assert context.attendance_required is False
    assert context.clock_in_required is False
    assert context.clock_out_required is False


def test_tracking_only_policy_tracks_without_forcing_payroll_impact() -> None:
    service = build_service(
        policy=make_policy(
            requirement="tracking_only",
            payroll_impact_enabled=False,
        ),
    )

    context = service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=date(2026, 8, 24),
    )

    assert context.attendance_required is True
    assert context.clock_in_required is True
    assert context.clock_out_required is True
    assert context.payroll_impact_enabled is False


def test_policy_payroll_rules_are_preserved() -> None:
    service = build_service(
        policy=make_policy(
            requirement="required",
            payroll_impact_enabled=True,
            overtime_enabled=True,
            undertime_enabled=True,
            late_deduction_enabled=True,
            grace_period_minutes=15,
        ),
    )

    context = service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=date(2026, 8, 24),
    )

    assert context.payroll_impact_enabled is True
    assert context.overtime_enabled is True
    assert context.undertime_enabled is True
    assert context.late_deduction_enabled is True
    assert context.grace_period_minutes == 15


@pytest.mark.parametrize(
    "arrangement",
    [
        "office",
        "remote",
        "hybrid",
    ],
)
def test_work_arrangement_is_preserved(
    arrangement: str,
) -> None:
    service = build_service(
        policy=make_policy(),
        arrangement=arrangement,
    )

    context = service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=date(2026, 8, 24),
    )

    assert context.work_arrangement == arrangement


def test_work_agreement_is_preserved() -> None:
    service = build_service(
        policy=make_policy(),
        compensation_basis="daily",
        pay_frequency="biweekly",
    )

    context = service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=date(2026, 8, 24),
    )

    assert context.compensation_basis == "daily"
    assert context.pay_frequency == "biweekly"


def test_missing_policy_raises_lookup_error() -> None:
    service = build_service(
        policy=None,
    )

    with pytest.raises(LookupError, match="attendance policy"):
        service.resolve(
            tenant_id=TENANT_ID,
            employee_id=EMPLOYEE_ID,
            effective_date=date(2026, 8, 24),
        )


def test_missing_work_arrangement_raises_lookup_error() -> None:
    service = build_service(
        policy=make_policy(),
        arrangement=None,
    )

    with pytest.raises(LookupError, match="work arrangement"):
        service.resolve(
            tenant_id=TENANT_ID,
            employee_id=EMPLOYEE_ID,
            effective_date=date(2026, 8, 24),
        )


def test_missing_work_agreement_raises_lookup_error() -> None:
    class MissingAgreementRepository:
        def get_effective_for_employee(
            self,
            *,
            tenant_id: str,
            employee_id: str,
            effective_date: date,
        ) -> None:
            return None

    service = AttendancePolicyResolutionService(
        attendance_policy_repository=(
            FakeAttendancePolicyRepository(
                make_policy(),
            )
        ),
        work_arrangement_repository=(
            FakeWorkArrangementRepository(
                "office",
            )
        ),
        work_agreement_repository=(
            MissingAgreementRepository()
        ),
    )

    with pytest.raises(LookupError, match="work agreement"):
        service.resolve(
            tenant_id=TENANT_ID,
            employee_id=EMPLOYEE_ID,
            effective_date=date(2026, 8, 24),
        )


@pytest.mark.parametrize(
    "tenant_id,employee_id",
    [
        ("", EMPLOYEE_ID),
        (TENANT_ID, ""),
    ],
)
def test_invalid_identity_inputs_raise_value_error(
    tenant_id: str,
    employee_id: str,
) -> None:
    service = build_service(
        policy=make_policy(),
    )

    with pytest.raises(ValueError):
        service.resolve(
            tenant_id=tenant_id,
            employee_id=employee_id,
            effective_date=date(2026, 8, 24),
        )