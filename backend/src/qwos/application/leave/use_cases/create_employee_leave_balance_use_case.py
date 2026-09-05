from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.results.create_employee_leave_balance_validator import (
    CreateEmployeeLeaveBalanceValidator,
)
from qwos.application.leave.commands.create_employee_leave_balance_command import (
    CreateEmployeeLeaveBalanceCommand,
)
from qwos.application.leave.responses.create_employee_leave_balance_response import (
    CreateEmployeeLeaveBalanceResponse,
)
from qwos.domains.leave.models.employee_leave_balance import EmployeeLeaveBalance
from qwos.domains.leave.repositories.employee_leave_balance_repository import (
    EmployeeLeaveBalanceRepository,
)


class CreateEmployeeLeaveBalanceUseCase:
    def __init__(
        self,
        *,
        employee_leave_balance_repository: EmployeeLeaveBalanceRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateEmployeeLeaveBalanceValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_leave_balance_repository = (
            employee_leave_balance_repository
        )
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateEmployeeLeaveBalanceCommand,
    ) -> CreateEmployeeLeaveBalanceResponse:
        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        if self._employee_leave_balance_repository.exists_by_assignment_and_period(
            tenant_id=command.tenant_id,
            employee_leave_assignment_id=command.employee_leave_assignment_id,
            period_start=command.period_start,
            period_end=command.period_end,
        ):
            raise DuplicateResourceException(
                resource="EmployeeLeaveBalance",
                field="period",
                value=(
                    f"{command.period_start.isoformat()}"
                    f" to "
                    f"{command.period_end.isoformat()}"
                ),
            )

        balance_id = self._id_generator.generate()

        balance = EmployeeLeaveBalance.create(
            id=balance_id,
            tenant_id=command.tenant_id,
            employee_leave_assignment_id=command.employee_leave_assignment_id,
            employee_id=command.employee_id,
            period_start=command.period_start,
            period_end=command.period_end,
            entitlement_days=command.entitlement_days,
            carried_forward_days=command.carried_forward_days,
            accrued_days=command.accrued_days,
            used_days=command.used_days,
            adjustment_days=command.adjustment_days,
            is_active=command.is_active,
            created_by=self._request_context.user_id,
        )

        with self._unit_of_work:
            self._employee_leave_balance_repository.save(balance)
            self._unit_of_work.flush()

        return CreateEmployeeLeaveBalanceResponse(
            id=balance.id,
            employee_leave_assignment_id=balance.employee_leave_assignment_id,
            employee_id=balance.employee_id,
            period_start=balance.period_start,
            period_end=balance.period_end,
            entitlement_days=balance.entitlement_days,
            carried_forward_days=balance.carried_forward_days,
            accrued_days=balance.accrued_days,
            used_days=balance.used_days,
            adjustment_days=balance.adjustment_days,
            is_active=balance.is_active,
            created_at=balance.created_at,
        )