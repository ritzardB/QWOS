"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Employee Work Agreement Repository Tests
===============================================================================
"""

from datetime import date

import pytest

from qwos.domains.attendance.models import EmployeeWorkAgreement

TENANT_ID = "01M0TEN00000000000000000001"
OTHER_TENANT_ID = "01M0TEN00000000000000000002"
EMPLOYEE_ID = "01M0EMP00000000000000000001"


def make_agreement(
    *,
    agreement_id: str = "01M0EWA00000000000000000001",
    tenant_id: str = TENANT_ID,
    employee_id: str = EMPLOYEE_ID,
    effective_from: date = date(2026, 8, 1),
    effective_until: date | None = None,
    compensation_basis: str = "monthly",
    pay_frequency: str = "monthly",
    is_active: bool = True,
) -> EmployeeWorkAgreement:
    return EmployeeWorkAgreement.create(
        id=agreement_id,
        tenant_id=tenant_id,
        employee_id=employee_id,
        compensation_basis=compensation_basis,
        pay_frequency=pay_frequency,
        effective_from=effective_from,
        effective_until=effective_until,
        is_active=is_active,
    )


def test_create_open_ended_agreement() -> None:
    agreement = make_agreement()

    assert agreement.employee_id == EMPLOYEE_ID
    assert agreement.compensation_basis == "monthly"
    assert agreement.pay_frequency == "monthly"
    assert agreement.effective_from == date(2026, 8, 1)
    assert agreement.effective_until is None
    assert agreement.is_active is True


@pytest.mark.parametrize(
    "compensation_basis",
    [
        "hourly",
        "daily",
        "monthly",
    ],
)
def test_create_supported_compensation_basis(
    compensation_basis: str,
) -> None:
    agreement = make_agreement(
        compensation_basis=compensation_basis,
    )

    assert agreement.compensation_basis == compensation_basis


@pytest.mark.parametrize(
    "pay_frequency",
    [
        "weekly",
        "biweekly",
        "semimonthly",
        "monthly",
    ],
)
def test_create_supported_pay_frequency(
    pay_frequency: str,
) -> None:
    agreement = make_agreement(
        pay_frequency=pay_frequency,
    )

    assert agreement.pay_frequency == pay_frequency


def test_compensation_basis_is_normalized() -> None:
    agreement = make_agreement(
        compensation_basis="  DAILY  ",
    )

    assert agreement.compensation_basis == "daily"


def test_pay_frequency_is_normalized() -> None:
    agreement = make_agreement(
        pay_frequency="  BIWEEKLY  ",
    )

    assert agreement.pay_frequency == "biweekly"


def test_effective_until_can_be_defined() -> None:
    agreement = make_agreement(
        effective_until=date(2026, 8, 31),
    )

    assert agreement.effective_until == date(2026, 8, 31)


def test_agreement_is_tenant_scoped() -> None:
    agreement = make_agreement(
        tenant_id=OTHER_TENANT_ID,
    )

    assert agreement.tenant_id == OTHER_TENANT_ID


def test_inactive_agreement_can_be_created() -> None:
    agreement = make_agreement(
        is_active=False,
    )

    assert agreement.is_active is False


def test_effective_date_boundary_is_inclusive() -> None:
    agreement = make_agreement(
        effective_from=date(2026, 8, 1),
        effective_until=date(2026, 8, 31),
    )

    assert agreement.effective_from <= date(2026, 8, 1)
    assert agreement.effective_until >= date(2026, 8, 31)


def test_effective_date_range_is_valid() -> None:
    agreement = make_agreement(
        effective_from=date(2026, 8, 1),
        effective_until=date(2026, 8, 31),
    )

    assert agreement.effective_until >= agreement.effective_from


def test_effective_until_cannot_be_before_effective_from() -> None:
    with pytest.raises(
        ValueError,
        match="effective_until cannot be earlier than effective_from",
    ):
        make_agreement(
            effective_from=date(2026, 8, 31),
            effective_until=date(2026, 8, 1),
        )


def test_missing_compensation_basis_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="compensation_basis is required",
    ):
        make_agreement(
            compensation_basis="",
        )


def test_invalid_compensation_basis_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="compensation_basis must be one of",
    ):
        make_agreement(
            compensation_basis="annual",
        )


def test_missing_pay_frequency_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="pay_frequency is required",
    ):
        make_agreement(
            pay_frequency="",
        )


def test_invalid_pay_frequency_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="pay_frequency must be one of",
    ):
        make_agreement(
            pay_frequency="daily",
        )