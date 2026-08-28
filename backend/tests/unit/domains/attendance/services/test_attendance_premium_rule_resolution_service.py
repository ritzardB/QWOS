"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    attendance_premium_rule_resolution_service.py

Description:
    Resolves applicable attendance premium rules from pay classifications.

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
    AttendancePremiumRuleType,
)


class AttendancePremiumRuleResolutionService:
    """
    Resolve premium rules applicable to an attendance pay classification.

    The service is responsible only for determining which configured rules
    apply. It does not calculate monetary values.
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

        Multiple premium classifications may apply simultaneously. For
        example, a worked period may qualify for both night differential
        and overtime.

        Exclusive rules take precedence within their applicable rule type.
        When multiple exclusive rules of the same type apply, the highest
        priority rule is selected. Rule code is used as a deterministic
        tie-breaker.

        Stackable rules remain applicable unless overridden by a higher
        priority exclusive rule of the same type.

        Results are ordered by descending priority and then rule code.
        """

        applicable_types = self._get_applicable_rule_types(
            classification,
        )

        if not applicable_types:
            return []

        applicable_rules = [
            rule
            for rule in rules
            if rule.rule_type in applicable_types
            and rule.applies_on(effective_date)
        ]

        if not applicable_rules:
            return []

        resolved_rules: list[AttendancePremiumRule] = []

        for rule_type in applicable_types:
            type_rules = [
                rule
                for rule in applicable_rules
                if rule.rule_type == rule_type
            ]

            if not type_rules:
                continue

            resolved_rules.extend(
                self._resolve_rule_type(type_rules),
            )

        return sorted(
            resolved_rules,
            key=lambda rule: (
                -rule.priority,
                rule.rule_code,
            ),
        )

    @staticmethod
    def _get_applicable_rule_types(
        classification: AttendancePayClassification,
    ) -> set[AttendancePremiumRuleType]:
        """
        Translate pay classification flags into applicable premium types.
        """

        rule_types: set[AttendancePremiumRuleType] = set()

        if classification.is_night_differential:
            rule_types.add(
                AttendancePremiumRuleType.NIGHT_DIFFERENTIAL,
            )

        if classification.is_holiday:
            rule_types.add(
                AttendancePremiumRuleType.REGULAR_HOLIDAY,
            )

        if classification.is_rest_day:
            rule_types.add(
                AttendancePremiumRuleType.REST_DAY,
            )

        if classification.is_overtime:
            rule_types.add(
                AttendancePremiumRuleType.OVERTIME,
            )

        return rule_types

    @staticmethod
    def _resolve_rule_type(
        rules: list[AttendancePremiumRule],
    ) -> list[AttendancePremiumRule]:
        """
        Resolve rules belonging to a single premium type.

        If an exclusive rule exists, only the highest-priority exclusive
        rule is retained. Otherwise, all stackable rules are retained.

        Rule code provides deterministic ordering when priorities are equal.
        """

        exclusive_rules = [
            rule
            for rule in rules
            if rule.is_exclusive
        ]

        stackable_rules = [
            rule
            for rule in rules
            if not rule.is_exclusive
        ]

        if not exclusive_rules:
            return sorted(
                stackable_rules,
                key=lambda rule: (
                    -rule.priority,
                    rule.rule_code,
                ),
            )

        selected_exclusive = min(
            exclusive_rules,
            key=lambda rule: (
                -rule.priority,
                rule.rule_code,
            ),
        )

        return [selected_exclusive]