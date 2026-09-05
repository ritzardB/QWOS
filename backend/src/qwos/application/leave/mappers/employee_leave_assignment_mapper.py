from __future__ import annotations

from qwos.api.contracts.requests.leave.create_employee_leave_assignment_request import (
    CreateEmployeeLeaveAssignmentRequest,
)
from qwos.api.contracts.responses.leave.create_employee_leave_assignment_response import (
    CreateEmployeeLeaveAssignmentResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.leave.commands.create_employee_leave_assignment_command import (
    CreateEmployeeLeaveAssignmentCommand,
)
from qwos.application.leave.responses.create_employee_leave_assignment_response import (
    CreateEmployeeLeaveAssignmentResponse as ApplicationCreateEmployeeLeaveAssignmentResponse,
)


class EmployeeLeaveAssignmentMapper:
    @staticmethod
    def to_create_command(
        *,
        request: CreateEmployeeLeaveAssignmentRequest,
        request_context: RequestContext,
    ) -> CreateEmployeeLeaveAssignmentCommand:
        return CreateEmployeeLeaveAssignmentCommand(
            tenant_id=request_context.tenant_id,
            employee_id=request.employee_id,
            leave_policy_id=request.leave_policy_id,
            effective_from=request.effective_from,
            effective_until=request.effective_until,
            is_active=request.is_active,
        )

    @staticmethod
    def to_create_response(
        response: ApplicationCreateEmployeeLeaveAssignmentResponse,
    ) -> CreateEmployeeLeaveAssignmentResponse:
        return CreateEmployeeLeaveAssignmentResponse(
            id=response.id,
            employee_id=response.employee_id,
            leave_policy_id=response.leave_policy_id,
            effective_from=response.effective_from,
            effective_until=response.effective_until,
            is_active=response.is_active,
            created_at=response.created_at,
        )