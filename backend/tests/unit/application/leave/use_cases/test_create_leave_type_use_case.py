"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_leave_type_use_case.py

Description:
    Unit tests for CreateLeaveTypeUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.leave.commands.create_leave_type_command import (
    CreateLeaveTypeCommand,
)
from qwos.application.leave.use_cases.create_leave_type_use_case import (
    CreateLeaveTypeUseCase,
)
from qwos.application.common.results.create_leave_type_validator import (
    CreateLeaveTypeValidator,
)

TENANT_ID = "01M0TEN00000000000000000001"
OTHER_TENANT_ID = "01M0TEN00000000000000000002"
USER_ID = "01M0USR00000000000000000001"
LEAVE_TYPE_ID = "01M0LT00000000000000000001"


class FakeRepository:
    def __init__(self) -> None:
        self.save_calls: list[object] = []
        self.exists_result = False

    def exists_by_code(
        self,
        *,
        tenant_id: str,
        leave_code: str,
    ) -> bool:
        return self.exists_result

    def save(self, entity: object) -> None:
        self.save_calls.append(entity)


class FakeIdGenerator:
    def generate(self) -> str:
        return LEAVE_TYPE_ID


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
    leave_code: str = "annual",
    leave_name: str = "Annual Leave",
    description: str | None = "Paid annual vacation leave.",
    is_paid: bool = True,
    is_active: bool = True,
) -> CreateLeaveTypeCommand:
    return CreateLeaveTypeCommand(
        tenant_id=tenant_id,
        leave_code=leave_code,
        leave_name=leave_name,
        description=description,
        is_paid=is_paid,
        is_active=is_active,
    )


def make_use_case() -> tuple[
    CreateLeaveTypeUseCase,
    FakeRepository,
    FakeIdGenerator,
    FakeUnitOfWork,
]:
    repository = FakeRepository()
    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    use_case = CreateLeaveTypeUseCase(
        leave_type_repository=repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=CreateLeaveTypeValidator(),
        request_context=make_request_context(),
    )

    return (
        use_case,
        repository,
        id_generator,
        unit_of_work,
    )


@pytest.mark.asyncio
async def test_create_leave_type_successfully() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(),
    )

    assert response.id == LEAVE_TYPE_ID
    assert response.leave_code == "annual"
    assert response.leave_name == "Annual Leave"
    assert response.description == "Paid annual vacation leave."
    assert response.is_paid is True
    assert response.is_active is True

    assert len(repository.save_calls) == 1
    assert unit_of_work.entered is True
    assert unit_of_work.exited is True
    assert unit_of_work.flush_called is True


@pytest.mark.asyncio
async def test_create_leave_type_normalizes_leave_code() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            leave_code="  ANNUAL  ",
        ),
    )

    assert response.leave_code == "annual"

    assert len(repository.save_calls) == 1
    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.leave_code == "annual"


@pytest.mark.asyncio
async def test_create_leave_type_normalizes_leave_name() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            leave_name="  Annual Leave  ",
        ),
    )

    assert response.leave_name == "Annual Leave"

    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.leave_name == "Annual Leave"


@pytest.mark.asyncio
async def test_create_leave_type_normalizes_description() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            description="  Paid annual vacation leave.  ",
        ),
    )

    assert response.description == "Paid annual vacation leave."

    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.description == "Paid annual vacation leave."


@pytest.mark.asyncio
async def test_create_leave_type_accepts_unpaid_leave() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            is_paid=False,
        ),
    )

    assert response.is_paid is False

    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.is_paid is False


@pytest.mark.asyncio
async def test_create_leave_type_accepts_inactive_leave_type() -> None:
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

    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.is_active is False


@pytest.mark.asyncio
async def test_create_leave_type_allows_null_description() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            description=None,
        ),
    )

    assert response.description is None

    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.description is None


@pytest.mark.asyncio
async def test_duplicate_leave_code_raises_duplicate_resource() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    repository.exists_result = True

    with pytest.raises(DuplicateResourceException):
        await use_case.execute(
            make_command(),
        )

    assert repository.save_calls == []


@pytest.mark.asyncio
async def test_duplicate_leave_code_check_uses_normalized_code() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    repository.exists_result = True

    with pytest.raises(DuplicateResourceException):
        await use_case.execute(
            make_command(
                leave_code="  ANNUAL  ",
            ),
        )

    assert repository.save_calls == []


@pytest.mark.asyncio
async def test_invalid_command_raises_validation_exception() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                leave_code="   ",
            ),
        )

    assert repository.save_calls == []


@pytest.mark.asyncio
async def test_invalid_leave_name_raises_validation_exception() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                leave_name="   ",
            ),
        )

    assert repository.save_calls == []


@pytest.mark.asyncio
async def test_create_leave_type_uses_request_context_tenant() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            tenant_id=OTHER_TENANT_ID,
        ),
    )

    assert response.id == LEAVE_TYPE_ID

    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.tenant_id == OTHER_TENANT_ID


@pytest.mark.asyncio
async def test_create_leave_type_sets_created_by_from_request_context() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.created_by == USER_ID
    assert saved_leave_type.updated_by == USER_ID


@pytest.mark.asyncio
async def test_create_leave_type_uses_generated_id() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    saved_leave_type = repository.save_calls[0]

    assert saved_leave_type.id == LEAVE_TYPE_ID


@pytest.mark.asyncio
async def test_create_leave_type_checks_duplicate_with_tenant_and_code() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    repository.exists_result = False

    await use_case.execute(
        make_command(),
    )

    assert len(repository.save_calls) == 1