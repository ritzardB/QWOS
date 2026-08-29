"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    clock_out_mapper.py

Description:
    Maps Attendance API contracts to application commands and responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.attendance.clock_out_request import (
    ClockOutRequest,
)
from qwos.api.contracts.responses.attendance.clock_out_response import (
    ClockOutResponse,
)
from qwos.application.attendance.commands.clock_out_command import (
    ClockOutCommand,
)
from qwos.application.attendance.responses.clock_out_response import (
    ClockOutResponse as ApplicationClockOutResponse,
)
from qwos.application.common.context.request_context import RequestContext


class ClockOutMapper:
    """
    Maps between Attendance API contracts and application objects.
    """

    @staticmethod
    def to_command(
        *,
        request: ClockOutRequest,
        request_context: RequestContext,
    ) -> ClockOutCommand:
        """
        Convert an API request into a ClockOutCommand.
        """

        return ClockOutCommand(
            tenant_id=request_context.tenant_id,
            employee_id=request.employee_id,
            clock_out_at=request.clock_out_at,
            event_source=request.event_source,
            notes=request.notes,
        )

    @staticmethod
    def to_response(
        response: ApplicationClockOutResponse,
    ) -> ClockOutResponse:
        """
        Convert an application response into an API response.
        """

        return ClockOutResponse(
            attendance_record_id=response.attendance_record_id,
            attendance_event_id=response.attendance_event_id,
            employee_id=response.employee_id,
            attendance_date=response.attendance_date,
            clock_in_at=response.clock_in_at,
            clock_out_at=response.clock_out_at,
            worked_minutes=response.worked_minutes,
            status=response.status,
            event_type=response.event_type,
            event_at=response.event_at,
        )
