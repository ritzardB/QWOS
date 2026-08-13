"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Repository Contract

User Profile Repository

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.identity.models.user_profile import UserProfile


class UserProfileRepository(Protocol):
    """
    Contract for UserProfile persistence.
    """

    # ------------------------------------------------------------------
    # Base Operations
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        profile_id: str,
    ) -> UserProfile | None:
        ...

    def save(
        self,
        profile: UserProfile,
    ) -> None:
        ...

    # ------------------------------------------------------------------
    # User Profile Queries
    # ------------------------------------------------------------------

    def get_by_user_id(
        self,
        user_id: str,
    ) -> UserProfile | None:
        """
        Retrieve a profile by user id.
        """
        ...

    def exists_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        """
        Determine whether a profile exists.
        """
        ...