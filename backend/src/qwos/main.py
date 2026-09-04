"""
===============================================================================
Quantum Workforce OS (QWOS)

File:
    main.py

Description:
    FastAPI application entry point.

Author:
    Richard Balabarcon

===============================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from qwos.api.exception_handlers.application_exception_handler import (
    application_exception_handler,
)
from qwos.api.router import api_router
from qwos.application.common.exceptions.application_exception import (
    ApplicationException,
)

app = FastAPI(
    title="Quantum Workforce OS",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    ApplicationException,
    application_exception_handler,
)

app.include_router(api_router)
