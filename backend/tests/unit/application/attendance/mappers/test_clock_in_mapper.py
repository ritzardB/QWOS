"""
===============================================================================
Quantum Workforce OS (QWOS)

Tests

Application Layer

Attendance Module

File:
    test_clock_in_mapper.py

Description:
    Tests ClockInMapper request and response mappings.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from qwos.api.contracts.requests.attendance.clock_in_request import (
    ClockInRequest,
)
from qwos.api.contracts.responses.attendance.clock_in_response import (
    ClockInResponse,
)
from qwos.application.attendance.commands.clock_in_command import (
    ClockInCommand,
)
from qwos.application.attendance.mappers.clock_in_mapper import (
    ClockInMapper,
)
from qwos.application.attendance.responses.clock_in_response import (
    ClockInResponse as ApplicationClockInResponse,
)
from qwos.application.common.context.request_context import (
    RequestContext,
)


TENANT_ID = "01TENANT000000000000000000"
USER_ID = "01USER000000000000000000000"
EMPLOYEE_ID = "01EMPLOYEE0000000000000000"

ATTENDANCE_RECORD_ID = "01ATTENDANCERECORD00000000"
ATTENDANCE_EVENT_ID = "01ATTENDANCEEVENT000000000"

CLOCK_IN_AT = datetime(
    2026,
    8,
    24,
    8,
    30,
    tzinfo=timezone.utc,
)

ATTENDANCE_DATE = date(2026, 8, 24)


def build_request(
    *,
    employee_id: str = EMPLOYEE_ID,
    clock_in_at: datetime | None = CLOCK_IN_AT,
    event_source: str = "web",
    notes: str | None = "Started work.",
) -> ClockInRequest:
    return ClockInRequest(
        employee_id=employee_id,
        clock_in_at=clock_in_at,
        event_source=event_source,
        notes=notes,
    )


def build_request_context() -> RequestContext:
    return RequestContext(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        correlation_id="01CORRELATION0000000000000",
        request_id="01REQUEST000000000000000000",
    )


def build_application_response() -> ApplicationClockInResponse:
    return ApplicationClockInResponse(
        attendance_record_id=ATTENDANCE_RECORD_ID,
        attendance_event_id=ATTENDANCE_EVENT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=ATTENDANCE_DATE,
        clock_in_at=CLOCK_IN_AT,
        status="present",
        event_type="clock_in",
        event_at=CLOCK_IN_AT,
    )


def test_to_command_maps_request_and_context() -> None:
    request = build_request()
    request_context = build_request_context()

    command = ClockInMapper.to_command(
        request=request,
        request_context=request_context,
    )

    assert isinstance(command, ClockInCommand)
    assert command.tenant_id == TENANT_ID
    assert command.employee_id == EMPLOYEE_ID
    assert command.clock_in_at == CLOCK_IN_AT
    assert command.event_source == "web"
    assert command.notes == "Started work."


def test_to_command_maps_optional_timestamp_as_none() -> None:
    request = build_request(
        clock_in_at=None,
    )

    command = ClockInMapper.to_command(
        request=request,
        request_context=build_request_context(),
    )

    assert command.clock_in_at is None


def test_to_command_maps_custom_event_source() -> None:
    request = build_request(
        event_source="mobile",
    )

    command = ClockInMapper.to_command(
        request=request,
        request_context=build_request_context(),
    )

    assert command.event_source == "mobile"


def test_to_command_maps_missing_notes() -> None:
    request = build_request(
        notes=None,
    )

    command = ClockInMapper.to_command(
        request=request,
        request_context=build_request_context(),
    )

    assert command.notes is None


def test_to_response_maps_application_response() -> None:
    application_response = build_application_response()

    response = ClockInMapper.to_response(
        application_response,
    )

    assert isinstance(response, ClockInResponse)
    assert response.attendance_record_id == ATTENDANCE_RECORD_ID
    assert response.attendance_event_id == ATTENDANCE_EVENT_ID
    assert response.employee_id == EMPLOYEE_ID
    assert response.attendance_date == ATTENDANCE_DATE
    assert response.clock_in_at == CLOCK_IN_AT
    assert response.status == "present"
    assert response.event_type == "clock_in"
    assert response.event_at == CLOCK_IN_AT
