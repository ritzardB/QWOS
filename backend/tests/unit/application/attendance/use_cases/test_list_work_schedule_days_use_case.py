"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_list_work_schedule_days_use_case.py

Description:
    Unit tests for ListWorkScheduleDaysUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, time, timezone
from types import SimpleNamespace

import pytest

from qwos.application.attendance.use_cases.list_work_schedule_days_use_case import (
    ListWorkScheduleDaysUseCase,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
OTHER_TENANT_ID = "01OTHER00000000000000000001"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
SCHEDULE_ID = "01K2TESTSCHEDULE000000001"


class FakeWorkScheduleRepository:
    """
    Fake repository used by ListWorkScheduleDaysUseCase tests.
    """

    def __init__(self) -> None:
        self.schedule: object | None = None
        self.received_tenant_id: str | None = None
        self.received_schedule_id: str | None = None

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        schedule_id: str,
    ) -> object | None:
        self.received_tenant_id = tenant_id
        self.received_schedule_id = schedule_id
        return self.schedule


class FakeWorkScheduleDayRepository:
    """
    Fake repository used to return schedule day rules.
    """

    def __init__(self) -> None:
        self.schedule_days: list[object] = []
        self.received_tenant_id: str | None = None
        self.received_work_schedule_id: str | None = None

    def list_by_schedule(
        self,
        *,
        tenant_id: str,
        work_schedule_id: str,
    ) -> list[object]:
        self.received_tenant_id = tenant_id
        self.received_work_schedule_id = work_schedule_id
        return self.schedule_days


def make_request_context(
    *,
    tenant_id: str = TENANT_ID,
) -> RequestContext:
    return RequestContext(
        tenant_id=tenant_id,
        user_id=USER_ID,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )


def make_schedule(
    *,
    schedule_id: str = SCHEDULE_ID,
    tenant_id: str = TENANT_ID,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=schedule_id,
        tenant_id=tenant_id,
        schedule_code="Standard-5-day-work",
        schedule_name="Standard 5-day work",
        timezone="UTC",
        is_active=True,
    )


def make_schedule_day(
    *,
    day_id: str,
    day_of_week: int,
    day_type: str = "workday",
    start_time: time | None = time(9, 0),
    end_time: time | None = time(18, 0),
    break_minutes: int = 60,
    is_overnight: bool = False,
    work_schedule_id: str = SCHEDULE_ID,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=day_id,
        work_schedule_id=work_schedule_id,
        day_of_week=day_of_week,
        day_type=day_type,
        start_time=start_time,
        end_time=end_time,
        break_minutes=break_minutes,
        is_overnight=is_overnight,
        created_at=datetime(
            2026,
            9,
            day_of_week,
            4,
            0,
            tzinfo=timezone.utc,
        ),
    )


def make_use_case(
    *,
    schedule: object | None = None,
    schedule_days: list[object] | None = None,
    tenant_id: str = TENANT_ID,
) -> tuple[
    ListWorkScheduleDaysUseCase,
    FakeWorkScheduleRepository,
    FakeWorkScheduleDayRepository,
]:
    work_schedule_repository = FakeWorkScheduleRepository()
    work_schedule_day_repository = FakeWorkScheduleDayRepository()

    work_schedule_repository.schedule = schedule

    if schedule_days is not None:
        work_schedule_day_repository.schedule_days = schedule_days

    use_case = ListWorkScheduleDaysUseCase(
        work_schedule_repository=work_schedule_repository,
        work_schedule_day_repository=work_schedule_day_repository,
        request_context=make_request_context(
            tenant_id=tenant_id,
        ),
    )

    return (
        use_case,
        work_schedule_repository,
        work_schedule_day_repository,
    )


