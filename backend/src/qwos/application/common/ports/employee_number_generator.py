"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Employee Number Generator Port

Description:
    Application-layer contract for generating tenant-specific employee
    numbers.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmployeeNumberGenerator(ABC):
    """
    Port for generating tenant-specific employee numbers.
    """

    @abstractmethod
    def generate(
        self,
        *,
        tenant_id: str,
    ) -> str:
        """
        Generate and reserve the next employee number for a tenant.

        Args:
            tenant_id: Tenant owning the employee number sequence.

        Returns:
            A unique employee number such as ``QW-00001``.
        """
        raise NotImplementedError