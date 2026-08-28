"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_attendance_premium_rule.py

Description:
    Unit tests for AttendancePremiumRule domain model.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from qwos.domains.attendance.models.attendance_premium_rule import (
    AttendancePremiumCalculationType,
    AttendancePremiumRule,
    AttendancePremiumRuleType,
    AttendancePremiumStackingStrategy,
)


def make_rule(
    *,
    rule_code: str = "NIGHT_DIFF",
    rule_type: AttendancePremiumRuleType = (
        AttendancePremiumRuleType.NIGHT_DIFFERENTIAL
    ),
    calculation_type: AttendancePremiumCalculationType = (
        AttendancePremiumCalculationType.PERCENTAGE
    ),
    value: Decimal = Decimal("10"),
    stacking_strategy: AttendancePremiumStackingStrategy = (
        AttendancePremiumStackingStrategy.STACK
    ),
    priority: int = 0,
    effective_from: date | None = None,
    effective_until: date | None = None,
    is_active: bool = True,
) -> AttendancePremiumRule:
    return AttendancePremiumRule(
        rule_code=rule_code,
        rule_type=rule_type,
        calculation_type=calculation_type,
        value=value,
        stacking_strategy=stacking_strategy,
        priority=priority,
        effective_from=effective_from,
        effective_until=effective_until,
        is_active=is_active,
    )


def test_create_valid_percentage_rule() -> None:
    rule = make_rule(
        value=Decimal("10"),
    )

    assert rule.rule_code == "NIGHT_DIFF"
    assert rule.rule_type == AttendancePremiumRuleType.NIGHT_DIFFERENTIAL
    assert (
        rule.calculation_type
        == AttendancePremiumCalculationType.PERCENTAGE
    )
    assert rule.value == Decimal("10")
    assert rule.stacking_strategy == AttendancePremiumStackingStrategy.STACK
    assert rule.priority == 0
    assert rule.is_active is True


def test_create_valid_multiplier_rule() -> None:
    rule = make_rule(
        rule_code="REGULAR_HOLIDAY",
        rule_type=AttendancePremiumRuleType.REGULAR_HOLIDAY,
        calculation_type=AttendancePremiumCalculationType.MULTIPLIER,
        value=Decimal("2.00"),
    )

    assert rule.is_multiplier is True
    assert rule.is_percentage is False
    assert rule.value == Decimal("2.00")


def test_empty_rule_code_is_rejected() -> None:
    with pytest.raises(ValueError, match="rule_code cannot be empty"):
        make_rule(rule_code="   ")


def test_negative_value_is_rejected() -> None:
    with pytest.raises(ValueError, match="value cannot be negative"):
        make_rule(value=Decimal("-1"))


def test_percentage_above_100_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="percentage value cannot exceed 100",
    ):
        make_rule(value=Decimal("100.01"))


def test_negative_priority_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="priority cannot be negative",
    ):
        make_rule(priority=-1)


def test_invalid_effective_date_range_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="effective_until cannot be earlier than effective_from",
    ):
        make_rule(
            effective_from=date(2026, 12, 31),
            effective_until=date(2026, 1, 1),
        )


def test_inactive_rule_does_not_apply() -> None:
    rule = make_rule(
        is_active=False,
    )

    assert rule.applies_on(date(2026, 9, 1)) is False


def test_rule_before_effective_from_does_not_apply() -> None:
    rule = make_rule(
        effective_from=date(2026, 9, 1),
    )

    assert rule.applies_on(date(2026, 8, 31)) is False


def test_rule_after_effective_until_does_not_apply() -> None:
    rule = make_rule(
        effective_from=date(2026, 9, 1),
        effective_until=date(2026, 12, 31),
    )

    assert rule.applies_on(date(2027, 1, 1)) is False


def test_rule_applies_on_effective_boundaries() -> None:
    rule = make_rule(
        effective_from=date(2026, 9, 1),
        effective_until=date(2026, 12, 31),
    )

    assert rule.applies_on(date(2026, 9, 1)) is True
    assert rule.applies_on(date(2026, 12, 31)) is True


def test_stack_and_exclusive_behavior() -> None:
    stack_rule = make_rule(
        stacking_strategy=AttendancePremiumStackingStrategy.STACK,
    )

    exclusive_rule = make_rule(
        stacking_strategy=AttendancePremiumStackingStrategy.EXCLUSIVE,
    )

    assert stack_rule.is_exclusive is False
    assert exclusive_rule.is_exclusive is True


def test_percentage_and_multiplier_properties() -> None:
    percentage_rule = make_rule(
        calculation_type=AttendancePremiumCalculationType.PERCENTAGE,
        value=Decimal("10"),
    )

    multiplier_rule = make_rule(
        calculation_type=AttendancePremiumCalculationType.MULTIPLIER,
        value=Decimal("2.00"),
    )

    assert percentage_rule.is_percentage is True
    assert percentage_rule.is_multiplier is False

    assert multiplier_rule.is_percentage is False
    assert multiplier_rule.is_multiplier is True