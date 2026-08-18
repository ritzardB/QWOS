"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Port

File:
    document_filename_generator.py

Description:
    Contract for generating standardized QWOS document filenames.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Protocol


class DocumentFilenameGenerator(Protocol):
    """
    Generates standardized QWOS document filenames.
    """

    def generate(
        self,
        *,
        employee_number: str,
        document_category: str,
        issue_date: date | None,
        expiry_date: date | None,
        version: int,
        extension: str,
    ) -> str:
        """
        Generate a standardized stored filename.
        """
        ...