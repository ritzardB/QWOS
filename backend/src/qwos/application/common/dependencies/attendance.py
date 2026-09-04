"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Common Dependencies

Attendance Dependencies

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import Depends

from qwos.application.attendance.use_cases.clock_in_use_case import (
    ClockInUseCase,
)
from qwos.application.attendance.use_cases.clock_out_use_case import (
    ClockOutUseCase,
)
from qwos.application.attendance.use_cases.create_employee_work_arrangement_use_case import (
    CreateEmployeeWorkArrangementUseCase,
)
from qwos.application.attendance.use_cases.create_employee_work_schedule_use_case import (
    CreateEmployeeWorkScheduleUseCase,
)
from qwos.application.attendance.use_cases.create_work_schedule_day_use_case import (
    CreateWorkScheduleDayUseCase,
)
from qwos.application.attendance.use_cases.create_work_schedule_use_case import (
    CreateWorkScheduleUseCase,
)
from qwos.application.attendance.use_cases.get_work_schedule_use_case import (
    GetWorkScheduleUseCase,
)
from qwos.application.attendance.use_cases.list_attendance_history_use_case import (
    ListAttendanceHistoryUseCase,
)
from qwos.application.attendance.use_cases.list_work_schedule_days_use_case import (
    ListWorkScheduleDaysUseCase,
)
from qwos.application.attendance.use_cases.list_work_schedules_use_case import (
    ListWorkSchedulesUseCase,
)
from qwos.application.attendance.validators.clock_in_validator import (
    ClockInValidator,
)
from qwos.application.attendance.validators.clock_out_validator import (
    ClockOutValidator,
)
from qwos.application.attendance.validators.create_employee_work_arrangement_validator import (
    CreateEmployeeWorkArrangementValidator,
)
from qwos.application.attendance.validators.create_employee_work_schedule_validator import (
    CreateEmployeeWorkScheduleValidator,
)
from qwos.application.attendance.validators.create_work_schedule_day_validator import (
    CreateWorkScheduleDayValidator,
)
from qwos.application.attendance.validators.create_work_schedule_validator import (
    CreateWorkScheduleValidator,
)
from qwos.application.common.context.request_context import (
    RequestContext,
)
from qwos.application.common.dependencies.authentication import get_authenticated_request_context
from qwos.application.common.dependencies.common import (
    get_clock,
    get_id_generator,
    get_request_context,
    get_unit_of_work,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.domains.identity.models.session import Session
from qwos.infrastructure.repositories.attendance.sqlalchemy_attendance_event_repository import (
    SQLAlchemyAttendanceEventRepository,
)
from qwos.infrastructure.repositories.attendance.sqlalchemy_attendance_record_repository import (
    SQLAlchemyAttendanceRecordRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_repository import (
    SQLAlchemyEmployeeRepository,
)


def __init__(
    self,
    session: Session,
) -> None:
    self._session = session

    self.employee_repository = SQLAlchemyEmployeeRepository(
        session,
    )

    self.attendance_record_repository = (
        SQLAlchemyAttendanceRecordRepository(
            session,
        )
    )

    self.attendance_event_repository = (
        SQLAlchemyAttendanceEventRepository(
            session,
        )
    )

def get_clock_in_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    clock: Clock = Depends(get_clock),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: ClockInValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> ClockInUseCase:
    """
    Provide the ClockInUseCase instance.
    """

    return ClockInUseCase(
        employee_repository=unit_of_work.employee_repository,
        attendance_record_repository=(unit_of_work.attendance_record_repository),
        attendance_event_repository=(unit_of_work.attendance_event_repository),
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )


def get_clock_out_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    clock: Clock = Depends(get_clock),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: ClockOutValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> ClockOutUseCase:
    """
    Provide the ClockOutUseCase instance.
    """

    return ClockOutUseCase(
        employee_repository=unit_of_work.employee_repository,
        attendance_record_repository=(unit_of_work.attendance_record_repository),
        attendance_event_repository=(unit_of_work.attendance_event_repository),
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

def get_authenticated_employee_id(
    request_context: RequestContext = Depends(
        get_authenticated_request_context
    ),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> str:
    if request_context.user_id is None:
        raise ValueError("Authenticated user is required.")

    employee = unit_of_work.employee_repository.get_by_user_id(
        tenant_id=request_context.tenant_id,
        user_id=request_context.user_id,
    )

    if employee is None:
        raise ResourceNotFoundException(
            resource="Employee",
            identifier=request_context.user_id,
        )

    return employee.id

def get_create_employee_work_arrangement_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: CreateEmployeeWorkArrangementValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> CreateEmployeeWorkArrangementUseCase:
    """
    Provide the CreateEmployeeWorkArrangementUseCase instance.
    """

    return CreateEmployeeWorkArrangementUseCase(
        employee_repository=unit_of_work.employee_repository,
        employee_work_arrangement_repository=(unit_of_work.employee_work_arrangement_repository),
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )


def get_create_employee_work_schedule_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: CreateEmployeeWorkScheduleValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> CreateEmployeeWorkScheduleUseCase:
    """
    Provide the CreateEmployeeWorkScheduleUseCase instance.
    """

    return CreateEmployeeWorkScheduleUseCase(
        employee_repository=unit_of_work.employee_repository,
        work_schedule_repository=(unit_of_work.work_schedule_repository),
        employee_work_schedule_repository=(unit_of_work.employee_work_schedule_repository),
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )


def get_create_work_schedule_day_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: CreateWorkScheduleDayValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> CreateWorkScheduleDayUseCase:
    """
    Provide the CreateWorkScheduleDayUseCase instance.
    """

    return CreateWorkScheduleDayUseCase(
        work_schedule_repository=unit_of_work.work_schedule_repository,
        work_schedule_day_repository=(unit_of_work.work_schedule_day_repository),
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )


def get_list_work_schedules_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    request_context: RequestContext = Depends(get_request_context),
) -> ListWorkSchedulesUseCase:
    """
    Provide the ListWorkSchedulesUseCase instance.
    """

    return ListWorkSchedulesUseCase(
        work_schedule_repository=unit_of_work.work_schedule_repository,
        request_context=request_context,
    )


def get_work_schedule_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    request_context: RequestContext = Depends(get_request_context),
) -> GetWorkScheduleUseCase:
    """
    Provide the GetWorkScheduleUseCase instance.
    """

    return GetWorkScheduleUseCase(
        work_schedule_repository=unit_of_work.work_schedule_repository,
        request_context=request_context,
    )


def get_list_work_schedule_days_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    request_context: RequestContext = Depends(get_request_context),
) -> ListWorkScheduleDaysUseCase:
    """
    Provide the ListWorkScheduleDaysUseCase instance.
    """

    return ListWorkScheduleDaysUseCase(
        work_schedule_repository=unit_of_work.work_schedule_repository,
        work_schedule_day_repository=(unit_of_work.work_schedule_day_repository),
        request_context=request_context,
    )

def get_list_attendance_history_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    request_context: RequestContext = Depends(
        get_authenticated_request_context
        ),
) -> ListAttendanceHistoryUseCase:
    """
    Provide the ListAttendanceHistoryUseCase instance.
    """

    return ListAttendanceHistoryUseCase(
        attendance_record_repository=unit_of_work.attendance_record_repository,
        employee_repository=unit_of_work.employee_repository,
        request_context=request_context,
    )

def get_create_work_schedule_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: CreateWorkScheduleValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> CreateWorkScheduleUseCase:
    """
    Provide the CreateWorkScheduleUseCase instance.
    """

    return CreateWorkScheduleUseCase(
        work_schedule_repository=unit_of_work.work_schedule_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )