from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.leave.commands.create_leave_policy_command import (
    CreateLeavePolicyCommand,
)
from qwos.application.common.results.create_leave_policy_validator import (
    CreateLeavePolicyValidator,
)
from qwos.application.leave.responses.create_leave_policy_response import (
    CreateLeavePolicyResponse,
)
from qwos.domains.leave.models.leave_policy import LeavePolicy
from qwos.domains.leave.repositories.leave_policy_repository import (
    LeavePolicyRepository,
)


class CreateLeavePolicyUseCase:
    def __init__(
        self,
        *,
        leave_policy_repository: LeavePolicyRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateLeavePolicyValidator,
        request_context: RequestContext,
    ) -> None:
        self._leave_policy_repository = leave_policy_repository
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateLeavePolicyCommand,
    ) -> CreateLeavePolicyResponse:
        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        normalized_code = command.policy_code.strip().lower()

        if self._leave_policy_repository.exists_by_code(
            tenant_id=command.tenant_id,
            policy_code=normalized_code,
        ):
            raise DuplicateResourceException(
                resource="LeavePolicy",
                field="policy_code",
                value=normalized_code,
            )

        leave_policy_id = self._id_generator.generate()

        leave_policy = LeavePolicy.create(
            id=leave_policy_id,
            tenant_id=command.tenant_id,
            leave_type_id=command.leave_type_id,
            policy_code=command.policy_code,
            policy_name=command.policy_name,
            description=command.description,
            entitlement_days=command.entitlement_days,
            accrual_method=command.accrual_method,
            accrual_frequency=command.accrual_frequency,
            carry_forward_allowed=command.carry_forward_allowed,
            carry_forward_days=command.carry_forward_days,
            minimum_service_days=command.minimum_service_days,
            is_active=command.is_active,
            created_by=self._request_context.user_id,
        )

        with self._unit_of_work:
            self._leave_policy_repository.save(leave_policy)
            self._unit_of_work.flush()

        return CreateLeavePolicyResponse(
            id=leave_policy.id,
            leave_type_id=leave_policy.leave_type_id,
            policy_code=leave_policy.policy_code,
            policy_name=leave_policy.policy_name,
            description=leave_policy.description,
            entitlement_days=leave_policy.entitlement_days,
            accrual_method=leave_policy.accrual_method,
            accrual_frequency=leave_policy.accrual_frequency,
            carry_forward_allowed=leave_policy.carry_forward_allowed,
            carry_forward_days=leave_policy.carry_forward_days,
            minimum_service_days=leave_policy.minimum_service_days,
            is_active=leave_policy.is_active,
            created_at=leave_policy.created_at,
        )