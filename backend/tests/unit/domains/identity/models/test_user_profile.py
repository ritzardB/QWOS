"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Tests for UserProfile Entity
===============================================================================
"""

from qwos.core.database.base import BaseEntity
from qwos.domains.identity.models.user_profile import UserProfile


def build_profile() -> UserProfile:
    """Create a valid UserProfile instance for testing."""

    return UserProfile(
        tenant_id="01HXXXXXXXXXXXXXXXABCDEFG",
        user_id="01HYYYYYYYYYYYYYYYHIJKLMN",
        first_name="Richard",
        last_name="Balabarcon",
        display_name="Richard Balabarcon",
    )


def test_user_profile_table_name() -> None:
    """UserProfile should map to the user_profiles table."""

    assert UserProfile.__tablename__ == "user_profiles"


def test_user_profile_inherits_base_entity() -> None:
    """UserProfile should inherit from BaseEntity."""

    assert issubclass(UserProfile, BaseEntity)


def test_create_user_profile_instance() -> None:
    """A valid UserProfile instance should be created."""

    profile = build_profile()

    assert profile.first_name == "Richard"
    assert profile.last_name == "Balabarcon"
    assert profile.display_name == "Richard Balabarcon"


def test_default_locale() -> None:
    """Locale should default to en-US."""

    profile = build_profile()

    assert profile.locale == "en-US"


def test_default_language_code() -> None:
    """Language should default to English."""

    profile = build_profile()

    assert profile.language_code == "en"


def test_default_timezone() -> None:
    """Timezone should default to UTC."""

    profile = build_profile()

    assert profile.timezone == "UTC"


def test_optional_fields_are_none() -> None:
    """Optional fields should default to None."""

    profile = build_profile()

    assert profile.middle_name is None
    assert profile.preferred_name is None
    assert profile.avatar_url is None
