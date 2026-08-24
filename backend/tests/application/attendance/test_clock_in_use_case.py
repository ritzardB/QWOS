"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Tests

Attendance Module

File:
    test_clock_in_use_case.py

Description:
    Unit tests for the ClockInUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import Mock

import pytest

from qwos.application.attendance.commands.clock_in_command import (
    ClockInCommand,
)
from qwos.application.attendance.use_cases.clock_in_use_case import (
    ClockInUseCase,
)
from qwos.application.attendance.validators.clock_in_validator import (
    ClockInValidator,
)
from qwos.application.common.context.request_context import (
    RequestContext,
)
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.domains.attendance.models.attendance_event import (
    AttendanceEvent,
)
from qwos.domains.attendance.models.attendance_record import (
    AttendanceRecord,
)


# =============================================================================
# Helpers
# =============================================================================


TENANT_ID = "01TENANT000000000000000000"
EMPLOYEE_ID = "01EMPLOYEE0000000000000000"
ATTENDANCE_RECORD_ID = "01ATTENDANCERECORD000000000"
ATTENDANCE_EVENT_ID = "01ATTENDANCEEVENT0000000000"
USER_ID = "01USER00000000000000000000"

CLOCK_IN_AT = datetime(
    2026,
    8,
    24,
    8,
    30,
    tzinfo=timezone.utc,
)


def build_request_context() -> Mock:
    """
    Build a request context suitable for the use case.
    """

    context = Mock(spec=RequestContext)
    context.tenant_id = TENANT_ID
    context.user_id = USER_ID

    return context


def build_employee() -> Mock:
    """
    Build a minimal employee mock.
    """

    employee = Mock()
    employee.id = EMPLOYEE_ID
    employee.tenant_id = TENANT_ID

    return employee


def build_unit_of_work() -> Mock:
    """
    Build a UnitOfWork mock that supports context-manager usage.
    """

    unit_of_work = Mock()

    unit_of_work.__enter__ = Mock(
        return_value=unit_of_work,
    )

    unit_of_work.__exit__ = Mock(
        return_value=False,
    )

    return unit_of_work


def build_use_case(
    *,
    employee_repository: Mock | None = None,
    attendance_record_repository: Mock | None = None,
    attendance_event_repository: Mock | None = None,
    id_generator: Mock | None = None,
    clock: Mock | None = None,
    unit_of_work: Mock | None = None,
    validator: ClockInValidator | Mock | None = None,
    request_context: Mock | None = None,
) -> ClockInUseCase:
    """
    Construct the ClockInUseCase with mocked dependencies.
    """

    employee_repository = (
        employee_repository
        or Mock()
    )

    attendance_record_repository = (
        attendance_record_repository
        or Mock()
    )

    attendance_event_repository = (
        attendance_event_repository
        or Mock()
    )

    id_generator = (
        id_generator
        or Mock()
    )

    clock = (
        clock
        or Mock()
    )

    unit_of_work = (
        unit_of_work
        or build_unit_of_work()
    )

    validator = (
        validator
        or ClockInValidator()
    )

    request_context = (
        request_context
        or build_request_context()
    )

    return ClockInUseCase(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )


def build_command(
    *,
    clock_in_at: datetime | None = CLOCK_IN_AT,
    event_source: str = "web",
    notes: str | None = None,
) -> ClockInCommand:
    """
    Build a standard ClockInCommand.
    """

    return ClockInCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        clock_in_at=clock_in_at,
        event_source=event_source,
        notes=notes,
    )


# =============================================================================
# Successful Clock-In
# =============================================================================


