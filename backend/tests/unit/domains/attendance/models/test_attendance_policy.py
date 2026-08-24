"""
===============================================================================
Quantum Workforce OS (QWOS)

Test:
    AttendancePolicy domain model

Author:
    Richard Balabarcon
===============================================================================
"""

import pytest

from qwos.domains.attendance.models.attendance_policy import (
    AttendancePolicy,
)

TENANT_ID = "01M0TEN00000000000000000001"
POLICY_ID = "01M0ATP00000000000000000001"


def test_create_normalizes_policy_values() -> None:
    policy = AttendancePolicy.create(
        id=POLICY_ID,
        tenant_id=TENANT_ID,
        policy_code=" MONTHLY_TRACKED ",
        policy_name=" Monthly Attendance Tracking ",
        attendance_requirement=" TRACKING_ONLY ",
    )

    assert policy.policy_code == "monthly_tracked"
    assert (
        policy.policy_name
        == "Monthly Attendance Tracking"
    )
    assert (
        policy.attendance_requirement
        == "tracking_only"
    )


def test_create_defaults_clocking_and_payroll_flags() -> None:
    policy = AttendancePolicy.create(
        id=POLICY_ID,
        tenant_id=TENANT_ID,
        policy_code="STANDARD",
        policy_name="Standard Attendance",
    )

    assert policy.clock_in_required is True
    assert policy.clock_out_required is True
    assert policy.payroll_impact_enabled is False
    assert policy.overtime_enabled is False
    assert policy.undertime_enabled is False
    assert policy.late_deduction_enabled is False
    assert policy.grace_period_minutes == 0


def test_create_allows_tracking_only_without_payroll_impact() -> None:
    policy = AttendancePolicy.create(
        id=POLICY_ID,
        tenant_id=TENANT_ID,
        policy_code="MONTHLY_TRACKED",
        policy_name="Monthly Attendance Tracking",
        attendance_requirement="tracking_only",
        payroll_impact_enabled=False,
        clock_in_required=True,
        clock_out_required=True,
    )

    assert (
        policy.attendance_requirement
        == "tracking_only"
    )
    assert policy.payroll_impact_enabled is False
    assert policy.clock_in_required is True
    assert policy.clock_out_required is True


def test_create_rejects_invalid_attendance_requirement() -> None:
    with pytest.raises(
        ValueError,
        match="attendance_requirement must be one of",
    ):
        AttendancePolicy.create(
            id=POLICY_ID,
            tenant_id=TENANT_ID,
            policy_code="INVALID",
            policy_name="Invalid Policy",
            attendance_requirement="something_else",
        )


def test_create_rejects_negative_grace_period() -> None:
    with pytest.raises(
        ValueError,
        match="grace_period_minutes cannot be negative",
    ):
        AttendancePolicy.create(
            id=POLICY_ID,
            tenant_id=TENANT_ID,
            policy_code="INVALID_GRACE",
            policy_name="Invalid Grace Policy",
            grace_period_minutes=-1,
        )


def test_create_rejects_empty_policy_code() -> None:
    with pytest.raises(
        ValueError,
        match="policy_code is required",
    ):
        AttendancePolicy.create(
            id=POLICY_ID,
            tenant_id=TENANT_ID,
            policy_code="   ",
            policy_name="Policy",
        )


def test_create_rejects_empty_policy_name() -> None:
    with pytest.raises(
        ValueError,
        match="policy_name is required",
    ):
        AttendancePolicy.create(
            id=POLICY_ID,
            tenant_id=TENANT_ID,
            policy_code="POLICY",
            policy_name="   ",
        )