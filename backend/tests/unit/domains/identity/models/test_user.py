"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Tests for User Entity
===============================================================================
"""

from qwos.core.database.base import BaseEntity
from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.enums.authentication_provider import (
    AuthenticationProvider,
)
from qwos.domains.identity.enums.user_type import UserType
from qwos.domains.identity.models.user import User


def test_user_table_name() -> None:
    """User should map to the users table."""

    assert User.__tablename__ == "users"


def test_user_inherits_base_entity() -> None:
    """User should inherit from BaseEntity."""

    assert issubclass(User, BaseEntity)


def test_create_user_instance() -> None:
    """User instance should be created successfully."""

    user = User(
        tenant_id="01HXXXXXXXXXXXXXXXABCDEFG",
        email="john.doe@example.com",
    )

    assert user.email == "john.doe@example.com"
    assert user.tenant_id == "01HXXXXXXXXXXXXXXXABCDEFG"


def test_default_account_status() -> None:
    """Default account status should be PENDING."""

    user = User(
        tenant_id="01HXXXXXXXXXXXXXXXABCDEFG",
        email="john.doe@example.com",
    )

    assert user.account_status == AccountStatus.PENDING


def test_default_authentication_provider() -> None:
    """Default authentication provider should be LOCAL."""

    user = User(
        tenant_id="01HXXXXXXXXXXXXXXXABCDEFG",
        email="john.doe@example.com",
    )

    assert (
        user.authentication_provider
        == AuthenticationProvider.LOCAL
    )


def test_default_user_type() -> None:
    """Default user type should be EMPLOYEE."""

    user = User(
        tenant_id="01HXXXXXXXXXXXXXXXABCDEFG",
        email="john.doe@example.com",
    )

    assert user.user_type == UserType.EMPLOYEE


def test_default_failed_login_attempts() -> None:
    """Failed login attempts should default to zero."""

    user = User(
        tenant_id="01HXXXXXXXXXXXXXXXABCDEFG",
        email="john.doe@example.com",
    )

    assert user.failed_login_attempts == 0


def test_nullable_fields() -> None:
    """Nullable fields should default to None."""

    user = User(
        tenant_id="01HXXXXXXXXXXXXXXXABCDEFG",
        email="john.doe@example.com",
    )

    assert user.password_hash is None
    assert user.email_verified_at is None
    assert user.last_login_at is None
    assert user.password_changed_at is None