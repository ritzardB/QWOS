"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_employee_leave_balance_use_case.py

Description:
    Unit tests for CreateEmployeeLeaveBalanceUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.results.create_employee_leave_balance_validator import (
    CreateEmployeeLeaveBalanceValidator,
)
from qwos.application.leave.commands.create_employee_leave_balance_command import (
    CreateEmployeeLeaveBalanceCommand,
)
from qwos.application.leave.use_cases.create_employee_leave_balance_use_case import (
    CreateEmployeeLeaveBalanceUseCase,
)

TENANT_ID = "01M0TEN00000000000000000001"
USER_ID = "01M0USR00000000000000000001"
EMPLOYEE_ID = "01M0EMP00000000000000000001"
ASSIGNMENT_ID = "01M0ELA00000000000000000001"
BALANCE_ID = "01M0ELB00000000000000000001"


class FakeRepository:
    def __init__(self) -> None:
        self.save_calls: list[object] = []
        self.exists_result = False

    def exists_by_assignment_and_period(
        self,
        *,
        tenant_id: str,
        employee_leave_assignment_id: str,
        period_start: date,
        period_end: date,
    ) -> bool:
        return self.exists_result

    def save(self, entity: object) -> None:
        self.save_calls.append(entity)


class FakeIdGenerator:
    def generate(self) -> str:
        return BALANCE_ID


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.entered = False
        self.exited = False
        self.flush_called = False

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.exited = True

    def flush(self) -> None:
        self.flush_called = True


def make_request_context() -> RequestContext:
    return RequestContext(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )


def make_command(
    *,
    tenant_id: str = TENANT_ID,
    employee_id: str = EMPLOYEE_ID,
    employee_leave_assignment_id: str = ASSIGNMENT_ID,
    period_start: date = date(2026, 1, 1),
    period_end: date = date(2026, 12, 31),
    entitlement_days: Decimal = Decimal("24.00"),
    carried_forward_days: Decimal = Decimal("2.00"),
    accrued_days: Decimal = Decimal("10.50"),
    used_days: Decimal = Decimal("5.50"),
    adjustment_days: Decimal = Decimal("1.00"),
    is_active: bool = True,
) -> CreateEmployeeLeaveBalanceCommand:
    return CreateEmployeeLeaveBalanceCommand(
        tenant_id=tenant_id,
        employee_leave_assignment_id=employee_leave_assignment_id,
        employee_id=employee_id,
        period_start=period_start,
        period_end=period_end,
        entitlement_days=entitlement_days,
        carried_forward_days=carried_forward_days,
        accrued_days=accrued_days,
        used_days=used_days,
        adjustment_days=adjustment_days,
        is_active=is_active,
    )


def make_use_case() -> tuple[
    CreateEmployeeLeaveBalanceUseCase,
    FakeRepository,
    FakeIdGenerator,
    FakeUnitOfWork,
]:
    repository = FakeRepository()
    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    use_case = CreateEmployeeLeaveBalanceUseCase(
        employee_leave_balance_repository=repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=CreateEmployeeLeaveBalanceValidator(),
        request_context=make_request_context(),
    )

    return (
        use_case,
        repository,
        id_generator,
        unit_of_work,
    )


@pytest.mark.asyncio
async def test_create_employee_leave_balance_successfully() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(),
    )

    assert response.id == BALANCE_ID
    assert response.employee_leave_assignment_id == ASSIGNMENT_ID
    assert response.employee_id == EMPLOYEE_ID
    assert response.period_start == date(2026, 1, 1)
    assert response.period_end == date(2026, 12, 31)
    assert response.entitlement_days == Decimal("24.00")
    assert response.carried_forward_days == Decimal("2.00")
    assert response.accrued_days == Decimal("10.50")
    assert response.used_days == Decimal("5.50")
    assert response.adjustment_days == Decimal("1.00")
    assert response.is_active is True

    assert len(repository.save_calls) == 1
    assert unit_of_work.entered is True
    assert unit_of_work.exited is True
    assert unit_of_work.flush_called is True


@pytest.mark.asyncio
async def test_create_employee_leave_balance_allows_negative_adjustment() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            adjustment_days=Decimal("-3.50"),
        ),
    )

    assert response.adjustment_days == Decimal("-3.50")

    saved_balance = repository.save_calls[0]

    assert saved_balance.adjustment_days == Decimal("-3.50")


@pytest.mark.asyncio
async def test_create_employee_leave_balance_allows_same_period_start_and_end() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            period_start=date(2026, 9, 1),
            period_end=date(2026, 9, 1),
        ),
    )

    assert response.period_start == date(2026, 9, 1)
    assert response.period_end == date(2026, 9, 1)


@pytest.mark.asyncio
async def test_create_employee_leave_balance_allows_inactive_balance() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            is_active=False,
        ),
    )

    assert response.is_active is False

    saved_balance = repository.save_calls[0]

    assert saved_balance.is_active is False


@pytest.mark.asyncio
async def test_create_employee_leave_balance_rejects_duplicate_assignment_period() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    repository.exists_result = True

    with pytest.raises(DuplicateResourceException):
        await use_case.execute(
            make_command(),
        )

    assert repository.save_calls == []
    assert unit_of_work.entered is False
    assert unit_of_work.flush_called is False


@pytest.mark.asyncio
async def test_create_employee_leave_balance_rejects_invalid_period() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                period_start=date(2026, 12, 31),
                period_end=date(2026, 1, 1),
            ),
        )

    assert repository.save_calls == []
    assert unit_of_work.entered is False
    assert unit_of_work.flush_called is False