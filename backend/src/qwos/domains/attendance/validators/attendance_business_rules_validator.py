"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Attendance Business Rules Validator
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


class AttendanceBusinessRuleError(ValueError):
    """
    Raised when an attendance business rule is violated.
    """


@dataclass(frozen=True)
class AttendanceBusinessRulesContext:
    """
    Resolved context required to validate an attendance action.
    """

    attendance_requirement: str
    clock_in_required: bool
    clock_out_required: bool
    payroll_impact_enabled: bool = False
    overtime_enabled: bool = False
    undertime_enabled: bool = False
    late_deduction_enabled: bool = False
    grace_period_minutes: int = 0


class AttendanceBusinessRulesValidator:
    """
    Validates attendance actions against the resolved attendance policy.
    """

    VALID_REQUIREMENTS = {
        "not_required",
        "tracking_only",
        "required",
    }

    # -------------------------------------------------------------------------
    # Context
    # -------------------------------------------------------------------------

    @classmethod
    def validate_context(
        cls,
        context: AttendanceBusinessRulesContext,
    ) -> None:
        """
        Validate the resolved attendance policy context.
        """

        requirement = context.attendance_requirement.strip().lower()

        if requirement not in cls.VALID_REQUIREMENTS:
            raise AttendanceBusinessRuleError(
                "Invalid attendance requirement.",
            )

        if context.grace_period_minutes < 0:
            raise AttendanceBusinessRuleError(
                "grace_period_minutes cannot be negative.",
            )

    # -------------------------------------------------------------------------
    # Clock In
    # -------------------------------------------------------------------------

    @classmethod
    def validate_clock_in(
        cls,
        *,
        context: AttendanceBusinessRulesContext,
        already_clocked_in: bool,
        already_clocked_out: bool,
    ) -> None:
        """
        Validate whether an employee may clock in.
        """

        cls.validate_context(context)

        if already_clocked_in:
            raise AttendanceBusinessRuleError(
                "Employee is already clocked in.",
            )

        if already_clocked_out:
            raise AttendanceBusinessRuleError(
                "Employee has already clocked out.",
            )

        if context.attendance_requirement == "not_required":
            raise AttendanceBusinessRuleError(
                "Attendance tracking is not required.",
            )

        if not context.clock_in_required:
            raise AttendanceBusinessRuleError(
                "Clock-in is not required by the attendance policy.",
            )

    # -------------------------------------------------------------------------
    # Clock Out
    # -------------------------------------------------------------------------

    @classmethod
    def validate_clock_out(
        cls,
        *,
        context: AttendanceBusinessRulesContext,
        already_clocked_in: bool,
        already_clocked_out: bool,
        break_active: bool,
    ) -> None:
        """
        Validate whether an employee may clock out.
        """

        cls.validate_context(context)

        if not already_clocked_in:
            raise AttendanceBusinessRuleError(
                "Employee must be clocked in before clocking out.",
            )

        if already_clocked_out:
            raise AttendanceBusinessRuleError(
                "Employee has already clocked out.",
            )

        if break_active:
            raise AttendanceBusinessRuleError(
                "Employee cannot clock out while a break is active.",
            )

        if not context.clock_out_required:
            raise AttendanceBusinessRuleError(
                "Clock-out is not required by the attendance policy.",
            )

    # -------------------------------------------------------------------------
    # Break Start
    # -------------------------------------------------------------------------

    @classmethod
    def validate_break_start(
        cls,
        *,
        context: AttendanceBusinessRulesContext,
        already_clocked_in: bool,
        already_clocked_out: bool,
        break_active: bool,
    ) -> None:
        """
        Validate whether an employee may start a break.
        """

        cls.validate_context(context)

        if not already_clocked_in:
            raise AttendanceBusinessRuleError(
                "Employee must be clocked in before starting a break.",
            )

        if already_clocked_out:
            raise AttendanceBusinessRuleError(
                "Employee cannot start a break after clocking out.",
            )

        if break_active:
            raise AttendanceBusinessRuleError(
                "Employee is already on a break.",
            )

    # -------------------------------------------------------------------------
    # Break End
    # -------------------------------------------------------------------------

    @classmethod
    def validate_break_end(
        cls,
        *,
        context: AttendanceBusinessRulesContext,
        already_clocked_in: bool,
        already_clocked_out: bool,
        break_active: bool,
    ) -> None:
        """
        Validate whether an employee may end a break.
        """

        cls.validate_context(context)

        if not already_clocked_in:
            raise AttendanceBusinessRuleError(
                "Employee must be clocked in before ending a break.",
            )

        if already_clocked_out:
            raise AttendanceBusinessRuleError(
                "Employee cannot end a break after clocking out.",
            )

        if not break_active:
            raise AttendanceBusinessRuleError(
                "Employee does not have an active break.",
            )
