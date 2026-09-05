from __future__ import annotations

from qwos.api.contracts.requests.leave.create_employee_leave_balance_request import (
    CreateEmployeeLeaveBalanceRequest,
)
from qwos.api.contracts.responses.leave.create_employee_leave_balance_response import (
    CreateEmployeeLeaveBalanceResponse as ApiResponse,
)
from qwos.application.leave.commands.create_employee_leave_balance_command import (
    CreateEmployeeLeaveBalanceCommand,
)
from qwos.application.leave.responses.create_employee_leave_balance_response import (
    CreateEmployeeLeaveBalanceResponse,
)


class CreateEmployeeLeaveBalanceMapper:
    @staticmethod
    def to_command(
        request: CreateEmployeeLeaveBalanceRequest,
        *,
        tenant_id: str,
    ) -> CreateEmployeeLeaveBalanceCommand:
        return CreateEmployeeLeaveBalanceCommand(
            tenant_id=tenant_id,
            employee_leave_assignment_id=request.employee_leave_assignment_id,
            employee_id=request.employee_id,
            period_start=request.period_start,
            period_end=request.period_end,
            entitlement_days=request.entitlement_days,
            carried_forward_days=request.carried_forward_days,
            accrued_days=request.accrued_days,
            used_days=request.used_days,
            adjustment_days=request.adjustment_days,
            is_active=request.is_active,
        )

    @staticmethod
    def to_response(
        response: CreateEmployeeLeaveBalanceResponse,
    ) -> ApiResponse:
        return ApiResponse(
            id=response.id,
            employee_leave_assignment_id=response.employee_leave_assignment_id,
            employee_id=response.employee_id,
            period_start=response.period_start,
            period_end=response.period_end,
            entitlement_days=response.entitlement_days,
            carried_forward_days=response.carried_forward_days,
            accrued_days=response.accrued_days,
            used_days=response.used_days,
            adjustment_days=response.adjustment_days,
            is_active=response.is_active,
            created_at=response.created_at,
        )