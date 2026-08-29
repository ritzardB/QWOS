"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_premium_calculation_service.py

Description:
    Domain service responsible for calculating attendance premiums from
    resolved premium rules.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from qwos.domains.attendance.models.attendance_premium_calculation import (
    AttendancePremiumCalculation,
)
from qwos.domains.attendance.models.attendance_premium_rule import (
    AttendancePremiumCalculationType,
    AttendancePremiumRule,
)


@dataclass(frozen=True, slots=True)
class AttendancePremiumCalculationService:
    """
    Calculate monetary attendance premiums from resolved premium rules.

    This service deliberately contains no employee-specific, payroll-specific,
    or currency-specific logic.

    The caller supplies the applicable base amount and the resolved premium
    rules. The service returns a domain value object describing the calculated
    premium.
    """

    def calculate(
        self,
        *,
        base_amount: Decimal,
        rules: list[AttendancePremiumRule],
    ) -> AttendancePremiumCalculation:
        """
        Calculate the total premium amount from applicable rules.

        Percentage rules are interpreted as an additional percentage of the
        supplied base amount.

        Multiplier rules are interpreted as a total compensation multiplier,
        where the base amount is multiplied by the rule value and the base
        amount itself is not added again as part of the premium.

        For example:

            base_amount = 100
            percentage rule = 30%

        produces:

            premium = 30

        While:

            base_amount = 100
            multiplier rule = 1.30

        produces:

            premium = 30

        Multiple applicable rules are accumulated according to the rules
        already resolved by AttendancePremiumRuleResolutionService.
        """

        if base_amount < Decimal("0"):
            raise ValueError(
                "base_amount cannot be negative.",
            )

        if not rules:
            return AttendancePremiumCalculation(
                base_amount=base_amount,
                premium_amount=Decimal("0"),
                total_amount=base_amount,
            )

        premium_amount = Decimal("0")

        for rule in rules:
            premium_amount += self._calculate_rule_premium(
                base_amount=base_amount,
                rule=rule,
            )

        total_amount = base_amount + premium_amount

        return AttendancePremiumCalculation(
            base_amount=base_amount,
            premium_amount=premium_amount,
            total_amount=total_amount,
        )

    def _calculate_rule_premium(
        self,
        *,
        base_amount: Decimal,
        rule: AttendancePremiumRule,
    ) -> Decimal:
        """
        Calculate the premium contribution of a single rule.
        """

        if rule.calculation_type == (AttendancePremiumCalculationType.PERCENTAGE):
            return self._calculate_percentage_premium(
                base_amount=base_amount,
                percentage=rule.value,
            )

        if rule.calculation_type == (AttendancePremiumCalculationType.MULTIPLIER):
            return self._calculate_multiplier_premium(
                base_amount=base_amount,
                multiplier=rule.value,
            )

        raise ValueError(
            f"Unsupported premium calculation type: {rule.calculation_type!s}",
        )

    @staticmethod
    def _calculate_percentage_premium(
        *,
        base_amount: Decimal,
        percentage: Decimal,
    ) -> Decimal:
        """
        Calculate a percentage-based premium.
        """

        return base_amount * percentage / Decimal("100")

    @staticmethod
    def _calculate_multiplier_premium(
        *,
        base_amount: Decimal,
        multiplier: Decimal,
    ) -> Decimal:
        """
        Calculate the premium portion represented by a multiplier.

        Only the amount above the original base amount is returned as the
        premium.

        Example:

            base_amount = 100
            multiplier = 1.30

            total = 130
            premium = 30
        """

        return base_amount * (multiplier - Decimal("1"))
