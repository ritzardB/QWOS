"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Router

Description:
    REST API endpoints for Human Resources management.

Responsibilities:
    - Receive HTTP requests
    - Delegate to HR application use cases
    - Return HTTP responses
    - No business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from qwos.api.contracts.requests.hr.create_employee_profile_request import (
    CreateEmployeeProfileRequest,
)
from qwos.api.contracts.requests.hr.create_employee_reporting_relationship_request import (
    CreateEmployeeReportingRelationshipRequest,
)
from qwos.api.contracts.requests.hr.create_employee_request import (
    CreateEmployeeRequest,
)
from qwos.api.contracts.requests.hr.link_employee_to_user_request import (
    LinkEmployeeToUserRequest,
)
from qwos.api.contracts.responses.hr.create_employee_profile_response import (
    CreateEmployeeProfileResponse,
)
from qwos.api.contracts.responses.hr.create_employee_reporting_relationship_response import (
    CreateEmployeeReportingRelationshipResponse,
)
from qwos.api.contracts.responses.hr.create_employee_response import (
    CreateEmployeeResponse,
)
from qwos.api.contracts.responses.hr.get_employee_manager_response import (
    GetEmployeeManagerResponse,
)
from qwos.api.contracts.responses.hr.get_employee_position_response import (
    GetEmployeePositionResponse,
)
from qwos.api.contracts.responses.hr.get_employee_profile_response import (
    GetEmployeeProfileResponse,
)
from qwos.api.contracts.responses.hr.get_employee_response import (
    GetEmployeeResponse,
)
from qwos.api.contracts.responses.hr.link_employee_to_user_response import (
    LinkEmployeeToUserResponse,
)
from qwos.api.contracts.responses.hr.list_employees_response import (
    ListEmployeesResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.hr import (
    get_create_employee_profile_use_case,
    get_create_employee_reporting_relationship_use_case,
    get_create_employee_use_case,
    get_get_employee_manager_use_case,
    get_get_employee_position_use_case,
    get_get_employee_profile_use_case,
    get_get_employee_use_case,
    get_link_employee_to_user_use_case,
    get_list_employees_use_case,
    get_request_context,
)
from qwos.application.hr.mappers.employee_mapper import EmployeeMapper
from qwos.application.hr.mappers.employee_position_mapper import (
    EmployeePositionMapper,
)
from qwos.application.hr.mappers.employee_profile_mapper import (
    EmployeeProfileMapper,
)
from qwos.application.hr.mappers.employee_reporting_relationship_mapper import (
    EmployeeReportingRelationshipMapper,
)
from qwos.application.hr.mappers.link_employee_to_user_mapper import (
    LinkEmployeeToUserMapper,
)
from qwos.application.hr.use_cases.create_employee_profile_use_case import (
    CreateEmployeeProfileUseCase,
)
from qwos.application.hr.use_cases.create_employee_reporting_relationship_use_case import (
    CreateEmployeeReportingRelationshipUseCase,
)
from qwos.application.hr.use_cases.create_employee_use_case import (
    CreateEmployeeUseCase,
)
from qwos.application.hr.use_cases.get_employee_manager_use_case import (
    GetEmployeeManagerUseCase,
)
from qwos.application.hr.use_cases.get_employee_position_use_case import (
    GetEmployeePositionUseCase,
)
from qwos.application.hr.use_cases.get_employee_profile_use_case import (
    GetEmployeeProfileUseCase,
)
from qwos.application.hr.use_cases.get_employee_use_case import (
    GetEmployeeUseCase,
)
from qwos.application.hr.use_cases.link_employee_to_user_use_case import (
    LinkEmployeeToUserUseCase,
)
from qwos.application.hr.use_cases.list_employees_use_case import (
    ListEmployeesUseCase,
)

router = APIRouter(
    prefix="/hr",
    tags=["HR"],
)

@router.get(
    "/employees",
    response_model=ListEmployeesResponse,
    status_code=status.HTTP_200_OK,
    summary="List Employees",
    description="List active employees for the current tenant.",
)
async def list_employees(
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: ListEmployeesUseCase = Depends(
        get_list_employees_use_case,
    ),
) -> ListEmployeesResponse:
    """
    List active employees for the current tenant.
    """

    application_response = await use_case.execute()

    return EmployeeMapper.to_list_response(
        application_response,
    )

@router.post(
    "/employees",
    response_model=CreateEmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee",
    description="Create a new HR employee record.",
)
async def create_employee(
    request: CreateEmployeeRequest,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: CreateEmployeeUseCase = Depends(
        get_create_employee_use_case,
    ),
) -> CreateEmployeeResponse:
    """
    Create a new employee.
    """

    command = EmployeeMapper.to_create_command(
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(command)

    return EmployeeMapper.to_create_response(
        application_response,
    )

@router.post(
    "/employees/{employee_id}/profile",
    response_model=CreateEmployeeProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee Profile",
    description="Create the core HR profile for an employee.",
)
async def create_employee_profile(
    employee_id: str,
    request: CreateEmployeeProfileRequest,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: CreateEmployeeProfileUseCase = Depends(
        get_create_employee_profile_use_case,
    ),
) -> CreateEmployeeProfileResponse:
    """
    Create the core HR profile for an employee.
    """

    command = EmployeeProfileMapper.to_create_command(
        employee_id=employee_id,
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(command)

    return EmployeeProfileMapper.to_create_response(
        application_response,
    )

@router.post(
    "/employees/{employee_id}/link-user",
    response_model=LinkEmployeeToUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Link Employee to User",
    description=(
        "Link an employee to an existing QWOS user and create the "
        "corresponding user profile."
    ),
)
async def link_employee_to_user(
    employee_id: str,
    request: LinkEmployeeToUserRequest,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: LinkEmployeeToUserUseCase = Depends(
        get_link_employee_to_user_use_case,
    ),
) -> LinkEmployeeToUserResponse:
    """
    Link an employee to an existing QWOS user.
    """

    command = LinkEmployeeToUserMapper.to_command(
        employee_id=employee_id,
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(command)

    return LinkEmployeeToUserMapper.to_response(
        application_response,
    )

@router.get(
    "/employees/{employee_id}",
    response_model=GetEmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee",
    description="Retrieve an employee by ID.",
)
async def get_employee(
    employee_id: str,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: GetEmployeeUseCase = Depends(
        get_get_employee_use_case,
    ),
) -> GetEmployeeResponse:
    """
    Retrieve an employee by ID.
    """

    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        employee_id=employee_id,
    )

    return EmployeeMapper.to_get_response(
        application_response,
    )

@router.post(
    "/employees/{employee_id}/manager",
    response_model=CreateEmployeeReportingRelationshipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assign Employee Manager",
    description="Assign the reporting manager for an employee.",
)
async def assign_employee_manager(
    employee_id: str,
    request: CreateEmployeeReportingRelationshipRequest,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: CreateEmployeeReportingRelationshipUseCase = Depends(
        get_create_employee_reporting_relationship_use_case,
    ),
) -> CreateEmployeeReportingRelationshipResponse:
    command = EmployeeReportingRelationshipMapper.to_create_command(
        employee_id=employee_id,
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(command)

    return EmployeeReportingRelationshipMapper.to_create_response(
        application_response,
    )

@router.get(
    "/employees/{employee_id}/profile",
    response_model=GetEmployeeProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee Profile",
    description="Retrieve an employee's personal HR profile.",
)
async def get_employee_profile(
    employee_id: str,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: GetEmployeeProfileUseCase = Depends(
        get_get_employee_profile_use_case,
    ),
) -> GetEmployeeProfileResponse:
    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        employee_id=employee_id,
    )

    return EmployeeProfileMapper.to_get_response(
        application_response,
    )

@router.get(
    "/employees/{employee_id}/manager",
    response_model=GetEmployeeManagerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee Manager",
    description="Retrieve the active primary manager for an employee.",
)
async def get_employee_manager(
    employee_id: str,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: GetEmployeeManagerUseCase = Depends(
        get_get_employee_manager_use_case,
    ),
) -> GetEmployeeManagerResponse:
    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        employee_id=employee_id,
    )

    return EmployeeReportingRelationshipMapper.to_get_manager_response(
        application_response,
    )

@router.get(
    "/employees/{employee_id}/position",
    response_model=GetEmployeePositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee Position",
    description="Retrieve the current organizational position for an employee.",
)
async def get_employee_position(
    employee_id: str,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: GetEmployeePositionUseCase = Depends(
        get_get_employee_position_use_case,
    ),
) -> GetEmployeePositionResponse:
    """
    Retrieve an employee's current organizational position.
    """

    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        employee_id=employee_id,
    )

    return EmployeePositionMapper.to_get_response(
        application_response,
    )

