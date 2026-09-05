"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_employee_leave_assignment_use_case.py

Description:
    Unit tests for CreateEmployeeLeaveAssignmentUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.results.create_employee_leave_assignment_validator import (
    CreateEmployeeLeaveAssignmentValidator,
)
from qwos.application.leave.commands.create_employee_leave_assignment_command import (
    CreateEmployeeLeaveAssignmentCommand,
)
from qwos.application.leave.use_cases.create_employee_leave_assignment_use_case import (
    CreateEmployeeLeaveAssignmentUseCase,
)

TENANT_ID = "01M0TEN00000000000000000001"
OTHER_TENANT_ID = "01M0TEN00000000000000000002"
USER_ID = "01M0USR00000000000000000001"
EMPLOYEE_ID = "01M0EMP00000000000000000001"
LEAVE_POLICY_ID = "01M0LP00000000000000000001"
ASSIGNMENT_ID = "01M0ELA00000000000000000001"


class FakeRepository:
    def __init__(self) -> None:
        self.save_calls: list[object] = []
        self.exists_result = False

    def exists_by_employee_and_start_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_from: date,
    ) -> bool:
        return self.exists_result

    def save(self, entity: object) -> None:
        self.save_calls.append(entity)


class FakeIdGenerator:
    def generate(self) -> str:
        return ASSIGNMENT_ID


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
    leave_policy_id: str = LEAVE_POLICY_ID,
    effective_from: date = date(2026, 9, 1),
    effective_until: date | None = date(2026, 12, 31),
    is_active: bool = True,
) -> CreateEmployeeLeaveAssignmentCommand:
    return CreateEmployeeLeaveAssignmentCommand(
        tenant_id=tenant_id,
        employee_id=employee_id,
        leave_policy_id=leave_policy_id,
        effective_from=effective_from,
        effective_until=effective_until,
        is_active=is_active,
    )


def make_use_case() -> tuple[
    CreateEmployeeLeaveAssignmentUseCase,
    FakeRepository,
    FakeIdGenerator,
    FakeUnitOfWork,
]:
    repository = FakeRepository()
    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    use_case = CreateEmployeeLeaveAssignmentUseCase(
        employee_leave_assignment_repository=repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=CreateEmployeeLeaveAssignmentValidator(),
        request_context=make_request_context(),
    )

    return (
        use_case,
        repository,
        id_generator,
        unit_of_work,
    )


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_successfully() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(),
    )

    assert response.id == ASSIGNMENT_ID
    assert response.employee_id == EMPLOYEE_ID
    assert response.leave_policy_id == LEAVE_POLICY_ID
    assert response.effective_from == date(2026, 9, 1)
    assert response.effective_until == date(2026, 12, 31)
    assert response.is_active is True

    assert len(repository.save_calls) == 1
    assert unit_of_work.entered is True
    assert unit_of_work.exited is True
    assert unit_of_work.flush_called is True


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_allows_open_ended_assignment() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            effective_until=None,
        ),
    )

    assert response.effective_until is None

    saved_assignment = repository.save_calls[0]

    assert saved_assignment.effective_until is None


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_allows_same_start_and_end_date() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            effective_from=date(2026, 9, 1),
            effective_until=date(2026, 9, 1),
        ),
    )

    assert response.effective_from == date(2026, 9, 1)
    assert response.effective_until == date(2026, 9, 1)


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_allows_inactive_assignment() -> None:
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

    saved_assignment = repository.save_calls[0]

    assert saved_assignment.is_active is False


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_rejects_duplicate_start_date() -> None:
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
async def test_create_employee_leave_assignment_rejects_missing_employee_id() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                employee_id="   ",
            ),
        )

    assert repository.save_calls == []
    assert unit_of_work.entered is False


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_rejects_missing_leave_policy_id() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                leave_policy_id="   ",
            ),
        )

    assert repository.save_calls == []
    assert unit_of_work.entered is False


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_rejects_invalid_date_range() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                effective_from=date(2026, 12, 31),
                effective_until=date(2026, 9, 1),
            ),
        )

    assert repository.save_calls == []
    assert unit_of_work.entered is False


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_uses_generated_id() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(),
    )

    assert response.id == ASSIGNMENT_ID

    saved_assignment = repository.save_calls[0]

    assert saved_assignment.id == ASSIGNMENT_ID


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_sets_audit_user() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    saved_assignment = repository.save_calls[0]

    assert saved_assignment.created_by == USER_ID
    assert saved_assignment.updated_by == USER_ID


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_preserves_tenant() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(
            tenant_id=OTHER_TENANT_ID,
        ),
    )

    saved_assignment = repository.save_calls[0]

    assert saved_assignment.tenant_id == OTHER_TENANT_ID


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_preserves_employee_id() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(
            employee_id="01M0EMP00000000000000000099",
        ),
    )

    saved_assignment = repository.save_calls[0]

    assert saved_assignment.employee_id == "01M0EMP00000000000000000099"


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_preserves_leave_policy_id() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(
            leave_policy_id="01M0LP00000000000000000099",
        ),
    )

    saved_assignment = repository.save_calls[0]

    assert saved_assignment.leave_policy_id == "01M0LP00000000000000000099"


@pytest.mark.asyncio
async def test_create_employee_leave_assignment_preserves_effective_dates() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(
            effective_from=date(2027, 1, 1),
            effective_until=date(2027, 6, 30),
        ),
    )

    saved_assignment = repository.save_calls[0]

    assert saved_assignment.effective_from == date(2027, 1, 1)
    assert saved_assignment.effective_until == date(2027, 6, 30)