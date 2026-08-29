"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_premium_calculation.py

Description:
    Domain value object representing the calculated result of an attendance
    premium rule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class AttendancePremiumCalculationType(StrEnum):
    """
    Types of premium calculations supported by QWOS.

    PERCENTAGE:
        A percentage premium applied to the applicable base amount.

    MULTIPLIER:
        A multiplier applied to the applicable base amount.
    """

    PERCENTAGE = "percentage"
    MULTIPLIER = "multiplier"


@dataclass(frozen=True, slots=True)
class AttendancePremiumCalculation:
    """
    Represents the calculated premium for a period of attendance.

    This value object contains the result of applying a premium rule
    to a base amount.

    It intentionally contains no employee, payroll, currency, or
    jurisdiction-specific information.
    """

    rule_code: str
    calculation_type: AttendancePremiumCalculationType
    base_amount: Decimal
    rule_value: Decimal
    premium_amount: Decimal

    def __post_init__(self) -> None:
        """
        Validate the premium calculation.
        """

        if not self.rule_code.strip():
            raise ValueError(
                "rule_code cannot be empty.",
            )

        if self.base_amount < Decimal("0"):
            raise ValueError(
                "base_amount cannot be negative.",
            )

        if self.rule_value < Decimal("0"):
            raise ValueError(
                "rule_value cannot be negative.",
            )

        if self.premium_amount < Decimal("0"):
            raise ValueError(
                "premium_amount cannot be negative.",
            )

        if self.calculation_type == AttendancePremiumCalculationType.PERCENTAGE and self.rule_value > Decimal("100"):
            raise ValueError(
                "percentage rule_value cannot exceed 100.",
            )

    @property
    def is_percentage(self) -> bool:
        """
        Return whether the calculation uses percentage treatment.
        """

        return self.calculation_type == AttendancePremiumCalculationType.PERCENTAGE

    @property
    def is_multiplier(self) -> bool:
        """
        Return whether the calculation uses multiplier treatment.
        """

        return self.calculation_type == AttendancePremiumCalculationType.MULTIPLIER

    @property
    def total_amount(self) -> Decimal:
        """
        Return the base amount plus the calculated premium.

        The premium_amount represents the additional compensation generated
        by the premium rule.
        """

        return self.base_amount + self.premium_amount
