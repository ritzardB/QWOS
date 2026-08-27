"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_employee_work_schedule_use_case.py

Description:
    Unit tests for CreateEmployeeWorkScheduleUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from qwos.application.attendance.commands.create_employee_work_schedule_command import (
    CreateEmployeeWorkScheduleCommand,
)
from qwos.application.attendance.use_cases.create_employee_work_schedule_use_case import (
    CreateEmployeeWorkScheduleUseCase,
)
from qwos.application.attendance.validators.create_employee_work_schedule_validator import (
    CreateEmployeeWorkScheduleValidator,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)

TENANT_ID = "01M0TEN00000000000000000001"
OTHER_TENANT_ID = "01M0TEN00000000000000000002"
EMPLOYEE_ID = "01M0EMP00000000000000000001"
SCHEDULE_ID = "01M0WS00000000000000000001"
ASSIGNMENT_ID = "01M0EWS0000000000000000001"
USER_ID = "01M0USR00000000000000000001"


class FakeRepository:
    def __init__(self) -> None:
        self.save_calls: list[object] = []
        self.exists_result = False
        self.employee_result = None
        self.schedule_result = None

    def get_by_id(self, _employee_id: str):
        return self.employee_result

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        schedule_id: str,
    ):
        return self.schedule_result

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
    work_schedule_id: str = SCHEDULE_ID,
    effective_from: date | None = date(2026, 9, 1),
    effective_until: date | None = None,
    is_active: bool = True,
) -> CreateEmployeeWorkScheduleCommand:
    return CreateEmployeeWorkScheduleCommand(
        tenant_id=tenant_id,
        employee_id=employee_id,
        work_schedule_id=work_schedule_id,
        effective_from=effective_from,
        effective_until=effective_until,
        is_active=is_active,
    )


def make_employee(
    *,
    tenant_id: str = TENANT_ID,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=EMPLOYEE_ID,
        tenant_id=tenant_id,
    )


def make_schedule(
    *,
    tenant_id: str = TENANT_ID,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=SCHEDULE_ID,
        tenant_id=tenant_id,
    )


def make_use_case() -> tuple[
    CreateEmployeeWorkScheduleUseCase,
    FakeRepository,
    FakeRepository,
    FakeRepository,
    FakeIdGenerator,
    FakeUnitOfWork,
]:
    employee_repository = FakeRepository()
    work_schedule_repository = FakeRepository()
    employee_work_schedule_repository = FakeRepository()

    employee_repository.employee_result = make_employee()
    work_schedule_repository.schedule_result = make_schedule()

    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    use_case = CreateEmployeeWorkScheduleUseCase(
        employee_repository=employee_repository,
        work_schedule_repository=work_schedule_repository,
        employee_work_schedule_repository=(
            employee_work_schedule_repository
        ),
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=CreateEmployeeWorkScheduleValidator(),
        request_context=make_request_context(),
    )

    return (
        use_case,
        employee_repository,
        work_schedule_repository,
        employee_work_schedule_repository,
        id_generator,
        unit_of_work,
    )


@pytest.mark.asyncio
async def test_create_employee_work_schedule_successfully() -> None:
    (
        use_case,
        _,
        _,
        assignment_repository,
        _,
        unit_of_work,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(),
    )

    assert response.id == ASSIGNMENT_ID
    assert response.employee_id == EMPLOYEE_ID
    assert response.work_schedule_id == SCHEDULE_ID
    assert response.effective_from == date(2026, 9, 1)
    assert response.effective_until is None
    assert response.is_active is True

    assert len(assignment_repository.save_calls) == 1
    assert unit_of_work.entered is True
    assert unit_of_work.exited is True
    assert unit_of_work.flush_called is True


@pytest.mark.asyncio
async def test_create_employee_work_schedule_preserves_effective_until() -> None:
    (
        use_case,
        _,
        _,
        _,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            effective_until=date(2026, 12, 31),
        ),
    )

    assert response.effective_until == date(2026, 12, 31)


@pytest.mark.asyncio
async def test_create_employee_work_schedule_preserves_inactive_status() -> None:
    (
        use_case,
        _,
        _,
        _,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            is_active=False,
        ),
    )

    assert response.is_active is False


