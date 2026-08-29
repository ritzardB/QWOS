"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_premium_rule.py

Description:
    Domain value object representing a configurable attendance premium rule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum


class AttendancePremiumRuleType(StrEnum):
    """
    Types of attendance premiums supported by QWOS.
    """

    NIGHT_DIFFERENTIAL = "night_differential"
    REGULAR_HOLIDAY = "regular_holiday"
    SPECIAL_HOLIDAY = "special_holiday"
    REST_DAY = "rest_day"
    OVERTIME = "overtime"


class AttendancePremiumCalculationType(StrEnum):
    """
    Methods used to interpret a premium value.
    """

    PERCENTAGE = "percentage"
    MULTIPLIER = "multiplier"


class AttendancePremiumStackingStrategy(StrEnum):
    """
    Determines how a premium interacts with other applicable rules.
    """

    STACK = "stack"
    EXCLUSIVE = "exclusive"


@dataclass(frozen=True, slots=True)
class AttendancePremiumRule:
    """
    Configurable premium rule used to determine compensation treatment.

    The rule contains no currency or employee-specific information.
    """

    rule_code: str
    rule_type: AttendancePremiumRuleType
    calculation_type: AttendancePremiumCalculationType
    value: Decimal
    stacking_strategy: AttendancePremiumStackingStrategy = AttendancePremiumStackingStrategy.STACK
    priority: int = 0
    effective_from: date | None = None
    effective_until: date | None = None
    is_active: bool = True

    def __post_init__(self) -> None:
        """
        Validate the premium rule.
        """

        if not self.rule_code.strip():
            raise ValueError(
                "rule_code cannot be empty.",
            )

        if self.value < Decimal("0"):
            raise ValueError(
                "value cannot be negative.",
            )

        if self.priority < 0:
            raise ValueError(
                "priority cannot be negative.",
            )

        if (
            self.effective_from is not None
            and self.effective_until is not None
            and self.effective_until < self.effective_from
        ):
            raise ValueError(
                "effective_until cannot be earlier than effective_from.",
            )

        if self.calculation_type == AttendancePremiumCalculationType.PERCENTAGE and self.value > Decimal("100"):
            raise ValueError(
                "percentage value cannot exceed 100.",
            )

    def applies_on(self, effective_date: date) -> bool:
        """
        Return whether the rule is effective on the supplied date.
        """

        if not self.is_active:
            return False

        if self.effective_from is not None and effective_date < self.effective_from:
            return False

        if self.effective_until is not None and effective_date > self.effective_until:
            return False

        return True

    @property
    def is_percentage(self) -> bool:
        """
        Return whether the rule uses percentage calculation.
        """

        return self.calculation_type == AttendancePremiumCalculationType.PERCENTAGE

    @property
    def is_multiplier(self) -> bool:
        """
        Return whether the rule uses multiplier calculation.
        """

        return self.calculation_type == AttendancePremiumCalculationType.MULTIPLIER

    @property
    def is_exclusive(self) -> bool:
        """
        Return whether this rule excludes stacking with other rules.
        """

        return self.stacking_strategy == AttendancePremiumStackingStrategy.EXCLUSIVE
