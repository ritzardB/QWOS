"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_get_work_schedule_use_case.py

Description:
    Unit tests for GetWorkScheduleUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from qwos.application.attendance.use_cases.get_work_schedule_use_case import (
    GetWorkScheduleUseCase,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
OTHER_TENANT_ID = "01OTHER00000000000000000001"
SCHEDULE_ID = "01K2TESTSCHEDULE000000001"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"


class FakeWorkScheduleRepository:
    """
    Fake repository used by GetWorkScheduleUseCase tests.
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
    schedule_code: str = "Standard-5-day-work",
    schedule_name: str = "Standard 5-day work",
    timezone_name: str = "UTC",
    is_active: bool = True,
    tenant_id: str = TENANT_ID,
    created_at: datetime | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=schedule_id,
        tenant_id=tenant_id,
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
    schedule: object | None = None,
    tenant_id: str = TENANT_ID,
) -> tuple[
    GetWorkScheduleUseCase,
    FakeWorkScheduleRepository,
]:
    repository = FakeWorkScheduleRepository()
    repository.schedule = schedule

    use_case = GetWorkScheduleUseCase(
        work_schedule_repository=repository,
        request_context=make_request_context(
            tenant_id=tenant_id,
        ),
    )

    return use_case, repository


@pytest.mark.asyncio
async def test_get_work_schedule_returns_schedule() -> None:
    created_at = datetime(
        2026,
        9,
        10,
        8,
        30,
        tzinfo=timezone.utc,
    )

    schedule = make_schedule(
        created_at=created_at,
    )

    use_case, repository = make_use_case(
        schedule=schedule,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.id == SCHEDULE_ID
    assert response.schedule_code == "Standard-5-day-work"
    assert response.schedule_name == "Standard 5-day work"
    assert response.timezone == "UTC"
    assert response.is_active is True
    assert response.created_at == created_at

    assert repository.received_tenant_id == TENANT_ID
    assert repository.received_schedule_id == SCHEDULE_ID


@pytest.mark.asyncio
async def test_get_work_schedule_maps_all_fields() -> None:
    created_at = datetime(
        2026,
        9,
        15,
        7,
        45,
        tzinfo=timezone.utc,
    )

    schedule = make_schedule(
        schedule_code="Night-shift",
        schedule_name="Night Shift",
        timezone_name="UTC",
        is_active=False,
        created_at=created_at,
    )

    use_case, _ = make_use_case(
        schedule=schedule,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.id == schedule.id
    assert response.schedule_code == "Night-shift"
    assert response.schedule_name == "Night Shift"
    assert response.timezone == "UTC"
    assert response.is_active is False
    assert response.created_at == created_at


@pytest.mark.asyncio
async def test_get_work_schedule_uses_tenant_from_request_context() -> None:
    schedule = make_schedule(
        tenant_id=OTHER_TENANT_ID,
    )

    use_case, repository = make_use_case(
        schedule=schedule,
        tenant_id=OTHER_TENANT_ID,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.id == SCHEDULE_ID
    assert repository.received_tenant_id == OTHER_TENANT_ID


@pytest.mark.asyncio
async def test_get_work_schedule_passes_requested_schedule_id() -> None:
    requested_schedule_id = "01DIFFERENTSCHEDULE000000001"

    schedule = make_schedule(
        schedule_id=requested_schedule_id,
    )

    use_case, repository = make_use_case(
        schedule=schedule,
    )

    response = await use_case.execute(
        requested_schedule_id,
    )

    assert response.id == requested_schedule_id
    assert repository.received_schedule_id == requested_schedule_id


@pytest.mark.asyncio
async def test_get_work_schedule_raises_not_found_when_missing() -> None:
    use_case, repository = make_use_case(
        schedule=None,
    )

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(
            SCHEDULE_ID,
        )

    assert repository.received_tenant_id == TENANT_ID
    assert repository.received_schedule_id == SCHEDULE_ID


@pytest.mark.asyncio
async def test_get_work_schedule_does_not_use_unscoped_lookup() -> None:
    schedule = make_schedule()

    use_case, repository = make_use_case(
        schedule=schedule,
    )

    await use_case.execute(
        SCHEDULE_ID,
    )

    assert repository.received_tenant_id == TENANT_ID
    assert repository.received_schedule_id == SCHEDULE_ID


@pytest.mark.asyncio
async def test_get_work_schedule_preserves_inactive_status() -> None:
    schedule = make_schedule(
        is_active=False,
    )

    use_case, _ = make_use_case(
        schedule=schedule,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.is_active is False


@pytest.mark.asyncio
async def test_get_work_schedule_preserves_timezone() -> None:
    schedule = make_schedule(
        timezone_name="Asia/Dubai",
    )

    use_case, _ = make_use_case(
        schedule=schedule,
    )

    response = await use_case.execute(
        SCHEDULE_ID,
    )

    assert response.timezone == "Asia/Dubai"