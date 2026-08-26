from __future__ import annotations

from qwos.api.contracts.requests.attendance.create_employee_work_arrangement_request import (
    CreateEmployeeWorkArrangementRequest,
)
from qwos.api.contracts.responses.attendance.create_employee_work_arrangement_response import (
    CreateEmployeeWorkArrangementResponse,
)
from qwos.application.attendance.commands.create_employee_work_arrangement_command import (
    CreateEmployeeWorkArrangementCommand,
)
from qwos.application.attendance.responses.create_employee_work_arrangement_response import (
    CreateEmployeeWorkArrangementResponse as ApplicationCreateEmployeeWorkArrangementResponse,
)
from qwos.application.common.context.request_context import RequestContext


class EmployeeWorkArrangementMapper:
    """
    Maps Employee Work Arrangement API contracts
    to application commands and responses.
    """

    @staticmethod
    def to_create_command(
        *,
        employee_id: str,
        request: CreateEmployeeWorkArrangementRequest,
        request_context: RequestContext,
    ) -> CreateEmployeeWorkArrangementCommand:
        """
        Convert an API request into a CreateEmployeeWorkArrangementCommand.
        """

        return CreateEmployeeWorkArrangementCommand(
            tenant_id=request_context.tenant_id,
            employee_id=employee_id,
            work_arrangement=request.work_arrangement,
            effective_from=request.effective_from,
            effective_until=request.effective_until,
            is_active=request.is_active,
        )

    @staticmethod
    def to_create_response(
        response: ApplicationCreateEmployeeWorkArrangementResponse,
    ) -> CreateEmployeeWorkArrangementResponse:
        """
        Convert an application response into an API response.
        """

        return CreateEmployeeWorkArrangementResponse(
            id=response.id,
            employee_id=response.employee_id,
            work_arrangement=response.work_arrangement,
            effective_from=response.effective_from,
            effective_until=response.effective_until,
            is_active=response.is_active,
            created_at=response.created_at,
        )