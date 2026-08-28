"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_time_segment_service.py

Description:
    Splits a worked attendance interval into contiguous time segments.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, time, timedelta

from qwos.domains.attendance.models.attendance_time_segment import (
    AttendanceTimeSegment,
)


class AttendanceTimeSegmentService:
    """
    Splits a worked attendance interval into classified time segments.

    The service does not calculate pay rates or multipliers. It only identifies
    contiguous intervals where a classification boundary occurs.
    """

    def segment(
        self,
        *,
        start_at: datetime,
        end_at: datetime,
        night_start: time | None = None,
        night_end: time | None = None,
        is_holiday: bool = False,
        is_rest_day: bool = False,
        is_overtime: bool = False,
    ) -> list[AttendanceTimeSegment]:
        """
        Split a worked interval into contiguous time segments.

        When a night-differential window is supplied, the interval is split
        at the boundaries of that window. Holiday, rest-day, and overtime
        classifications are applied to the resulting segments.
        """

        if end_at <= start_at:
            raise ValueError(
                "end_at must be later than start_at.",
            )

        if night_start is None or night_end is None:
            return [
                AttendanceTimeSegment(
                    start_at=start_at,
                    end_at=end_at,
                    is_overnight=end_at.date() > start_at.date(),
                    is_holiday=is_holiday,
                    is_rest_day=is_rest_day,
                    is_overtime=is_overtime,
                ),
            ]

        boundaries = self._build_boundaries(
            start_at=start_at,
            end_at=end_at,
            night_start=night_start,
            night_end=night_end,
        )

        segments: list[AttendanceTimeSegment] = []

        for segment_start, segment_end in zip(
            boundaries,
            boundaries[1:],
        ):
            if segment_end <= segment_start:
                continue

            night_differential = self._is_night_differential(
                moment=segment_start,
                night_start=night_start,
                night_end=night_end,
            )

            segments.append(
                AttendanceTimeSegment(
                    start_at=segment_start,
                    end_at=segment_end,
                    is_overnight=segment_end.date()
                    > segment_start.date(),
                    is_holiday=is_holiday,
                    is_rest_day=is_rest_day,
                    is_night_differential=night_differential,
                    is_overtime=is_overtime,
                ),
            )

        return segments

    @staticmethod
    def _build_boundaries(
        *,
        start_at: datetime,
        end_at: datetime,
        night_start: time,
        night_end: time,
    ) -> list[datetime]:
        """
        Build interval boundaries for the night-differential window.
        """

        boundaries = {start_at, end_at}

        current_date = start_at.date()

        while current_date <= end_at.date():
            night_window_start = datetime.combine(
                current_date,
                night_start,
                tzinfo=start_at.tzinfo,
            )

            if night_end > night_start:
                night_window_end = datetime.combine(
                    current_date,
                    night_end,
                    tzinfo=start_at.tzinfo,
                )
            else:
                night_window_end = datetime.combine(
                    current_date + timedelta(days=1),
                    night_end,
                    tzinfo=start_at.tzinfo,
                )

            if start_at < night_window_start < end_at:
                boundaries.add(night_window_start)

            if start_at < night_window_end < end_at:
                boundaries.add(night_window_end)

            current_date += timedelta(days=1)

        return sorted(boundaries)

    @staticmethod
    def _is_night_differential(
        *,
        moment: datetime,
        night_start: time,
        night_end: time,
    ) -> bool:
        """
        Determine whether a moment falls inside the night window.
        """

        current_time = moment.timetz().replace(
            tzinfo=None,
        )

        if night_end > night_start:
            return night_start <= current_time < night_end

        return (
            current_time >= night_start
            or current_time < night_end
        )