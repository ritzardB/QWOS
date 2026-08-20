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

from datetime import date
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)

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
from qwos.api.contracts.requests.hr.update_employee_profile_request import (
    UpdateEmployeeProfileRequest,
)
from qwos.api.contracts.requests.hr.upload_employee_document_request import (
    UploadEmployeeDocumentRequest,
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
from qwos.api.contracts.responses.hr.get_employee_immigration_response import (
    GetEmployeeImmigrationResponse,
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
from qwos.api.contracts.responses.hr.list_employee_documents_response import (
    ListEmployeeDocumentsResponse,
)
from qwos.api.contracts.responses.hr.list_employee_immigration_response import (
    ListEmployeeImmigrationResponse,
)
from qwos.api.contracts.responses.hr.list_employees_response import (
    ListEmployeesResponse,
)
from qwos.api.contracts.responses.hr.list_expiring_employee_immigration_response import (
    ListExpiringEmployeeImmigrationResponse,
)
from qwos.api.contracts.responses.hr.upload_employee_document_response import (
    UploadEmployeeDocumentResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.hr import (
    get_create_employee_profile_use_case,
    get_create_employee_reporting_relationship_use_case,
    get_create_employee_use_case,
    get_get_employee_document_content_use_case,
    get_get_employee_immigration_use_case,
    get_get_employee_manager_use_case,
    get_get_employee_position_use_case,
    get_get_employee_profile_use_case,
    get_get_employee_use_case,
    get_link_employee_to_user_use_case,
    get_list_employee_documents_use_case,
    get_list_employee_immigration_use_case,
    get_list_employees_use_case,
    get_list_expiring_employee_immigration_use_case,
    get_request_context,
    get_update_employee_profile_use_case,
    get_upload_employee_document_use_case,
)
from qwos.application.hr.mappers.employee_document_mapper import (
    EmployeeDocumentMapper,
)
from qwos.application.hr.mappers.employee_immigration_mapper import (
    EmployeeImmigrationMapper,
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
from qwos.application.hr.use_cases.get_employee_document_content_use_case import (
    GetEmployeeDocumentContentUseCase,
)
from qwos.application.hr.use_cases.get_employee_immigration_use_case import (
    GetEmployeeImmigrationUseCase,
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
from qwos.application.hr.use_cases.list_employee_documents_use_case import (
    ListEmployeeDocumentsUseCase,
)
from qwos.application.hr.use_cases.list_employee_immigration_use_case import (
    ListEmployeeImmigrationUseCase,
)
from qwos.application.hr.use_cases.list_employees_use_case import (
    ListEmployeesUseCase,
)
from qwos.application.hr.use_cases.list_expiring_employee_immigration_use_case import (
    ListExpiringEmployeeImmigrationUseCase,
)
from qwos.application.hr.use_cases.update_employee_profile_use_case import (
    UpdateEmployeeProfileUseCase,
)
from qwos.application.hr.use_cases.upload_employee_document_use_case import (
    UploadEmployeeDocumentUseCase,
)

router = APIRouter(
    prefix="/hr",
    tags=["HR"],
)


# -------------------------------------------------------------------------
# Employee Collection
# -------------------------------------------------------------------------


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


# -------------------------------------------------------------------------
# Employee Documents
# -------------------------------------------------------------------------


@router.get(
    "/employees/{employee_id}/documents",
    response_model=ListEmployeeDocumentsResponse,
    status_code=status.HTTP_200_OK,
    summary="List Employee Documents",
    description="List documents belonging to an employee.",
)
async def list_employee_documents(
    employee_id: str,
    document_category: str | None = None,
    use_case: ListEmployeeDocumentsUseCase = Depends(
        get_list_employee_documents_use_case,
    ),
) -> ListEmployeeDocumentsResponse:
    """
    List documents belonging to an employee.
    """

    application_response = await use_case.execute(
        employee_id=employee_id,
        document_category=document_category,
    )

    return EmployeeDocumentMapper.to_list_response(
        application_response,
    )


@router.post(
    "/employees/{employee_id}/documents",
    response_model=UploadEmployeeDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Employee Document",
    description="Upload a document for an employee.",
)
async def upload_employee_document(
    employee_id: str,
    request: UploadEmployeeDocumentRequest = Depends(),
    file: UploadFile = File(...),
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: UploadEmployeeDocumentUseCase = Depends(
        get_upload_employee_document_use_case,
    ),
) -> UploadEmployeeDocumentResponse:
    """
    Upload a document for an employee.
    """

    original_filename = file.filename or ""

    if not original_filename.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Uploaded file must have a filename.",
        )

    extension = Path(
        original_filename,
    ).suffix.lstrip(".").lower()

    if not extension:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Uploaded file must have a file extension.",
        )

    content = await file.read()

    command = EmployeeDocumentMapper.to_upload_command(
        employee_id=employee_id,
        request=request,
        content=content,
        original_filename=original_filename,
        mime_type=file.content_type,
        file_extension=extension,
        request_context=request_context,
    )

    application_response = await use_case.execute(
        command,
    )

    return EmployeeDocumentMapper.to_upload_response(
        application_response,
    )


@router.get(
    "/employees/{employee_id}/documents/{document_id}/content",
    status_code=status.HTTP_200_OK,
    summary="Get Employee Document Content",
    description="Retrieve the content of an employee document.",
)
async def get_employee_document_content(
    employee_id: str,
    document_id: str,
    use_case: GetEmployeeDocumentContentUseCase = Depends(
        get_get_employee_document_content_use_case,
    ),
) -> Response:
    """
    Retrieve an employee document's physical content.
    """

    application_response = await use_case.execute(
        employee_id=employee_id,
        document_id=document_id,
    )

    filename = (
        application_response.filename
        .replace('"', "")
        .replace("\r", "")
        .replace("\n", "")
    )

    return Response(
        content=application_response.content,
        media_type=(
            application_response.mime_type
            or "application/octet-stream"
        ),
        headers={
            "Content-Disposition": (
                f'inline; filename="{filename}"'
            ),
        },
    )


# -------------------------------------------------------------------------
# Employee Profile
# -------------------------------------------------------------------------


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
    """
    Retrieve an employee's personal HR profile.
    """

    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        employee_id=employee_id,
    )

    return EmployeeProfileMapper.to_get_response(
        application_response,
    )


@router.patch(
    "/employees/{employee_id}/profile",
    response_model=GetEmployeeProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Employee Profile",
    description="Update an employee's personal HR profile.",
)
async def update_employee_profile(
    employee_id: str,
    request: UpdateEmployeeProfileRequest,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: UpdateEmployeeProfileUseCase = Depends(
        get_update_employee_profile_use_case,
    ),
) -> GetEmployeeProfileResponse:
    """
    Update an employee's personal HR profile.
    """

    command = EmployeeProfileMapper.to_update_command(
        employee_id=employee_id,
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(
        command,
    )

    return GetEmployeeProfileResponse(
        id=application_response.id,
        employee_id=application_response.employee_id,
        date_of_birth=application_response.date_of_birth,
        gender=application_response.gender,
        nationality=application_response.nationality,
        marital_status=application_response.marital_status,
        personal_email=application_response.personal_email,
        personal_phone=application_response.personal_phone,
        address_line_1=application_response.address_line_1,
        address_line_2=application_response.address_line_2,
        city=application_response.city,
        state_province=application_response.state_province,
        postal_code=application_response.postal_code,
        country_code=application_response.country_code,
        emergency_contact_name=application_response.emergency_contact_name,
        emergency_contact_relationship=(
            application_response.emergency_contact_relationship
        ),
        emergency_contact_phone=(
            application_response.emergency_contact_phone
        ),
        created_at=application_response.created_at,
    )


# -------------------------------------------------------------------------
# Employee ↔ User
# -------------------------------------------------------------------------


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


# -------------------------------------------------------------------------
# Employee Reporting
# -------------------------------------------------------------------------


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
    """
    Assign the reporting manager for an employee.
    """

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
    """
    Retrieve the active primary manager for an employee.
    """

    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        employee_id=employee_id,
    )

    return EmployeeReportingRelationshipMapper.to_get_manager_response(
        application_response,
    )


# -------------------------------------------------------------------------
# Employee Position
# -------------------------------------------------------------------------


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


# -------------------------------------------------------------------------
# Employee Immigration
# -------------------------------------------------------------------------


@router.get(
    "/employees/{employee_id}/immigration",
    response_model=GetEmployeeImmigrationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee Immigration",
    description="Retrieve the current immigration record for an employee.",
)
async def get_employee_immigration(
    employee_id: str,
    immigration_type: str,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: GetEmployeeImmigrationUseCase = Depends(
        get_get_employee_immigration_use_case,
    ),
) -> GetEmployeeImmigrationResponse:
    """
    Retrieve the current immigration record for an employee.
    """

    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        employee_id=employee_id,
        immigration_type=immigration_type,
        as_of_date=date.today(),
    )

    return EmployeeImmigrationMapper.to_get_response(
        application_response,
    )


@router.get(
    "/employees/{employee_id}/immigration/history",
    response_model=ListEmployeeImmigrationResponse,
    status_code=status.HTTP_200_OK,
    summary="List Employee Immigration History",
    description="Retrieve immigration history for an employee.",
)
async def list_employee_immigration(
    employee_id: str,
    immigration_type: str | None = None,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: ListEmployeeImmigrationUseCase = Depends(
        get_list_employee_immigration_use_case,
    ),
) -> ListEmployeeImmigrationResponse:
    """
    Retrieve immigration history for an employee.
    """

    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        employee_id=employee_id,
        immigration_type=immigration_type,
    )

    return EmployeeImmigrationMapper.to_list_response(
        application_response,
    )


@router.get(
    "/immigration/expiring",
    response_model=ListExpiringEmployeeImmigrationResponse,
    status_code=status.HTTP_200_OK,
    summary="List Expiring Immigration Records",
    description=(
        "List immigration records expiring within a specified "
        "number of days."
    ),
)
async def list_expiring_employee_immigration(
    days: int = 30,
    immigration_type: str | None = None,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: ListExpiringEmployeeImmigrationUseCase = Depends(
        get_list_expiring_employee_immigration_use_case,
    ),
) -> ListExpiringEmployeeImmigrationResponse:
    """
    Retrieve immigration records expiring within the requested window.
    """

    application_response = await use_case.execute(
        tenant_id=request_context.tenant_id,
        as_of_date=date.today(),
        days=days,
        immigration_type=immigration_type,
    )

    return EmployeeImmigrationMapper.to_expiring_list_response(
        application_response,
    )