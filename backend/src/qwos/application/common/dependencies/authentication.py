"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Authenticated Request Dependencies

File:
    authentication.py

Description:
    Provides authenticated request identity from the JWT bearer token.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import logging
from uuid import uuid4

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.common import get_token_provider
from qwos.application.common.ports.token_provider import TokenProvider


logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)


async def get_authenticated_request_context(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_provider: TokenProvider = Depends(get_token_provider),
) -> RequestContext:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    if not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = await token_provider.validate_token(token.strip())
    except Exception as exc:
        logger.exception(
            "AUTH DEBUG: JWT validation failed: %s",
            exc,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    logger.warning(
        "AUTH DEBUG: JWT payload type=%r sub=%r tenant_id=%r session_id=%r",
        payload.get("type"),
        payload.get("sub"),
        payload.get("tenant_id"),
        payload.get("session_id"),
    )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")

    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not isinstance(tenant_id, str) or not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token tenant.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return RequestContext(
        tenant_id=tenant_id,
        user_id=user_id,
        correlation_id=request.headers.get(
            "X-Correlation-ID",
            str(uuid4()),
        ),
        request_id=request.headers.get(
            "X-Request-ID",
            str(uuid4()),
        ),
        locale=request.headers.get(
            "Accept-Language",
            "en-US",
        ),
        timezone="UTC",
        ip_address=(
            request.client.host
            if request.client is not None
            else None
        ),
        user_agent=request.headers.get("User-Agent"),
    )