@pytest.mark.asyncio
async def test_clock_in_creates_attendance_record_and_event() -> None:
    """
    A first clock-in should create both an attendance record
    and an attendance event.
    """

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = build_employee()

    attendance_record_repository = Mock()
    attendance_record_repository.get_by_employee_and_date.return_value = None

    attendance_event_repository = Mock()

    id_generator = Mock()
    id_generator.generate.side_effect = [
        ATTENDANCE_RECORD_ID,
        ATTENDANCE_EVENT_ID,
    ]

    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
    )

    response = await use_case.execute(
        build_command(
            notes="Started work from office.",
        )
    )

    assert response.attendance_record_id == ATTENDANCE_RECORD_ID
    assert response.attendance_event_id == ATTENDANCE_EVENT_ID
    assert response.employee_id == EMPLOYEE_ID
    assert response.attendance_date == CLOCK_IN_AT.date()
    assert response.clock_in_at == CLOCK_IN_AT
    assert response.status == "present"

    attendance_record_repository.save.assert_called_once()
    attendance_event_repository.save.assert_called_once()
    unit_of_work.flush.assert_called_once()

    saved_record = (
        attendance_record_repository.save.call_args.args[0]
    )

    saved_event = (
        attendance_event_repository.save.call_args.args[0]
    )

    assert isinstance(
        saved_record,
        AttendanceRecord,
    )

    assert isinstance(
        saved_event,
        AttendanceEvent,
    )

    assert saved_record.id == ATTENDANCE_RECORD_ID
    assert saved_record.tenant_id == TENANT_ID
    assert saved_record.employee_id == EMPLOYEE_ID
    assert saved_record.attendance_date == CLOCK_IN_AT.date()
    assert saved_record.clock_in_at == CLOCK_IN_AT
    assert saved_record.status == "present"

    assert saved_event.id == ATTENDANCE_EVENT_ID
    assert saved_event.tenant_id == TENANT_ID
    assert saved_event.employee_id == EMPLOYEE_ID
    assert saved_event.attendance_record_id == ATTENDANCE_RECORD_ID
    assert saved_event.event_type == "clock_in"
    assert saved_event.event_at == CLOCK_IN_AT
    assert saved_event.event_source == "web"
    assert saved_event.notes == "Started work from office."


@pytest.mark.asyncio
async def test_clock_in_uses_clock_when_timestamp_is_not_supplied() -> None:
    """
    When clock_in_at is omitted, the application Clock should provide
    the timestamp.
    """

    clock = Mock()
    clock.now.return_value = CLOCK_IN_AT

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = build_employee()

    attendance_record_repository = Mock()
    attendance_record_repository.get_by_employee_and_date.return_value = None

    id_generator = Mock()
    id_generator.generate.side_effect = [
        ATTENDANCE_RECORD_ID,
        ATTENDANCE_EVENT_ID,
    ]

    attendance_event_repository = Mock()
    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
    )

    command = build_command(
        clock_in_at=None,
    )

    response = await use_case.execute(command)

    clock.now.assert_called_once()

    assert response.clock_in_at == CLOCK_IN_AT

    saved_record = (
        attendance_record_repository.save.call_args.args[0]
    )

    assert saved_record.clock_in_at == CLOCK_IN_AT


@pytest.mark.asyncio
async def test_clock_in_updates_existing_attendance_record_without_clock_in() -> None:
    """
    If an attendance record already exists for the day but has not yet
    been clocked in, the existing record should be reused.
    """

    existing_record = AttendanceRecord.create(
        id=ATTENDANCE_RECORD_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=CLOCK_IN_AT.date(),
        status="present",
        created_by=USER_ID,
    )

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = build_employee()

    attendance_record_repository = Mock()
    attendance_record_repository.get_by_employee_and_date.return_value = (
        existing_record
    )

    attendance_event_repository = Mock()

    id_generator = Mock()
    id_generator.generate.return_value = ATTENDANCE_EVENT_ID

    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
    )

    response = await use_case.execute(
        build_command()
    )

    assert response.attendance_record_id == ATTENDANCE_RECORD_ID
    assert response.attendance_event_id == ATTENDANCE_EVENT_ID

    saved_record = (
        attendance_record_repository.save.call_args.args[0]
    )

    assert saved_record is existing_record

    # The current production use case reuses the existing record but
    # does not explicitly assign clock_in_at. This assertion documents
    # the intended domain behavior and will expose that gap.
    assert saved_record.clock_in_at == CLOCK_IN_AT


# =============================================================================
# Duplicate Clock-In
# =============================================================================


@pytest.mark.asyncio
async def test_clock_in_rejects_duplicate_clock_in() -> None:
    """
    An employee cannot clock in twice for the same attendance day.
    """

    existing_record = AttendanceRecord.create(
        id=ATTENDANCE_RECORD_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=CLOCK_IN_AT.date(),
        clock_in_at=CLOCK_IN_AT,
        status="present",
        created_by=USER_ID,
    )

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = build_employee()

    attendance_record_repository = Mock()
    attendance_record_repository.get_by_employee_and_date.return_value = (
        existing_record
    )

    attendance_event_repository = Mock()
    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(DuplicateResourceException):
        await use_case.execute(
            build_command()
        )

    attendance_record_repository.save.assert_not_called()
    attendance_event_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


# =============================================================================
# Employee Validation
# =============================================================================


@pytest.mark.asyncio
async def test_clock_in_rejects_unknown_employee() -> None:
    """
    Clock-in should fail when the employee does not exist.
    """

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = None

    attendance_record_repository = Mock()
    attendance_event_repository = Mock()

    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(
            build_command()
        )

    employee_repository.get_by_id.assert_called_once_with(
        EMPLOYEE_ID,
    )

    attendance_record_repository.save.assert_not_called()
    attendance_event_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


