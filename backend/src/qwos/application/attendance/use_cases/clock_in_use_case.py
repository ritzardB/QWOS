"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    clock_in_use_case.py

Description:
    Application use case for clocking in an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.clock_in_command import (
    ClockInCommand,
)
from qwos.application.attendance.responses.clock_in_response import (
    ClockInResponse,
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
from qwos.application.common.persistence.unit_of_work import (
    UnitOfWork,
)
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.domains.attendance.models.attendance_event import (
    AttendanceEvent,
)
from qwos.domains.attendance.models.attendance_record import (
    AttendanceRecord,
)
from qwos.domains.attendance.repositories.attendance_event_repository import (
    AttendanceEventRepository,
)
from qwos.domains.attendance.repositories.attendance_record_repository import (
    AttendanceRecordRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class ClockInUseCase:
    """
    Clock an employee in for the attendance day.

    The use case:

    1. Validates the command.
    2. Resolves the clock-in timestamp.
    3. Verifies that the employee exists.
    4. Verifies tenant ownership.
    5. Retrieves or creates the daily attendance record.
    6. Prevents duplicate clock-in events.
    7. Creates the clock-in attendance event.
    8. Persists the changes atomically.
    9. Returns the clock-in response.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        attendance_record_repository: AttendanceRecordRepository,
        attendance_event_repository: AttendanceEventRepository,
        id_generator: IdGenerator,
        clock: Clock,
        unit_of_work: UnitOfWork,
        validator: ClockInValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._attendance_record_repository = attendance_record_repository
        self._attendance_event_repository = attendance_event_repository
        self._id_generator = id_generator
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: ClockInCommand,
    ) -> ClockInResponse:
        # ---------------------------------------------------------------------
        # Validation
        # ---------------------------------------------------------------------

        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        # ---------------------------------------------------------------------
        # Resolve clock-in timestamp
        # ---------------------------------------------------------------------

        clock_in_at = command.clock_in_at

        if clock_in_at is None:
            clock_in_at = self._clock.now()

        if clock_in_at.tzinfo is None:
            raise ValueError(
                "clock_in_at must be timezone-aware.",
            )

        attendance_date = clock_in_at.date()

        # ---------------------------------------------------------------------
        # Employee
        # ---------------------------------------------------------------------

        employee = self._employee_repository.get_by_id(
            command.employee_id,
        )

        if employee is None:
            raise ResourceNotFoundException(
                resource="Employee",
                identifier=command.employee_id,
            )

        if employee.tenant_id != command.tenant_id:
            raise ValueError(
                "Employee does not belong to the requested tenant.",
            )

        # ---------------------------------------------------------------------
        # Existing attendance record
        # ---------------------------------------------------------------------

        attendance_record = self._attendance_record_repository.get_by_employee_and_date(
            tenant_id=command.tenant_id,
            employee_id=command.employee_id,
            attendance_date=attendance_date,
        )

        # ---------------------------------------------------------------------
        # Duplicate clock-in protection
        # ---------------------------------------------------------------------

        if attendance_record is not None:
            if attendance_record.clock_in_at is not None:
                raise DuplicateResourceException(
                    resource="AttendanceRecord",
                    field="clock_in_at",
                    value=command.employee_id,
                )

            attendance_record.clock_in_at = clock_in_at

        else:
            # -----------------------------------------------------------------
            # Create the daily attendance record.
            # -----------------------------------------------------------------

            attendance_record = AttendanceRecord.create(
                id=self._id_generator.generate(),
                tenant_id=command.tenant_id,
                employee_id=command.employee_id,
                attendance_date=attendance_date,
                clock_in_at=clock_in_at,
                status="present",
                created_by=self._request_context.user_id,
            )

        # ---------------------------------------------------------------------
        # Create attendance event
        # ---------------------------------------------------------------------

        attendance_event = AttendanceEvent.create(
            id=self._id_generator.generate(),
            tenant_id=command.tenant_id,
            attendance_record_id=attendance_record.id,
            employee_id=command.employee_id,
            event_type="clock_in",
            event_at=clock_in_at,
            event_source=command.event_source,
            notes=command.notes,
            created_by=self._request_context.user_id,
        )

        # ---------------------------------------------------------------------
        # Persist atomically
        # ---------------------------------------------------------------------

        with self._unit_of_work:
            self._attendance_record_repository.save(
                attendance_record,
            )

            # Ensure the attendance record exists before
            # inserting the event that references it.
            self._unit_of_work.flush()

            self._attendance_event_repository.save(
                attendance_event,
            )

            self._unit_of_work.flush()

        # ---------------------------------------------------------------------
        # Response
        # ---------------------------------------------------------------------

        return ClockInResponse(
            attendance_record_id=attendance_record.id,
            attendance_event_id=attendance_event.id,
            employee_id=attendance_record.employee_id,
            attendance_date=attendance_record.attendance_date,
            clock_in_at=attendance_record.clock_in_at,
            status=attendance_record.status,
            event_type=attendance_event.event_type,
            event_at=attendance_event.event_at,
        )
