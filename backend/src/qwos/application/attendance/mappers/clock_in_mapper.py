"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    clock_in_mapper.py

Description:
    Maps Attendance API contracts to application commands and responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.attendance.clock_in_request import (
    ClockInRequest,
)
from qwos.api.contracts.responses.attendance.clock_in_response import (
    ClockInResponse,
)
from qwos.application.attendance.commands.clock_in_command import (
    ClockInCommand,
)
from qwos.application.attendance.responses.clock_in_response import (
    ClockInResponse as ApplicationClockInResponse,
)
from qwos.application.common.context.request_context import RequestContext


class ClockInMapper:
    """
    Maps between Attendance API contracts and application objects.
    """

    @staticmethod
    def to_command(
        *,
        request: ClockInRequest,
        request_context: RequestContext,
    ) -> ClockInCommand:
        """
        Convert an API request into a ClockInCommand.
        """

        return ClockInCommand(
            tenant_id=request_context.tenant_id,
            employee_id=request.employee_id,
            clock_in_at=request.clock_in_at,
            event_source=request.event_source,
            notes=request.notes,
        )

    @staticmethod
    def to_response(
        response: ApplicationClockInResponse,
    ) -> ClockInResponse:
        """
        Convert an application response into an API response.
        """

        return ClockInResponse(
            attendance_record_id=response.attendance_record_id,
            attendance_event_id=response.attendance_event_id,
            employee_id=response.employee_id,
            attendance_date=response.attendance_date,
            clock_in_at=response.clock_in_at,
            status=response.status,
            event_type=response.event_type,
            event_at=response.event_at,
        )