@pytest.mark.asyncio
async def test_clock_in_rejects_employee_from_different_tenant() -> None:
    """
    Clock-in should reject an employee belonging to another tenant.
    """

    employee = build_employee()
    employee.tenant_id = "01OTHER00000000000000000000"

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = employee

    attendance_record_repository = Mock()
    attendance_event_repository = Mock()

    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ValueError, match="tenant"):
        await use_case.execute(
            build_command()
        )

    attendance_record_repository.save.assert_not_called()
    attendance_event_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


# =============================================================================
# Command Validation
# =============================================================================


@pytest.mark.asyncio
async def test_clock_in_rejects_missing_tenant_id() -> None:
    """
    tenant_id is required.
    """

    command = ClockInCommand(
        tenant_id="",
        employee_id=EMPLOYEE_ID,
        clock_in_at=CLOCK_IN_AT,
    )

    use_case = build_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_clock_in_rejects_missing_employee_id() -> None:
    """
    employee_id is required.
    """

    command = ClockInCommand(
        tenant_id=TENANT_ID,
        employee_id="",
        clock_in_at=CLOCK_IN_AT,
    )

    use_case = build_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_clock_in_rejects_naive_timestamp() -> None:
    """
    A supplied clock-in timestamp must be timezone-aware.
    """

    naive_timestamp = datetime(
        2026,
        8,
        24,
        8,
        30,
    )

    command = ClockInCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        clock_in_at=naive_timestamp,
    )

    use_case = build_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_clock_in_allows_missing_timestamp_for_clock_resolution() -> None:
    """
    clock_in_at is optional because the application Clock can provide it.
    """

    clock = Mock()
    clock.now.return_value = CLOCK_IN_AT

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = build_employee()

    attendance_record_repository = Mock()
    attendance_record_repository.get_by_employee_and_date.return_value = None

    attendance_event_repository = Mock()

    id_generator = Mock()
    id_generator.generate.side_effect = [
        ATTENDANCE_RECORD_ID,
        ATTENDANCE_EVENT_ID,
    ]

    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
    )

    response = await use_case.execute(
        build_command(
            clock_in_at=None,
        )
    )

    assert response.clock_in_at == CLOCK_IN_AT
    clock.now.assert_called_once()


@pytest.mark.asyncio
async def test_clock_in_rejects_blank_event_source() -> None:
    """
    event_source must contain a non-whitespace value.
    """

    command = build_command(
        event_source="   ",
    )

    use_case = build_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(command)


# =============================================================================
# Event Source
# =============================================================================


@pytest.mark.asyncio
async def test_clock_in_persists_custom_event_source() -> None:
    """
    The requested event source should be stored on the attendance event.
    """

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = build_employee()

    attendance_record_repository = Mock()
    attendance_record_repository.get_by_employee_and_date.return_value = None

    attendance_event_repository = Mock()

    id_generator = Mock()
    id_generator.generate.side_effect = [
        ATTENDANCE_RECORD_ID,
        ATTENDANCE_EVENT_ID,
    ]

    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
    )

    await use_case.execute(
        build_command(
            event_source="mobile",
        )
    )

    saved_event = (
        attendance_event_repository.save.call_args.args[0]
    )

    assert saved_event.event_source == "mobile"


# =============================================================================
# Transaction
# =============================================================================


@pytest.mark.asyncio
async def test_clock_in_persists_record_and_event_in_same_unit_of_work() -> None:
    """
    Attendance record and event should be persisted within the same
    UnitOfWork transaction.
    """

    employee_repository = Mock()
    employee_repository.get_by_id.return_value = build_employee()

    attendance_record_repository = Mock()
    attendance_record_repository.get_by_employee_and_date.return_value = None

    attendance_event_repository = Mock()

    id_generator = Mock()
    id_generator.generate.side_effect = [
        ATTENDANCE_RECORD_ID,
        ATTENDANCE_EVENT_ID,
    ]

    unit_of_work = build_unit_of_work()

    use_case = build_use_case(
        employee_repository=employee_repository,
        attendance_record_repository=attendance_record_repository,
        attendance_event_repository=attendance_event_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
    )

    await use_case.execute(
        build_command()
    )

    unit_of_work.__enter__.assert_called_once()
    unit_of_work.flush.assert_called_once()
    unit_of_work.__exit__.assert_called_once()

    attendance_record_repository.save.assert_called_once()
    attendance_event_repository.save.assert_called_once()