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

app = FastAPI(
    title="Quantum Workforce OS API",
    description="Enterprise Workforce Management Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to Quantum Workforce OS API"
    }


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "Quantum Workforce OS API",
        "version": "0.1.0",
    }