"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Leave Router

Description:
    REST API endpoints for Leave management.

Responsibilities:
    - Receive HTTP requests
    - Delegate to Leave application use cases
    - Return HTTP responses
    - No business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from qwos.api.contracts.requests.leave.create_leave_type_request import (
    CreateLeaveTypeRequest,
)
from qwos.api.contracts.responses.leave.create_leave_type_response import (
    CreateLeaveTypeResponse,
)
from qwos.api.contracts.responses.leave.create_leave_policy_response import (
    CreateLeavePolicyResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.api.contracts.requests.leave.create_leave_policy_request import (
    CreateLeavePolicyRequest,
)
from qwos.application.common.dependencies.leave import (
    get_create_leave_policy_use_case,
)
from qwos.application.common.dependencies.leave import (
    get_create_leave_type_use_case,
)
from qwos.application.leave.mappers.leave_type_mapper import (
    LeaveTypeMapper,
)
from qwos.application.leave.use_cases.create_leave_type_use_case import (
    CreateLeaveTypeUseCase,
)
from qwos.application.leave.mappers.leave_policy_mapper import LeavePolicyMapper
from qwos.application.leave.use_cases.create_leave_policy_use_case import (
    CreateLeavePolicyUseCase,
)

router = APIRouter(
    prefix="/leave",
    tags=["Leave"],
)


# -------------------------------------------------------------------------
# Create Leave Type
# -------------------------------------------------------------------------


@router.post(
    "/types",
    response_model=CreateLeaveTypeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Leave Type",
    description="Create a tenant-defined leave type.",
)
async def create_leave_type(
    request: CreateLeaveTypeRequest,
    request_context: RequestContext = Depends(
        get_authenticated_request_context,
    ),
    use_case: CreateLeaveTypeUseCase = Depends(
        get_create_leave_type_use_case,
    ),
) -> CreateLeaveTypeResponse:
    """
    Create a leave type.
    """

    command = LeaveTypeMapper.to_create_command(
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(
        command,
    )

    return LeaveTypeMapper.to_create_response(
        application_response,
    )

@router.post(
    "/policies",
    response_model=CreateLeavePolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Leave Policy",
    description="Create a tenant-defined leave policy.",
)
async def create_leave_policy(
    request: CreateLeavePolicyRequest,
    request_context: RequestContext = Depends(
        get_authenticated_request_context
    ),
    use_case: CreateLeavePolicyUseCase = Depends(
        get_create_leave_policy_use_case
    ),
) -> CreateLeavePolicyResponse:
    command = LeavePolicyMapper.to_create_command(
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(command)

    return LeavePolicyMapper.to_create_response(application_response)
