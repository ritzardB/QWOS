"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_work_schedule_day_use_case.py

Description:
    Creates a work schedule day rule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.create_work_schedule_day_command import (
    CreateWorkScheduleDayCommand,
)
from qwos.application.attendance.responses.create_work_schedule_day_response import (
    CreateWorkScheduleDayResponse,
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
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.domains.attendance.models.work_schedule_day import WorkScheduleDay
from qwos.domains.attendance.repositories.work_schedule_day_repository import (
    WorkScheduleDayRepository,
)
from qwos.domains.attendance.repositories.work_schedule_repository import (
    WorkScheduleRepository,
)


class CreateWorkScheduleDayUseCase:
    """
    Use case for creating a work schedule day.
    """

    def __init__(
        self,
        *,
        work_schedule_repository: WorkScheduleRepository,
        work_schedule_day_repository: WorkScheduleDayRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateWorkScheduleDayValidator,
        request_context: RequestContext,
    ) -> None:
        self._work_schedule_repository = work_schedule_repository
        self._work_schedule_day_repository = work_schedule_day_repository
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateWorkScheduleDayCommand,
    ) -> CreateWorkScheduleDayResponse:
        """
        Create a work schedule day rule.
        """

        # ------------------------------------------------------------------
        # Validate command
        # ------------------------------------------------------------------

        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        # ------------------------------------------------------------------
        # Locate work schedule
        # ------------------------------------------------------------------

        work_schedule = self._work_schedule_repository.get_by_id_for_tenant(
            tenant_id=command.tenant_id,
            schedule_id=command.work_schedule_id,
        )

        if work_schedule is None:
            raise ResourceNotFoundException(
                resource="WorkSchedule",
                identifier=command.work_schedule_id,
            )

        # ------------------------------------------------------------------
        # Duplicate day check
        # ------------------------------------------------------------------

        if self._work_schedule_day_repository.exists_by_schedule_and_day(
            tenant_id=command.tenant_id,
            work_schedule_id=command.work_schedule_id,
            day_of_week=command.day_of_week,
        ):
            raise DuplicateResourceException(
                resource="WorkScheduleDay",
                field="day_of_week",
                value=str(command.day_of_week),
            )

        # ------------------------------------------------------------------
        # Generate identifier
        # ------------------------------------------------------------------

        schedule_day_id = self._id_generator.generate()

        # ------------------------------------------------------------------
        # Create schedule day
        # ------------------------------------------------------------------

        schedule_day = WorkScheduleDay.create(
            id=schedule_day_id,
            tenant_id=command.tenant_id,
            work_schedule_id=work_schedule.id,
            day_of_week=command.day_of_week,
            day_type=command.day_type,
            start_time=command.start_time,
            end_time=command.end_time,
            break_minutes=command.break_minutes,
            is_overnight=command.is_overnight,
            created_by=self._request_context.user_id,
        )

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._work_schedule_day_repository.save(
                schedule_day,
            )
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return CreateWorkScheduleDayResponse(
            id=schedule_day.id,
            work_schedule_id=schedule_day.work_schedule_id,
            day_of_week=schedule_day.day_of_week,
            day_type=schedule_day.day_type,
            start_time=schedule_day.start_time,
            end_time=schedule_day.end_time,
            break_minutes=schedule_day.break_minutes,
            is_overnight=schedule_day.is_overnight,
            created_at=schedule_day.created_at,
        )