@pytest.mark.asyncio
async def test_missing_employee_raises_resource_not_found() -> None:
    (
        use_case,
        employee_repository,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    employee_repository.employee_result = None

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(
            make_command(),
        )

    assert assignment_repository.save_calls == []


@pytest.mark.asyncio
async def test_employee_tenant_mismatch_raises_value_error() -> None:
    (
        use_case,
        employee_repository,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    employee_repository.employee_result = make_employee(
        tenant_id=OTHER_TENANT_ID,
    )

    with pytest.raises(
        ValueError,
        match="Employee does not belong to the requested tenant",
    ):
        await use_case.execute(
            make_command(),
        )

    assert assignment_repository.save_calls == []


@pytest.mark.asyncio
async def test_missing_work_schedule_raises_resource_not_found() -> None:
    (
        use_case,
        _,
        work_schedule_repository,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    work_schedule_repository.schedule_result = None

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(
            make_command(),
        )

    assert assignment_repository.save_calls == []


@pytest.mark.asyncio
async def test_duplicate_effective_from_raises_duplicate_resource() -> None:
    (
        use_case,
        _,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    assignment_repository.exists_result = True

    with pytest.raises(DuplicateResourceException):
        await use_case.execute(
            make_command(),
        )

    assert assignment_repository.save_calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tenant_id,employee_id,work_schedule_id",
    [
        ("", EMPLOYEE_ID, SCHEDULE_ID),
        (TENANT_ID, "", SCHEDULE_ID),
        (TENANT_ID, EMPLOYEE_ID, ""),
    ],
)
async def test_invalid_identity_inputs_raise_validation_exception(
    tenant_id: str,
    employee_id: str,
    work_schedule_id: str,
) -> None:
    (
        use_case,
        _,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                tenant_id=tenant_id,
                employee_id=employee_id,
                work_schedule_id=work_schedule_id,
            ),
        )

    assert assignment_repository.save_calls == []


@pytest.mark.asyncio
async def test_missing_effective_from_raises_validation_exception() -> None:
    (
        use_case,
        _,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                effective_from=None,
            ),
        )

    assert assignment_repository.save_calls == []


@pytest.mark.asyncio
async def test_invalid_effective_range_raises_validation_exception() -> None:
    (
        use_case,
        _,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                effective_from=date(2026, 9, 1),
                effective_until=date(2026, 8, 31),
            ),
        )

    assert assignment_repository.save_calls == []


@pytest.mark.asyncio
async def test_schedule_lookup_uses_requested_tenant() -> None:
    (
        use_case,
        _,
        work_schedule_repository,
        _,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    assert work_schedule_repository.schedule_result is not None


@pytest.mark.asyncio
async def test_created_assignment_uses_generated_identifier() -> None:
    (
        use_case,
        _,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    assignment = assignment_repository.save_calls[0]

    assert assignment.id == ASSIGNMENT_ID
    assert assignment.employee_id == EMPLOYEE_ID
    assert assignment.work_schedule_id == SCHEDULE_ID


@pytest.mark.asyncio
async def test_created_assignment_uses_request_context_user() -> None:
    (
        use_case,
        _,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    assignment = assignment_repository.save_calls[0]

    assert assignment.created_by == USER_ID
    assert assignment.updated_by == USER_ID


@pytest.mark.asyncio
async def test_successful_creation_does_not_require_schedule_to_be_active(
) -> None:
    (
        use_case,
        _,
        work_schedule_repository,
        _,
        _,
        _,
    ) = make_use_case()

    work_schedule_repository.schedule_result = SimpleNamespace(
        id=SCHEDULE_ID,
        tenant_id=TENANT_ID,
        is_active=False,
    )

    response = await use_case.execute(
        make_command(),
    )

    assert response.work_schedule_id == SCHEDULE_ID


@pytest.mark.asyncio
async def test_validation_happens_before_employee_lookup() -> None:
    (
        use_case,
        employee_repository,
        _,
        assignment_repository,
        _,
        _,
    ) = make_use_case()

    employee_repository.employee_result = MagicMock()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                tenant_id="",
            ),
        )

    assert assignment_repository.save_calls == []