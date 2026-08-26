"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Employee Work Arrangement Repository Tests
===============================================================================
"""

from datetime import date

from qwos.domains.attendance.models import EmployeeWorkArrangement

TENANT_ID = "01M0TEN00000000000000000001"
OTHER_TENANT_ID = "01M0TEN00000000000000000002"
EMPLOYEE_ID = "01M0EMP00000000000000000001"


def make_arrangement(
    *,
    arrangement_id: str = "01M0EWA00000000000000000001",
    tenant_id: str = TENANT_ID,
    employee_id: str = EMPLOYEE_ID,
    effective_from: date = date(2026, 8, 1),
    effective_until: date | None = None,
    work_arrangement: str = "office",
    is_active: bool = True,
) -> EmployeeWorkArrangement:
    return EmployeeWorkArrangement.create(
        id=arrangement_id,
        tenant_id=tenant_id,
        employee_id=employee_id,
        work_arrangement=work_arrangement,
        effective_from=effective_from,
        effective_until=effective_until,
        is_active=is_active,
    )


def test_create_open_ended_arrangement() -> None:
    arrangement = make_arrangement()

    assert arrangement.employee_id == EMPLOYEE_ID
    assert arrangement.work_arrangement == "office"
    assert arrangement.effective_from == date(2026, 8, 1)
    assert arrangement.effective_until is None
    assert arrangement.is_active is True


def test_create_hybrid_arrangement() -> None:
    arrangement = make_arrangement(
        work_arrangement="hybrid",
    )

    assert arrangement.work_arrangement == "hybrid"


def test_create_remote_arrangement() -> None:
    arrangement = make_arrangement(
        work_arrangement="remote",
    )

    assert arrangement.work_arrangement == "remote"


def test_effective_until_can_be_defined() -> None:
    arrangement = make_arrangement(
        effective_until=date(2026, 8, 31),
    )

    assert arrangement.effective_until == date(2026, 8, 31)


def test_arrangement_is_tenant_scoped() -> None:
    arrangement = make_arrangement(
        tenant_id=OTHER_TENANT_ID,
    )

    assert arrangement.tenant_id == OTHER_TENANT_ID


def test_inactive_arrangement_can_be_created() -> None:
    arrangement = make_arrangement(
        is_active=False,
    )

    assert arrangement.is_active is False


def test_effective_date_boundary_is_inclusive() -> None:
    arrangement = make_arrangement(
        effective_from=date(2026, 8, 1),
        effective_until=date(2026, 8, 31),
    )

    assert arrangement.effective_from <= date(2026, 8, 1)
    assert arrangement.effective_until >= date(2026, 8, 31)


def test_effective_date_range_is_valid() -> None:
    arrangement = make_arrangement(
        effective_from=date(2026, 8, 1),
        effective_until=date(2026, 8, 31),
    )

    assert arrangement.effective_until >= arrangement.effective_from
