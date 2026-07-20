"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    authentication_service.py

Description:
    Service responsible for authentication.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Any
from qwos.core.services.base_service import BaseService
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)


class AuthenticationService(BaseService):
    """
    Business service responsible for authentication.
    """

    def __init__(
        self,
        users: UserRepository,
    ) -> None:
        super().__init__()

        self._users = users

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> Any:
        """
        Authenticate a user.
        """
        raise NotImplementedError()

    async def logout(
        self,
        user_id: str,
    ) -> None:
        """
        Log a user out.
        """
        raise NotImplementedError()

    async def refresh_token(
        self,
        refresh_token: str,
    ) -> Any:
        """
        Refresh an access token.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------
    # Password Management
    # ------------------------------------------------------------------

    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ) -> None:
        """
        Change a user's password.
        """
        raise NotImplementedError()

    async def request_password_reset(
        self,
        email: str,
    ) -> None:
        """
        Request a password reset.
        """
        raise NotImplementedError()

    async def reset_password(
        self,
        token: str,
        new_password: str,
    ) -> None:
        """
        Reset a user's password.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------
    # Account Management
    # ------------------------------------------------------------------

    async def verify_email(
        self,
        token: str,
    ) -> None:
        """
        Verify a user's email address.
        """
        raise NotImplementedError()

    async def lock_account(
        self,
        user_id: str,
    ) -> None:
        """
        Lock a user account.
        """
        raise NotImplementedError()

    async def unlock_account(
        self,
        user_id: str,
    ) -> None:
        """
        Unlock a user account.
        """
        raise NotImplementedError()
