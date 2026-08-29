"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Port

File:
    document_storage_key_generator.py

Description:
    Contract for generating standardized QWOS document storage keys.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol


class DocumentStorageKeyGenerator(Protocol):
    """
    Generates standardized QWOS document storage keys.
    """

    def generate(
        self,
        *,
        employee_number: str,
        document_category: str,
        stored_filename: str,
    ) -> str:
        """
        Generate a storage key for a document.
        """
        ...
