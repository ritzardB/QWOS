"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Duplicate Resource Exception
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.business_rule_exception import (
    BusinessRuleException,
)


class DuplicateResourceException(BusinessRuleException):
    """
    Raised when a duplicate resource already exists.
    """

    def __init__(
        self,
        *,
        resource: str,
        field: str,
        value: str,
    ) -> None:
        super().__init__(
            f"{resource} with {field} '{value}' already exists."
        )

        self.resource = resource
        self.field = field
        self.value = value