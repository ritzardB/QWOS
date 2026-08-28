"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    test_attendance_premium_calculation.py

Description:
    Unit tests for AttendancePremiumCalculation.

Author:
    Richard Balabarcon
===============================================================================
"""

from decimal import Decimal

import pytest

from qwos.domains.attendance.models.attendance_premium_calculation import (
    AttendancePremiumCalculation,
    AttendancePremiumCalculationType,
)


def make_calculation(
    *,
    rule_code: str = "NIGHT_10",
    calculation_type: AttendancePremiumCalculationType = (
        AttendancePremiumCalculationType.PERCENTAGE
    ),
    base_amount: str = "1000",
    rule_value: str = "10",
    premium_amount: str = "100",
) -> AttendancePremiumCalculation:
    """
    Create a valid premium calculation for testing.
    """

    return AttendancePremiumCalculation(
        rule_code=rule_code,
        calculation_type=calculation_type,
        base_amount=Decimal(base_amount),
        rule_value=Decimal(rule_value),
        premium_amount=Decimal(premium_amount),
    )


def test_calculation_stores_values() -> None:
    calculation = make_calculation()

    assert calculation.rule_code == "NIGHT_10"
    assert (
        calculation.calculation_type
        == AttendancePremiumCalculationType.PERCENTAGE
    )
    assert calculation.base_amount == Decimal("1000")
    assert calculation.rule_value == Decimal("10")
    assert calculation.premium_amount == Decimal("100")


def test_calculation_is_frozen() -> None:
    calculation = make_calculation()

    with pytest.raises(AttributeError):
        calculation.base_amount = Decimal("2000")  # type: ignore[misc]


def test_percentage_calculation() -> None:
    calculation = make_calculation(
        calculation_type=AttendancePremiumCalculationType.PERCENTAGE,
        rule_value="10",
        premium_amount="100",
    )

    assert calculation.is_percentage is True
    assert calculation.is_multiplier is False


def test_multiplier_calculation() -> None:
    calculation = make_calculation(
        calculation_type=AttendancePremiumCalculationType.MULTIPLIER,
        rule_value="1.25",
        premium_amount="250",
    )

    assert calculation.is_multiplier is True
    assert calculation.is_percentage is False


def test_total_amount_adds_base_and_premium() -> None:
    calculation = make_calculation(
        base_amount="1000",
        premium_amount="100",
    )

    assert calculation.total_amount == Decimal("1100")


def test_total_amount_supports_decimal_precision() -> None:
    calculation = make_calculation(
        base_amount="1234.56",
        premium_amount="123.456",
    )

    assert calculation.total_amount == Decimal("1358.016")


def test_empty_rule_code_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="rule_code cannot be empty",
    ):
        make_calculation(rule_code="   ")


def test_negative_base_amount_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="base_amount cannot be negative",
    ):
        make_calculation(base_amount="-1")


def test_negative_rule_value_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="rule_value cannot be negative",
    ):
        make_calculation(rule_value="-1")


def test_negative_premium_amount_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="premium_amount cannot be negative",
    ):
        make_calculation(premium_amount="-1")


def test_percentage_rule_value_cannot_exceed_100() -> None:
    with pytest.raises(
        ValueError,
        match="percentage rule_value cannot exceed 100",
    ):
        make_calculation(
            calculation_type=AttendancePremiumCalculationType.PERCENTAGE,
            rule_value="100.01",
        )


def test_percentage_rule_value_of_100_is_valid() -> None:
    calculation = make_calculation(
        calculation_type=AttendancePremiumCalculationType.PERCENTAGE,
        rule_value="100",
        premium_amount="1000",
    )

    assert calculation.rule_value == Decimal("100")
    assert calculation.is_percentage is True


def test_multiplier_can_exceed_one() -> None:
    calculation = make_calculation(
        calculation_type=AttendancePremiumCalculationType.MULTIPLIER,
        rule_value="2.00",
        premium_amount="1000",
    )

    assert calculation.rule_value == Decimal("2.00")
    assert calculation.is_multiplier is True


def test_zero_values_are_valid() -> None:
    calculation = make_calculation(
        base_amount="0",
        rule_value="0",
        premium_amount="0",
    )

    assert calculation.base_amount == Decimal("0")
    assert calculation.rule_value == Decimal("0")
    assert calculation.premium_amount == Decimal("0")
    assert calculation.total_amount == Decimal("0")


def test_total_amount_for_multiplier_example() -> None:
    calculation = make_calculation(
        calculation_type=AttendancePremiumCalculationType.MULTIPLIER,
        base_amount="2000",
        rule_value="1.25",
        premium_amount="500",
    )

    assert calculation.total_amount == Decimal("2500")