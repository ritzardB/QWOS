"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Event Sequencing Validator
===============================================================================
"""

from __future__ import annotations

from typing import Iterable


class AttendanceEventSequenceError(ValueError):
    """
    Raised when attendance events occur in an invalid sequence.
    """


class AttendanceEventSequenceValidator:
    """
    Validates the chronological business sequence of attendance events.
    """

    # -------------------------------------------------------------------------
    # Event Order
    # -------------------------------------------------------------------------

    VALID_EVENTS = {
        "clock_in",
        "break_start",
        "break_end",
        "clock_out",
    }

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    @classmethod
    def validate(
        cls,
        events: Iterable[str],
    ) -> None:
        """
        Validate an attendance event sequence.

        Valid sequence:

            clock_in
            break_start
            break_end
            clock_out

        Break events may repeat, but must always occur in pairs.
        """

        normalized_events = [event.strip().lower() for event in events]

        for event in normalized_events:
            if event not in cls.VALID_EVENTS:
                raise AttendanceEventSequenceError(
                    f"Invalid attendance event: {event}.",
                )

        if not normalized_events:
            return

        if normalized_events[0] != "clock_in":
            raise AttendanceEventSequenceError(
                "The first attendance event must be clock_in.",
            )

        clocked_in = False
        clocked_out = False
        break_started = False

        for event in normalized_events:
            if clocked_out:
                raise AttendanceEventSequenceError(
                    "No events are allowed after clock_out.",
                )

            if event == "clock_in":
                if clocked_in:
                    raise AttendanceEventSequenceError(
                        "clock_in cannot occur more than once.",
                    )

                if break_started:
                    raise AttendanceEventSequenceError(
                        "clock_in cannot occur during a break.",
                    )

                clocked_in = True

            elif event == "break_start":
                if break_started:
                    raise AttendanceEventSequenceError(
                        "break_start cannot occur twice without break_end.",
                    )

                break_started = True

            elif event == "break_end":
                if not break_started:
                    raise AttendanceEventSequenceError(
                        "break_end requires a preceding break_start.",
                    )

                break_started = False

            elif event == "clock_out":
                if break_started:
                    raise AttendanceEventSequenceError(
                        "clock_out cannot occur while a break is active.",
                    )

                clocked_out = True

        if break_started:
            raise AttendanceEventSequenceError(
                "An attendance sequence cannot end with an active break.",
            )
