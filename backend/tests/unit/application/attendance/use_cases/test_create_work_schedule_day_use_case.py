"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_work_schedule_day_use_case.py

Description:
    Unit tests for CreateWorkScheduleDayUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import time
from types import SimpleNamespace

import pytest

from qwos.application.attendance.commands.create_work_schedule_day_command import (
    CreateWorkScheduleDayCommand,
)
from qwos.application.attendance.use_cases.create_work_schedule_day_use_case import (
    CreateWorkScheduleDayUseCase,
)
from qwos.application.attendance.validators.create_work_schedule_day_validator import (
    CreateWorkScheduleDayValidator,
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
SCHEDULE_ID = "01M0WS00000000000000000001"
DAY_ID = "01M0WSD0000000000000000001"
USER_ID = "01M0USR00000000000000000001"


class FakeWorkScheduleRepository:
    def __init__(self) -> None:
        self.schedule_result = None

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        schedule_id: str,
    ):
        return self.schedule_result


class FakeWorkScheduleDayRepository:
    def __init__(self) -> None:
        self.exists_result = False
        self.save_calls: list[object] = []

    def exists_by_schedule_and_day(
        self,
        *,
        tenant_id: str,
        work_schedule_id: str,
        day_of_week: int,
    ) -> bool:
        return self.exists_result

    def save(self, schedule_day: object) -> None:
        self.save_calls.append(schedule_day)


class FakeIdGenerator:
    def generate(self) -> str:
        return DAY_ID


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
    work_schedule_id: str = SCHEDULE_ID,
    day_of_week: int = 1,
    day_type: str = "workday",
    start_time: time | None = time(9, 0),
    end_time: time | None = time(18, 0),
    break_minutes: int = 60,
    is_overnight: bool = False,
) -> CreateWorkScheduleDayCommand:
    return CreateWorkScheduleDayCommand(
        tenant_id=tenant_id,
        work_schedule_id=work_schedule_id,
        day_of_week=day_of_week,
        day_type=day_type,
        start_time=start_time,
        end_time=end_time,
        break_minutes=break_minutes,
        is_overnight=is_overnight,
    )


def make_schedule(
    *,
    tenant_id: str = TENANT_ID,
    is_active: bool = True,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=SCHEDULE_ID,
        tenant_id=tenant_id,
        is_active=is_active,
    )


def make_use_case() -> tuple[
    CreateWorkScheduleDayUseCase,
    FakeWorkScheduleRepository,
    FakeWorkScheduleDayRepository,
    FakeIdGenerator,
    FakeUnitOfWork,
]:
    work_schedule_repository = FakeWorkScheduleRepository()
    work_schedule_day_repository = FakeWorkScheduleDayRepository()

    work_schedule_repository.schedule_result = make_schedule()

    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    use_case = CreateWorkScheduleDayUseCase(
        work_schedule_repository=work_schedule_repository,
        work_schedule_day_repository=work_schedule_day_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=CreateWorkScheduleDayValidator(),
        request_context=make_request_context(),
    )

    return (
        use_case,
        work_schedule_repository,
        work_schedule_day_repository,
        id_generator,
        unit_of_work,
    )


@pytest.mark.asyncio
async def test_create_work_schedule_day_successfully() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        unit_of_work,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(),
    )

    assert response.id == DAY_ID
    assert response.work_schedule_id == SCHEDULE_ID
    assert response.day_of_week == 1
    assert response.day_type == "workday"
    assert response.start_time == time(9, 0)
    assert response.end_time == time(18, 0)
    assert response.break_minutes == 60
    assert response.is_overnight is False

    assert len(day_repository.save_calls) == 1
    assert unit_of_work.entered is True
    assert unit_of_work.exited is True
    assert unit_of_work.flush_called is True


@pytest.mark.asyncio
async def test_create_work_schedule_day_supports_rest_day() -> None:
    (
        use_case,
        _,
        _,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            day_of_week=6,
            day_type="rest_day",
            start_time=None,
            end_time=None,
            break_minutes=0,
        ),
    )

    assert response.day_of_week == 6
    assert response.day_type == "rest_day"
    assert response.start_time is None
    assert response.end_time is None
    assert response.break_minutes == 0


@pytest.mark.asyncio
async def test_create_work_schedule_day_supports_overnight_workday() -> None:
    (
        use_case,
        _,
        _,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            start_time=time(22, 0),
            end_time=time(6, 0),
            break_minutes=30,
            is_overnight=True,
        ),
    )

    assert response.start_time == time(22, 0)
    assert response.end_time == time(6, 0)
    assert response.break_minutes == 30
    assert response.is_overnight is True


@pytest.mark.asyncio
async def test_missing_work_schedule_raises_resource_not_found() -> None:
    (
        use_case,
        work_schedule_repository,
        _,
        _,
        _,
    ) = make_use_case()

    work_schedule_repository.schedule_result = None

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(
            make_command(),
        )


@pytest.mark.asyncio
async def test_duplicate_day_raises_duplicate_resource() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    day_repository.exists_result = True

    with pytest.raises(DuplicateResourceException):
        await use_case.execute(
            make_command(
                day_of_week=1,
            ),
        )

    assert day_repository.save_calls == []


@pytest.mark.asyncio
async def test_missing_tenant_id_raises_validation_exception() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                tenant_id="",
            ),
        )

    assert day_repository.save_calls == []


@pytest.mark.asyncio
async def test_missing_work_schedule_id_raises_validation_exception() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                work_schedule_id="",
            ),
        )

    assert day_repository.save_calls == []


@pytest.mark.asyncio
async def test_invalid_day_of_week_raises_validation_exception() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                day_of_week=8,
            ),
        )

    assert day_repository.save_calls == []


@pytest.mark.asyncio
async def test_missing_workday_start_time_raises_validation_exception() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                start_time=None,
            ),
        )

    assert day_repository.save_calls == []


@pytest.mark.asyncio
async def test_missing_workday_end_time_raises_validation_exception() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                end_time=None,
            ),
        )

    assert day_repository.save_calls == []


@pytest.mark.asyncio
async def test_invalid_rest_day_configuration_raises_validation_exception() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                day_type="rest_day",
                start_time=None,
                end_time=None,
                break_minutes=30,
            ),
        )

    assert day_repository.save_calls == []


@pytest.mark.asyncio
async def test_negative_break_minutes_raises_validation_exception() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                break_minutes=-1,
            ),
        )

    assert day_repository.save_calls == []


@pytest.mark.asyncio
async def test_created_day_uses_generated_identifier() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    schedule_day = day_repository.save_calls[0]

    assert schedule_day.id == DAY_ID
    assert schedule_day.work_schedule_id == SCHEDULE_ID
    assert schedule_day.day_of_week == 1


@pytest.mark.asyncio
async def test_created_day_uses_request_context_user() -> None:
    (
        use_case,
        _,
        day_repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    schedule_day = day_repository.save_calls[0]

    assert schedule_day.created_by == USER_ID
    assert schedule_day.updated_by == USER_ID


@pytest.mark.asyncio
async def test_work_schedule_lookup_is_tenant_scoped() -> None:
    (
        use_case,
        work_schedule_repository,
        _,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    assert work_schedule_repository.schedule_result.tenant_id == TENANT_ID