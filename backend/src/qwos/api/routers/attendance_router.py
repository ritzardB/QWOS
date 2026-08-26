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
from qwos.api.contracts.requests.attendance.create_employee_work_arrangement_request import (
    CreateEmployeeWorkArrangementRequest,
)
from qwos.api.contracts.responses.attendance.clock_in_response import (
    ClockInResponse,
)
from qwos.api.contracts.responses.attendance.create_employee_work_arrangement_response import (
    CreateEmployeeWorkArrangementResponse,
)
from qwos.application.attendance.mappers.clock_in_mapper import (
    ClockInMapper,
)
from qwos.application.attendance.mappers.employee_work_arrangement_mapper import (
    EmployeeWorkArrangementMapper,
)
from qwos.application.attendance.use_cases.clock_in_use_case import (
    ClockInUseCase,
)
from qwos.application.attendance.use_cases.create_employee_work_arrangement_use_case import (
    CreateEmployeeWorkArrangementUseCase,
)
from qwos.application.common.context.request_context import (
    RequestContext,
)
from qwos.application.common.dependencies.attendance import (
    get_clock_in_use_case,
    get_create_employee_work_arrangement_use_case,
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
