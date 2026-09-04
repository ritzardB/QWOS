from qwos.api.contracts.requests.leave.create_leave_policy_request import (
    CreateLeavePolicyRequest,
)
from qwos.api.contracts.responses.leave.create_leave_policy_response import (
    CreateLeavePolicyResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.leave.commands.create_leave_policy_command import (
    CreateLeavePolicyCommand,
)
from qwos.application.leave.responses.create_leave_policy_response import (
    CreateLeavePolicyResponse as ApplicationCreateLeavePolicyResponse,
)


class LeavePolicyMapper:
    @staticmethod
    def to_create_response(
        response: ApplicationCreateLeavePolicyResponse,
    ) -> CreateLeavePolicyResponse:
        return CreateLeavePolicyResponse(
            id=response.id,
            leave_type_id=response.leave_type_id,
            policy_code=response.policy_code,
            policy_name=response.policy_name,
            description=response.description,
            entitlement_days=response.entitlement_days,
            accrual_method=response.accrual_method,
            accrual_frequency=response.accrual_frequency,
            carry_forward_allowed=response.carry_forward_allowed,
            carry_forward_days=response.carry_forward_days,
            minimum_service_days=response.minimum_service_days,
            is_active=response.is_active,
            created_at=response.created_at,
        )

    @staticmethod
    def to_create_command(
        *,
        request: CreateLeavePolicyRequest,
        request_context: RequestContext,
    ) -> CreateLeavePolicyCommand:
        return CreateLeavePolicyCommand(
            tenant_id=request_context.tenant_id,
            leave_type_id=request.leave_type_id,
            policy_code=request.policy_code,
            policy_name=request.policy_name,
            description=request.description,
            entitlement_days=request.entitlement_days,
            accrual_method=request.accrual_method,
            accrual_frequency=request.accrual_frequency,
            carry_forward_allowed=request.carry_forward_allowed,
            carry_forward_days=request.carry_forward_days,
            minimum_service_days=request.minimum_service_days,
            is_active=request.is_active,
        )