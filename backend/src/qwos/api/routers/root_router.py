from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    """
    Root endpoint.
    """

    return {
        "application": "Quantum Workforce OS",
        "version": "1.0.0",
        "status": "running",
    }
