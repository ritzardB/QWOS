"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_premium_rule_resolution_service.py

Description:
    Resolves applicable attendance premium rules for a classified
    attendance segment.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from qwos.domains.attendance.models.attendance_pay_classification import (
    AttendancePayClassification,
)
from qwos.domains.attendance.models.attendance_premium_rule import (
    AttendancePremiumRule,
    AttendancePremiumStackingStrategy,
)


class AttendancePremiumRuleResolutionService:
    """
    Resolves premium rules applicable to an attendance classification.

    This service determines WHICH premium rules apply. It deliberately does
    not calculate monetary compensation.
    """

    def resolve(
        self,
        *,
        classification: AttendancePayClassification,
        rules: list[AttendancePremiumRule],
        effective_date: date,
    ) -> list[AttendancePremiumRule]:
        """
        Return the premium rules applicable to a classification.

        Rules that are inactive or outside their effective date range are
        ignored.

        If one or more exclusive rules apply, only the highest-priority
        exclusive rule is returned together with applicable stacking rules.

        Otherwise, all applicable stacking rules are returned.

        Results are ordered by descending priority.
        """

        applicable_rules = [
            rule for rule in rules if rule.rule_type == classification.rule_type and rule.applies_on(effective_date)
        ]

        if not applicable_rules:
            return []

        exclusive_rules = [
            rule for rule in applicable_rules if (rule.stacking_strategy == AttendancePremiumStackingStrategy.EXCLUSIVE)
        ]

        stacking_rules = [
            rule for rule in applicable_rules if (rule.stacking_strategy == AttendancePremiumStackingStrategy.STACK)
        ]

        if exclusive_rules:
            highest_priority_exclusive = max(
                exclusive_rules,
                key=lambda rule: rule.priority,
            )

            applicable_rules = [
                highest_priority_exclusive,
                *stacking_rules,
            ]
        else:
            applicable_rules = stacking_rules

        return sorted(
            applicable_rules,
            key=lambda rule: rule.priority,
            reverse=True,
        )
