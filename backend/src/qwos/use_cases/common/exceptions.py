"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    exceptions.py

Description:
    Application layer exceptions.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations


class ApplicationException(Exception):
    """
    Base application exception.
    """


class ValidationException(ApplicationException):
    """
    Raised when validation fails.
    """


class AuthorizationException(ApplicationException):
    """
    Raised when authorization fails.
    """


class AuthenticationException(ApplicationException):
    """
    Raised when authentication fails.
    """


class ResourceNotFoundException(ApplicationException):
    """
    Raised when a requested resource does not exist.
    """


class BusinessRuleViolationException(ApplicationException):
    """
    Raised when a business rule is violated.
    """


class ConcurrencyException(ApplicationException):
    """
    Raised when optimistic concurrency fails.
    """


class InfrastructureException(ApplicationException):
    """
    Raised when an infrastructure dependency fails.
    """
