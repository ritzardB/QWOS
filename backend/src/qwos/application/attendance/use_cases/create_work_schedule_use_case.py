from __future__ import annotations

from qwos.application.attendance.commands.create_work_schedule_command import (
    CreateWorkScheduleCommand,
)
from qwos.application.attendance.responses.create_work_schedule_response import (
    CreateWorkScheduleResponse,
)
from qwos.application.attendance.validators.create_work_schedule_validator import (
    CreateWorkScheduleValidator,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.domains.attendance.models.work_schedule import WorkSchedule
from qwos.domains.attendance.repositories.work_schedule_repository import (
    WorkScheduleRepository,
)


class CreateWorkScheduleUseCase:
    """
    Use case for creating a master work schedule.
    """

    def __init__(
        self,
        *,
        work_schedule_repository: WorkScheduleRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateWorkScheduleValidator,
        request_context: RequestContext,
    ) -> None:
        self._work_schedule_repository = work_schedule_repository
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateWorkScheduleCommand,
    ) -> CreateWorkScheduleResponse:
        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        normalized_code = command.schedule_code.strip().lower()

        if self._work_schedule_repository.exists_by_code(
            tenant_id=command.tenant_id,
            schedule_code=normalized_code,
        ):
            raise DuplicateResourceException(
                resource="WorkSchedule",
                field="schedule_code",
                value=normalized_code,
            )

        schedule_id = self._id_generator.generate()

        schedule = WorkSchedule.create(
            id=schedule_id,
            tenant_id=command.tenant_id,
            schedule_code=command.schedule_code,
            schedule_name=command.schedule_name,
            timezone=command.timezone,
            is_active=command.is_active,
            created_by=self._request_context.user_id,
        )

        with self._unit_of_work:
            self._work_schedule_repository.save(schedule)
            self._unit_of_work.flush()

        return CreateWorkScheduleResponse(
            id=schedule.id,
            schedule_code=schedule.schedule_code,
            schedule_name=schedule.schedule_name,
            timezone=schedule.timezone,
            is_active=schedule.is_active,
            created_at=schedule.created_at,
        )