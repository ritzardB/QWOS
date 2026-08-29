"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    employee_immigration_mapper.py

Description:
    Maps employee immigration application responses to API responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.hr.create_employee_immigration_request import (
    CreateEmployeeImmigrationRequest,
)
from qwos.api.contracts.responses.hr.create_employee_immigration_response import (
    CreateEmployeeImmigrationResponse,
)
from qwos.api.contracts.responses.hr.get_employee_immigration_response import (
    GetEmployeeImmigrationResponse,
)
from qwos.api.contracts.responses.hr.list_employee_immigration_response import (
    EmployeeImmigrationItemResponse,
    ListEmployeeImmigrationResponse,
)
from qwos.api.contracts.responses.hr.list_expiring_employee_immigration_response import (
    ExpiringEmployeeImmigrationItemResponse,
    ListExpiringEmployeeImmigrationResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.hr.commands.create_employee_immigration_command import (
    CreateEmployeeImmigrationCommand,
)
from qwos.application.hr.responses.create_employee_immigration_response import (
    CreateEmployeeImmigrationResponse as ApplicationCreateEmployeeImmigrationResponse,
)
from qwos.application.hr.responses.get_employee_immigration_response import (
    GetEmployeeImmigrationResponse as ApplicationGetEmployeeImmigrationResponse,
)
from qwos.application.hr.responses.list_employee_immigration_response import (
    ListEmployeeImmigrationResponse as ApplicationListEmployeeImmigrationResponse,
)
from qwos.application.hr.responses.list_expiring_employee_immigration_response import (
    ListExpiringEmployeeImmigrationResponse as ApplicationListExpiringEmployeeImmigrationResponse,
)


class EmployeeImmigrationMapper:
    """
    Maps Employee Immigration application objects to API contracts.
    """

    @staticmethod
    def to_get_response(
        response: ApplicationGetEmployeeImmigrationResponse,
    ) -> GetEmployeeImmigrationResponse:
        return GetEmployeeImmigrationResponse(
            id=response.id,
            employee_id=response.employee_id,
            immigration_type=response.immigration_type,
            status=response.status,
            document_number=response.document_number,
            sponsor_name=response.sponsor_name,
            issuing_authority=response.issuing_authority,
            issue_date=response.issue_date,
            expiry_date=response.expiry_date,
            notes=response.notes,
        )

    @staticmethod
    def to_list_response(
        response: ApplicationListEmployeeImmigrationResponse,
    ) -> ListEmployeeImmigrationResponse:
        return ListEmployeeImmigrationResponse(
            items=[
                EmployeeImmigrationItemResponse(
                    id=item.id,
                    employee_id=item.employee_id,
                    immigration_type=item.immigration_type,
                    status=item.status,
                    document_number=item.document_number,
                    sponsor_name=item.sponsor_name,
                    issuing_authority=item.issuing_authority,
                    issue_date=item.issue_date,
                    expiry_date=item.expiry_date,
                    notes=item.notes,
                )
                for item in response.items
            ],
        )

    @staticmethod
    def to_expiring_list_response(
        response: ApplicationListExpiringEmployeeImmigrationResponse,
    ) -> ListExpiringEmployeeImmigrationResponse:
        return ListExpiringEmployeeImmigrationResponse(
            items=[
                ExpiringEmployeeImmigrationItemResponse(
                    id=item.id,
                    employee_id=item.employee_id,
                    immigration_type=item.immigration_type,
                    status=item.status,
                    document_number=item.document_number,
                    issue_date=item.issue_date,
                    expiry_date=item.expiry_date,
                    days_until_expiry=item.days_until_expiry,
                )
                for item in response.items
            ],
        )

    @staticmethod
    def to_create_command(
        *,
        employee_id: str,
        request: CreateEmployeeImmigrationRequest,
        request_context: RequestContext,
    ) -> CreateEmployeeImmigrationCommand:
        return CreateEmployeeImmigrationCommand(
            tenant_id=request_context.tenant_id,
            employee_id=employee_id,
            immigration_type=request.immigration_type,
            status=request.status,
            document_number=request.document_number,
            sponsor_name=request.sponsor_name,
            issuing_authority=request.issuing_authority,
            issue_date=request.issue_date,
            expiry_date=request.expiry_date,
            notes=request.notes,
        )

    @staticmethod
    def to_create_response(
        response: ApplicationCreateEmployeeImmigrationResponse,
    ) -> CreateEmployeeImmigrationResponse:
        return CreateEmployeeImmigrationResponse(
            id=response.id,
            employee_id=response.employee_id,
            immigration_type=response.immigration_type,
            status=response.status,
            document_number=response.document_number,
            sponsor_name=response.sponsor_name,
            issuing_authority=response.issuing_authority,
            issue_date=response.issue_date,
            expiry_date=response.expiry_date,
            notes=response.notes,
        )
