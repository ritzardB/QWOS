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
from qwos.api.contracts.responses.attendance.clock_in_response import (
    ClockInResponse,
)
from qwos.application.attendance.mappers.clock_in_mapper import (
    ClockInMapper,
)
from qwos.application.attendance.use_cases.clock_in_use_case import (
    ClockInUseCase,
)
from qwos.application.common.context.request_context import (
    RequestContext,
)
from qwos.application.common.dependencies.attendance import (
    get_clock_in_use_case,
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