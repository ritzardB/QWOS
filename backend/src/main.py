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

from qwos.api.router import api_router

app = FastAPI(
    title="Quantum Workforce OS",
    version="1.0.0",
)

app.include_router(api_router)