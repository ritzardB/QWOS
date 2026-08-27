"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_list_work_schedules_use_case.py

Description:
    Unit tests for ListWorkSchedulesUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from qwos.application.attendance.use_cases.list_work_schedules_use_case import (
    ListWorkSchedulesUseCase,
)
from qwos.application.common.context.request_context import RequestContext

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
OTHER_TENANT_ID = "01OTHER00000000000000000001"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"


class FakeWorkScheduleRepository:
    def __init__(self) -> None:
        self.schedules: list[object] = []
        self.received_tenant_id: str | None = None

    def list_by_tenant(
        self,
        *,
        tenant_id: str,
    ) -> list[object]:
        self.received_tenant_id = tenant_id
        return self.schedules


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
    schedule_id: str,
    schedule_code: str,
    schedule_name: str,
    timezone_name: str = "UTC",
    is_active: bool = True,
    created_at: datetime | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=schedule_id,
        schedule_code=schedule_code,
        schedule_name=schedule_name,
        timezone=timezone_name,
        is_active=is_active,
        created_at=created_at
        or datetime(
            2026,
            9,
            1,
            4,
            0,
            tzinfo=timezone.utc,
        ),
    )


def make_use_case(
    *,
    schedules: list[object] | None = None,
    tenant_id: str = TENANT_ID,
) -> tuple[
    ListWorkSchedulesUseCase,
    FakeWorkScheduleRepository,
]:
    repository = FakeWorkScheduleRepository()

    if schedules is not None:
        repository.schedules = schedules

    use_case = ListWorkSchedulesUseCase(
        work_schedule_repository=repository,
        request_context=make_request_context(
            tenant_id=tenant_id,
        ),
    )

    return use_case, repository


@pytest.mark.asyncio
async def test_list_work_schedules_returns_schedules() -> None:
    schedules = [
        make_schedule(
            schedule_id="01SCHEDULE000000000000000001",
            schedule_code="Standard-5-day-work",
            schedule_name="Standard 5-day work",
        ),
        make_schedule(
            schedule_id="01SCHEDULE000000000000000002",
            schedule_code="Night-shift",
            schedule_name="Night Shift",
        ),
    ]

    use_case, repository = make_use_case(
        schedules=schedules,
    )

    response = await use_case.execute()

    assert response.total == 2
    assert len(response.items) == 2
    assert repository.received_tenant_id == TENANT_ID


@pytest.mark.asyncio
async def test_list_work_schedules_returns_empty_result() -> None:
    use_case, repository = make_use_case(
        schedules=[],
    )

    response = await use_case.execute()

    assert response.items == []
    assert response.total == 0
    assert repository.received_tenant_id == TENANT_ID


@pytest.mark.asyncio
async def test_list_work_schedules_maps_schedule_fields() -> None:
    created_at = datetime(
        2026,
        9,
        10,
        8,
        30,
        tzinfo=timezone.utc,
    )

    schedule = make_schedule(
        schedule_id="01SCHEDULE000000000000000001",
        schedule_code="Standard-5-day-work",
        schedule_name="Standard 5-day work",
        timezone_name="UTC",
        is_active=True,
        created_at=created_at,
    )

    use_case, _ = make_use_case(
        schedules=[schedule],
    )

    response = await use_case.execute()

    item = response.items[0]

    assert item.id == schedule.id
    assert item.schedule_code == "Standard-5-day-work"
    assert item.schedule_name == "Standard 5-day work"
    assert item.timezone == "UTC"
    assert item.is_active is True
    assert item.created_at == created_at


@pytest.mark.asyncio
async def test_list_work_schedules_preserves_inactive_schedule() -> None:
    schedule = make_schedule(
        schedule_id="01SCHEDULE000000000000000001",
        schedule_code="Archived-5-day-work",
        schedule_name="Archived 5-day work",
        is_active=False,
    )

    use_case, _ = make_use_case(
        schedules=[schedule],
    )

    response = await use_case.execute()

    assert response.total == 1
    assert response.items[0].is_active is False


@pytest.mark.asyncio
async def test_list_work_schedules_uses_request_context_tenant() -> None:
    schedules = [
        make_schedule(
            schedule_id="01SCHEDULE000000000000000001",
            schedule_code="Standard-5-day-work",
            schedule_name="Standard 5-day work",
        ),
    ]

    use_case, repository = make_use_case(
        schedules=schedules,
        tenant_id=OTHER_TENANT_ID,
    )

    response = await use_case.execute()

    assert response.total == 1
    assert repository.received_tenant_id == OTHER_TENANT_ID


@pytest.mark.asyncio
async def test_list_work_schedules_preserves_repository_order() -> None:
    schedules = [
        make_schedule(
            schedule_id="01SCHEDULE000000000000000001",
            schedule_code="Standard-5-day-work",
            schedule_name="Standard 5-day work",
        ),
        make_schedule(
            schedule_id="01SCHEDULE000000000000000002",
            schedule_code="Weekend",
            schedule_name="Weekend Schedule",
        ),
        make_schedule(
            schedule_id="01SCHEDULE000000000000000003",
            schedule_code="Night-shift",
            schedule_name="Night Shift",
        ),
    ]

    use_case, _ = make_use_case(
        schedules=schedules,
    )

    response = await use_case.execute()

    assert [item.id for item in response.items] == [
        schedules[0].id,
        schedules[1].id,
        schedules[2].id,
    ]


@pytest.mark.asyncio
async def test_list_work_schedules_total_matches_item_count() -> None:
    schedules = [
        make_schedule(
            schedule_id="01SCHEDULE000000000000000001",
            schedule_code="Schedule-1",
            schedule_name="Schedule 1",
        ),
        make_schedule(
            schedule_id="01SCHEDULE000000000000000002",
            schedule_code="Schedule-2",
            schedule_name="Schedule 2",
        ),
        make_schedule(
            schedule_id="01SCHEDULE000000000000000003",
            schedule_code="Schedule-3",
            schedule_name="Schedule 3",
        ),
    ]

    use_case, _ = make_use_case(
        schedules=schedules,
    )

    response = await use_case.execute()

    assert response.total == len(response.items)
    assert response.total == 3


@pytest.mark.asyncio
async def test_list_work_schedules_does_not_mutate_repository_result() -> None:
    schedules = [
        make_schedule(
            schedule_id="01SCHEDULE000000000000000001",
            schedule_code="Schedule-1",
            schedule_name="Schedule 1",
        ),
        make_schedule(
            schedule_id="01SCHEDULE000000000000000002",
            schedule_code="Schedule-2",
            schedule_name="Schedule 2",
        ),
    ]

    use_case, repository = make_use_case(
        schedules=schedules,
    )

    original = list(repository.schedules)

    await use_case.execute()

    assert repository.schedules == original