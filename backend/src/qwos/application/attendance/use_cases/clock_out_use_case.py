"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    clock_out_use_case.py

Description:
    Application use case for clocking out an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.clock_out_command import (
    ClockOutCommand,
)
from qwos.application.attendance.responses.clock_out_response import (
    ClockOutResponse,
)
from qwos.application.attendance.validators.clock_out_validator import (
    ClockOutValidator,
)
from qwos.application.common.context.request_context import (
    RequestContext,
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
from qwos.domains.attendance.repositories.attendance_event_repository import (
    AttendanceEventRepository,
)
from qwos.domains.attendance.repositories.attendance_record_repository import (
    AttendanceRecordRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class ClockOutUseCase:
    """
    Clock an employee out for the attendance day.
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
        validator: ClockOutValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._attendance_record_repository = (
            attendance_record_repository
        )
        self._attendance_event_repository = (
            attendance_event_repository
        )
        self._id_generator = id_generator
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: ClockOutCommand,
    ) -> ClockOutResponse:
        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        clock_out_at = command.clock_out_at

        if clock_out_at is None:
            clock_out_at = self._clock.now()

        if clock_out_at.tzinfo is None:
            raise ValueError(
                "clock_out_at must be timezone-aware.",
            )

        attendance_date = clock_out_at.date()

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

        attendance_record = (
            self._attendance_record_repository
            .get_by_employee_and_date(
                tenant_id=command.tenant_id,
                employee_id=command.employee_id,
                attendance_date=attendance_date,
            )
        )

        if attendance_record is None:
            raise ResourceNotFoundException(
                resource="AttendanceRecord",
                identifier=command.employee_id,
            )

        if attendance_record.clock_in_at is None:
            raise ValueError(
                "Employee must clock in before clocking out.",
            )

        if attendance_record.clock_out_at is not None:
            raise ValueError(
                "Employee has already clocked out.",
            )

        if clock_out_at < attendance_record.clock_in_at:
            raise ValueError(
                "clock_out_at cannot be earlier than clock_in_at.",
            )

        worked_minutes = int(
            (
                clock_out_at
                - attendance_record.clock_in_at
            ).total_seconds()
            // 60
        )

        attendance_record.clock_out_at = clock_out_at
        attendance_record.worked_minutes = worked_minutes

        attendance_event = AttendanceEvent.create(
            id=self._id_generator.generate(),
            tenant_id=command.tenant_id,
            attendance_record_id=attendance_record.id,
            employee_id=command.employee_id,
            event_type="clock_out",
            event_at=clock_out_at,
            event_source=command.event_source,
            notes=command.notes,
            created_by=self._request_context.user_id,
        )

        with self._unit_of_work:
            self._attendance_record_repository.save(
                attendance_record,
            )

            self._attendance_event_repository.save(
                attendance_event,
            )

            self._unit_of_work.flush()

        return ClockOutResponse(
            attendance_record_id=attendance_record.id,
            attendance_event_id=attendance_event.id,
            employee_id=attendance_record.employee_id,
            attendance_date=attendance_record.attendance_date,
            clock_in_at=attendance_record.clock_in_at,
            clock_out_at=attendance_record.clock_out_at,
            worked_minutes=attendance_record.worked_minutes,
            status=attendance_record.status,
            event_type=attendance_event.event_type,
            event_at=attendance_event.event_at,
        )
    