"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Router

Description:
    REST API endpoints for Attendance management.

Responsibilities:
    - Receive HTTP requests
    - Delegate to Attendance application use cases
    - Return HTTP responses
    - No business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from qwos.api.contracts.requests.attendance.clock_in_request import (
    ClockInRequest,
)
from qwos.api.contracts.requests.attendance.clock_out_request import (
    ClockOutRequest,
)
from qwos.api.contracts.requests.attendance.create_employee_work_arrangement_request import (
    CreateEmployeeWorkArrangementRequest,
)
from qwos.api.contracts.requests.attendance.create_employee_work_schedule_request import (
    CreateEmployeeWorkScheduleRequest,
)
from qwos.api.contracts.requests.attendance.create_work_schedule_day_request import (
    CreateWorkScheduleDayRequest,
)
from qwos.api.contracts.responses.attendance.clock_in_response import (
    ClockInResponse,
)
from qwos.api.contracts.responses.attendance.clock_out_response import (
    ClockOutResponse,
)
from qwos.api.contracts.responses.attendance.create_employee_work_arrangement_response import (
    CreateEmployeeWorkArrangementResponse,
)
from qwos.api.contracts.responses.attendance.create_employee_work_schedule_response import (
    CreateEmployeeWorkScheduleResponse,
)
from qwos.api.contracts.responses.attendance.create_work_schedule_day_response import (
    CreateWorkScheduleDayResponse,
)
from qwos.api.contracts.responses.attendance.get_work_schedule_response import (
    GetWorkScheduleResponse,
)
from qwos.api.contracts.responses.attendance.list_work_schedule_days_response import (
    ListWorkScheduleDaysResponse,
)
from qwos.api.contracts.responses.attendance.list_work_schedules_response import (
    ListWorkSchedulesResponse,
)
from qwos.application.attendance.mappers.clock_in_mapper import (
    ClockInMapper,
)
from qwos.application.attendance.mappers.clock_out_mapper import (
    ClockOutMapper,
)
from qwos.application.attendance.mappers.employee_work_arrangement_mapper import (
    EmployeeWorkArrangementMapper,
)
from qwos.application.attendance.mappers.employee_work_schedule_mapper import (
    EmployeeWorkScheduleMapper,
)
from qwos.application.attendance.mappers.work_schedule_day_mapper import (
    WorkScheduleDayMapper,
)
from qwos.application.attendance.mappers.work_schedule_mapper import (
    WorkScheduleMapper,
)
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
from qwos.application.attendance.use_cases.get_work_schedule_use_case import (
    GetWorkScheduleUseCase,
)
from qwos.application.attendance.use_cases.list_work_schedule_days_use_case import (
    ListWorkScheduleDaysUseCase,
)
from qwos.application.attendance.use_cases.list_work_schedules_use_case import (
    ListWorkSchedulesUseCase,
)
from qwos.application.common.context.request_context import (
    RequestContext,
)
from qwos.application.common.dependencies.attendance import (
    get_clock_in_use_case,
    get_clock_out_use_case,
    get_create_employee_work_arrangement_use_case,
    get_create_employee_work_schedule_use_case,
    get_create_work_schedule_day_use_case,
    get_list_work_schedule_days_use_case,
    get_list_work_schedules_use_case,
    get_work_schedule_use_case,
)
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


# -------------------------------------------------------------------------
# Clock In
# -------------------------------------------------------------------------


