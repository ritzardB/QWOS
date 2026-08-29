from __future__ import annotations

from qwos.api.contracts.requests.hr.create_employee_reporting_relationship_request import (
    CreateEmployeeReportingRelationshipRequest,
)
from qwos.api.contracts.responses.hr.create_employee_reporting_relationship_response import (
    CreateEmployeeReportingRelationshipResponse,
)
from qwos.api.contracts.responses.hr.get_employee_manager_response import (
    GetEmployeeManagerResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.hr.commands.create_employee_reporting_relationship_command import (
    CreateEmployeeReportingRelationshipCommand,
)
from qwos.application.hr.responses.create_employee_reporting_relationship_response import (
    CreateEmployeeReportingRelationshipResponse as ApplicationResponse,
)
from qwos.application.hr.responses.get_employee_manager_response import (
    GetEmployeeManagerResponse as ApplicationGetEmployeeManagerResponse,
)


class EmployeeReportingRelationshipMapper:
    """
    Maps Employee Reporting Relationship API contracts.
    """

    @staticmethod
    def to_create_command(
        *,
        employee_id: str,
        request: CreateEmployeeReportingRelationshipRequest,
        request_context: RequestContext,
    ) -> CreateEmployeeReportingRelationshipCommand:
        return CreateEmployeeReportingRelationshipCommand(
            tenant_id=request_context.tenant_id,
            employee_id=employee_id,
            manager_employee_id=request.manager_employee_id,
            relationship_type=request.relationship_type,
            effective_from=request.effective_from,
            effective_to=request.effective_to,
            is_primary=request.is_primary,
        )

    @staticmethod
    def to_create_response(
        response: ApplicationResponse,
    ) -> CreateEmployeeReportingRelationshipResponse:
        return CreateEmployeeReportingRelationshipResponse(
            id=response.id,
            employee_id=response.employee_id,
            manager_employee_id=response.manager_employee_id,
            relationship_type=response.relationship_type,
            effective_from=response.effective_from,
            effective_to=response.effective_to,
            is_primary=response.is_primary,
            created_at=response.created_at,
        )

    @staticmethod
    def to_get_manager_response(
        response: ApplicationGetEmployeeManagerResponse,
    ) -> GetEmployeeManagerResponse:
        """
        Convert an application employee-manager response
        into an API response.
        """

        return GetEmployeeManagerResponse(
            employee_id=response.employee_id,
            manager_employee_id=response.manager_employee_id,
            manager_employee_number=response.manager_employee_number,
            relationship_type=response.relationship_type,
            effective_from=response.effective_from,
        )
