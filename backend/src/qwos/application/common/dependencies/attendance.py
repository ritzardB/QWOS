"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Common Dependencies

Attendance Dependencies

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import Depends

from qwos.application.attendance.use_cases.clock_in_use_case import (
    ClockInUseCase,
)
from qwos.application.attendance.validators.clock_in_validator import (
    ClockInValidator,
)
from qwos.application.common.context.request_context import (
    RequestContext,
)
from qwos.application.common.dependencies.common import (
    get_clock,
    get_id_generator,
    get_request_context,
    get_unit_of_work,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator


def get_clock_in_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    clock: Clock = Depends(get_clock),
    id_generator: IdGenerator = Depends(get_id_generator),
    validator: ClockInValidator = Depends(),
    request_context: RequestContext = Depends(get_request_context),
) -> ClockInUseCase:
    """
    Provide the ClockInUseCase instance.
    """

    return ClockInUseCase(
        employee_repository=unit_of_work.employee_repository,
        attendance_record_repository=(
            unit_of_work.attendance_record_repository
        ),
        attendance_event_repository=(
            unit_of_work.attendance_event_repository
        ),
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )