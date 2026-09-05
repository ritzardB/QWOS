"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Common Dependencies

Leave Dependencies

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import Depends

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.authentication import get_authenticated_request_context
from qwos.application.common.dependencies.common import (
    get_id_generator,
    get_request_context,
    get_unit_of_work,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.results.create_employee_leave_assignment_validator import (
    CreateEmployeeLeaveAssignmentValidator,
)
from qwos.application.common.results.create_leave_policy_validator import (
    CreateLeavePolicyValidator,
)
from qwos.application.common.results.create_employee_leave_balance_validator import (
    CreateEmployeeLeaveBalanceValidator,
)
from qwos.application.common.results.create_leave_type_validator import (
    CreateLeaveTypeValidator,
)
from qwos.application.leave.use_cases.create_employee_leave_assignment_use_case import (
    CreateEmployeeLeaveAssignmentUseCase,
)
from qwos.application.leave.use_cases.create_leave_policy_use_case import (
    CreateLeavePolicyUseCase,
)
from qwos.application.leave.use_cases.create_employee_leave_balance_use_case import (
    CreateEmployeeLeaveBalanceUseCase,
)
from qwos.application.leave.use_cases.create_leave_type_use_case import (
    CreateLeaveTypeUseCase,
)


def get_create_leave_type_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: CreateLeaveTypeValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> CreateLeaveTypeUseCase:
    """
    Provide the CreateLeaveTypeUseCase instance.
    """

    return CreateLeaveTypeUseCase(
        leave_type_repository=unit_of_work.leave_type_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

def get_create_leave_policy_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: CreateLeavePolicyValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> CreateLeavePolicyUseCase:
    return CreateLeavePolicyUseCase(
        leave_policy_repository=unit_of_work.leave_policy_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

def get_create_employee_leave_assignment_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: CreateEmployeeLeaveAssignmentValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> CreateEmployeeLeaveAssignmentUseCase:
    return CreateEmployeeLeaveAssignmentUseCase(
        employee_leave_assignment_repository=(
            unit_of_work.employee_leave_assignment_repository
        ),
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

def get_create_employee_leave_balance_use_case(
    request_context: RequestContext = Depends(
        get_authenticated_request_context
    ),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> CreateEmployeeLeaveBalanceUseCase:
    return CreateEmployeeLeaveBalanceUseCase(
        employee_leave_balance_repository=(
            unit_of_work.employee_leave_balance_repository
        ),
        id_generator=...,
        unit_of_work=unit_of_work,
        validator=CreateEmployeeLeaveBalanceValidator(),
        request_context=request_context,
    )