@router.post(
    "/clock-in",
    response_model=ClockInResponse,
    status_code=status.HTTP_200_OK,
    summary="Clock In",
    description="Clock in an employee.",
)
async def clock_in(
    request: ClockInRequest,
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: ClockInUseCase = Depends(
        get_clock_in_use_case,
    ),
) -> ClockInResponse:
    """
    Clock in an employee.
    """

    command = ClockInMapper.to_command(
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(
        command,
    )

    return ClockInMapper.to_response(
        application_response,
    )


# -------------------------------------------------------------------------
# Clock Out
# -------------------------------------------------------------------------


@router.post(
    "/clock-out",
    response_model=ClockOutResponse,
    status_code=status.HTTP_200_OK,
    summary="Clock Out",
    description="Clock out an employee.",
)
async def clock_out(
    request: ClockOutRequest,
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: ClockOutUseCase = Depends(
        get_clock_out_use_case,
    ),
) -> ClockOutResponse:
    """
    Clock out an employee.
    """

    command = ClockOutMapper.to_command(
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(
        command,
    )

    return ClockOutMapper.to_response(
        application_response,
    )


# -------------------------------------------------------------------------
# Create Employee Work Arrangement
# -------------------------------------------------------------------------


@router.post(
    "/employees/{employee_id}/work-arrangements",
    response_model=CreateEmployeeWorkArrangementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee Work Arrangement",
    description="Create an effective-dated work arrangement for an employee.",
)
async def create_employee_work_arrangement(
    employee_id: str,
    request: CreateEmployeeWorkArrangementRequest,
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: CreateEmployeeWorkArrangementUseCase = Depends(
        get_create_employee_work_arrangement_use_case,
    ),
) -> CreateEmployeeWorkArrangementResponse:
    """
    Create an employee work arrangement.
    """

    command = EmployeeWorkArrangementMapper.to_create_command(
        employee_id=employee_id,
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(
        command,
    )

    return EmployeeWorkArrangementMapper.to_create_response(
        application_response,
    )


# -------------------------------------------------------------------------
# Create Employee Work Schedule
# -------------------------------------------------------------------------


@router.post(
    "/employees/{employee_id}/work-schedules",
    response_model=CreateEmployeeWorkScheduleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee Work Schedule",
    description=("Create an effective-dated work schedule assignment for an employee."),
)
async def create_employee_work_schedule(
    employee_id: str,
    request: CreateEmployeeWorkScheduleRequest,
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: CreateEmployeeWorkScheduleUseCase = Depends(
        get_create_employee_work_schedule_use_case,
    ),
) -> CreateEmployeeWorkScheduleResponse:
    """
    Create an employee work schedule assignment.
    """

    command = EmployeeWorkScheduleMapper.to_create_command(
        employee_id=employee_id,
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(
        command,
    )

    return EmployeeWorkScheduleMapper.to_create_response(
        application_response,
    )


# -------------------------------------------------------------------------
# Create Work Schedule Day
# -------------------------------------------------------------------------


@router.post(
    "/work-schedules/{work_schedule_id}/days",
    response_model=CreateWorkScheduleDayResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Work Schedule Day",
    description="Create a weekly day rule for a work schedule.",
)
async def create_work_schedule_day(
    work_schedule_id: str,
    request: CreateWorkScheduleDayRequest,
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: CreateWorkScheduleDayUseCase = Depends(
        get_create_work_schedule_day_use_case,
    ),
) -> CreateWorkScheduleDayResponse:
    """
    Create a work schedule day rule.
    """

    command = WorkScheduleDayMapper.to_create_command(
        work_schedule_id=work_schedule_id,
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(
        command,
    )

    return WorkScheduleDayMapper.to_create_response(
        application_response,
    )


# -------------------------------------------------------------------------
# List Work Schedules
# -------------------------------------------------------------------------


@router.get(
    "/work-schedules",
    response_model=ListWorkSchedulesResponse,
    status_code=status.HTTP_200_OK,
    summary="List Work Schedules",
    description="List work schedules for the current tenant.",
)
async def list_work_schedules(
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: ListWorkSchedulesUseCase = Depends(
        get_list_work_schedules_use_case,
    ),
) -> ListWorkSchedulesResponse:
    """
    List work schedules for the current tenant.
    """

    application_response = await use_case.execute()

    return WorkScheduleMapper.to_list_response(
        application_response,
    )


# -------------------------------------------------------------------------
# Get Work Schedule
# -------------------------------------------------------------------------


@router.get(
    "/work-schedules/{work_schedule_id}",
    response_model=GetWorkScheduleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Work Schedule",
    description="Retrieve a work schedule for the current tenant.",
)
async def get_work_schedule(
    work_schedule_id: str,
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: GetWorkScheduleUseCase = Depends(
        get_work_schedule_use_case,
    ),
) -> GetWorkScheduleResponse:
    """
    Retrieve a work schedule for the current tenant.
    """

    application_response = await use_case.execute(
        work_schedule_id,
    )

    return WorkScheduleMapper.to_get_response(
        application_response,
    )


# -------------------------------------------------------------------------
# List Work Schedule Days
# -------------------------------------------------------------------------


@router.get(
    "/work-schedules/{work_schedule_id}/days",
    response_model=ListWorkScheduleDaysResponse,
    status_code=status.HTTP_200_OK,
    summary="List Work Schedule Days",
    description="List weekly day rules for a work schedule.",
)
async def list_work_schedule_days(
    work_schedule_id: str,
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: ListWorkScheduleDaysUseCase = Depends(
        get_list_work_schedule_days_use_case,
    ),
) -> ListWorkScheduleDaysResponse:
    """
    List weekly day rules for a work schedule.
    """

    application_response = await use_case.execute(
        work_schedule_id,
    )

    return WorkScheduleDayMapper.to_list_response(
        application_response,
    )