@pytest.mark.asyncio
async def test_list_work_schedule_days_returns_schedule_days() -> None:
    schedule = make_schedule()

    schedule_days = [
        make_schedule_day(
            day_id="01WSDAY00000000000000000001",
            day_of_week=1,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000002",
            day_of_week=2,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000003",
            day_of_week=3,
        ),
    ]

    (
        use_case,
        schedule_repository,
        day_repository,
    ) = make_use_case(
        schedule=schedule,
        schedule_days=schedule_days,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.total == 3
    assert len(response.items) == 3

    assert schedule_repository.received_tenant_id == TENANT_ID
    assert schedule_repository.received_schedule_id == SCHEDULE_ID

    assert day_repository.received_tenant_id == TENANT_ID
    assert day_repository.received_work_schedule_id == SCHEDULE_ID


@pytest.mark.asyncio
async def test_list_work_schedule_days_returns_empty_result() -> None:
    (
        use_case,
        _,
        day_repository,
    ) = make_use_case(
        schedule=make_schedule(),
        schedule_days=[],
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.items == []
    assert response.total == 0
    assert day_repository.received_tenant_id == TENANT_ID
    assert day_repository.received_work_schedule_id == SCHEDULE_ID


@pytest.mark.asyncio
async def test_list_work_schedule_days_maps_workday_fields() -> None:
    schedule_day = make_schedule_day(
        day_id="01WSDAY00000000000000000001",
        day_of_week=1,
        day_type="workday",
        start_time=time(9, 0),
        end_time=time(18, 0),
        break_minutes=60,
        is_overnight=False,
    )

    use_case, _, _ = make_use_case(
        schedule=make_schedule(),
        schedule_days=[schedule_day],
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    item = response.items[0]

    assert item.id == schedule_day.id
    assert item.work_schedule_id == SCHEDULE_ID
    assert item.day_of_week == 1
    assert item.day_type == "workday"
    assert item.start_time == time(9, 0)
    assert item.end_time == time(18, 0)
    assert item.break_minutes == 60
    assert item.is_overnight is False
    assert item.created_at == schedule_day.created_at


@pytest.mark.asyncio
async def test_list_work_schedule_days_maps_rest_day_fields() -> None:
    schedule_day = make_schedule_day(
        day_id="01WSDAY00000000000000000006",
        day_of_week=6,
        day_type="rest_day",
        start_time=None,
        end_time=None,
        break_minutes=0,
        is_overnight=False,
    )

    use_case, _, _ = make_use_case(
        schedule=make_schedule(),
        schedule_days=[schedule_day],
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    item = response.items[0]

    assert item.day_of_week == 6
    assert item.day_type == "rest_day"
    assert item.start_time is None
    assert item.end_time is None
    assert item.break_minutes == 0
    assert item.is_overnight is False


@pytest.mark.asyncio
async def test_list_work_schedule_days_maps_overnight_day() -> None:
    schedule_day = make_schedule_day(
        day_id="01WSDAY00000000000000000001",
        day_of_week=1,
        start_time=time(22, 0),
        end_time=time(6, 0),
        break_minutes=30,
        is_overnight=True,
    )

    use_case, _, _ = make_use_case(
        schedule=make_schedule(),
        schedule_days=[schedule_day],
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    item = response.items[0]

    assert item.start_time == time(22, 0)
    assert item.end_time == time(6, 0)
    assert item.break_minutes == 30
    assert item.is_overnight is True


@pytest.mark.asyncio
async def test_list_work_schedule_days_raises_not_found_when_schedule_missing() -> None:
    (
        use_case,
        schedule_repository,
        day_repository,
    ) = make_use_case(
        schedule=None,
        schedule_days=[],
    )

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(
            SCHEDULE_ID,
        )

    assert schedule_repository.received_tenant_id == TENANT_ID
    assert schedule_repository.received_schedule_id == SCHEDULE_ID

    assert day_repository.received_tenant_id is None
    assert day_repository.received_work_schedule_id is None


@pytest.mark.asyncio
async def test_list_work_schedule_days_uses_request_context_tenant() -> None:
    (
        use_case,
        schedule_repository,
        day_repository,
    ) = make_use_case(
        schedule=make_schedule(
            tenant_id=OTHER_TENANT_ID,
        ),
        schedule_days=[
            make_schedule_day(
                day_id="01WSDAY00000000000000000001",
                day_of_week=1,
            ),
        ],
        tenant_id=OTHER_TENANT_ID,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.total == 1

    assert schedule_repository.received_tenant_id == OTHER_TENANT_ID
    assert day_repository.received_tenant_id == OTHER_TENANT_ID


@pytest.mark.asyncio
async def test_list_work_schedule_days_passes_schedule_id_to_repositories() -> None:
    requested_schedule_id = "01DIFFERENTSCHEDULE000000001"

    schedule = make_schedule(
        schedule_id=requested_schedule_id,
    )

    schedule_days = [
        make_schedule_day(
            day_id="01WSDAY00000000000000000001",
            day_of_week=1,
            work_schedule_id=requested_schedule_id,
        ),
    ]

    (
        use_case,
        schedule_repository,
        day_repository,
    ) = make_use_case(
        schedule=schedule,
        schedule_days=schedule_days,
    )

    response = await use_case.execute(
        requested_schedule_id,
    )

    assert response.total == 1
    assert schedule_repository.received_schedule_id == requested_schedule_id
    assert day_repository.received_work_schedule_id == requested_schedule_id


@pytest.mark.asyncio
async def test_list_work_schedule_days_preserves_repository_order() -> None:
    schedule_days = [
        make_schedule_day(
            day_id="01WSDAY00000000000000000001",
            day_of_week=1,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000005",
            day_of_week=5,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000007",
            day_of_week=7,
            day_type="rest_day",
            start_time=None,
            end_time=None,
            break_minutes=0,
        ),
    ]

    use_case, _, _ = make_use_case(
        schedule=make_schedule(),
        schedule_days=schedule_days,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert [item.id for item in response.items] == [
        schedule_days[0].id,
        schedule_days[1].id,
        schedule_days[2].id,
    ]
    assert [item.day_of_week for item in response.items] == [
        1,
        5,
        7,
    ]


@pytest.mark.asyncio
async def test_list_work_schedule_days_total_matches_item_count() -> None:
    schedule_days = [
        make_schedule_day(
            day_id="01WSDAY00000000000000000001",
            day_of_week=1,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000002",
            day_of_week=2,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000003",
            day_of_week=3,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000004",
            day_of_week=4,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000005",
            day_of_week=5,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000006",
            day_of_week=6,
            day_type="rest_day",
            start_time=None,
            end_time=None,
            break_minutes=0,
        ),
        make_schedule_day(
            day_id="01WSDAY00000000000000000007",
            day_of_week=7,
            day_type="rest_day",
            start_time=None,
            end_time=None,
            break_minutes=0,
        ),
    ]

    use_case, _, _ = make_use_case(
        schedule=make_schedule(),
        schedule_days=schedule_days,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.total == 7
    assert response.total == len(response.items)